# determinism-check report, task479, 2026-11-03

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance (capacity-constraint emission calculation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Process note: the runtime had no Agent tool, so the judge thread was spawned by the main session from /tmp/determinism-check-task479-r1/judge_brief.md. Its verdict is /tmp/determinism-check-task479-r1/verdict.md (copy of the substance below). Design note and metadata.json were read only after it returned.

## Why
From the shipped files alone, minute-summed vent flow exceeds RTO-1's 3,800 scfm maximum (cvs1 register) in about 10,000 RUN minutes; D.1 defines emitted as released to atmosphere and the register has PSV-31 discharging to atmosphere. Proportional release of the excess gives 3.196 tons against the 2.5-ton limit (B.1), over by 0.7. All three asks reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Q1/Q2/Q3/Q4 tons | 1.4/0.7/0.5/0.6 | 1.376/0.709/0.495/0.615 | yes |
| Year to date | 1.4/2.1/2.6/3.2 | 1.376/2.085/2.580/3.196 | yes |
| Margin over limit | 0.7 | 0.696 | yes |
| PSV-31 release | about 2,700 lb | 2,704 lb | yes |
| Controlled-only figure | 1.9 | 1.85 | yes |
| Solvent lb (7 solvents) | 1,435,200 / 855,300 / 55,100 / 108,700 / 295,500 / 47,900 / 88,700 | 1,435,218 / 855,321 / 55,136 / 108,670 / 295,472 / 47,868 / 88,702 | yes |
| Quarter lb | 659,500 / 660,600 / 775,200 / 791,100 | 659,502 / 660,561 / 775,198 / 791,127 | yes |

## Competing answers that survived
None on the call. Literal alternatives: no PSV pathway (1.9, within) and hourly capacity check (2.1, within) are the declared easy routes, closed by D.1 plus the register facts; whole-minute VOC release (11.3) contradicts the fan still drawing 3,800. DST/EST, Orbitas boundary, half-open intervals (pinned by B.3), hold-for-dryer rows, wash rows, Nm3 correction: all stay over 2.5 and round to the golden or shift only the figure (3.06 to 3.36 under non-natural readings). Residual sensitivity: the over call needs at least about 48 per cent of the proportional excess released; the golden reading is the coherent one but this is the thinnest point.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | 4 (xlsx, pdf, csv, parquet) | yes |
| Large file | 25,000+ rows | rto1_dahs_1min_2026.csv 525,600 | yes |
| Distractors | 2+ in metadata, none labelled in file names | 3 (EU-B1 boiler, EU-G1 generator, LDAR); names neutral | yes |
| Distractors unused yet weighable | yes | none answers a graded quantity; each ruled out by a shipped fact (own stack, own condition, own unit) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | quarters x YTD, 7 solvents, 4 quarters; units and rounding stated | yes |
| Prompt shape / rubric 25+ | yes | shape 15 (fields to one schema), 25 criteria per design note (not independently generated here) | yes |
| Not LLM-reading, goldens realistic | yes | judge: operational artifacts with plausible noise; AQ-117 and determination are work products | yes |
| Prompt | one paragraph, under 1,000 chars, no counts | 668 chars; no count the data hold | yes |

## Gate G reconciliation
Thread: mechanism etl_conformance, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card/design note: strategy binding_constraint, gap objective, Layer 2 allocation_constraints, stump_class analytical. Consistent. Gate G line: PASS, no shipped artifact ranks the candidates wrong; the AQ-117 ships blank; declared distractors are not a surface read carrying the task (they are other emission units). Difficulty survives deleting wrong numbers (nothing wrong is shipped).

Gate H line: domain pass, layers pass, decisive_step analytical (matches the note's Three rules: No decoy, Not semantics, Not rule application). Thread caveat: the PSV-31 pathway is inferred from register facts and D.1, not stated; classed domain reasoning, not a withheld rule. Main thread should weigh this against the "decisive rule left unstated" ban; the note's Pins and SF1/SF11/SF12 rows close it.

## Stump power (Gate F)
Good on paper. Easy routes (99.4 percent on all RUN gas 1.9; hourly capacity 2.1) both land within limit; 3.2 needs minute-level coincidence plus three clocks, PX conversion, migrated step, uncontrolled OFF/WARMUP. Honest risk: a solver who reads the register's fan maximum and PSV-31 lands the call; exact quarters still need the full stack, and asks 2 and 3 add reconciliation traps. The decisive step is an expert-recognised capacity check, a landable call for a strong solver (stumping 1.3), not a data-semantics step.

## Findings, ranked
1. Thin point: over-limit call holds only if at least about 48 percent of proportional excess is released; PSV-31 pathway is inferred, not filed (non-blocking, closed by D.1 and register).
2. Minor: cmms WO26101785 RTO-1 planned outage 07-21 to 07-31 vs DAHS RUN until 07-29 (DAHS is the B.7 record; golden unaffected).
3. Minor: PSV-31 last inspected 05-20 in the register vs 05-21 in WO26101668.
4. Process: leak reader result for stage 4 was not part of this pass; rubric criteria count not independently verified.

## Next action for the author
Proceed to stage 5 on the current cut; optionally align the CMMS outage open date and the PSV-31 inspection date in the generator (cosmetic, would require a rebuild and fresh gates).

## Main-thread disposition (2026-11-03)
1. Ruled, no change to the record: RTO-1's 3,800 scfm is a hard cap on the draw and, while RTO-1 is in RUN, PSV-31 at the inlet plenum is HDR-1's only outlet besides RTO-1 (XV-30 opens only out of RUN), so the whole proportional excess leaves untreated; fork row SF18 in the design note, asserted in checks.py SF18 (proportional release 2,704 lb, 3.196 tons, over; the call holds at 48 per cent of it or more).
2. Fixed in the generator: the planned outage order (now WO26101811) opens 2026-07-29 00:40 local, 20 minutes before the DAHS shows RTO-1 OFF, and closes 2026-07-31 09:35, after RUN resumes; checks.py S13.
3. Fixed in the generator: the register's PSV-31 last-inspected date is 2026-05-21, the date of WO26101668; checks.py S13.
4. Noted: the leak reader ran in the same stage; the rubric count is the shape's in the design note.
No graded figure moved (figures_check 54 of 54, freeze.py determinism PASS); no re-judge, the verdict being APPROVE with no FIX_NOW.
