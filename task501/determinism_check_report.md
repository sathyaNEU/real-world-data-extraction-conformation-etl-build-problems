# determinism-check report, task501, 2026-11-02 (run a5, architecture 5, target.zip md5 4dd0c07728517f0c7278c201bc196350)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (network flow reconstruction against a stated standard), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One sonnet judge thread (verdict at /tmp/determinism-check-task501-a5/verdict.md). NOS 12 s4.2/4.3 and the outage plan fix the comparison: works peak (districts' inflows for 15 Mar to 15 Sep 2026 through the plan's valves) against the highest hourly flow actually carried Nov 2025 to Oct 2026. Only TM112 (140 vs 65) and IC05 (121 vs 0) exceed their reference; the other four sit 34 to 57 l/s under their June/July 2026 Mill Road peaks, so no margin is thin. Every golden figure reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Works peaks TM104/TM109/TM110/TM112/IC03/IC05 (l/s) | 229/179/124/140/84/121 | 229.4/178.9/124.0/140.4/84.3/120.6 | yes (dma_inlet_flows, register, plan) |
| Carried peaks, same order | 263/228/177/65/141/0 | 263.3/227.6/177.4/65.2/141.0/0.0 | yes (valve log, inflows) |
| Flush set | TM112, IC05 | TM112, IC05 | yes |
| Flushing m3/100 m by DN, 2025/2026 | 1.5/1.5; 2.7/2.7; 6.1/6.2; 13.8/14.0; 23.0/22.1 | 1.54/1.48; 2.74/2.66; 6.12/6.22; 13.83/14.03; 22.96/22.14 | yes (job sheets, C14 differenced) |
| Non-household Ml, 7 districts | 141.9/40.5/203.2/85.7/160.7/104.4/26.7 | 141.92/40.51/203.17/85.74/160.74/104.40/26.69 | yes (consumption, AMR, inlets) |

## Competing answers that survived
No fork moves a golden under the literal reading. Three residual forks, watch only:
1. EXERCISE valve-log rows on normally shut IC valves: ignored; counting them as open creates a loop, not a reasonable reading. Same call.
2. Flushing ask: mean of per-section ratios vs total water over total length. "per 100 metres of main flushed" reads as total over total and reproduces the golden; the mean-of-ratios reading would move 100 mm 2025 (2.75), 225 mm (13.97/14.13) and 300 mm (22.91/22.64). Ask only, not the call. Worth a closing phrase in the ask if the author wants the rounded digits safe.
3. Misregistered AMR customers (6641, 7233, 8131, 8432) must be re-placed by inference; data uniquely support one DMA each (step correlation 0.40 to 0.82, next best below 0.10). Ask only.

## Spec gates (checked by me on the unzipped bundle and metadata)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / 3 (csv, xlsx, pdf) | yes |
| Large file | 25,000+ rows | 157,704 inflow rows; 315,360 turbidity | yes |
| Distractors named, none labelled by file name | 2+ | 3 in metadata.json (condition assessment 2024, weather, regulatory taps); no file name says distractor | yes |
| Distractor unused yet weighable, none answers a graded quantity | yes | judge: none used by solution; none yields a graded figure | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt closes with units/rounding for all three figure types; asks are grids | yes |
| Shape and 25+ criteria | identifiable, 25+ | shape 07; design note estimates about 36 | yes (by design note count; rubric is generated downstream) |
| Not LLM-reading, goldens realistic | yes | judge found no authoring language; coherent dates, real-system noise | yes |

## Gate G reconciliation
Thread: mechanism other (network flow reconstruction), family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical; the card has no mechanism/family fields to contradict. The design note's decisive step (rebuild carried flow through the valve-log arrangements, not the register's normal positions) matches the thread's trap exactly, including the easy route flushing all six. The declared distractors (condition assessment, weather, taps) are not named by the thread as carrying anything. No mismatch.
**Gate G line:** method_or_model_selection, consistent; surface read = normal-position routing (six mains), not a declared distractor; no sole data defect.

## Gate H / 10-10 test
Thread: domain pass, layers pass, decisive_step analytical (borderline toward rule_application). Card analyst_test and note's Three rules: a strong analyst who conforms the meters, reads NOS 12 and the plan correctly and builds reference flows through the register's normal valves flushes six; only flows rebuilt through every logged arrangement give two. The note's enumerated family spans six, six, six, five, three, two mains.
Plain answer: yes, analytical. Cleaning and reading every rule correctly still leaves the easy route on six, because the standard files the reference as flow carried and no file or rule says how a main's past flow is built; no trunk flow is metered, so the decider is estimating it by mass balance through the network as it was operated. That is the choice of estimand and model for a quantity the field estimates, not a field reading or an executed procedure. Concession: after the valve log is composed the comparison is mechanical, which is why the thread hedged. The hedge is the standard-method caveat, and the stump power below carries it.
**Gate H line:** domain pass, layers pass, decisive_step analytical (thread hedged toward rule_application; reconciled as analytical, matches the card and note).

## Stump power (Gate F)
Two routes fail: normal-position routing (six) and taking works peaks without rebuilding carried flow. Margins are wide, so a solver who reconstructs gets two reliably. Landing risk: a strong solver who reads NOS 12 literally ("flow actually carried") will go to the valve log, because the log is the only file recording operated arrangements; mass-balance routing is a textbook step. Main thread should weigh this against the ladder: the call is landable by a thorough solver, and the ladder must lean on the asks (C14 cumulative meter, misregistered AMR customers, twin-hydrant lengths) to hold the top-two bar.

## Findings, ranked
1. None blocking.
2. Flushing ask, total-over-total vs mean-of-ratios: optional wording closure.
3. Thread's hedge toward rule_application: the main thread should keep the "no filed rule says how a past flow is built" sentence in the note intact.

## Next action for the author
Proceed to ship; optionally add a closing phrase to the flushing ask making water-over-length explicit, then re-run the free gates if the prompt changes.
