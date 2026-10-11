# task133 design note: Bellbird personal loans, the 30 September 2026 ECL allowance

Private, never ships. Architecture v1, hardening loop 1 (2026-10-11). The portal round: one model was stumped, the
other landed AUD 13,773,000 at 100 per cent by dividing the curve's increments by survival to date, and every ask went
with it because each was an output of the same construction. This loop takes the main rung one step deeper (the curve
is now the crude default share of every loan drawn, so survival to date is itself a wrong rung) and replaces the asks
with two that the call's construction never touches. Seed FC04 (station maturity) was not used: its forward-maturity
driver repeats the age-forward structure of task132 drawn the same day. Stage 6b (2026-10-11) answers the loop 1 round,
whose careful solver missed the call and cracked both asks: each ask now sits under a silent device on rows the call never
reads, the deferred forks are pinned, CRM-ECL-04 and the run-folder dictionary read as working documents, and PLPD-2026.06
is released smoothed. The prompt, the call, the ladder and every golden figure are unchanged.

## DRAW

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task133.json`, rewritten for loop 1 with the v1 driver in `lineage`, opening move deliverable-first since the pre-round repair, `layer1` brought up to the 6b pack; check and heart WARN only, surface 2 promoted on the deliverable order alone (GUARD below) |
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
read as at 30 September, with the 2020 and 2021 COVID-19 deferrals loaded in bulk and never moved on; origination scores
on two scorecard versions with a published conversion; a smoothed curve file with one curve per product and a model
version, beside the complete-term development sample it was fitted to; scenario weights in a committee workbook beside
the prior quarter's; the June quarter-end extract from the same job without the behaviour score column (added by a
change in July) and, from before the same change, counting days past due to its 07:30 run, beside month-end scoring runs
stamped with the day each run was made; a Collections MI file whose case resolution is set when the case closes, so a
cure recorded on an approved arrangement stands after the arrangement is withdrawn; a receipts ledger across every
cohort with dishonoured direct debits reversed by negative rows and one debt-sale receipt carried without a loan number,
and the sale schedule priced in cents per dollar of face value; a write-off file (settlement shortfalls included) and a
roll-rate workbook that set nothing.

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
| R0 | Curve read from origination for every loan | 18,265,903 | +38.80% |
| Rh | Default hazard from the sample rolled forward with no early repayment (any default-only survival or Kaplan-Meier rebuild lands here) | 14,069,675 | +6.91% |
| **Answer** | Increment from months on book divided by S(a) = 1 - C(a) - Cl(a), stage 2 scalar, scenarios, re-amortised EAD, discounted | **13,160,123, AUD 13,160,000** | |
| R4b | S(a) conditioning plus a second early-repayment survival factor on EAD (repayment counted twice) | 12,366,781 | -6.03% |
| R4 | Divided by 1 - C(a), survival to date (v1's answer, the path the portal response took) | 11,736,900 | -10.81% |
| R3 | Shifted to months on book, no division (the loop 1 round's answer) | 11,421,233 | -13.21% |

Every rung misses the allowance and both stage amounts at the nearest thousand and sits at least 5 per cent from the
answer (asserted in checks.py and verify.py; the nearest are R4b at 6.03 per cent and Rh at 6.91 per cent, with nothing
planted to widen either). The answer's stage amounts are AUD 10,563,202 and 2,596,921. Off the curve: no discounting is
+9.32 per cent, the balance held flat +16.66 per cent; dropping the hardship register moves 470 loans out of stage 2 and
the allowance -1.76 per cent, skipping the v3 conversion moves 786 and -0.85 per cent (floors of 300 and 100 loans
asserted).

**The released curve (6b).** PLPD-2026.06 is released smoothed, as a model team releases a curve (loop 1 shipped the
sample's crude share, with a step in each product's last month). From month on book 4 the log of each month's increment
is a natural cubic spline in month on book (knots and coefficients in world.py), fitted to the sample's monthly default
shares weighted by the defaults in each month, the final month (which collects every default recorded after the last
repayment date) left out of the fit; months 1 to 3 are the sample's own shares. `tune_curve.py` then moves the
coefficients as little as the fit allows so the allowance and both stage amounts come out as they do on the sample's own
shares, with the divisor's default share read from the curve and from the sample (closure row 6). Asserted: within 0.001
of the sample before the term; increments positive and peaking in months 5 to 7, as the sample's do; roughness past the
peak 0.084 (PL36) and 0.031 (PL60) of the sample's, with 2 turns against 15 and 39; lifetime shares 0.0893 and 0.1056
against the sample's 0.0926 and 0.1066. The header says the column is smoothed and how, and still defines it as a share
of every loan drawn.

## SURVIVAL PROPERTIES

1. Not written: 3.2 names the curve (PLPD-2026.06) and defines PD(k); the header defines the curve's shares as of every
   loan drawn, smoothed. No sentence says how a performing loan reads it, and the header and the policy carry no word
   about dividing, conditioning, survival, attrition, early repayment or payout (asserted; "performing" appears in the
   policy only in 3.3's cure clause, in the LGD review).
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
| 4 | As-of dating | stage at the reporting date; days past due at close of business (1.3); hardship in force on the date under 2.2's dates; the behaviour score from the September month-end scoring run (the book's current_score_v4) |
| 5 | Version basis | the Q1 FY27 scenarios sheet, not the prior quarter's (sheet named; ARC approval date); the PLPD-2026.06 curve |
| 6 | Divisor | S(a) from the sample. C1 converge: the divisor's default share read from the curve (13,160,123) or from the sample's own shares (13,160,122), and the curve rebuilt from the sample unsmoothed (13,160,130), put all three figures in their bins with 5 per cent to spare (asserted in checks.py and verify.py; the smoothing is fitted under exactly these constraints); Cl(a) as repaid early only or early or at term gives 13,160,123 (nothing matures before its term at the months the book uses, asserted) |
| 7 | Weighting | probability-weighted scenarios, linear in PD, one multiplier of 1.06 |
| 8 | Window | 12 months stage 1, remaining term stage 2 (3.1); a loan past maturity outside stage 3 has one month remaining (3.2); read as carrying nothing instead, 13,160,056 (C3 corridor: 28 loans, AUD 66) |
| 9 | Boundary | 30 and 90 days past due, 60-point score fall: "or more" (filed) |
| 10 | Rounding | unrounded loan level (3.7); every graded figure at least 5 per cent of its bin from the edge under every kept reading (asserted; the allowance sits 0.377 of a bin from its edge, stage 1 0.298, stage 2 0.421; the nearest kept reading is the status-label staging at 13,160,286) |
| 11 | Tie-break | none |
| 12 | Maturity | months on book as repayments fallen due, pause dates counted (3.2, the curve header, the sample metadata, the dictionary); read without them (1,413 loans, 3,272 dates) the allowance is 13,204,961 and all three main figures move, so the pin is load-bearing (asserted) |
| 13 | Order of operations | multipliers commute with sums |
| 14 | Row order | sums only |
| 15 | Duplicates | none in the book; register rows per arrangement |
| 16 | Identity | loan_no joins book and register |
| 17 | Netting | none |
| 18 | Units | AUD; annual contract rate over 12 (3.5) |
| 19 | Codes | a cancelled arrangement is not in force (2.2: "unless it has been cancelled"; no cancellation falls on 30 September or 30 June, asserted); two arrangements that ended 29 September still show Active, and staging on the label keeps the allowance in its bin (13,160,286, asserted); the 384 bulk-loaded COVID-19 rows still read Active and every one sits on a loan closed before 2026 (asserted) |
| 20 | Integerisation | none |
| 21 | Clause scope | the 2.4 scalar applies to PD(k) for stage 2 only (3.2) |
| 22 | Forward window | the decisive axis, the attrition-conditioned curve. Exits are counted to the end of month a, as the header counts defaults; counting payouts in month a as still at risk, Cl(a-1) for Cl(a), lands 13,010,833 (-1.13 per cent) with stage 1 at 10,445,239 and stage 2 at 2,565,594, all three off their bins (asserted in checks.py and verify.py). The sample's metadata pins it: outcome_month_on_book is the month on book by the end of which the loan had defaulted, been repaid in full or matured, in the header's own words ("by the end of that month on book"), with nothing about conditioning, survival, open loans or the allowance (asserted) |

## ASK LEDGER (supplemental-stumping Part 9, step 4; hardened at 6b)

The loop 1 round's solver missed the call (R3, AUD 11,421,000) and banked both asks: it shared the lump sale receipt out
at 3.85 cents a dollar of face value, netted the dishonours, discounted monthly from the default month end, set cures to
nothing, scored June from the 1 July run and took hardship in force by 2.2's dates. Every device it beat sat on the
hygiene battery's path (a blank loan number) or behind a filed rule it executed (3.3's sale clause, the run_date note,
2.2's wording). 6b keeps those devices as hazards and puts one silent device under each ask, on rows the call never
reads, visible only at a cross-file or cross-grain cut nothing invites, and resolved uniquely by the pack's own records.
No golden figure moved: each device changes what the careful path reads, not what happened.

**The main call's declared row population** (checks.py `separation`): the September book's loans in stages 1 and 2, the
arrangements in force at 30 September, the curve and the development sample. Zero-counts asserted: none of the 59
withdrawn collections arrangements and none of the 384 bulk COVID-19 rows is in force at 30 September or at 30 June,
none of them sits on a loan in either book, and no written-off withdrawn cure is a stage 1 or 2 loan; the 1,827 June
loans whose days past due the June extract counts to its run sit in a file the call never reads; of the 506
arrangements in force at 30 June and not at 30 September (57 cancelled after June), none is in force at 30 September
and none of the cancelled ones reads Active. Deleting the June extract, the scoring runs, the Collections files and the
sale schedule leaves the allowance and both stage amounts identical; deleting the curve and the sample leaves all 24 ask
figures identical; deleting the two distractors moves nothing. The September book, the receipts ledger, the sale
schedule, the scenarios and the migration note are byte-identical to loop 1.

**Ask A, realised loss of the 2023-24 defaults by product and quarter (8 figures, per cent to one decimal, in the workbook)**

- Answer (unchanged): PL36 67.9, 65.8, 70.7, 70.9; PL60 70.4, 77.3, 73.5, 79.3 (July to September 2023 through April to
  June 2024).
- Named use: the auditors set the 70 and 76 per cent LGDs (CRM-ECL-04 3.3) against what the defaults have lost; it enters
  the call as the audit trail of the LGD input (H18).
- Primary device A1, silent (D2, a stored label taken before a silent switch): Collections closes a default case as cured
  when it approves a collections hardship arrangement, dated from the arrangement's start, and does not reopen the case
  when the arrangement is withdrawn. 59 arrangements approved on 2023-24 defaults were withdrawn before they started: on
  43 loans that stayed in default, were written off and were still paying Wirraway at the March 2026 sale (so none was
  sold), and on 16 that caught up instead. The MI file reads Cured for all 59. Taking every label at its word (the
  careful path) zeroes 43 written-off losses and lands every figure 2.4 to 3.1 points low.
- Why it survives the battery: keys unique, no duplicate rows, every receipt and every case joins, every cure carries a
  date, and 3.3's cure clause ("A loan that returns to performing has lost nothing.") reads as executed. The
  inconsistency exists only across files: a case closed as cured whose loan the agency later collects from (the
  dictionary's source field: agency remittances fall on written-off accounts), and whose arrangement the register shows
  cancelled before its start.
- Resolution, unique: the 43 never returned to performing (the arrangement never began, no catch-up, write-off and agency
  recoveries followed), so 3.3 measures them on their receipts; the register rule and the ledger rule select the same 43
  (asserted), and the rule the golden states holds over every case (every arrangement approved after a 2023-24 default
  closed its case as cured, dated from its start: 120 of 120, 61 completed and 59 withdrawn). Over-cleaning half: the 16 that caught up did return to
  performing and lose nothing (each has its catch-up receipt); doubting every cure on a withdrawn arrangement lands every
  figure 0.8 to 1.6 points high.
- Sizing (generator, asserted): in each product and quarter the written-off cases are drawn until the loss their labels
  hide is at least 2 points of the cell's balance at default and 1 point more than the sale recovered there, so taking
  the labels at their word and leaving the sale out cannot cancel; the caught-up cases until their doubted loss is at
  least 0.8 points.
- Hazards crossed (the careful solver executes these): the sale receipt with no loan number (D6, shared out by face
  value), the cure clause, the discount clock (3.3 and 3.5), the dishonour reversals (texture: dropping them moves no
  figure).
- Pins for the deferred forks, in 3.3: "A loan that returns to performing has lost nothing." (reading a cure as its full
  balance recovered at the cure and discounted moves all 8) and "discounted to the default month end monthly at the
  contract rate, as in 3.5" (the annual rate per whole month moves all 8). Neither names a device.
- Organ pair: CRM-ECL-04 3.3 with the register (the withdrawn arrangement) and the ledger (agency remittances); the
  referee is the sale schedule's consideration, AUD 1,499,480.34, face value times 3.85 cents and the blank receipt to
  the cent.
- File path (6 files): collections_defaults_2023-24.csv, collections_receipts_2023-07_2026-09.csv,
  debt_sale_2026-03_schedule.xlsx, hardship_register_2026-09-30.xlsx, CRM-ECL-04 (3.3, 3.5), ecl_extract_dictionary.txt
  (section C).
- Columns (15): loan_no, product, contract_rate, default_month, balance_at_default, resolution, resolution_date;
  received_date, amount_aud, source; face_value_aud and the Price line; arrangement_start, arrangement_status,
  cancelled_date.
- Stops (PL36 then PL60, Q1 to Q4; none equals the answer at one decimal on any figure, each at least 0.15 points off):
  - careful, this round's path with every cure at its word: 65.11 63.38 67.92 68.37 67.92 74.64 70.87 76.21
  - s3, the per-loan sum, no sale, cures at their word: 66.32 64.58 69.17 69.69 69.03 76.02 72.17 77.76
  - s1, written-off cases only, undiscounted, no sale: 74.63 78.78 80.43 81.02 82.79 84.39 83.09 88.03
  - s2, cures in, undiscounted, no sale: 61.94 61.49 65.88 66.63 66.16 73.44 69.15 75.87
  - s4, the sale receipt spread over the written-off cases by balance: 61.18 59.63 63.89 64.03 64.08 70.47 66.74 71.76
  - over-cleaner, every cure on a withdrawn arrangement doubted: 69.22 66.83 71.58 72.29 71.99 78.37 74.33 80.16
  - answer: 67.90 65.81 70.71 70.92 70.41 77.30 73.48 79.32
  - also off on all 8: cures from their receipts, cures left out, the sale undiscounted, everything undiscounted, the lazy
    path; 3.3 misread by days 7 of 8, from the month start, at the annual rate or with the cure discounted 8 of 8.
- Composed mishandlings (cure rule by sale handling by discounting, 79 paths): every path with one or two mishandled
  devices misses all 8, the days misreading aside; three at once reach at most 2 (asserted).
- Insulation: reads no curve, no sample and no September staging; identical with them deleted (asserted).

**Ask B, where the loans in stage 1 and stage 2 at 30 June stand at 30 September (16 counts, deck slide 2)**

- Answer (unchanged; stage 1, stage 2, stage 3, closed at 30 September): PL36 stage 1 at June 14,470, 680, 42, 1,586;
  PL36 stage 2 468, 658, 115, 123; PL60 stage 1 17,724, 831, 46, 1,180; PL60 stage 2 560, 942, 140, 112.
- Named use: the board sees the quarter's deterioration, cures and closures behind the stage 2 amount it signs; it enters
  the call as the audit trail of the staging the call consumes (H18).
- Primary device B3, silent (D8, a clock against a filed cutoff): ECL_QE_BOOK ran the June extract at 07:30 on 1 July,
  before CHG-26-0418, when it counted days past due to its run, so every one of the 1,827 June loans in arrears reads a
  day further than at close of business on 30 June: the 69 at 29 days read 30 and the 6 at 89 read 90. Read as
  extracted, 14 of the 16 counts move.
- Why it survives the battery: the column parses, keys join, the two extracts agree on every static field, the
  dictionary describes both as loans open at close of business on the quarter end, and the change log records only
  CHG-26-0418's new column. The inconsistency exists only across grains: no June value sits on a due date counted back
  from 30 June (0 of 1,827, asserted), and 15 loans read 180 days after a batch that writes off at 180.
- Resolution, unique: 1.3 takes days past due at close of business on the reporting date, one day less than the extract
  shows, floored at 0.
- Hazards crossed (the careful solver executes these): B1 the status label after the switch and the cancellations (2.2's
  dates), B2 the run dated 1 July for the June month end (the runs file names the month ends it scores), 2.2's end date,
  the September status lag (2 counts).
- Pin for the deferred fork: the dictionary says a loan leaves the extract once it closes (repaid in full, settled or
  written off), and stage 3 is a stage (1.1, 1.2), so the slide's four states are stages 1, 2 and 3 and closed.
- File path (7 files): personal_loan_book_2026-06-30.csv, personal_loan_book_2026-09-30.csv,
  behaviour_score_runs_2026-03_2026-08.parquet, hardship_register_2026-09-30.xlsx, scorecard_v4_migration_note.pdf,
  CRM-ECL-04 (1.3, 2.1 to 2.3), ecl_extract_dictionary.txt.
- Columns (13): loan_no, product, days_past_due, first_repayment_date, origination_score, origination_scorecard at both
  dates; run_date, score_v4; arrangement_start, arrangement_end, cancelled_date, arrangement_status; current_score_v4.
- Stops (counts moved of 16, every pair distinct, asserted): careful, as extracted with the 1 July run and 2.2's dates,
  14; 1 labels and the May run 16; 2 dates without any cancelled and the May run 16; 3 dates and the May run 16; 4 dates
  without any cancelled and the June run 11; 5 cancellation ignored 14; 6 September scores for June 16; labels and the
  June run 16; the July run 16; the end date excluded 14. Every composed path (days past due by hardship rule by run, 39
  paths) moves at least 6.
- Insulation: reads no curve and no sample; the September staging it uses is the call's, which no device touches.

**Necessity matrix** (one device mishandled, everything else right): A1 the cure labels at their word 8 of 8, the sale
left out 8, receipts undiscounted 8, every cure measured on its receipts 8, the sale spread over every write-off 8; B3
the June arrears as extracted 14 of 16, B1 the label 16, B1 every cancelled out 14, B2 the May run 16.

**Pair simulation** (planning weights 38 / 7 / 55; r = 5, the stage 2 count and the multiplier surviving a wrong curve
reading). Both top responses are this round's careful solver: the hygiene battery applied, every filed rule it points at
executed, every field read as its file describes it. Each keeps 2 of the 24 ask figures (the two PL36 counts into stage
2 that B3 does not move). One on the call: cracker 49.6, mirror 16.6, pair **33.1**. Neither on the call: 16.6. The
habitual sheet (per-loan sums, the last run made by the date, hardship off the status label) keeps none: pair 28.5. What
the pass rests on: the two silent devices. Both responses catching A1 alone would put the pair at 51.4, B3 alone at 65.2,
both at 83.5.

**Span floor.** Not met: ask A spans 6 files and ask B 7, against a floor of 8. Neither ask may read the curve or the
development sample (the separation that keeps both decoupled from the call), which leaves 11 of the 13 files the
solution uses, and no further file enters either computation without a dependency written for the purpose.

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

6b left the prompt word for word (934 characters): both devices and every pin sit in the pack, so the asks' wording
needed no change, and the repair goes to the judge without a fresh solver round on the prompt's account.

## PRE-SHIP CHECK (the client's three rules and two layers)

1. Domain: the deciding quantity is the AASB 9 allowance from staging, an attrition-conditioned crude default curve,
   LGD, re-amortised EAD, scenario weights and discounting; with another field's nouns none of that has anything to
   attach to.
2. The inputs take real work (dates rather than months on book, a register read as at September, two scorecard
   versions, a June extract without the score and counting arrears to its morning run, runs stamped the next day, a
   sale receipt with no loan number, Collections cases closed as cured on arrangements later withdrawn) and none of it
   is planted: each is how the lender's systems record it.
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

6b: `guard.py check` and `heart task133` WARN with the same lines as above and no BLOCK; `surface task133` promotes the
same two pairs at the same scores (task124 0.149, task89 0.143) and nothing new; the card's `layer1` now names the
June extract's arrears clock, the Collections case closure, the bulk COVID-19 statuses and the smoothed curve.

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
- 6b cut, `leak.py --asof 2026-10-12`: REVIEW, no LEAK. The "the model" line is gone (3.2 now names Credit Risk
  Modelling and PLPD-2026.06). Each remaining line:
  - golden figures 560 and 680 in the migration note: v3 scores in its conversion table, as before.
  - CRM-ECL-04 carries 8 of 9 words of the call: its scope sentence, with no figure.
  - stump-term overlap, CRM-ECL-04 9 of 25 (months, performing, reporting, staging, nothing, status, repayment,
    arrangement, forward): the subject's own words; "performing" and "nothing" sit only in 3.3's cure clause, about the
    LGD review, and "forward" is section 4's heading. The dictionary 9 of 25 (sample, months, reporting, nothing,
    development, repayment, arrangement, dictionary, register): field definitions and its own section names; "nothing"
    is the pause's "nothing payable". Neither names the move or says anything about dividing, conditioning, survival or
    early repayment (asserted).
  - dates after the setting: unchanged (arrangement end dates and approved starts; first repayments of September
    drawdowns).
- 6b changed documents under `target/` (CRM-ECL-04, the dictionary, the curve header, the descriptions in both parquet
  files) and data on the ask paths (the June extract's days past due, the Collections MI file, the register's new rows
  and COVID-19 statuses, the write-off file), so a reader's pass on this cut is owed before the round or the judge
  reads it; the earlier reader sections stay appended to the report.

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
- The blank-key sale receipt as ask A's primary device (loop 1 round): the careful solver found the blank loan number with the hygiene battery and shared the receipt out at the schedule's price, as 3.3 told it to; it stays as a hazard under the silent cure-label device.
- The status label and the run date as ask B's primaries (loop 1 round): the solver took hardship in force by 2.2's dates and the 1 July run from the file's own run_date note; both stay as hazards under the silent arrears clock.
- Smoothing PLPD-2026.06 freely (6b): a three- or five-month moving average, a log-linear tail, block-preserving fits and an unconstrained log spline moved the allowance by 12k to 235k and split the divisor's default share between the curve and the sample by 0.5k to 6.4k, several bins either way; the released spline is fitted under the six constraints that keep both readings, and the unsmoothed rebuild, in every bin.
- Smoothing only the last month's step (6b): left the noise the reader flagged and moved the allowance by 20k on its own.
- A cure that re-defaults as ask A's device (6b): the cure clause either blesses the wrong answer (a loan that returned to performing and later defaulted again "lost nothing") or announces the check ("and does not default again"); a cure recorded on an arrangement withdrawn before it started has no such fork, because the loan never returned to performing.
- Paused loans left out of the June extract as a second silent device for ask B (6b): 7 of the 181 pauses in force at 30 June sit on loans closed by 30 September, whose product nothing else in the pack gives, so the June population could not be rebuilt; not built.
- Agency remittances carried gross of Wirraway's commission as a span-adding ask A device (6b): needs a filed "net of commission" rule the careful solver would execute and a commission source; not built.
- The caught-up half of the cure-label device sized at 0.3 points (6b): doubting every cure on a withdrawn arrangement and leaving the sale share undiscounted then cancelled to the answer in one cell; the caught-up cases are drawn to 0.8 points.
- The 8-file span floor for both asks (6b): not met (6 and 7 files). The asks may not read the curve or the sample, and every other file left (the scenarios, the two distractors) could enter only through a dependency written for the purpose.
