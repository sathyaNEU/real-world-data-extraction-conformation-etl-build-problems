# determinism-check report, task273, 2026-10-28 (pass 3, architecture 5)

This is the first judge pass on architecture 5 (the Tallowbark Networks minimum-load substation
designation, load-forecasting), run on target.zip 3d17e193; the judge wrote it as
`determinism_check_report_pass3.md` and the build renamed it to this file, replacing architecture 4's final
report, which stays in git history. `determinism_check_report_pass2.md`, `determinism_check_report_a4_pass1.md`
and `determinism_check_report_portal.md` judge earlier architectures and are kept as history. The shipped
target.zip is f641cf2c: after this pass the prompt's further-capacity clause was narrowed to "before any of
those half-hours fell below its threshold", the solar outlook's header lost the reference day's date, the
applications register's substation column was named `zone_substation_at_approval`, and the voltage
enquiries' outcomes and the outlook's basis text were redrawn; no graded figure moved. The isolated judge
thread saw only a fresh unzip of `target.zip` plus the five extracted blocks, and never opened
`submission.md`, `DESIGN_NOTE.md`, `metadata.json`, `generator/`, or any earlier report.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution (secondary: forecasting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call (7 of 16 substations designated: Gerrimbal, Kinnabar, Mundaree, Ondarra, Quorrabin,
Tarravine, Wirrandel) and every figure in all four asks of `minimum_load_spring_2027.xlsx` were
independently recomputed by the judge thread from the raw shipped files and matched exactly to the
stated rounding, including the two thinnest margins (Gerrimbal 0.6 MW, Quorrabin 0.7 MW). The decisive
step is forced by `approved_meter_models.xlsx`'s meter-model descriptions joined through
`metering_installations_2026-12-11.csv` to `load_control_register_2026-12-10.csv`: 23,257 of 31,832
controlled-load heaters sit on meters with an integral audio-frequency receiver (reached by
`network_notice_NN-2027-02.pdf`'s new signal) and 8,575 sit on meters with an internal time switch
(not reached, so they keep heating overnight). This join reproduces exactly and is not a toss-up: the
"easy" route of applying the new switch-on times to every controlled-load heater gives a specific,
different, named wrong answer (4 substations, clearing Kinnabar, Quorrabin and Gerrimbal), and the route
of applying no soak load at all gives another named wrong answer (11 substations). No committed answer
(main call or any of the four deliverable asks) is affected by any defect.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reference day / lowest network half-hour | Sun 25 Oct 2026, -153.3 MW | -153.311 MW, same day, after UTC-to-local/DST conversion | Yes |
| Heater reach split | 23,257 AF-receiver / 8,575 time-switch of 31,832 | 23,257 / 8,575 (meter-model join) | Yes |
| All 16 substations' forecast lowest demand (ask 1) | per submission | all 16 match, incl. thresholds and designation flags | Yes |
| Designated set | 7 (Gerrimbal, Kinnabar, Mundaree, Ondarra, Quorrabin, Tarravine, Wirrandel) | same 7 | Yes |
| Curtailment, 7 designated substations (ask 2) | 0.6-1.1 MW | all 7 match exactly | Yes |
| Further capacity, 9 cleared substations (ask 3) | per submission | all 9 match exactly | Yes |
| In-service / backstop solar, all 16 (ask 4) | 254.64 MW / 32.50 MW total | matches exactly, after chaining `der_applications_2026-12-08.xlsx` through `prior_application` per independent root (the file holds up to three parallel "New connection" roots per NMI, not one linear history) | Yes |
| Rejected "four" (every heater reached) | named in FINAL_RECOMMENDATION | reproduces as a specific wrong set, clearing Gerrimbal/Kinnabar/Quorrabin | Yes |
| Rejected "eleven" (no soak load) | named in FINAL_RECOMMENDATION | reproduces as a specific wrong set | Yes |
| Naive single-root DER chain (ask-4 undercount) | not committed | ~248.0 MW vs shipped 254.64 MW (~2.5% understatement), a real and distinct wrong answer | Confirms the parallel-root trap is load-bearing, not decorative |

## Competing answers that survived
None. The judge thread enumerated the two named alternative heater-reach routes (every heater reached;
no soak load at all) and the naive single-root DER chain, and all three reproduce as specific, different,
wrong answers rather than defensible alternatives to the golden; none survives as a competing defensible
answer to any committed figure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 12 files in `target/` | Yes |
| Format mix | >=3 | csv x5, xlsx x3, pdf x3, json x1 (4 formats) | Yes |
| Large file | >=25,000 rows, or large DB | `metering_installations_2026-12-11.csv` 114,571 rows; `cl_customer_reads_spring2026.csv` 78,047 rows; `zss_net_demand_spring2026.csv` 69,856 rows; `der_applications_2026-12-08.xlsx` 53,400 rows (design note) | Yes |
| Distractors declared, unlabeled by filename | >=2, named in `metadata.json`, no filename gives it away | `summer_demand_outlook_2027-28.pdf`, `voltage_enquiries_2026.csv`; both named only in `metadata.json`, neither filename says "distractor" | Yes |
| Distractor relevance / unused | relevant enough to weigh, unused by solution; one reproduces an answer to a graded quantity, ruled out by a shipped fact | Both are genuine, on-topic Tallowbark planning artifacts (summer peak-demand outlook; power-quality complaint log) a network planner's desk would hold; design note confirms deleting either leaves every golden and ask figure unchanged (`checks.py`). Neither file is shown, in the design note or by this pass, to *arithmetically reproduce* a graded figure before being ruled out by a shipped fact -- this specific sub-requirement is not documented. Not a determinism defect, but worth tightening for the author (see Findings). | Partial |
| Deliverables | 1-3, present in golden, no format family required | 2 (`minimum_load_spring_2027.xlsx`, `minimum_load_briefing_2027.docx`), both present in `golden/` | Yes |
| Asks multi-dimensional, unit + rounding stated | yes | all 4 asks are multi-row (16/7/9/16 rows) with unit and rounding stated in the prompt's closing sentence | Yes |
| Prompt shape / rubric >=25 criteria | identifiable shape, rubric size | prompt shape (multi-candidate threshold screen + briefing) is identifiable; rubric criteria count not present in this task folder (no rubric file read by this pass) to verify numerically | Not verified |
| Realism / not LLM-generated | yes | judge thread hygiene check: PASS, no README/benchmark/solver-facing language, dates internally coherent, no public/verbatim dataset | Yes |

## Gate G reconciliation
Judge's Gate G/H: `mechanism: decomposition_attribution` (secondary `forecasting`), `stumping_family:
analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`; `domain: pass`, `layers:
pass`, `decisive_step: analytical`. The card's `stump_class: analytical`, with `analyst_test` and
`domain_test` (`.claude/skills/fingerprint/cards/task273.json` lines 34-35) and the design note's `##
Three rules` (lines 21-35) name the identical mechanism in the same words the thread arrived at
independently: the decisive join is "which controlled-load heaters the new signal times actually
switch," found only through each heater's current meter and that meter's model, and the named easy-route
wrong answer is the same 4-substation set (clearing Gerrimbal, Kinnabar, Quorrabin) in both the card and
the judge's H3 line. The design note's "Not semantics" and "Not rule application" lines argue the same
case the thread made unprompted: every field and register id can be read correctly and the easy route
still lands on the wrong set, because no filed sentence says which heaters the signal reaches. This is a
clean match, not a mismatch -- the thread was not told the design or the card, and converged on the same
classification, which is itself evidence the H3 analytical call is sound rather than a self-serving
author assertion. The library's load-forecasting method here (reference-day replay, solar-adjusted
threshold comparison) is the field's standard route; the thread's finding that it took independent
judgment (the device-reach join, the parallel DER-chain reconstruction) to execute it correctly, with no
textbook shortcut, supports landing the call as `stumping` 1.3 intends.

## Stump power (Gate F)
The thread rates stump power "strong," citing four independently load-bearing difficulties: the
device-reach join (not a flat read of the notice), manufacturer-specific controlled-load register codes,
UTC/local/DST reference-day selection, and the non-linear (parallel-root) DER application chain for
ask 4. Two margins are thin (Gerrimbal 0.6 MW, Quorrabin 0.7 MW) but fully and uniquely determined with
no estimation freedom, so Gate C's margin-robustness test is satisfied rather than flagged. The three
named wrong answers (4, 11, and the ask-4 undercount) are concrete, reachable failure modes for a
competent but insufficiently careful analyst, consistent with the design note's enumerated family
(designated sets of 4, 5, 7 and 11 across nine alternative constructions).

## Findings, ranked
1. (Minor, non-blocking) The design note documents that both distractors are deletable without moving
   any figure, but does not show either one *arithmetically reproducing* a graded quantity before a
   shipped fact rules it out -- the stronger form of the distractor-relevance gate. Not a determinism
   defect; tighten the design note's distractor rationale if revisited, no rerun required.
2. (Informational) The task folder does not contain a rubric artifact this pass could use to verify the
   >=25-criteria floor numerically; nothing here suggests a problem, just unverified by this pass.
3. No Gate A-E, F, G, or H finding. No fix location applies.

## Next action for the author
None required; ship as-is. If revisiting the design note, add one sentence showing one distractor's
numbers plausibly answering a graded quantity and the shipped fact that rules it out, to make the
stronger distractor-relevance gate explicit (optional, does not block shipping).
