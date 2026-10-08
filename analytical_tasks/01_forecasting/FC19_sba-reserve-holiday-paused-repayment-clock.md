# FC19 — The year-end loss reserve for the 2019–21 government-guaranteed small-business loans, when a payment holiday paused some loans' clocks

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · small-business lending and loss reserving |
| Mirrors | Lifetime-loss reserves on loan books whose seasoning clock stopped during payment holidays (CECL reserves at banks after disaster and pandemic deferrals, merchant-lending books at Amazon, Shopify and Square after repayment pauses, card and buy-now-pay-later portfolios with forbearance programmes) |
| Decision shape | One figure committed at a date: the year-end reserve booked for the FY2019–21 vintages |
| Committed call | Remaining lifetime expected charge-offs on the unguaranteed balances of the bank's active FY2019–21 7(a) loans at year-end, in $ millions to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · Pattern B, the reserve method recovered from audited close-outs, whose one unwritten component is a per-loan repayment clock built from the deferral ledger, with two flawless grains (loans and dollars) below it |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #3 stops at a close but inexact match · #8 papers over a failed reproduction · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the bank's audited reserves at the last three year-ends, by approval vintage and term class (48 cells), each with the data snapshot it was computed from |
| Driving force | The reserve's curves are competing-risk incidences of charge-off and payoff by loan age, and the audited close-outs reproduce to the dollar only when age runs on a repayment clock that stops while a loan is in a payment holiday. After the 2021 floods the bank granted 1,140 borrowers holidays of six, nine or twelve months, and a loan in a holiday can neither default nor prepay. Calendar age makes those loans look older than they are, and older loans have passed most of their risk. The months come only from the servicing deferral ledger, joined loan by loan, and they enter the estimation as well as the projection. |

## 1. Situation

A community bank holds the unguaranteed portions of its SBA 7(a) loans and books a lifetime loss reserve on them at each year-end. The
reserving memo files the estimator: competing-risk cumulative incidence of charge-off, with payoff as the competing event, by term class
(ten years or less, longer), conditional on each loan's survival to the reserve date and estimated on the bank's own loans approved since
FY2010. The analyst who built the method has left, and the model-risk standard admits a year-end method only if, run on each prior
close-out's snapshot, it reproduces every audited reserve cell to the dollar. This year-end the reserve for the FY2019–21 vintages,
2,860 active loans with $342 million unguaranteed, has to be booked.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the loan ledger, the charge-off and payoff dates, the guarantee shares, the deferral ledger and
  the audited close-outs. No one's claim about their own numbers is overturned. The difficulty is the clock the incidence curves run on,
  which no document states.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the regulator's ratio. The dollar-weighted incidence on calendar age still reproduces 34
  of 48 cells and still books $15.3 million.
* **Instrument repair.** No file is suspect: every loan's events, balances and guarantees are recorded, and the deferral ledger holds every
  holiday month. On perfect records rungs 0–2 still return $28.8M, $21.5M and $15.3M, because calendar age is a correct count of months
  since disbursement, not of months at risk.
* **Lens swap.** The naive read and the answer differ in moment: the same loans placed on their hazard curves by months since
  disbursement against months actually spent repaying.

## 3. The driving force

A strong solver rejects charge-offs to date, treats payoff as a competing risk, and weights incidence by unguaranteed dollars because
the memo reserves dollars and small loans default far more often. That build reproduces 34 of the 48 audited cells to the dollar. The
14 misses all sit low, and every one contains loans from the flood counties. After the 2021 floods the bank granted 1,140 borrowers
payment holidays of six, nine or twelve months, with maturities extended by the same months. A loan in a holiday can neither charge off
nor prepay, so its months in the holiday are not months at risk. The predecessor's method ran each loan's age on a repayment clock that
stops for the loan's own holiday months, in the estimation sample and in the projection alike. Calendar age makes a FY2020 loan with a
twelve-month holiday look a year further past its hazard peak than it is. The months sit only in the servicing deferral ledger, joined
loan by loan, and no single shift of the clock reproduces six- and twelve-month holidays at once.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Kaplan–Meier charge-off curve by term class, payoffs censored, loan counts, applied to each active loan's unguaranteed balance at the memo's severity | $28.8M, +62% | The textbook survival estimator, conditioned on survival as the memo asks | The loan ledger: 38% of mature loans paid in full before maturity, and a paid-off loan cannot charge off; every audited cell sits below this construction |
| 1 | Competing-risk (Aalen–Johansen) incidence of charge-off with payoff competing, loan counts | $21.5M, +21% | The memo's estimator family, payoff handled correctly | **E07 (two grains, both flawless):** the memo reserves unguaranteed dollars, and loans under $150,000 charge off at 2.8× the rate of loans over $1 million, so loan-count incidence has the wrong shape for dollars |
| 2 | The same incidence weighted by unguaranteed balance, age from first disbursement | $15.3M, −14% | The right estimator on the right grain, and 34 of 48 audited cells reproduce to the dollar | The 14 unreproduced cells: all low, and each holds loans the deferral ledger shows in a 2021 payment holiday |
| 3 | **Decisive:** the same with every loan's age on a repayment clock that stops for its own holiday months, joined from the deferral ledger, in estimation and projection | **$17.8M** | — | — |

