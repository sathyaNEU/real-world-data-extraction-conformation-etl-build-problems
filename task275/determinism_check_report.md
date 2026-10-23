# determinism-check report, task275, 2026-10-23

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle judged: target.zip md5 b24d9e4b8a8ca8369c75263291b20f74, fresh unzip at /tmp/determinism-check-task275-r1/target/. One thread (sonnet, medium); verdict at /tmp/determinism-check-task275-r1/verdict.md.

## Why
Run literally (terms 2.1 and 3.1 to 3.4: every trip begun in 2025, discards over catch by weight, live weight), the shares are TR1 13.03, TR2 12.31, NEP 14.23, BT 11.77, SN 7.85, GN 7.28, POT 6.33, LL 4.83. TR1, TR2, NEP and BT are designated. Nearest miss SN 7.85, nearest designated BT 11.77; neither is near a rounding edge. A 300-draw bootstrap within ground leaves no interval touching 10 (BT 11.3 to 12.3, SN 7.6 to 8.1). Asks 1 to 3 and the chart ask are determinate.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Trips / observed | 12,000 / 856 | 12,000 / 856 (1,058 deployment rows, 3 cancelled unmatched) | yes |
| BMS kg/h obs vs unobs TR1, TR2, NEP, BT, SN | 25.28/2.10, 9.97/0.84, 1.44/0.11, 4.66/0.06, 6.81/0.05 | same | yes |
| BT hours on WC14+WC15 | 39 vs 69 per cent | 39.1 vs 68.7 | yes |
| Discard shares whole per cent | 13, 12, 14, 12, 8, 7, 5, 6 | 13, 12, 14, 12, 8, 7, 5, 6 | yes |
| Ask 2 first-sale value (kStg) | 12,096.9 / 7,236.8 / 8,018.4 / 9,701.5 / 3,558.7 / 1,731.4 / 695.0 / 2,355.0 | identical (2,887 excluded Barlow & Hobbs lines all duplicate market lines at ratio 1.000) | yes |
| Ask 3 days at sea | 2,236 / 3,032 / 3,502 / 2,128 / 1,724 / 2,417 / 1,377 / 2,594 | identical (inclusive and exclusive removal day agree) | yes |
| Observers-DIS-only variant | NEP 12.0, TR1 4.0, TR2 4.6, BT 2.9 | same | yes |

## Competing answers that survived
None that change the call without being refuted by shipped data.
- Raise by hours, segment only: BT 8.5, drops BT. Refuted by the ground mix (39 vs 69 per cent) and unwanted-catch rate 12 to 13 kg/h on WC14/15 vs 2.8 on WC12.
- Observer DIS only / declared discards only: NEP only / none. Refuted by the BMS gap, which the data show.
- Not subtracting unobserved declared BMS: adds GN at 10.6. Logically excluded (terms 3.2: declared BMS was landed).
- Per-trip, per-haul, ground x quarter variants: same four designated.
- Ask forks (sale date vs landing date; vessel name on report vs transponder; UTC dates) change figures, each closed by the terms (4.3, 4.2) and the data dictionary.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 (README included) | yes |
| Formats | 3 or more | csv, pdf, xlsx, txt | yes |
| Large file | 25,000 rows or more | vms 197,003; sales 99,364; landings 75,319; hauls 65,501 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | quota_uptake_2025.xlsx, gear_specifications_2025.csv; names neutral | yes |
| Distractors unused yet weighable; a shipped fact rules out any that answers a graded quantity | yes | unused by solution; neither answers a graded quantity (judge also notes discards_declared_kg and landing-obligation flags as in-bundle decoy-free noise) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 8 segments x 3 measures plus chart; units and rounding in prompt | yes |
| Prompt shape, 25 or more criteria | yes | descriptive/distribution; 8 x (share, designation, value, days) plus call, components and chart comfortably exceeds 25 by count, rubric not itself generated here | yes (by count, unverified against generated rubric) |
| Not LLM-flavoured, goldens realistic | yes | judge found documents business-realistic; no generation disclosure in README | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note stump sentence: ground-stratified raising of observed unwanted catch with unobserved declared BMS subtracted, against the default of raising observers' discards (NEP only). Same mechanism and same easy route; no mismatch. The declared distractors (quota uptake, gear specifications) are not the surface read carrying the task; the competing routes the judge names (observer DIS, declared discards, unstratified raising) use the core files, not the distractors. No shipped artifact ranks the segments on the decision. Gate G passes.

## Gate H reconciliation
Judge: domain pass, layers pass, decisive_step analytical. Card: stump_class analytical, analyst_test (raising observer discard share area by area names only NEP), domain_test (observer effect in discard estimation; swap loses the incentive and undersize signature). The note's Three rules lines (No decoy, Not semantics, Not rule application) are present. Consistent with the thread; no mismatch.

## Stump power (Gate F)
Moderate to strong per the judge: even after cleaning and reading every term, a 7 per cent observer sample must be raised, and the pooled or unstratified route loses BT while the observers-DIS route designates only NEP. Caveat for the main thread: the corrective method (stratified raising from an observed-vs-unobserved comparison) is a field-standard technique, and the stratum and BMS comparison are findable in the pack, so a strong solver may land it. Weigh with the scored readers' result (stumping 1.3), not on this thread's judgment alone.

## Findings, ranked
1. None blocking.
2. Non-blocking: prompt does not name the raising method; the data separate the candidates (all stratified constructions agree on the whole per cents, spread under 0.71 points per the note). Do not file the HOW.

## Next action for the author
Proceed to ship; no generator change. Nothing was modified in the task folder other than this report.
