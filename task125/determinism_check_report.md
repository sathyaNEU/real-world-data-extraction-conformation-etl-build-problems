# determinism-check report, task125, 2026-10-10

Pass 1. Scratch universe: `/tmp/determinism-check-task125-20261010T044207Z-8815/target/`, a fresh copy of `target/` (the folder ships no `target.zip`). The judge's verdict is at `/tmp/determinism-check-task125-20261010T044207Z-8815/verdict.md`.

Run note (read first): this harness exposed no Agent tool, so no separate judge thread could be spawned. The judge pass ran inside the orchestrator thread under the same isolation rules:
- It saw only `guidelines/determinism_judge_system_prompt.md` (v3, read in full), the blocks extracted from `submission.md` and the scratch copy.
- It recomputed every figure with pandas from the bundle.
- It wrote `verdict.md` before opening `metadata.json`, `golden/` or `DESIGN_NOTE.md`.

The orchestrator had also read the repo's `CLAUDE.md` and the submission's Tags block. Neither carries anything task-specific about the trap. Even so, the isolation is weaker than a separate thread. If you want a fully separated judgement, re-invoke the pass where the Agent tool is available. The cross-batch fingerprint check was not run, because the isolation rules forbid reading other task folders.

## Verdict
DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer is forced and reproduces from the shipped files.
- Methodology 4 pins the screen basis. Only gross payments (net plus VAT) of 1,000.00 to 999,999.99 with credit notes excluded reproduce all 63 statement figures. Net gives 30/63, and keeping payments of £1m and over gives 51/63.
- Methodology 5 pins the 2025/26 screen, which has 5 flagged cells. Waste & Environment 11 drops out.
- The Tenancy Sustainment term is 30 instalments in both rounds, and the scheme note rules out a new round.
- The Home First closure, read through the rate schedule and the payment history, puts 194 carer payments a run in cell 14 over the 13 plan-year runs.

Together these give 6,914 routed payments, so 6,900.

Gates A to G all pass. The send-back comes from the hygiene check alone. The decisive ledger reads as generated:
- Every flagged cell holds only the designed streams.
- Four of the five flagged cells have identical counts three years running.
- Direct-payment recipients never change.
- Supplier pools are reused across unrelated expense types.

