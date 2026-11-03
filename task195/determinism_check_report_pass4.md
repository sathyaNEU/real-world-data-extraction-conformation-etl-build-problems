# determinism-check report, task195, 2026-11-03 (pass 4, reship of 11-03)

The build session had no agent tool, so it wrote the brief (`<scratch>/t195/judge_1103/judge_brief.md`) and
the coordinating session spawned the one isolated thread from it on candidate target.zip 18d896f6. The
thread's verdict is at `<scratch>/t195/judge_1103/verdict.md`; its findings follow.

## Verdict
NOT_DETERMINISTIC on supplementary ask 3 only; the main recommendation, asks 1 and 2 and the chart ask are
forced and reproduce.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect,
surface_read_dependency: no, sole_data_defect: no

## Why
Ask 3's "those the screen in service flagged, reviewed ones by their review outcome" did not read as
attaching the review outcome to the flag: in the comma list the clause could be its own item. The warehouse
extract carries the screen's own call in hetx_call and the duty bioinformatician's in review_outcome, and
KVAL-07 3.4 counts a recorded FLAG call for the 2027 exports. Taken on hetx_call alone the flagged cells are
219, 60, 160 and 48 (13.8, 34.1, 23.5 and 12.0 per thousand) against the golden's 206, 67, 159 and 45.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Comparison, events, panel-clean | 5,839, 393, 5,446 | same | yes |
| Screen in service detects, false calls | 292, 91 (1.67) | same | yes |
| Per cutoff detections, increase, points, false-call rate | as filed | same, no estimate on a cutoff | yes |
| Paired verdicts | 0.050 not established, 0.030 established | Wald, Newcombe paired, exact McNemar, bootstrap all agree | yes |
| Ask 3 released and reviewed per method | 15,852/475, 1,758/63, 6,802/208, 3,989/123 | same, codes read on the 2025 table before 2 November 2026 and on the extract's labels after | yes |
| Ask 3 flagged and per thousand | 206/13.0, 67/38.1, 159/23.4, 45/11.3 | reproduces only when a reviewed specimen counts by its review outcome | fork |

## Competing answers that survived
One: ask 3's flagged and per-thousand cells, the call of record (a reviewed specimen by its review outcome)
against the screen's own call on every record. Nothing shipped said which governs.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 5 (csv, tsv, json, xlsx, pdf) | yes |
| Large file | 25,000+ rows | the warehouse extract, 32,644 | yes |
| Distractors | 2+ named in metadata.json, none in a file name | 6 | yes |
| Deliverables | 1 to 3, all in the golden | 2 | yes |
| Asks | multi-dimensional, unit and rounding stated | per cutoff and per method, rounding at the close | yes |

## Gate G reconciliation
The thread's `statistical_rigor` / `analytical_non_defect` with no surface-read dependency and no sole data
defect sits beside the card's `method_or_model_selection`: both describe a paired design analysed as paired
against a stated rule, no reported number rejected. Earlier passes recorded both labels; no finding.

## Stump power (Gate F)
Moderate to good, as the thread put it: the easy routes land on the hold or on 0.015, and a strong model that
reads KVAL-07 carefully will often take a paired method. Unchanged from the shipped version's record.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the card's stump_class, analyst_test and
domain_test.

## Findings, ranked
1. FIX_NOW: pin which call counts as flagged in ask 3. Fixed in the prompt with a WHAT clause ("taking a
   reviewed specimen's flag from its review outcome and any other's from the screen in service's own call");
   the golden keeps the call of record, so no figure moved. "Reviewed" checked for the same fork: a record
   carries a review outcome exactly when call_source is REVIEWED, before and after the amendments, asserted.
2. Declined: naming the interval's basis in the chart ask ("from the specimens the two screens call
   differently"). It would file the decisive step in the prompt; the chart's verdict per bar does not depend
   on the paired estimator chosen.

## Next action for the author
The one re-judge a FIX_NOW gets, on the re-cut (target.zip 7ea6c4d9), with the leak reader re-run beside it.
