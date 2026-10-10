# task131 design note

Replaces task130 (failed on the portal 2026-10-10, both top models filed the golden). Drawn bespoke
under the template caps: no calibration corpus, no licensed wrong basis, no certified record to
reproduce.

## DRAW

| Axis | Value |
|---|---|
| Domain / subdomain | Marketing & Consumer Research / crm-loyalty-retention |
| Objective | Experiment & Causal Analysis |
| Niche | a regional consumer co-operative choosing which of four member-card reward offers its 2027 programme runs on every card, from a summer test its offer engine randomised card by card |
| Shape | 07 grid of cells: six regions by four offers, plus the four offers' 2027 programme values |
| Decision type / unit | pick one of four offers (named option), plus its 2027 programme value in CHF thousands |
| Gap / pattern / generators | population (the randomisation unit is not the economic unit), no A to E pattern; G10 cross-dimensional duplication (moved spend counted as gain on the offer card and as loss on its sibling), G4 attribution at transition |
| Gate G mechanism | method_or_model_selection (the unit of analysis an interference-affected test has to be read at) |
| Stump strategy | causal_design; decisive rule filed (the programme standard states the quantity: incremental net margin at a full rollout per active card-week); no official decoy; no validated decoy |
| Calibration form | none, because the strategy needs none |
| Context artifact | register (the offer engine's allocation register) |
| Stakeholder | head of the member programme, who puts the 2027 offer and its budget line to the executive board (Geschaeftsleitung) |
| Forum / forcing event / org family | executive_team / budget_or_appropriation (2027 budget round) / cooperative_or_member_body |
| World | Talwerk Genossenschaft, a consumer co-operative with 42 shops in six regions of eastern Switzerland, CHF; personas drawn de_CH seed 131 |
| Deliverables | `programme_offer_2027.docx` (commits), `offer_grid_2027.png` (reads at a glance) |
| Guard | PASS, no WARN; nearest driver 0.10 (task52) |

**Data-native sentence.** A Talwerk membership is a household that holds a main card and up to
three additional cards and buys from one household budget, while the offer engine allocates offers
card by card because rewards are credited to the card that is used; so the test's natural unit is the
card and its economic unit is the membership, and the inflation of every card-level lift by baskets
that only moved between cards of one membership is a property of how a co-operative's household
memberships shop, not of the test's arithmetic.

## Gate G

- **Litmus.** No reported number or stakeholder conclusion is overturned. The pack ships no test
  readout, no dashboard and no ranking of the offers; every figure in it is a correct record of
  card activity. The difficulty is choosing the unit at which a card-randomised test has to be read
  when cards of one membership share a budget. Answer: no.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Primary mechanism:** method_or_model_selection.
- **Deletion test.** Delete every wrong number and every claim: nothing in the pack is wrong and no
  voice argues an offer, so the pack after deletion is the pack, and it is still hard.
- **Clean-data test.** The main call's rows carry no planted defect; the card-week facts are complete
  and correct. Asserted in the generator: the main path reads no device row.
- **Lens-swap test.** The naive reading and the answer are not one population under two lenses: the
  naive reading averages every allocated card, the answer averages only the cards of memberships whose
  cards all drew the same arm (about 64 per cent of memberships, 42 per cent of cards), and its
  figures are not a re-labelling of the naive figures.

## Stump sentence

A competent solver takes each card's change in net margin after reward cost from the spring baseline
weeks to the six run-rate weeks, differences each offer against the control cards as randomised, and
commits to the personalised weekly coupons (D); the step that lands it there is reading each card as an
independent shopper, when the cards of one membership share a household's baskets and a card carrying
an offer pulls them off its sibling cards, so the lift on the card is partly spend that only moved;
measured on memberships whose cards all drew the same arm, the fresh-produce bonus (A) leads.

## The decisive move, and why it survives the opponent

1. **Written in no sentence.** The standard defines the quantity (incremental net margin per active
   card-week if every card carried the offer) and the windows; nothing says that cards of a membership
   share baskets, that the allocation mixes arms inside memberships, or that same-arm memberships are
   the clean comparison. The programme terms say a membership may carry additional cards, which is
   world furniture, not the move.
2. **No sweepable corpus nominates it.** There is no corpus.
3. **No arithmetic symptom.** Card-level totals tie to the week totals; the allocation is balanced
   20/20/20/20/20 by card and by region; pre-period balance holds; the control arm's run-rate decline
   sits inside the summer seasonal decline every arm shares.
4. **Not a per-row predicate.** It needs a group (membership), a property of the group (all cards in
   one arm), and a re-estimate on that subset; no column marks a pure membership.
5. **Enumeration is arithmetic.** The subset is defined by a group property computed over the
   allocation register joined through the card master.
6. **No cutover date.** The test start is dated, and the event study at the card level gives the
   wrong answer, so the date sits on the decoy's side.
7. **Survives the deletion** (above).

## Ladder (targets; realised values in the build record)

Chain-wide, per active card-week, CHF, run-rate unless stated.

| Rung | Construction | Winner | Killed by |
|---|---|---|---|
| 0 | card-level gross sales lift over the whole test | C monthly target voucher | the standard scores net margin after reward cost |
| 1 | card-level net margin lift over all twelve test weeks | B triple points | the standard scores the run-rate weeks (13 Jul to 23 Aug), and B's lift fades |
| 2 | card-level net margin lift, run-rate weeks (the filed basis, read at the randomisation unit) | **D weekly coupons, the stump** | a card's lift includes baskets moved off its membership's other cards, which nets to zero at a full rollout |
| 3 | same, on memberships whose cards all drew one arm | **A fresh-produce bonus** | answer |

Realised (CHF per active card-week, from the shipped bundle, asserted in `checks.py` and recomputed by
`verify.py`):

| Rung | A | B | C | D | Winner, lead |
|---|---|---|---|---|---|
| 0 gross sales, whole test | 9.14 | 10.90 | 13.29 | 10.43 | C, 1.22x (A 4th) |
| 1 net, whole test | 0.66 | 1.70 | 1.29 | 0.77 | B, 1.31x (A 4th) |
| 2 net, run rate, card level | 0.54 | 0.35 | 0.55 | 0.71 | D, 1.28x (A 3rd) |
| 3 net, run rate, same-cell memberships | **0.49** | 0.26 | 0.16 | 0.34 | **A, 1.45x over D** |

The partial correction (membership totals with mixed memberships kept, each in its main card's cell)
lands on A too but files every figure wrong (A 0.47); it is the decisive insight half applied, and the
graded figures separate it. Estimators on same-cell memberships converge at the stated rounding: card
weighted, membership weighted and single-card memberships only (C1, asserted on all four offers, the
gap and all 24 cells).

## Determinism: the 22 axes

| # | Axis | Disposition |
|---|---|---|
| 1 | Population | every allocated card; the register holds every card of every membership with a purchase in the baseline weeks (C1, asserted: no membership has an unallocated card) |
| 2 | Unit of account | the card for the quantity (per active card-week, filed), the membership for the comparison (the move); single-card-only, all-same-arm and size-reweighted estimators converge at the stated rounding (C1, asserted) |
| 3 | Attribution window | baseline W15 to W22 and run-rate W29 to W34 filed in the standard (pin) |
| 4 | As-of dating | the membership's home branch and card roles are static over the extract; region by the 1 July 2026 network (pin in the standard), only the grid reads it |
| 5 | Version basis | the branch register is January's; the network notice carries the 1 July changes (grid device, off the main path) |
| 6 | Divisor | active card-weeks, every week counted, weeks without a purchase as zero (pin in the standard and the field notes) |
| 7 | Weighting | pooled over cards (pin); card-weighted and membership-weighted per-card means converge (C1, asserted) |
| 8 | Window length | six run-rate weeks, eight baseline weeks (pin) |
| 9 | Boundary inclusivity | ISO weeks Monday to Sunday, both ends inclusive (pin in the field notes) |
| 10 | Rounding path | round once at the end; per card-week to two decimals, 2027 values to CHF thousands; every graded figure mid-bin (asserted distance to the bin edge) |
| 11 | Tie-break | no tie within 0.05 on any graded comparison (asserted) |
| 12 | Maturity and censoring | none: the windows are closed and the facts final at the extract (field notes) |
| 13 | Order of operations | net margin per card-week then averaged; averaging then netting gives the same figure (linear, C1) |
| 14 | Row order | irrelevant (sums) |
| 15 | Duplicate resolution | one row per card and week (asserted unique key) |
| 16 | Identity normalisation | card numbers are 13-digit strings with a leading zero in a minority; read as strings (field notes); integer reads keep the key unique (C1) |
| 17 | Netting against gross | net margin = gross margin minus reward cost (pin) |
| 18 | Dimensional units | CHF throughout; points converted at CHF 0.01 already in reward cost (field notes) |
| 19 | Code semantics | offer codes K, A, B, C, D in the register, described in the catalogue |
| 20 | Integerisation | none |
| 21 | Scope of a clause | the standard's 2027 value clause governs every offer, not only the pick |
| 22 | Forward window contents | 2027 value = run-rate per active card-week x 52 x planned active cards (pin in the standard; planned cards from the 2027 plan) |

Estimator forks the judge may raise, each closed by C1 convergence asserted in the generator: (a) single-card memberships only, (b) every same-arm membership pooled, (c) same-arm memberships reweighted to the population's card-size mix, (d) per-card means weighted by card against by membership.

## Ask sheet and ledger

**Main call row population.** Card-week rows of cards in memberships whose cards share one arm,
weeks W15 to W22 and W29 to W34, columns gross_margin and reward_cost; the allocation register; the
card master's membership link; the standard; the 2027 plan's total. Device rows inside it: zero
(asserted).

**Ask 1, the grid (24 figures).** Run-rate incremental net margin per active card-week for every
region by offer, CHF to two decimals. Construction layer: the membership-level read cut by region.
Devices, both off the main path (the main call reads no region):
- D2 vintage: three branches moved region on 1 July 2026; the branch register is the January edition, the network notice carries the move.
- D7 chain: two branches closed on 30 June 2026; memberships still carry the closed branch as home branch, and the notice names each successor.
Use: the board sequences the 2027 regional rollout and the regional managers' targets off the grid.

**Ask 2, the four 2027 programme values** (CHF thousands), the call's own figure for every
candidate, plus the gap between the pick and the runner-up per card-week. Decision furniture.

**Chart.** Heatmap of the 24 cells, rows regions, columns offers, the chosen offer outlined, the
runner-up labelled, chain-wide values in a header row, title stating the call.

**Pair arithmetic.** Responses that miss the decisive move file every grid cell wrong (the card-level
read moves every cell) and three of four 2027 values wrong; they keep instruction following and the
chart's structural parts. A response that lands the call loses the grid cells in the regions the two
devices touch (four of six regions, 16 of 24 cells) unless it also handles both devices.

## Build record (stage 3)

- Pack: 14 files, 8 formats, spine `card_week_sales_2026w15_w34.parquet` 611,400 rows; 37,298 cards in
  24,000 memberships; two consecutive builds byte-identical (zip entry times, xlsx core and app
  properties, PDF dates, document id and checksum pinned in `postprocess.py`).
- Golden: A 0.49, D 0.34, B 0.26, C 0.16 per active card-week; 2027 values CHF 966, 666, 516, 316
  thousand on 37,720 planned active cards; gap 0.15; 24 cells by 1 July 2026 region.
- Regional targets are forced per area (core region, the Rorschach group that moved to St. Gallen
  Stadt, the Degersheim group that moved to Appenzellerland), so the 2027 cells are true mixtures and
  both network devices move every cell of the four regions they touch (asserted).
- `checks.py` 149 assertions green; `verify.py` (no generator code) reproduces every figure and the
  memo's tables; surface screen 0 promoted (nearest task109, 0.096); heart PASS.
- `leak.py` REVIEW, no LEAK (the catalogue renamed from `st26_test_catalogue.json` after sweep 1 read
  `test_` as author vocabulary). The two REVIEW lines: `MP-3_measuring_offers_rev3.pdf` shares
  standard, margin, membership, reward, engine and run-rate with the stump paragraph because it is the
  standard that defines the quantity; it never says the cards of a membership share baskets or that a
  comparison should be made by membership. `crm_extract_field_notes.md` shares the world's nouns
  (membership, register, engine) and states one fact, that a membership has one main card and up to
  three additional cards, which is world furniture the card master shows anyway. Both harmless.
- Containers: no writer signature or out-of-band stamp in target/ or golden/ (H1 audit clean).

## Tried and rejected

- Store-randomised geo test with cross-store shopping as the interference: rejected at the draw, because the redemption file would show offer redemptions at control stores, a symptom the hygiene battery surfaces, and a store-level counterfactual needs a third group the pack would have to ship.
- Household-randomised offer delivered to the main card only: rejected at the draw, because an analyst who analyses at the randomisation unit (the membership) lands the answer by default.
- Per-membership planning basis in the standard: rejected at the draw, because a per-membership quantity sends the solver to group cards by membership, where the mixed arms are in plain view; the co-op budgets rewards per active card, which is the realistic basis and keeps the natural read at the card.
- Signature population + pattern D + method selection: blocked by the guard (spent in eight builds); the honest label is no A to E pattern with G10 decisive.
- Equal per-row forcing of a group's run-rate margin shift: put margin above sales on small baskets; the shift is now spread across cards and rows in proportion to their spend.
- Region-level forcing with the moved members sharing their new region's target: the January-register misreading then moved the St. Gallen cells only by sampling noise; forcing per area makes the device bite by construction.
- Plan total placed by stepping one region: grew St. Gallen 14 per cent against about 1 per cent elsewhere; the placement now walks totals outward and spreads the steps across regions.
