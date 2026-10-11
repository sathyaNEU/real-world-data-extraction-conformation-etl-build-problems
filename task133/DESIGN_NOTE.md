# task133 design note: Bellbird personal loans, the 30 September 2026 ECL allowance

Private, never ships. Architecture v1, hardening loop 1 (2026-10-11). The portal round: one model was stumped, the
other landed AUD 13,773,000 at 100 per cent by dividing the curve's increments by survival to date, and every ask went
with it because each was an output of the same construction. This loop takes the main rung one step deeper (the curve
is now the crude default share of every loan drawn, so survival to date is itself a wrong rung) and replaces the asks
with two that the call's construction never touches. Seed FC04 (station maturity) was not used: its forward-maturity
driver repeats the age-forward structure of task132 drawn the same day.

## DRAW

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task133.json`, rewritten for loop 1 with the v1 driver in `lineage`, opening move deliverable-first since the pre-round repair; check and heart WARN only, surface 2 promoted on the deliverable order alone (GUARD below) |
| Domain / task type | banking-credit-financial-risk / expected-credit-loss-provisioning (client domain itself) |
| Objective | Forecasting & Predictive Modeling: the allowance is the expected loss over each loan's next 12 months or remaining life |
| Shape | 02: one committed figure with its stage split, plus two grids (realised loss by product and quarter, 8 cells; the June book's stages by where they stand at 30 September, 16 cells) |
| Gate G mechanism | forecasting |
| Gap, pattern | time (each loan's forward default probability given that it is still open and performing); pattern none |
| Generators | G9 downstream survival against upstream acquisition, G13 horizon mismatch, G16 method selection |
| Stump strategy | stated_rule_hard_construction |
| Layer 2 family / pattern | field_method / `own:attrition-conditioned-lifetime-pd` |
| Decisive rule filed | yes: CRM-ECL-04 3.2 files PD(k) as the probability of default in the k-th month after the reporting date from the model team's curve; the curve header defines its column as the share of the loans drawn in the development window that had defaulted by the end of each month on book. The step from one to the other is not written, and no sentence anywhere says anything about dividing, conditioning, survival or early repayment (asserted) |
| Official decoy, validated decoy | no, no |
| Decision | quantity_figure, currency |
| Stakeholder | Head of Credit Risk Reporting (finance_controller), to the board (board_of_directors) with the Audit and Risk Committee chair presenting, at the quarter close (period_close) |
| Context artifact | filed_model (the PLPD-2026.06 curve and its development sample) |
| Calibration form | none: the curve is filed and complete, the method is filed, the difficulty is the construction |
| World | New South Wales, AUD; Bellbird Personal Finance (fictional non-bank lender); PL36, PL60; Wirraway Mercantile Agents (collections agency) and Tarwin Receivables Pty Ltd (debt buyer), both invented |
| People | Matthew Gardner, Stephanie Manning, Joseph Mitchell, Tamara Farrell, Adam Gordon, Renee Foster, Troy Olson, Natalie Hanna, Kayla Stokes, Christine Fletcher (guard.py names, en_AU, seed 133) |

**Data-native sentence.** A model team that develops its curve on complete-term cohorts publishes the crude default
share of every loan drawn, because that is what a closed cohort gives without any modelling, and a young unsecured book
repays early in volume: 41 per cent of the PL36 and 54 per cent of the PL60 development loans were repaid in full before
term, and at the book's median month on book (14 for PL36, 21 for PL60) 14.6 and 22.3 per cent of the cohort have
already left that way, so a performing loan's forward PD has to be measured against the loans still open, which only
the sample's outcomes give.

**Layer 1 (the mess, and the systems that make it).** A loan system extract that gives drawdown and first-repayment
dates rather than months on book; loans 90 or more days past due still on the book until write-off at 180; a hardship
register of approved, active, completed and cancelled arrangements whose status is set by a Tuesday-night batch and
read as at 30 September; origination scores on two scorecard versions with a published conversion; a curve file with
one curve per product and a model version, beside the complete-term development sample it was read from; scenario
weights in a committee workbook beside the prior quarter's; the June quarter-end extract from the same job without the
behaviour score column (added by a change in July), beside month-end scoring runs stamped with the day each run was
made; a Collections defaults file, a receipts ledger across every cohort with dishonoured direct debits reversed by
negative rows and one debt-sale receipt carried without a loan number, and the sale schedule priced in cents per dollar
of face value; a write-off file and a roll-rate workbook that set nothing.

**Layer 2 (the shortcut, and why an expert refuses it).** The textbook conditional PD for a loan that has survived to
month a is the curve's increment divided by one less the curve to date. That is right for a curve of default against
the loans still at risk, and wrong for this one: the header says the shares are of every loan drawn, so a loan repaid in
full at month 10 is still in the base at month 20. A performing loan at month a is one of the development loans that
have neither defaulted nor been repaid by then, so the divisor is S(a) = 1 - C(a) - Cl(a), with Cl(a) read from the
sample. The over-correction (a default hazard rolled forward with no repayment) and the double count (S(a) plus a second
repayment factor on EAD) are also wrong.

## GATE G

- **Litmus.** No reported figure is overturned: the curve, the sample, the book, the scenarios and the method are all
  correct. Litmus: no.
- **Primary mechanism:** `forecasting` (lifetime and 12-month expected losses), with the attrition-conditioned PD as the
  decisive construction.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data and instrument tests.** No file is incomplete or stale in a way the call rests on. Replacing every
  instrument with a perfect one (a forward PD curve per month on book for loans still open) would hand over the answer,
  but no model team ships that object: a crude cohort curve plus its development sample is the standard deliverable, and
  conditioning it is the analyst's construction.
- **Lens swap.** Not one population under two lenses: every rung uses the same loans and the same curve, and they differ
  in the divisor.

## THE STUMP

A competent solver stages the book, reads the PD curve as cumulative default by months on book, conditions each
performing loan's forward increments on survival to date by dividing by 1 - C(a), and books about AUD 11.74 million,
10.8 per cent low; the step that lands it there is taking the curve's shares as shares of loans still open when the
header says they are shares of every loan drawn, so the loans repaid in full by month a stay in the at-risk base and
every forward PD is understated. That decisive step is the one the v1 portal response completed, and it now returns the
wrong answer.

## LADDER (allowance against the answer, measured by checks.py and verify.py)

| Rung | Construction | Allowance | vs answer |
|---|---|---|---|
| R0 | Curve read from origination for every loan | 18,283,649 | +38.93% |
| Rh | Default hazard from the sample rolled forward with no early repayment (any default-only survival or Kaplan-Meier rebuild lands here) | 14,072,673 | +6.93% |
| **Answer** | Increment from months on book divided by S(a) = 1 - C(a) - Cl(a), stage 2 scalar, scenarios, re-amortised EAD, discounted | **13,160,125, AUD 13,160,000** | |
| R4b | S(a) conditioning plus a second early-repayment survival factor on EAD (repayment counted twice) | 12,364,852 | -6.04% |
| R4 | Divided by 1 - C(a), survival to date (v1's answer, the path the portal response took) | 11,736,551 | -10.82% |
| R3 | Shifted to months on book, no division | 11,421,240 | -13.21% |

Every rung misses the allowance and both stage amounts at the nearest thousand and sits at least 5 per cent from the
answer (asserted in checks.py and verify.py; the nearest are R4b at 6.04 per cent and Rh at 6.93 per cent, with nothing
planted to widen either). The
answer's stage amounts are AUD 10,563,204 and 2,596,921. Off the curve: no discounting is +9.33 per cent, the balance
held flat +17.85 per cent; dropping the hardship register moves 470 loans out of stage 2 and the allowance -1.76 per
cent, skipping the v3 conversion moves 786 and -0.86 per cent (floors of 300 and 100 loans asserted).

## SURVIVAL PROPERTIES

1. Not written: 3.2 names the curve and defines PD(k); the header defines the curve's shares as of every loan drawn. No
   sentence says how a performing loan reads it, and the header and the policy carry no word about dividing,
   conditioning, survival, attrition, early repayment, payout or performing loans (asserted).
2. The divisor sits in a second file: only the development sample's outcomes give Cl(a), and CRM-ECL-04 carries no
   sentence about the sample (asserted), so nothing points a solver at it and nothing forbids it. The sample is in the
   run folder for an in-world reason the dictionary states: PLPD-2026.06 was approved on 24 June 2026, this is the
   first quarter-end run on it, so its release package (the curves and the sample) is filed for the external auditors'
   review of the PD model change; the entry says nothing about the sample's use (asserted).
3. The textbook move is the wrong one: 1 - C(a) is the standard survival divisor, so a careful solver who conditions
   at all reaches it first; it is wrong only because of the curve's denominator.
4. No arithmetic symptom: an allowance on 1 - C(a) reconciles to every control the pack has.
5. Not a row predicate and not an enumeration: each loan's PD path depends on its own month on book along two filed
   shares, and no column carries a conditional PD or a survival share.
6. No cutover date.
7. Survives deletion: nothing wrong to delete; deleting the asks' files moves nothing on the call (asserted).

## THREE RULES (client update, 10/10)

- **Domain (swap test).** The deciding quantity is each loan's 12-month or lifetime expected credit loss under AASB 9:
  a crude cumulative default curve under competing early repayment, turned into forward monthly PDs for loans still open
  and performing, staged on significant-increase triggers, scenario-weighted, re-amortised and discounted at the contract
  rate. Swap the nouns into another field and staging, LGD, EAD, prepayment and the coverage ratios have nothing to
  attach to, so the task does not read the same.
- **Two layers.** Layer 1 as above, all of it what a lender's systems produce. Layer 2: conditioning a crude cohort curve
  on surviving both exits.
- **Decisive step: analytical.** Analyst test: a strong analyst who cleans the book and reads 3.2 and the curve header
  correctly conditions the curve on survival to date, dividing by 1 - C(a) as the textbook conditional PD, and books
  about AUD 11.74 million against AUD 13,160,000. The v1 portal response did exactly that. The staging inputs (the
  hardship dates rule, the v3 conversion, the 90-day filter) are stated rules and move the stage split, not the call.

## CLOSURE TABLE (22 axes, the main call)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | loans open at close of business 30 September, stage 3 out (CRM-ECL-04 1.1) |
| 2 | Unit | loan |
| 3 | Attribution window | default month k after the reporting date (3.2) |
| 4 | As-of dating | stage at the reporting date; hardship in force on the date under 2.2's dates; the September month-end scoring run (2.1) |
| 5 | Version basis | the Q1 FY27 scenarios sheet, not the prior quarter's (sheet named; ARC approval date); the PLPD-2026.06 curve |
| 6 | Divisor | S(a) from the sample. C1 converge: C(a) read from the curve or recomputed from the sample (the curve is the sample's crude share to six decimals, asserted) gives 13,160,130; Cl(a) as repaid early only or early or at term gives 13,160,125 (nothing matures before its term at the months the book uses, asserted) |
| 7 | Weighting | probability-weighted scenarios, linear in PD, one multiplier of 1.06 |
| 8 | Window | 12 months stage 1, remaining term stage 2 (3.1); a loan past maturity outside stage 3 has one month remaining (3.2); read as carrying nothing instead, 13,159,860 (C3 corridor: 28 loans, AUD 266) |
| 9 | Boundary | 30 and 90 days past due, 60-point score fall: "or more" (filed) |
| 10 | Rounding | unrounded loan level (3.7); every graded figure at least 5 per cent of its bin from the edge under every kept reading (asserted; the allowance sits 0.375 of a bin from its edge, the nearest kept reading is the status-label staging at 13,160,285) |
| 11 | Tie-break | none |
| 12 | Maturity | months on book as repayments fallen due, pause dates counted (3.2, the curve header, the sample metadata, the dictionary); read without them (1,413 loans, 3,272 dates) the allowance is 13,203,812 and all three main figures move, so the pin is load-bearing (asserted) |
| 13 | Order of operations | multipliers commute with sums |
| 14 | Row order | sums only |
| 15 | Duplicates | none in the book; register rows per arrangement |
| 16 | Identity | loan_no joins book and register |
| 17 | Netting | none |
| 18 | Units | AUD; annual contract rate over 12 (3.5) |
| 19 | Codes | a cancelled arrangement stops being in force on its cancellation day (2.2); two arrangements that ended 29 September still show Active, and staging on the label keeps the allowance in its bin (13,160,285, asserted) |
| 20 | Integerisation | none |
| 21 | Clause scope | the 2.4 scalar applies to PD(k) for stage 2 only (3.2) |
| 22 | Forward window | the decisive axis, the attrition-conditioned curve. Exits are counted to the end of month a, as the header counts defaults; counting payouts in month a as still at risk, Cl(a-1) for Cl(a), lands 13,010,574 (-1.14 per cent) with stage 1 at 10,445,065 and stage 2 at 2,565,509, all three off their bins (asserted in checks.py and verify.py). The sample's metadata pins it: outcome_month_on_book is the month on book by the end of which the loan had defaulted, been repaid in full or matured, in the header's own words ("by the end of that month on book"), with nothing about conditioning, survival, open loans or the allowance (asserted) |

## ASK LEDGER (supplemental-stumping Part 9, step 4)

**The main call's declared row population** (checks.py `separation`): the September book's loans in stages 1 and 2,
the arrangements in force at 30 September, the curve and the development sample. Zero-counts asserted: of the 506
arrangements in force at 30 June and not at 30 September (57 of them cancelled after June), none is in force at 30
September under 2.2 and none of the cancelled ones carries an Active label; deleting the June extract, the scoring runs,
the Collections files and the sale schedule leaves the allowance and both stage amounts identical; deleting the curve
and the development sample leaves all 24 ask figures identical; deleting the two distractors moves nothing.

**Ask A, realised loss of the 2023-24 defaults by product and quarter (8 figures, per cent to one decimal, in the workbook)**

- Answer: PL36 67.9, 65.8, 70.7, 70.9; PL60 70.4, 77.3, 73.5, 79.3 (July to September 2023 through April to June 2024).
- Named use: the auditors set the 70 and 76 per cent LGDs (CRM-ECL-04 3.3) against what the defaults have actually lost;
  a quarter running above the filed LGD (PL60 at 77.3 and 79.3) is what the Audit and Risk Committee weighs for a
  recalibration or an overlay. It enters the call as the audit trail of the LGD input (H18).
- Primary device: the March 2026 debt sale (D6 grain). The consideration arrives as one receipt with a blank loan number
  (source Debt sale, the buyer and the sale reference in the narrative), so a per-loan sum drops it silently; each sold
  loan's share is its face value at the cut-off times the price in the schedule's header. 591 of the 1,148 2023-24
  defaults were sold, in every product and quarter, so all 8 figures move.
- Hazards crossed: cures (3.3 treats a return to performing as full recovery; taking cures from their own receipts or
  leaving them out moves all 8), the discount clock (3.3: end of the month received, whole months, contract rate;
  undiscounted moves all 8, a day count moves 7 of 8, the start of the month all 8), the dishonour reversals (texture:
  summing handles them, dropping them as errors moves no figure, asserted).
- Organ pair: CRM-ECL-04 3.3 (the measure, sale proceeds included) and the sale schedule (accounts, face values, price,
  consideration); the referee is the schedule's consideration, AUD 1,499,480.34, which equals face value times 3.85 cents
  and the blank receipt to the cent (asserted).
- File path (5 files, below the 8-file floor): collections_defaults_2023-24.csv, collections_receipts_2023-07_2026-09.csv,
  debt_sale_2026-03_schedule.xlsx, CRM-ECL-04 (1.2, 3.3), ecl_extract_dictionary.txt (Collections section).
- Columns (12 distinct): loan_no, product, contract_rate, default_month, balance_at_default, resolution; received_date,
  amount_aud, source, narrative; face_value_aud and the schedule's Price line.
- Stops (8 figures each, PL36 then PL60, Q1 to Q4; none equals the answer at one decimal on any figure):
  - s1, written-off only, undiscounted, no sale: 73.90 75.98 79.05 79.03 82.72 84.24 82.93 87.06
  - s2, cures at full recovery, undiscounted, no sale: 64.32 63.08 68.20 68.59 68.51 75.97 71.63 78.71
  - s3, discounted, no sale (the per-loan sum): 69.10 67.02 71.96 72.24 71.52 78.68 74.78 80.87
  - s4, the whole sale receipt spread over the 2023-24 written-off loans by balance (over-corrected): 63.96 61.98 66.64 66.53 66.61 73.16 69.39 74.84
  - answer: 67.90 65.81 70.71 70.92 70.41 77.30 73.48 79.32
  - also asserted off on all 8: cures from their receipts, cures left out, sale undiscounted, everything undiscounted.
- Lazy delta (every receipt summed as it stands, cures from their receipts, no sale): 75.27 78.28 79.15 80.33 84.81 84.01
  83.19 87.07, all 8 off. Converged readings: a loss floored at zero and the receipt shared over the sold loans by face
  value give the same eight figures (within 0.01 points, asserted).
- Insulation: reads no curve, no sample and no September staging; identical with them deleted (asserted).

**Ask B, where the loans in stage 1 and stage 2 at 30 June stand at 30 September (16 counts, deck slide 2)**

- Answer (stage 1, stage 2, stage 3, closed at 30 September): PL36 stage 1 at June 14,470, 680, 42, 1,586; PL36 stage 2
  468, 658, 115, 123; PL60 stage 1 17,724, 831, 46, 1,180; PL60 stage 2 560, 942, 140, 112.
- Named use: the board sees the quarter's deterioration, cures and closures behind the stage 2 amount it signs; it
  enters the call as the audit trail of the staging the call consumes (H18).
- Primary devices: B1, the stored label after a switch (D2): arrangement_status is as at 30 September, so of the 624
  arrangements in force at 30 June only 120 still read Active, and 57 that were in force then were cancelled since;
  staging June on the label, or on the dates with every Cancelled row out, misses them. B2, the run date (D8): each
  month-end run is made on the first day of the next month, so the run on the 30 June position is dated 1 July and a
  filter on run dates up to 30 June takes the May position.
- Hazards crossed: 2.2's end date counts (8 arrangements end on 30 June; excluding the end date moves 6 of 16),
  cancellation ignored (moves 8 of 16), the September status label (moves 2 of 16).
- Organ pair: CRM-ECL-04 2.1 and 2.2 (the scoring run on the position at the date; the in-force dates rule) and the
  scoring runs' own description (run_date is the day the run was made) with the dictionary's June extract section;
  the referee is 2.2's dates, which the 30 September register reproduces for every status at that date (asserted).
- File path (7 files, below the 8-file floor): personal_loan_book_2026-06-30.csv, behaviour_score_runs_2026-03_2026-08.parquet,
  hardship_register_2026-09-30.xlsx, personal_loan_book_2026-09-30.csv, scorecard_v4_migration_note.pdf, CRM-ECL-04
  (2.1 to 2.3), ecl_extract_dictionary.txt.
- Columns (12 distinct): loan_no, product, days_past_due, origination_score, origination_scorecard at both dates;
  run_date, score_v4; arrangement_start, arrangement_end, cancelled_date, arrangement_status; current_score_v4.
- Stops (counts moved of 16, every pair of stops distinct, asserted): 1 labels and the May run 16; 2 dates without any
  Cancelled and the May run 14; 3 dates and the May run 16; 4 dates without any Cancelled and the June run 14;
  5 cancellation ignored and the June run 8 (over-corrected); 6 September scores for June 16 (over-corrected);
  answer. Also off: labels with the June run 16, labels with start dates and the May run 16, the July run 16, the end
  date excluded 6. Each device alone moves at least 12 (B1 label 16, B1 every Cancelled out 14, B2 16, asserted).
- Lazy delta (labels and the May run): 16 of 16 off. Converged reading: a cancellation dated 30 June read either way
  (none falls on it).
- Insulation: reads no curve and no sample; the September staging it uses is the call's, which no device touches.

**Hazard table.** Two asks share no file but the policy and the dictionary, so each hazard sits on one ask:

| Hazard | Ask | Moves |
|---|---|---|
| cures taken from receipts or left out | A | 8 of 8 |
| receipts undiscounted, or discounted by days or from the month start | A | 8, 7 and 8 of 8 |
| dishonour reversals dropped | A | 0 (texture) |
| end date excluded | B | 6 of 16 |
| cancellation ignored | B | 8 of 16 |
| September staged on the status label | B | 2 of 16 |

**Necessity matrix** (one device mishandled, everything else right): the sale left out 8 of 8, receipts undiscounted
8, cures from their receipts 8, the sale spread over every write-off 8; B1 label 16 of 16, B1 every Cancelled out 14,
B2 the May run 16.

**Pair ceiling and the two sheets** (planning weights 38 / 7 / 55, both sheets on the strongest solver's habitual path:
per-loan sums on the ledger, the September staging code run at 30 June with a status filter and the last run dated on
or before the date): 2 of the 24 ask figures survive (two Ask B counts on stop 2). Cracker 49.6, mirror 16.6 (r = 5:
the stage 2 count and the multiplier survive a wrong curve reading), pair **33.1**. No ask answer moves between the
sheets. What the pass rests on: the habitual path. With both sheets handling the sale and Ask B left habitual the pair
is 51.4; with both handling B1 and B2 and Ask A left habitual it is 65.2; both asks right on both sheets is 83.5.
With neither top response on the call (two mirror sheets) the same cases are 34.9, 48.7 and 67.0. The 8-file span
floor is not met (5 and 7 files).

## PROMPT

934 characters and 155 words in one paragraph. `voice-check.py 133` gives 22.1 words a sentence, one sentence under
eight words, one rounding tag, no "because", and no carrier or six-word-run flag; it reads the opening as
deliverable-first, the only one in the twelve-build window. The card files the same move, against task130
stakes-first, task132 constraint-first, task134 calendar-first and task135 stakes-first.

The order since the pre-round repair: Stephanie Manning's two slides for the board; the first slide's figure, the
allowance, with the sign-off on 23 October; the chart of where the 30 June stage 1 and stage 2 loans stood at 30
September; then the workbook behind the slides, with the stage amounts and the realised loss by product and quarter.
Loop 1 ran the 23 October sign-off, the figure, the workbook and then the chair's slides, the one build order the
clone check read across task130, task132, task133, task134 and task135 (Idiom). Every requirement, unit and rounding
carries over. Ask B names 30 September where loop 1 said "now", and the "what it needs from my team" frame is gone.

## PRE-SHIP CHECK (the client's three rules and two layers)

1. Domain: the deciding quantity is the AASB 9 allowance from staging, an attrition-conditioned crude default curve,
   LGD, re-amortised EAD, scenario weights and discounting; with another field's nouns none of that has anything to
   attach to.
2. The inputs take real work (dates rather than months on book, a register read as at September, two scorecard
   versions, a June extract without the score, runs stamped the next day, a sale receipt with no loan number) and none
   of it is planted: each is how the lender's systems record it.
3. The flipping step is methodological: a crude cohort curve conditioned on surviving both exits. Not a planted catch,
   not a field reading, not a stated rule applied.
4. Analyst test: an analyst who reads every rule and the header correctly and divides by survival to date books
   AUD 11,737,000; the portal's v1 response did exactly that.
5. 3.2 defines PD(k) as the probability of default in the k-th month after the reporting date, and the header defines
   the curve as a share of every loan drawn; for a loan still open and performing only the attrition-conditioned
   increment is that probability.
6. No decoy memo, staff draft or briefing; the distractors are the roll-rate workbook and the write-off file.
7. No certified, published or prior-quarter allowance in the pack, so nothing pins the method by replay.
8. The lesson (condition a crude cohort curve on both exits) is not one an earlier build teaches: guard heart WARN, the
   nearest driver task134 at 0.18, differentiated.

## GUARD (guard.py check and heart, WARN only; surface 2 promoted on the deliverable order alone)

- three_rules.strategy_risk: the analyst test is the answer; the easy route that still fails once every rule is read is
  dividing by survival to date.
- driver.near task134 (0.18, heart 0.14): differentiated on the card. task134 estimates the probability that a released
  unit has an event within a fixed horizon from censored follow-up with competing exits, an estimator under incomplete
  observation; here the curve is filed and every development cohort is complete, nothing is censored or estimated, and
  the move is conditioning a filed crude cohort curve on each performing loan having come through both exits.
- driver.near task133 v1 (0.27, this slot): differentiated; the loop moves the decisive rung from survival to date to
  survival of both exits on the same curve.
- people.first Kayla (task118) and Christine (task104): older builds only, ordinary first names, drawn by guard.py names.
- repeat.gate_g forecasting (task130 v3, task132): both sit in the Forecasting block with different mechanisms.
- people: the only persona the cut pack names is Stephanie Manning, on the card.

Surface after the pre-round repair: two pairs promoted, task124 (0.149) and task89 (0.143), and the one axis that moved
is the deliverable species, which the screen reads in the order the prompt names the files. The prompt now names the
deck before the workbook, as both of those prompts do. Neither pair shares wording, a file name, a schema, a persona
or an invented name with task133, and before the repair the same pairs scored 0.089 and 0.083. Naming the workbook
first again would undo the prompt-order repair, so the pairs are left for the author's /clone-check.

## LEAK REVIEW

- `leak.py --asof 2026-10-12` on the loop 1 cut: REVIEW, no LEAK. Each line:
  - author vocabulary "the model" in CRM-ECL-04 3.2: it is the model team, the department that owns the curve.
  - golden figures 680 and 560 in the scorecard migration note: v3 scores in its conversion table, not the migration
    counts they coincide with.
  - CRM-ECL-04 carries 8 of 9 words of the call: its scope sentence names the allowance it governs, with no figure.
  - stump-term overlap (CRM-ECL-04 10 of 25: staging, status, months, forward, reporting, repayment; the dictionary 8
    of 25: sample, months, reporting, repayment, arrangement, performing): the subject's own words, with "performing"
    only in the cure definitions of 3.3 and the Collections fields; neither document names the move, and neither says
    anything about dividing, conditioning, survival or early repayment (asserted).
  - dates after the setting: in the register, the end dates of arrangements in force and the dates of approved ones
    not yet started; in the September book, the first repayment dates of loans drawn in September.
- v1's four reader rounds left these in the generator, and they stand: the pause pin and the past-maturity pin in 3.2,
  the curve header, the sample metadata and the dictionary; Office 2013-2022 containers with in-fiction creators and
  dates; the development sample extracted Tuesday 2 June 2026; the plain clauses 1.5, 1.6, 1.7, 2.4, 2.5, 3.6 and 3.7;
  57 blank states for overseas addresses and a few pre-July 2020 cases with no reason; the Tuesday-night status batch;
  the policy's statistics and revision ids; the register written by svc_crr_batch and last saved by Kayla Stokes; the
  migration note left as LibreOffice output; the 2021 lockdown pauses on loans closed before 30 September.
- Loop 1 changed documents under `target/` and the prompt, so the main session's reader pass runs on this cut.
- Pre-round repair of the loop 1 read. The reader found no sentence that hands over the step and no file that states
  the answer. Its question 3 (the development sample read as there only to help) is answered by a filing note under
  the sample's entry in the run folder's list of other files. The fork on the main call (whether a loan repaid in full
  during month on book a is still on the books at a) is closed by closure row 22's pin. The filing note is not repeated
  in the sample's own description, which was written at extraction on 2 June 2026, before the approval. leak.py on the
  repaired cut: REVIEW, no LEAK, the same files and lines as above. Under `target/` only `ecl_extract_dictionary.txt`
  and `pd_model_development_sample.parquet` changed, so the next read covers those two files and the prompt.
- The same commit replaces two stale blobs left under `target/` at 22d2dfd, the September book (three rows) and the
  roll-rate workbook, each an older build's file of the same byte size, which git never saw change. `target.zip` and
  the generator already carried the current files; on the stale folder BPL2247062 stays in stage 1 (3,265 in stage 2
  against 3,266) and two ask B counts move.

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
- Stale arrangement_status labels, revisited in repair 3: built after all with a Tuesday-night status batch (two arrangements that ended 29 September still show Active), because a Sunday or Monday batch moved a status-only staging's allowance out of its bin (AUD 13,778,000 or 13,775,000) while the Tuesday batch moves one PL36 loan and keeps the bin (asserted); the line above records the earlier refusal.
- v1's conditioning on survival to date was landed on the portal: one model filed AUD 13,773,000 by dividing the curve's increments by 1 - C(a) and scored 100 per cent, the other was stumped; loop 1 files the curve as the crude default share of every loan drawn, so that division is now rung R4 (10.8 per cent low).
- The inheriting asks (stage by product, drawdown year, the stage 3 count) were banked by the response that landed the call, because each was an output of the same construction; loop 1 retires them for two asks that read neither the curve nor the sample.
- A debt-sale price of 10.35 cents: leaving out the discounting and leaving out the sale move each figure by similar amounts in opposite directions anywhere from about 7 to 22 cents, so stop s2 landed 0.11 points from a figure; at 5 cents or below the two effects stay at least 0.8 points apart, and a few cents is what aged written-off unsecured debt sells for, so the price is 3.85 cents.
- Agency remittances capped at a fixed monthly amount: 62 per cent of the remittances sat exactly on the cap, a pattern no collections ledger shows; replaced by a log-normal affordability draw per arrangement, its median raised to AUD 320 when the first draw left recoveries under the level the 70 and 76 per cent LGDs imply.
- Dating each default on the day it reached 90 days past due: 39 of the 2023-24 defaults resolved inside that same month, so the population turned on a day-or-month reading; 1.2 now records the default at the first month end at 90 or more days past due, and the defaults file carries only those (no default resolves in its default month, and no receipt falls in it).
- Hardship windows that reached the instalments of a default run (18 loans, 4 of them 2023-24 defaults) cleared those instalments in the simulation; the windows now stop before the run's first missed instalment.
- The release-package filing note in the development sample's own metadata (pre-round repair): not built. It was written at extraction on 2 June 2026, before the 24 June approval and months before the September run, so a note about this run cannot sit there without moving the file's date; the note is in the run folder's list of other files, which Credit Risk Reporting keeps for the run.
- A calendar-first prompt with the workbook commissioned before the chair's slides (loop 1): the same build order as task130, task132, task134 and task135, read by the clone check as one skeleton across the lane (Idiom); it now opens on the slides and puts the workbook behind them.