* **Figure shape.** The corrections walk the figure down (+62%, +21%, −14%) and the decisive rung turns it back up by 16%. A solver who
  stops anywhere short is wrong in a known direction.
* **Partial correction priced (L3).** Shifting every holiday loan by the programme's standard nine months reproduces 41 cells and books
  $16.3M (−8.4%), because the twelve-month holidays cluster in the FY2020 vintage. Pausing the clock in the projection but keeping
  calendar-age curves reproduces 39 cells and books $15.9M (−10.7%): the estimation sample's own holiday loans flatten the curves at the
  ages they passed through in 2021.
* **Grid.** Estimator (Kaplan–Meier, competing risks) × grain (loans, dollars) × clock (calendar, flat nine-month shift, ledger pause
  in projection only, ledger pause throughout) gives 16 cells. Only competing risks on dollars with the full ledger clock reproduces all
  48 audited cells; every other cell sits at least 8.4% from $17.8M, the nearest being the flat shift.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo names the estimator, the unit and the conditioning. No document says what age the curves run on, and
   the deferral ledger ships for the servicing team's delinquency reporting.
2. **The reproduction numbers.** The ledger clock in estimation and projection reproduces 48 of 48 audited cells to the dollar; calendar
   age 34, the flat nine-month shift 41, the projection-only pause 39, and every rival misses low, so each fails on the close-out totals
   too. The reproducing rule is a per-loan clock built through a join on loan number, not a parameter: no single shift fits six- and
   twelve-month holidays at once.
3. **No arithmetic symptom.** Balances tie to the general ledger, events to the loan ledger and guarantees to the authorisations, under
   every rung. The misses are a few per cent and all one sign.
4. **Not a row predicate.** No loan is dropped or flagged. Each loan's months at risk are rebuilt as calendar months less its cumulative
   holiday months at each date, which changes the risk sets the estimator runs on and the point at which each active loan is conditioned.
5. **The enumeration is arithmetic.** Each loan's repayment age at each snapshot is computed from the ledger. No column holds it.
6. **No cutover date.** Holidays began over five months of 2021 and ran for different lengths. No outcome series steps, and the effect
   lives in where each loan sits on its curve.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The audited close-outs at the last three year-ends: reserves by approval vintage (FY2014–FY2021) and term class, 48 cells,
  each with the loan, event and ledger snapshot it was computed from.
* **What it certifies.** The estimator (competing risks), the grain (unguaranteed dollars) and the clock (repayment months), jointly: only
  that construction reproduces every cell, and the cells with no holiday loans reproduce under calendar age as well.
* **What it pins.** The clock: each loan's own holiday months, removed from its age in the estimation sample and in the projection.
* **Twin pair.** Loans L-30417 and L-52288 (FY2020, ten-year term) are identical on every loan-ledger column: approval amount, guarantee
  share, rate, industry, disbursement month and an unbroken payment record. Their reserves in last year's close-out were $11,480 and $5,690
  (2.0×), because L-30417 spent twelve months in a holiday and sat at repayment month 29 against 41. Calendar age gives both $5,690.
