# Determinism check, task272 (architecture 3, Domains Fit repair), 2026-11-07

Judge thread: general-purpose, Sonnet, medium effort, isolated to `/tmp/determinism-check-task272-dfit/` (the
unzipped bundle of target.zip 5445a679 and the brief's graded blocks). Verdict file:
`/tmp/determinism-check-task272-dfit/verdict.md`. The repair under review: the call sentence kept word for word, a
second sentence asking each product to be judged on its estimated 2026 rate per 100,000 doses made with its 90 per
cent interval, and the PDF saying where the limit of 10 sits against each interval; the input PDFs and the golden
exported by LibreOffice Writer; the dose log without writer metadata.

## Verdict

**DETERMINISTIC.** Disposition **APPROVE**, no repair, no rerun.

- The main call reproduces: Cefoxitin 2 g, Phenylephrine, Cefazolin 2 g and Midazolam over the limit of 10, the other
  eight under 0.2, one to three orders of magnitude from the line.
- Every graded figure reproduces: all 60 monthly dose counts (Ontario local time, PC-3's two serials one station),
  all 12 set counts (a re-seat the same lot), all 12 in or out marks and all 12 limit sides.
- The interval's side was tested under pooled OLS, a method-of-moments random start and a REML mixed model, each
  with a set-level bootstrap: every side holds, and Midazolam's lower end sits at 18 to 19 per 100,000 in every
  method, clear of 10. The naive fork (a pooled normal fit to the weighed doses) reproduces as the design says:
  it adds the three bags and drops Cefazolin 2 g and Phenylephrine.
- Gates A, B, C, D and E pass; hygiene PASS (12 files in 5 formats, a 477,875-row parquet, distractors present and
  unused).

## Gate G

`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`. The files are correct; the difficulty is estimating a tail rate from sparse weighed doses with
the record's own structure (delivery falling with the litres a set has pumped, a set-level start) and an interval
that resamples sets. On clean data it still stumps.

## Gate H

`domain: pass`, `layers: pass`, `decisive_step: analytical`. The deciding quantity is a modelled tail rate of a
gravimetric process with a cluster-resampled interval, the field's own analysis; the swap test fails to leave the
task intact. Layer 1 is the UTC log against Ontario months, the register's gross-to-net change, the PC-3 serial
swap and the recount rows; none carries the call.

## Residual (Gate C, minor) and why it is not filed

The judge notes that no shipped file names the dose-to-dose distribution, and that Midazolam rests on a tail beyond
3.4 standard deviations. It measured the residuals as normal (skew about 0, excess kurtosis -0.3 to 0.5) and found
that heavier tails (t with 10 or 30 degrees of freedom) only raise Midazolam's rate (113 to 376), so no reasonable
distribution moves any product's side. Its optional fix, naming the normal distribution in the policy or the
request, is declined: it would file a piece of the method (the HOW, against `determinism-check` section 1 and the
three rules), and it moves no graded answer.

## Leak read (same day)

The isolated reader (Sonnet, medium) on the leak copy of the same pack: no leak, Q6 analytical, the prompt reads as
a manager's request. Its one item, the xlsx registers carrying a person as creator, is fixed in the reship (every
xlsx input's creator and last saver the issuing body, asserted in checks.py); only file properties changed, so no
further read is owed.
