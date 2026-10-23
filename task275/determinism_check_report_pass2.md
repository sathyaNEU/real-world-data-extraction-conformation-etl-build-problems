# determinism-check report (pass 2), task275, 2026-10-23

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle judged: target.zip md5 d6cd71d9e37b3fba3efbd93b4c2cc353, fresh unzip at /tmp/determinism-check-task275-r2/target/. One thread; verdict at /tmp/determinism-check-task275-r2/verdict.md. The round-1 report (determinism_check_report.md) is kept as history. Round 2 follows the re-sited asks; the main call and shares are unchanged.

## Why
The call (designate TR1, TR2, NEP, BT; SN highest of the rest) reproduces. Golden-method shares: TR1 12.81, TR2 12.01, NEP 14.16, BT 11.83, SN 7.69, GN 7.11, LL 4.81, POT 6.33, rounding to 13/12/14/12/8/7/5/6. Variants (sampled hours, DIS scaling, ground x quarter, ground x mesh, per-landed-kg) keep the same four above 10 and SN below, with the same whole per cents. Bootstrap within segment and ground: BT 11.26 to 12.42, TR2 11.46 to 12.50, SN 7.41 to 7.95.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Observed trips | 856 of 12,000 | 856 match one logbook trip each (within 2.3 h) | yes |
| BMS kg/h obs vs unobs TR1, TR2, NEP, BT, SN | 25.28/2.10, 9.97/0.84, 1.44/0.11, 4.66/0.06, 6.81/0.05 | same | yes |
| BT hours on WC14+WC15 39 vs 69 per cent | claimed | not recomputed individually (per-ground rates and trip counts were) | partial |
| Shares, whole per cent | 13, 12, 14, 12, 8, 7, 5, 6 | 12.81, 12.01, 14.16, 11.83, 7.69, 7.11, 4.81, 6.33 | yes |
| Observers'-DIS-only (NEP, TR1, TR2, BT) | 12.0, 4.0, 4.3, 2.9 | 11.95, 3.98, 4.21, 2.85 | yes to rounding |
| Ask 2 kStg | 12,012.6 / 7,159.1 / 8,031.6 / 9,687.6 / 3,561.4 / 1,725.9 / 694.5 / 2,338.2 | identical, only when the 714 B&H lines that repeat a market lot are removed | yes (rule inferred from data) |
| Ask 3 days | 2,236 / 3,032 / 3,517 / 2,128 / 1,737 / 2,419 / 1,362 / 2,593 | identical (UK days, transponder assignment by report date) | yes |

## Competing answers that survived
- Ask 2, repeat-line rule: the submission's step 7 says to leave out the lines B&H filed for fish it bought on Kestlemouth and Brindlesea, "which repeat the market's lots". Read as every B&H line at those two ports, it gives TR1 11,997.4 / TR2 7,135.2 / NEP 8,016.1 / BT 9,660.0 / SN 3,557.1 / GN 1,724.7 / LL 693.4 / POT 2,335.0, which differs at 1 dp. The golden removes only lines whose weight is 0.97 to 1.02 of the market lot (714 lines); the other 606 are 0.25 to 0.72 of the lot and are kept. The split is clean, and the logbook reconciliation forces it (market lot plus partial parcel is about landed weight; market lot plus a repeat is about twice). Data-resolved but the softest committed figure; the prompt does not state the rule.
- Ask 3 by the vessel name or PLN stamped on the position row gives other totals (BT 1,932, LL 1,442); closed by the data dictionary and terms (transponder table governs). Sale date instead of landing date: closed by the terms and the prompt's "2025 landings".
- Main call: pooled raising (BT 8.5) and DIS-only (NEP alone) change the call; both are refuted by the data (BMS gap, ground mix).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 17 / csv, pdf, xlsx, txt | yes |
| Large file | 25,000 rows | vms 197,077; sales 99,002; landings 75,319; hauls 64,570 | yes |
| Distractors | 2+ in metadata.json, none named by file | quota_uptake_2025.xlsx, gear_specifications_2025.csv; unused; names neutral | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), in golden/ | yes |
| Asks | unit and rounding stated | stated in prompt for every ask | yes |
| Prompt shape, 25+ criteria | yes | 8 segments x several measures plus call and chart exceed 25 by count; generated rubric not seen | yes (by count) |
| Not LLM-flavoured | yes | judge: realistic documents, README is a plain inventory | yes |

## Gate G reconciliation
Judge: statistical_rigor / analytical_non_defect / surface_read_dependency no / sole_data_defect no (round 1 said method_or_model_selection; same mechanism, different label, both match the note's stratified raising of an observer sample). The declared distractors do not carry the task; the weak surface read the judge names (logbook-declared discards, zero except NEP) is a core-file field, not a declared distractor, and ranks nothing. Passes.

## Gate H reconciliation
Judge: domain pass, layers pass, decisive_step analytical. Matches the card (stump_class analytical, analyst_test, domain_test) and the note's Three rules. No mismatch.

## Stump power (Gate F)
Judge: strong. The pooled and DIS-only routes land on a wrong set. Per the coordinator, the round-2 scored readers both missed the call, which supports this. The main call is not the concern; the days-at-sea ask was landed by one reader, which is being re-sited.

## Findings, ranked
1. Non-blocking, softest figure: ask 2's repeat-line rule is not stated in step 7 and the wording is readable as every B&H line at the two ports (1 dp fork, data-resolved). Fix in the solution wording only: state the rule as lines repeating a market lot (weight within 3 per cent), filing the WHAT not a method. Then re-check that the data still forces it.
2. The coordinator's planned re-siting of ask 3 changes the bundle; this pass does not cover it.

## Next action for the author
Tighten submission.md step 7 for the repeat lines, rebuild only if the bundle changes, and request a round-3 brief after the ask 3 re-siting rebuild is green.
