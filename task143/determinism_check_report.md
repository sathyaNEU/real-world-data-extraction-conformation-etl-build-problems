# Verdict, task143 (re-judge, fresh)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed and no rerun. Optional one-line pin only if the author wants extra margin (see Residual forks).

**Why:** Every committed answer reproduced from the shipped files. The reserve is forced by the policy's estimand (FIN-RS-04 3.2: the sum over packs of each pack's probability, with the pack failing on its weakest cell per spec rev D s4). The data then fixes the dependence structure: RL-3's error on the 20 finished lots is about 78% formation-tray, and 7,063 of 7,200 packs are three tray-mates. Every standard estimator lands on 394 to 402 packs, which rounds to 400. The 500 answer (independent cells, 514) is the easy route and is wrong on the data.

## Evidence (recomputed from target/)

| Item | Golden | Mine | Source |
|---|---|---|---|
| RL-3 features F1/F2 for 3,000 cells (fleet A cycle 0 is the first, fleet B cycle 1, 4,704 duplicate B rows dropped, 4 continued tests stitched incl. ZC2638-3111526 B 72 + A 28 = 100) | n/a | 3,000 cells, each with 100 cycles; refit of the b0/b1/b2 on the 2,373 EOL cells gives 8.7067/-0.4265/-0.0671 exactly | fleet_a, fleet_b, register, life results |
| RL-3 error RMSE, 2,373 EOL cells | 0.182 (LOLO) | 0.1814 in-sample, 0.1823 LOLO. Lot-mean errors match QM-07 Table 1 within 0.003 | life results |
| Error normal | stated | Shapiro p=0.37, skew -0.03, kurtosis -0.09 | same |
| Tray sd / cell sd / tray share | 0.160 / 0.086 / 78% | REML 0.1601 / 0.0856 / 77.7%; one-way ANOVA 0.1601; moments 0.1599; LOLO errors 0.1602 to 0.1609 | register tray key + life results |
| Lot-level residual effect | none implied | sd of lot-mean errors 0.0355 vs 0.0366 expected from tray sampling alone, so no separate lot effect | same |
| ZC2638 predictions | all outlive 600 | min pred life 702 cycles, median 887, none under 700 (release criterion met) | fleets + register |
| Pack structure | 7,063 / 136 / 1 | 7,063 three-tray-mate, 136 two-plus-one, 1 three-tray; 7,200 packs, 21,600 unique cells, none in Model J, none outside A-limits | model_k_genealogy x zelvora_cell_data |
| Reserve | 398.9 (5.5%) | 397.3 to 398.5 with sd 0.160/0.086 and empirical 120 predictions | policy 3.2, spec s4 |
| Independent-cell route | 514 | 7.14% a pack, 514.0 | QM-07 s5 RMSE |
| Partner counts | DVG 99, TMR 81, LJQ 58, FRC 79 | 99 / 81 / 58 / 79 (CAP, WTY, REPLACED, invoice service period Oct 2025 to Sep 2026, TM-2603-R1 replaces TM-2603, which is dropped with its duplicate TMJ117922 line) | invoices x service cases |
| Monthly totals | 8,17,23,25,26,39,41,51,57,56,74,71 = 488 | identical, all 12 months (DACH from SAP Techn. Abschluss to 1 Mar, then the case-system closing day, deduped on legacy_ref; partners by invoice period) | all |
| Average cost | 99 / 102 / 112 / 96 | 99.09 / 101.89 / 111.73 / 95.93 | invoices, treasury, carrier, returns log, cost sheet |

Cost build checked: invoice line (labour + handling) converted at the service-period month-end rate (cost sheet Costing tab). Freight is the carrier charge divided by pieces (pieces equal the returns-log rows for every consignment). The returns-log "Freight EUR" column repeats the full consignment charge on every row, so using it gives 149 to 159 and is wrong. Seven scrapped batteries have no row and zero freight. Service pack is 52.40 before 1 Jan 2026 and 49.80 after. Dropping the seven no-freight batteries from the mean still rounds to 99/102/112/96. Using case close date for the pack price also rounds the same.

## Competing answers stress-tested (Gate C)

