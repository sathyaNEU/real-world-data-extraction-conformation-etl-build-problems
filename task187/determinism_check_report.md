# determinism-check report, task187, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (optional WHAT-pin hardening, see Findings)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, scratch /tmp/determinism-check-task187-1791859754/, verdict at verdict.md there. The thread judged the pack before a realism-only rebuild (duplicated hub serial HB-93-0612 since fixed; no figure moved).

## Why
CH04 and 100 MWh is the only call that holds once blade loss is measured against the as-new power in the same winds, turbulence included. Three turbulence-aware variants all put CH04 first and CH02 second, with CH04 at 83 to 89 MWh, so 100 at the 50 MWh rounding. The literal "Schedule 3 at the same mean wind" reading gives CH07 (235, so 250). Shipped data refutes it: CH07 runs above the warranted curve at 4 to 8.5 m/s and below it at 9.5 to 12 m/s, which eroded blades cannot do. CH09 is excluded by rule 2.5 through the crane log and site layout (361 MWh whole year, about 0 on its own months, start date not a fork).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Downtime MWh CH01..CH10 | 60,47,103,130,51,430,56,129,341,71 | 60.09,46.78,102.66,129.65,50.92,429.85,55.59,128.57,341.30,71.13 | yes |
| Curtailment MWh CH01..CH10 | 292,297,297,293,302,291,302,304,300,302 | 291.70,297.12,297.12,293.13,301.64,290.93,302.03,303.67,299.80,301.54 | yes |
| Bin shortfall vs Schedule 3 (CH07, CH01, CH05, CH04, CH02) | 235,115,114,93,71 | 234.8,114.9,114.0,93.0,71.3 | yes |
| Blade loss, zero-turbulence model (CH04, CH02) | 89, 65 | 88.9, 65.3 | yes |
| Fleet same-bin comparison CH04 | 83 | 82.8 | yes |
| Recovered energy | 100 | 83 to 89, so 100 | yes |
| Clock alignment | local to 26 Oct, UTC after | r 0.988 vs 0.931 at -1 h before; zero shift after | yes |

## Competing answers that survived
None survived. Closed forks: CH07/250 (own-curve signature), CH09/361 (rule 2.5 plus shipped lift log and pads), CH02 on a below-rated cut (clause 2.4 values all normal operation), mast wind as "the same winds" (gives absurd 680 to 835 MWh).
Residual (moderate): OM-07 2.4 and Schedule 3 never mention turbulence and the zero-turbulence model is not in the package, so a strictly literal executor stopping at Schedule 3 files CH07/250. The data separates the candidates, so the judge kept DETERMINISTIC. The design note's own Three-rules line concedes no filed rule says how turbulence enters.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 5 (pdf, xlsx, csv, parquet, txt) | yes |
| Large file | 25,000+ rows | parquet 522,159 | yes |
| Distractors | 2+ in metadata.json, none named in a file | export_meter_halfhourly, lost_production_2024_25.xlsx; file names do not label them | yes |
| Distractors weigh but are unused, and a shipped fact rules them out | yes | judge found them present and unused; 2024-25 file is rev 2 basis | yes (not individually stress-tested) |
| Deliverables | 1 to 3 | 2 (pdf, xlsx), all in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 10 turbines x 2 losses, nearest MWh, 50 MWh | yes |
| Prompt shape and 25+ criteria | yes | shape 14, 29 criteria by design-note arithmetic (rubric not generated here) | yes (by note) |
| Not LLM-like, goldens real | yes | judge found no authoring language; golden realism not re-read by me | yes (judge) |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: strategy and mechanism decomposition_attribution, Gate G decomposition_attribution. Match. The declared distractors (export meter, 2024-25 file) are not what carries the task; the trap is the warranted-curve shortfall, a derived figure and not a shipped wrong ranking, so Gate G passes.
Gate H: thread says domain pass, layers pass (Layer 1 BST/UTC, comms and grid gaps, work-order times; Layer 2 turbulence-normalised blade loss), decisive_step analytical. This matches the card and note (stump_class analytical, domain and analyst tests).

## Stump power (Gate F)
Two hops stack. Ignoring 2.5 gives CH09; applying 2.5 but using the shortfall at the same mean wind gives CH07 (250 MWh). Only the turbulence-matched as-new comparison gives CH04/100. The CH07 hop is the real analytical trap and a strong model is likely to take it. The CH09 hop is a rule-and-lookup layer and not the main stump.

## Findings, ranked
1. Residual literal-reader risk (moderate): the as-new reference is not filed with turbulence. Optional fix, which needs a rerun: add a WHAT pin to OM-07 2.4 such as "in the same winds, wind speed and turbulence as recorded at the turbine's nacelle". Do not file the Cp 0.470 model or Annex M, as that turns the step into rule application.
2. Design note staleness: its Default path says CH09's rotor went up on 20 March 2026, while the solution and the shipped crane log give 24/25 April 2026 (BC-26-0314, pad P08). The judge showed the start date is not a fork (own-months loss -4.6 to +0.4 MWh for 24 Apr, 25 Apr or 1 May), but the note should be aligned.
3. The chart itself was not an input to the thread, so only its numbers were checked against the xlsx values.

## Next action for the author
Proceed to ship. Optionally apply the OM-07 2.4 WHAT pin and re-judge once; otherwise fix the 20 March date in the design note.
