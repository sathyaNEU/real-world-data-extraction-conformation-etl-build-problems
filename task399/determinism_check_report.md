# determinism-check report, task399, 2026-11-04

## Verdict
DETERMINISTIC, with a minor SOLUTION_WRONG (one sentence of solution step 4).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no (borderline), sole_data_defect: no

Judge thread: one pass, model sonnet, medium effort. It kept the order (derivation.md written before graded_blocks.md was opened). Its derivation matched the submission on every committed answer before it saw it. Scratch: /tmp/determinism-check-task399-817491/ (verdict.md, derivation.md). target.zip sha256 63ad083e...cd3b.

## Why
Clause 2.3 ("an incident counts for a programme when it would not have happened had that programme been in place") makes the count a counterfactual. The control system's own records decide it. In the actions log the signaller requested the route the register calls wrong. In workstation_layout_export_r8.2.1.json the set exit and the required exit are drawn 8.1 to 11.4 px apart in 76 of the 90 wrong-route incidents (next closest same-entrance pair anywhere is 49 px; the other 14 are 60 to 449 px). Per-request error on the 74 twin-exit routes is 0.23% (experienced) against 0.25% (first two years), so A would not have prevented them. B = 76 slips (8,173) + 10 VDS-3 display-fault incidents (812) = 8,985, ahead of every rival under every overlap reading (C 7,331, E 6,642, A 6,517 liberal). The investigation-label route funds A (8,240; 4,210 inside A's first-two-years scope) and is contradicted by 2.3 and by the control-system record. W03 start is 3,544 against 1,487, no fork. All ask tables reproduced to the decimal.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Window incidents (UK time) / minutes after agreed moves | n/a | 470 / 18,108 | yes |
| Wrong routes on drawn-close pair | 76 inc, 8,173 min | 76, 8,173 | yes |
| Display faults | 10 inc, 812 min | 10, 812 | yes |
| B total | 8,985 | 8,985 | yes |
| B by workstation | W03 3,544; W05 1,487; W01 1,266; W06 1,230; W02 762; W04 696 | identical | yes |
| Hours, first two years / others (6 workstations) | W01 1,296.0/7,464.0 ... W06 1,975.5/6,784.5 | identical (clock hours) | yes |
| ARS-off sub-area hours by quarter (6 x 4) | per submission block 4 | identical to the decimal | yes |
| Step 4: cancel-within-20s-and-reset pairs on a drawn-close pair | "every" | 357 of 360 | NO (wording) |

## Competing answers that survived
No fork changes the funded programme or the start workstation. Four residual forks move graded figures, none closed by a shipped sentence:
1. **Display faults counted for B (8,985 against 8,173).** Moves: the headline minutes, critical components 2 and 3 (total), and five of the six chart bars (W02 762 vs 608, W03 3,544 vs 3,412, W04 696 vs 616, W05 1,487 vs 1,142, W06 1,230 vs 1,129; W01 unchanged). Programme, start workstation and all asks unchanged. The literal text favours counting (catalogue B: "The six workstations' display system (Corvane VDS-3 ...) replaced by the supplier's current product"; the ten narratives are failures of that system) but no sentence says the replacement would not fail. The design note's own row SF19 says "same call", yet the figure the prompt asks for moves; the row closes the call, not the figure. Weakest fork. Closure: one scope sentence in the catalogue that the VDS-3 equipment is removed from every workstation. That states WHAT the programme replaces (scope), the same kind of fact as the sentence already there; it does not say that drawn-close exits cause slips or that A is blind to them, so it files no part of the decisive step. It does turn the 812 into a plain 2.3 consequence (rule application on a minor component, which the main-call rule permits as a component; the decisive step remains the 76).
2. **Clock hours against rostered 12-hour shifts.** Moves only W04, 1.0 h in the two hours cells (3,947.5/4,812.5 against 3,946.5/4,813.5), because the 13-hour night of 25/26 Oct 2025 was worked by a first-two-years signaller. The prompt's "hours ... was worked" is the literal basis (SF16 asserted). A pin ("hours on the clock") sits inside the asking sentence as a unit statement; it would name, though not resolve, the clock-change device, so it is an ask-device decision for the author. Literal reading already lands on the golden; pin optional.
3. **FAIL rows counted as switched off.** Their state column reads OFF (90.8 h in total); excluding them moves the ARS cells of the affected sub-areas (e.g. W01 Q4 289.5 against 296.0). Not in the fork table. Closure: a field definition of FAIL in a shipped file header or the layout/ARS documentation. That is data semantics on an ask, permitted, and it carries no device of the main call. Optional because the column text is literal.
4. **Per-sub-area table against the 6 x 4 workstation table; HT-A Q4 near-tie.** The prompt's "each workstation's sub-area hours" can be read as one total per workstation (golden) or as one row per sub-area (15 x 4). The golden is 6 x 4 only; a solver filing 15 rows has to be graded against totals it did not file. Prompt wording does not license the per-sub-area table over the total, nor rule it out. HT-A Q4 120.649 h sits 0.0005 h from a one-decimal rounding line, so a per-sub-area table would be a coin-flip cell. The golden's 24 workstation cells are at least 0.034 h from a line, so the near-tie lives only in the table the golden does not hold. Closure: put "in total" (or "summed over its sub-areas") inside the asking sentence, which is the unit statement the contract requires; it names no device. Alternatively add the per-sub-area rows to the golden, which is worse because of the near-tie.

