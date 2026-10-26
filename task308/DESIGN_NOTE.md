# task308: which region's home book takes the 2027 catastrophe layer, and what the layer is worth there

Architecture 2 spent 2026-10-26 at stage 4 round 4 (a reader landed the call; `## Tried and rejected`), re-root at stage 1.

Architecture 2, drawn 2026-10-26 (wave 7, Opportunity Sizing & Decision Support, perssathya). Re-root after
architecture 1 (300 e-bikes for one of five bike-share networks, the rides on record censored by empty stations) was
spent at stage 4. The number's seed (OS10, the bike-share world) is not carried: the world, the decision and the quantity
are new, and about sixty candidates were screened on paper and by call-only probes before this one (`## Tried and
rejected`).

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task308.json`, architecture v2 (v1 in lineage) |
| Pairing | Actuarial Science & Insurance / catastrophe-exposure-accumulation / Opportunity Sizing & Decision Support |
| Niche | which of a UK mutual home insurer's four regional home books takes a 2027 catastrophe excess of loss layer (GBP 15 million excess of 10 million each loss occurrence, one reinstatement at 100 per cent), valued as the expected 2027 recoveries on the region's own 2010 to 2025 storm, flood and freeze events brought to the 2027 book, less the quoted premium and the expected reinstatement premium, when what a claim costs rises with the claims each repair panel firm has to take on at once and one region's book doubled in 2021 while its panel did not grow |
| Call | the region whose book takes the layer, and the layer's 2027 value on each of the four regions, GBP million to one decimal |
| Decision | `pick_one_of_n`, answer unit `named_option` (with its GBP figure) |
| Mechanism | gap objective then time; pattern none (G14 carries the decisive rung); generators G14 (decisive: the cost of a claim conditioned on its event's claims per repair panel firm, read across every event and carried to the event's 2027 scale), G13 (each historical year's events carried forward to the 2027 book and the 2027 panel) |
| Gate G | `binding_constraint`: the repair panel's capacity binds at the 2027 scale and moves the pick off the region the on-levelled losses name |
| Strategy | `binding_constraint`; layer 2 family `field_method`, own pattern: post-event demand surge at the cover year's scale |
| Calibration | none |
| Furniture | forum `board_of_directors` (the mutual's board decides the placement on the head of reinsurance's paper), forcing event `purchase_order_or_contract` (the brokers' quotations are firm until 15 December 2026 and the order must be signed with the lead reinsurer before then for cover from 1 January 2027), organisation `financial_institution` (a mutual home insurer), role `portfolio_manager` (the head of reinsurance writing the placement paper), context artifact `filed_model` (the 2027 business plan workbook the head of reinsurance works from: each region's 2027 policies and the plan's 2027 rebuild cost index, with its version, approval date and preparer; the valuation policy and the event definitions are the governing documents) |
| People | Donna Phillips, Anne Shah, Nicholas Hardy, drawn with `guard.py names --geo uk --seed 308` (Amanda replaced on a persona WARN) |

**Data-native sentence.** A catastrophe's claims are repaired by the region's panel of contractors, and when one event
hands each panel firm a few dozen jobs at once the firms subcontract, materials run short and every repair costs more,
so a claim's cost in the record is the cost at its own event's claims per firm; Pennine's book doubled with the 2021
Calder and Colne transfer while its panel stayed at 30 to 34 firms, so each of its pre-2021 events would put about twice
as many claims on each firm in 2027, and only the cost of a claim read against claims per firm across every region's
events shows what that does to them.

**Guard.** `guard.py check` on the card: PASS, no WARN. The draft's three BLOCKs were cleared on the furniture, not the
design: `test.same_puzzle_older` on (time, G14, pick_one_of_n), where three priors sit, by the honest gap pair (the
reported, on-levelled loss is right and is not what the layer pays at the 2027 scale: objective first); the forum
`committee_or_panel` (barred against task121) by the board, which decides the placement; and the forcing event
`purchase_order_or_contract` (barred against task137 at the draw) by the budget round. At stage 3 (2026-10-26) `heart`
BLOCKed on two axes against task269, the forcing event `budget_or_appropriation` and the context artifact
`filed_standard`, with task137 spent and out of the window. Both were redrawn in the pack, not relabelled: the board paper
now leads with the quotations' expiry and the order to be signed before it (its budget sentence is gone), and the
business plan workbook carries the version, approval and preparer of the filed planning model the head of reinsurance
works from. `heart` PASS after the redraw. Nearest driver 0.10 (task120 v1, lineage), next 0.08.

**Abstraction test.** Stripped of nouns: a past loss carried to a larger book is scaled claim by claim at the cost each
claim carried, when the cost of a claim rises with the claims per unit of a capacity that did not grow with the book;
only cost per claim read against claims per unit of capacity across every past event shows the uplift. Against task303
v2 (a renewal increase priced on claims whose storm days a model must hold out): there the record holds the frequency
the decision needs once the storms are set aside; here every claim's cost is right for its own event and wrong for the
same event at the 2027 scale. Against task130 v4 (a cover paying only events first reported inside a short window):
there the count of past events is the quantity; here the count and the date of every event are given, and the cost of
each claim at a scale no past event of that region reached is the quantity.

**Call-only probes (2026-10-26, the probe pack at scratchpad `s308/probes`, an earlier set of quotations).** Both
isolated probes (sonnet and opus at medium, prompt and pack only) named Severn Vale, at GBP +1.2 and +1.9 million on
that pack's quotations. Both built each year's occurrences with a window dynamic programme over the dates of loss and
on-levelled every claim by its district's policies and the rebuild cost index; neither read the cost of a claim
against its event's size. The probes' window programme split long floods into two occurrences on that pack; storm and
flood claims are now front-loaded on their first days, and the window programme and one period per event agree on
every region and year.

**Sources, one line each.**
- `layer2-rigor-patterns.md`, catastrophe-accumulation-risk #1 (occurrence against aggregate): the layer pays each
  loss occurrence over the retention and the reinstatement caps the year at two limits, so annual totals cannot stand
  in for occurrences; this build's step is not that one, it is the cost of each occurrence at the 2027 scale.
- The catastrophe-modelling literature's post-event loss amplification (demand surge): claim costs rise with an
  event's demands on local repair capacity, modelled as a function of the event's size against that capacity; run here
  on the company's own events, with the capacity the panel firms on record.
- Burning-cost (as-if) pricing of a catastrophe layer: past events re-stated at current exposure and costs, then the
  layer's terms applied; the field's own method, which this build's default path executes faithfully.

## Default path

1. Read the committee's valuation basis, the quotations, the event definitions, the business plan and the claims and
   exposure files; build each region's windstorm, flood and freeze claims into loss occurrences under the hours clause
   (72 hours for a windstorm, 168 for a flood or a freeze), one period from each catastrophe's first loss.
2. Bring every claim to 2027: its district's 2027 policies (the plan's region total spread by the mid-2025 district mix)
   over the year's, and the plan's 2027 rebuild cost index over the index in its month of loss (or of sign-off).
3. Apply the layer to each occurrence, cap each year at two limits, average over 2010 to 2025, and take off the premium
   and the expected reinstatement premium.
Ends on: Severn Vale, GBP 0.0 million (Pennine GBP -0.4 million at the loss-month index, -0.5 at sign-off; every surge read on a catastrophe's size, its claim count or its loss, names Severn Vale too).
Golden: Pennine, GBP 0.1 million (Severn Vale 0.0, Coastal North -0.5, Fenland -0.8).

## Stump sentence

A competent analyst brings every claim to 2027 by its district's policies and the rebuild cost index, adds at most the
surge the field reads on a catastrophe's size, applies the layer to the occurrences the hours clause allows and names
Severn Vale (GBP 0.0 million at the index alone), because the record prices each claim at its own event's claims per
repair panel firm: Pennine's book doubled with the 2021 transfer while its panel stayed at 30 to 34 firms, so its four
pre-2021 freezes, struck at 22.6 to 25.1 claims a firm, would put 44 to 50 claims on each firm in 2027, and the cost of
a claim read against claims per firm across every region's events (about 2.8 per cent more for each claim a firm past
about 16) carries each of those freezes past the top of the layer and puts Pennine first at GBP 0.1 million.

## Three rules

Task type: catastrophe-exposure-accumulation (actuarial-science-insurance), which serves Opportunity Sizing: the call sizes what a catastrophe layer is worth on each of four books (expected recoveries less premium and reinstatement premium) and places the one layer the plan provides for where it is worth most.
Domain test: the deciding quantity is a catastrophe layer's expected recoveries at the cover year's exposure and costs, which a reinsurance actuary prices by burning cost from the company's own events, and the field's catastrophe models carry post-event demand surge: an event's claim costs rise with its demands on local repair capacity, so an event striking a larger book costs more than in proportion where the capacity has not grown.
Swap: "Pennine takes the layer because its old freezes, struck on its 2027 book, would swamp its 34 repair firms and cost more per claim" with a hospital's admissions in place of claims and wards in place of repair firms reads as a capacity question with nothing to price: no retention, no limit, no reinstatement, no hours clause, no premium to set against recoveries; with a utility's outage repairs it loses the layer's terms, which are what turn a cost per claim into recoveries.
Layer 1: event codes only for declared events and missing on most late-notified claims (the claims system); occurrences built from dates of loss under the hours clause, one period from each catastrophe's first loss (the company's event definitions); incurred as paid plus outstanding on 31 October 2026, a few 2025 claims still reserved (the claims ledger); cash settlements with no panel firm or sign-off date (the settlement route); repairs signed off months after the loss, so the index can be read at the month of loss or of sign-off (the panel's workflow); the 1 January 2021 Calder and Colne book transfer into eight Pennine districts (the policy administration system's district counts); ordinary windstorm, flood and freeze claims on quiet days and inside the catastrophe periods (the claims system); nothing placed to be caught.
Layer 2: field_method, post-event demand surge: the cost of a claim rises with its event's claims per panel firm, read from every event's indexed cost per claim against its claims per firm, and each past event is re-priced at its own 2027 claims per firm before the layer's terms apply.
Decisive step: price each historical event at the repair cost its 2027 scale implies (the cost of a claim read against claims per panel firm across every event, each event carried from its own claims per firm to its 2027 claims per firm on the 2025 panel) instead of carrying each claim's recorded cost forward by the index alone.
Not semantics: every field can be read correctly (what incurred is, what a panel firm is, what the transfer added, and what the index measures, which RC-07 s.3 files as the price of rebuilding a standard home in ordinary times) and the analyst still files Severn Vale, carrying each claim by the index or adding the surge the field reads on a catastrophe's size, because no field, flag or document says the cost of a claim depends on how many claims its event put on each firm; only the cost per claim against claims per firm across the events shows it.
Not rule application: the valuation basis files the estimand (each year's events had they struck the 2027 book, at what repairing them would cost in 2027, under the layer's terms, the plan's index carrying only a standard rebuild's price in ordinary times) and the hours clause files the occurrence; nothing names demand surge, panel capacity or what drives a catastrophe's cost per claim. Enumerated family on the cut pack, 57 constructions (the 32 surge-aware routes below; two index-only defaults; a region-level scaling; three severity trends; a post-2021 analog; two cost-per-claim steps read on the event's claim count; sixteen surges read on the catastrophe's size, its claim count or its loss, linear, log, quadratic or hinge, pooled or a curve per peril): Pennine GBP -2.13 to +0.09 million, and all 25 that never build claims per firm file Severn Vale or Fenland. Standing family, 32 routes (index at loss or at sign-off, claims per firm on all claims or on panel jobs, four surge forms, pooled or Pennine-only): 32 of 32 name Pennine at +0.087 exactly, a spread of zero because its four pre-2021 freezes exhaust the layer under every form (smallest 28.1 against a top of 25), and every other region in one printed bin. The easy route sits outside this family, refuted by the record, so unanimity here is the determinacy the build wants (stumping 1.1, the one-ended dial). Loudness of the ruling-out: no column, clause or document separates the routes; the record does once claims per firm is built from the panel-firm column and each event's claim count (the surge term at F = 2,414 on 1 and 60 degrees of freedom against a per-peril level; the hinge on claims per firm leaves a residual sum of squares of 46.6 against 725.3 for the best reading on the catastrophe's size), while the cheapest one-group-by stand-in, cost per claim on the event's claim count, files Severn Vale (Pennine -0.235 against +0.008).
Analyst test: the easy route, every claim carried to 2027 by its district's policies and the rebuild cost index with the layer applied to the hours clause's occurrences, names Severn Vale at GBP 0.0 million (the default path's Ends on), against Pennine at GBP 0.1 million; a strong analyst who reads RC-07 s.3 and adds the surge the field reads on a catastrophe's size names Severn Vale too (16 forms, Pennine at most +0.061 against Severn Vale's +0.118); on the generator's clean truth the index-only route files Severn Vale and the surge at the 2027 scale files Pennine (R3a and R3b in checks.py).
Estimand: `catastrophe_layer_valuation_basis.pdf` (policy RC-07): expected 2027 recoveries are the average over 2010 to 2025 of what the layer would have recovered had each year's windstorm, flood and freeze events struck the region's 2027 home book, each event's claims at the 2027 policies in force in each postcode district, at what repairing them would cost in 2027, under the layer's retention, limit, reinstatement and loss occurrence definitions, less the quoted premium and the expected reinstatement premium, in GBP million to one decimal; s.3 files the plan's 2027 rebuild cost index as the price of rebuilding a standard home in ordinary times, which does not carry what else made a catastrophe's repairs cost what they did (the pass-4 judge's SEND_BACK, answered by filing what is valued; the method stays open).
No decoy: nothing is planted; no document argues for a region, carries a value for one or ranks them; the brokers' quotations price the layer in each region (an input the value nets, not a ranking on it), the group's 2026 catastrophe programme and the 2024 flood resilience survey are declared distractors.
No certified replay: no certified or published loss figure is shipped for a method to be recovered from; the golden is built from the claims, the exposure, the index and the plan.
Lesson: an as-if loss carried to a larger book is not the old loss scaled up when the cost of a claim depends on the load each event puts on a fixed repair capacity; a model learns to read cost per claim against load per unit of capacity across every event and to re-price each event at its forward load, which no build on file teaches for catastrophe pricing.

## Readability screen

| Rung | Step | Where a reader meets it | Verdict |
|---|---|---|---|
| 0 | each region's windstorm, flood and freeze claims built into occurrences from their dates of loss, one period from each catastrophe's first loss, per peril | the event definitions file the hours, the start proviso, the per-peril rule and that every claim of the peril dated in the period belongs | readable |
| 1 | each claim carried to the 2027 book by its district's policies and to 2027 costs by the rebuild cost index | RC-07 files both, and s.3 that the index is the price of rebuilding a standard home in ordinary times; the plan carries the 2027 policies and the 2027 index | readable |
| 2 | the layer's terms on each occurrence, the annual cap and the reinstatement premium pro rata as to amount | the quotations file them | readable |
| 3 | a surge on a catastrophe's cost per claim beyond the index, read on the catastrophe's size (its claim count or its loss) | s.3 says the index does not carry what else made a catastrophe's repairs cost what they did; the field's catastrophe models read demand surge on an event's size | readable |
| 4 (decisive) | the cost of a claim read against its event's claims per repair panel firm across every event, each event re-priced from its own claims per firm to its 2027 claims per firm on the 2025 panel | no field, clause, column or document: s.3 names no driver; claims per firm is built from the claims' panel-firm column and the event's claim count, and the uplift shows only across events | silent |

## Semantic fork table

| ID | Term or convention | Readings | Ruled out by |
|---|---|---|---|
| SF1 | the 2027 book by district | the plan's region totals spread by the mid-2025 district mix; by the 2024 mix; by the 2023 to 2025 mix | same call, same bins under all three (asserted) |
| SF2 | policies in force by district and year | one mid-year count a district a year | the extract's grain, one row each (asserted) |
| SF3 | the index month | the month of loss; the month the repair was signed off | same call, same bins across the 32-route product (asserted) |
| SF4 | the 2027 cost level | the plan's 2027 average index, 146.4; the last published month | RC-07 names the plan's assumption (asserted) |
| SF5 | incurred | paid plus outstanding at 31 October 2026; paid only | filed; no catastrophe claim carries a material reserve, and paid only keeps every value (asserted, R2b) |
| SF6 | where a catastrophe's period starts | at its first loss; at the spike; split in two | the start proviso and front-loaded claims: every catastrophe sits in one period from its first loss (asserted) |
| SF7 | wind and surge from one storm | one occurrence; one a peril | filed: each peril under its own hours |
| SF8 | claims per firm | all claims over panel firms; panel jobs over panel firms | same bins across the product (asserted) |
| SF9 | the 2027 panel | the 2025 firms; two more; each region's 2016 to 2025 or 2021 to 2025 trend | same bins (asserted) |
| SF10 | the surge's form and pooling | hinge or straight line in claims per firm, on log or on level cost, quadratic; pooled or Pennine alone | 32 of 32 routes in one bin a region, asserted as the product of SF3, SF8 and SF10 |
| SF11 | rounding | each value once from its unrounded figure | every value 0.025 or more from a bin edge, Fenland the nearest (asserted); Fenland stays between -0.826 and -0.766 across the 32 standing routes and every further reading measured (SF1, SF9, SF20, a fit on events of any minimum size, weighted or not, a hinge fixed anywhere from 10 to 20 claims a firm, the 2027 panel carried on each region's 2016 to 2025 or 2021 to 2025 trend) |
| SF12 | the reinstatement premium | pro rata as to amount on the first limit | filed in the quotations (asserted) |
| SF13 | event codes | the codes decide the occurrence; the dates do | filed (the code does not decide); the codes-only mishandling with the surge keeps the call and Pennine's value; at the index alone the codes-only route and the coded-storms route both name Severn Vale (all three asserted) |
| SF14 | which claims sit in an occurrence | every claim of the peril dated in the period; the period's claims less the usual day's | filed: "all the peril's individual losses dated within" (asserted; taking the usual day off would move Severn Vale's bin) |
| SF15 | ask A's denominator | the exposure extract's mid-year count; a 31 December 2025 count for 2025 | filed in the prompt ("per policy in force at mid-year"), the stage 4 judge's FIX_NOW; the extract holds the only count for 2023 and 2024 (asserted) |
| SF16 | ask A's as-at | the unit's October 2026 report | the last report in the workbook (asserted) |
| SF17 | ask B's day boundary | effective on, before or after 31 December | no cancellation, endorsement or term end falls on 31 December or 1 January (asserted) |
| SF18 | ask B's direct grain | one home a policy, by district | the direct table's grain (asserted) |
| SF19 | ask B, a term listed after its Cancelled row | reinstated; still running to its effective date | filed (SF21) and the data agree: a reinstated term stays listed for every later month of its term, a term given notice is listed through the month it takes effect and never after; only a listing for a month that began after the effective date marks a reinstatement (golden, verify and the truth agree; the two heuristic routes miss by GBP 0.88 and 7.80 million or more) |
| SF20 | the repair panel behind claims per firm | the firms on every claim the region repaired that year; the firms on its windstorm, flood and freeze claims only; the firms that worked each catastrophe | the 2025 panel and every value identical under the first two, the same bins under the third (asserted); the pass-3 judge's fork (Fenland -0.727 when the 2025 panel was counted on weather claims, 131 firms against 137), closed in the data: weather work goes round the whole panel before any firm takes a second weather job in the year |
| SF22 | what repairing a catastrophe's claims would cost in the cover year | the recorded cost carried by the index alone; that cost with whatever else the record shows made a catastrophe's repairs cost what they did | filed in RC-07 s.3 (the pass-4 judge's SEND_BACK): the plan's index is the price of rebuilding a standard home in ordinary times and does not carry the rest, so the index alone is not a reading of the estimand; what drives the rest is method, which the record forces (the hinge on claims per firm leaves a residual sum of squares of 46.6 against 725.3 for the best of 16 readings on the catastrophe's size, and every size reading puts another region ahead of Pennine by 0.057 or more; asserted) |
| SF21 | ask B, what a bordereau lists | every term the coverholder's month-end records show in force at some time in the month, with each cancellation processed in the month and its effective day; a list that lags | filed in the claims operations report, section 4 (the pass-3 judge's SEND_BACK); every term that stops being listed before February 2026 has its end or a Cancelled row in the bordereaux, so a reading that also asks for a December-or-later listing files the golden (asserted) |

## Ladder

| Rung | Route | Values, GBP million | Call |
|---|---|---|---|
| 0 | the transfer read region by region: each claim scaled by its region's 2027 policies over the year's, index at the month of loss | SV +0.012, CN -0.505, FL -0.825, PN -0.890 | Severn Vale |
| 1 (default) | district scaling, index at the month of loss | SV +0.017, PN -0.436, CN -0.507, FL -0.827 | Severn Vale |
| 1b | the same, index at sign-off | SV -0.019, PN -0.463, CN -0.535, FL -0.849 | Severn Vale |
| 1c (Layer 1 mishandled) | rung 1 on occurrences built from the event codes, the late-notified claims without a code dropped | SV -0.305, FL -0.880, CN -1.008, PN -1.159 | Severn Vale |
| 1d (Layer 1 mishandled) | rung 1 on the coded storms only, every claim of the peril dated in each one's period counted | SV +0.017, PN -0.436, CN -0.507, FL -0.827 | Severn Vale |
| 2 | a surge read without the panel: severity trends, each region's post-2021 cost per claim carried back, cost per claim on the event's claim count | best for Pennine, the claim count: PN -0.235 against SV +0.008 | Severn Vale |
| 2b | the surge the field reads on a catastrophe's size, after RC-07 s.3: cost per claim on the catastrophe's claim count or its loss at the index, linear, log, quadratic or hinge, pooled or a curve per peril, each catastrophe re-priced at its 2027 size (16 forms) | best for Pennine, the loss pooled and linear: PN +0.061 against SV +0.118 | Severn Vale on all 16 |
| 3 (golden) | cost per claim against claims per panel firm, pooled, a hinge on log cost at 16.5 claims a firm with slope 0.0279; each event re-priced at its 2027 claims per firm | PN +0.087, SV +0.017, CN -0.491, FL -0.775 | Pennine |

Pennine's four pre-2021 freezes at the golden rung (GBP million):

| Freeze | Claims | Claims a firm then | At 2027 | On-levelled loss | At the 2027 scale |
|---|---|---|---|---|---|
| 18 December 2010 | 677 | 22.6 | 44.1 | 20.5 | 37.3 |
| 17 January 2013 | 738 | 23.8 | 47.7 | 22.6 | 44.0 |
| 10 December 2017 | 803 | 25.1 | 49.6 | 24.7 | 49.0 |
| 27 February 2018 | 773 | 24.2 | 46.4 | 21.8 | 40.5 |

At the index alone they recover 10.5, 12.6, 14.7 and 11.8; at the 2027 scale each exhausts the layer under every
standing form, so Pennine recovers 3.75 a year against a premium of 2.93 and an expected reinstatement premium of 0.73.

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | RC-07: the region's windstorm, flood and freeze events 2010 to 2025 had they struck the 2027 book; ask A the five perils' claims by loss year; ask B the direct book and every scheme term in force |
| 2 Unit of account | the loss occurrence (event definitions); ask A per policy in force; ask B per region |
| 3 Attribution window | an occurrence's year is its first day's; no occurrence spans a year end (C3, SF6) |
| 4 As-of dating | incurred at 31 October 2026 (RC-07 and the prompt); ask A at the unit's October 2026 report; ask B on 31 December 2025 |
| 5 Version basis | one claims extract, one exposure extract, one plan, one index; no revised release shipped |
| 6 Denominator | the average over the sixteen years 2010 to 2025, a year with no recovery counting as nil (RC-07) |
| 7 Weighting | each year equally (RC-07); the surge fit claim-weighted, and every weighting in the family files the same bins (SF10) |
| 8 Window length | sixteen years, filed |
| 9 Boundary inclusivity | no claim, cancellation or endorsement on a boundary that moves a figure (SF6, SF17) |
| 10 Rounding path | once from the unrounded figure (SF11); ask A to the penny from unrounded totals |
| 11 Tie-break | none needed: Pennine clears Severn Vale by 0.071 (C2), and by 0.068 or more on every standing route |
| 12 Maturity and censoring | every catastrophe claim settled or immaterially reserved (SF5); ask A at 31 October 2026 as filed |
| 13 Order of operations | each occurrence, then the annual cap, then the reinstatement premium (quotations, RC-07) |
| 14 Row order | every figure a group-by; verify.py's independent recompute agrees on all 21 |
| 15 Duplicate resolution | no repeated claims (R3c); ask A's reopened cases are further costs on one claim (device, asserted against the truth) |
| 16 Identity normalisation | districts join claims, exposure and the bordereaux exactly; the unit's policy numbers are the platform's nine digits |
| 17 Netting against gross | gross of reinsurance; no recoveries in the data |
| 18 Dimensional units | GBP throughout; the index in points; policies as counts |
| 19 Code and status semantics | event codes do not decide occurrences (filed, SF13); ask B's transactions read as listed |
| 20 Integerisation | none |
| 21 Clause scope | the hours clause per peril and per region (filed) |
| 22 Forward window contents | the 2027 book and index from the plan; the 2027 panel at the 2025 firms (SF9) |

## Literal reader

Executed word for word, RC-07 asks for each year's events had they struck the 2027 book, each event's claims at the 2027
policies in each district, at what repairing them would cost in 2027, under the layer's terms, and s.3 says the plan's
2027 index is the price of rebuilding a standard home in ordinary times, which does not carry what else made a
catastrophe's repairs cost what they did. A reader who carries the recorded cost by the index alone files Severn Vale at
GBP 0.0 million and leaves that sentence unanswered; a reader who answers it with the surge the field reads on a
catastrophe's size files Severn Vale too (16 forms; Pennine at most +0.061 against Severn Vale's +0.118). The basis
fixes what is valued (the 2027 cost of repairing each past event's claims on the 2027 book) and leaves the method open,
and the record forces it: the cost of a claim rises with its event's claims per panel firm, a fit the size readings do
not approach (SF22), and 32 of 32 standing constructions file Pennine at GBP 0.1 million. The prompt's "under the
board's valuation basis" points at RC-07 alone. Ask A's "incurred at 31 October 2026 per policy in force ... taken
together, for each of 2023, 2024 and 2025" executes to each claim's loss year by the date it now carries, over the
exposure extract's mid-year count, step 6 naming the unit's case handling the golden uses; ask B's "buildings sums
insured on 31 December 2025" executes to the direct table plus every scheme term in force that day at its sum insured
that day, the claims operations report filing what a bordereau lists.

## Oracles

- The generator's clean truth: R3a and R3b (on the world's own events the index-only route files Severn Vale and the
  surge at the 2027 scale files Pennine); AA and AB (both asks' goldens equal the generator's truth in every cell).
- verify.py: an independent recompute of all 21 graded figures from target/ (its own occurrence builder, surge fit, claim
  chains and the scheme terms in force on 31 December), OK.
- pair.py: every ask route's cells against the golden, the ceiling below.
- Four isolated probes, prompt and pack only: C and D on t5, E and F on t7 (the table below).

## Ask sheet

Pair ceiling: 35.4 (best wrong path keeps 1 of 16 ask cells)
Mirror leakage: 6.2 per cent of ask weight
Measured by: generator/pair.py

**Ask A, 12 figures**: each region's incurred at 31 October 2026 per policy in force at mid-year on its escape of water,
accidental damage, theft, fire and subsidence claims, for each of 2023, 2024 and 2025, in pounds and pence ("at
mid-year" added to the prompt at stage 4, the judge's FIX_NOW: a 31 December count moved 2025 by about 1.5 per cent). Path: the platform's
claims, the Major Loss Unit's 46 monthly reports, the exposure extract. Off the call: no windstorm, flood or freeze claim
reaches the unit (SEP).
- A1, seen and repaired right: the platform keeps a claim's figures from the day it went to the unit.
- A2, silent: a case the unit cuts below GBP 70,000 goes back to the home claims team and leaves the report open, with
  no Closed row; the platform's figure is current and the unit's last row is stale. Moves every cell.
- A3, seen, reflex repair wrong: the unit's adjusters date a leak or a subsidence claim from when the damage began, so
  the platform's date and year are stale, and three claims the platform dates in 2026 (outside the extract) are 2025
  losses. Moves 11 of 12 cells (Fenland 2025 has no candidate).
- A4, seen, reflex repair wrong: a closed case needing more work reopens under a new reference carrying only the
  further cost, so the claim is the sum of its cases, not the latest. Moves every cell under both mishandlings.

**Ask B, 4 figures**: each region's buildings sums insured on 31 December 2025, GBP million to one decimal. Path: the
direct table on 31 December 2025 and five monthly bordereaux. Off the call: the call reads neither file (SEP).
- B0, seen: the scheme is not in the direct table.
- B1, seen and repaired right: processing against effective dates (redemptions keyed on the 10th of the next month,
  late endorsements).
- B2, seen and repaired right since the pass-3 judge filed the listing rule (SF21): a term cancelled for a missed
  direct debit and reinstated within the month is listed in force again after its Cancelled row (3 to 5 a region).
- B3, seen, reflex repair wrong at policy level: a rewrite onto the fuller cover cancels one term and starts another
  under the same policy number (22 to 71 a region with both rows in the window).
- B4, seen and repaired right since SF21: notice given ahead of the day cover ends, so a term whose cancellation was
  processed in October or November is still listed for the month it takes effect and is out from that day (3 or 4 a
  region covering 31 December).
- B5, silent, the primary since the pass-3 judge: a listing carries a term's sum insured as it stood when the month
  opened, so it moves in the month after an endorsement is keyed, whatever day the endorsement takes effect. The
  society's further advances for home improvements are keyed when it lends and raise the sum insured from the day the
  works are finished, two to five months on, so 22 to 65 terms a region in force on 31 December already carry in the
  December listing a sum insured that takes effect only in 2026. Read the December listing as the year end with the
  endorsements keyed from December on applied over it, and every region is high by GBP 1.43 to 4.27 million; take December's
  own endorsements as already in its listing and it is high by 0.93 to 2.89. Only each term's first listing moved by its
  endorsements in effective-date order files the golden. Nothing filed says when a listing's sum insured moves; the
  endorsement rows' effective dates beside the listings are the only evidence (law 2, split evidence), and the same
  kind of row with an effective date inside 2025 is the benign twin (law 7).

| Ask | Cracker's path (lands the call, runs the battery, executes every filed rule) | Cells kept | Verdict |
|---|---|---|---|
| A, 12 figures | the unit's figures over the platform's; each case's latest row; the platform's loss year; one case a claim | 0 of 12 | miss |
| B, 4 figures | the direct table plus every scheme term whose dates cover 31 December, out on a cancellation effective by then unless listed for a later month that began after it (the rule SF21 files), each at its December listing's sum insured with the endorsements keyed from December on | 0 of 4 | miss |

The mirror stops at the default (Severn Vale) on the same ask paths: 12 of 38 recommendation points (Fenland, Severn Vale
and Coastal North's values), the same 0 of 16 ask cells. Every route in the grid (18 for ask A, 10 for ask B)
misses every ask B cell by GBP 0.81 million or more; the sharpest ask A route (A3 alone mishandled) keeps Fenland
2025.

Measured, isolated probes at medium effort, prompt and pack only:

| Probe | Pack | Call | Ask A | Ask B | Where each ask went |
|---|---|---|---|---|---|
| C, sonnet | t5, first ask layer | Severn Vale | 0 of 12 | 4 of 4 | B by effective dates |
| D, opus | t5, first ask layer | Severn Vale | 12 of 12 | 4 of 4 | found the cases that left the report open |
| E, sonnet | t7, this layer | Severn Vale | 0 of 12 | 0 of 4 | A2 and A3 mishandled; B2 and B3 mishandled |
| F, opus | t7, this layer | Severn Vale | 0 of 12 | 0 of 4 | A2 mishandled; B2 mishandled |

Stage 4 round 1, isolated scored readers on the cut pack (sha 22b02f2f), prompt and pack only, medium effort:

| Reader | Call | Ask A | Ask B | score_reader | Where each ask went |
|---|---|---|---|---|---|
| I, sonnet | Severn Vale | 0 of 12 | 0 of 4 | 3 of 20 (the three values the default shares), PASS | A3 and A2 mishandled; B2 missed |
| J, opus | Severn Vale | 1 of 12 | 4 of 4 | 8 of 20, FAIL at 40 per cent | A3 mishandled (Fenland 2025 has no A3 candidate); B whole |

Both readers missed the call on the default path. Reader J's ask B fell to "a cancellation followed by later In force
rows was reinstated", so B4 and B5 were added.

Stage 4 round 2, fresh isolated scored readers on 1e97a7a4:

| Reader | Call | Ask A | Ask B | score_reader | Where each ask went |
|---|---|---|---|---|---|
| K, sonnet | Pennine, by the coded storms alone, at GBP -0.4 | 0 of 12 | 0 of 4 | call hit, asks 0 of 20, FAIL | took the coded storms as the occurrences, so the floods and storms the claims team never coded dropped out; B4 kept in |
| L, opus | Severn Vale | 0 of 12 | 0 of 4 | 2 of 20 (shared values), PASS | A2 and A4 handled, A3 by the first-listed date; B4 read as reinstatements |

Neither reader took the decisive step (reader K's Pennine figure is the default's -0.4). Reader K named Pennine through
a lower rung that ranked it first: the April 2012, June 2019 and November 2019 floods and the January 2015 windstorm
carried no event code, and taking the coded storms as the occurrences dropped Severn Vale to -0.669 and Coastal North
to -0.660 while Pennine's coded freezes held it at -0.428. A separation failure (stumping 6.2: never first on an
intermediate rung), closed in the data: those four catastrophes are now declared late and coded on their own stream,
so no loss figure moved, and both event-code routes name Severn Vale (asserted). A sweep of the other data-handling
slips at the index alone (notification-date periods, paid only, no exposure scaling, wind and flood combined, calendar
months) names Severn Vale or Coastal North every time. Round 3 readers measure the closed pack.

Stage 4 round 3, fresh isolated scored readers on 8851863d:

| Reader | Call | Ask A | Ask B | score_reader | Where each ask went |
|---|---|---|---|---|---|
| M, sonnet | Severn Vale | 0 of 12 | 0 of 4 | 3 of 20 (the three values the default shared), PASS | A2 mishandled (the unit's last figure kept for cases that left the report open); B2 missed, and B given in GBP billions |
| N, opus | Severn Vale | 0 of 12 | 0 of 4 | 3 of 20 (the three values the default shared), PASS | A2 mishandled; B2 missed (GBP 0.8 to 1.6 million off a region) |

Both filed Severn Vale on the index alone and both quoted RC-07 s.2 for question 5 with the index-only result, which the
pass-4 judge then returned as the main-call fork (`## Tried and rejected`). Their realism tells, each fixed in the
generator or answered: repair lags stopping at one floor (fixed: lags by peril, RS7), same-day duplicate claims on a
policy (fixed: one claim a policy for a peril on a day, RS7), every catastrophe of a peril dated over the same number of
days (fixed: each catastrophe's own span and fall-off inside the hours clause), dates after the reader's own clock
(the fiction's quotations and plan postdate the 31 October extract, as they should), round premiums and sums insured
(how both are quoted), event codes mixing names and codes (UK storms carry names only from 2015), the unit's cases
leaving the report open (the device A2; the sheet's footnote describes closures only), a near-constant cash share and
smooth exposure growth (kept: both feed the main call's panel and scale, and neither is out of line for a mutual's
book), one-page documents and one endorsement a term (kept).

## Leak review

`leak.py --asof 2026-11-24` on eb9d2db9: REVIEW, no LEAK; sweeps 1, 2 and 5 to 11 clean, the containers carry the
issuing organisation. Each REVIEW line:
- Sweep 3, `home_claims_2010_2025.parquet` holds 125.88, 121.28, 134.52, 113.58 and 130.95, and the bordereaux 134.52:
  five accidental damage or theft claims' paid amounts among 483,625 rows and one annual premium among 79,894 rows equal
  ask A's per-policy figures, which sit in the same range of pounds and pence; coincidences nothing points at. Harmless.
- Sweep 3, `catastrophe_layer_valuation_basis.pdf` shares 7 of 9 of the call's distinctive words: RC-07 says how a
  layer's value for the cover year is reckoned, and names no region and no figure. Harmless.
- Sweep 4, `cat_xl_quotations_2027.pdf` (severn, pennine, premium, clause, january, definitions): the brokers price each
  region's layer and cite the event definitions. Harmless.
- Sweep 4, `catastrophe_layer_valuation_basis.pdf` (repair, premium, standard, expected, recoveries, definitions): the
  estimand, which fixes what is valued (each past event's 2027 repair cost on the 2027 book, by district) and, since the
  pass-4 repair, what the plan's index covers (a standard rebuild's price in ordinary times); it names no driver, no
  panel and no method. Six isolated probes and readers read the estimand before the repair and none took the step; the
  s.3 sentence is new and round 4 reads it cold. Harmless on the sweep; the reader's question 1 is the test.
- Sweep 4, `claims_operations_report_2025.pdf` (severn, pennine, repair, carries, january): section 2 says a claim's
  record carries the panel firm and the sign-off date, the claims file's two columns, which the report uses for its
  settlement split; section 4 says what a bordereau lists (SF21), an ask B convention the call never reads. Neither says
  anything about cost against claims per firm. Harmless.

Single-use test: no file or sentence exists only for the decisive step. The claims, exposure, index and plan are the
burning-cost inputs any layer valuation reads, and the panel firm is the settlement record's own field. RC-07 s.3's
index sentence is the caveat a valuation basis states beside any building-cost index (what the index measures and what
it leaves out); its deletion reopens the pass-4 fork, so it carries the estimand, and it leaves the size readings (SF22,
16 forms, all on Severn Vale) and the claims-per-firm reading equally open, so it does not single out the step. The
plan's About sheet carries the plan's version, approval date and preparer and one line naming what it holds; it names no
step and no sweep moved.

## Tried and rejected

- 2026-10-25, before the pack: the seed's own step (cannibalisation measured on flat streets carried to a hilly
  district) is a visible-state stratification on elevation, which the probes on this lane land by reflex; a
  station-level pilot comparison missing members who switched stations is a contaminated comparison, found by both
  probes on task304; battery swaps capping a hilly district's rides are handed over by battery columns. Set aside on paper.
- 2026-10-25, stage 2: twenty small University stations; per-station cells by day of week within month overshot the
  turned-away requests by 13 per cent (a station's stocked seconds and empty seconds move together when a few bikes
  drain), so the family forked; five large hubs (two residence halls, three class hubs) cut it to 3 per cent.
- 2026-10-25, stage 2: the graded figure to the nearest USD 10,000; the standing family on University spans about USD
  8,000 (induced riders on the rides served, day-of-week cells, the simulated e-bike world), so no seed holds it in one
  10,000 bin; 25,000 holds every network with USD 5,000 to spare.
- 2026-10-25, stage 2: per-station 2024 trips as a distractor; it licenses a difference-in-differences reading of the
  pilot that moves the uplift by a point and University's figure by USD 6,000. Dropped for the vendor's quotation.
- 2026-10-25, stage 2: the operations director's line that the e-bikes should go where the riders are, in the board
  paper; a stakeholder view pointing at the wrong answer reads as a planted decoy. Cut.
- 2026-10-25, stage 2: billing ZIP codes with a lookup for ask A; any real ZIP ties the invented city to a real one. The
  register carries the rider's home area from sign-up instead.
- 2026-10-26, stage 2: road-test retests reopened within 90 minutes only; a one-day window repair then lands the golden.
  Retests now reopen up to 39 hours later and intermittent faults come back within a ride or two, so no window separates
  them from genuine repeats.
- 2026-10-26, stage 3: the e-bike crew's moves on a 15-second grid, every charging session taking the lowest free point and
  192 sessions plugged in at local midnight on 1 January read as generated; the crew's pace, the point a rider picks and
  the New Year's Eve plug-ins now come from their own stream, and no call figure moved.
- 2026-10-26, stage 3: the 03:00 audit showed each station at its par on 92 per cent of mornings, a constant stream; the
  night crew now leaves a station a bike or two off par when the van runs short, and the call's figures moved by under
  USD 200 (University USD 127,946 to 127,804).
- 2026-10-26, stage 3: the first controller replacement in April; with the points re-drawn, a register-must-rise filter
  landed two of the three months before it. Moved to January, the filter misses every month.
- 2026-10-26, stage 4: architecture 1 spent. Both isolated scored readers (sonnet and opus at medium, prompt and pack
  only) rebuilt each station's classic stock from the 03:00 audit, the trips and the van moves, imputed the requests the
  empty seconds turned away and named University (USD 100,000 on station x day x hour-by-weekend cells; USD 125,000, the
  golden, on station x hour x day type x term cells): demand censored at empty stations is the field's textbook estimate,
  and a pack holding the audit and the dispatch log makes it executable. Both landed ask B (the re-sent sessions by their
  repeated registers) and neither ask A (one person a card) nor ask C (every job card). The judge thread returned
  NOT_DETERMINISTIC, SEND_BACK on Gate C (the estimation grain and the e-bikes' new riders unfiled in the measure; the
  person and job definitions in asks A and C), Gate G analytical_non_defect and Gate H pass. Realism tells the readers
  named: the inventory closing to zero on every station-day, one par per network at the 03:00 audit, Harbour's flat
  per-station rides, trip durations and the e-bike share flat across networks, hours and distances, the pilot note issued
  in January in the past tense, the pilot stations' capacities against the 5 per cent match. Re-root at stage 1.
- 2026-10-26, re-root screen (scratch t308v2): the pilot's comparison stations ran dry too, so the ride-based uplift
  double counts the relief; call-only probe B (opus) found the comparison stations' empty hours and measured the uplift
  on demand (University at USD 125,000). Any stump that runs through censoring or stock in this world is spent.
- 2026-10-26, re-root concept readers (opus, medium, scenario text only): household interference in an
  account-randomised retention trial, appraisal-smoothed private-fund returns, first-round against repeat screening
  yield. Each reader took the named textbook move at once (household-level contrasts, Geltner desmoothing, first kits
  split from repeats). Dropped before a pack.
- 2026-10-26, re-root, the journey unit (scratch t308v3): members re-dock at 45 minutes and day-pass holders at 30 to
  restart their included minutes, and the pilot's riders choose an e-bike once per journey, so take-up read per ride
  undervalues Central's day-pass tours. Both concept readers and both call-only probes on the first pack missed it
  (Riverside at USD 125,000 against the golden Central at USD 200,000). On the second pack (tourists riding two or
  three journeys a pass-day), probe D (opus) read the pile-up of classic rides just under the included minutes and
  the cliff after them as riders re-docking, chained same-station restarts within five minutes and filed the golden
  exactly (Central USD 225,000), and probe C (sonnet) reached Central through the day-pass e-bike rides' uncapped
  lengths. The allowance's cliff in the ride-length distribution announces the re-dock. Dead.
- 2026-10-26, re-root screen (plan-only Opus readers, text only, no figures): county procurement savings that budget-bound
  departments re-spend, a growth grant's induced jobs where the workforce commutes in, a Medicaid plan's savings past its
  members' churn, bus journeys from housing sites that build out slower than the developers' survey says, and contingent
  business interruption carried by suppliers' locations. Each reader named the step itself as the decisive one, unprompted.
  An economic mechanism that the filed estimand's own wording invites ("the fall in expenditure", "regional jobs", "the
  plan's spending") is a reflex, whatever the world.
- 2026-10-26, re-root probe pack (job-search app, a cancellation-flow save offer tested in two markets, carried to five):
  subscribers who cancel because an employer on the platform has just hired them cannot be saved by a price, and one
  market's employer side hires half its cancellers. The plan-only reader missed it; on the pack the Sonnet probe filed
  Mexico (USD 510,000) and the Opus probe linked the employer placement invoices to the cancellers and filed Colombia
  (USD 420,000, the golden). A hire record in its own file is read as churn by the first reader who opens it. Dead.
- 2026-10-26, plan-only screen of six general mechanisms (Opus readers, text only): a list-price rise judged on promotion-week elasticities (stockpiling), an adherence programme sized on the adherent against non-adherent admission gap (healthy adherer), a heat programme sized on same-day excess deaths (harvesting), threshold clinics sized on the last reading (regression to the mean), fare-free days sized on the trial days' lift (trips moved between days), and a ward sized on average occupancy (queueing at the peaks). Every reader named its mechanism unprompted, five of them as a numbered step. A general statistical mechanism is a reflex whatever world it is dressed in; only a world-specific structure is worth a pack.
- 2026-10-26, plan-only screen of four world-specific candidates (Opus readers, text only): a road reconstruction sized on patching avoided (the reader weighted traffic by standard axles unprompted), a station car park sized on new rail journeys (the reader named railheading and the full car park's hidden demand), and a cancellation-screen save offer carried to five markets (the reader named app-store billing as the first thing that could move the winner). All three dead on paper. The fourth, a bus priority corridor whose late running carries into the vehicles' next journeys, passed: the reader worked the corridor's own journeys only.
- 2026-10-26, probe pack (bus priority on one of four corridors, sized by the passenger lateness removed in 2027; Mill Lane's buses go straight on to the busy cross-town 22 and 30 on a short layover, so the lateness the scheme removes there stops passing into those journeys; the corridor-journeys replay files Harbour Road at 62,000 against the golden Mill Lane at 96,000): the plan-only reader missed it, but on the pack the Opus probe rebuilt the 2025 operation from the AVL, found that holding at timing points and a two-minute stand on each running board reproduced every recorded arrival to the second, replayed every board-day with the scheme and filed Mill Lane at 96,000 in eight tool calls; the Sonnet probe read the same two-minute stand off the running boards and filed Mill Lane at 96,000 too. A record that a replay of its own rules reproduces exactly invites the replay, and a replay of the whole operation carries every knock-on with it. Dead.
- 2026-10-26, plan-only screen of eight more (Opus readers, text only): an express lane whose toll would pass the statutory cap (the reader solved the toll under the cap and the speed standard), a security programme on a layered defence (marginal effect after the controls in place), a card limit increase whose defaulters draw the new limit (the pilot's own charge-off gap carried by score and utilisation band), a lender's product line whose losses sit with brokers since removed from the panel, an unlit artificial pitch (floodlight conditions applied slot by slot), courier-delayed potassium samples, a price rise that rivals follow, and a GP surgery sited by floating catchments. Each mechanism was a numbered step in the reader's plan. Dead on paper.
- 2026-10-26, plan-only screen of two more (Opus readers, text only): a motor rate cut sized by underwriting profit with one segment's case reserves strengthened by a claims-handling change (step 1 of the reader's plan checked case-reserve adequacy against the reserve history and fell back to paid), and a recycling service sized by tonnes diverted with contaminated loads rejected at the sorting plant (step 2 netted each area's reject rate). Both mechanisms were numbered steps. Dead on paper.
- 2026-10-26, plan-only screen of four more (Opus readers, text only): an extra ambulance crew sized by category 2 calls reached in time (step 4 split each late call into an availability miss and a geography miss, step 5 replayed the dispatch with the extra vehicle), e-bikes sized by ride revenue with flat batteries waiting for the swap van (step 6 capped usable e-bike-days by the 2027 swap rota), a home renewal increase sized by the underwriting result with multi-line households cancelling their car policy (step 6 priced the car-line spillover), and four nurse posts sized by agency spending avoided with the bank nurses the posts free covering agency shifts on other wards (missed: the reader netted bank-filled gaps as no saving, but the freed pool is a workforce mechanism any staffing field shares, so the swap test fails). Dead.
- 2026-10-26, plan-only screen of four more (Opus readers, text only): a survey boost sized by the cut in the regional standard error (step 4 rebuilt the design effect of the added sample by PSU take and interviewer workload), a regional catastrophe cover sized by expected recoveries less premium (step 4 rebuilt events from uncoded claims under the hours clause), a bus priority scheme sized by passenger time riding and waiting (step 5 priced waiting from each stop's headway spread, E[H squared] over 2E[H]), and a seven-day discharge team sized by bed-days released (steps 2 and 3 kept only the delay the team can remove and counted midnights, weekends first). All named. Dead on paper. The bus reader used the smartcard taps only to sense-check the counters and never followed a passenger from one bus to the next.
- 2026-10-26, the bus corridors with an hourly country connection at Grove Road (passengers set down late by the corridor bus wait for the next hour's country bus): two plan-only readers passed it on paper (one priced the country buses' waits against the timetable and used the smartcard taps only to reconcile loads; the other chained taps only to find alighting stops), but the estimand cannot carry it. Counting the connection wait needs either a sentence naming the change of bus (which hands the step over) or an arrival convention for passengers who walk to a stop, whose scope is then the decisive step (a definition reading under rule 3). Dropped before any data was cut.
- 2026-10-26, stage 2: the first ask layer (the unit's figures over the platform's, cases that left the report open;
  the scheme rebuilt by effective dates). On pack t5 the opus probe kept 16 of 16, finding the open cases and the
  effective dates, and the sonnet probe 4 of 16 by the effective dates: every device sat on a path a careful reader
  takes. Re-sited onto the unit's re-dated losses and reopened cases and the scheme's reinstatements and rewrites; on
  t7 both fresh probes kept 0 of 16.
- 2026-10-26, stage 2: taking the usual day's claims off each period moves Severn Vale to the bin edge (-0.150 against
  -0.084); the event definitions now say every claim of the peril dated in the period belongs to the occurrence.
- 2026-10-26, stage 2: the unit's re-dating capped at 120 days for a leak and 210 for subsidence reached 9 or 10 of 12
  cells on every stream, Fenland having no leak or subsidence case near a year start; widened to 200 and 300 days it
  reaches 11 (Fenland 2025 stays out of reach).
- 2026-10-26, stage 4 round 1: event claims notified late without the code at 8 per cent across every peril let the
  codes-only route at the index alone name Pennine (-0.771 against Severn Vale -0.992): the dropped claims pull Severn
  Vale's floods under the retention while Pennine's large freezes stay over it, a cheap route onto the golden region.
  Freeze claims now come in late more often (16 per cent, frozen pipes found after the thaw) and storm and flood claims
  less (3 per cent); the codes-only route names Fenland with Pennine third (asserted).
- 2026-10-26, stage 4 round 1: ask B's devices B0 to B3 fell whole to reader J (opus), who read a cancellation followed by
  later In force rows as a reinstatement. Re-sited with B4 and B5 (notice given ahead of the day cover ends, so a term
  is listed for the month its cancellation takes effect); the golden figures did not move, the heuristic now misses by
  GBP 0.89 million or more in every region.
- 2026-10-26, stage 4 round 2: four catastrophes that reach the layer (Severn Vale's floods of April 2012, June and
  November 2019; Coastal North's windstorm of January 2015) carried no event code, so the coded storms read as the
  occurrences named Pennine at its default -0.428 (reader K, sonnet). Coded on their own stream as declared late; every
  graded figure unchanged; the coded-storms route now names Severn Vale (asserted in checks.py).
- 2026-10-26, stage 4 re-judge (pass 3): NOT_DETERMINISTIC, SEND_BACK on ask B, the main call forced (Pennine +0.087
  on every route the judge built, Gate H analytical). Ask B's population was open: 17 terms given notice in September for
  a day in October or November were listed for October and never again, their Cancelled rows before the window, and
  nothing filed said what a listing means (GBP 0.5 to 1.8 million a region). Read as an ask-layer and fork repair, not a
  re-root, because both findings sit outside the decisive step and the judge found the call forced. A notice for a day
  inside the bordereaux is now keyed inside them (no term leaves the bordereaux without its end or a Cancelled row,
  asserted), the claims operations report files what a bordereau lists (SF21) and step 7 states the golden's rule.
  Filing the rule made B2 and B4 readable, and a December-listing snapshot then filed the golden in every region (gaps
  0.00 to 0.07), so the old B5 (the terms listed once) went and ask B's primary became the listing's sum insured moving
  when an endorsement is keyed, carried by the society's further advances. The judge's Fenland fork (the 2025 panel
  counted on weather claims only, 131 firms against 137, Fenland -0.727 against -0.775) was closed in the data (SF20),
  and the claims parquet lost its pandas schema block.
- 2026-10-26, stage 4 pass 4 (8851863d): NOT_DETERMINISTIC, SEND_BACK on the main-call estimand. RC-07's "at what
  repairing them would cost in the cover year", beside the plan's 2027 index, executed literally to the recorded cost
  carried by the index alone (Severn Vale -0.1), and nothing filed said the 2027 cost of repairing a catastrophe's
  claims is anything else; both round-3 readers took that reading for question 5. Ask A's step 6 did not reproduce the
  twelve figures (the judge's reconstruction differed by 0.05 to 1.5 pounds a policy). Repaired rather than re-rooted,
  because the judge found the effect in the data and the decisive step analytical (Gate H), and its own fix is a
  filing of what is valued, not of how: RC-07 s.3 now says the plan's index follows the price of rebuilding a standard
  home in ordinary times and does not carry what else made a catastrophe's repairs cost what they did, naming no
  driver, panel or method. Filing it makes a surge readable, so the surge the field reads on a catastrophe's size
  became a rung: on the old quote 3 of its 16 forms filed Pennine (the catastrophe's loss, pooled: linear, quadratic
  and hinge), a cheap route onto the golden. Severn Vale's quote was re-priced from GBP 4.42 to 4.34 million (rate on
  line 29.47 to 28.93 per cent), which moves no other region and puts all 16 size readings on Severn Vale (SF22, with
  the claims-per-firm fit far ahead of every size reading); the default now ends on Severn Vale at GBP 0.0 million.
  Step 6 states the unit's case handling word for word and the rival clause in block 1 was rewritten for a runner-up
  at nil. Round 3's realism tells were fixed in the same pass (repair lags by peril, one claim a policy for a peril on
  a day, each catastrophe's own span); no graded figure but Severn Vale's value moved.
- 2026-10-26, stage 4 round 4 and judge pass 5 (eb9d2db9): architecture 2 spent. Reader O (sonnet) landed the call: it
  read RC-07 s.3's new sentence (the index does not carry what else made a catastrophe's repairs cost what they did)
  as demand surge, fitted the cost of a claim on claims per panel contractor (flat to about 17.5, then 3.9 per cent a
  claim a firm), re-priced each event at its 2027 load and filed Pennine at GBP 0.9 million, quoting the s.3 sentence
  and the contractor column as what decided it. Reader P (opus) read the same sentence as leaving the recorded surge
  in the costs and filed Severn Vale at the index alone (0 of 1 call, 4 of 20). The pass-5 judge returned
  DETERMINISTIC, FIX_NOW: the main call forced by the s.3 sentence and the claims, with the 2027 panel unfiled (a
  panel grown with the book, or a fit not carried past the 35 claims a firm on record, gives no uplift) and ask B's
  term identity read by policy number (10 to 30 million high, the rewrites' old terms kept). The dial is the
  architecture's own: filing that the index leaves out what a catastrophe's own repair load adds (Gate C, the pass-4
  SEND_BACK) hands a reader holding the panel-firm column the step (Gate F), and without the sentence the pass-4 judge
  read the index alone as the literal estimand. A call any reader lands is spent; re-root at stage 1, architecture 3
  (the last before the number is retired, which needs the author).
