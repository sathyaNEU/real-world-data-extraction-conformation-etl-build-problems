# determinism-check report, task177, 2026-10-28 (pass 3)

## Verdict
DETERMINISTIC

**Disposition:** APPROVE. No repair is needed and no model rerun is required; the thread's one optional wording note on step 3 moves no figure.

**Stumping type:** mechanism: forecasting (also method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
This pass re-judges the build after the portal's determinism return of 2026-10-28. Both portal judges failed Gates C and D (competing_defensible_answer, underspecified_objective): nothing shipped said which repayment regime the forecast carries across the cyclone of 16 October 2026, and responses calibrated on December 2026, on November and December, or on everything after landfall filed 500, 800 and 1,100 against the committed 300. The repair added one clause to the term sheet, clause 12 (Assessment basis): the Assignee prices the pool on its forecast of the pool's loans 90 or more days past due on 30 June 2027, made from the pool as it stands at the cut-off and taking members' repayment from 1 January 2027 to be as it was in the Assignor's experience before the cyclone. It files the WHAT (the population at the cut-off and the forward window's repayment conditions) and no method.

The isolated thread wrote its derivation from `target/` before opening the graded blocks. It reads the estimand as filed literally (the pool at the cut-off, 90 or more days past due on 30 June 2027, repayment from 1 January 2027 as before the cyclone, nearest 100), with operating policy sections 4 and 6 fixing the payment codes and the days-past-due clock, and a NOT_PAID instalment absorbing in the ledger, so a loan is 90 or more days past due on 30 June exactly when its first miss falls due on or before 1 April 2027. The count of members the loan's group was carrying at its last meeting separates the candidate methods on held-out data (log-loss times 1e-4 on April to June 2026 after training to December 2025: no feature 393, the member's own payment 380, an any-carried group flag 345, the carried count 321) and gives 276 to 302 loans under every specification it ran, 300 in each. The branch guardrail ask reproduces on all fourteen rows. No Gate A to E failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pool loans, principal | 12,880, INR 4,104.15 lakh | 12,880, INR 4,104.151 lakh | yes |
| Pool loans by members carried at the group's last meeting (none, one, two, three or more) | 9,082 / 3,372 / 412 / 14 | 9,082 / 3,372 / 412 / 14 | yes |
| Groups carrying two or more, loans in them | 97, 426 | 97, 426 | yes |
| Six-month 90-day rates by state | 0.34 / 3.11 / 31.15 / 100 per cent | 0.35 / 3.2 / 29.9 per cent on both platforms' eras (its own windows); the three-or-more cell rests on one September 2025 meeting | yes, the forecast in the same cell |
| Forecast | 278.1, 300 | state bins 268 to 277, logit 276 to 302, every one 300 | yes |
| Branch breaches, total | 2,528 borrowers, INR 821.3 lakh | 2,528, INR 821.33 lakh | yes |
| Branch rows (borrowers, INR lakh) | the fourteen rows as filed | identical on all fourteen | yes |

## Competing answers that survived
None. The forecast routes the thread ran, each with its answer:
- the member's own payment, or an unconditional hazard before the cyclone: about 91 to 120 (100), the default path, an easier method on the same estimand;
- a group flagged for carrying anyone: about 180 (200);
- a member-level logit on the payer's burden (the thread's own first derivation): 165 to 178 (200), dominated by the carried-count model on the same held-out data;
- the group's carried count: 276 to 302 (300), the golden;
- a hazard calibrated after landfall: about 1,550, ruled out by term sheet clause 12.

The distance to the 250 and 350 edges is about 25 or more under every specification. On the branch ask, no SFB0014 de-duplication (2,572, INR 842.9 lakh), no parent or successor mapping (2,759, INR 891.0 lakh), the bureau's summary columns (2,796) and GOLD and KCC lines counted (3,162) are each closed by CPN-MF-07 sections 2 and 3.

## Spec gates
Checked by the main thread against the unzipped bundle.

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, parquet, pdf, xlsx | yes |
| Large file | 25,000 rows or more | Kshetra parquet 776,608; CollectPro 333,018 and 445,272; bureau review 54,991 | yes |
| Distractors | 2 or more named in metadata.json, none labelled by a file name | 3 (credit-life claims, field officer postings, portfolio report), each with why_relevant, why_unused and ruled_out_by | yes |
| Deliverables | 1 to 3, each in the golden | pool_90dpd_forecast.xlsx, pool_purchase_note.docx | yes |
| Asks | multi-dimensional, unit and rounding stated | fourteen branches by two figures, INR lakh to one decimal, in the prompt's last sentence | yes |
| Shape and rubric | 25 or more criteria | the forecast, four state counts, two group figures, 28 branch figures, the chart | yes |
| Realism | nothing reads as generated | the thread's hygiene PASS; the only change since pass 2 is one term sheet clause | yes |

## Gate G reconciliation
Thread: mechanism `forecasting` (method_or_model_selection by held-out validation), stumping_family `analytical_non_defect`, surface_read_dependency `no`, sole_data_defect `no`; Gate H `domain: pass`, `layers: pass`, `decisive_step: analytical`.

Card and design note: `stump_class: analytical`, `gate_g: binding_constraint` (a group carries one short member at a meeting and stops at two), `analyst_test` filing 100 against 300, `domain_test` on the loan's group; `## Three rules` names the decisive step as conditioning each loan's six-month default on how many members its group was carrying at its last meeting. No mismatch, as in passes 1 and 2. No distractor is named as the surface read carrying the task. The thread reads clause 12 as fixing the estimand and the forward condition, which is how the fourth leak reader read it (question 1: "states the estimand and condition, not the method").

## Stump power (Gate F)
The thread rates it good: the easy routes file 100 (each member's own payment) and 200 (any carried member), both cleanly wrong, and 300 needs the group's carried count as the unit, a threshold effect the policy's "GRP_SUPP counts as paid in full" hides.

Main thread weighing. The thread's own first derivation, a member-level logit on the payer's burden, filed 200, and it reached 300 only through the held-out comparison, so the step needs a judgment the data settles rather than a filed rule. Against that, the portal's returned round had already built group-state reads and parted from the golden only on the calibration regime (500, 800 and 1,100); with clause 12 filed, a response taking that route lands 300. The ladder still holds a response that reads each member's own payment or flags any carried member; whether one of the top two stays off the call on the next round is the portal's measurement.

## Findings, ranked
1. **(Optional, no figure moves) Step 3's history windows and the thin three-or-more cell.** The month ends to 30 June 2026 have 181-day windows that partly close after landfall, and the three-or-more cell is one meeting at 100 per cent. The write-up already gives the reading from month ends whose windows closed before landfall (277.4, the same 300), and with the three-or-more cell at the two-or-more rate the forecast is about 269 to 277, still 300. Not applied: the 14 loans in that cell move the forecast by about 10 at most, against 28.1 to the nearest edge.

## Next action for the author
Reship as built (zip `3a18f553c3611317`) and send it to the portal.
