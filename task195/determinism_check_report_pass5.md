# determinism-check report, task195, 2026-11-03 (pass 5, the re-judge after pass 4's FIX_NOW)

The build session had no agent tool, so it wrote the brief (`<scratch>/t195/judge_1103b/judge_brief.md`) and
the coordinating session spawned the one isolated thread from it on target.zip 7ea6c4d9, the cut that ships.
The thread's verdict is at `<scratch>/t195/judge_1103b/verdict.md`.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (paired against unpaired inference on correct reported
figures), with etl_conformance on the asks; stumping_family: analytical_non_defect;
surface_read_dependency: no; sole_data_defect: no

## Why
Every golden figure reproduces from the shipped files. The comparison is 5,839 specimens (393 MIXED, 5,446
CONCORDANT), and under KVAL-07 4.1 the highest listed cutoff whose increase has a paired 95 per cent interval
above zero, with a false-call rate not above the screen in service's 1.67 per cent, is 0.030. Ask 3 reproduces
exactly once the extract's method codes are read on the table in force when the DNA was extracted, the
amendments applied, each specimen counted once and a reviewed specimen's flag taken from its review outcome.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Comparison, events, panel-clean | 5,839, 393, 5,446 | same; the five specimens with conflicting aliquot verdicts fall outside it | yes |
| Screen in service | 292 detected, 91 false calls, 1.67 | same | yes |
| 0.050 | 294, +2, 0.51, 1.12 | same; paired Wald lower bound -2.03, exact McNemar p 0.845 | yes |
| 0.030 | 308, +16, 4.07, 1.36 | same; paired Wald lower bound +1.37, Newcombe paired +1.36, exact p 0.0052 | yes |
| 0.020, 0.015, 0.010 | 310/18/4.58/1.47, 319/27/6.87/1.56, 326/34/8.65/1.91 | same; 0.010 fails 4.1(b) | yes |
| The call | 0.030 | 0.030, robust to setting aside the 126 control-well specimens and to the re-runs completed by 16 June | yes |
| Ask 3, magnetic bead | 15,852 / 475 / 206 / 13.0 | same | yes |
| Ask 3, magnetic bead, low input | 1,758 / 63 / 67 / 38.1 | same | yes |
| Ask 3, silica column | 6,802 / 208 / 159 / 23.4 | same | yes |
| Ask 3, salting out | 3,989 / 123 / 45 / 11.3 | same | yes |

The thread found the method re-coding forced by the files: code 4 first booked on 2 November 2026, no
extractions on 31 October or 1 November, and each code's DNA concentration before and after the go-live.
Read on the labels as given, the low-input program holds 13,206 and salting out 1,124; with the amendments
left out, magnetic bead's flags are 283. Both are wrong. The amendments match their rows exactly (0 unmatched).

## Competing answers that survived
None. The interval method is not filed, but every paired estimator gives 0.030 and the thread rules the
unpaired (0.015) and non-overlap (hold) readings analytical errors on two screens read on the same
specimens, not equally licensed readings: residual risk, not a fail. No population fork moves the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 5 (csv, tsv, json, xlsx, pdf) | yes |
| Large file | 25,000+ rows | the warehouse extract, 32,644 rows | yes |
| Distractors | 2+ named in metadata.json, none in a file name | 6 | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | per cutoff and per method, rounding at the close | yes |
| Reads as real | no LLM tells | the thread found none | yes |

## Gate G reconciliation
statistical_rigor / analytical_non_defect, no surface-read dependency and no sole data defect, against the
card's method_or_model_selection: both describe a paired design analysed as paired against a stated rule,
with no reported number rejected. Pass 4 used the same label; no finding.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. The field's analysis is a paired parallel-run
method-comparison validation against a reference standard; Layer 1 is the code-table change, the amendment
log, the re-runs and aliquots and the late identity reports; Layer 2 the paired estimand. Matches the card's
stump_class, analyst_test and domain_test.

## Stump power (Gate F)
Three natural easy routes fail: an unpaired interval files 0.015, non-overlap files the hold, and reading the
screen's own flag rate with the model card's limit of detection pushes toward the hold. The ask layer's
re-coding, amendments and once-per-specimen counting are an independent trap layer that does not decide the
call.

## Findings, ranked
1. Optional, declined: filing in the prompt or protocol that the increase is judged on the same specimens. It
   names the decisive step (the paired analysis is the stump), the same tightening declined at passes 3 and 4.

## Next action for the author
Ship: target.zip 7ea6c4d9, committed RESHIPPED.
