# determinism-check report, task280, 2026-10-24

## Verdict
NOT_DETERMINISTIC (the main call is forced and reproduces; supplementary answers 2 and 3 are not forced, and answer 1's whole-per-cent shares are estimator-dependent). Taxonomy: underspecified_objective (competing_defensible_answer on the credits and capacity asks). SOLUTION_WRONG does not apply: every golden reproduces under the reading the golden states.
**Disposition:** SEND_BACK, on the judge thread's reading. The main call, the stump and the ladder stay frozen; the asks need a filed convention and a rerun. The coordinator reports that both scored readers landed the main call (1 of 1 each), so the architecture is spent on Gate F whatever this verdict is. This report is for the record and for the re-root.
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call (Carrow Mills, Dunfield, Greyhaven, Kesterbrook designated; Larchmoor highest of the rest at 18) reproduces from target/ and holds under every hub- or node-aware estimator the thread tried. The naive share of tests designates only Carrow Mills and Dunfield (22 and 25). Two asks hold only under a rule no shipped text states:
- Credits: the golden treats every ticket labelled "Planned" as planned work. Schedule 4, 5.3 defines planned work as notified 48 hours ahead and carried out between midnight and 6.00 am. Fourteen "Planned" tickets (cause MAINT) run past 6.00 am local, for example TT-434243 (GH-024), TT-460739 (KB-042), TT-465336 (GH-048), TT-493409 (CM-073). Read literally they are outages. The dictionary says only "Planned work notified under Schedule 4, 5.3", which asserts notice and not hours.
- Capacity: Schedule 4, 4.1 sums "the hub's nodes in service that day". The register shows 16 extra child rows in service on 13 November. The golden drops them as second records of the split nodes, an inference from their missing subscriber counts that no shipped sentence licenses.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Panel households | 1,137 | 1,137 | yes |
| Duplicate tests removed | 86 exact repeats | 86 | yes |
| Naive share (household-equal) | not claimed (wrong route) | BW 12.3, CM 22.3, DF 24.9, EH 6.2, GH 18.5, KB 16.7, LM 12.6, SC 10.0 | n/a |
| Node load, tested vs all peak intervals | GH 65.3 vs 68.0; KB 64.3 vs 67.1 | same; lighter in every hub | yes |
| Shares, whole per cent (household x plan threshold model) | 17/29/31/10/25/22/18/14 | 17.1/29.2/30.9-31.1/10.1/25.2/22.3/18.1/14.3 | yes (this method) |
| Shares, other threshold choices | same | BW 16.4-17.5, CM 28.3-29.3, EH 9.3-10.9, GH 24.5-25.4, KB 21.2-22.5, LM 17.1-18.4, SC 14.0-14.9 | whole-per-cent values shift by 1 for BW, CM, EH, KB, SC; designations unchanged |
| Shares, plan-only pooled reweighting | not claimed | GH 19.9, KB 24.7, DF 33.9 | flips GH (a weaker method) |
| Credits, label rule | BW 2,549, CM 2,531, DF 2,401, EH 3,149, GH 1,095, KB 2,559, LM 2,808, SC 3,140 | identical | yes |
| Credits, literal 5.3 | n/a | BW 2,549, CM 2,755, DF 2,401, EH 3,656, GH 1,226, KB 2,737, LM 2,808, SC 4,033 | differs in 5 of 8 hubs |
| Capacity, all register rows | n/a | BW 19,300, CM 17,300, DF 18,600, EH 18,010, GH 13,370, KB 7,740, LM 19,770, SC 23,940 | the literal 4.1 answer |
| Capacity, minus the 16 second records | BW 13,200, CM 14,960, DF 16,840, EH 11,910, GH 11,030, KB 5,980, LM 13,670, SC 17,840 | identical | yes |
| Window edge (UTC vs local start) | DF 2,401 | DF 2,402 under UTC | one boundary outage; local is filed only implicitly |

## Competing answers that survived
1. Planned work (Ask A): label-only gives the golden; the 5.3 midnight-to-6.00 am test gives CM 2,755, EH 3,656, GH 1,226, KB 2,737, SC 4,033. Nothing in the pack says which governs.
2. In-service capacity (Ask B): the register as filed gives the larger sums (BW 19,300); the golden needs the unstated step that the second child records are phantom. Which child pair is the phantom one is itself inferred (the earlier pair kept).
3. Shares to whole per cent (Ask 1): the extrapolation from panel tests to untested intervals is not filed. Reasonable variants move BW, CM, EH, KB, SC by 1 point; KB sits at 22.3-22.5 and DF at 30.9-32.4 across hub-aware methods. Designations are stable except under a plan-only pooled method (GH 19.9).
Minor: "Friday nine weeks later" is pinned only by dictionary dates.

## Spec gates
Checked by me on the unzipped bundle and metadata.json after the thread returned; the rubric and the prose-quality gates rest on the thread's reading and the design note.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, txt) | yes |
| Large file | 25,000 rows or more | 403,017-row test extract; 432,612-row utilisation file | yes |
| Distractors named, none labelled by file name | 2 or more | 2 in metadata.json (ovcc_consumer_complaints_2026.csv, panel_latency_2026_evening.csv); neither name labels one | yes |
| Distractors unused and weighable | yes | unused by the solution; the thread judged them relevant and ruled out by shipped facts. designation_closeout_2025.pdf (prior-year capacity) is a further non-named lure | yes (the closeout is not named; noted) |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both present | yes |
| Asks multi-dimensional with unit and rounding | yes | 3 xlsx asks over 8 hubs, unit and rounding stated | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 10 (scorecard); 8 hubs x 3 columns plus designations gives well over 25 | yes |
| Reads as real, not LLM generated | yes | thread found no leakage; index and methods note read as in-fiction | yes |
| Determinism of every golden | forced | asks 2, 3 and the whole-per-cent shares not forced | NO |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no, Gate G passes. Design note and card: estimation_fit, "own: missing at random given an auxiliary utilisation record", no decoy, no planted defect. These match. The declared distractors (complaints, latency) do not carry the surface read, so they are not too load-bearing. The credits and capacity asks are decoupled from the call (the design note records zero device rows reaching it), which is why the main call is unaffected.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Layer 1: duplicate uploads, local time vs UTC and the 1 November change, split nodes, plan changes, replaced units. Layer 2: estimating compliance with the franchise share test from a sample that under-covers congested intervals. Matches the design note's `## Three rules` (decisive step: condition each household's peak tests on its node's utilisation and carry that to every peak interval).

## Stump power (Gate F)
Strong on the main call per the thread: the easy route files two hubs, a capable analyst who reads every rule would still file it, and the pack shows why (tested intervals lighter than the peak in every hub, GH 65.3 vs 68.0). The coordinator's scored result agrees on one point only: both readers landed the call, so the stump did not hold on the portal's measure. Note for the main thread: the decisive method is the field's standard one (conditioning on an auxiliary record), the kind a strong solver reaches, and the thread did not find a judgment the data had to settle beyond the filed estimand. The asks carry much of their difficulty through unstated conventions, the wrong kind.

## Findings, ranked
1. Ask A credits: Schedule 5.3's midnight-to-6.00 am test and the "Planned" label disagree for 14 tickets; 5 of 8 hubs differ. Not forced.
2. Ask B capacity: 4.1 as filed gives the larger sums; the golden rests on an unstated phantom-record inference. Not forced.
3. Ask 1 shares: the extrapolation is unfiled, so whole-per-cent values are estimator-dependent (KB 22.3-22.5, DF 30.9-32.4); designations hold except under plan-only pooling (GH 19.9).
4. Minor: window start is local only implicitly (DF 2,401 vs 2,402); the end-date wording is pinned only by dictionary dates.
5. The design note records the shares as the same whole per cent across the standing family; the thread's extra variants (min-low, max-ok, peak-only) are less principled and are the source of the 1-point shifts.

## Next action for the author
Re-root (the architecture is spent on Gate F). If any of this build's asks are reused, file in the dictionary or prompt that a Planned ticket past 6.00 am is an outage (or end those 14 tickets by 6.00 am), file which register rows count as in service, and file the share unit loosely (tolerance or bands) without filing the method for the main call.
