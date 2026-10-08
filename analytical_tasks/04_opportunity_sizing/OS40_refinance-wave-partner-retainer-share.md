# OS40 — What the recapture partners cost in the refinance wave, when last year's cost per loan carries each partner's retainer

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · mortgage lending and servicing |
| Mirrors | Unit costs carried onto a surge when vendor contracts are mostly fixed (cloud and CDN budgets for a launch priced at last quarter's cost per request under committed-spend contracts, peak-season parcel budgets at average cost per parcel when carrier lanes are paid by the trailer, outsourced marketplace support priced per ticket under retainer contracts) |
| Decision shape | One figure committed at a date: the recapture-partner budget for the wave quarter, written into Friday's operating plan |
| Committed call | What the three recapture partners will invoice for next quarter, in dollars to the nearest $10,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · S6 (the cost per funded recapture everyone holds is each loan's correct share of its own quarter's invoice, not the price of a wave-quarter loan; the retainer and fee behind it are recovered from last year's quarters), with E19 below it (recaptures identified by same-day, same-amount payoff pairs, not by campaign codes) |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #7 uses the ready-made measure · #17 guesses an attribution the data can settle · #12 stops at the first control that passes |
| Calibration form | Existing-book actuals: last year's recapture book by market and quarter (payoffs, the funding ledger's disbursements, campaign-coded loans, the finance team's cost allocation per funded recapture and the partners' quarterly invoices) |
| Driving force | A partner's quarterly invoice is a retainer plus a fee per loan, and nothing in the pack labels either. Last year's cost per funded recapture ($2,014 to $2,500 by market) is each loan's correct share of its own quarter's invoice, so it carries the retainer once per loan. The wave quarter funds 2.3× last year's average volume and Phoenix 3.7×, so carried shares repay $1.12M of retainers 2.65 times. Each market's retainer and fee are recovered from last year's third-quarter mini-wave, the one quarter whose volume moved, counted on payoff pairs. |

## 1. Situation

A mortgage lender services 214,000 loans in six metropolitan markets and runs a recapture programme: when a borrower it services
refinances, it wants to be the lender. Three fulfilment partners take the calls, gather documents and package files for its underwriters,
and invoice it quarterly: partner A in Phoenix and Dallas, partner B in Denver and Columbus, partner C in Pittsburgh and Hartford. Rates
fell this month, and the pricing desk's prepayment projection expects 11,392 voluntary payoffs of in-the-money loans next quarter, against
about 3,960 in a typical quarter last year. Friday's operating plan must carry the partner budget for that quarter. The controller notes
that cost per funded recapture has barely moved in two years.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the projection, the funding ledger, the campaign codes, the cost allocation and the invoices. The
  controller is right that cost per funded recapture has been steady. Nothing reported is overturned. The difficulty is that a cost per
  loan is a share of a quarter's invoice, and the wave quarter is a different book.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the controller's view and every voice. The allocation file still prices every funded recapture, and volume ×
  cost per loan is still the standard budget build.
* **Instrument repair.** Suspect file: the campaign codes, which stand in for a missing recapture field and also tag purchase loans after a
  home sale. Repaired, rung 0 becomes rung 1 ($6.57M), and rung 2 stays at $5.24M. Invoices and allocations are complete: allocated costs
  sum to every invoice to the cent, and an invoice records what was billed. Its split into retainer and fee is a rule recovered from
  complete records, so the retainer construction is still needed for $3.39M.
* **Lens swap.** The answer prices a different moment: the invoices of a quarter whose density no closed quarter had, not last year's
  costs under another lens.

## 3. The driving force

A strong solver builds forward funded recaptures from the projection: it identifies last year's recaptures from the funding ledger rather
than the campaign codes, and it removes loans the retention policy will not solicit. It then multiplies by last year's cost per funded
recapture, which the finance team allocates loan by loan. Each allocated cost is correct: it is that loan's share of its own market's
quarterly invoice, and the shares sum to every invoice. But an invoice is a retainer plus a fee per loan. Last year's third quarter was a
brief rate dip, the only quarter whose volume moved: recaptures rose about 60% in every market and invoices rose by exactly $600, $900 or
$1,800 per extra recapture, by partner. Solving each market's flat and mini-wave quarters gives its retainer and fee, and the wave
quarter's invoice is the retainer once plus the fee per loan. Carried at last year's density, the shares repay the $1.12M of quarterly
retainers 2.65 times. The error is largest in Phoenix, whose wave is 3.7 times its average quarter and whose partner is mostly retainer.

## 4. The ladder

| Rung | Construction (partner budget for the wave quarter) | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Projected payoffs × the retention dashboard's recapture share (40%, from campaign codes) × last year's cost per funded recapture | $10.10M, +198.0% | The desk's projection, the programme's own recapture metric and finance's own unit cost | The funding ledger: only 26% of last year's eligible payoffs were paid by the lender's own same-day disbursement of the identical amount; campaign codes also tag purchase loans after a home sale, which no partner handles |
| 1 | Recapture share from same-day, same-amount payoff pairs (26%) | $6.57M, +93.7% | The attribution the money settles, confirmed by the retention desk's bonus payroll | The retention policy: loans inside their investors' 180-day early-payoff window are not solicited, and they are 20% of projected payoffs (31% in Phoenix) |
| 2 | Projected payoffs outside the window only (9,154 of 11,392) × 26% = 2,380 funded recaptures | $5.24M, +54.5% | Volume built from the right population, priced at a unit cost that reproduces every annual total | Last year's invoices: the Q3 mini-wave's 60% more recaptures raised them by only 13% to 53% |
| 3 | **Decisive:** each market's retainer and fee recovered from last year's four quarters on pair-counted recaptures; budget = Σ (retainer + fee × forward funded) | **$3,390,000** | — | — |

* **Figure shape.** Every correction walks the budget down (−35.0%, −20.2%, −35.3%), and the answer is the minimum cell of the grid.
* **The answer.** Phoenix $621,000, Dallas $690,000, Denver $588,000, Columbus $495,000, Pittsburgh $552,000 and Hartford $444,000:
  $3,390,000.
* **Partial correction priced (L3).** Pricing the wave at last year's Q3 cost per loan, taking the mini-wave as the analogue, gives
  $4.39M (+29.4%), nearer rung 2 than the answer. Fitting one retainer and one fee across all 24 market-quarters ($128,256 and $1,411)
  gives $4.13M (+21.8%), because pooling hands partner C's fee to partner A's volume. Neither half-step comes within 21% of the answer.
* **Grid.** Recapture attribution (campaign codes, payoff pairs) × early-payoff window (ignored, applied) × cost law (carried cost per
  loan, retainer plus fee) = 8 cells. The nearest wrong cell is payoff pairs and the retainer law without the window, $3.88M (+14.4%),
  reached only by budgeting for loans the policy will not solicit. Every other cell is at least 36% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The partner agreements are not in the pack. Each invoice carries one amount, "recapture fulfilment services", and
   the allocation file carries one cost per loan. No document says an invoice has a part that does not move with volume.
2. **The corpus pins the law only by reproduction (Pattern B).** Retainer plus fee on pair-counted recaptures reproduces 24 of 24 quarterly
   invoices to the dollar. The best rival, last year's cost per funded recapture, reproduces 6 of 6 annual totals and 0 of 24 quarters
   (−1.5% to −10.5% in flat quarters, +3.1% to +27.7% in Q3). The same affine law fitted on campaign-coded counts reproduces none, because
   those counts carry purchase loans no partner touched. The law is two unknowns per market, solved against counts that exist only after
   the payoff-pair join.
3. **No arithmetic symptom.** Allocated costs sum to every invoice, invoices tie to the ledger, and pairs reconcile to payoffs and
   disbursements. Carrying the shares breaks no total.
4. **Not a row predicate.** A retainer is an intercept across a market's quarters, not a property of any loan or invoice row.
5. **The enumeration is arithmetic.** No column holds a retainer or a fee. Six retainers and three fees are computed from 24 invoices.
6. **No cutover date.** The mini-wave is a volume swing, not a step in the cost law, and the wave quarter changes density, not contracts.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Last year's book by market and quarter: 15,850 eligible voluntary payoffs, the funding ledger's disbursements, campaign-coded
  funded loans, the finance team's allocated partner cost for each of the 4,120 funded recaptures, and the 24 quarterly invoices.
* **What it certifies.** The payoff-pair recapture share (26%), which alone reproduces the retention desk's bonus payroll ($150 a
  recapture) in 24 of 24 market-quarters. Also the allocation, whose shares sum to every invoice, and last year's cost per funded
  recapture, which reproduces every annual total. A solver who back-tests rungs 1 and 2 on annual totals is confirmed.
