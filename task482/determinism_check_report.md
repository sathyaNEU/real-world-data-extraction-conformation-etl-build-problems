# determinism-check report, task482, 2026-10-23

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: planted_defect_flip (borderline method inference), stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes
Governing label: competing_defensible_answer. Judge thread: /tmp/determinism-check-task482-190003/verdict.md (one pass, sonnet, medium).

## Why
Read literally, the shipped records give one priority station (W-16), not the golden's four. The golden needs unreported broken docked bikes inferred from nonuse plus a depot stay of a day or more. No shipped file or filed rule states that rule. Schedule C.1 defines "working order" functionally, and C.5 names trips, fleet moves and fault reports as the records the City determines availability from. All of these give W-16 alone. The golden's own recommendation text concedes the feed reading yields W-16 alone.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Feed reading, lowest months | n/a | W-16 87.49, W-09 90.68, W-02 91.02, W-12 91.79, W-19 92.09; priority = {W-16} | yes, but != golden |
| Trips + fleet moves rebuild, all bikes working | n/a | W-16 87.66, W-09 90.68, W-02 91.02; priority = {W-16} | yes, but != golden |
| Same rebuild, fault-reported bikes out from report time | n/a | W-16 87.22, W-19 91.5, W-12 91.61, W-02 91.02; priority = {W-16} | yes, but != golden |
| Golden-style inference (24 lowest-month availabilities, 4 priority stations) | 88/88/86/88 | reproduced | only under the unfiled rule |
| W-09 margin | 91 per cent, 0.7 | 90.68, 0.7 | yes (needs unrounded value) |
| Card sales, 24 stations | listed | exact to the cent | yes |
| Card-down hours, 24 stations | listed | exact (e.g. W-19 104.92, W-02 6.22) | yes |

## Competing answers that survived
1. Main call. Reading A (feed or City records, nothing inferred) gives {W-16}. Reading B (the golden) gives {W-02, W-12, W-16, W-19}. No shipped file says unreported broken bikes exist or how to identify them. Schedule C D.1/D.2 refer to an inspection rota "filed with the City" that is not shipped.
2. Unfiled depot-stay cut and "other renters took bikes" test (SOLUTION_STEPS only). Priority membership holds for cuts of 0 to 48 h. Graded whole-per-cent figures move: at 36 h W-17 goes 91 to 92; at 48 h W-01, W-17 and W-19 move; with 2 or more other rides W-19 goes 88 to 89. At 60 h or more W-12 leaves the priority set. W-17 and W-19 availability is therefore not forced.
3. Minor: alarm clear at RESTART (not in the register, but effectively forced by the data); the margin needs the unrounded 90.68, since on whole-per-cent figures W-05, W-09 and W-17 tie at 91.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, json) | yes |
| Large file | 25,000+ rows | trips 50,254; status archive 93,441 | yes |
| Distractors in metadata, none labelled in a file name | 2+ | 2 (weather csv, quarterly report pdf); the GBFS station-information json is not named | yes |
| Distractors unused yet relevant; none answers a graded quantity | yes | quarterly report and weather state no station figure; relevance is moderate | yes (weak) |
| Deliverables | 1 to 3 | 2 (xlsx, html) | yes |
| Asks state unit and rounding | yes | yes | yes |
| Asks multi-dimensional | yes | 24-row grids, determinate | yes |
| Rubric 25+ criteria | 25+ | design note says about 80 (not generated here) | yes (unverified) |
| Prompt shape identifiable | yes | shape 07, grid read at its binding cell | yes |
| Not LLM generated; goldens realistic | yes | judge found no authoring leakage | yes |
Judge hygiene: PASS. Layer 1 mess is realistic (DST, repeated week of 16 Nov, W-17 move, terminal swaps, voids).

## Gate G reconciliation
Judge: mechanism planted_defect_flip, family surface_read_rejection, surface_read_dependency yes, sole_data_defect yes. Design note and card: strategy `other`, Gate G `method_or_model_selection`, generator G12 (absence of record against record of absence), Layer 2 `estimation_fit`. Mismatch: the note frames a fitted estimate of an unrecorded state, but the judge finds a latent defect planted in the logs, caught by rejecting the feed's count. This predicts a send-back. The declared distractors (weather, quarterly report) do not carry the task, so no finding there. Gate H line: `domain: pass`, `layers: pass`, `decisive_step: planted`. The note's "Not semantics" and "no decoy" claims do not hold. The note itself says the decisive fact is "which no record or filed rule states", which is the unfiled rule behind the NOT_DETERMINISTIC verdict. The note was read only after the thread returned.

## Stump power (Gate F)
Trusting the feed or the City's records files W-16 alone and fails, which is plausible stump power. But the failure is partly for the wrong reason, since a careful model can defensibly stop at the records. The pay-station asks (terminal swaps, restart-bounded alarms, DST, voids) are hard and fully determinate. Keep them.

## Findings, ranked
1. Main call not forced: the working-order inference is unfiled, so W-16 alone survives (competing_defensible_answer).
2. Unfiled depot-stay and passed-over thresholds move the graded availability figures for W-17 and W-19 (and W-01 at the 48 h cut).
3. Gate G/H: the decisive step reads as a planted latent defect with surface-read rejection (banned scaffold), and the design note and judge disagree on the mechanism.
4. Minor: RESTART clearing absent from the register; the margin depends on unrounded values.

## Next action for the author
Redesign (do not patch with a filed method). The decisive step must be an analysis on honest data, not the catch of a misleading feed. File the WHAT, not the HOW. Do not add the inference rule to Schedule C, since that turns the step into rule application. Keep the pay-station sales and card-down asks as they are.
