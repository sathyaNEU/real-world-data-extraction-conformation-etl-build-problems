# determinism-check report, task169, 2026-10-25

One isolated judge thread (general-purpose, sonnet, medium) on a fresh unzip of target.zip 73e3137b, after the
determinism repair of portal round 1. The thread's own report is `scratchpad/determinism-check-task169-r2/verdict.md`,
with `blind_derivation.md` beside it.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (a counterfactual under a regime change), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The order was kept: the blind derivation went to disk before the graded blocks were opened. Its own estimate was
19.7 per cent (arrests per day at liberty, times each grade's conversion to a DOC sentence, an 82-day lag, the window
of 730 days at liberty), 20.2 with the cohort's covariates, 20.8 at a 60-day lag: every correct variant prints 20.
The structural fact it found is the one the call stands on: every arrest the Board revoked on was nolle prossed, and
the courts' own arrests convict to a DOC sentence at 62 per cent (felony A and B), 27 (felony C to E) and 3
(misdemeanour); under the Act those arrests reach the courts.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Call, two-year return share (nearest 5 points) | 20 (20.40) | 19.7 to 20.8 | yes |
| Cohort | 6,466 | 6,466 (PAR 5,290, RPR 1,176) | yes |
| Table 1, recommitments by office, arrest and conditions (8) | as filed | all 8 exact | yes |
| Table 2, detainer parolee-days by district and half (8) | as filed | all 8 exact | yes |
| Table 3, writ days by institution and half (10) | as filed | all 10 exact | yes |

## Competing answers that survived
none on the call. Tested: any admission 51.8 (50), a new-commitment filter 8.71 (10), the first return only 5.9 (5), a
covariate model on new commitments 8.84 (10), a hazard on new commitments 10.5 to 10.8 (10), arrests imputed without
the exposure correction 16.5 to 18.2 (15 or 20, an incomplete method rather than a reading). Ask notes, each closed by
a shipped sentence or the records: table 1 per case (3,521) or per order (3,174), closed by the Act's recommitment;
the unreturned writs' end in table 3, read from the release dates; parolee-days against detainer-days, closed by the
unit word.

## Gate G reconciliation
The thread's mechanism and Gate H line (domain pass, layers pass, decisive step analytical; the easy route is the
new-commitment filter at 8.7 per cent, filing 10) match the card's `stump_class` analytical and the analyst test.

## Stump power (Gate F)
Strong on the readers: both scored readers filed 10. The judge's own blind estimate reached the golden, a sign the step
is findable from the files, which the portal measures.

## Findings, ranked
none blocking.

## Next action for the author
Reship. The asks leak to careful readers (23 and 18 of 26), at the level the portal's round 1 measured; a rubric repair
of tables 2 and 3 is the next step if the portal returns it on the rubric.
