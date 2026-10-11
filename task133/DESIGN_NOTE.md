# task133 design note: Bellbird personal loans, the 30 September 2026 ECL allowance

Private, never ships. Architecture v1, drawn 2026-10-11. Seed FC04 (station maturity) not used: its forward-maturity
driver repeats the age-forward structure of task132 drawn the same day, so the slot keeps the objective and draws a fresh
world.

## DRAW

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task133.json`, registered before the ladder; guard WARN only (Gate G forecasting repeats task132, answered on the card: both sit in the Forecasting block, different mechanisms) |
| Domain / task type | banking-credit-financial-risk / expected-credit-loss-provisioning (client domain itself) |
| Objective | Forecasting & Predictive Modeling: the allowance is the expected loss over each loan's next 12 months or remaining life |
| Shape | 02 used as a set of forward cuts (stage, product, drawdown year) around one committed figure |
| Gate G mechanism | forecasting |
| Gap, pattern | time (each loan's forward probability given where it stands on the curve); pattern none |
| Generators | G9 downstream survival against upstream acquisition, G13 horizon mismatch, G16 method selection |
| Stump strategy | stated_rule_hard_construction |
| Layer 2 family / pattern | field_method / `own:seasoning-conditional-lifetime-pd` |
| Decisive rule filed | yes: CRM-ECL-04 files PD(k) as the probability of default in the k-th month after the reporting date, the curve file is stated as running from origination; the step from one to the other is not written |
| Official decoy, validated decoy | no, no |
| Decision | quantity_figure, currency |
| Stakeholder | Head of Credit Risk Reporting (finance_controller), to the Audit and Risk Committee (committee_or_panel), at the quarter close (period_close) |
| Context artifact | filed_model (the PD curve) |
| Calibration form | none: the curve is filed, the method is filed, the difficulty is the construction |
| World | New South Wales, AUD; Bellbird Personal Finance (fictional non-bank lender); PL36, PL60 |
| People | Matthew Gardner, Stephanie Manning, Joseph Mitchell (guard.py names, en_AU, seed 133) |

**Data-native sentence.** A personal loan book is a stack of vintages at every point on their default curve, and the model team's curve is written from origination, so every loan's forward default probability is the rest of the curve from where it stands, scaled by the fact that it is still performing; the book is young (most of it drawn in the last two years) and the curve's riskiest months come early, from the fourth repayment on, which is where reading the curve from the wrong end costs the most.

**Layer 1 (the mess, and the systems that make it).** A loan system extract that gives drawdown and first-repayment dates rather than months on book; loans 90 or more days past due still on the book until write-off at 180; a hardship register of active, completed and cancelled arrangements, including requests cancelled before they began; origination scores on two scorecard versions with a published conversion; a curve file with one curve per product and a model version; scenario weights in a committee workbook beside the prior quarter's; a development sample, a write-off file and a roll-rate report that look relevant and set nothing.

**Layer 2 (the shortcut, and why an expert refuses it).** The shortcut reads the cumulative curve from month 1 for every loan's remaining months, as if the curve were a term structure from the reporting date. An expert sees that the curve is indexed by months on book from origination: a loan 20 months in has already come through the months where most defaults fall, and its probability of defaulting in the k-th month from now is the curve's increment at month a + k divided by its survival to month a. The half-step (shift to months on book without dividing by survival) is also wrong, low.

## GATE G

- **Litmus.** No reported figure is overturned: the curve, the book, the scenarios and the methodology are all correct. Litmus: no.
- **Primary mechanism:** `forecasting` (lifetime and 12-month expected losses), with the conditional PD as the decisive construction.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data and instrument tests.** No file is incomplete or stale in a way the answer rests on; stage 3 loans and cancelled hardship arrangements are ordinary system states. Replacing every instrument with a perfect one (a curve from the reporting date for each loan's age) would hand over the answer, but no lender's model team produces that object: a cumulative curve by months on book is the standard deliverable, and conditioning it is the analyst's construction.
- **Lens swap.** Not one population under two lenses: the naive and the answer use the same loans and the same curve, and differ in a computation (where on the curve each loan's forward months sit).

## THE STUMP

A competent solver stages the book, reads the model team's cumulative default curve from month 1 for every loan's next 12 months or remaining term, and books about AUD 19.6 million, 43 per cent high; the step that lands it there is treating a curve that runs from origination as a term structure from the reporting date, when most of the book is already past its riskiest months.

## LADDER (allowance against the answer)

| Rung | Construction | vs answer |
|---|---|---|
| 0 | Curve read from origination for every loan (unconditional) | +43.4% |
| 1 | Balance held flat instead of re-amortised | +19.6% |
| 2 | No discounting at the contract rate | +9.9% |
| 3 | Curve shifted to months on book without the survival division | -3.3% |
| 4 (answer) | Increment from months on book divided by survival to date, stage 2 scalar, scenarios, re-amortised EAD, discounted | **AUD 13,667,000** |

The answer sits between the two natural misreadings of the curve (bracketing, `proven-in-production` L5). The half-step (shift without the survival division) is the nearest rung at 3.3 per cent low, AUD 13.22 million, still about 450 thousand dollars from the answer at the nearest thousand; shift plus no discounting lands 6.3 per cent high. Staging devices move the stage split, not the call: dropping the hardship register moves 441 loans, skipping the v3 conversion moves 698 (floors 300 and 100 asserted).

## SURVIVAL PROPERTIES

1. Not written: CRM-ECL-04 3.2 defines PD(k) and names the curve; the curve file's own header says it gives a new loan's cumulative probability by month on book, counted in repayments fallen due. No sentence turns the one into the other.
2. No corpus: the development sample ships as a distractor, and rebuilding the curve from it returns the filed curve, which settles nothing about conditioning.
3. No arithmetic symptom: an unconditional allowance reconciles to every control the pack has (stage counts, balances, scenario weights).
4. Not a row predicate: each loan's PD path depends on its own months on book along a filed curve.
5. Enumeration is arithmetic: no column carries a loan's conditional PD.
6. No cutover date.
7. Survives deletion: nothing wrong to delete.

## CLOSURE TABLE (22 axes)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | loans open at close of business 30 September, stage 3 out (filed) |
| 2 | Unit | loan |
| 3 | Attribution window | default month k after the reporting date |
| 4 | As-of dating | stage at the reporting date (filed), hardship in force on the date (filed) |
| 5 | Version basis | Q3 FY27 scenario sheet, not the prior quarter's (sheet named; ARC approval date) |
| 6 | Divisor | coverage over gross carrying amount, the sum of current balances (filed) |
| 7 | Weighting | probability-weighted scenarios (filed; linear in PD, so one multiplier) |
| 8 | Window | 12 months stage 1, remaining term stage 2 (filed) |
| 9 | Boundary | 30 and 90 days past due, 60-point score fall: "or more" (filed) |
| 10 | Rounding | unrounded loan level; every graded figure at least 5 per cent of its bin from the edge after TUNE (one extra repayment on one up-to-date loan, asserted) |
| 11 | Tie-break | none |
| 12 | Maturity | months on book as repayments fallen due (the curve file's header and CRM-ECL-04 3.2) |
| 13 | Order of operations | multipliers commute with sums |
| 14 | Row order | sums only |
| 15 | Duplicates | none in the book; hardship rows per arrangement |
| 16 | Identity | loan_no joins book and register |
| 17 | Netting | none |
| 18 | Units | AUD; annual contract rate over 12 (filed) |
| 19 | Codes | Cancelled arrangements never in force (filed) |
| 20 | Integerisation | none |
| 21 | Clause scope | the stage 2 scalar applies to PD(k) for stage 2 only (filed) |
| 22 | Forward window | the conditional curve, the decisive axis |

## ASK SHEET

| Ask | Figures | Device |
|---|---|---|
| Allowance | 1 | the conditional curve |
| Stage x product: loans, GCA, allowance, coverage | 16 | staging (hardship register, v3 conversion, stage 3 filter); allowance and coverage move with the curve |
| Drawdown year x product | 8 | the curve error grows with seasoning, so every older year moves |
| Stage 3 loans | 1 | the 90-day filter |

Pair arithmetic: a solver on rung 0 keeps the eight stage counts and balances if it stages correctly and loses the rest (allowances, coverages, years): about 5 + 7 + 58 x 8/26 = 30. A solver on rung 3 loses every allowance figure at the nearest thousand as well. Criteria about 26 asks + call + components + slides, over 30.

## LEAK REVIEW

- `leak.py` (after the realism rebuild): REVIEW, no LEAK. The policy and dictionary share the subject's vocabulary with the call (collective, expected credit loss, allowance, PL36, PL60) and carry no figure of the answer; the migration note's conversion sentence is the published formula CRM-ECL-04 section 2 calls for; dates after 30 September are hardship arrangement ends and first repayments of September loans.
- Reader round 1 (before the rebuild): no sentence names the decisive step (it read 3.2 and the curve definition as the stated standard), no file states or ranks the answer, no planted file; its realism list (arrears off the repayment calendar, annuity balances with round-hundred tuning edits, hardship records outside loan lives, curve defaults before month 4, loss flows that did not reconcile, calendar and pricing artefacts, template containers, local times stamped as UTC, a thin policy document, the Q3 FY27 label, pandas number formatting) was fixed in the generator. A second read runs on the rebuilt pack.

## Tried and rejected

- Healthcare same-day access with demand censored at sell-out time (the slot's first draw): too mild a censoring to separate the rungs and two rigorous uncensoring methods disagreed by one session in several cells.
- Building the PD curve from the outcome history inside the task: the naive denominator (every loan originated) and the unconditional reading cancel to within 2.3 per cent of the answer, so the curve is filed as model output instead.
- Months-on-book bands as the breakdown ask: it names the decisive dimension in the prompt; drawdown year carries the same information the way a credit committee reads it.
- No stage 2 scalar: stage 2 coverage came out barely above stage 1 (7.6 against 6.3 per cent), which no credit reviewer would accept; CRM-ECL-04 now files a 2.4 scalar.
- Realistic default levels (lifetime default 10 per cent PL36, 14 per cent PL60, no 90-day default before the fourth repayment) put the half-step rung (curve shifted, no survival division) at 3.3 per cent low against its 6 per cent floor; reaching 6 per cent needs PL60 lifetime default near 20 per cent, a loss-making lender, so the floor is 2.5 per cent and the rung stays a distinct wrong answer at the nearest thousand.
