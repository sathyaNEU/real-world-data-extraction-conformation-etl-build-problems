# determinism-check report, task267, 2026-11-01 (pass 4)

Judged on the prompt as it stood in the brief (billing ask: "for each month, what the laboratory billed us..."). The later edit ("from March to November") is not covered here.

## Verdict
NOT_DETERMINISTIC (ask 3 only; main call and asks 1 and 2 hold)
**Disposition:** FIX_NOW (the thread wrote SEND_BACK; the fix is a one-ask prompt pin and the call, shares and cartridges do not move, so I class it FIX_NOW and a re-judge is required)
**Stumping type:** mechanism: statistical_rigor (verification-bias reweighting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Invoice lines hold tests done 21 Nov to 25 Dec 2026. The prompt names no window. The golden lists March to November in full calendar months. Literal readings: every month billed (adds December: 17,748.50 net, 17,055.50 adults screened); season days only (November = 30,992.50 / 30,530.50, against the golden's 47,509.00 / 46,739.00); the golden's whole months. The golden applies season days only to the cartridges but not to billing, so it matches neither literal rule. Label underspecified_objective. Clause 2.3 (the season dates) makes the inconsistency sharper.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Adults | 37,269 | 37,269 | yes |
| Complete OGTT / diabetes | 10,715 | 10,715 / 1,117 | yes |
| Six rule shares | 51/79/80/62/90/93; 8.4/24.9/28.2/35.9/36.3/49.3 | same | yes |
| Cartridges A01 to A12, total | 40,248 | same | yes |
| Billing March to October | as golden | same | yes |
| Billing November | 47,509.00 / 46,739.00 | window-dependent | no (fork) |

## Competing answers that survived
Ask 3 window: whole calendar months March to November, versus season days only, versus every month billed (adds December). Nothing shipped closes it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, rows | 10+, 3+, 25k+ | 12, 4 (csv, txt, xlsx, pdf), run log 49k | yes |
| Distractors | 2+ in metadata, not in file names | feedback, 2024 profile (calendar and close-out also noted by the thread) | yes |
| Deliverables | 1 to 3 | 2 | yes |
| Asks state unit and rounding | yes | yes | yes |
| Rubric 25+ criteria | 25+ | not verifiable from the pack | open |
| Realism | no LLM tells | thread found none | yes |

## Gate G reconciliation
The thread named verification-bias reweighting and analytical_non_defect. Both match the design note (stump is whom the two-by-two table represents). No declared distractor carries the task.

## Gate H
domain pass, layers pass, decisive_step analytical. This matches the note's `## Three rules`.

## Stump power (Gate F)
Good. The easy route is the unweighted complete-test table, which gives R26A60 at 94%. Only protocol 6.2 hints at weighting, and the method is unfiled.

## Findings, ranked
1. Ask 3 window unpinned (December invoices exist). The pass 3 note called this harmless; the cold thread did not.
2. Rubric count unverified.

## Next action for the author
Pin ask 3's window in the prompt, regenerate the golden if it moves, and re-judge once.
