# task133 design note: Bellbird personal loans, the 30 September 2026 ECL allowance

Private, never ships. Round 2 (2026-10-14), the slot's second architecture under the same draw. The 10/10 audit found
the loop 1 build compliant but weak: its decisive step (conditioning a crude cohort curve on survival of both exits) sat
one rung above the step the v1 portal winner solved, and the development sample's prepaid outcomes beside a "share of
every loan drawn" header signposted it. Round 2 moves the decisive step inside the same world. There is no filed curve
any more: CRM-ECL-04 3.2 files the PD estimand and points at the loan system's record of every loan it has held, and the
record holds the earlier platform's loans only from the 1 October 2019 go-live, when the loan system took over those
still open. A competent PD build (monthly default and repayment rates by month on book, repayment as a competing exit,
the textbook survival product) counts those loans from their drawdown and fills every early month's loans at risk with
months the record never observed. The allowance is now reported in AUD million to one decimal. Ask A gains a second
silent device (reissued agency references); ask B keeps its June arrears clock, now with the record's default month as
in-world evidence. At stage 4 the judge reproduced the main call (13.179) and found both asks open: every Collections cure
taken at its word, the remittances taken where the receipts file posts them and the June column read as close of
business gave its own loss shares and counts. The asks repair (2026-10-14, main call frozen) files each in the text the
lender would write: 3.3 measures a loan the record shows written off on what it recovered, pools the share by balance
and keeps 70 and 76 per cent in force; the dictionary says what the receipts file's loan number and Wirraway's
reference hold, that a closed loan is in no stage, and records the job's move to the end-of-day snapshot at
CHG-26-0418; 2.2 says when a cancelled arrangement stops. No graded figure moved. The re-judge (round 2b) reproduced the main call,
the stage amounts and all eight loss shares and found one gap, slide 2's June clock: no file said the June extract counts
days past due to its run date. The dictionary's two loan book lines now record each extract's run clock (the judge's
prescribed fix), CRM-ECL-04 2.4, 3.3, 3.6 and the 4.2 history line read plainer. Round 2c gives ask B a new silent
device (B4: the June month end's scoring run carried one partition's last scores forward on 1 July and rescored it on 2
July), with no ask B figure moving, redraws the forum to the Audit and Risk Committee (deck arc_ecl_q3_2026.pptx) and the
hardship register's job-account persona, both against heart BLOCKs.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task133.json`, edited in place for round 2 (the slot's 2026-10-11 draw kept: world, forum, forcing event, organisation), v1 and loop 1 in `lineage`; heart WARN, no BLOCK (GUARD lines in Ask sheet's tail and below) |
| Domain / task type | banking-credit-financial-risk / expected-credit-loss-provisioning (client domain itself) |
| Objective | Forecasting & Predictive Modeling: the allowance is the expected loss over each performing loan's next 12 months or remaining life, its PD estimated from the record's default and repayment experience |
| Shape | 02: one committed figure with its stage split, plus two grids (realised loss by product and quarter, 8 cells; the June book's stages by where they stand at 30 September, 16 cells) |
| Gate G mechanism | forecasting |
| Gap, pattern | population (who is at risk in each month on book: a taken-over loan only from the take-over), then time; pattern none, the generators leading with G12 |
| Generators | G12 absence of record against record of absence, G9 downstream survival against upstream acquisition, G13 horizon mismatch |
| Stump strategy | maturity_censoring (relabelled from stated_rule_hard_construction): left truncation, the record watching the taken-over loans only from the go-live; population_selection names the same risk-set error from the denominator side and is banned against task132 at this draw |
| Layer 2 family / pattern | estimation_fit / `own:delayed-entry-for-a-taken-over-book` |
| Decisive rule filed | no: 3.2 files the estimand (PD(k) for a loan in month on book a is the probability that a loan of the product open and not in default at the end of a first defaults at a + k, from every loan of the product in the record) and no method; nothing filed names entry, truncation, the risk set or the take-over's effect (asserted) |
| Official decoy, validated decoy | no, no |
| Decision | quantity_figure, currency |
| Stakeholder | Head of Credit Risk Reporting (finance_controller), to the Audit and Risk Committee (committee_or_panel, redrawn from board_of_directors in round 2c), at the quarter close (period_close) |
| Context artifact | register: the loan record, the loan system's list of every loan it has held |
| Calibration form | none |
| World | New South Wales, AUD; Bellbird Personal Finance (fictional non-bank lender); PL36, PL60; Wirraway Mercantile Agents (collections agency) and Tarwin Receivables Pty Ltd (debt buyer), both invented |
| People | Matthew Gardner, Stephanie Manning, Joseph Mitchell, Tamara Farrell, Adam Gordon, Renee Foster, Troy Olson, Natalie Hanna, Declan Wallace (round 2c, seed 133, for Vanessa King), Christine Fletcher (guard.py names, en_AU, seed 133; Vanessa King replaces Kayla Stokes, whose first name the guard now blocks against task118) |

**Data-native sentence.** Bellbird's loan system went live on 1 October 2019 and took over only the loans still open and
under 90 days past due on the earlier platform, so the record's 2014 to 2019 vintages are survivors (163 loans from 2014
against 5,271 from 2018, mostly PL60s from before 2017): 16,479 loans the record holds only from their month on book at
30 September 2019, whose earlier months could not end in a recorded default or closing, sit in every early month on
book's loans at risk if each loan is counted from its drawdown, and the young book (median month on book 14 for PL36,
21 for PL60) reads its PD from exactly those months.

