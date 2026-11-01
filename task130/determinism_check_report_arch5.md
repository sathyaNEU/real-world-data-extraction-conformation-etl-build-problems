# determinism-check report, task130, 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one optional author pin on ask 4, below)
**Stumping type:** mechanism: forecasting (with method selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, scratch /tmp/determinism-check-task130-20261031210936/ (verdict.md there). Bundle sha256 ffdcfd56...9abc.

## Why
The plan (s.3) files the rule (third officer if the 2027 schedule's forecast unsatisfactory routine inspections exceed 540) and the attribution (the inspector named in Table 1). The data separate the candidates: the unsatisfactory rate falls steeply with the named inspector's earlier visits to the permit, and the redistricting makes 1,277 of 5,512 scheduled inspections first visits. Every familiarity-keeping variant that handles the 2019 left-censoring lands 626 to 714, all over 540. Category-only (437), one rate per inspector (451) and permit-own record (458) are the easy routes and are refuted by a visible cut by visit number. Main call and asks 1 to 3 forced; asks 4 to 6 reproduce in all 11 districts.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Schedule inspections | 5,512 | 5,512 | yes |
| First / second / third+ | 1,277 / 1,031 / 3,204 | same | yes |
| First-visit rates cat 1/2/3 | 14.4 / 28.2 / 32.4 | same | yes |
| Third+ rates | 2.9 / 4.8 / 8.4 | same | yes |
| Forecast | 693.4 (700) | 693.40 | yes |
| Category-only | 437 | 437.3 | yes |
| Permit-own record | 458 | 416 under judge's construction | no on the figure, same call (under 540) |
| Ask 4 (11 districts) | 10, 10, 9, 9, 11, 8.5, 10, 9, 9, 8.5, 13 as filed | identical | yes |
| Ask 5 (11) | 71.9 ... 155.5 | identical | yes |
| Ask 6 (11) | 1,416 ... 2,424 | identical | yes |

## Competing answers that survived
No fork flips the main call. Residuals:
1. Rate window: from 2019 gives 521.5 (wrong call) because 2019 is left-censored (about 50 percent "first visits"). No shipped sentence excludes 2019, so a literal reader could land it; the judge treats the artefact as visible in the data and the separation as analytical (the design note's fork row 8 says the same). Windows from 2020 on give 681 to 708.
2. Class granularity: two classes give 626, which rounds to 600 against 700 on ask 2; the second-visit rate is about double the later-visit rate, so the data separate them.
3. Permit vs address key: 697 to 714, still 700.
4. Ask 4 date source (weak point): export dates of 359 inspected return visits lag the day-sheet log by 0 to 15 days up to 15 Sep 2026. A literal export-date reading gives 12, 13, 13, 11, 13, 11, 13, 11, 12, 11, 15.5. The golden needs the day sheet taken as the true date and the "earliest unused same officer and address within 20 days earlier" pairing. The source hierarchy is inferred, not filed.
5. Ask 6: export-date reading moves only District 1 (1,432) and District 9 (2,544); first-completed-inspection reading moves Districts 3, 8, 10; the filed text supports the golden.
6. Ask 5: foodborne-illness dates change only District 1 (72.0).
7. Working-day counting inclusive of both ends adds 1; all inspections fall on weekdays so the plan's "from X to Y" supports the golden.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000+ rows | 30,164 (legacy export) | yes |
| Distractors | 2+ named, none labelled by file name | foodborne_illness_investigations xlsx and permit_fee_invoices csv, named in metadata.json; no file name labels them | yes (relevance to weigh taken from the judge, who found both unused; not separately tested by me) |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (memo pdf, xlsx); golden/ holds both | yes |
| Asks | multi-dimensional, unit and rounding stated | forecast to 100, working days / hours to one decimal, dollars; 11 districts each | yes |
| Prompt shape / rubric | identifiable, 25+ criteria | design note counts about 39 | yes (from design note) |
| Prompt | one paragraph, under 1,000 chars, no data-count | 846 chars, one paragraph, no count | yes |
| Em dashes | none | 0 in prompt.txt and submission.md | yes |
| LLM-read / realism | none | judge found no authoring language; golden realism not re-read by me | yes (judge) |

## Gate G reconciliation
Read after the thread returned. Judge: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, analyst_test and domain_test present (analyst test lands about 450 and "do not add", matching the judge's 437 to 458 easy routes). Design note: no decoy; distractors are the two named files and rank nothing. The judge names neither distractor as the surface read, so no too-load-bearing finding. Gate H: judge domain pass, layers pass, decisive_step analytical; design note decisive step is the same (the pair's visit count as the judgment's state, 693.4). No mismatch. The card carries no mechanism or stumping_family field, so those two were compared with the design note only.

## Stump power (Gate F)
High and analytical. Easy routes give "do not add" (437, 451, 458, and 521 from an uncensored 2019 window). The decisive step is a modelled human judgment conditioned on pair history, not a field reading or an executed rule. Not the "textbook method the field standard" case: the judge reached the golden by finding the familiarity effect in the data. The main thread should still weigh that the cut by visit number is loud (first visits 3.9 to 5.9 times later visits), so a strong solver who cuts by visit finds it.

## Findings, ranked
1. Ask 4 (and marginally ask 6): the day-sheet date hierarchy and pairing rule are inferred, not filed. Literal export-date reading gives 12 to 15.5 against the golden's 8.5 to 13. Fix (author's call): file the WHAT in the plan or capacity report, for example that the day sheets record the date each completed return inspection was made. This changes what solvers see and needs a rerun of the judge.
2. Main call: the 2019 window is not excluded by any shipped sentence and flips the call (521.5). The judge counts it as the trap, not a fork. No fix required; if the author wants to close it, a filed window of rates (population, not method) would do it.
3. Ask 2 rounds on class granularity (626 vs 693): data-separated, no fix.
4. Permit-own-record figure 458 did not reproduce under the judge's construction (416); the call is the same. Check the 458 wording in the golden's rationale or drop the figure.

## Next action for the author
Decide on the ask 4 pin (finding 1); if pinned, edit in the generator, rebuild byte-identically, and re-judge once. Otherwise ship as is.
