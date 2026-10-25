# task166 design note

Architecture 2, drawn 2026-10-25 (wave 7 slot, Forecasting lane, sathya8571), a re-root after portal round 1. Architecture 1
(a regional bank's ALCO designating a swap overlay against one of five fixed-rate pools, seed FC37) was landed by both
portal responses on its golden: conditioning each commercial real estate balloon's extension on refinance cover at the
planning rate is a reflex for the portal's models, and both responses also fitted the mortgages' prepayment on their own
rate incentive, the textbook curve. Its identity is in the card's lineage and its dead ends below. Nothing of the seed or of
architecture 1's world is kept: this draw is a credit union's fixed-rate home equity book, and the reflex the portal's
models showed (a prepayment curve on each loan's own rate incentive) is what this draw makes wrong.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task166.json`, architecture v2, registered 2026-10-25T17:31:36Z, v1 in its
   lineage. `guard.py check` on the registered card: WARN, `repeat.question_form` only, answered below.
2. Pairing: Banking, Credit & Financial Risk (client domain) / `deposit-liquidity-behaviour` / Forecasting & Predictive
   Modeling. The client taxonomy files prepayment behaviour with deposit behaviour under this task type (its rigor group
   is deposit-prepayment-interest-rate-behavior, whose fourth card is a prepayment S-curve fitted pooled across pools),
   and the task type serves forecasting. The deciding quantity is each region's 2027 home equity loan payoffs under the
   planning cycle's base-case rates, a prepayment forecast.
3. Niche: a West Michigan credit union (about $4 billion of assets; regional lending centers in Grand Rapids, the
   Lakeshore, Kalamazoo and Battle Creek, and Muskegon and the north) whose lending committee opens a payoff-retention
   pilot (a dedicated mortgage loan officer and outreach to home equity members before they pay off) in one region on
   Monday 4 January 2027, the region whose members will pay off the most home equity loan principal in 2027. The
   fixed-rate home equity book (closed-end seconds, 10 to 20 year terms) grew fastest in the 2024 to 2026 equity-tap boom,
   when members kept 2020 and 2021 first mortgages at 2.5 to 3.5 per cent and borrowed against their equity at 8.25 to
   9.25 per cent; the newer suburbs' loans sit behind 2025 and 2026 purchase mortgages at 6.25 to 7.25 per cent. Both
   kinds of first mortgage are mostly held at other lenders.
4. Call and shape: the region (`pick_one_of_n`, a named region of four, question form which) and the home equity loan
   principal its members will pay off in 2027 (payoffs and curtailments, $ millions, rounding fixed at stage 2 from the
   family spread). Shape `other`: the call with its critical components and a decoupled ask layer; the criteria are
   counted in `## Ask sheet` at stage 2.
5. Mechanism keys: gap population (what drives one loan's exit), decisive pattern E (each loan's payoff conditioned on the
   senior mortgage's refinance incentive, an absolute split no column names) with G6 (the forward book's mix on that
   property differs from every closed year's: the record's high-rate seconds sat behind high-rate firsts, the forward
   book's mostly do not); Gate G `method_or_model_selection` (stumping 1.4 maps the population gap there: the record
   selects the senior-lien payoff model over the own-rate model on the loans whose two incentives diverged); strategy
   `composition_mix`.
6. Layer 2: `field_method`, pattern `own:junior-lien-payoffs-set-by-the-senior-mortgages-refinance-incentive`. The
   client's banking rigor cards carry the own-rate S-curve as the textbook route (deposit-prepayment card 4, pooled across
   pools); the field's method for a junior lien is to model its exits on the senior mortgage's incentive and lock-in.
7. Furniture: forum `committee_or_panel` (the credit union's management lending committee chooses the pilot region at
   its December meeting); forcing event `launch_or_rollout` (the pilot opens in one region on 4 January 2027); organisation
   family `financial_institution` (a member-owned depository institution); role family `finance_controller` (the lending
   analytics manager, who prepares the regional payoff forecast); context artifact `close_out_summary` (the third-quarter
   ALM report: the balance sheet, net economic value and the home equity book's size, ranking no region); calibration
   `existing_book_actuals` (the credit union's own payoff history and its semiannual bureau refreshes since 2019).
8. Spine: the new core system's monthly home equity loan extract (loan by month, September 2024 to November 2026, beside
   the legacy core's extract for January 2019 to August 2024); constructed in the layout of a credit union core's loan
   extract. The forcing file is the bureau refresh: the semiannual account-management soft pull of each home equity
   member's mortgage tradelines (the first mortgage's open date, original amount, balance, scheduled payment and terms,
   and the credit union's own home equity tradeline), two layouts across a 2023 bureau change. Other files at stage 3.
9. Deliverables: fixed at stage 2 (a workbook with the call, the regional forecast and the asks, and one visual the
   lending committee reads); the format set is checked against the last three builds then.
10. People, drawn with `guard.py names --geo "United States" --seed 166`: Sherri Bautista, Brandon Coffey, Joel Singh,
    Cody Li (roles at stage 3; no persona in the prompt). The credit union's name is invented at stage 3 and checked
    against real credit unions (H21); West Michigan already holds real credit unions with lake and lakeshore names, so the
    name avoids both words.

**Data-native sentence.** A closed-end second is paid off almost only at the closing of something that happens to the
first mortgage ahead of it, a refinance (which takes the second with it about three times in five, the rest subordinated)
or a sale, so its exits follow the first mortgage's rate against the market and not its own; the credit union's payoff
record since 2019 supports a curve on each loan's own rate because the loans written at high rates then sat behind
high-rate firsts (the 2018 and 2019 seconds in the 2020 wave, the 2023 purchase seconds in the 2025 and 2026 dips), but
the 2024 to 2026 boom put high-rate seconds behind 2020 and 2021 firsts that no planning rate brings into the money, and
the first mortgages' rates sit at other lenders, recovered only from the bureau refresh's tradelines.

**Guard and similarity.** `guard.py check` WARN on the registered card, one line: `repeat.question_form` (which, against
task485): the decision is a pick of one region, so the form is the decision's own. The structural signatures (gap
population, pattern E, `pick_one_of_n`; and with `method_or_model_selection`) repeat older builds only and carry a
differentiation line each on the card (task228, task268, task28, task30, task32, task53, task167, task31, task448,
task471, task500, task57, task69, task76). A plain run-off figure for the plan (the first framing, `quantity_figure`)
repeats task170 v5's gap, pattern and decision type inside the batch; the pilot region is the decision the payoff forecast
serves, so the decision type follows it. `ban.forcing_event` blocked `budget_or_appropriation` (task301) and `ban.forum`
blocked `executive_team` (task301) and `line_manager_or_team` (task302); the committee and the launch are the honest
furniture of a pilot a lending committee places. Nearest driver 0.05 (task137 v1).

**Abstraction test.** Stripped of nouns: a junior unit leaves when the senior unit ahead of it is replaced or the whole
stack is sold, so its exits follow the senior's incentive and lock-in, a rate set by another holder; the junior's own
incentive, every reflex's covariate, met the senior's in the record and parts from it in the forward book. Read against
the nearest by structure:
- task137 v1 conditions a renewal share at maturity on the gap between the locked rate and the posted rate, a unit's own
  rate gap; here the unit's own rate gap is the losing rival, and the rate that decides is another lender's.
- task500 v2 (lineage) reads a spillover on untouched units through a link in another entity's register; here no causal
  spillover is estimated, a junior lien is retired by its own senior's refinance or sale.
- task28 v1 (lineage) and task32 v1 (lineage) condition a volume or a yield on a property recovered through a join; here
  the property is a rate no file states, recovered from a third party's summary of another lender's account by an
  amortization solve (or read near enough from the first mortgage's open month against the rate sheet archive).
- Architecture 1 of this slot conditioned a maturity's extension on the property's own refinance cover; no maturity, no
  cover and no extension decide here.
None shares the latent structure, the default path and the correction together.

**Sources, one line each.**
- `guard.py recent`, `coverage`, `mechanisms --objective forecasting` (90 builds) and `slots` on the mechanism's nouns
  (second lien, first lien, subordination, tradeline, bureau, home equity, piggyback, refinance) and the setting's: no
  slot note or card spends a junior lien's exit on its senior mortgage.
- `stumping/references/client/layer2-rigor-patterns.md`, deposit-prepayment-interest-rate-behavior: the client's own
  shortcut is one incentive S-curve fitted pooled (card 4); the textbook route a strong solver takes is the own-rate curve.
- `stumping/SKILL.md` Part 6 (the forcing file first: the bureau refresh is the only file that sees the first mortgage)
  and `references/client/measured-drivers.md` (held tasks whose missing dimension lives on another entity).
- `dataset-generation/references/layer1-messiness.md`, Banking 1 (monthly loan tapes with status transitions) and the
  universal techniques for a core conversion and a vendor's layout change.

## Three rules

Task type: deposit-liquidity-behaviour (Banking, Credit & Financial Risk: prepayment behaviour, the client's rigor group deposit-prepayment-interest-rate-behavior), which serves Forecasting & Predictive Modeling in the taxonomy; the decisive forecast is each region's 2027 home equity loan payoffs under the planning cycle's base-case rates.
Domain test: the deciding quantity is each region's 2027 home equity payoffs, which prepayment modeling forecasts from the refinancing incentive and lock-in of the first mortgage ahead of each closed-end second, because a member refinances or sells on the first and the second is paid off at that closing (or subordinated to the new first); the first mortgage's rate is recovered from the bureau tradeline's payment, balance and term by the amortization identity.
Swap: "which district opens the retention pilot, by the follow-up visits its patients will cancel next year" keeps a regional pick on a forecast count of exits, but loses a junior claim that leaves only when the senior claim ahead of it is refinanced or the collateral is sold, a refinancing incentive measured on a rate another lender holds, and lock-in by a below-market first mortgage: with clinic visits nothing sits behind anything, so the quantity the call turns on stops making sense.
Layer 1: the core conversion (the legacy extract to August 2024 and the new core's from September 2024, different layouts and codes, loan numbers through the conversion xref), the bureau's layout change in 2023 (fixed-width segments to a delimited file, Metro 2 style status codes, MMYYYY open dates, whole-dollar amounts), joint borrowers whose shared tradelines appear once per consumer, servicers that report the mortgage payment with escrow, the credit union's own home equity tradeline among the member's tradelines, the credit union's own first mortgages in a separate servicing file, the weekly rate sheet archive with mid-week re-prices, payoff and curtailment codes, internal refinances that close a home equity loan into a credit union first mortgage, and region from the collateral's county; each is how its system writes, none carries the call (each asserted neutral in checks.py at stage 3).
Layer 2: field_method (a junior lien's prepayment modeled on the senior lien it sits behind): the choice that flips the call is forecasting each home equity loan's payoff from its first mortgage's refinancing incentive and lock-in under the planning path, selected by the record on the loans whose own and senior incentives diverged, not from the loan's own note rate against the posted home equity rate.
Decisive step: recover each home equity member's first-mortgage rate from the bureau refresh's tradeline (the payment, the original amount and the term, or the open month against the rate sheet archive), estimate the home equity loan's monthly payoff hazard by that first mortgage's incentive against the posted 30-year rate on every loan-month since 2019, and apply it under the planning path to the loans on the books at 30 November 2026, summed by region.
Not semantics: every field is read correctly on the default path (the conversion, the codes, the payoffs, the posted rates, the tradelines); a prepayment curve on each loan's own rate incentive is the textbook construction, it fits the 2019 to 2026 payoffs, and it is still the wrong forecast for a book whose high-rate loans now sit mostly behind low-rate first mortgages.
Not rule application: no filed rule forecasts a payoff; the credit union's policy files the estimand (the loans on the books at the as-of, payoffs and curtailments, calendar 2027, the planning path, $ millions, the region of the collateral) and nothing about behaviour, and executing every filed rule with any own-rate prepayment model names Grand Rapids; the enumerated and standing families' spreads on the graded figure are measured at stage 2 and entered here.
Analyst test: a strong analyst who joins the two cores, reads every field and fits the home equity payoffs on their own rate incentive against the posted home equity rate (validated on 2019 to 2026) names Grand Rapids, whose 2024 to 2026 loans the planning path puts in the money on their own notes; a trailing payoff rate names Kalamazoo and Battle Creek, whose 2023 purchase seconds paid off in the 2025 and 2026 dips; only reading each loan's payoff off its first mortgage's incentive names the Lakeshore (executed in checks.py on the generator's clean truth at stage 3).
Estimand: the credit union's ALM and lending policy (section to be fixed at stage 2, a shipped PDF) files the population (fixed-rate home equity loans on the books at the close of 30 November 2026, loans opened after it excluded), the outcome (principal paid ahead of schedule: payoffs and curtailments, charge-offs excluded), the window (1 January to 31 December 2027), the unit ($ millions), the region (the county of the collateral) and the rate path (the planning cycle's base case); the prompt adds the pilot's start and the rounding.
No decoy: no memo, draft, ranking, vendor speed table, model output or stakeholder figure argues for any region or any behaviour; the third-quarter ALM report states the book's size and the credit union's position and ranks no region; nothing is copied, backfilled or withheld.
No certified replay: no shipped figure is to be reproduced to recover a method; the payoff record and the bureau refreshes are closed outcomes every route reads alike.
Lesson: a model learns that a junior lien's run-off is set by the mortgage ahead of it, refinanced or sold on that mortgage's rate against the market, so a prepayment curve on the loan's own note puts a refinance wave's exits on the wrong loans once the book's junior and senior rates part; no build on file conditions one claim's exit on another claim's rate.

## Default path
1. Read the lending policy's estimand: the fixed-rate home equity loans on the books at 30 November 2026, their 2027
   payoffs and curtailments under the planning cycle's base-case rates, by the region of the collateral.
2. Stack the legacy and new core extracts through the conversion xref into one loan-month history, January 2019 to
   November 2026, with each loan's balance, note rate, scheduled payment, payoff and curtailment.
3. Fit the textbook prepayment curve: each loan-month's payoff probability on the loan's own incentive (its note rate
   less the posted home equity rate for its term a month earlier), with age and seasonality, validated on the 2019 to 2026
   payoffs (the strong analyst's reflex, and the one both portal responses took on architecture 1's mortgages).
4. Run each loan on the books at 30 November 2026 through 2027 on the planning path's posted home equity rate, which falls
   below the 2024 to 2026 notes from the first quarter.
5. Sum by region and pick the largest.

Ends on: Grand Rapids (figure measured at stage 2)
Golden: the Lakeshore (figure measured at stage 2)

## Stump sentence
Fitting the home equity loans' payoffs on their own note rate against the credit union's posted home equity rate names
Grand Rapids; the step that lands it there is reading a second lien's payoff off its own rate, when a member pays off the
second almost only on refinancing or selling on the first mortgage ahead of it, and the planning path's falling rates
reach the Lakeshore's 2025 and 2026 purchase mortgages at 6.25 to 7.25 per cent while Grand Rapids' boom-era seconds sit
behind 2020 and 2021 first mortgages at 2.5 to 3.5 per cent that stay put: a payoff hazard read off each first mortgage's
incentive, its rate recovered from the bureau refresh, names the Lakeshore.

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
- Redfern Capital Markets as a dealer's name, at stage 3: a letter from a real Florida real estate investor (H21); renamed
  Larkmoor Capital Markets, no figure moved.
- A soft extension response (a logistic scale of 0.05 in cover) with the push's balloons spread across the break, at
  stage 4 round 1: a data-chosen hard cut at 1.18 to 1.20 scored the best hold-out Brier and filed 160 to 161, and a
  constant share of 0.68 to 0.83 on every balloon landed the $150 million bin (0.75 gave 149.3); the $25 million bin
  could not narrow that band. Rebuilt with a sharp break near a cover of 1.10, half the push written as lower-leverage
  refinances, the bin cut to $10 million and the overlay's start filed in the prompt (a spot start would move the
  twelve month-ends and the figure to $160 million).
- Keeping the wall's extension share near four-fifths with a finer bin: the every-balloon guess band still held
  three-quarters, and the later balloons needed to separate the two bands raised the contractual loss and the
  note-rate DSCR rival past R2c's 1.2x margin.
- A $5 million bin: every construction would have to agree within $1.25 million, which no cover mix of the wall held
  against the bands and the debt yield since 2023.
- More seven-year 2021 loans to widen the gap between the two constant-share bands: the note-rate DSCR fitted on 2023
  onward moved into the bin (145 to 148) and R2c past 1.2x.
- Repaying the already-extended loans at their extended date with the practice stated only in the write-up, at stage 4
  round 2: the cover model run on their current maturities gave 156.1 on that pack, so the reading was an open fork;
  the bank's one extension is now filed in the extract notes with its terms, and the second extension (152.7 on this
  book) is asserted as the alternative.
- An extension on the note's rate and payment with nothing paid down (round 1's terms), at stage 4 round 2: no bank
  extends a five-year balloon three years on unchanged terms; the filed terms are a tenth paid down, the posted
  five-year rate on the maturity date and 25-year amortization, and on this book the old terms would file 159.9 (SF21).
- A break at a cover of 1.05: the 1.00 rule came within $7 million of the golden in half the lab draws and the
  bootstrap sigma ran 1.4 to 1.9 in the median draw; at 1.12 the 1.25 convention came within $7 million in most draws;
  the break was set at 1.08.
- A softer extension response (a logistic scale of 0.03 in cover, for a more gradual book): the 1.25 convention moved
  to within $5 million of the golden and, with the break at 1.10, the sigma rose to 1.4; kept at 0.025.
- Interest-only on a third of the push: the bootstrap sigma rose to 1.8 in the median lab draw, the family's plus or
  minus one sigma out of the middle half; interest only for the first 24 months and amortizing after left in-place
  cover too close to refinance cover; half the push interest only for its whole term puts the in-place and watch-list
  routes 72 to 117 below the golden.
- A larger later fixed-rate book (1.5 then 1.0 loans a month after 2022, or a quarter to a third of it on seven- and
  ten-year terms): the balloons-repaid loss rose to $42 to $44 million and the sigma to 1.5 to 1.9 in the median draw,
  the later balloons' extension adding model spread outside the wall; the later book was cut to a handful of five-year
  loans a year, new lending moved to floating rate.
- Total assets held at $31.15 billion: the 2027 wall would be 10.3 per cent of the balance sheet falling due in one
  year; raised to $38.06 billion (8.4 per cent), C&I taking up the rest, the EVE figures unchanged.
- Convenience extensions at high cover (about 1 per cent at any cover, the round 3 recheck's suggestion), at stage 4
  round 4: a logistic has no floor, so a few extensions at covers of 1.5 to 2.5 flattened the fitted scale from 0.023
  to 0.09 and split the family by 15 to 34 million in the lab; dropped, the response has none above a cover of 1.25.
- Softening the shoulder instead (3 per cent of maturities at covers of 1.10 to 1.35 taking the extension): the family
  held in the lab, but in the file-built golden the near-best hard cut at 1.12 left the middle half with one sigma
  (152.0 plus 0.6); dropped.
- Trailing twelve-month statements for the hotels and retail centres maturing in 2020 and 2021, so their decisions read
  the pandemic: a solver who reads only the fiscal-year statements sees those loans extend at covers of 1.5 to 2.3 and
  files 141.1 in the lab; dropped. The pandemic reaches the record through the 2020 statements, so its extensions run
  from 2021, and the 2020 maturities read 2019 statements (52 of 54 repaid).
- Sale extensions whatever the cover (round 2's 1.2 per cent): on the keyed world a sale-pending six months at a cover
  of 0.81 put a non-extension in the wall's densest band and moved the band constructions by 2.5 to 3.1; a sale repays
  the loan only from a property with equity, so a sale extension now needs a cover of 1.0 or more.
- Statements reviewed after a loan's payoff left in the operating statement file: the fiscal-year reading then picked up
  a hotel's collapsed 2020 statement for a loan paid in February 2021 and moved 4.6; the file now closes with the loan's
  credit file at its payoff.
- Keeping the round 2 realization: with one stream through the book, adding hotels or the ramp moved every later loan's
  draws. Each loan now draws from streams keyed by its origination month and place; on that world the round 2
  settings alone fail the middle half (lab spread plus sigma 5.7), and the ramp, the equity rule and the break at 1.10
  together hold it (2.2).
- The break kept at a cover of 1.08 on the keyed world: the 1.00 rule landed (inside the bin by 0.1); moved to 1.10.
- Loans below a cover of 1.0 sent to special assets at their original maturity (the recheck's coherence exceptions): the
  plateau the wall sits on would fall by about 0.07 and the figure by about $5 million, with a fork on how a transfer
  is read; dropped, and the support agreement and interest reserve that make the plateau real are filed instead.
- A deeper push (pro forma rents 19 to 21 per cent over actual) for a tighter family: the spread fell (lab 2.0) but the
  1.00 rule and every 2027 balloon extended landed; kept at 15 per cent.
- More lending after the push (14 to 18 loans a month from May 2022) to lift every 2027 balloon extended further above
  the bin: the near-best cut at 1.12 left the middle half (lab 2.8 to 3.0); kept at 10.
- The support agreement filed with an income condition ("Where the property's net operating income falls short of the
  extension's payments, the extension is granted on the guarantor's support agreement..."), at stage 4 round 4: the
  reader read it as a mild-to-moderate hint and the recheck as the first filed sentence setting income against forward
  debt service, one step from the cover metric; reworded as a blanket practice on every extension, the pin that the
  payments are made as scheduled kept, no figure moved.
- Portal round 1 (2026-10-25): both responses landed the call, Fixed-rate commercial real estate at $150 million, so conditioning each balloon's extension on refinance cover at the planning rate is a reflex for the portal's models, not a decisive step; the stump sentence's step is spent and the build returns to stage 2.
- Architecture 1 re-rooted at the draw of 2026-10-25, its card's identity moved to the v2 card's lineage: the portal's
  models executed every correction the ladder held (the servicing stitch, an incentive curve on the mortgages' own rates,
  the cover-conditioned extension chosen on held-out maturities), so a redesign inside the overlay world would only add a
  rung above a spent one; the new draw makes the own-rate prepayment curve, the reflex both responses showed, the wrong
  route.
- A plain 2027 run-off figure for the plan (the home equity production that would hold the book flat) as architecture 2's
  call, at the draw: `quantity_figure` with gap population and pattern E repeats task170 v5's structural signature inside
  the batch (`guard.py` test.same_puzzle), and the payoff forecast's own decision is where the retention pilot opens, so
  the call is the pilot's region with its payoff figure.