**Sources.** `layer2-rigor-patterns.md`, banking (PD term structures from loan-level performance with prepayment as a
competing risk): teaches the default path's own construction; here the competing exit is the reflex and the step past it
is where exposure starts. `exemplars.md` (the client's ECL and survival tasks): the depth of a staged ECL build; none
turns on entry to observation. task134 v1 (an estimator under censoring with competing exits, landed): the reason the
audit's suggestion (Aalen-Johansen on right-censored vintages) was not taken; censoring and competing exits are the
default path here. task255 (deductibles carried as truncation on a size distribution): truncation of sizes by a floor;
here it is truncation in time, by the date a record began. task132 (module-age band rates over a go-live window with
renewal): a renewal process; here a loan defaults once and the issue is which months the record watched.

**Layer 1 (the mess, and the systems that make it).** A loan system extract that gives drawdown and first-repayment
dates rather than months on book, repayment dates moved to the next NSW business day; a loan record carrying the earlier
platform's loans under their own lower numbering block, defaults at month ends and closures by reason; a hardship
register of approved, active, completed and cancelled arrangements whose status is set by a Tuesday-night batch and read
as at 30 September, with the 2020 and 2021 COVID-19 deferrals loaded in bulk and never moved on; origination scores on
two scorecard versions with a published conversion; scenario weights in a committee workbook beside the prior quarter's;
the June quarter-end extract from the same job without the behaviour score column (added by a change in July) and, from
before the same change, counting days past due to its 07:30 run, beside month-end scoring runs stamped with the day each
run was made; a Collections MI file whose case resolution is set when the case closes, so a cure recorded on an approved
arrangement stands after the arrangement is withdrawn; a receipts ledger across every cohort with dishonoured direct
debits reversed by negative rows, one debt-sale receipt carried without a loan number and agency remittances posted by
the reference they quote; the agency's placement report with its own column names and day-first dates, whose references
the agency reissues after a placement closes; the sale schedule priced in cents per dollar of face value; a write-off
file and a roll-rate workbook that set nothing.

**Layer 2 (the shortcut, and why an expert refuses it).** The textbook PD build from a loan-level record: for each
product and month on book, the share of the loans open and not in default at its start that default in it and the share
that close, then PD(k) as the default rate at a + k times the survival through a + 1 to a + k - 1. Every step of that is
right except who is at risk: the record holds a loan drawn in 2016 only because it was still open in October 2019, so its
months on book before then are months nobody watched it could have defaulted in. Counting it from drawdown puts it among
the loans at risk in months where only survivors appear, which drives every early month's default rate down; an expert
counts each taken-over loan only from its first month on book after the take-over (delayed entry), or reads the rates off
the loans the record watched from drawdown, and either way lands the same figure.

## Default path

1. Stage `personal_loan_book_2026-09-30.csv` under CRM-ECL-04 sections 1 and 2: 3,266 loans in stage 2, 343 in stage 3.
2. Read `loan_record_2026-09-30.parquet`: each loan's month on book of first default (default_month), of closing without
   a default (closed_date), or the month it has reached if still open, counted in calendar months from its drawdown month
   (3.2).
3. For each product and month on book m, take the loans open and not in default at the start of m, every loan counted
   from month on book 1, and the shares of them that first default in m and that close in m.
4. PD(k) for a loan at month on book a: the default share at a + k times the shares neither defaulting nor closing in
   each month a + 1 to a + k - 1; the 2.4 scalar on stage 2 (3.2).
5. Apply LGD, the re-amortised balance and monthly discounting at the contract rate over 12 months or the remaining term
   (3.1, 3.3 to 3.5), and the probability-weighted multiplier 1.0555 from the Q1 FY27 sheet (section 4).
6. Sum: AUD 11,551,554.

Ends on: AUD 11.6 million
Golden: AUD 13.2 million

## Stump sentence

A strong solver builds each product's monthly default and repayment rates by month on book from the loan record,
counting every loan from its drawdown, rolls each performing loan forward from its own month on book, and books AUD 11.6
million against AUD 13.2 million (12.3 per cent low); the step that lands it there is counting the 16,479 loans the
record took over at the October 2019 go-live as at risk from their drawdown, when the record holds them only because
they were still open that day, so their earlier months fill every early month's loans at risk with exposure that could
not end in a recorded default.

## Three rules

Task type: expected-credit-loss-provisioning, the banking domain's task type that serves Forecasting & Predictive Modeling: each performing loan's expected loss over its next 12 months or remaining life at 30 September 2026.
Domain test: The deciding quantity is each loan's AASB 9 12-month or lifetime ECL, whose PD term is the product's default probability by month on book estimated from a loan-level performance record with repayment as a competing exit, then staged, scenario-weighted, re-amortised and discounted at the contract rate.
Swap: Written as a maintenance reserve on pump leases from a lease register, the survival estimate survives, but staging on a significant increase in credit risk, the 2.4 scalar, LGD from recoveries, re-amortised EAD and probability-weighted scenarios have nothing to attach to, so the call stops reading the same.
Layer 1: Dates rather than months on book (loan system), the earlier platform's numbering block (take-over), as-at hardship statuses moved by a Tuesday batch and stale COVID-19 rows (hardship workflow), v3 and v4 scores (scorecard migration), a June extract without the score column and counting arrears to its run, runs stamped the next day (batch scheduler), a blank-key sale receipt and reissued agency references (collections ledger); none carries the call.
Layer 2: Estimation that fits the data (estimation_fit): left truncation; a record that took over the earlier platform's open loans watched them only from the go-live, so each taken-over loan enters the loans at risk at its month on book after 30 September 2019, not at drawdown.
Decisive step: Delayed entry in the PD's life table: each loan taken over at the 1 October 2019 go-live counts among the loans at risk only from its first month on book after September 2019, because the earlier platform's loans that defaulted or closed before then never reached the record.
Not semantics: Every field, the record's population sentence and 3.2's estimand read correctly still leave the textbook build counting each loan from drawdown, AUD 11.6 million; the miss is in which months a loan was observed at risk, an estimation choice, not the meaning of any field or code.
Not rule application: CRM-ECL-04 3.2 files what PD(k) is and that it comes from every loan of the product in the record; no filed sentence says how to estimate it, when a loan enters the loans at risk, or anything about the take-over's effect (asserted), so executing every stated rule still files AUD 11.6 million.
Analyst test: A strong analyst who stages the book cleanly, reads CRM-ECL-04 and the record's dictionary entry correctly and builds the textbook PD from monthly default and repayment rates by month on book over every loan in the record, each counted from its drawdown, books AUD 11.6 million against AUD 13.2 million, 12.3 per cent low.
Estimand: CRM-ECL-04 1.1, 3.1 and 3.2 fix the population (loans open at close of business on 30 September 2026 in stages 1 and 2), the outcome (first default in month on book a + k for a loan open and not in default at the end of a, from every loan of the product in the loan record), the window (12 months or the remaining term), the unit (loan, 3.7) and the AUD allowance.
No decoy: Nothing is planted to carry the wrong answer: no memo, draft, briefing, prior allowance, fitted curve or stakeholder figure ships; the record, the book, the register, the scenarios and the policy are all correct, and the distractors are the roll-rate workbook and the write-off file.
No certified replay: No certified, published or prior-quarter allowance or PD ships, so the method cannot be recovered by reproducing a figure; the estimators that respect what the record watched (delayed entry, the taken-over loans left out, landmark shares) agree with each other, not with a filed number.
Lesson: A loan-level record that took over a predecessor's open loans watched them only from the take-over, so a life table built from it must enter each taken-over loan at its age then; no build on file teaches left truncation of a taken-over cohort (nearest drivers 0.10 and below, task255's size truncation and task134's right censoring differentiated).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 risk grade added to the rates, from drawdown | 7.1 says PD is by product and month on book only | risk_grade is a column | the covariate reflex itself | none | no | no | readable |
| R2 repayment censored (default-only survival), from drawdown | 3.2's "open and not in default ... first defaults" | closure_reason column | the textbook Kaplan-Meier reflex | none | no | no | readable |
| R3 each taken-over loan held from its month on book at the go-live (decisive) | no: 3.2 and the dictionary state the record's population, never entry, exposure or the take-over's effect (asserted) | no: no flag, entry or month-on-book column; the taken-over loans are known only by drawdown before the go-live | no: the reflexes (pool, stratify, censor, compete, smooth) all land wrong (R0 to R2b, the audit's crude routes) | no: no control, corpus or published PD scores the risk set | no: keys unique, no duplicates, every join lands; thin early vintages read as a smaller old book | no: rebuilding every month's loans at risk, not one ratio | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "collective expected credit loss allowance" | stages 1 and 2 | stage 3 included | off (and no PD for stage 3) | 1.1: stage 3 is assessed under CRM-ECL-06, outside this method |
| SF2 | "our PL36 and PL60 loans at 30 September 2026" | the September extract, loans open at close of business | the record's Open loans | same call (the same 40,897 loans, asserted) | same call |
| SF3 | "every loan of its product in the loan record" | every loan, the taken-over ones included, each where the record held it | the taken-over loans left out | same call, 13.2 (AUD 13,226,802) | same call |
| SF4 | "open and not in default at the end of month on book a ... first defaults in month on book a + k" | default with repayment as a competing exit | repayment treated as censoring (default-only survival) | 14.1 | 3.2: a loan repaid before a + k never first defaults at a + k |
| SF5 | months on book | calendar months from the drawdown month | counted from the first repayment month | same call, 13.2 | 3.2 pins the drawdown month; same call |
| SF6 | the significant-increase scalar | on PD(k) | on the monthly default rate | 13.1 | 3.2: "Stage 2 loans carry the significant-increase scalar of 2.4 on PD(k)" |
| SF7 | PD's dimensions | product and month on book | grade added | 13.3 | 7.1: "PD is set by product and month on book only" |
| SF8 | "the record's experience is used as it stands" | rates read off the record, no fit | landmark shares read off the loans followed that far | same call, 13.2 | same call |
| SF9 | a loan past contractual maturity | one month remaining | nothing remaining | same call, 13.2 | 3.2; same call |
| SF10 | pause dates | count as repayments fallen due | left out | same call (AUD 13,192,848) | 3.2; same call |
| SF11 | hardship in force at 30 September | 2.2's dates | the status label; the register ignored | label same call; ignored 12.9 | 2.2; 2.1 names the condition |
| SF12 | v3 origination scores | converted to v4 | read as v4 | 13.1 | 2.3 |
| SF13 | scenario weighting | probability-weighted multiplier 1.0555 | base only; the prior quarter's sheet | 12.5; 13.0 | section 4: the quarter's approved workbook, probability-weighted |
| SF14 | EAD(k) | re-amortised current balance | balance held flat | 15.3 | 3.4 |
| SF15 | DF(k) | monthly at the contract rate | none | 14.4 | 3.5 |
| SF16 | rounding path | loan totals, rounded when reported | stage amounts rounded first | same call (10.6 + 2.6 = 13.2) | 3.7; same call |
| SF17 | the record's default | first month end at 90 or more days past due | the day 90 was reached | not computable from the record | the record's field definition (1.2) |
| SF18 | the record's window | events to 30 September 2026 | events to an earlier cut | not offered by the files | the record's population note |
| SF19 | "the loans that defaulted in 2023-24" | the Collections MI file, July 2023 to June 2024 | calendar 2023 and 2024 | not offered by the files | the file's own population and name |
| SF20 | "by product and quarter" | quarter of the default month within 2023-24 | quarter of resolution | off on all 8 | the MI file's default month; the prompt ties the ask to the defaults |
| SF21 | "actually lost as a share of their balance at default" | 3.3's measure: receipts and the sale share, monthly discounting to the default month end | undiscounted; by days; from the month start; at the annual rate | off on 6 to 8 | 3.3 and 3.5 |
| SF22 | a case Collections closed as cured that the loan record shows written off or settled | measured on what it recovered: the 59 cured on arrangements withdrawn before they started, every one written off | every cure at its word (the judge's round 2 build); every withdrawn cure doubted | off on all 8; off on 7 of 8 | 3.3: "a loan the loan record shows written off or settled for less did not return to performing, whatever resolution Collections recorded, and is measured on what it recovered"; the record and the register select the same 59 (C1) and every other cure is repaid in full or open (asserted) |
| SF23 | "every amount received" on a loan | each remittance on the account placed under the reference it quotes that day | the receipts file's posted loan (the judge's round 2 build); the reference's latest placement; reissued references dropped | off on all 8 each | the dictionary: the loan number is the one "the receipt was posted to; an agency remittance is posted on the Wirraway reference its narrative quotes", and the Agency Ref is "Wirraway's reference for the account while it is placed"; each of the 20,902 remittances falls inside exactly one placement of its reference, none on a first or last day, and each of the 2,034 posted elsewhere arrives outside the posted account's own placement (asserted) |
| SF24 | the sale proceeds | each sold account's face value at the cut-off times 3.85 cents | the receipt spread over the written-off cases | off on all 8 | 3.3 counts the proceeds of the debt's sale; the schedule prices each account |
| SF25 | stage at 30 June | section 2 with days past due at close of business on 30 June | the June extract's days past due as they stand (the judge's round 2 build) | 14 of 16 counts move | 1.3 and the dictionary's loan book lines: the June extract's days_past_due "counted to the run date, 1 July 2026", the September extract's "counted to the reporting date, 30 September 2026"; executed literally (each June value put back by the day between) all 16 counts are the golden, read unadjusted 14 move (both asserted, the clock parsed from the dictionary by the verifier); the record dates the default of the 6 loans at 90 days to July and the 15 at 180 had not been written off by 1.4's June batch |
| SF26 | the June behaviour score | the month-end run on the 30 June position, made 1 July | the run made before 30 June | 16 of 16 move | 2.1 at the reporting date; the runs file names the month ends it scores and dates each run by the day it was made |
| SF27 | "the number closed" | June loans absent from the September extract | the record's Closed status in the quarter | same call (3,317, asserted) | the dictionary: a loan leaves the extract once it closes |
| SF28 | hardship in force at 30 June | 2.2's dates | the September status label | 16 of 16 move | 2.2 |
| SF29 | "as a share of their balance at default" by product and quarter | the quarter's balance not recovered, summed over its defaults, over their total balance at default | the mean of each loan's own share | off on all 8 (nearest 0.58 points) | 3.3: "summed over the quarter's defaults, as a share of their total balance at default" |
| SF30 | the LGD the allowance uses | 70 and 76 per cent | the 2023-24 losses the review is setting them against (PL36 68.9, PL60 75.1 per cent) | 13.0 | 3.3: "the rates in force until the Audit and Risk Committee approves a change"; the prompt's "will be set" |
| SF31 | a cancelled arrangement, and the end date, at 30 June | in force to its end date, both days included, until the day it is cancelled (57 cancelled after 30 June were in force) | every cancelled arrangement out whenever cancelled; the cancellation ignored; the end date excluded | 14, 8 and 6 of 16 move | 2.2: "one that is cancelled stops being in force on the day it is cancelled"; the dictionary: the end date is "the last day of the varied repayments"; no cancellation falls on 30 June (C1) |
| SF32 | "60 or more points below" on the June scores | 60 or more on whole points: every score whole, every v3 score converted and rounded to the nearest point, none within 0.02 of a half (82 June loans fall exactly 60) | more than 60 | 12 of 16 move | 2.1's "60 or more"; the migration note: "rounded to the nearest whole point" |
| SF33 | stage 3 and written-off loans at 30 September | stage 3: in the September extract at 90 or more days past due; written off: closed | written off counted as stage 3 (6 loans of the four groups) | 4 of 16 move | the dictionary: "a closed loan is in no stage"; 1.4: a loan written off is closed |

## Ladder

Measured by `checks.py` and `verify.py` on the shipped pack (allowance, AUD; reported to AUD 0.1 million):

| Rung | Construction | Allowance | Reported | vs answer |
|---|---|---|---|---|
| R0 (default path) | life table by product and month on book, every loan from its drawdown, repayment competing | 11,551,554 | 11.6 | -12.35% |
| R1 | the covariate reflex: rates by product, grade and month on book, from drawdown | 11,653,209 | 11.7 | -11.58% |
| R2 | the textbook survival curve: repayment censored, from drawdown | 12,243,098 | 12.2 | -7.10% |
| R3 (decisive) | each taken-over loan held from its month on book at the go-live | 13,178,713 | 13.2 | answer |
| R2b | repayment censored, held from the take-over (over-correction) | 14,073,342 | 14.1 | +6.79% |

- Every correction walks up and only the over-correction overshoots; the decisive move is the largest (+14.1 per cent
  over the default path). R0 misses the allowance and both stage amounts; R1 and R2 miss the allowance and stage 1 and
  land stage 2's bin (2.64 and 2.57 against 2.59) by offsetting errors, priced in the pair simulation.
- The audit's routes on the record (a crude cumulative default share and its conditional readings) all land off:
  resolved loans over 1 - C(a) 14.8, over the share still open 17.1, plain increments 14.3; every loan over 1 - C(a)
  8.6, over the share still open 9.2; read from month on book 0 24.8; repayment counted again on EAD, on top of the
  competing exit, 12.4 (-5.92 per cent).
- C4 cells, each off the bin and ruled out by a quoted sentence: grade held from the take-over 13.3 (7.1), the scalar on
  the default rate 13.1 (3.2), v3 read as v4 13.1 (2.3), hardship ignored 12.9 (2.1, 2.2), base scenario only 12.5
  (section 4), EAD flat 15.3 (3.4), no discounting 14.4 (3.5).
- C3 corridor: the answer and every convergent estimator sit inside AUD 13.15 to 13.25 million (13,174,979 to
  13,226,802: taken-over loans left out, landmark shares, the first-repayment clock, past-maturity nil, the status label).
  The answer sits 0.29 of a bin from its lower edge, stage 1 0.34, stage 2 0.45 (asserted at 0.2 or more).
- R3a and R3b (three-rules block): the easy route with every filed rule executed files AUD 11.6 million on the answer's
  stages and multiplier; changing only the entry of the taken-over loans files the answer to the cent.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | allowance: loans open at close of business 30 September 2026 in stages 1 and 2; PD: every loan of the product in the record | 1.1, 3.2 filed; C1: taken-over loans in or out land the same bin (SF3) |
| 2 Unit of account | the loan | 3.7: ECL per loan, the allowance their total |
| 3 Attribution window | forward months k from October 2026 | 3.1, 3.2; the record's events dated at month ends and closing dates |
| 4 As-of dating | close of business 30 September 2026 | 1.3 and the extract and record headers |
| 5 Version basis | CRM-ECL-04 v4.2, the Q1 FY27 scenario sheet | the document control; the sheet name; the prior quarter's sheet lands 13.0 (SF13) |
| 6 Denominator | PD: loans open and not in default at the start of each month on book, each where the record held it | 3.2 files the estimand; the method is forced by the record's structure and every valid estimator converges (C3); the stump lives here as HOW |
| 7 Weighting | 55 / 30 / 15 per cent on the scenario multipliers | section 4 and the approved sheet |
| 8 Window length | the record's whole history | 3.2 "every loan of its product in the record"; C1 across own-only and landmark |
| 9 Boundary inclusivity | 30, 90 and 60-point thresholds inclusive; arrangement dates inclusive | 2.1, 1.2, 2.2; C1: no arrangement ends or is cancelled on 30 September (asserted) |
| 10 Rounding path | loan level, rounded when reported, AUD million one decimal | 3.7 and the prompt; stage amounts add (asserted) |
| 11 Tie-break | none (one figure) | not applicable, asserted single answer |
| 12 Maturity and censoring | open loans followed to September 2026; taken-over loans entered at the go-live; past-maturity loans one month | 3.2; the record's population; C3 |
| 13 Order of operations | scalar on PD(k), then the multiplier (both multiply PD) | 3.2, section 4; the scalar on the rate is SF6 (13.1) |
| 14 Row order | sums | C1, order-free |
| 15 Duplicate resolution | one row per loan in every extract | asserted unique keys |
| 16 Identity normalisation | loan numbers join book, record and register | asserted; the earlier platform's lower block joins as it stands |
| 17 Netting against gross | per-loan ECL, no netting | 3.7 |
| 18 Dimensional units | AUD; annual rates divided by 12 | 3.4, 3.5 |
| 19 Code and status semantics | hardship status against dates; v3 against v4; closure reasons | 2.2, 2.3, the record's field definitions; never the stump |
| 20 Integerisation | repayments fallen due counted on the business-day schedule | 3.2 and the dictionary's repayment day rule |
| 21 Clause scope | 7.1 applies to PD; 3.2's estimand per product | 7.1, 3.2 |
| 22 Forward window contents | PD from the record's experience, multipliers on PD, EAD on schedule | 3.2, section 4, 7.4 |

## Literal reader

A reader executing CRM-ECL-04 3.2 word for word estimates, per product and month on book, the probability that a loan
open and not in default at the end of a first defaults at a + k, from every loan of the product in the loan record; the
record files its own population as every loan the loan system has held since it went live on 1 October 2019, when it took
over the earlier platform's book, so the earlier platform's loans in it are there because they were open at the go-live,
and a literal estimate cannot treat their months before the go-live as months watched; every literal method that keeps to
what the record holds (delayed entry, the taken-over loans left out, landmark shares) files AUD 13.2 million (C3,
asserted), and the default path is an easy method on the same estimand, never another reading of it. The ask readings
are closed in SF19 to SF33, each by a quoted sentence the lender files (3.3's measure, its cure and its rates in force;
2.1 to 2.3; the dictionary's field descriptions, its change log and its closed loans) or by records that converge. The
judge's round 2 builds are reproduced to the figure in `checks.py` (60.5 to 74.7; 14,450 to 113) and part from the
golden only at the cure, the remittance attribution and the June clock, each now ruled on by one filed sentence; the
literal execution of the repaired text gives all eight loss shares and all sixteen counts on the verifier's own code.

## Oracles

- The write-offs extract (distractor): monthly write-offs and recoveries, totals invariant under either attribution of
  agency remittances (D9, asserted); it states no PD, loss rate or allowance.
- The roll-rate workbook (distractor): FY26 arrears roll rates by count; no PD by month on book, no allowance.
- The scenario workbook's prior-quarter sheet: last quarter's multipliers (1.04 weighted), off the bin (13.0) and ruled
  out by section 4's "the quarter's approved scenario workbook".
- The sale schedule's header: face value times 3.85 cents equals the consideration and the blank-key receipt to the
  cent under every reading of ask A.
- The receipts total: the same under either attribution.
- None ties only under the golden; no document states a graded figure (asserted).

## Ask sheet

Both asks are decoupled from the call: neither reads the PD (asserted by running both with the PD code disabled), and
the main call reads none of the June extract, the scoring runs, the Collections files, the sale schedule or the
placement report (deleting them leaves the allowance identical, asserted). Zero device and hazard rows sit in the main
call's population: none of the 72 withdrawn collections arrangements and none of the 1,334 bulk COVID-19 rows is in force
at 30 September or 30 June or sits on a loan in either book; the 1,827 June loans whose arrears the extract counts to its
run sit in a file the call never reads; the reissued references sit in the receipts ledger and the placement report,
which the call never reads.

**Ask A, realised loss of the 2023-24 defaults by product and quarter (8 figures, per cent to one decimal, workbook)**

- Answer: PL36 67.9, 65.8, 70.7, 70.9; PL60 70.2, 77.4, 73.2, 79.3 (July to September 2023 through April to June 2024).
- Named use and H18 home: the LGDs in 3.3 (70 and 76 per cent) are reviewed against what the defaults have lost; the
  audit trail of the LGD input the call consumes.
- Primary device A2, silent (D7, codes reissued to other entities): Wirraway reissues the reference of a placement it
  closed at least 90 days earlier to some new placements from its November 2024 platform move, the most recently freed
  first, and Bellbird's receipts loader posts a remittance to the first placement on file with the reference it quotes:
  639 references carried twice or more, 2,034 remittances posted to another account, 719 of them on accounts sold to
  Tarwin in March 2026, after the sale. The posted read credits 2023-24 loans with later accounts' remittances. The
  dictionary says what the two fields hold, the way the ledger and the agency document them: the receipts file's loan
  number is the one the receipt was posted to, an agency remittance posted on the reference it quotes; the Agency Ref is
  Wirraway's reference for the account while it is placed. Nothing says a reference is reissued or how the posting picks
  a placement; the reuse shows only in the placement report's rows.
- Hazard A1, filed (round 2 repair; D2, a stored label taken before a silent switch): Collections closes a default case
  as cured when it approves a collections arrangement, dated from its start, and does not reopen it when the arrangement
  is withdrawn: 72 withdrawn, 59 on loans the record shows written off (some sold in March 2026), 13 that caught up. 3.3
  now files that a loan the record shows written off or settled is measured on what it recovered, whatever Collections
  recorded, so every careful path executes it; taking every label at its word, as the judge's round 2 build did, zeroes
  the 59 and misses all eight.
- Why A2 survives the battery: keys unique, no duplicate rows, every receipt joins the record and the defaults, the
  receipts and write-off totals tie under every attribution. The inconsistency exists only across files, at a cut nothing
  in the battery makes: a remittance whose posted account's placement had closed, or been recalled for the sale, while
  the placement report shows its reference on another account that day.
- Resolution, unique: 3.3's cure sentence on the record (the 59, the same set the register gives, C1); each remittance to
  the account placed under its reference on the day it was received (exactly one per remittance, none on a first or last
  day, asserted).
- Hazards crossed: A1 (filed), the sale receipt with no loan number (shared by face value), the dishonour reversals
  (texture), the discount clock (3.3, 3.5), the pooled share (3.3, SF29).
- File path (7 files on the golden's path, the register an eighth that reaches the same cure set):
  collections_defaults_2023-24.csv, collections_receipts_2023-07_2026-09.csv, debt_sale_2026-03_schedule.xlsx,
  wirraway_placements_2026-09-30.csv, loan_record_2026-09-30.parquet (closure reasons), CRM-ECL-04 (3.3, 3.5),
  ecl_extract_dictionary.txt (loan_no, Agency Ref); hardship_register_2026-09-30.xlsx (the withdrawn arrangements, C1).
- Columns (17 on the golden's path): loan_no, product, contract_rate, default_month, balance_at_default, resolution;
  received_date, amount_aud, source, narrative; face_value_aud and the Price line; Agency Ref, Client Ref, Placed, Closed;
  closure_reason.
- Stops (nearest figure to the answer, every figure off at one decimal, asserted): the judge's round 2 build (cures at
  their word, remittances as posted) 2.50; A1 executed, as posted 0.55 (the cracker's and the mirror's path); A2
  cracked, cures at their word 1.96; over-cleaner (every withdrawn cure doubted), as posted 0.36; the reference's
  latest placement 0.87; reissued references dropped 0.87; latest placement with cures at their word 0.61; the sale
  left out 1.10; the sale spread 4.39; not discounted 2.77; every cure on its receipts 8.00; the mean of loan shares
  0.58. Composed (cure rule by sale by discounting by attribution, 319 paths): at most 1 of 8
  with one, two or three mishandlings: the over-cleaner that also cracks A2 hits PL60 April to June (no caught-up case
  there was withdrawn), with the annual rate as well PL60 July to September, and the sale left out with no discounting
  and the latest placement PL60 January to March.
- Realism: an approved arrangement closing a case is how collections MI records a cure; agencies reissue account
  references and a lookup on the first match is an ordinary loader's behaviour; the placement report is the agency's
  standard client export; a run folder's dictionary says what each field holds and where a ledger's postings come from.

**Ask B, where the loans in stage 1 and stage 2 at 30 June stand at 30 September (16 counts, deck slide 2)**

- Answer (stage 1, stage 2, stage 3, closed at 30 September): PL36 stage 1 at June 14,470, 680, 42, 1,586; PL36 stage 2
  468, 658, 115, 123; PL60 stage 1 17,724, 831, 46, 1,180; PL60 stage 2 560, 942, 140, 112.
- Named use and H18 home: the Audit and Risk Committee sees the quarter's deterioration and cures behind the stage 2 amount it signs; the
  audit trail of the staging the call consumes.
- Primary device B4 (round 2c, a scoring-run partition carried forward): Behaviour Scoring's run for the June month end,
  made 1 July, could not score one partition of the engine's book (loan numbers whose last digit before the check digit
  is 3 or 4) and wrote each of those loans its last score, marked Carried forward: the May month-end score, or the
  application score on v4 for a loan first due in June. The partition was run again on 2 July, so the file holds a
  Scored row for every loan of the June month end and, for the partition, a carried-forward row dated 1 July beside it.
  The careful path takes the run dated 1 July for the June month end (B2's own logic), every join lands and every
  score is a plausible number: read as it stands, 16 of the 16 counts move; its Scored rows alone (the partition left
  unscored, as the loans before their first repayment are), 16 of 16. Resolved from the scoring file alone: its
  `score_status` description says what a Carried forward score is, and its `runs` and `run_date` say the file holds
  month-end runs dated by the day they were made, so the 2 July rows can only be the June month end's. Each loan's
  latest June month-end row gives the golden too (C1). No filed rule on the path: neither the dictionary nor the
  policy mentions the rerun (asserted).
- B3, filed since round 2b (D8 spent): the dictionary records the June extract's days_past_due as counted to its run
  date, 1 July, and the September extract's as counted to the reporting date; staging at 30 June under 1.3 puts each
  June value in arrears back a day. Read unadjusted, 14 of the 16 counts move; now a hazard the careful path crosses.
- In-world evidence, consistent with the filed source: 0 of the 1,827 June values sit on a due date counted back from
  30 June and every one from 1 July; the 15 loans at 180 days were at 179 when the June batch ran (1.4); the loan record
  dates the default of each of the 6 loans the extract shows at 90 days to the July month end (at close of business on
  30 June they were at 89, in stage 2, inside the four groups), and of every loan above 90 to June or before.
- Hazards crossed: B1 the status label and the cancellations (2.2, restated: a cancelled arrangement stops on the day it
  is cancelled), B2 the run dated 1 July for the June month end, 2.2's end date, the 60-point fall on whole points
  (SF32), written-off loans closed rather than in stage 3 (SF33), the September status lag (2 counts).
- File path (8 files): personal_loan_book_2026-06-30.csv, personal_loan_book_2026-09-30.csv,
  behaviour_score_runs_2026-03_2026-08.parquet, hardship_register_2026-09-30.xlsx, scorecard_v4_migration_note.pdf,
  loan_record_2026-09-30.parquet (default months), CRM-ECL-04 (1.3, 1.4, 2.1 to 2.3), ecl_extract_dictionary.txt.
- Columns (15): loan_no, product, days_past_due, first_repayment_date, origination_score, origination_scorecard at both
  dates; run_date, score_v4, score_status; arrangement_start, arrangement_end, cancelled_date, arrangement_status; current_score_v4;
  default_month.
- Stops (counts moved of 16, every pair distinct, asserted): the judge's round 2 build (as extracted, the 1 July run,
  2.2's dates) 14; labels and the May run 16; dates without any cancelled and the May run 16; dates and the May run 16;
  dates without any cancelled and the June run 11; cancellation ignored 14; September scores for June 16; the July run
  16; the end date excluded 14. Every composed path moves at least 6. With the June clock read from the change log:
  every cancelled arrangement out 14, the cancellation ignored 8, the end date excluded 6, more than 60 points 12,
  written off as stage 3 4. Round 2c, the clock executed: the run dated 1 July as it stands 16, its Scored rows only 16,
  as it stands with the June column unadjusted 16; every composed path, the B4 readings included, moves at least 6.

**Necessity matrix** (one device mishandled, everything else right): A2 8 of 8, A1 (filed) 8 of 8, the sale left out 8,
not discounted 8, every cure on its receipts 8, the sale spread 8, the mean of loan shares 8; B4 the run dated 1 July as it stands 16 of 16, its Scored rows only 16; B3 (filed since round 2b) 14 of 16, B1 the label
16, B1 every cancelled out 14, B2 the May run 16, more than 60 points 12, the end date excluded 6, written off as stage
3 4.

**Hazard table.** Sale receipt (A, 8 figures, 1.1 to 1.6 points); discounting (A, 8, 2.8 to 5.5); dishonours (A, none:
texture); B1 label (B, 16); B2 run date (B, 16); the September status lag (B, 2 counts).

**Referee.** The sale schedule's consideration, AUD 1,800,666.58: face value times 3.85 cents and the blank receipt to the
cent, under every handling of A1 and A2.

| Ask | The cracker's path (lands the call, runs the battery, executes every filed rule it points at) | Figures kept | Verdict |
|---|---|---|---|
| A, 8 realised losses | 3.3 as filed (pooled, the cure sentence on the record, the sale by face value, monthly discounting); remittances as the receipts file posts them, every join landing | 0 of 8 (nearest 0.55 points) | miss |
| B, 16 migration counts | the run dated 1 July for the June month end as it stands (B4), 2.2's dates, 60 or more on whole points, closed loans in no stage; June days past due put back to 30 June by the dictionary's run clock | 0 of 16 | miss |

Mirror leakage: 0.0 per cent of the ask weight (the mirror takes the same ask paths and keeps none of the 24).

Pair ceiling: 28.5 (planning weights 38 / 7 / 55, r = 5; cracker 45.0, 0 of 24, mirror 12.0, 0 of 24; asserted in
`checks.py`). With the mirror on R1 or R2 also keeping stage 2's component, 31.0; both top responses on the call, each
executing the June clock, 45.0. The most obvious device is A2 (the dictionary's loan_no entry names the posting rule),
and the cracker cracking it puts the pair at 37.7 (asserted at or under 40). Residuals: the cracker cracking B4 instead
46.8, both A2 and B4 56.0; both top responses cracking A2 63.3, B4 81.7. B4 is the quieter of the two: every join of the
battery lands on the run dated 1 July and its scores are ordinary numbers, and only the file's own status column and its
seventh run date show the partition. The habitual sheet 28.5.

**Span floor.** Ask B 8 files; ask A 7 on the golden's path since the cure is read off the record (3.3), the register an
eighth route to the same 59.

**Guard lines.** Round 2c clears the two BLOCKs heart read at round 2b: ban.forum board_of_directors against task119
(forum redrawn to committee_or_panel, which guard.py check passes now that task129 is outside the three builds drawn
before this one) and people.first Vanessa against task108 (Declan Wallace drawn with guard.py names, seed 133). Heart is
WARN, no BLOCK. Earlier (heart WARN, no BLOCK): people.last Olson (task181) and people.first Vanessa (task108), Christine
(task104): older builds only, names drawn by guard.py. repeat.gate_g forecasting against task132: both in the
Forecasting block, mechanisms differ (renewal against left truncation). repeat.deliverables pptx and xlsx against
task129: the deliverables are the slot's since v1. Driver nearest 0.10 (this slot's loop 1), 0.06 task501 v3 and task23;
same_driver_older against task180 differentiated on the card.

## Leak review and stage 3 gates

- Round 2c (2026-10-14): `checks.py` PASS 600 (SF34 and B4's readings, the pair sheet asserted), `verify.py` PASS,
  two rebuilds byte-identical to `target/`, `target.zip` and `golden/`, `figures_check.py` exit 0 (65 figures), `precut.py`
  49 PASS, voice-check PASS (874 characters), `leak.py --asof 2026-10-12` REVIEW no LEAK, guard validate 169 valid,
  surface 1 promoted (task180, unchanged), heart WARN no BLOCK, freeze check --mode rubric PASS (--mode determinism names only the deck's renamed
  heading, board_ecl to arc_ecl, every figure unchanged).
  Documents changed under `target/`: the scoring runs parquet, the CRM-ECL-04 docx and the hardship register (metadata).

- Round 2b (2026-10-14, after the re-judge's fix): `checks.py` PASS 581, `verify.py` PASS (the June clock parsed from
  the dictionary), two rebuilds byte-identical to `target/`, `target.zip` and `golden/`, `figures_check.py` exit 0,
  `precut.py` 49 PASS, voice-check PASS, `leak.py --asof 2026-10-12` REVIEW no LEAK (the same lines as below), freeze
  check --mode determinism PASS, guard validate 169 valid, surface as below, heart BLOCK pre-existing (Guard lines).
  Documents changed under `target/`: `ecl_extract_dictionary.txt` and the CRM-ECL-04 docx.

- `leak.py task133 --asof 2026-10-12` (rerun after the round 2 asks repair): REVIEW, no LEAK. Each line:
  - 7.1 in CRM-ECL-04: the limitations clause number, which the write-up cites, not a figure.
  - 560 and 680 in the migration note: v3 scores in its conversion table, not the counts they coincide with.
  - CRM-ECL-04 carries 9 of 10 words of the call: its scope sentence (1.1) names the allowance it governs, with no figure.
  - stump-term overlap, CRM-ECL-04 6 of 25 (record, repayment, status, months, points, arrangement) and the dictionary 10
    of 25 (record, drawdown, repayment, status, months, earlier, agency, among them): the subject's own words. The
    repair's new dictionary lines say what two fields hold and where the extract is read from; none names the reissue,
    the posting rule or a recount (asserted in `residue_and_pins`). The dictionary's
    "earlier platform" and "took over" are the loan record's population sentence, the filed WHAT the literal reader
    needs; neither document says anything about entry, exposure, truncation, the loans at risk or how to count a
    taken-over loan (asserted in `forks`).
  - dates after the setting: arrangement end dates and approved starts in the register; first repayment dates of loans
    drawn in September in the book and the record.
- `guard.py surface task133`: 1 pair promoted, task180 (surface 0.078, corpus percentile 52), on the card-level
  same-driver signature (gap population, pattern G12, Gate G forecasting), not on wording, file names, schema or
  personas; differentiated on the card (task180 restores events a detector masked, so its record misses events that
  happened; here every default after the take-over is recorded and what the record lacks is the taken-over loans'
  earlier months). Left for the author's `/clone-check`. The only persona the cut pack names is Stephanie Manning.
- `guard.py validate`: 169 cards valid. `guard.py heart task133`: WARN, no BLOCK (lines in the Ask sheet's tail).
- `golden-realism`: the round 2 repair rewrote two notes on the workbook's Method sheet to the filed wording (the June
  clock, closed loans in no stage, the pooled share, the cure and the attribution); no figure moved, the container
  audit is clean. Named sheets, findings as titles, precision by quantity (AUD million, whole loans, the
  multiplier to two decimals, balances to the cent, losses to one decimal), source lines from the fiction, the rounding
  convention and the method on a notes sheet; the deck's titles are findings with a source strip and slide numbers.
- `reduce-house-fixes`: H1 container audit clean on `target/` and `golden/`; H4 the zip holds the 15 files flat; H6 the
  golden's attribution rule holds for every remittance (one placement each) and its cure rule for every case (asserted);
  H7 two rebuilds byte-identical to the shipped `target/`, `target.zip` and `golden/`; H8 every clause cited resolves;
  H9 every shipped file named in the run folder's dictionary and in `metadata.json` (asserted); H11 one write-up and one
  prompt; H16 no record dated after its extract; H24 the constructed-pack statement sits only in `metadata.json`.

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
- Round 1 shipped design: weak per the 10/10 audit, because its decisive step (dividing a crude cohort curve's increments by the share of the cohort neither defaulted nor repaid, read from the development sample) sat one rung above the step the v1 portal winner had already solved, and the sample's prepaid outcome column beside a curve header saying "share of every loan drawn" pointed straight at it; round 2 ships no curve and no sample and moves the decisive step to where a taken-over loan's exposure starts.
- The audit's suggestion, a crude curve rebuilt by Aalen-Johansen from right-censored recent vintages: an estimator under censoring with competing exits is task134 v1's driver, whose default construction landed; censoring and the competing repayment exit are this build's default path instead, and the decisive move is left truncation.
- EAD at default (re-amortised against the balance at default) as the decisive step: 3.4 files EAD, so the step would be rule application.
- A cure followed by a re-default as the PD's decisive step: the cure clause either blesses the wrong answer or announces the check (already rejected for ask A at 6b).
- Hazard against landmark estimation as the stump: both are valid on the record and land the same bin, so the choice between them is no stump; both sit in the corridor.
- LGD development (recoveries not yet complete) as the main call's step: 3.3 files the LGDs, so the call estimates none.
- Scenario weighting as the step (the weighted multiplier against weighting scenario ECLs): linear in PD, identical; no stump.
- The allowance at the nearest AUD thousand: the estimators that respect what the record watched (taken-over loans left out, landmark shares, the first-repayment clock) sit 0.1 to 0.4 per cent apart and split the thousand-dollar bins; reported in AUD million to one decimal they all file 13.2 (C3).
- Stage amounts at two decimals of a million: leaving the taken-over loans out moves stage 2 from 2.59 to 2.62; one decimal keeps the corridor, and R1 and R2 then land stage 2's bin by offsetting errors (accepted and priced: the call and stage 1 miss on both).
- The earlier platform's loans numbered as a separate go-live block: a marker column in all but name; they keep their own BPL numbers, below the loan system's range.
- The first-repayment clock at -2.9 per cent: an artefact of reading rates on one clock and positions on the other; on one clock throughout it lands the answer's bin (13.2), so SF5 converges.
- Withdrawn-arrangement cures drawn at one rate for every 2023-24 case (6 or 12 per cent): the over-cleaner hit 6 or 7 cells; drawn by how each case ended (55 per cent of the caught-up, 9 per cent of the written off and settled) it misses every cell unless it also cracks A2, then 1 (PL60 April to June, where no caught-up case was withdrawn).
- A2 with references reissued from the go-live, at random or oldest first: new 2023-24 placements took references first held by 2019 to 2022 write-offs, so the posted read raised losses 1 to 4 points while A1 lowered them, the two composed to within 0.1 point of the answer in two cells, and the reference's latest holder reproduced the answer in seven cells; reissued from the agency's November 2024 platform move, the most recently freed first, the posted read sits below the answer in every cell and the latest holder above it.
- A second silent device for ask B (a superseded re-run of the June scoring run; an origination scorecard label corrected between the June and September extracts; paused loans left out of the June extract): the first two need a filed rule to adjudicate them, the third loses the truth; B3 stays the one silent primary, with the loan record's default month added as its in-world evidence, and the pair is priced with A1 as the most obvious device and B3 as the residual risk (49.1).
- The change log naming the June arrears clock (the audit's suggested WHAT for B3): a filed sentence on the ask's path is executed by the cracker; 1.3 files the WHAT (close of business) and three records show the June column counts to the run, so the device stays unnarrated.
- A1 as a silent device (round 2 judge): the judge took every Collections cure at its word (with the posted remittances, 60.5 to 74.7) and found the cure's treatment unfiled; 3.3 now files that a loan the loan record shows written off or settled is measured on what it recovered, so A1 is a filed rule every careful path executes. No replacement drawn: the cracker sheet already had the cracker resolving it, so the pair sheet does not move.
- The receipts file's loan number described only as a loan number (round 2 judge): the judge read the posting as the attribution and the placement report as a distractor; the dictionary now says what both fields hold (the loan number the receipt was posted to, an agency remittance posted on the reference it quotes; Wirraway's reference for the account while it is placed). Describing the reissue or the first-match posting as well was not built: it would announce the device.
- The June clock left out of the change log (round 2 judge): the judge read the June column as close of business and the 6 loans at 90 days with July defaults as a defect; CHG-26-0418 now records the move from the live system at the run to the quarter-end day's end-of-day snapshot, the job's source and nothing about days past due (the line above still holds against a sentence naming the clock; the judge showed the clock needs its source filed to be literal). Not taken: dropping the clock (ask B would carry no device), removing the loans at 89 and 179 days at the June close (the clock would stay with nothing filed to resolve it), a run log or a position-date column (a new file, or a load stamp marking the June file).
- Moving the 82 June loans that fall exactly 60 points off the threshold (round 2 judge): a gap at exactly 60 on whole-point scores would itself be a tell; 2.1 says 60 or more and the migration note rounds the converted score to a whole point, so the boundary is literal (SF32).
- A second device on ask B that a literal reader could resolve (round 2 repair): ask B classifies filed fields and every condition is pinned (1.3, 2.1 to 2.3, the runs file's dates, the register's dates); a backdated hardship approval, a superseded scoring run and a silently partial June extract each need a filed rule or lose the truth. Not built; the risk is priced on the pair line.
- The June clock left silent behind the change log's source (round 2 re-judge, FIX_NOW on slide 2 only): the judge's literal build read the June column unadjusted (PL36 stage 1 14,450 / 680 / 39 / 1,582) and no file said the June days past due count to the run date. Applied as prescribed: the dictionary's loan book lines record each extract's run clock, and B3 dies as a device (pair 65.2 with both careful, 49.1 cracker only). Not taken: restating the June column at close of business (the re-judge's alternative), which leaves ask B a plain read; re-keying slide 2 to the literal counts, which the re-judge ruled out and freeze.py holds.
- Ask B left device-less after the June clock was filed (round 2b, not shipped): the pair sat at 65.2 with both careful responses executing the clock. Round 2c draws B4 from the scoring engine's own failure mode (a partition carried forward on 1 July, rescored on 2 July), one digit of the loan number at first: single digits moved 10 to 16 counts on the run as it stands and 4 to 16 on its Scored rows alone, no digit both at 16; digits 3 and 4 together move all 16 both ways. Not taken: a status column alone without the rerun rows (loses the June-position score), a split run with no carried-forward rows (the battery's coverage check finds the missing loans), a Sept-side closed-or-stage-3 device (contradicts the dictionary's population sentences).