- Reserve 500 (514), independent cells: loses to the tray structure in the data (78% tray variance). It is the intended easy route, not a defensible alternative.
- Reserve about 150, finished lots' own tray-mate packs as they lived: ignores RL-3, which policy 3.3 prescribes, and ignores this lot's lower predictions (mean predicted life about 888 against about 967 for the finished lots).
- Reserve 350 needs tray sd of about 0.1555 or less. Only ML with lot as a fixed effect gives 0.1559, which is a biased variance estimator. REML (the statsmodels/lme4 default), ANOVA and moments all give 0.160. Thin but clean.
- 450 would need sd above 0.1645. No reasonable estimator gets there. LOLO errors give 402, a parameter-uncertainty-integrated version 394, and a P(N<=600.5) edge 401. All round to 400.
- The 375 and 425 boundaries sit about 22 to 28 packs from the point estimate. I rate this thin but clean (all rigorous point estimators agree), not margin_or_boundary_fragility.

## Residual forks (low risk, none flips a committed answer under a reasonable reading)

1. Partner "carried out" date. Case-system closed_utc lags the invoice service period by 1 to 2 months for all 317 included partner jobs, and 49 invoiced replaced cases have no close date. Counting by closed_utc would give 277 partner replacements (DVG 88, FRC 69, LJQ 51, TMR 69) and different months. The invoice workbooks are "a line per job in the invoice's service period", and the cost sheet also keys on the invoice's service period, so the invoice reading is the better-supported one. The prompt does not say so in words. Optional prompt pin: "by the service period of the partner's invoice line".
2. Gauge cycles vs QP-3 cycles. Spec rev D s5 says the gauge adds one cycle per 4,820 mAh discharged, which would count fewer cycles than QP-3 as cells fade. FIN-RS-04 3.3 states they are the same cycles, so the policy closes it. A solver who rescales would shift the threshold and the reserve.
3. The monthly table is "across all five regions". The golden lists totals per month. The region split lives only in the chart. A grader could want it in the table too (a rubric concern, not a determinism one).

## Files/Hygiene: PASS

24 files, formats csv, xlsx, pdf, txt (4). Fleet A is 174,006 rows, fleet B 130,698, and the genealogy 21,600. Distractors present and unused: Model J genealogy, certificate of analysis, the DACH depot and Model J tabs, and the Sep 2025 invoice sheets. Layer 1 mess is real and not planted: semicolon and decimal-comma local-time fleet A against UTC fleet B, three serial formats, continued tests, overlapping weekly pulls, the SAP to case-system migration with legacy_ref, four-language partner invoices in EUR/GBP/SEK, a reissued invoice, the consignment-share freight. No authoring or benchmark language. No tool signatures in the PDFs. The xlsx authors are in-fiction. Dates are coherent: extracts of 5 to 12 October 2026, the last pack built 9 October, no decisive fact after the snapshot. No public-data contamination. No exclusion-level finding.

## Stump power (Gate F)

Strong. The reserve is 400 against a plausible 500 from the document's own RMSE of 0.182 and a normal per-cell tail, since the independence step looks innocuous. Nothing in the pack announces the tray correlation. The tray key appears only in the register note and the cell data. Reaching 400 needs the stitched features, a tray-level variance decomposition on the finished lots, and the genealogy join to formation trays. The 12-month tables add independent mess (reissue, dedupe, share-of-consignment freight).

## Stumping type (Gate G)

mechanism: statistical_rigor (clustering and variance components, plus etl_conformance in the asks) | stumping_family: analytical_non_defect | surface_read_dependency: no | sole_data_defect: no

The reported RMSE and normality are correct and nothing is misleading. The trap is ignoring the dependence among a pack's cells. On clean data it would still stump.

## Three rules (Gate H)

domain: pass | layers: pass (Layer 1 = two cycler exports, serial and time conventions, SAP/case migration, multilingual multi-currency invoices; Layer 2 = clustered-error variance components for a weakest-link pack) | decisive_step: analytical

Swap test: replacing the cell-life reliability work with another field's nouns breaks the task, because the deciding quantity is a pack-failure probability from a release-model's prediction error under a 3S weakest-cell rule. Easy route for a strong analyst who read everything: treat each cell's RL-3 error as independent with RMSE 0.182, giving 7.1% a pack, 514 packs, filed as 500. The data-correct answer is 400. No planted defect, no decoy, no hidden rule, and the semantics are closed by policy 3.2/3.3 and spec s4.

## Fix

none. Optional: add the invoice-service-period pin to the prompt (fork 1 above). It would not change the golden but would change what solvers see, so only do it if a rerun is acceptable.
