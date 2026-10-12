# determinism-check report, task230, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (method/model selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced by the shipped files. QCP-04 section 4 fixes the estimand (stream residual over its own routed November documents, blind re-key as truth), the rule (over limit only if strictly greater) and one method for every stream. The log joined to the audit shows the miss rate falling as the queue's shift-day OCR error rate rises. The plan moves Thistlecombe to nights and adds Hollings & Pryce to days, so the day rate falls from 4.3% to 1.85% and the night rate rises from 2.5% to 5.17%. The over-limit set is BMC-FROI, WBH-EXTR, CIP-IPCL, WPC-PETC and HPY-TYPD. The gap is wide (lowest in-set ratio about 1.16, highest outside about 0.78 to 0.83). No gate failed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Q3 day / night OCR rate | 4.3% / 2.5% | 4.32% / 2.49% | Yes |
| Nov day / night rate | 1.9% / 5.2% | 1.85% / 5.17% | Yes (rounds) |
| Slope on log queue rate | 0.63 | -0.625 | Yes in magnitude (sign not printed in the solution block) |
| Nov forecast ratios | 1.22, 1.26, 1.25, 1.26, 1.22; others 0.73 to 0.80 | 1.19, 1.23, 1.23, 1.25, 1.16; others 0.71 to 0.78 | Same calls; values differ by 0.03 to 0.06 (roster and verifier handling) |
| Hours, 11 streams | 985, 882, 771, 348, 589, 2035, 3097, 1139, 1731, 2217, 2526 | identical | Yes, all 11 |
| Slide order and title stream | EXTR, HPY, TCM, HOSP, WPC, CIP, INST, PROF, NDS, HPB, BMC | identical | Yes |
| Residuals KBA-INST, KBA-PROF, NDS-DENT, BMC-FROI, HPB-UCF | 0.14, 0.97, 1.29, 1.45, 0.19 | identical | Yes |
| Residuals WBH-HOSP, WBH-EXTR, CIP-IPCL | 1.52, 3.89, 5.73 | 1.52, 3.89, 5.73 with spec-fill of pre-log documents; 1.52, 3.92, 5.79 log-only | Yes, only with the form-spec fill |
| Residuals WPC-PETC, TCM-FNOL | 4.27, 14.53 | identical | Yes |
| HPY-TYPD residual | none (audits start 2027) | supported by client_quality_schedules_2026.pdf | Yes |

## Competing answers that survived
None survives on the main call. Residual hazards on supplementary answers, not forks under a literal read:
1. Basket-based minutes per document instead of document-level stream: HPY-TYPD goes to 3,169 hours, above WBH-EXTR (3,097), which flips the slide title and order. The labour note's wording ("those documents", per-document stream) is the closing text. The judge calls the document-level reading natural.
2. Omitting pre-log documents' key fields: WBH-EXTR 3.92 and CIP-IPCL 5.79 instead of 3.89 and 5.73. The form specification closes it.
3. Per-line instead of per-distinct-document average: every hour value changes. The labour note's "divided by the number of those documents" closes it.
4. Queue-indicator or attribute forecast models give a different set (for example TCM-FNOL near 20 against its 18.9 limit). The data separates them (worse out-of-sample, queue term vanishes once the rate is in) but only through a back-test the solver runs.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 26 in the unzip | Yes |
| Formats | 3+ | 7 (parquet, csv, xlsx, docx, pdf, json, md) | Yes |
| Large file | 25,000+ rows | 2,381,352 rows (blind_rekey_audit); first_pass 1.26M, delivery_index 1.32M | Yes |
| Distractors | 2+, named in metadata.json, none labelled in file names | 7 named; no file name or content under target/ labels one (grep for distractor/decoy returned nothing) | Yes |
| Distractor relevance and ruling out | same world, rejected by a shipped fact | Client forecast files are superseded by the plan of record (labour note); telemetry and OCR summary are same-world, not used | Yes (judge found none decisive) |
| Deliverables | 1 to 3 | 2 (xlsx, pptx); both present in golden/ | Yes |
| Asks multi-dimensional | yes | 11 streams x call, hours, residual, plus the chart | Yes |
| Units and rounding stated | yes | whole hours, errors per 1,000 key fields, two decimals | Yes |
| Prompt shape and 25 criteria | shape identifiable, 25+ | shape 07 (grid); 11 x 3 cells plus slide and recommendation, well above 25 | Yes (arithmetic by count, not the generated rubric) |
| Realism | no LLM tells | Judge found none; the MIS notes read as an internal note | Yes (golden look not opened by me; golden-realism owns it) |

## Gate G reconciliation
Judge: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card claims stump_class analytical, and its driver is detection falling with pool error rate, so carrying each stream's measured miss rate forward clears breaching units and keeps non-breaching ones. The judge reads the same thing from outside: the naive set {KBA-INST, KBA-PROF, NDS-DENT, BMC-FROI, HPB-UCF} against the golden five (only BMC-FROI overlaps), with the pool error rate as the decisive step. Match. No declared distractor was named as carrying the task. The one difference in detail: the card's analyst test says the attribute-model route keeps night streams and motor claims on and leaves HPY off, and the judge's attribute-model variant gives a different set. Both are wrong against the golden.

## Stump power (Gate F)
Good. The naive answer and the golden are nearly disjoint, and the trap is analytic (rate-dependent detection and a diluted pilot), not a planted defect. A queue-indicator model gives a credible path to a miss. The judge rates the too-easy risk as low and the risk that no solver finds it as moderate.

## Gate H
domain: pass (low-prevalence detection, human reliability), layers: pass, decisive_step: analytical. Matches the card's domain_test and analyst_test.

## Findings, ranked
1. Low, solution blocks: print the slope sign (negative, -0.63 on log queue rate) and say that pre-log documents take key fields from form_specifications.xlsx. Answer-block edit only, no rerun.
2. Low, optional: the basket versus document-stream reading of "documents of the family's streams" can flip the slide title. Pinning it in second_pass_labour_planning_note.docx would change the bundle and invalidate the prior solver round, so only do it if the author wants the hazard gone.
3. Minor: the submission rounds forecast ratios 0.03 to 0.06 above the judge's own fit. The calls are unaffected and the gap is not a fork.

## Next action for the author
Ship. Optionally apply finding 1 to the submission.md answer blocks (no bundle change, no rerun).