Repairing this means regenerating ledger data, with a rerun.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Statement figures matched by the screen basis | 63 | 63 of 63 (gross, 1,000 to 999,999.99, credit notes out; spend CSV `net_amount`+`vat_amount`) | yes |
| 2025/26 flagged cells | ASC 14, HS 14, HT 49, HT 99, PF 12 | same (obs/exp 2,706/1,009.8; 2,706/176.8; 792/79.4; 432/39.5; 972/460.0); no near misses | yes |
| 2023/24 screen = cells in the run log | (implied) | ASC 14, HS 14, HT 49/99, WE 11, PF 12 | yes |
| 2024-25 round instalments in 2027/28 | 648 | 648 (tenancy CSV; 30-instalment term; all amounts in cell 14) | yes |
| HS cell 14, 2027/28 | 816 | 816 (648 + floating support block 14 a month) | yes |
| Carer payments in cell 14 per run, from April 2027 | 194 (102 now) | 194 = 102 + 60 single + 16 halves of 8 households + 16 one-guest households paid whole | yes |
| One-guest payment rule (decisive) | from 15 Nov 2023, 21 Aug 2024, 17 Sep 2025 | vendor pairs 701372/3, 701385/6, 701311/2; 3-to-2 guests stays in halves (701334/5, 5 Feb 2025) | yes |
| Carer runs in the plan year | 13 | 13 (BACS calendar 2027-28; December 2027 holds two by submission month) | yes |
| ASC cell 14, 2027/28 | 3,902 | 3,902 | yes |
| Plan-year total | 6,914 | 6,914 (ASC 3,902, HS 816, HT 1,224, PF 972) | yes |
| Order (docx 1) | 6,900 | 6,900 | yes |
| Largest department and count (docx 2) | Adult Social Care, 3,900 | Adult Social Care, 3,900 | yes |
| Fernhollow's closed-year figure (docx 3) | 8,100 | 8,102 → 8,100 (run log: October re-run replaces, January supplementary adds; rebuilt from the spend CSV with 0 mismatches) | yes |
| Gap (docx 4) | 1,200 below | 1,188 → 1,200 below | yes |
| Chart line / busiest month (docx 5) | 675 / Dec 2027, 700 | 675.2 / Dec 2027, 700 by run month | yes |
| April 2027 | 650 | 650 | yes |
| May 2027 | 632 | 632 | yes |
| June 2027 | 614 | 614 | yes |
| July 2027 | 596 | 596 | yes |
| August 2027 | 578 | 578 | yes |
| September 2027 | 560 | 560 | yes |
| October 2027 | 542 | 542 | yes |
| November 2027 | 524 | 524 | yes |
| December 2027 | 700 | 700 | yes |
| January 2028 | 506 | 506 | yes |
| February 2028 | 506 | 506 | yes |
| March 2028 | 506 | 506 | yes |
| April 2025 routed / examined | 634 / 628 | 634 / 628 | yes |
| May 2025 | 652 / 643 | 652 / 643 | yes |
| June 2025 | 664 / 656 | 664 / 656 | yes |
| July 2025 | 668 / 658 | 668 / 658 | yes |
| August 2025 | 673 / 667 | 673 / 667 | yes |
| September 2025 | 676 / 669 | 676 / 669 | yes |
| October 2025 | 681 / 675 | 681 / 675 (re-run batches; scheduled batches withdrawn) | yes |
| November 2025 | 663 / 656 | 663 / 656 | yes |
| December 2025 | 663 / 658 | 663 / 658 | yes |
| January 2026 | 685 / 680 | 685 / 680 (includes S1's 11) | yes |
| February 2026 | 669 / 661 | 669 / 661 | yes |
| March 2026 | 774 / 761 | 774 / 761 | yes |
| Q1 premium / unused charge | 27 / £0 | 27 / £0 (charged 1,927 against 1,900) | yes |
| Q2 | 94 / £0 | 94 / £0 (charged 1,994 against 1,900) | yes |
| Q3 | 0 / £1,553 | 0 / £1,553 (charged 1,989 against 2,200; 211 x £7.36) | yes |
| Q4 | 0 / £618 | 0 / £618 (charged 2,116 with S1 at the 25 minimum; 84 x £7.36) | yes |

## Competing answers that survived
None. Each fork below was built in full and closed by a shipped fact:

| Fork | Answer it produces | Shipped fact that closes it |
|---|---|---|
| Order last year's routed count | 8,100 | Methodology 5 (cells change), the tenancy term, the closure notice |
| Screen on net amounts | 8,300 | Methodology 4 (30 of 63 figures) |
| Keep the 2023/24 cells (WE 11) | 7,400 | Methodology 5; the 2025/26 statement was published 10 July 2026 |
| Carry tenancy at its 2025/26 count | 8,800 | 30 instalments in both rounds; the scheme note's "no further round" |
| Ignore the closure | 5,700 | Closure notice; "each run pays the four weeks ending on its payment date" |
| Joint households always paid in halves | 6,700 | The three one-guest transitions in the spend CSV |
| Half-payments left undecomposed | 6,500 | Every half doubles to a unique rate set on consecutive vendor numbers |
| 12 carer runs | 6,700 | 2027-28 calendar: 13 four-weekly runs |

The thinnest link is the one-guest rule. No document states it, and it is learned from three transitions. It still holds: the rival reading (the second carer happened to leave each time) needs three coincidences, and it is contradicted by the 3-to-2 household whose carers both stayed.

The headline sits 64 above the lower rounding boundary (6,850) and 36 below the upper one (6,950). That margin is thin but clean only because every non-designed stream in the flagged cells is exactly flat. See finding 1.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 20 | yes |
| Distinct formats | 3 or more | 7 (csv, xlsx, pdf, docx, eml, json, txt) | yes |
| Largest row count | 25,000+ rows or a large database | 408,795 (spend CSV) | yes |
| Distractors declared | 2 or more in `metadata.json`, none labelled under `target/` | `internal_audit_plan_2026-27.docx`, `household_support_fund_2026-27_allocations.xlsx`; no label in any name or file | yes |
| Distractors unused yet relevant | same world, worth weighing | Audit plan names the 2025/26 screen notification and the Shared Lives and Tenancy Sustainment audits. HSF allocations are Housing Support's 2026/27 awards, paid by partners. Neither is used. | yes |
| Distractor answering the decision or a graded quantity | reproduces, ruled out by a shipped fact | none answers either | n/a |
| Deliverable count | 1 to 3 | 2 (docx, xlsx) | yes |
| Format family | none required | not assessed, by spec | n/a |
| Multi-dimensional asks | no stacked lookups | 12 plan-year months, 12 x 2 closed-year months, 4 x 2 quarters, plus the order bridge and chart | yes |
| Golden deliverables present | every one named | both in `golden/`, and every figure matches the submission | yes |
| Units and rounding stated | every ask | "to the nearest hundred"; "whole payments", "whole pounds". The chart line's rounding is unstated, which is immaterial. | yes |
| Prompt shape and 25-criteria floor | identifiable, 25+ | 02 forecast across many periods; about 55 separately gradable figures | yes |
| Realism | nothing reads as generated; goldens read as real work | Spend CSV fails (finding 1). Golden memo contradicts its own evidence once (finding 2). All four docx (three input, one golden) carry python-docx default metadata (finding 6). | no |

## Gate G reconciliation
The judge and the design note agree on every field:
- forecasting as the primary mechanism, with method_or_model_selection at the screen rungs;
- `analytical_non_defect`;
- `surface_read_dependency: no`;
- `sole_data_defect: no`.

They also agree on the decisive step. The judge named the joint-household one-guest payment rule, and the design note places its decisive rung (rung 6) there too. Neither declared distractor was named as the surface read carrying the task.

So the build reads the same shape from the inside and the outside, and no send-back risk is predicted on stumping type.

Two notes, neither of which changes the classification:
- The design note's `## Gate G` block still quotes pre-harden figures (answer 6,522; rungs 7,632 and 5,742) against the built 6,914. Bring that block to the built ladder.
- The objective tag is Anomaly Detection & Diagnostics while the mechanism is forecasting. The tag is carried by rebuilding the screen and diagnosing what each flagged cell holds, and CLAUDE.md warns against retagging, so leave it.

## Stump power (Gate F)
Strong. The headline needs every rung right: the screen basis by reproduction, the screen year, the tenancy run-off on a term recovered from history, re-summing carer fees after the closure, recognising joint households, applying the one-guest rule, and the 13-run cadence.

The decisive trap is the joint households. Half-payments decompose into no rate set. A household left with one guest is paid whole, which is learnable only from three transitions, against an email asserting "the same carers the same amounts for three years". A strong model that does everything else files 6,700 (halves) or 6,500 (halves left undecomposed).

The judge named no too-easy signal that matters. The closure and the scheme's end are stated plainly, but the computation carries the difficulty.

## Findings, ranked
1. **Ledger realism (`wealdmoor_spend_over_500_2023-04_to_2027-02.csv`; SEND_BACK-class).** The ledger has four problems:
   - Every flagged cell holds only the designed streams. Every other expense type has zero payments in ASC 14, HS 14, HT 49, HT 99 and PF 12, while the cells either side carry Benford-scale counts (residential care: 558 in cell 13, 0 in 14, 669 in 15; repairs and maintenance: 823 in 11, 0 in 12, 736 in 13).
   - The flagged counts are identical in 2023/24, 2024/25 and 2025/26 (2,706, 792, 432, 972). The run log therefore routes 217 / 66 / 36 / 81 every month, and the golden chart shows near-identical bars from June 2025 to January 2027.
   - The 535 direct-payment recipients are each paid one identical amount every month for 47 months.
   - Supplier pools are reused across unrelated expense types (a coach firm paid for traffic-signal maintenance and street lighting; a cleaning firm for utilities, rents and capital works; a recruitment firm for counsel and software licences).

   **Change:** in the generator's background model, give each flagged cell ordinary payments from the department's other expense types, at recurring, year-stable volumes. Add starters and leavers before 2025/26, and map each supplier to a coherent expense type. Rebuild the statements, run log, Fernhollow files and goldens from the new ledger.

   Keep the background in flagged cells flat from 2025/26 into the 2026/27 extract. Noisy background would reopen the headline's 36-payment margin to 6,950.
2. **Golden memo contradicts its own evidence** (`golden/examination_calloff_2027-28.docx`). "Wendy's point that Shared Lives has paid the same carers the same amounts for three years holds for every year up to this one" sits beside the memo's own citation of changed households in November 2023, August 2024 and September 2025. **Change:** say her point holds for all but those three households.
3. **Critical Component 3 reads as a wrong sum** (`submission.md`). "194 ... (102 now): 60 single carers, 16 halves ... and 16 joint households": the listed parts total 92. **Change:** restate as "102 now plus 92 new: 60 ..., 16 ..., 16 ...".
4. **Step 2 omits the closing fact for the run-off** (`submission.md`). **Change:** cite `tenancy_sustainment_scheme_note.docx` ("No further round is provided for in the medium-term financial strategy 2026 to 2030") beside the 30-instalment term. Also note that the July and August 2024 households visibly stop at 30.
5. **The chart's 2026/27 bars are undocumented in the submission** (`submission.md`, Deliverable Answers). No log covers those months, and the March 2027 run is not in the extract. **Change:** carry over the golden caption's basis: April 2026 to January 2027 counted on the 2026/27 call-off's cells; February and March 2027 projected. Keep the rubric off those bar values.
6. **python-docx default metadata** in all three input docx and the golden docx. `app.xml` reads Words 0, Pages 1, TotalTime 0, and there is an empty APA bibliography customXml. **Change:** write realistic `app.xml` values and drop the stub customXml (a metadata-only edit).
7. **Authoring-flavoured line** in `calloff_working_papers_index.txt`: "none has been edited for this pack". **Change:** "none has been edited for this file of working papers".
8. **Fourth sheet in the golden workbook.** It has a `Notes` sheet where the prompt says "three sheets". Low risk. Fold the notes into the three sheet headers if a literal sheet-count criterion is a concern.

## Next action for the author
Rework the generator's background model so that every flagged cell also carries the department's other expense types at recurring volumes that hold flat from 2025/26 into the 2026/27 extract, and suppliers map coherently. Then regenerate the pack, confirm the order still files 6,900 with the background carried forward, and re-run this pass.
