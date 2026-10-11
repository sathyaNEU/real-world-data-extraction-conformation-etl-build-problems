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

**Layer 1 (the mess, and the systems that make it).** A loan system extract that gives drawdown and first-repayment dates rather than months on book; loans 90 or more days past due still on the book until write-off at 180; a hardship register of active, completed and cancelled arrangements, including requests cancelled before they began; origination scores on two scorecard versions, the version set by the application date (loans applied for in June 2024 and funded in July stay on v3), with a published conversion; a curve file with one curve per product and a model version; scenario weights in a committee workbook beside the prior quarter's; a development sample, a write-off file and a roll-rate report that look relevant and set nothing.

**Layer 2 (the shortcut, and why an expert refuses it).** The shortcut reads the cumulative curve from month 1 for every loan's remaining months, as if the curve were a term structure from the reporting date. An expert sees that the curve is indexed by months on book from origination: a loan 20 months in has already come through the months where most defaults fall, and its probability of defaulting in the k-th month from now is the curve's increment at month a + k divided by its survival to month a. The half-step (shift to months on book without dividing by survival) is also wrong, low.

## GATE G

- **Litmus.** No reported figure is overturned: the curve, the book, the scenarios and the methodology are all correct. Litmus: no.
- **Primary mechanism:** `forecasting` (lifetime and 12-month expected losses), with the conditional PD as the decisive construction.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data and instrument tests.** No file is incomplete or stale in a way the answer rests on; stage 3 loans and cancelled hardship arrangements are ordinary system states. Replacing every instrument with a perfect one (a curve from the reporting date for each loan's age) would hand over the answer, but no lender's model team produces that object: a cumulative curve by months on book is the standard deliverable, and conditioning it is the analyst's construction.
- **Lens swap.** Not one population under two lenses: the naive and the answer use the same loans and the same curve, and differ in a computation (where on the curve each loan's forward months sit).

## THE STUMP

A competent solver stages the book, reads the model team's cumulative default curve from month 1 for every loan's next 12 months or remaining term, and books about AUD 19.8 million, 44 per cent high; the step that lands it there is treating a curve that runs from origination as a term structure from the reporting date, when most of the book is already past its riskiest months.

## LADDER (allowance against the answer)

| Rung | Construction | vs answer |
|---|---|---|
| 0 | Curve read from origination for every loan (unconditional) | +43.6% |
| 1 | Balance held flat instead of re-amortised | +20.0% |
| 2 | No discounting at the contract rate | +10.0% |
| 3 | Curve shifted to months on book without the survival division | -3.3% |
| 4 (answer) | Increment from months on book divided by survival to date, stage 2 scalar, scenarios, re-amortised EAD, discounted | **AUD 13,773,000** |

The answer sits between the two natural misreadings of the curve (bracketing, `proven-in-production` L5). The half-step (shift without the survival division) is the nearest rung at 3.3 per cent low, AUD 13.32 million, still about 455 thousand dollars from the answer at the nearest thousand; shift plus no discounting lands 6.3 per cent high. Staging devices move the stage split, not the call: dropping the hardship register moves 470 loans, skipping the v3 conversion moves 786 (floors 300 and 100 asserted).

## SURVIVAL PROPERTIES

1. Not written: CRM-ECL-04 3.2 defines PD(k) and names the curve; the curve file's own header says it gives a new loan's cumulative probability by month on book, counted in repayments fallen due. No sentence turns the one into the other.
2. No corpus: the development sample ships as a distractor, and rebuilding the curve from it returns the filed curve, which settles nothing about conditioning.
3. No arithmetic symptom: an unconditional allowance reconciles to every control the pack has (stage counts, balances, scenario weights).
4. Not a row predicate: each loan's PD path depends on its own months on book along a filed curve.
5. Enumeration is arithmetic: no column carries a loan's conditional PD.
6. No cutover date.
7. Survives deletion: nothing wrong to delete.

## THREE RULES (client update, 10/10)

- **Domain (swap test).** The deciding quantity is each loan's 12-month or lifetime expected credit loss under AASB 9: a cumulative default curve by months on book turned into forward monthly PDs, staged on significant-increase triggers, scenario-weighted, re-amortised and discounted at the contract rate. That is the provisioning work of the expected-credit-loss task type. Swap the nouns into another field and staging, LGD, EAD, the scenario overlay and the coverage ratios have nothing to attach to, so the task does not read the same.
- **Two layers.** Layer 1: a loan-system extract that gives drawdown and first-repayment dates rather than months on book, a hardship register with lagging statuses and cancelled arrangements, origination scores on two scorecard versions with a published conversion, a scenario workbook beside the prior quarter's, and a development sample, roll-rate report and write-off file that set nothing. Layer 2: turning an origination-indexed cumulative curve into a performing loan's forward PDs.
- **Decisive step: analytical.** Analyst test: a strong analyst who cleans the book and reads CRM-ECL-04 3.2 and the curve header correctly (PD(k) is the probability of default in the k-th month after the reporting date; the curve is a new loan's cumulative default probability by month on book) takes the curve's increments from each loan's months on book as its forward PDs, without dividing by the probability that the loan has survived to date, and books about AUD 13.32 million against AUD 13,773,000. Round 1's two solvers did exactly that. The staging inputs (the hardship dates rule, the v3 conversion, the 90-day filter) are stated rules, and they move the stage split, not the call.

## CLOSURE TABLE (22 axes)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | loans open at close of business 30 September, stage 3 out (filed) |
| 2 | Unit | loan |
| 3 | Attribution window | default month k after the reporting date |
| 4 | As-of dating | stage at the reporting date (filed), hardship in force on the date (filed) |
| 5 | Version basis | Q3 FY27 scenario sheet, not the prior quarter's (sheet named; ARC approval date) |
| 6 | Divisor | coverage over gross carrying amount, the sum of current balances (filed in CRM-ECL-04 1.5 and 1.6) |
| 7 | Weighting | probability-weighted scenarios (filed; linear in PD, so one multiplier) |
| 8 | Window | 12 months stage 1, remaining term stage 2 (filed); a loan past contractual maturity outside stage 3 is treated as being in the final month of its term, one month remaining (CRM-ECL-04 3.2, filed), at its curve's last month; read as carrying nothing instead, every graded figure keeps its bin (C3, asserted: 28 loans, AUD 222) |
| 9 | Boundary | 30 and 90 days past due, 60-point score fall: "or more" (filed) |
| 10 | Rounding | unrounded loan level; every graded figure at least 5 per cent of its bin from the edge after TUNE (six extra repayments on up-to-date loans), under both readings of axis 8 (asserted; nearest is stage 1 PL36 coverage at 6.3 per cent) |
| 11 | Tie-break | none |
| 12 | Maturity | months on book as repayments fallen due, repayment dates in a payment pause counted (CRM-ECL-04 3.2, the curve header, the sample metadata, the dictionary's hardship section); read with pause dates left out (1,413 loans, 3,272 dates) the allowance is AUD 13,821,000 and 17 of 28 graded figures move (checks.py prints it) |
| 13 | Order of operations | multipliers commute with sums |
| 14 | Row order | sums only |
| 15 | Duplicates | none in the book; hardship rows per arrangement |
| 16 | Identity | loan_no joins book and register |
| 17 | Netting | none |
| 18 | Units | AUD; annual contract rate over 12 (filed) |
| 19 | Codes | Cancelled arrangements never in force (filed); status labels lag the Tuesday-night batch and 2.2's dates decide: the two arrangements that ended 29 September still show Active, the stage 2 set is unchanged, and staging on the label alone keeps the allowance in its bin (asserted) |
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
- Reader round 1 (before the rebuild): no sentence names the decisive step (it read 3.2 and the curve definition as the stated standard), no file states or ranks the answer, no planted file; its realism list (arrears off the repayment calendar, annuity balances with round-hundred tuning edits, hardship records outside loan lives, curve defaults before month 4, loss flows that did not reconcile, calendar and pricing artefacts, template containers, local times stamped as UTC, a thin policy document, the Q3 FY27 label, pandas number formatting) was fixed in the generator.
- Reader round 2 (on the rebuilt pack): twelve findings, all fixed in the generator. The curve's development performance ends 31 May 2026, before the 19 June extraction and the 24 June approval. Behaviour scores hold the v4 origination score until the first repayment falls due (a dictionary field line). About one default in six is resolved before write-off, and write-off cohorts three years on have recovered about 24 per cent of the balance (21 per cent of write-offs inside the 15-month window), against LGDs of 70 and 76 per cent. The scorecard version follows the application date and loan numbers follow applications. Nothing falls due under a payment pause in force. A loan past maturity outside stage 3 has one remaining month (CRM-ECL-04 3.2). Five policy passages now read as plain rules, the dictionary describes the scenario workbook's two sheets, the state mix and the agreed hardship repayments read like a lender's, the Office containers carry Excel's and Word's own structures, the deck rebuilds byte for byte, and the migration note's PDF stamp is Sydney time with its offset. The repair also fixed collections arrangements that ended before they began. Graded figures moved: the allowance is AUD 13,773,000. leak.py after the repair: REVIEW, no LEAK; the next read runs on the repaired pack.
- Reader round 3 (on the round 2 pack): no sentence names the decisive step; no file ranks or states the answer; the development sample and the roll-rate workbook are the distractors. Its findings went into the generator as below, and no graded figure moved: AUD 13,773,000, every block 4 figure, the stage 1 and stage 2 sets and each loan's ECL are identical to full precision.
- A1, pause pin: 3.2, the curve header, the sample metadata and the dictionary's hardship section now say repayment dates in a pause count and a pause leaves the schedule and the maturity date alone, which is how sim.py treats a paused instalment (nothing payable, interest charged to the balance on each repayment date, maturity unchanged). Read the other way, the allowance is AUD 13,821,000 and 17 of 28 graded figures move, so checks.py asserts the pin is load-bearing.
- A2, past maturity: 3.2 now says the loan is treated as being in the final month of its term, with one month remaining, and the bin assertion stays. This goes in at the author's direction; it names the term, not the curve, so the rejection of "the curve's final month" below still describes the sentence that was turned down.
- A3: every other pin is unchanged.
- B1, containers: every docx and xlsx carries the Office 2013-2022 theme (family 62F939B6) as Word or Excel writes it (full declaration, CRLF, one line; Word's copy differs in three script fonts), byte-checked against Office 2016 files. Workbooks keep Calibri and defaultThemeVersion 166925, so the rolled-forward ones carry creation dates before the 2023 Aptos theme (roll rates July 2022, scenarios August 2022, the golden allowance workbook February 2023), and the register comes from the job's template under its service account (asserted).
- B2: the development sample is extracted on Tuesday 2 June 2026 (file stamp the same day), leaving 14 business days before the 24 June approval (asserted).
- B3: old 3.6 is now 3.7 in plain words; 1.6 defines the coverage ratio once and section 5 drops the bracket; the dictionary loses the computation-shaped lines and the file pointers; the curve header names the PLPD-2026.06 development sample; the migration note shows a short table of conversions. New plain clauses: 1.5 the system balance as the gross carrying amount, 1.7 hardship variations as modifications that are not derecognised (gain or loss immaterial), 3.6 the contract rate as the effective interest rate with establishment fees not deferred (immaterial; CFO approval November 2019), a one-line no-probation rationale in 2.4. 2.5 now quotes 5.5.11 as more than 30 days past due, and 2.1's 30 or more is unchanged.
- B4, residue: 57 blank states for overseas addresses (dictionary line); 5 cases from before 1 July 2020 with no reason (dictionary: required from that date); arrangement_status refreshed by a Tuesday-night batch (dictionary line), so two arrangements that ended 29 September show Active. Staging on the label alone moves one PL36 loan (4 ask figures) and keeps the allowance in its bin, and the stage 2 set is asserted by hash.
- B5: the policy's statistics are the word processor's own measurement of the laid-out file (3 pages, 134 lines, 95 paragraphs, 1,205 words, header and footer counted once). Its revision ids follow the version history: 13 sittings over six revisions, with runs retyped in later revisions marked.
- B6: the register's creator is the job's account svc_crr_batch, and its last modifier is Kayla Stokes, Credit Risk Reporting (guard.py names, added to the card).
- B7, left: the migration note stays LibreOffice output. There is no Word or Arial here to make a Word PDF, and rewriting the producer or the embedded font name would be a forgery. Its own story holds: Writer 24.2 shipped in February 2024, and Liberation Sans is the metric twin of the Arial the source names. The H1 audit misses its producer because the PDF stores it as UTF-16 hex.
- B8: 101 pauses from the 2021 Sydney, Melbourne and Canberra lockdowns, on loans closed before 30 September only, recorded without replaying their repayments, so no book loan and no figure from the repayment histories moves (asserted).
- After this round: leak.py REVIEW, no LEAK (the same six classes); checks.py 121 pass; verify.py PASS; the H1 audit is clean on target and golden; two scratch builds are byte-identical to each other and to the shipped pack.

## Tried and rejected

- Healthcare same-day access with demand censored at sell-out time (the slot's first draw): too mild a censoring to separate the rungs and two rigorous uncensoring methods disagreed by one session in several cells.
- Building the PD curve from the outcome history inside the task: the naive denominator (every loan originated) and the unconditional reading cancel to within 2.3 per cent of the answer, so the curve is filed as model output instead.
- Months-on-book bands as the breakdown ask: it names the decisive dimension in the prompt; drawdown year carries the same information the way a credit committee reads it.
- No stage 2 scalar: stage 2 coverage came out barely above stage 1 (7.6 against 6.3 per cent), which no credit reviewer would accept; CRM-ECL-04 now files a 2.4 scalar.
- Realistic default levels (lifetime default 10 per cent PL36, 14 per cent PL60, no 90-day default before the fourth repayment) put the half-step rung (curve shifted, no survival division) at 3.3 per cent low against its 6 per cent floor; reaching 6 per cent needs PL60 lifetime default near 20 per cent, a loss-making lender, so the floor is 2.5 per cent and the rung stays a distinct wrong answer at the nearest thousand.
- Post-default resolution near one default in five with recoveries near 26 per cent of the written-off balance: the implied gross LGD fell to about 60 per cent, ten points under the filed 70 and 76, so resolution is set near one in six and recoveries near a quarter (about 24 per cent at three years: PL36 30, PL60 20).
- Tuning the rounding margins on the one-month reading of past-maturity loans alone: the allowance and the PL60 2023-and-earlier figure straddled their edges between that reading and the zero one (the loans carry about AUD 220), so the tuner now centres both readings at once.
- Pinning the past-maturity PD by curve position ("the curve's final month") in CRM-ECL-04: rejected, the sentence would tell a solver that a loan reads the curve from its own month on book, which is the decisive step; 3.2 pins only the one-month remaining term and the corridor assertion covers the PD reading.
- Stale arrangement_status labels from a weekly status refresh: not built. The labels sit on the main call's staging path, so a solver staging on status instead of dates would move a handful of loans and the allowance bin; the statuses stay current to the reporting date and CRM-ECL-04 2.2's date rule decides.
- Weekly status batch on Sunday or Monday night (round 3, B4): 12 or 6 arrangements end after the run, 9 or 5 book loans otherwise in stage 1, and staging on the label alone moves the allowance to AUD 13,778,000 or 13,775,000 (set STATUS_RUN_WEEKDAY to 6 or 0 to reproduce). The Tuesday run leaves two and moves one loan, and the allowance keeps its bin, so the main call stays mess-neutral.
- Blank state or channel for loans migrated at the October 2019 go-live (round 3, B4): no such loan is on the book, where the earliest drawdown is May 2021, so the blank states are overseas addresses.
