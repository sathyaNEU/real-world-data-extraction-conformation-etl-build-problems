# determinism-check report, task162, 2026-10-28 (run r2, target.zip sha256 a8146587633b1cd3)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

(r1 on target.zip 828ecbc5 was superseded before a thread ran; this is the only judged pass. Thread verdict: scratchpad/determinism-check-task162-r2/verdict.md.)

## Why
Executed literally, the prompt, Schedule 4, LW-LA-04 issue 6, rev C settings and the planning e-mail give one main call: replaying each hourly inlet pressure through the fixed-outlet setting (lower of recorded and setting) and rebuilding N1 and the night-day factor gives 3.22 to 2.81 Ml/d, reduction 0.41, shortfall 0.07 (0.0701), 2 gang-years. The night-ratio shortcut gives 0.63 Ml/d and 0 gang-years; the routes separate cleanly. Every Ask figure reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Phase 3 2025-26 leakage | 3.22 | 3.2211 (export Year sheet 3.2210) | yes |
| Forecast 2027-28 | 2.81 | 2.8112 | yes |
| Reduction / shortfall | 0.41 / 0.07 | 0.4099 / 0.0701 | yes |
| Gang-years | 2 | ceil(0.0701/0.05)=2 | yes |
| Night-ratio route (easy) | n/a | 2.5908, reduction 0.6303, 0 gang-years | yes |
| Twelve districts (3dp) | NZ01 0.153 ... NZ12 0.114 | identical, all 12 | yes |
| System input | 30.36 | 30.3619 | yes |
| Billed unmetered | 5.61 | 5.613 | yes |
| Real losses | 5.97 | 5.972 | yes |
Sensitivities (proportional zone pressure, 0.1 m head loss) keep shortfall 0.065 to 0.071 and 2 gang-years.

## Competing answers that survived
None on the main call. Residual forks on Ask 2 (all inferred from data, not filed in text), recorded for the author:
- Dwelling count (LW-LA-04 s4 "each dwelling"; the extract's counting is not defined in shipped text). Golden counts each dwelling once (plot to address handover, each flat once). Alternatives: all records counted (NZ01 0.151), distinct supply points (0.159), plot records dropped (0.155). The thread judged the golden pinned by data (plot records without UPRN, bills starting on connection date, 345 handovers, k identical bill lines per flat supply point). Design note SF5 says Phase 3 is the same under every reading but the twelve-district asks are not; the design note deliberately declined the optional pin (Ask A's primary).
- NZ09/NZ10 12 to 20 January 2026 exclusion (no valve log shipped; evidence is the dry NZ09 inlet and doubled NZ10 inflow). Without it NZ09 0.140, NZ10 0.152 (golden 0.146, 0.146 with the exclusion).
- Identical assessed bill lines kept (dedup gives 5.36 and 6.22); bill_to inclusive (exclusive gives 6.00). Both pinned by the extract.
None touches the main call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / rows | 10+ / 3+ / 25,000+ | 16 / 4 (csv, xlsx, pdf, eml) / 306,523 rows | yes |
| Distractors | 2+ named in metadata.json, none labelled by file name | customer_contacts and brackenby_mill_amr named; neither named "distractor" in a file name | yes |
| Distractors unused yet weighty | unused by golden, ruled out by a shipped fact | contacts unused; mill AMR explains weekday inlet drop only, does not answer a graded figure | yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt states Ml/d to 2dp, 12 districts to 3dp, gang-years whole | yes |
| Prompt shape, rubric 25+ | identifiable, 25+ | shape in metadata (go/hold plus grid plus chart); rubric is generated downstream, not verifiable here | yes (shape); rubric not checked |
| Not LLM-looking, goldens real | yes | thread found no tool banner or generator signature; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, analyst_test is the night-ratio-through-the-day route (0.63, target met), identical to the thread's competing answer. Design note stump sentence: same. Match. The thread did not name either declared distractor as the surface read carrying the task. Watch item: the rev C schedule's "AZNP after commissioning" column is the true night figure that equals the replayed night AZP and invites the easy route. The design note states it as a true night figure with no benefit stated, so it is not a wrong shipped ranking; thread did not raise it as a Gate G violation.

Gate H reconciliation: thread domain pass, layers pass, decisive_step analytical. Design note and card (domain_test, Three rules lines present: No decoy, Not semantics, Not rule application) agree. Mismatch: none.

## Stump power (Gate F)
Thread: moderate on the main call, plus heavy independent weight in the asks (dwelling dedupe, NZ09/NZ10 exclusion, flat bills kept, calibration cut-off). One caution for the main thread: the fixed-outlet valve behavior is physical judgment, not filed, but a strong solver who asks what a fixed-outlet valve does to an already-low inlet reaches it. The note's own ladder governs; the thread did not class the step analytical merely because the golden is a standard method.

## Findings, ranked
1. None blocking.
2. Ask 2 dwelling count rests on data inference rather than a filed sentence (design note declined the pin on purpose; it is the intended Ask device, but it is a determinism exposure on twelve gradable figures).
3. NZ09/NZ10 exclusion rests on telemetry evidence only.

## Next action for the author
Proceed to ship. If the portal flags a determinism finding on Ask 2, file the WHAT ("a dwelling is counted once") not the HOW.