Readings 1 to 3 (investigation label, clause 2.3 overlap, late-shift and display faults) and 4 to 6 (start workstation, who worked a desk, server clocks) are ruled out or collapse to the golden as the thread documents: the label route is killed by the quoted text of 2.3; roster-only and roster-plus-changes fail 12 unrecorded swaps and 184 relief shifts without a desk; ROC-A is UTC, ROC-B is CET/CEST.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 5 (csv, json, pdf, docx, xlsx) | yes |
| Large file | 25,000 rows or more | actions log 357,103 rows (25 MB) | yes |
| Distractors | 2 or more named in metadata.json, no file name labels one | 2 named (workload assessment PDF, railhead adhesion CSV); names are neutral | yes |
| Distractors weigh, unused, ruled out by shipped fact | each | thread: present and unused; adhesion reports are the weaker weigh (adhesion does not produce wrong-route selections), workload PDF reproduces no graded figure | yes (adhesion marginal) |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (pptx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each | 6 x 2 hours and 6 x 4 ARS grids; "whole minutes", "one decimal" in the prompt | yes |
| Prompt shape and 25 criteria | shape identifiable, 25 or more | shape 12 (drill-down); count from the prompt's cells: 2 headline + 6 bars + 12 hours + 24 ARS = 44 | yes |
| Prompt form | one paragraph, under 1,000 characters, no data-held count | 834 characters | yes |
| Reads as generated / golden reads as real | none | thread hygiene PASS (no authoring language; in-fiction creators); goldens not opened by this pass, left to golden-realism | yes (goldens not re-read here) |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no (borderline), sole_data_defect no. Card: gate_g decomposition_attribution, stump_strategy classification_error, stump_class analytical, layer2_family field_method. Mechanism matches. Family and strategy are two names for the same thing (a recorded cause overturned by the mechanism), no mismatch. Surface read: the design note names rung 0 (findings booked to the catalogue, A at 8,240) as the surface read, not the declared distractor; the workload assessment is not what carries the task. So the distractor is not too load-bearing. The borderline: the surface read is the investigation Finding column and it is overturned. The thread notes the overturning needs an exposure-adjusted error-rate comparison and the layout geometry, and still stumps with blank labels, so it is not a reflex rejection of a wrong number; the Finding column is an honest record of what the investigators concluded (the design note states this). Gate G itself: no artifact ranks the candidates on the decision question and gets it wrong; the Finding column books causes, and the programme ranking is the solver's sum. Held.

## Stump power (Gate F)
Good. Three independent traps move graded figures (label cause against geometry and rate comparison; server B's CET clock, lost events and renamed codes; relief and 12 unrecorded swaps plus the clock-change nights). The decisive step is analytical by the card's analyst_test: the strong analyst who cleans and reads every rule sums by finding and funds A. The thread does not class the step analytical merely because it is a standard method; it required a join across three files and an exposure-adjusted comparison, so no landable-call warning applies. Design note ladder: B 8,985 leads the widest honest rival reach 2.35 times; cracker sheets keep 0 of 36 ask cells. The ask-device claims in the note (roster-only, B-as-UTC) agree with the thread's forks 5 and 6.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the card (analyst_test, domain_test) and the note's `## Three rules` (Not semantics, Not rule application, No decoy all present). One reconciliation note: the note says the 37 quick-reset pairs "are exactly the drawn-close pairs"; the thread counts 357 of 360 cancel-and-reset pairs on a drawn-close pair. Fix the sentence.

## Findings, ranked
1. Fork 1 (display faults): the graded headline and five chart bars depend on counting the 812 minutes; SF19 in the note says "same call" and does not state that the figure moves. Weigh the catalogue scope sentence; update SF19 to say the figure is closed by that sentence.
2. Solution step 4 (and design note, "exactly the drawn-close pairs") says every quick reset falls on a drawn-close pair; 357 of 360. Reword to "all but three".
3. Fork 4: prompt's "each workstation's sub-area hours" does not exclude a 15 x 4 table; HT-A Q4 120.649 is 0.0005 h from a line. Add "in total" or "summed over its sub-areas" to the asking sentence (check voice-check and the 1,000 character limit).
4. Fork 3 (FAIL rows) is not in the fork table; add a row and, optionally, a field definition in a shipped file.
5. Fork 2 (clock hours): leave literal or add a unit phrase in the asking sentence; W04 moves 1.0 h.

## Next action for the author
Reword step 4 to "all but three" in submission.md and the note, and add the fork-table rows for faults (figure-moving, not "same call"), FAIL rows and the per-sub-area table. Then weigh the two cheap bundle pins together in one generator pass (catalogue VDS-3 removal sentence; "in total" in the asking sentence). If the bundle or prompt changes, rebuild twice byte-identical, re-run the free gates, and re-judge once; if only the solution wording and the note change, no rerun is needed.
