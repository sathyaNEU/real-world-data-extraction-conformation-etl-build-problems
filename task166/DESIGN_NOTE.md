# task166 design note

Architecture 1, drawn 2026-10-18 (wave 7, the first of the wave, Forecasting lane, sathya8571), numbered from seed
FC37. The seed (a regional bank's ALCO designating one $1.2 billion, four-year pay-fixed swap overlay against one of
five fixed-rate pools, ranked by the hedge policy on the +200 bp loss in economic value averaged over the swap's first
twelve months, with the September planning cycle's base-case mortgage rate at 6.25 per cent) was read at its header
and Situation only. Its world, decision and quantity are kept. Its two decoy-era devices are not shipped: no policy
clause makes a forward-loss method conditional on reproducing a model validation control set, and no ALM report ranks
the pools on their trailing-year loss. The pitfall is re-found from how each pool's balance will run off under the
planning cycle's base case.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task166.json`, architecture v1, registered 2026-10-18. `guard.py check`
   WARN, answered below.
2. Pairing: Banking, Credit & Financial Risk (client domain) / `stress-testing-capital` / Forecasting & Predictive
   Modeling. The seed's house label was Economics (bank balance-sheet risk management); the domains README files
   lending and bank risk under Banking, never Economics ("Economics is macro, labour, trade and fiscal reads, never
   corporate finance, markets trading or lending"). The deciding quantity is a +200 bp economic value of equity (EVE)
   stress on each pool's expected cash flows through a forward year, which is interest-rate risk in the banking book,
   the rate-stress part of `stress-testing-capital`; the task type serves forecasting, and the forecast that decides
   is each pool's behavioural balance path under the planning cycle's base case.
3. Niche: a Pittsburgh regional bank holding company (about $31 billion of assets) designating its one $1.2 billion
   four-year pay-fixed swap overlay, traded on 15 December 2026 and effective 4 January 2027, against the fixed-rate
   pool whose +200 bp economic value loss averaged over calendar 2027 is largest, when the 2023-24 portfolio jumbo
   mortgages carry rates the planning path's 6.25 per cent now beats and about $2.2 billion of five-year fixed-rate CRE
   loans written in the bank's early-2022 push, at peak values and sized to its minimum cover, fall due inside 2027.
4. Call and shape: the pool the overlay is designated against (`pick_one_of_n`, a named pool, question form which) and
   its +200 bp loss averaged over the twelve month-ends of 2027, in $ millions at the precision every defensible
   construction shares (set at stage 2 from the measured spread). Shape `other`: the call with its critical
   components and decoupled ask tables in a workbook, and a two-slide ALCO deck; the criteria are counted in
   `## Ask sheet`.
5. Mechanism keys: gap time (the maturity record is a statement about due dates whose loans could carry a new loan;
   the decision bets on a wall whose loans mostly cannot) with population (which loans are still in each pool through
   the year); decisive pattern E (the share of due balloons that stays, conditioned on each loan's refinance cover, an
   absolute split no column names), then G13 (the year holds the wall) and G6 (the wall's mix on cover differs from
   every closed year's); Gate G `forecasting`; strategy `composition_mix` (a recent or pooled extension share does not
   apply to a wall whose mix on refinance cover differs from the measurement corpus).
6. Layer 2: `forecast_uncertainty` (the conditioning chosen on held-out maturities), pattern
   `own:balloon-maturities-extended-by-refinance-cover`. Banking has no library patterns
   (`layer2-rigor-patterns.md`); the pattern is built from the client's family (model choice on out-of-sample error)
   and the field's own refinance test.
7. Furniture: forum `committee_or_panel` (ALCO approved the overlay at its November meeting; the designation memo goes
   to ALCO's chair before the trade); forcing event `purchase_order_or_contract` (hedge designation must be documented
   at the swap's inception, so the memo is due on Monday 14 December, the day before the trade); organisation family
   `financial_institution`; role family `portfolio_manager` (the head of balance sheet management, who runs the bank's
   interest-rate risk position and its hedge programme); context artifact `close_out_summary` (the third-quarter ALM
   report: the bank's quarter-end EVE and earnings-at-risk position at balance-sheet level, which ranks no pool);
   calibration `existing_book_actuals` (the bank's own loan-level prepayment history and its CRE maturity log with
   every outcome since 2015).
8. Spine: the servicing system's monthly loan-level extract for the 2023-24 portfolio mortgages (loan by month,
   January 2023 to November 2026, about 160,000 rows, two layouts across the 2024 servicing platform conversion);
   constructed in the layout of a mortgage servicing system's monthly extract. Other files are listed at stage 3.
9. Deliverables: `overlay_designation_2027.xlsx` (the call, its components and the ask tables) and
   `overlay_designation_alco.pptx` (two slides for ALCO); the format set xlsx and pptx is in none of the last three
   builds.
10. People, drawn with `guard.py names --geo "United States" --seed 166`: Guy Morrison, Sheri Roberts, Cody Li, Jeff
    Guzman, Joshua Boyd (roles assigned at stage 3; no persona in the prompt). Invented names: Carrick Valley Bancorp
    and Carrick Valley Bank (a web search found no bank or bancorp of that name; Carrick is a Pittsburgh
    neighbourhood); counterparty and system names are left generic or checked the same way when the pack is cut.

**Data-native sentence.** Carrick Valley's records show every pool's monthly balance and every CRE maturity's outcome,
so nothing is hidden: but the 2023-24 mortgages hold rates the planning path now beats, so they will leave faster
than their own trailing year, while the fixed-rate CRE pool's 2027 balloons were written in the bank's push of
December 2021 to June 2022 at peak values and sized to its 1.25 cover minimum, and their properties' income has
slipped since, so at the planning cycle's CRE rate most of them cannot carry a new loan of their balloon balance and
will be extended for 36 months at their note rates, as the maturity log shows for every loan at that cover since 2023,
while the 2026 maturities, written at the 2021 lows with cover to spare, mostly refinanced and leave the recent
extension share low.

**Guard and similarity.** `guard.py check` WARN at registration, one line: `repeat.question_form` (which, against
task245 and task471): the decision is a pick of one pool, so the form is the decision's own. The structural
signatures (gap time, pattern E, Gate G forecasting; and with `pick_one_of_n`) repeat older builds only and carry a
differentiation line each on the card (task37 v2, task44 v2, task97 v5, task117, task137 v1 and its round-1
lineage, task155, task197). The ban window at registration held task163, task245 and task471; nothing on the card
repeats an axis of theirs.

**Abstraction test.** Stripped of nouns: two parts of a stock answer the same forward terms in opposite directions,
one leaving faster than its own past because its units' rates are beaten by the terms, the other keeping every due
unit whose own earnings no longer cover the terms it would roll onto; the part with the most exposure over the
window is found only when both answers are projected. Read against the nearest by structure:
- task137 v1 conditions a renewal share at maturity on the gap between the locked rate and the card; that is this
  build's lower rung for the mortgages (prepayment by incentive, the field's textbook curve, a reused device), and it
  is the losing rival for the CRE wall: the 2027 balloons' rate gaps are no wider than those of the 2026 maturities
  that refinanced, and what keeps them is each property's income against a new loan's debt service at the planning
  rate, joined from the operating statements. task137's current architecture rebuilds a class from entry data; no
  class is rebuilt here.
- task155 and task97 condition a take-up or repeat rate on a covariate the history carries in another form; here the
  conditioned share decides a value-sensitivity ranking only together with another pool's opposite run-off.
- task134 v2 (a hazard by time since entry) and task157 (a returning wave's leading edge) share no structure: no age
  clock and no leading edge decide.
None shares the latent structure, the default path and the correction together.

**Sources, one line each.**
- Seed FC37 header and Situation (`status.py task166`): the world, the five pools, the overlay, the policy measure and
  the 6.25 per cent planning rate; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting` (76 builds): behaviour at a maturity conditioned on a rate gap
  (task137 v1) and on a class of money (task137), hazards by time since entry (task134 v2), leading edges (task157),
  stepped payouts from a resampled distribution (task151), delayed entry (task133), a conversion yield read against
  untreated states (task163); none projects a balance sheet's pools through a forward year on their own behaviour.
- `stumping/references/client/two-layer-task-design.md`: the client's example of validating a forecast on data it was
  not built on (the extension model chosen on held-out maturities, the rivals rejected there).
- `stumping/references/strategies.md` F5 (the conditioning property rebuilt from a history, one band moving against
  the rest) and F6 (the natural fit fails forward because the rate is stationary only in a constructed quantity).
- `dataset-generation/references/layer1-messiness.md`, Banking 1 (monthly loan tapes with status transitions) and 8
  (rates on different bases and day counts), with the universal techniques for the servicing conversion and the
  custodian's securities layout.

## Tried and rejected

- The mortgages' prepayment by refinancing incentive as the decisive step (the brief's first idea), worked at the
  draw: an incentive curve fitted to the bank's own loan history is the field's textbook construction and the strong
  solver's reflex, and as a decisive step it is task137 v1's driver (a behavioural share stable only per unit of the
  rate gap) in mortgage nouns; kept as the default path's own correction, the rung that moves the mortgages off the
  call, never as the step that lands it.
- The +200 bp loss with behaviour re-projected under the shock (negative convexity) as the decisive step, prototyped:
  with the policy's swap-curve discounting the in-the-money mortgages' extension under the shock adds value (their
  coupons sit above the shocked curve), so the re-projected loss came out at half the static one (3.1 against 6.2 per
  cent of balance), and with product-rate discounting the scheduled-only and flat-hold routes land on the same pool as
  the golden; the policy files the base-case cash flows, re-discounted.
- Burnout (a pool's response falling with its time already in the money) as the decisive step: the 2023-24 vintage
  has already been through the 2024 and 2025 rate dips, so burnout slows it, which puts the golden on the pool every
  flat-hold route picks; and the latent-depletion structure sits in task137's family.
- Seasoning (a hazard by loan age) as the decisive step: task134 v2's driver, and an age covariate any full model
  carries.
- Eligibility as a forecast (a pool eligible only if its base-case balance stays above the notional to the swap's
  maturity, the portfolio layer method's own test): an eligibility check deciding the call is a backdrop and a
  threshold on a forecast; eligibility is filed as a plain fact on the designation-date balance.
- A first card with the honest keys gap time and pattern E blocked on the older same-puzzle and same-driver
  signatures; the keys were kept (pattern C was the other candidate and does not describe a conditioned share) and
  each older build got a differentiation line on the card.