* **Resemblance points at the decoy.** The FY2019–21 vintages match FY2014–16 at the same calendar age on every ledger column, and the
  FY2014–16 cells reproduce under calendar age.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The reserving memo: lifetime expected charge-offs of each loan's unguaranteed balance, competing risks of charge-off and
  payoff, by term class, conditional on survival to the reserve date, estimated on the bank's loans approved since FY2010, at the memo's
  severity by term class. The model-risk standard: a year-end method must reproduce every audited close-out cell to the dollar from that
  close-out's snapshot. The holiday agreements: maturity extended by the holiday's length.
* **Empirical pins.** Events and balances, from the loan ledger. Each loan's holiday months, from the deferral ledger. The clock, from the
  close-outs.
* **Voices.** The chief credit officer: "The flood borrowers caught up long ago; the holiday is behind them." The finance director:
  "Charge-offs to date are what the auditors read first."
* **Licensed wrong basis.** The memo records that the bank's regulator compares reserves with the peer group's charge-offs to date over
  originations by vintage, and will see that ratio in the call report.

## 8. Determinism by construction

* **Clock.** Holidays start on the first of a month and run whole months, and the ledger is effective-dated, so each loan's repayment age
  at every snapshot is a single integer.
* **Ties.** Events are monthly; the memo orders a charge-off before a payoff in the same month, and no loan has both.
* **Horizon.** Each loan's remaining term in repayment months is its original term less its repayment age, because holidays extended
  maturity by their own length.
* **Severity and guarantee.** Severity by term class is the memo's, and guarantee shares come from each authorisation; both reproduce
  under every clock, so neither can absorb the misses.
* **Snapshots.** Each close-out ships with its snapshot, so the reproduction never depends on later revisions.

## 9. Prompt sketch and deliverables

> I book the year-end reserve for our 2019–21 7(a) loans next week, and it goes to the audit committee as one number in millions to one
> decimal. Our chief credit officer says the flood borrowers are long past their holiday and nothing about them should change. Send me
> `reserve_2019_21.xlsx`, a chart `incidence_by_clock.png`, and a one-page `reserve_memo.pdf` that commits to the figure.

* `reserve_2019_21.xlsx` — the reserve build by loan, vintage and term class, the delinquency sheet (ask A) and the recovery sheet
  (ask B).
* `incidence_by_clock.png` — cumulative incidence of charge-off by term class on repayment months and on calendar months, the FY2019–21
  book's ages on both clocks as histograms, the 48 audited cells as a reproduction strip, and the four rung reserves as labelled bars.
* `reserve_memo.pdf` — the committed reserve, the reproduction count, and the peer ratio the regulator will compare.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each vintage FY2014–FY2021, the share of loans and of unguaranteed dollars 30 or more days
  past due at year-end. *Device:* a returned direct debit posts as the payment, a reversal and the re-presented payment, and the servicing
  guide runs days past due from the original due date to the settled payment. Reading the first payment as settled understates
  delinquency in three vintages.
* **Ask B (device-carried).** For each of the last eight quarters, the bank's recoveries on charged-off loans and the recovery rate on
  loans charged off two years earlier. *Device:* a recovery posts as a gross receipt followed by a remittance row passing the SBA's share
  back, and the bank's recovery is the net. Summing receipts overstates recoveries by the guaranteed share. Recoveries play no part in the
  memo's severity.
* **Ask C (validity).** The reserve under each of the four rung constructions, with each one's count of reproduced audited cells.
* **Decoupling.** Replacing the repayment clock with calendar age changes no figure in asks A or B.

## 11. Rubric arithmetic

8 vintages × 2 (ask A) + 8 quarters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed reserve, the holiday loans' share of the
book and the cells reproduced + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* FY2019–21 active book: 2,860 loans, $342 million unguaranteed. 790 of them took holidays (31% of the balance): six months for 310,
  nine for 260, twelve for 220, the twelve-month holidays concentrated in FY2020.
* Rung figures $28.8M / $21.5M / $15.3M / $17.8M; partial cells $16.3M and $15.9M; no grid cell within 8.4% of the answer.
* Audited cells reproduced: 0 / 0 / 34 / 48 by rung; 41 for the flat shift and 39 for the projection-only pause. Every miss is low.
* Loans under $150,000 charge off at 2.8× the rate of loans over $1 million. 38% of mature loans paid in full before maturity.
* L-30417 and L-52288 are identical on every loan-ledger column.
* Returned debits and recovery remittances never touch events, balances, guarantees or the deferral ledger.