* **What it pins.** The retainer and fee by market, through the mini-wave (above).
* **Twin pair.** Denver and Hartford are identical on every annual column a lookup reaches: funded recaptures in each quarter (156, 156,
  252, 156), the annual invoice ($1,488,000) and the cost per funded recapture ($2,067). The mini-wave's 96 extra recaptures raised
  Denver's invoice by $86,400 and Hartford's by $172,800, 2.0× apart, because partner B is mostly retainer and partner C mostly fee. A
  carried cost per loan prices both the same.
* **Resemblance points at the decoy.** The wave quarter most resembles last year's Q3 mini-wave, and Q3's cost per loan, carried as the
  wave rate, lands at $4.39M.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The operating-plan policy budgets a programme at what its vendors will invoice in the quarter. The retention policy does
  not solicit loans inside their investors' 180-day early-payoff window, evaluated on the quarter's first day. The prepayment desk's
  projection is the planning projection of payoffs. The recapture share is carried from last year's book.
* **Empirical pins.** The recapture share from payoff pairs; each market's retainer and fee from last year's invoices.
* **Voices.** The controller: "Cost per funded loan has barely moved in two years." That is true. The head of retention: "A wave this size
  will stretch every partner we have."
* **Licensed wrong basis.** The operating-plan policy records that the board's finance committee reviews programme budgets as unit cost ×
  volume and will see that basis.

