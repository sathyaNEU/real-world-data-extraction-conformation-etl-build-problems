# determinism-check report, task200, pass 3, 2026-11-03

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (estimand and comparison group), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pass 3 judged the bundle again (fresh unzip at /tmp/determinism-check-task200-r3/target/, 17 files) against the updated blocks. What changed since pass 2 is the Fell screen time: it is now 4,484.2 h (pass 2: 4,603.7). The Pier B close now respects the 20-minute rule in SPS-04 5.1. The longest Pier B span is 1,200 s, and spans end at own log-off, next log-on or shutdown (10,935, 5,688 and 5 spans respectively). That closes the live alternative that pass 2 flagged as finding 3.

## Why
The judge derived everything before reading the blocks against it. All the critical components, the order and all 24 supplementary cells reproduce exactly. SPS-04 section 3 pins team, screen time, search charging, certificate arithmetic and cancelled projections. The call rests on 4.2's "least likely to find a prohibited article in a passenger's cabin bag", which for a real bag is an article the screener has not been shown. The image IDs make exposure observable, and the repeat rate exceeds the first-meeting rate for every team (Fell 84 against 63).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| First-meeting rates (Fell, Brook, Dene, Esk, Arden, Cleve) | 63 (707/1,125), 69, 74, 77, 81, 85 | 62.84, 69.24 (3,480/5,026), 73.73, 77.15, 80.85, 84.93 | yes |
| Fell repeats | 4,104 of 5,229, 84% | same, 84.33% | yes |
| Overall rate | Brook 71, Fell 80 | 71.31 and 79.71 (Dene 75.4, Esk 78.6, Arden 81.9, Cleve 85.6) | yes |
| Screen time h | Arden 5,168.8; Brook 4,750.9; Cleve 5,545.6; Dene 4,593.8; Esk 5,297.1; Fell 4,484.2 | 5,168.815; 4,750.906; 5,545.590; 4,593.785; 5,297.090; 4,484.199 | yes (nearest edge 0.035 h, Arden and Dene) |
| Clear searches | 6,608; 4,399; 6,737; 6,429; 11,915; 5,683 | identical (all 51,588 trays matched, gaps 0.02 to 18 min) | yes |
| Expiring certificates | 4; 2; 3; 2; 5; 3 | identical (nearest: Dene 22 Jun 2027 inside, Cleve 9 Jul 2027 outside) | yes |
| Order | Fell, Brook, Dene, Esk, Arden, Cleve | same | yes |

## Competing answers that survived
| Reading | Result |
|---|---|
| Overall 2026 TIP rate (the surface read) | Brook, Dene, Esk, Fell, Arden, Cleve |
| First meeting, history 2026 only | Brook 70.8 first, Fell 77.2 |
| First meeting, history from 1 Jan 2025 | Brook 69.9, Fell 70.7 (Brook first) |
| Team-level "seen by anyone in the team" | call holds (Fell 60.0 against Brook 68.6), Arden and Cleve swap |
| Duplicates kept, or cancelled counted as seen | call holds (Fell 63.2 against Brook 69.2) |
| Certificates by LMS keyed date | 3/0/1/1/3/2 |
| Certificates from LMS-internal rows only | 8/5/10/4/10/6 |
| Search charged to the holder at taken time | 5,653 / 3,765 / 5,684 / 5,453 / 9,917 |
| Counting only the literal code CLEAR | about half |

The judge ruled out the last four: SPS-04 pins the assessment day and later pass, and "charged to the screener whose decision sent it" and "finds nothing at all" close the search readings. The residual fork is the history-cut reading, which discards shipped data and is not a licensed reading. Real prohibited finds are 9.1 to 9.7 per cent for every team, so they are no rival estimand.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 | yes |
| Large file | 25,000 rows or more | CT sessions about 121,885 rows, search log about 50k | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 (compliance PDF, throughput, queue time), unlabelled in names | yes |
| Deliverables | 1 to 3, all in golden | 2 | yes |
| Asks | multi-dimensional, unit and rounding stated | per team, hours to 1 dp, counts | yes |
| Prompt shape and 25 criteria | identifiable shape, 25 or more | shape 06; the count is not verifiable by me | unverified |
| Realism | not LLM generated | judge: nothing exclusion-level | yes (judge) |

## Gate G reconciliation
The judge's Gate G line is method_or_model_selection / analytical_non_defect / surface_read_dependency no / sole_data_defect no. This differs from passes 1 and 2 only in the mechanism label (previously statistical_rigor), and the substance is the same: an exposure-aware estimand on honest data. The design note's Three rules declares no decoy, no withheld rule and no ranking artifact, which agrees. No shipped artifact ranks the teams, and no declared distractor carries the surface read; it falls out of the obvious computation. Clean-data test: the stump survives perfectly clean data.
**Gate G class:** clean.
**Gate H:** domain: pass, layers: pass, decisive_step: analytical.
- Swap test: with "hospital" and "visits" nouns the task does not read the same.
- Layer 1: CT, Pier B, LMS, centre and search-log reconciliation. Layer 2: the repeat-exposure effect in TIP scoring.
- The first-meeting restriction is an analytical estimand choice recognised in TIP work, not data semantics or rule application. A strong analyst who cleaned every file and executed every SPS-04 rule would still file Brook first.
- The text only allows the restriction through the "cabin bag" wording and does not state it.

## Stump power (Gate F)
Good. The pull is strong: a solver who reproduces all three supplementary tables perfectly still files Brook on the overall rate, and d-prime is flat across teams. Only a solver who rebuilds per-screener exposure history across three years of exports and sees Fell's 4,104 of 5,229 repeats lands Fell. It is still the field's standard exposure-adjusted approach once the solver thinks of it (library `stumping` 1.3), so the main thread should weigh that against the design note's ladder.

## Findings, ranked
1. The first-meeting restriction is not stated, and 4.2 does not name TIP as the measure. A literal reader lands on Brook first. The judge rules that reading a surface read the "passenger's cabin bag" wording does not license. This is the one place a reviewer could contest, not a fail. The judge's optional fix is a WHAT sentence about articles in passengers' bags not previously shown to the operator, with no method.
2. The call is not fragile on the full history (a 6.4-point lead), but it flips if history is cut to 2025 or later. The 2024 and 2025 exports are not stated as required.
3. SOLUTION_STEPS step 5 does not mention the 20-minute cap on a Pier B span. The judge reproduced Fell's 4,484.2 with the cap (max span 1,200 s), which the step text as written would not give (pass 2 got 4,603.7 without it). The graded figure is right and SPS-04 5.1 files the rule, but the step should say so. This is a prose repair to submission.md only (SOLUTION_WRONG-class wording, not a task defect).
4. Pass 2's open Pier B close fork is closed by the cap.
5. The search-log code lists (NF, PA, RI, CLEAR) are documented nowhere and are inferable only from the month split. Minor, and no figure moves.
6. Rounding is safe: the nearest edge is 0.035 h and the first-meeting percents are at least 0.34 point from a .5 edge.
7. Not assessed: the cross-batch fingerprint and the 25-criteria count.

## Next action for the author
Edit step 5 in submission.md to say a Pier B stretch is capped at the SPS-04 5.1 twenty-minute limit, and confirm the golden xlsx and note carry 4,484.2 for Fell. Nothing else is required to ship on the determinism gate.
