# FC37 — Which fixed-rate pool the bank's one swap overlay is designated against, when last year's losses and this year's exposure rank the pools almost in reverse

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · bank balance-sheet risk management |
| Mirrors | Placing a limited hedge or protection budget by forward exposure rather than last year's loss (bank asset-liability hedging after the 2023 regional-bank failures, insurers' duration overlays, corporate treasuries hedging fixed-rate assets), where the assets that lost most are the ones about to run off |
| Decision shape | Which of N gets one scarce thing: the $1.2 billion pay-fixed overlay, designated against one of five pools |
| Committed call | The pool the overlay is designated against, and the measure the hedge policy ranks it on, in $ millions to one decimal |
| Gap · Pattern | Gap 1 (time) over Gap 4 (rule) · Pattern A (past exceedance against forward yield, with the moderator in how the forward period's rates treat each loan), with a mixed segment split through a join (measured #6) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #7 uses the ready-made measure · #6 treats a mixed segment all one way · #13 validates on one population, applies to another |
| Calibration form | Published control set with a reproduction clause: ALCO's 40 certified pool-quarter figures since 2024, and the policy clause that a forward-loss method must reproduce every one |
| Driving force | The policy ranks pools on their +200 bp economic-value loss averaged over the swap's first twelve months, so what counts is how much exposure stays on the book through the year. The 2023–24 mortgages carry 7.25% notes; last year, with rates rising, they prepaid at 5%, but against the planning rate of 6.25% they are in the money and the certified record prices them at 35% a year. The Treasury ladder that lost most last year matures by a third. The commercial real estate loans, locked by yield maintenance, lose almost nothing to runoff, and they rank fourth on last year's loss. |

## 1. Situation

A regional bank's ALCO approved one $1.2 billion, four-year pay-fixed swap overlay, to be designated as a hedge against one of five
fixed-rate pools: a Treasury ladder, agency mortgage-backed securities, 2023–24 residential mortgages, auto loans, and fixed-rate
commercial real estate loans. The hedge policy designates it against the eligible pool whose +200 bp loss in economic value, averaged
over the swap's first twelve months, is largest. ALCO certifies each pool's figure on that measure every quarter, and the policy allows a
method only if it reproduces every certified figure. The quarterly ALM report leads with each pool's trailing-year loss in economic value.
The designation memo is due on the 14th.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the ALM report's trailing losses, the static sensitivities, the loan tapes, the pledge register,
  ALCO's planning rate path and the certified figures. The report labels its headline in-file as a statement about the last four quarters.
  No stakeholder's reading of their own numbers is overturned; the ladder did lose most. The difficulty is ranking on exposure that has
  not yet run off.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the treasurer's view, every voice and the report's headline. The static sensitivity, the natural forward
  measure, still ranks the mortgage pool first after the eligibility split.
* **Instrument repair.** Make every pool's valuation perfect. The trailing losses and static sensitivities are already exact; the forward
  year's runoff, set by each loan's incentive against rates that have not yet come, is not something a better instrument of the past shows.
* **Lens swap.** The naive read and the answer weigh different moments: what each pool lost over the last four quarters, or holds today,
  against what it will still hold, and at what duration, through the swap's first year.

## 3. The driving force

A strong solver sets the report's trailing losses aside as backward-looking, computes each pool's static +200 bp loss from balances and
effective durations, applies the policy's exclusion of pledged securities, and ranks. Every step is correct and the mortgage pool leads.
The policy's measure, though, averages the loss over the year, so it depends on what each pool still holds month by month. The ladder
matures by a third and pulls towards par. The 2023–24 mortgages are the subtle case: last year, with rates rising past their notes, they
prepaid at 5% a year, the speed the static duration assumes. ALCO's planning rate for the coming year is 6.25%, so a 7.25% note is a
point in the money, and every certified pool-quarter with that incentive shows prepayment near 35% a year. The commercial real estate
loans are locked by yield maintenance, amortise slowly and keep almost all their exposure. Ranked on the year, the pool fourth on last
year's loss comes first.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The ALM report's trailing-year loss in economic value | A, Treasury ladder ($403M; 1.55× the runner-up) | The bank's own headline risk number, and the ladder really did lose most | The report's in-file label: the figure describes the last four quarters, and the policy ranks the next twelve months |
| 1 | Static +200 bp loss: balance × effective duration × 2% | B, agency MBS ($600M; 1.70×) | The textbook forward measure, the one the regulator sees | The hedge policy excludes pledged positions, and the pledge register shows 70% of the MBS pledged to the home loan bank |
| 2 | Static loss on eligible positions only | C, 2023–24 mortgages ($352M; 1.47×) | Eligibility applied record by record through the pledge register | The certified figures: a static or trailing-speed runoff misses every pool-quarter with an in-the-money incentive |
| 3 | **Decisive:** the +200 bp loss averaged over the swap's first year, with maturities, amortisation and prepayment by each loan's incentive against the planning rate, as the certified figures reproduce | **E, commercial real estate loans** ($221.9M; 4th of 5 on rung 0) | — | — |

* **Position table.** The real estate pool ranks 4th on rung 0, 3rd on rung 1 and 2nd on rung 2 (1.47× behind the mortgages), and leads
  only rung 3, by 1.27× over the MBS. Rung leaders beat their runners-up by 1.55×, 1.70×, 1.47× and 1.27×.
* **Discriminator dominance.** The mortgage pool carries a 1.47× advantage into rung 3 ($352M against $239M). The year's runoff keeps 48%
  of the mortgages' static loss ($168M) and 93% of the real estate loans' ($221.9M), an edge of 1.95× against the 1.76× that 1.2 × 1.47
  requires. The product, (1/1.47) × 1.95 = 1.32×, is the real estate loans' margin over the mortgages.
* **Partial correction priced (L3).** A solver who runs off every pool at its trailing-year speed treats the mortgages as if rates were
  still rising and keeps them first ($311M). One who applies the incentive curve but forgets that the ladder's remaining bonds shorten as
  they pull to par names the ladder second and the mortgages still first.
* **Grid.** Measure (trailing loss, static, year-average) × eligibility (as labelled, pledged excluded) × prepayment (static, trailing speed,
  incentive) = 12 feasible cells. Every cell without the incentive-driven year average names the ladder, the MBS or the mortgages; only the
  year average with eligibility and incentive names the real estate loans.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy states the measure and the reproduction condition; no document gives a prepayment curve, mentions
   refinancing incentives, or says how certified figures were built.
2. **Reproduction (Pattern B).** Incentive-driven runoff reproduces 40 of 40 certified pool-quarters to $0.1M; trailing-speed runoff 28 of
   40, missing every pool-quarter with an in-the-money incentive, all on the high side; static exposure 19. The rule is a construction, not
   a menu: each loan's incentive is its note rate against the period's planning rate, joined from the tape to ALCO's path, bucketed, and
   carried through a month-by-month runoff.
3. **No arithmetic symptom.** Balances tie to the general ledger, durations to the ALM model, the pledge register to custody, and the
   static and trailing figures reproduce the report exactly.
4. **Not a row predicate.** The year average needs a monthly projection of every pool under maturities, amortisation and incentive-driven
   prepayment, then a loss at each month.
5. **The enumeration is arithmetic.** No column says "in the money"; incentives are computed against a rate path in another document.
6. **No cutover date.** No outcome series steps; the mortgages' speed changes because the forward period's rate sits below their notes,
   a relation, not an event.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** ALCO's certified year-average +200 bp losses for each of the five pools in each of the eight quarters since 2024, with each
  quarter's planning rate path, and the policy's reproduction clause.
* **What it certifies.** The duration model and the maturity runoff, which reproduce every certified figure for the ladder and the auto
  loans.
* **What it pins.** Prepayment by incentive bucket: near 5% a year below par, about 35% a year at a point in the money, unique on the 40
  figures.
* **Twin pair.** Two certifications carry identical tape statistics (balance, note distribution, effective duration and trailing speed):
  the 2023–24 mortgage pool at 2026Q2 and the bank's 2022 purchased-mortgage pool at 2024Q2. Their certified year-average losses are
  $168M and $331M (1.97× apart), because the 2024Q2 planning rate (7.5%) left those notes out of the money and the 2026Q2 rate (6.25%) put
  them in. Only incentive-driven runoff reproduces both.
* **Resemblance points at the decoy.** By tape and trailing speed, the mortgage pool most resembles its own 2025 certifications, in which it
  ranked first.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The hedge policy: the overlay is designated against the eligible pool whose +200 bp loss in economic value, averaged over
  the swap's first twelve months, is largest; positions pledged as collateral are hedged within the borrowing programme and are not
  eligible; a forward-loss method may be used only if it reproduces every certified figure. ALCO's planning rate path is the bank's base
  case.
* **Empirical pins.** The incentive curve, from the certified figures. Maturities and amortisation, from the tapes.
* **Voices.** The treasurer: "The ladder took the biggest hit last year; that's where the hedge belongs." The ALM analyst: "Nothing on the
  balance sheet carries more duration than the mortgage book." The head of commercial real estate: "Our loans are locked. There's no rate
  risk in them to speak of."
* **Licensed wrong basis.** The policy records that the bank's examiners review interest-rate risk on the static +200 bp sensitivity and
  will see the designation against it.

## 8. Determinism by construction

* **Rate path.** ALCO's planning path is flat at 6.25% for mortgages through the swap's first year, so no path-shape choice arises.
* **Incentive buckets.** No loan's note sits within 10 bp of a bucket edge, so 25 bp and 50 bp bucketings assign every loan alike.
* **Averaging.** Monthly and quarterly averaging over the year agree within 0.4% for every pool.
* **Eligibility.** The pledge register is dated the designation date; no position is pledged or released within a week of it.
* **Rounding.** The real estate pool's figure ($221.9M) sits mid-way within its $0.1M bin.

## 9. Prompt sketch and deliverables

> ALCO approved one $1.2 billion pay-fixed overlay this year, and on the 14th I designate it against one of our five fixed-rate pools. The
> treasurer says the Treasury ladder took the biggest hit last year, so that is where it belongs. Name the pool, with the figure that puts it
> first in $ millions to one decimal, in a sentence I can put in the designation memo, and send `overlay_designation.xlsx` with the build and
> the sheets below, a chart `pool_exposure_path.png`, and a one-page `designation_memo.pdf`.

* `overlay_designation.xlsx` — each pool's measures and monthly projection, the margin sheet (ask A) and the delinquency sheet (ask B).
* `pool_exposure_path.png` — each pool's +200 bp loss month by month over the swap's first year as lines, with the year averages as
  labelled markers, last year's trailing loss as a hollow marker at the left edge, the pledged MBS shown separately, and the designated pool
  highlighted.
* `designation_memo.pdf` — the designated pool, its figure, and why each of the other four is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the five pools and each of the last four quarters, net interest income. *Device:*
  deferred origination fees and costs are amortised into yield through a separate fee-amortisation ledger, as the accounting policy
  documents; reading the coupon ledger alone misstates income for the three loan pools. Income enters no part of the loss projection.
* **Ask B (device-carried).** For each pool and quarter-end, positions 30 or more days past due, by count and balance. *Device:* loans in a
  payment-deferral programme are reported current by the servicer, with the deferral in the forbearance table, as the servicing guide
  documents; reading the servicer status alone understates delinquency in two pools. No deferred loan sits in the mortgage or real estate
  pools.
* **Ask C (validity).** Each pool's rank under each of the four rung constructions, and how many certified pool-quarters each construction
  reproduces.
* **Decoupling.** Clearing the incentive runoff changes no figure in asks A or B.

## 11. Rubric arithmetic

5 pools × 4 quarters (ask A) + 5 × 4 × 2 (ask B) + 5 pools × 4 constructions (ask C) + the committed pool, its figure and its margin + 5
named chart parts + 3 files ≈ 91 criteria.

## 12. World-building constraints

* Trailing-year loss ($M): ladder 403, MBS 260, mortgages 95, real estate 70, auto 40. Static +200 bp loss ($M): MBS 600 (180 eligible),
  mortgages 352, real estate 239, ladder 208, auto 56.
* Year-average loss ($M): real estate 221.9, MBS (eligible) 175, mortgages 168, ladder 139, auto 30. Mortgages with trailing-speed runoff
  311.
* Mortgage notes 7.00–7.50%; planning rate 6.25%; incentive CPR about 35% at a point in the money, 5% below par.
* Certified figures: 40 pool-quarters; reproduction 40 / 28 / 19 as above.
* The twin certifications are identical on every tape statistic.
* Fee amortisation and payment deferrals touch no balance, duration or prepayment in the projection.
