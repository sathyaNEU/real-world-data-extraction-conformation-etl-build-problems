# determinism-check report, task118, 2026-11-07

Re-judge pass (architecture 6, one re-judge after the FIX_NOW that pinned the SF17 unit-connection
construction). Supersedes nothing: `determinism_check_report.md` (pass 1 of this architecture, NOT_DETERMINISTIC
on Gate C) stays as the record of the finding that triggered this repair; this file is the next free name
after `determinism_check_report_pass10.md` (those earlier-numbered passes belong to prior architectures).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: binding_constraint, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## SF17 fork: CLOSED
The thread rebuilt the unit-chain replay independently from `train_running_autumn_2026.csv` and
`working_timetable_autumn_2026.xlsx` (not from the design note) and found 276 later-workings that departed
late in the real record, across all four turnback termini (RAVLCEN, RAVLAPT, CROSMOR, HOLMFRY) and roughly
200 distinct units over the 60 weekdays. Every one of the 276 departed exactly 240 seconds after its unit's
recorded arrival, with zero exceptions; the minimum observed turnback gap even among on-time departures is
also exactly 240 seconds at all four termini, never less. That rules out a floor-with-slack, a
station-specific offset, or an independent-delay model as competing constructions: the data admits exactly
one rule (`replayed_departure = max(booked_departure, replayed_prior_arrival + 240s)`, applied only when the
working was actually late in the record). Implemented literally, it reproduces all six CRITICAL_COMPONENTS
figures to the exact rounding bin (see ledger). The second construction that caused the first-pass finding
does not survive a fresh, adversarial reconstruction of the shipped files. The repair holds.

## Why
Gates A and C both pass on the main recommendation and its directly-keyed asks (1, 2): the committed figures
for all six shortlisted stations reproduce from an independent re-implementation of the dwell-reduction and
unit-chain replay, and no second defensible construction of "carrying a unit's lateness into its next
working" survives the shipped running record. Gates B, D, E were run fresh by the thread and pass: no decisive
fact is missing or external, the difficulty traces to analysis (tracing units through the day) not to a
word's meaning, and the prompt commits to one station, one gap, with unit and rounding stated.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pellingham saving | 4,100 | 4,107 → 4,100 | yes |
| Saltgate saving | 2,900 | 2,910 → 2,900 | yes |
| Brathwick Road saving | 1,700 | 1,669 → 1,700 | yes |
| Ambrey Parkway saving | 1,600 | 1,627 → 1,600 | yes |
| Holcroft Green saving | 400 | 415 → 400 | yes |
| Ostley Lane saving | 400 | 407 → 400 | yes |
| Pick/runner-up gap (ask 2) | 1,200 | 1,197 → 1,200 | yes |
| Gateline counts (ask 3) | per station | underlying artifacts (SLG-MAIN 16-bit wrap, AMP-1 restart, BWR-B tidal imbalance) confirmed real; final to-the-passenger figures not independently re-derived | partial (flagged, not a defect) |
| Delay Repay bands (ask 4) | per line/band | appeal top-up rows (119 claim_refs, two payment rows each) confirmed real; final to-the-pound bands not independently re-derived | partial (flagged, not a defect) |

The thread explicitly scoped its full independent re-derivation to the main recommendation and its two
directly-keyed asks (the task instructions here asked for a fresh, adversarial Gate A/C pass focused on the
SF17 repair); it verified the gateline and Delay Repay asks' underlying data artifacts are genuine and
load-bearing (a naive uncorrected gateline total differs substantially from the committed figures) but did
not re-derive the final banded/counted figures to the pound or passenger. This is reported as an open item,
not a finding: nothing it checked contradicted the committed answers.

