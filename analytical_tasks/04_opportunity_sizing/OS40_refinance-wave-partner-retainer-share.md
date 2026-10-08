# OS40 — What the recapture partners cost in the refinance wave, when last year's cost per loan carries retainers the wave multiplies

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · mortgage lending and servicing |
| Mirrors | Unit costs carried onto a surge when vendor contracts are mostly fixed (cloud and CDN budgets for a launch priced at last quarter's cost per request under committed-spend contracts, peak-season parcel budgets at average cost per parcel when carrier lanes are paid by the trailer, outsourced marketplace support priced per ticket under retainer contracts) |
| Decision shape | One figure committed at a date: the recapture-partner budget for the wave quarter, written into Friday's operating plan |
| Committed call | What the three recapture partners will invoice for next quarter, in dollars to the nearest $10,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · S6 (the cost per funded recapture everyone holds is each loan's correct share of its partner's monthly invoice, not the price of a wave-quarter loan: a partner bills a retainer for every market it works in a month plus a fee per loan, and the wave both spreads those retainers over more loans and switches on partners that worked none of last year's months in a market), with E19 below it (recaptures identified by same-day, same-amount payoff pairs, not by campaign codes) |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #7 uses the ready-made measure · #17 guesses an attribution the data can settle · #12 stops at the first control that passes |
| Calibration form | Existing-book actuals: last year's recapture book by market and month (payoffs, the funding ledger's disbursements with each loan's packaging partner, campaign-coded loans, the finance team's cost allocation per funded recapture and the partners' 36 monthly invoices) |
| Driving force | Each partner bills a retainer for every market in which it packages at least one loan that month, plus a fee per loan, and nothing in the pack labels either. Last year's cost per funded recapture ($2,349 to $2,878 by market) is each loan's correct share of its partner's monthly invoice, so carried onto the wave it repays the retainers once per loan. But the wave also overflows each market's first partner: the routing table sends loans past its monthly capacity to the next partner, who then bills that market's retainer too. In Phoenix, Pittsburgh and Hartford these are partners that worked none of last year's months there. The budget is built month by month from active partner-market-months, a unit no file stores. |

## 1. Situation

A mortgage lender services 214,000 loans in six metropolitan markets and runs a recapture programme: when a borrower it services
refinances, it wants to be the lender. Three fulfilment partners take the calls, gather documents and package files for its underwriters,
and each invoices it monthly for all its markets together. A routing table sends each market's recaptures to a first partner up to a monthly
capacity and the rest to the next. Rates fell this month, and the pricing desk's prepayment projection expects 11,392 voluntary payoffs of
in-the-money loans next quarter, front-loaded into its first month, against about 3,800 in a typical quarter last year. Friday's operating
plan must carry the partner budget for that quarter. The controller notes that cost per funded recapture has barely moved in two years.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the projection, the funding ledger, the campaign codes, the cost allocation, the routing table and
  the invoices. The controller is right that cost per funded recapture has been steady. Nothing reported is overturned. The difficulty is
  that a cost per loan is a share of a month's invoice, and the wave quarter is a different book with different partners working.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the controller's view and every voice. The allocation file still prices every funded recapture, and volume ×
  cost per loan is still the standard budget build.
* **Instrument repair.** Suspect file: the campaign codes, which stand in for a missing recapture field and also tag purchase loans after a
  home sale. Repaired, rung 0 becomes rung 1 ($8.09M), and rungs 2 and 3 stay at $6.49M and $3.00M. The invoices, allocations, routing
  table and packaging-partner field are complete: allocated costs sum to every invoice to the cent, and an invoice records what was billed.
  An active partner-market-month is a unit no row records, so the construction is still needed for $4.54M.
* **Lens swap.** The answer prices a different moment: a quarter whose density and working partners no closed month had, not last year's
  costs under another lens.

## 3. The driving force

A strong solver builds forward funded recaptures from the projection: it identifies last year's recaptures from the funding ledger rather
than the campaign codes, and it removes loans the retention policy will not solicit. It multiplies by last year's cost per funded
recapture, which finance allocates loan by loan from each partner's monthly invoice. A careful one then sees that the invoices do not
scale with volume, and finds that the partners' invoices follow an exact monthly retainer plus a fee per loan in 31 of their 36 months. It
prices the wave on that law, every market's loans going to its first partner. But the five months the law misses are the months a partner
packaged loans in an extra market, and each misses by exactly one retainer per extra market. A partner bills a retainer per market it
works each month. The wave's first month carries 55% of the quarter, two to seven times last year's average month, so it overflows the
first partner in every market. Overflow switches on the next partner and its retainer, in Phoenix (two partners), Pittsburgh and Hartford
for the first time. The budget is the active partner-market-months the routing table produces month by month, priced at each partner's
retainer, plus its fees.

## 4. The ladder

| Rung | Construction (partner budget for the wave quarter) | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Projected payoffs × the retention dashboard's recapture share (40%, from campaign codes) × last year's cost per funded recapture | $12.44M, +174.1% | The desk's projection, the programme's own recapture metric and finance's own unit cost | The funding ledger: only 26% of last year's eligible payoffs were paid by the lender's own same-day disbursement of the identical amount; campaign codes also tag purchase loans after a home sale, which no partner handles |
| 1 | Recapture share from same-day, same-amount payoff pairs (26%) | $8.09M, +78.2% | The attribution the money settles, confirmed by the retention desk's bonus payroll | The retention policy: loans inside their investors' 180-day early-payoff window are not solicited, and they are 20% of projected payoffs (31% in Phoenix) |
| 2 | Projected payoffs outside the window only (9,154 of 11,392) × 26% = 2,380 funded recaptures | $6.49M, +43.0% | Volume built from the right population, priced at a unit cost that reproduces every annual total | Partner B's invoices moved by exactly $550 per extra loan all year, so its cost per loan fell from $3,101 in January to $2,633 in each Q3 month |
| 3 | Each partner's flat-month law (a monthly retainer plus a fee, exact in 31 of 36 months), every market's wave loans at its first partner | $3.00M, −33.8% | An exact law for 31 of 36 partner-months, with the Q3 misses read as a one-off | The packaging-partner field: each of the five misses is a month in which the partner packaged loans in one or two extra markets, and it misses by exactly one retainer per extra market |
| 4 | **Decisive:** a retainer per active partner-market-month plus a fee, recovered from all 36 invoices; the wave routed month by month through the routing table | **$4,538,750** | — | — |

* **The answer.** Partner A $1,780,750 (11 active market-months, 963 loans), partner B $1,584,400 (10, 608) and partner C $1,173,600 (10,
  809): $4,538,750, committed as $4,540,000.
* **Figure shape.** The first three corrections walk the budget down (−35.0%, −19.8%, −53.7%), and the decisive move reverses the last
  (+51.1%), landing between rungs 2 and 3.
* **The deciding comparison.** The flat-month law leaves out $1.54M of retainers for 13 overflow partner-market-months. Six of them are
  partners that worked none of last year's months in that market: C and B in Phoenix, B in Pittsburgh and B in Hartford.
* **Partial correction priced (L3).** Each half-built construction lands at least 16% from the answer. Pricing the wave at last year's Q3
  cost per loan, taking the mini-wave as the analogue, gives $6.40M (+41.0%). Building active partner-months but letting only last year's
  working partners take overflow gives $3.79M (−16.5%). Routing the quarter's volume against three months of capacity gives $5.44M
  (+19.9%), because the wave's third month overflows almost nowhere. Charging one retainer per active partner-month instead of per market
  gives $1.95M (−57.1%).
* **Grid.** Recapture attribution (campaign codes, payoff pairs) × early-payoff window (ignored, applied) × cost law (carried cost per
  loan, flat-month law, active partner-market-months) = 12 cells. The nearest wrong cells are campaign codes with the window ignored on
  the flat-month law, $3.80M (−16.4%), and payoff pairs with the window ignored on the active law, $5.35M (+17.9%). Every other cell is at
  least 23% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The partner agreements are not in the pack. Each monthly invoice carries one amount, "recapture fulfilment
   services", and the allocation file one cost per loan. No document says a partner bills by market or by month.
2. **The corpus pins the law by reproduction (Pattern B).** A retainer per active partner-market-month plus a fee reproduces all 36 monthly
   invoices to the dollar. The flat-month law reproduces 31, missing exactly the five months in which a partner worked an extra market.
   Last year's cost per loan reproduces every annual total and no month, and both laws on campaign-coded counts reproduce none. The active
   partner-market-month is a unit no row records: a group-by of the funding ledger's packaging-partner field by market and month, after
   the payoff-pair join.
3. **No arithmetic symptom.** Allocated costs sum to every invoice, invoices tie to the ledger, and pairs reconcile to payoffs and
   disbursements. Carrying the shares breaks no total.
4. **Not a row predicate.** A retainer attaches to a partner-market-month with at least one packaged loan, a property of a group, not of
   any loan or invoice row.
5. **The enumeration is arithmetic.** No column holds a retainer, a fee or an active month. Three retainers and three fees come from 36
   invoices over 78 active partner-market-months, and the wave's 31 come from routing 18 market-months through the routing table.
6. **No cutover date.** The terms and the routing held all year. The wave changes the book's density and which partners work each market,
   not the contracts.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Last year's book by market and month: 15,190 eligible voluntary payoffs, the funding ledger's disbursements with each funded
  loan's packaging partner, campaign-coded funded loans, the finance team's allocated partner cost for each of the 3,949 funded recaptures,
  and the 36 monthly partner invoices.
* **What it certifies.** The payoff-pair recapture share (26%), which alone reproduces the retention desk's bonus payroll ($150 a
  recapture) in 72 of 72 market-months. Also the allocation, whose shares sum to every invoice, and last year's cost per funded recapture,
  which reproduces every annual total. A solver who back-tests rungs 1 and 2 on annual totals is confirmed, and one who back-tests rung 3
  is confirmed in 31 of 36 months.
* **What it pins.** Each partner's retainer per active market-month and its fee, through the five Q3 months (above). A partner that worked
  none of last year's months in a market is priced from the markets it did work: B from Denver and Columbus, C from Pittsburgh and
  Hartford.
* **Twin pair.** Partner A's July and August invoices cover the same 184 funded recaptures, and the flat-month law prices both at
  $326,000. July's invoice is $606,000 and August's $466,000, $280,000 and $140,000 above the law, 2.0× apart, because A packaged loans in
  Denver and Columbus in July and in Denver alone in August. No law in recaptures alone separates them.
* **Resemblance points at the decoy.** The wave quarter most resembles last year's Q3 mini-wave, and Q3's cost per loan, carried as the
  wave rate, lands at $6.40M.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The operating-plan policy budgets a programme at what its vendors will invoice in the quarter. The retention policy does
  not solicit loans inside their investors' 180-day early-payoff window, evaluated on the quarter's first day. The prepayment desk's
  projection, by market and month, is the planning projection of payoffs. The recapture share is carried from last year's book. The
  routing table, in force for the wave quarter, lists each market's partners in order with a monthly capacity for every partner but the
  last.
* **Empirical pins.** The recapture share from payoff pairs; each partner's retainer and fee from last year's invoices through active
  partner-market-months.
* **Voices.** The controller: "Cost per funded loan has barely moved in two years." That is true. The head of retention: "Our partners are
  paid by the loan, so a bigger wave is just a bigger bill."
* **Licensed wrong basis.** The operating-plan policy records that the board's finance committee reviews programme budgets as unit cost ×
  volume and will see that basis.

## 8. Determinism by construction

* **Payoff pairing.** A pair is a payoff and a disbursement on the same day for the identical amount to the cent. No payoff matches two
  disbursements, and no recapture funded on a different day.
* **Early-payoff window.** Pinned to the quarter's first day, and no loan's window ends within 10 days of it.
* **Packaging partner.** Every funded recapture carries exactly one packaging partner, and a partner-market-month is active when it holds
  at least one loan.
* **Routing.** Every wave month's volume in every market sits at least three loans from a capacity, so the 26% share's rounding moves no
  activation.
* **Month assignment.** Invoices, pairs, allocations and the projection are all dated by funding month, so no recapture crosses a month.
* **Recovery.** The active-month law fits all 36 invoices with zero residual, so any solve returns the same retainers and fees.
* **Rounding.** $4,538,750 sits $3,750 from the nearest $10,000 rounding boundary.
* **Maturity.** Last year's invoices are paid and final, with no credit notes open.

## 9. Prompt sketch and deliverables

> Rates broke lower this month and the pricing desk expects a refinance wave next quarter. Finance closes the operating plan on Friday and
> needs one number from us: what our recapture partners will cost for that quarter, to the nearest $10,000. Our controller points out
> that cost per funded loan has barely moved in two years. Send `wave_partner_budget.xlsx`, a chart `partner_cost_lines.png`, and a
> one-page `operating_plan_note.pdf`.

* `wave_partner_budget.xlsx`: the build under the five rung bases, the recovered retainers and fees, the wave's routing by market and
  month, the escrow sheet (ask A) and the contact-centre sheet (ask B).
* `partner_cost_lines.png`: three small panels, one per partner, each plotting last year's twelve monthly invoices against funded
  recaptures with points coloured by the number of markets worked, the active-month law's lines, the carried cost-per-loan line for
  contrast, and the wave months' invoices marked.
* `operating_plan_note.pdf`: the committed budget, the partner split and the basis the finance committee will bring.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six markets, the number of escrow accounts that showed a shortage at last year's
  annual analysis, and the median shortage. *Device:* a shortage paid in a lump posts as one escrow deposit with a shortage code, while a
  spread shortage posts inside twelve monthly payments as an escrow-only increment, per the escrow servicing guide. Counting coded deposits
  alone misses 70% of shortages in the four markets with property-tax reassessments.
* **Ask B (device-carried).** For each market, the average monthly number of borrower calls to the servicing centre last year and the share
  resolved on first contact. *Device:* a transferred call keeps its call ID and adds a leg, and one call is all legs under one ID, per the
  contact-centre data guide. Counting legs as calls overstates volume by 22% in the two markets routed through the overflow centre.
* **Ask C (validity).** The budget under each of the five rung bases; the reproduction of last year's 36 invoices under the carried cost per
  loan (none, with every annual total), the flat-month law (31) and the active-month law (36); and the bonus payroll under payoff pairs and
  campaign codes (72 and 0 of 72 market-months).
* **Decoupling.** Clearing the active-month construction changes no figure in asks A or B, and neither touches payoffs, disbursements or
  partner invoices.

## 11. Rubric arithmetic

6 markets × 2 (ask A) + 6 × 2 (ask B) + 5 bases + 5 reproduction counts (ask C) + the committed budget, and each partner's retainer, fee,
wave active market-months and wave loans (12) + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Partner terms (retainer per active market-month, fee per loan): A $140,000 + $250, B $125,000 + $550, C $85,000 + $400.
* Routing table (partners in order, monthly capacity): Phoenix A 100, C 85, then B; Dallas A 86, then C; Denver B 60, then A; Columbus B
  60, then A; Pittsburgh C 90, then B; Hartford C 60, then B.
* Last year's pair-counted recaptures by month: January to June and October to December run at each market's base plus −3, −1, +1, +3, 0,
  −2, +2, 0 and 0, on bases of Phoenix 44, Dallas 64, Denver 52, Columbus 52, Pittsburgh 41 and Hartford 52. July to September: Phoenix
  58/56/54, Dallas 96/92/88, Denver 80/102/60, Columbus 80/60/60, Pittsburgh 49/48/50, Hartford 58/57/56 (3,949 in all). Annual invoices
  $10,627,000; cost per funded recapture $2,801 / $2,793 / $2,857 / $2,878 / $2,356 / $2,349.
* Recapture share 26% by payoff pairs and 40% by campaign codes, in every market. Projected payoffs next quarter, all and outside the
  window: Phoenix 3,123 / 2,154, Dallas 2,500 / 2,077, Denver 1,923 / 1,615, Columbus 1,577 / 1,385, Pittsburgh 1,288 / 1,077, Hartford
  981 / 846. Forward funded recaptures 560 / 540 / 420 / 360 / 280 / 220 = 2,380, split 55%, 30% and 15% across the quarter's months.
* Rung figures $12.44M / $8.09M / $6.49M / $3.00M / $4.54M; partials and grid cells as stated, none within 16% of the answer. Partner A's
  July and August invoices cover 184 recaptures each at $606,000 and $466,000.
* Escrow analyses and contact-centre legs never touch payoffs, the funding ledger, the allocation or the invoices.