## 8. Determinism by construction

* **Payoff pairing.** A pair is a payoff and a disbursement on the same day for the identical amount to the cent. No payoff matches two
  disbursements, and no recapture funded on a different day.
* **Early-payoff window.** Pinned to the quarter's first day, and no loan's window ends within 10 days of it.
* **Quarter assignment.** Invoices, pairs and allocations are all dated by funding date, so no recapture crosses a quarter.
* **Recovery.** The retainer law fits all 24 invoices with zero residual, so two-point solves, least squares and any pair of quarters
  return the same retainers and fees.
* **Rounding.** $3,390,000 sits $5,000 from the nearest $10,000 rounding boundary.
* **Maturity.** Last year's invoices are paid and final, with no credit notes open.

## 9. Prompt sketch and deliverables

> Rates broke lower this month and the pricing desk expects a refinance wave next quarter. Finance closes the operating plan on Friday and
> needs one number from us: what our recapture partners will cost for that quarter, to the nearest $10,000. Our controller points out
> that cost per funded loan has barely moved in two years. Send `wave_partner_budget.xlsx`, a chart `partner_cost_lines.png`, and a
> one-page `operating_plan_note.pdf`.

* `wave_partner_budget.xlsx`: the build by market under the four rung bases, the recovered retainers and fees, the escrow sheet (ask A) and
  the contact-centre sheet (ask B).
* `partner_cost_lines.png`: six small panels, one per market, each plotting last year's four quarterly invoices against funded recaptures,
  the retainer-plus-fee line extended to the wave quarter's volume, the carried cost-per-loan line for contrast, and the wave-quarter
  budget marked.
* `operating_plan_note.pdf`: the committed budget, the market split and the basis the finance committee will bring.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six markets, the number of escrow accounts that showed a shortage at last year's
  annual analysis, and the median shortage. *Device:* a shortage paid in a lump posts as one escrow deposit with a shortage code, while a
  spread shortage posts inside twelve monthly payments as an escrow-only increment, per the escrow servicing guide. Counting coded deposits
  alone misses 70% of shortages in the four markets with property-tax reassessments.
* **Ask B (device-carried).** For each market, the average monthly number of borrower calls to the servicing centre last year and the share
  resolved on first contact. *Device:* a transferred call keeps its call ID and adds a leg, and one call is all legs under one ID, per the
  contact-centre data guide. Counting legs as calls overstates volume by 22% in the two markets routed through the overflow centre.
* **Ask C (validity).** The budget under each of the four rung bases; the reproduction of last year's 24 invoices under the carried cost
  per loan (0 of 24, with 6 of 6 annual totals) and the retainer law (24 of 24); and the bonus payroll under payoff pairs and campaign codes
  (24 and 0 of 24).
* **Decoupling.** Clearing the retainer construction changes no figure in asks A or B, and neither touches payoffs, disbursements or
  partner invoices.

## 11. Rubric arithmetic

6 markets × 2 (ask A) + 6 × 2 (ask B) + 4 bases + 5 reproduction counts (ask C) + the committed budget, and each market's retainer, fee and
forward funded recaptures (18) + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Quarterly retainer and fee per funded recapture: Phoenix $285,000 + $600 and Dallas $366,000 + $600 (partner A), Denver $210,000 + $900
  and Columbus $180,000 + $900 (partner B), Pittsburgh $30,000 + $1,800 and Hartford $48,000 + $1,800 (partner C). Retainers total
  $1,119,000 a quarter.
* Last year's pair-counted recaptures (Q1, Q2, Q3, Q4): Phoenix 130/130/210/130, Dallas 190/190/310/190, Denver 156/156/252/156, Columbus
  139/139/223/139, Pittsburgh 122/122/194/122, Hartford 156/156/252/156 (4,120 in all). Cost per funded recapture $2,500 / $2,264 /
  $2,067 / $2,025 / $2,014 / $2,067.
* Recapture share 26% by payoff pairs and 40% by campaign codes, in every market. Projected payoffs next quarter, all and outside the
  window: Phoenix 3,123 / 2,154, Dallas 2,500 / 2,077, Denver 1,923 / 1,615, Columbus 1,577 / 1,346, Pittsburgh 1,288 / 1,115, Hartford
  981 / 846. Forward funded recaptures 560 / 540 / 420 / 350 / 290 / 220 = 2,380.
* Rung figures $10.10M / $6.57M / $5.24M / $3.39M, and the nearest other cell is $3.88M (+14.4%). Denver and Hartford are identical on
  every annual column.
* Escrow analyses and contact-centre legs never touch payoffs, the funding ledger, the allocation or the invoices.
