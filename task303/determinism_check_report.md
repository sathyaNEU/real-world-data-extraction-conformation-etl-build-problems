# determinism-check report, task303, 2026-10-25

## Verdict
NOT_DETERMINISTIC, SOLUTION_WRONG on the headline figure
**Disposition:** SEND_BACK
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The product is forced: Essentials leads under every specification the thread tried (Essentials 0.32 to 0.44, Lifetime
Cat about 0.16, Condition Year about -0.02, Lifetime Dog about -0.32, CAD million). The figure is not: the thread's
best-faith construction (a logit on the offered change and age by product, claims by age band and continuing condition
at the start of the policy year) gives 0.425, which prints 0.4, and the timing of the condition flag on the 2025 base
moves it to 0.32. The golden's 144 constructions print 0.5 (0.463 to 0.509), so across the licensed family the printed
figure runs over three cells at CAD 0.1 million. Critical components 1 and 2 depend on how a continuing condition is
marked and do not reproduce at their printed precision.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Call | Essentials | Essentials under every specification | yes |
| Addition | CAD 0.5 million | 0.425 best faith; 0.32 to 0.437 over variants | no |
| Component 1, lifetime renewal with and without a continuing condition | 95 and 70 per cent | 97 and 69 (Dog), 97 and 75 (Cat), observed | no |
| Component 2, Lifetime Dog 2025 claims with and without | CAD 2,260 and 420 | 2,375 and 424 (flag at year start), 2,185 and 339 (at year end) | 420 only |
| Ask A calls, 16 cells | listed | identical, option 2 before 5 October and option 3 after, read from the wrap codes | yes, against the dictionary's menu |
| Ask B complaints, 16 cells | listed | identical with the acknowledgement quarter for the 171 letters-only cases; CR-26-01142 sits between case numbers received 30 September and 1 October | yes, one boundary case read |
| Ask C instalments, 16 cells | listed | identical with the re-presentation window rolled to the next banking day (10 to 16 days); exactly ten days gives 1,955 against 2,813 | yes, under the rolled window |

## Competing answers that survived
- The addition: CAD 0.3, 0.4 and 0.5 million under licensed condition markings, flag timings and response fits.
- Lifetime Dog Q3 and Q4 complaints: 44 and 45 against 45 and 44, on one letters-only case at the quarter boundary.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, parquet, docx, xlsx | yes |
| Large file | 25,000 rows | pad_collections_2026-27.csv, 376,301 rows | yes |
| Distractors | 2 or more, named in metadata.json | vet fee benchmark, clinic network | yes |
| Deliverables | 1 to 3 | a PDF and a workbook | yes |
| Asks | unit and rounding stated | stated | yes |

## Gate G reconciliation
The thread's mechanism (statistical rigor: heterogeneous price response and adverse selection on honest data) matches
the card's stump_class analytical and the note's decisive step. No distractor named as the surface read.

## Stump power (Gate F)
The thread rated it good once the figure is fixed: the pooled route names Lifetime Dog at +1.06 and the split route
turns Lifetime Dog negative. The scored readers measured otherwise: reader A named Essentials with a claims-aware
retention model by product (lifetime claimants almost never leave) without marking any condition, so the decisive
step is reachable by a standard covariate reflex.

## Findings, ranked
1. The headline figure is not forced at CAD 0.1 million (SEND_BACK).
2. Components 1 and 2 depend on the unfiled condition marking.
3. The dictionary states the menu as it stood at the extract; the golden reads the earlier option from the wrap codes.
4. Letters-only complaints carry no received date; one case sits on a quarter boundary.
5. Step 7's "ten days later" does not execute literally against the banking-day roll.

## Next action for the author
Architecture 1 is spent (reader A landed the call, the judge returned SEND_BACK and both readers took every ask cell):
re-root task303 at stage 1.
