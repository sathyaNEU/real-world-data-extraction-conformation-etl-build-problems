# determinism-check report, task470, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium, run r1) saw only a fresh unzip of target.zip and the five blocks. Executed literally, the shipped files give the seven qualifying fields (T13, A71, L08, U44, O16, F37, W33). Every committed figure reproduced. The only open step is the estimator in method 4.4. The ten counted fields pin it: unrecorded operations per never-recorded based piston airplane is near-constant (65 to 73, CV 4 percent), against capture rate (CV 50 percent) and operations per based aircraft (CV 42 percent). The seven are stable for any ratio from 56 to 923. Using only the four commissioned counts (69.76) or only the six towers (68.9) gives the same seven.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Unrecorded ops, ten counted fields | 23,376 | 23,376 (towers 2,544/2,368/3,290/2,512/2,988/2,768; F37 2,120, G42 1,928, D19 2,712, L08 146) | yes |
| Never-recorded based piston airplanes, counted fields | 338 | 338 | yes |
| Operations per airplane | 69.2 | 69.16 | yes |
| Never-recorded airplanes, 20 uncounted fields | T13 33 ... D73 3 | all 20 exact | yes |
| 2026 lead, 24 fields (kg) | 22 down to 2 | 22.13 ... 1.83, all round to the golden | yes |
| Towered ops and lead | 17,600/9,900/19,400/12,200/13,600/7,900; 22/18/23/16/16/13 | 17,625/9,916/19,414/12,191/13,616/7,928; 22.1/17.9/23.2/16.0/16.0/12.9 | yes |
| Events kept in Pacific 2026 | n/a | 186,494, all resolved to a registration | yes |
| Wrong sets (8 pooled, 9 split, 8 per based aircraft) | named in the recommendation | reproduced | yes |

## Competing answers that survived
- Method 4.4 does not name the estimator (Gate C, mild). The data and the network notes close it by leave-one-out on the ten counts. The reading of "fields with a count" does not change the set.
- Towered fields' "piston-engine operations" (supplementary ask 3): the golden takes unrecorded tower civil operations whole as piston (methods 4.2 and 3.2). Scaling by the recorded piston share would give HWK 17,264, CRV 9,241, OSY 19,268 and leads of 21.5 and 16.8 kg for HWK and CRV. The literal method closes it, but the prompt wording invites the other reading. This is an ask-side fork only; the main call is unaffected. Advisory.
- Never recorded anywhere versus at the home field, changeover-day events (17, under 0.1 kg total) and the tower closing minute (KTY by 1 operation) move no rounded figure and no qualifier.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | csv, txt, xlsx, pdf | yes |
| Large file | 25,000 rows or more | 187,403 rows (adsb events) | yes |
| Distractors named, none labelled in a file name | 2 or more | metadata.json names airport_master_records_5010.xlsx (declared wrong-basis) and cvaqd_lead_monitoring_2026.csv; no file name labels one | yes |
| Distractors unused yet weighable | yes | 5010 gives operations estimates (all aircraft, 2018 to 2025), ruled out by its own notes and method section 4; lead monitors sit at two towered fields and rank no candidate. I did not recompute the 5010 arithmetic myself; the judge reproduced the per-based-aircraft 8-field set from it | yes |
| Deliverables | 1 to 3, all in the golden | 2 (csv, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24-field lead and 6 towered fields; whole kg and nearest hundred stated | yes |
| Prompt shape and rubric | shape identifiable; 25 or more criteria | shape 01 (candidates against a cap); rubric is generated at ship, 24 fields plus 6 towers plus components make it reachable | yes (rubric not yet generated) |
| Not LLM generated | yes | judge: no authoring leakage, real FAA layouts, coherent dates | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: the decisive step is the choice of estimation auxiliary (never-recorded airplanes) over a capture share; the default path, a pooled 0.815 capture rate, gives A71 F37 K58 L08 P05 S27 T13 T61, and the split by flight training gives nine. These match the thread's wrong sets exactly. The declared distractor (5010) does not carry the task: it yields a different wrong set, and the thread names the capture-rate scaling as the surface read. No finding. Gate G passes.

Gate H: domain pass, layers pass, decisive_step analytical. This matches the note's Three rules (domain: emissions-inventory ratio estimator; Layer 1: UTC against Pacific, register history, N-number forms; Layer 2: estimation_fit; No decoy, Not semantics, Not rule application). No mismatch.

## Stump power (Gate F)
The capture-rate route and the per-based-aircraft route both file a wrong qualifying set, and leave-one-out on the counts separates them from the golden. The risk is that it is somewhat easy: the receiver notes state the broadcast-and-record rule, and the register join is mechanical. The portal is the measure.

## Findings, ranked
1. Advisory, ask 3: restate in the solution or write-up that unrecorded tower operations are taken whole as piston under method 4.2. Note only; no rebuild.
2. Advisory: method 4.4 is silent on the estimator. This is mild, closed by the data, and the main call is stable.
No send-back finding.

## Next action for the author
Proceed to ship stage 5. Optionally add one clause on the whole-piston treatment of unrecorded tower operations to the submission step list (note-only, no regeneration).
