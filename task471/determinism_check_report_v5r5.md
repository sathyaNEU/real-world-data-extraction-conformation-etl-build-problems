# determinism-check report, task471, 2026-10-31 (pass v5r5, the one re-judge of the v5r4 FIX_NOW)

## Verdict
DETERMINISTIC. No SOLUTION_WRONG: the v5r4 item (critical component 2) is fixed ("about 3.59 million"; the thread's 3,593,178 recomputation agrees with the earlier claimed figure).
**Disposition:** FIX_NOW, low severity (one optional one-sentence pin, no rerun of figures); APPROVE is defensible if the author leaves the data-forced electorate key as Layer 1 mess, as the thread itself says.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Thread (sonnet, medium, v5r5 scratch prefix only; verdict at /tmp/determinism-check-task471-v5r5/verdict.md) reproduced every committed figure from the bundle: the 16 organisers (27,20,25,26,29,5,11,12,7,5,4,8,6,3,8,4), NEW_ELECTORS 166,710 and REMOVED_DIED 33,188, region by region. The call is forced by the DSE correlation-bias correction against demographic analysis. Rounding margin is wide (sixth remainder 0.602 against 0.387).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Residential electors | 3,329,031 | 3,329,031 | yes |
| DSE adults | about 3.59M | 3,593,178 | yes |
| DA men per woman 18-24/25-34/35-49 | 1.04/1.03/1.02 | 1.044/1.031/1.021 (unchanged under YoB offsets) | yes |
| DSE men per woman | 1.01/0.99/0.97 | 1.006/0.991/0.973 | yes |
| Corrected adults | about 3.63M | 3,633,959 | yes |
| Organisers | golden | exact; raw DSE 8 regions differ, census counts 14 | yes |
| NEW_ELECTORS | 166,710 | 166,710, every region | yes |
| REMOVED_DIED | 33,188 | 33,188, every region | yes |

## Competing answers that survived
1. Old-platform (R25-) electorate numbers read as the 2023 list's (golden) vs the current electorates_and_regions.csv. The migration notes say only that references and elector numbers were carried over unchanged; no sentence names the 2023 list. Using the current list changes 14 of 16 NEW_ELECTORS regions and the REMOVED_DIED column. The data settle it (102 of 102 old-platform removals later reinstated agree with the 2023 list by region, 38% with the current; per-electorate volumes correlate 0.974 with the 2023 roll against 0.29). Supplementary asks only, not the main call; a data-discoverable key mismatch (Layer 1). This is the one open fork for a strictly word-for-word reader.
2. Imputed records added back: changes 12 regions. Closed by methods report 3.3 and consistency (the PES counts imputed-dwelling people as unmatched, so adding back double counts). Weak survivor on a literal reading, closed by the flagged column and the formula.
3. Calibrating levels to DA at 65 and over (thread: changes 8 regions, e.g. Ardenmere 27 to 26, Hawksridge 5 to 6). The thread says it rests on DA standing about 6 per cent above the DSE at 65+ for both sexes. Main thread's measurement (labelled, supplied by the coordinator, not re-run by me): DA from all births, both deaths files and the movements stands at 0.9994 (men) and 0.9984 (women) of the DSE at 65+, and 1.0085 and 1.0034 even with the 1925-1944 deaths workbook omitted. On that measurement the premise does not hold on the shipped files, so this alternative does not reproduce and I rank it as not surviving. The thread's 6 per cent figure conflicts with it; the likeliest cause is the thread comparing DA with the census count (it quotes DA/census 1.04 to 1.4) or a cohort-build slip, but I did not recompute it and the conflict is recorded rather than settled by me. If the author wants certainty, one cheap check of DA against DSE at 65+ in checks.py settles it.
4. Setting the DA ratio inside each region or cell: changes 12 regions, unreasonable (regional ratios legitimately vary). Does not survive.
Closed: men shortage spread pro rata to men/women/both (no change), rounded DA ratios (no change), time zone (specification note 2), first address versus first residential (0 persons differ), reversal by record versus by elector (identical 280).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 20 / 4 (csv 12, pdf 4, xlsx 3, docx 1) | yes |
| Large file | 25,000 rows | 362,786 | yes |
| Distractors in metadata.json | 2+, none named by file | 2 declared (subnational_population_estimates_jun2024.csv wrong-basis, field operations summary); thread also sees the 2023 roll and sampled meshblocks as weighable | yes |
| Distractor ruled out by a shipped fact, not the stump | yes | plan 2.1 rules out the 2018-base estimates | yes |
| Deliverables | 1 to 3, in golden | 2 (csv, png), both in golden/ | yes |
| Asks unit and rounding, multi-dimensional | yes | 16 regions x 3 whole-number figures | yes |
| Prompt shape, 25+ criteria | identifiable, 25+ | shape 05 in metadata; criteria count unverifiable here | shape yes, count unverified |
| Not LLM-looking, golden realistic | yes | no authoring language found; plain 16-row CSV | yes |

## Gate G reconciliation
Thread: method_or_model_selection / analytical_non_defect / surface_read_dependency no / sole_data_defect no. Design note and card (stump_class analytical): stump is the DSE correlation bias against DA sex ratios; the declared distractor is ruled out by plan 2.1 and is not the surface read. Match. Gate G: pass (analytical_non_defect, no shipped artifact ranks the regions wrongly, distractor not load-bearing). The thread's decisive step is a correction the data must reveal (a sex-ratio gap), not a field's standard method executed without judgment.
Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test and the note's Three rules.

## Stump power (Gate F)
Good on the thread's read: the raw DSE is the tempting finished answer and misallocates 8 of 16 regions; the census counts 14. A solver must notice men 18-49 about 4 per cent short against DA while the women agree, which needs the cohort rebuild. The main thread should weigh that the correction is a textbook coverage-evaluation organ a strong census-methods solver may reach (stumping 1.3). Over-correcting (65+ levels, per-region ratio) is a wrong route, not a valid one.

## Findings, ranked
1. Open reading fork on the supplementary asks: no shipped sentence names the numbering of old-platform electorate numbers; data settle it, a word-for-word reader may not. Fix by one sentence in roll_platform_migration_notes.pdf (file the WHAT: the numbers are those of the 2023 list). Optional; APPROVE defensible.
2. Conflict to close: the thread's 65+ DA-level alternative (8 regions) rests on a 6 per cent gap that the main thread's measurement does not find (0.9994 and 0.9984 of DSE). I rank it as not reproducing; recommend one asserted check, and optionally a sentence saying DA is used for sex ratios only.
3. Imputed-records add-back (12 regions) is closed by the methods report and the flag, not by a plan sentence; confirm the fork-table row.
4. Cosmetic: repeated 13:00-13:59Z hour at the September DST start (two row-order reversals, no effect); transactions run a day past the 30 Sept 2026 specification date, no effect.
5. Rubric criterion count not verifiable here. Metadata licence record present.

## Next action for the author
Either add the one-sentence electorate-numbering pin to the migration notes (then rebuild; no figure moves), or ship as is on the data-forced reading; and assert in checks.py that DA stands within about 1 per cent of the DSE at 65 and over, so the 65+ alternative is closed on record.
