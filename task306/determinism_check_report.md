# determinism-check report, task306, 2026-10-24

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet judge thread (scratch /tmp/determinism-check-task306-1792824984/, verdict.md there) executed the prompt and the tooling plan word for word. The estimand is "pack fails in 2027 on a car in use in the Netherlands, OEM warranty ended", which includes used imports not yet arrived. The warranty PDF (first admission anywhere in the EU) and the RDW field sheet (first admission "in the Netherlands or elsewhere") support it. Soft spot: the plan's "a car in use is taken to stay in use through 2027" can be read as freezing the 30 June register, but "in use in 2027" favours the golden. The judge called it forced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Register-car failures | 3,448 | 3,448.4 | yes |
| Import failures (Mira) | 363 (360) | 363.1 (359.8) | yes |
| Platform forecasts M/V/P/K/T | 1,829/1,144/425/322/91 | 1,828.9/1,144.5/425.5/322.1/90.5 | yes |
| Total to nearest 100 | 3,800 | 3,811 -> 3,800 | yes |
| Slots | 1,450/900/350/250/50 | same | yes |
| Ask 3 modules per 50 (V/K/P/M/T) | 167/274/190/149/224 | 167.1/274.3/189.7/149.2/223.8 | yes |
| Ask 4 first-run pass share | 92.6/88.2/94.0/88.3/90.5 | identical | yes |
| Ask 5 intake reject share | 8.9/5.9/11.0/14.7/8.3 | 8.91/5.92/10.99/14.70/8.33 | yes |

## Competing answers that survived
None on the main call. Sensitivity (age divisor 365/365.2425, import rate +-10%, last-6-month rate, taxis excluded) leaves the slots unchanged. Only a -15% import rate moves them (Tern 100, Mira 1,400). The total sits 39 below the 3,850 rounding edge; a rate about +10% would round to 3,900, but yearly import counts are stable (1,205 to 1,389), so that is not a reasonable estimate.
Traps, not forks: register only (3,400; 1,250/1,000/350/300/100); unconditional hazard (about 2,700; 1,300/900/400/300/100).
Asks: ask 3 without the pick-list dedupe (283/150/195/238/171) is contradicted by eight supplier lots whose receipts the dedupe reproduces exactly. Ask 4 per pakket_id (87.2/88.0/94.2/91.3/92.3) is contradicted by the toelichting (BMS swap gives a new pakket_id). Ask 5: the dock-2 "does not scan rejects" fact is in no shipped file and is recoverable only by inference from the data (see Findings).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | csv, xlsx, pdf, docx, md | yes |
| Large file | 25,000 rows or more | rdw_gekentekende_voertuigen 88,128 rows | yes |
| Distractors in metadata.json, none named by file | 2 or more | prijslijst_revisiepakketten_2026.pdf, module_levertijden_2026.xlsx; file names do not label them | yes |
| Distractors unused yet weighable, none answering a graded quantity | yes | price list and module lead times, not used in any golden figure; neither reproduces a graded quantity (judge found no arithmetic route) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 3 per-platform asks plus total and slots; prompt states hundred, whole modules, one decimal of a per cent | yes |
| Prompt shape and 25+ criteria | identifiable, 25 or more | shape "other" (slots plus sized demand plus per-lot measures); about 25 gradable figures (call, 5 slots, total, 15 platform shares/counts, chart items); at the floor, not independently counted | yes, thin |
| Not LLM-generated, goldens realistic | yes | judge found clean metadata, no authoring disclosure; golden realism not re-read here | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: strategy `maturity_censoring`, Gate G `forecasting`, decisive step the full import arrival stream (G13), nothing planted. Match. The declared distractors (price list, lead times) were not named as the surface read carrying the task. The thread's surface-read trap is the register-only split, which is the intended default path, not a shipped artifact ranking candidates wrongly. The ladder's "1,350 (either half of the stream)" fork in the note is not a literal-reading fork; the judge's rate/window sensitivities support the standing family. metadata.json carries no `stump_class`, `analyst_test` or `domain_test` keys; the card was not located in this pass, so the card side of the comparison is incomplete and the note's `## Three rules` was used instead.

## Gate H (the three rules)
domain: pass; layers: pass; decisive_step: analytical.
The thread's decisive step (carry the monthly import inflow into the 2027 pool with conditional hazard, rather than the 30 June register) matches the note's. Both Not-semantics and Not-rule-application lines in the note stand: no filed sentence rules out the register-only route, only the register's two date columns do. No decoy.

## Stump power (Gate F)
Moderate to good, per the thread. Two analytical traps move the call: the register-only population (Mira 1,250 to 1,450) and the unconditional hazard (understated total). The thread found no hint that imports keep arriving beyond the RDW "elsewhere" and warranty wording. The note's pre-draw probes (four of four missed the step) agree. The decisive step is not "the field's standard method applied with no judgment", so no landable-call discount applies. The asks add reconciliation traps (ask 3 dedupe, ask 5 dock 2).

## Findings, ranked
1. Soft spot: "a car in use is taken to stay in use through 2027" admits a register-frozen reading. The judge calls the golden forced; the real reviewer may see it as an open fork. Consider a closure sentence only if the main session wants more margin, and file the WHAT (population), not the HOW.
2. Ask 5: the dock-2 "does not scan rejects" fact appears in no shipped file; the 119 recycler lines enter numerator and denominator only by inference (the judge reached it from the data). A literal reader could leave them out (ask 5 then differs). Risk of an `answer_contradicts_files` reading on ask 5.
3. Hygiene: lijn_exports_toelichting.md says the exports were pulled on 1 July 2026, but afvoer_recycler_2025-26.xlsx has collections dated 8, 14 and 15 July 2026 (outside the window, non-decisional).
4. Total margin: 39 below the 3,850 rounding edge; slots margin 0.263 lots worst (Plover over Tern 0.27 in the judge's count).

## Next action for the author
Fix the toelichting pull date in the generator and, if wanted, state the dock-2 non-scanning fact in lijn_exports_toelichting.md (a fact about the data, not the method), then rebuild; no re-judge is needed for the call.