## Competing answers that survived
None for the main recommendation or asks 1–2. The thread stress-tested the one plausible competitor (dropping
unit-chain propagation entirely, valuing each train's saving locally) and confirmed it is not a second
defensible reading of SOLUTION_STEPS 4 or the data's own unit numbers, it is simply the easy, wrong route
(Pellingham collapses to ~1,900, below Saltgate's ~2,884, flipping the pick to Saltgate) — this is the
intended stump mechanism, not a surviving fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / formats / large file | 10+ files, 3+ formats, 1 file 25,000+ rows | 10 files; csv x7, docx x1, xlsx x2 (3 formats); `train_running_autumn_2026.csv` at 363,900 rows | PASS |
| Distractors declared | metadata.json names 2+, no filename labels one | `incident_log_autumn_2026.csv`, `station_usage_estimates_2025-26.csv` declared; neither file name says "distractor" | PASS |
| Distractors relevant, unused | each weighs, none decides | both unused by SOLUTION_STEPS; design note's single-use test also gives `performance_summary_autumn_2026.xlsx` a stated use (operator's own punctuality) without declaring it a distractor — a third unused-by-solution file that reads as background/color rather than a weighed distractor. Not a finding; noted for completeness. | PASS |
| Deliverables | 1–3 requested, all present in golden | 2 requested (`dispatch_team_siting_2027.xlsx`, `lateness_saved_by_station.png`), both present under `task118/golden/` | PASS |
| Asks multi-dimensional, unit/rounding stated | yes | every ask (saving, pick/runner-up/gap, gateline, Delay Repay) is multi-cut with unit and rounding in the prompt sentence | PASS |
| Prompt shape / rubric 25+ | shape identifiable, 25+ criteria | card records `shape: "01"`; no rubric file is shipped in the task folder to independently count criteria against (rubric generation is a separate house process keyed to the prompt shape) — not independently verifiable from the bundle, deferred to the portal/rubric pipeline | not checked (out of bundle scope) |
| LLM-generation / realism | none reads as LLM-generated, goldens read as real work product | thread found irregular gateline cadence, genuine counter artifacts, varied claim amounts/payment methods, plausible docx core/app properties (creator "Ravelstoke Rail", no benchmark disclosure); no LLM tells observed | PASS |

## Gate G reconciliation
The card (`.claude/skills/fingerprint/cards/task118.json`) files `gate_g: "decomposition_attribution"` /
`stump_strategy: "decomposition_attribution"` as the design-time classification. The judge thread
independently classified the mechanism as `binding_constraint` (a correctly-reported dataset where a real
operational constraint, the unit's turnback floor, changes the naive per-train pick). These are different
labels inside the same family: both are FINE-numbers, non-surface-read-rejection shapes
(`stumping_family: analytical_non_defect` in both the thread's read and what the card's `decisive_rule_filed:
false` / `official_decoy: false` / `validated_decoy: false` fields imply), both set
`surface_read_dependency: no`, and neither names the declared distractors (`incident_log_autumn_2026.csv`,
`station_usage_estimates_2025-26.csv`) as the surface read carrying the task. This is a labeling mismatch,
not a substantive one: nothing here reads as "a reported number is wrong, catch it," on either account. I am
not treating this as a Gate G reconciliation finding that predicts a send-back, because the two labels
describe the same underlying mechanism from two different angles (a decomposition of where lateness-saved
splits across a station's own trains vs. a constraint, the turnback floor, that changes the naive
per-station ranking); the design note itself frames it as "the vehicle passes on to its next assignment
whatever part of its lateness exceeds the slack before that assignment," which reads as both at once. Worth
a one-line house note for future cards: pin whichever label the author intends so future judge threads do
not have to reconcile it from scratch.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`, with the easy route named (value each
train's saving locally, never tracing the unit forward) and the wrong answer it gives (Saltgate instead of
Pellingham).

Card: `stump_class: "analytical"`, `analyst_test`: "A strong analyst who reads every file correctly prices
each station's team at the dwell overrun it would remove there, carried down the same train to each
passenger's alighting stop net of the timetable's recovery allowances, and files the station whose trains
carry the most passengers through the largest overruns; that route never follows a late unit into its next
working and names the wrong station." `domain_test`: "The deciding quantity is each siting's passenger
lateness avoided across the network, which rail performance analysis builds from train running records, the
working timetable's recovery allowances and turnaround slack and the units each working uses; with hospital
nouns... there is no timetable whose allowances absorb lateness, no passenger loading along a route and no
unit carrying a late arrival into a full working, so the call stops making sense."

These align closely: the thread's "easy route" is the card's `analyst_test` almost verbatim (price each
station's team at its own train's overrun, never trace the unit forward, land on the wrong station), and the
thread's swap test (hospital nouns) matches the card's `domain_test` reasoning. The design note's `## Three
rules` section (line 113) and its SF17 fork-table row (line 171, `same call`, asserted) both state the same
single construction the thread rediscovered independently. No mismatch between the thread's Gate H read and
the design note/card. This is a landed-call-worthy construction in the sense the contract names: the golden's
method (follow the unit through its day via the turnback floor) is the field's own recognized way of valuing
a timetable intervention, not an arbitrary device, and the thread reached it by applying real constraints the
data forced, not by executing an unstated rule. Recorded here under stump power, weighed by the main session
against the design note's ladder as instructed.

## Stump power (Gate F)
A solver that computes each shortlisted station's saving train-by-train, without tracing the unit (rolling
stock) diagram into each unit's next working, undercounts Pellingham by more than half (4,100 vs. ~1,900) and
recommends Saltgate instead, a specific, provable wrong answer from a specific missed mechanism, not a
coin-flip. This is real delay-attribution-through-rolling-stock-diagram work a railway performance analyst
would have to do. No too-easy signal observed (the construction is not documented anywhere the solver can
read it off; it has to be derived and justified from the running record's own behavior, per the thread's
276/276 exact match finding).

## Findings, ranked
1. (informational, no action) Gate G label on the card (`decomposition_attribution`) and the independent
   judge thread's mechanism (`binding_constraint`) differ in name but not in substance or in Gate G outcome;
   both pass. Pin one label on the card for future reference.
2. (informational, no action) `performance_summary_autumn_2026.xlsx` is unused by the solution and not
   declared a distractor in `metadata.json`, though the design note gives it a stated use (operator's own
   punctuality, serving the single-use test). Not a defect; noted for completeness only.
3. (informational, not independently verified) The gateline (ask 3) and Delay Repay (ask 4) asks' final
   to-the-passenger / to-the-pound figures were not independently re-derived by the judge thread, though their
   underlying data artifacts (16-bit wraparound, controller restart, tidal imbalance, appeal top-ups) were
   confirmed real and load-bearing. No evidence of error found; this is an open item for a future pass if the
   author wants it closed, not a disposition-changing finding on this pass.

## Next action for the author
None required to ship architecture 6: the SF17 fork is closed, the main recommendation and its two
directly-keyed asks (1, 2) reproduce exactly, and Gates B–H all pass fresh under an adversarial re-judge. If
the author wants belt-and-braces closure on asks 3 and 4's final figures (finding 3 above), that is optional
and does not block shipping.
