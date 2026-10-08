# FC38 — The largest one-time campaign draw the endowment's ten-year rule allows, when the underwater floor binds gift by gift and the recent campaign's gifts sit closest to it

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Nonprofit & Grant-making · endowment management |
| Mirrors | Committing a one-off draw from a pooled fund whose floors bind per contribution (university endowment campaigns, corporate foundation pooled funds, donor-advised fund sponsors, pension plans with per-tranche guarantees) |
| Decision shape | An allocation under a cap: the special campaign draw, as large as the board's ten-year preservation rule allows |
| Committed call | The largest special draw the board can approve, in $ millions to the nearest million |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · S5 (a floor that does not commute: per-gift floors against a pooled spending rule), with validated-on-one-population-applied-to-another (measured #13) at rung 1 |
| Gate G mechanism | binding_constraint, with forecasting support |
| Measured traps engaged | #13 validates on one population, applies to another · #6 treats a mixed segment all one way · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: the custodian's quarterly acknowledgements since 2008, every fund's units by gift lot with each lot's original amount and the distribution acknowledged on it |
| Driving force | The spending policy pays 4.5% of each gift's twelve-quarter average value, and a gift worth less than the amount given distributes nothing. The pool is one unitised account, but each gift is a lot that bought units at its own price, and 38% of the pool's value is lots from the 2021–24 campaign, bought at unit values 40% above 2008's. In a bad path those lots go under water first and stop paying, so the pool keeps more than a pooled rule spends. The 2009–11 acknowledgements show the floor working lot by lot; the realised rate they imply (3.1% in deep drawdowns) was set by a much older lot mix. |

## 1. Situation

A university's $4.0 billion endowment pays out 4.5% a year of each gift's twelve-quarter average value. Its spending policy holds that a
gift worth less than the amount given distributes nothing that quarter, the shortfall staying in the gift. The board will approve a
one-time special draw for the campaign's matching programme at its March meeting, and its preservation rule allows a draw only if, after
it, the tenth-percentile real value ten years on, from historical simulation over every 40-quarter window since 1926 deflated by the
higher-education price index, is at least 85% of today's value. The pack holds the custodian's acknowledgements, the gift register, the
pool's policy-portfolio return history, the price index and the spending policy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the acknowledgements, the gift register, returns, the price index and every past distribution. The
  CFO is right that the endowment grows on average. No reported number is overturned; the difficulty is how much the pool keeps in the
  paths that decide the tenth percentile, which depends on a floor that binds per gift.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CFO's view and every voice. The historical simulation with pooled spending is still the natural build,
  still follows the board's rule to the letter, and still allows a draw less than half the answer.
* **Instrument repair.** Imagine the custodian reporting every gift's value daily. The floor's bite in the simulated bad paths is still a
  property of when each gift bought its units, which the acknowledgements already record exactly.
* **Lens swap.** The naive read and the answer weigh different populations: the 2008 lot mix whose drawdown set the realised 3.1%, against
  today's lots, two fifths of them from a campaign that bought near the top.

## 3. The driving force

A strong solver runs the board's simulation: every 40-quarter window, the policy portfolio's returns, 4.5% of the twelve-quarter average
paid each quarter, the draw taken now, and finds the largest draw that keeps the tenth percentile at 85%. Knowing endowment law, it adds the
underwater floor, testing each fund's value against its historic gift value; or, noticing in the record that the pool spent only 3.1% a
year through 2009–11, it spends less in deep drawdowns. Each step is correct. But the policy's floor is on the gift, and the custodian
holds each gift as a lot with its own price: a fund with an old gift and a campaign gift is two lots, one far above water and one barely
above it. The 2009–11 acknowledgements reproduce only lot by lot. Today two fifths of the pool's value sits in campaign lots that go under
water in any drawdown over 12%, so in exactly the paths that set the tenth percentile, far more of the pool stops paying than in 2009 and
the pool ends larger.

## 4. The ladder

| Rung | Construction | Lands on (largest draw) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Historical simulation as the board specifies, 4.5% paid in every quarter of every path | $95M (−60%) | The rule implemented exactly, on the official return history | The acknowledgements: through 2009–11 the pool distributed 3.1% a year, not 4.5%, because some gifts stopped paying |
| 1 | Pooled spending at 3.1% in quarters when the pool is 20% or more below its high, 4.5% otherwise, as 2009–11 realised | $160M (−33%) | Calibrated on the one deep drawdown in the record, and it reproduces that period's total distribution exactly | The 2009–11 total is a consequence of which gifts were under water then; today's gifts were bought at unit values 40% above 2008's |
| 2 | The floor tested fund by fund: a fund's value against its total historic gift value | $185M (−23%) | The usual reading of the law, applied per fund in every simulated quarter | The 2009–11 acknowledgements: per-fund testing reproduces 1,630 of 2,140 lot-quarter distributions |
| 3 | **Decisive:** the floor tested lot by lot, each gift's units against its own original amount, with today's lots carried through every path | **$240M** | — | — |

* **Figure shape.** Every correction walks the draw up and the decisive rung is the largest step, so the answer is the maximum cell and
  every partial build understates what the board may approve. Rungs 0–2 sit 60%, 33% and 23% below it.
* **Partial correction priced (L3).** A solver who tests lots but spreads each fund's total historic value across its lots pro rata by
  units, instead of using each lot's own amount, lands at $201M (−16%). One who applies the 2009–11 lot-level suspension rates by
  drawdown depth, rather than today's lots, lands at $172M (−28%).
* **Grid.** Spending (pooled, drawdown-conditioned, fund floor, lot floor) × lot values (own amount, pro-rata split) × floor calibration
  (2009–11 suspension rates, today's lots) = 8 feasible cells. Every wrong cell sits at least 16% below $240M; the nearest is the pro-rata
  split, which needs the custodian's lot amounts ignored after the lots themselves were found. The draw is taken at approval, as the rule
  states, so timing is not a toggle.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says a gift worth less than the amount given distributes nothing; it does not say a gift is a lot, and
   the gift register keeps one historic value per fund. Nothing links the floor's grain to the custodian's lots.
2. **Reproduction (Pattern B).** The lot-level floor reproduces all 2,140 lot-quarter distributions the custodian acknowledged in 2009–11;
   the fund-level floor 1,630, every miss an over-payment; pooled spending at the realised rate reproduces the period's total and none of its
   lots. The rule is a construction, not a menu: each lot's value is its units at the quarter's unit price against its own amount, joined
   from the custodian's file, never a fund-level field.
3. **No arithmetic symptom.** Since 2012 no lot has been under water, so every reading reproduces every acknowledged distribution and the
   pool's value to the cent in the record a solver checks first.
4. **Not a row predicate.** In each simulated quarter, each lot's status depends on its path-dependent value against its amount, and the
   pool's spending is a sum over 3,100 lots of floors that do not commute with the pooled rule.
5. **The enumeration is arithmetic.** Which lots stop paying in which paths is computed; no column marks a lot as near its floor.
6. **No cutover date.** The campaign's gifts arrived over four years; nothing steps, and the floor's bite lives only in simulated paths.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The custodian's quarterly acknowledgements since 2008: for every fund, each gift lot's units, purchase date and original
  amount, and the distribution acknowledged on the lot that quarter.
* **What it certifies.** Since 2012, the pooled rule exactly: every lot paid 4.5% of its twelve-quarter average, so rung 0's spending
  reproduces fourteen years of distributions.
* **What it pins.** The floor's grain, from 2009–11 (above), and that a suspended distribution stays in its lot.
* **Twin pair.** The Harlan and Okafor professorship funds were identical at the fund level at 30 June 2008: value, total historic gift
  value, units, school and purpose. Through 2009–10 Harlan distributed $412,000 and Okafor $205,000 (2.0× apart), because Harlan's value was
  one 1997 gift and Okafor's was three gifts, two bought in 2006–07 near the then-high. Only the lot-level floor reproduces both.
* **Resemblance points at the decoy.** The simulation's bad paths most resemble 2008–11, whose realised 3.1% rung 1 transports.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The spending policy: 4.5% a year of each gift's twelve-quarter average value, paid quarterly; a gift worth less than the
  amount given distributes nothing that quarter, and the shortfall stays in the gift. The board's preservation rule: a special draw is
  approved only if the tenth-percentile real value ten years on, by historical simulation over every 40-quarter window since 1926 deflated
  by the higher-education price index, stays at or above 85% of today's value, the draw being taken on approval.
* **Empirical pins.** Each lot's units and original amount, from the custodian's acknowledgements. The floor's grain, from 2009–11.
* **Voices.** The CFO: "At our average return the endowment grows comfortably; we can afford a generous draw." The chair of the
  investment committee: "We lived through 2009. Spending fell to about three percent and we came through." The general counsel: "Under
  the law the test is on the fund; that's how every institution reads it."
* **Licensed wrong basis.** The preservation rule records that the board's auditors review the draw against a projection at the pool's
  average return and will present that projection.

## 8. Determinism by construction

* **Windows.** The rule fixes every 40-quarter window from the third quarter of 1926 and inclusive interpolation for the tenth
  percentile, so the simulation has one result per draw.
* **Draw search.** The tenth percentile falls smoothly with the draw; at $240M it sits at 85.0% and at $241M below it, so bisection and grid
  search agree to the million.
* **Lots.** Every lot's amount is acknowledged to the cent; no two lots of one fund share a purchase date, so lot identity is unambiguous.
* **Testing date.** The policy tests at each quarter-end, the custodian's valuation date, so no intra-quarter convention arises.
* **Price index.** The rule names the deflator; the consumer price index would move the draw by $9M and is not the rule's index.

## 9. Prompt sketch and deliverables

> The board approves a one-time campaign draw from the endowment at its March meeting, and it can be as large as our ten-year rule
> allows. The CFO projects the endowment growing comfortably at its average return. Tell me the largest draw the board can approve, in $
> millions to the nearest million, in a sentence for the board book, and send `campaign_draw.xlsx` with the build and the sheets below, a
> chart `ten_year_paths.png`, and a two-page `draw_note.pdf`.

* `campaign_draw.xlsx` — the simulation and draw search, the purpose sheet (ask A) and the gifts sheet (ask B).
* `ten_year_paths.png` — the tenth, fiftieth and ninetieth percentile real value paths over ten years under pooled spending and under the
  lot-level floor, with the 85% line, the committed draw's tenth-percentile path highlighted, and the share of pool value in paying lots
  shaded beneath.
* `draw_note.pdf` — the committed draw and the readings of the floor the board will hear.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight schools, last fiscal year's distributions by purpose (scholarships,
  professorships, programmes, unrestricted). *Device:* a gift re-designated by a signed amendment distributes to its new purpose from the
  amendment's date, as the gift-agreement register documents; using year-end purposes misattributes distributions at five schools.
  Purposes change no lot's units, amount or value.
* **Ask B (device-carried).** For each school and quarter of last fiscal year, new gifts received, counted by donor commitment. *Device:*
  instalments on a multi-year pledge are booked against the original pledge, as the gift-accounting manual documents; counting each
  instalment as a new gift overcounts at six schools. The simulation uses the custodian's lots, which are unchanged.
* **Ask C (validity).** The largest draw under each of the four rung constructions, and how many 2009–11 lot-quarter distributions each
  reproduces.
* **Decoupling.** Clearing the lot-level floor changes no figure in asks A or B.

## 11. Rubric arithmetic

8 schools × 4 purposes (ask A) + 8 × 4 quarters (ask B) + 4 constructions × 2 (ask C) + the committed draw, the tenth-percentile value at it
and the campaign lots' share of value + 5 named chart parts + 3 files ≈ 83 criteria.

## 12. World-building constraints

* Pool $4.0B in 3,100 lots across 1,240 funds; campaign lots (2021–24) hold 38% of value at unit prices 40% above 2008's and go under
  water in any drawdown over 12%.
* Draws: $95M / $160M / $185M / $240M; pro-rata lot values $201M; 2009–11 suspension rates by depth $172M.
* 2009–11: realised spending 3.1% a year; 2,140 lot-quarter distributions; fund-level floor reproduces 1,630. No lot under water since 2012.
* The twin funds are identical on every fund-level column at 30 June 2008.
* Purpose amendments and pledge instalments touch no lot, unit or amount.
