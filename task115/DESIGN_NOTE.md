# task115 design note

Domain Marketing & Consumer Research (author-declared at /build, 2026-10-08, tag confirmed by the author at checkpoint A; vocab key
`marketing-consumer-research`, subdomain `pricing-promotion`). Objective Forecasting & Predictive
Modeling. Shape 07, grid of cells. Decision pick_one_of_n with a licensed non-pick.

## DRAW

```
Card filed with guard.py register before the ladder was written? yes (2026-10-08)   Verdict: PASS, no WARN
Shape: 07 grid of cells (regions x mechanics)   Gate G mechanism: forecasting
Gap: time (decisive), population   Pattern: D (decisive), E behind it   Generators: G2, G14, G16
Domain: marketing-consumer-research   Subdomain: pricing-promotion   Objective: forecasting
Pairing repeated from last build? no (domain never drawn before)
Stakeholder role: revenue growth manager at a branded tea company (research_desk)
Context-artifact type: close_out_summary (the symbol group's 2026 deal-event recap)
Calibration form: existing_book_actuals (Delahunt's own closed deal events)
Decision type: pick_one_of_n (the group's March event menu: Save a third, Save 40%, Half price,
  a money-off deal), or sit the event out
Forum: executive_team   Forcing event: vote_or_meeting (the group's event selection meeting)
Org family: manufacturer   Geography: Ireland, EUR
Decisive mechanism: a deal earns own-label switching only in the store-weeks where its deal price
  sits at or below that store's own-label shelf price; measured on the deal line itself in other
  brands' deals (twice the packs own label loses), applied store by store
Repeats from prior builds: none on the structural keys (guard PASS); nearest driver 0.04
```

**Decisive rung from the measured catalogue.** Trap 13, *validates on one population, applies to
another*: Delahunt's own deal curve fits every one of its closed deals (all Save 20% and Save 25%,
none below own label anywhere) and gets carried to mechanics that cross own label in some stores.
Behind it, trap 14 (*coarsens the segment*: the crossing tested against the chain-average own-label
price) and trap 25 (*assumes an effect the log could measure*: the switch is in the scan data
around other brands' deals). The measured architecture (pattern B with a reproduction clause) is
not available this draw: B, A and C carry the decisive rung of task109, task114 and task116. task116
also names trap 13, on a different mechanism (trusts that buy centrally); the trap number is a
component, the driver is not shared.

**Nearest exemplars read.** *Capital Grant Drawdown Forecasting* (0.34): a schedule field fits every
paid certificate and is stale for the awards not yet drawing, the nearest forecasting architecture
to a curve that fits every closed case. *Lifecycle Campaign Prioritization* (0.50, the client's only
Marketing & Sales exemplar): its difficulty was log coverage, not an analytical gap, so there is no
measured marketing architecture to lean on and the rung is named by trap number.

**Similarity claim.** No prior build turns on a response that exists only where a planned price
crosses a rival line's own price at the same point, measured from the rival line's volume during
other subjects' moves and tested point by point.

## GATE G

- **Litmus.** No reported figure is wrong or misleading and nothing is overturned. Delahunt's own
  deal lifts are measured correctly, the group's recap uplifts are correct for the lines and events
  it lists. (The 2026 debit-note errors are Ask C's devices and sit off the main call's path.) The March
  menu goes deeper than any deal
  Delahunt has run, and at some of those depths Delahunt's deal price falls to or below the
  own-label 160s shelf price in some stores. Own-label buyers switch only in those store-weeks, so
  the forecast needs a component that no closed Delahunt deal contains: it is measured from other
  brands' deals and applied store by store.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Primary mechanism:** forecasting (a forecast the correctly read past does not pin).
- **Delete every wrong number from the pack.** There are none to delete. Still hard because the
  crossing component appears nowhere in Delahunt's own record and nowhere in any document.
- **Clean-data test.** On perfectly clean data the switch still has to be found and tested store by
  store. Asserted in the generator at stage 3.
- **Lens-swap test.** The naive read and the answer are not one number under two lenses: the answer
  adds a component built from another line's prices and volumes, measured from other brands' deals.
  Rung 3 against rung 4 is not one either: rung 3 reads one line's loss (own label, down 0.35 of
  normal), rung 4 reads a different line's gain (the deal line, up 0.70 of own-label normal).
- **Pre-draw identity.** Event cases = sum over stores of base x (1 + deal lift at the depth) + the
  switch share x own-label base in the stores where the deal price crosses. The switch term is
  neither filed nor visibly forced, so the identity does not close over shipped quantities.
- **Corpus direction.** Under the naive path Delahunt's own event corpus reproduces: its curve fits
  every closed Delahunt deal exactly, because none crossed own label (L1). Under rung 3 (one-for-one
  transfer of the own-label loss) the recap refutes: every all-crossing cycle is under-predicted by
  19 to 28 per cent, while the deal-line measure fits each within 1 per cent (asserted). A solver
  that back-tests its switch against the recap escapes rung 3; that is the known leak of this rung.

## STUMP

A competent solver either never finds the switch, fits Delahunt's own Save 20% and Save 25% deals and
sits March out, or finds it the way the data shows it first, own-label 160s sales falling by about a
third wherever another brand's 160s deal undercut the store's own-label price, credits those lost
packs to the deal line one for one, forecasts Save 40% at 2.2 times base and offers half price; the
step that lands it there is never measuring the response on the deal line itself, which in those
store-weeks sold twice the packs own label lost, enough to put Save 40% at 2.7 in the stores whose
own-label price is highest.

## ENTITY, UNIT OF VALUE, DECISION

Delahunt Tea sells its Original 160s into Tullan Grocers, a franchise symbol group of about 180
member stores on three store price files (Value, Core, Premium) that each member subscribes to.
Tullan's Big Deals run in three-week cycles; March 2027 (w/c 1, 8, 15 March) has one tea slot.
Delahunt funds the shopper's saving on every deal pack. Two quantities both read as how well a deal
works: the multiple a line's own deals delivered, and the multiple the deal will deliver at a
price that crosses own label. They rank the menu differently because only the second carries the
switch.

Decision: exactly one of {Save a third, Save 40%, Half price, EUR 2.40 off} on the Original 160s,
or sit the event out (licensed), chosen as the cheapest deal whose forecast clears Tullan's floor:
event units at least 2.5 times base over the three weeks, across participating scanning stores, on
the brief's base (13 weeks w/c 29 Jun to 21 Sep 2026, weeks with a record and off deal, averaged
per store, summed).

**ANSWER: Save 40%, forecast 2.7 times base** (2.7117 as built, 8.5 per cent over the floor). Packs
over the three weeks graded to the nearest thousand: 36,155 as built, filed as 36,000. Every graded
figure sits off-centre inside its bin (asserts.py section 6), never on the round value.

## WORLD PARAMETERS (design targets; the generator computes and asserts the actuals)

- Deal price = store regular price less the deal, rounded down to the cent (filed in the brief).
- Pure deal lift, common to every tea line, piecewise linear in depth: 20% 0.40, 25% 0.56, a third
  0.720, 40% 0.732, half 0.86 (world.KNOTS). Measured from the feed (13-week pre-windows, pooled):
  0.70 at a third, 0.73 at 40%, 0.87 at half. Money-off deals take the depth the saving is of that
  store's price.
- The switch: in a store-week where a branded line's deal price is at or below that store's regular
  price for the own-label line of the same bag count, own-label units fall to 0.65 of normal and the
  deal line gains 0.70 of own-label normal (world.SWITCH_LOSS 0.35, SWITCH_GAIN 0.70: switching
  shoppers buy two packs on deal for each own-label pack they drop). Absolute: no store-week in history sits within EUR 0.10
  of the boundary on either side.
- Prices to Dec 2025 / from 5 Jan 2026. Own label 160s: Premium 4.29/4.39, Core 3.69/3.79, Value
  3.29/3.39. Delahunt 160s: 6.79/6.99, 6.29/6.49, 5.79/5.99. Carrow 160s (mainstream): 5.39/5.49,
  4.79/4.89, 4.59/4.69. Carnmore 160s: 5.19/5.29, 4.69/4.79, 4.19/4.39. Rathmore Reserve 160s
  (luxury): 7.39/7.59, 6.69/6.89, 6.19/6.39. Own-label RRP (Core price): 3.69 in 2025, 3.79 in 2026.
- March 2027 Delahunt deal prices (Premium/Core/Value): third 4.66/4.32/3.99, Save 40% 4.19/3.89/3.59,
  half 3.49/3.24/2.99, EUR 2.40 off 4.59/4.09/3.59. Against own label 4.39/3.79/3.39, Save 40%
  crosses Premium only (margin 0.20), EUR 2.40 off crosses nowhere (0.20/0.30/0.20), a third
  nowhere, half everywhere. Against the RRP 3.79, Save 40% and EUR 2.40 off both cross Value only.
- Own-label 160s normal volume: Delahunt 160s x 3.93 / 3.05 / 3.85 (Premium / Core / Value) times
  a store draw, with per-region multipliers on Delahunt and on Premium and Core own label
  (simulate.DEFAULT_TUNE) solved so every graded cell sits off-centre in its bin and survives the
  estimator variants. Own label is 3.6 times Delahunt's base chain-wide. Christmas weeks x1.03,
  otherwise no seasonality; units are Poisson by inverse CDF from fixed uniforms (common random
  numbers), so a retune moves only the counts it touches.
- Tea cycles as built (world.EVENTS, 21 of them on the three-week grid): Delahunt Gold 80s Save 20%
  BD24-16; Carrow 160s Save 25% BD25-01 (Premium and Core cross, Value not); Wildmeadow Green 40s
  half BD25-02; Delahunt 160s Save 20% BD25-03; Rathmore 160s Save a third BD25-05 (none); Carrow
  160s Save a third BD25-07 (all); Delahunt 160s Save 25% BD25-09; Wildmeadow Green Save 40% BD25-10;
  Rathmore Save 40% BD25-11 and BD26-06 (none); Carnmore 160s EUR 1.50 off BD25-13 (all); Carrow
  120s half BD25-14 (no own-label 120s); Delahunt 80s Save 25% BD25-15; Carrow 80s Save a third
  BD25-16 (all, against own-label 80s); Carnmore 160s Save a third BD26-02 (all); Wildmeadow
  Peppermint Save a third BD26-03 and Save 40% BD26-11; Delahunt 160s Save 20% BD26-04; Carrow 160s
  half BD26-08 (all); Wildmeadow Chamomile half BD26-10; Delahunt 160s Save 25% BD26-13. The 160s
  crossings are 18 weeks apart and none falls in the March base window. BD25-01 carries both
  refutations of the RRP reading: Value stores priced below the RRP do not switch, Premium stores
  priced above it do.

## LADDER

```
RUNG 0  Delahunt's own curve (its Save 20% and Save 25% cycles, each reproduced by its own
        reviews) carried to the menu, linear: third 1.80, EUR 2.40 off 1.91, Save 40% 2.00,
        half 2.28 -> SIT OUT (none clears)
        killed by: the own-label 160s collapsing to 0.30 in exactly the crossing store-weeks of
        other brands' deals, and Rathmore's Save a third / Save 40% at 1.66 / 1.75 (the lift
        flattens below Delahunt's extrapolation)
        stop sentence: the brand's own record fits every closed deal and the recap agrees with it
RUNG 1  the recap's multiples by mechanic (mainstream lines dominate): Save a third mean 2.57,
        median 2.67, Save 40% 1.74, half 2.19 -> SAVE A THIRD clears
        killed by: Rathmore's Save a third at 1.66 and the crossing law (the mainstream deals
        crossed own label in every store)
        stop sentence: the group's own record of what each mechanic delivered
RUNG 2  switch found, crossing tested at the own-label RRP (or the chain-average price)
        -> EUR 2.40 OFF at 2.61 (crosses Value stores, clears; Save 40% 2.62 funds more)
        killed by: each store's own-label regular price in the feed (Value 3.39 < 3.59) and
        Carrow's Save 25% Value-store weeks (below the RRP, no switching)
        stop sentence: the law is found and applied with Tullan's published own-label price
RUNG 3  crossing tested store by store, the switch read off the own-label loss and credited one
        for one (0.35 of own-label base) -> Save 40% 2.22, short; HALF PRICE 3.13 is the only
        deal clearing
        killed by: the deal line's own units in the crossing store-weeks (0.70 of own-label base,
        twice the loss), which the recap's crossing cycles reproduce and one-for-one misses by
        19 to 28 per cent
        stop sentence: the switch is found, measured where it is visible, and applied store by store
RUNG 4  the switch measured on the deal line -> SAVE 40% (Premium stores cross), 2.7117, cheapest
        clearing
```

Every rung names a different option. The decisive rung is rung 4 (trap 25, an effect the log could
measure, with trap 4 behind it: the recap is the control a one-for-one reading never tests); rung 3
is the stop the v1 portal response passed through; rung 2 is the trap 14 stop.
Variant paths: Rathmore as the closest analog (third and Save 40% both fail) lands on EUR 2.40 off
or half price; a convex extrapolation of Delahunt's curve lands on half price. None reaches Save 40%,
because the only Save 40% evidence in the recap is Rathmore at 1.75, which fails.

**Seven survival properties of rung 3.** 1 no sentence in any file names own label, switching or
price crossing. 2 Delahunt's corpus is blind (L1 sentence below) and the recap prints multiples
only. 3 every rung completes and ties. 4 the test reads another entity's price (own label's, per
store-week) through a join nothing signposts, and the share is measured from other brands' deals.
5 the crossing set is arithmetic on prices. 6 no cutover date. 7 deleting nothing changes it.

**L1.** In every closed Delahunt deal the deal price sat at least EUR 0.80 above the own-label
160s regular price in every store, because its deepest mechanic was Save 25% and its regular
price is at least 1.58 times own label's, so its own curve reproduces every one of them with no
switching term.

**Margins (asserts.py sections 2 and 3).** Save 40% 2.7117 against the 2.5 floor (8.5 per cent
clear). EUR 2.40 off 1.7173 and Save a third 1.6998, both over 25 per cent short. Half 4.4099,
clears, funding 1.98 times Save 40%'s. Under rung 3 Save 40% is 2.2161 (11 per cent short) and half
3.1286. Under the RRP reading EUR 2.40 off clears at 2.6142 and funds EUR 83,651 against Save 40%'s
EUR 88,758, so rung 2 never names Save 40% (in Value stores both deals price at 3.59, so whenever
Save 40% crosses there EUR 2.40 off does too, more cheaply).

**Rival sweep as asserted (asserts.py section 4).** Own curve: linear, proportional and power sit
out; exponential and quadratic name half price. Recap mean, median and 160s-only name Save a third.
Rathmore as the closest analog, a depth regression over the recap and the pure lift with no switch
all sit out. A chain-level regression of multiple on deal price over own-label price names half
price; the floor read per region names half price (the brief pins chain-wide). Crossing at the RRP
and at the chain-average own-label price (3.91) name EUR 2.40 off. Two readings converge on the
answer (C1): store-level crossing with Appendix B ignored (2.7083) and crossing against 2025
own-label prices (the same store set crosses).

## DETERMINISM CLOSURE (the 22 axes)

| # | Axis | Reading chosen | Closed by |
|---|---|---|---|
| 1 | Population | participating scanning stores (brief, Appendix B) | filed rule; Appendix B chosen chain-neutral (C1: all four chain multiples identical to one decimal with or without it, asserted); it does move regional cells and every base, which is the D5 ask hazard |
| 2 | Unit of account | selling unit (a pack) for every line | feed spec; same bag count pairs lines (C1, no mixed packs on the main path) |
| 3 | Attribution window | event weeks w/c 1, 8, 15 Mar 2027 | brief |
| 4 | As-of dating | each store-week's own regular prices | feed; March prices = current (Tullan circular: no tea price change before April 2027) |
| 5 | Version basis | n/a on the main path | C1 |
| 6 | Divisor | base per the brief | filed |
| 7 | Weighting | chain units over chain base (volume) | brief defines the ratio on totals |
| 8 | Window length and estimator (lift, switch) | 13 weeks before each cycle, pooled, switch on the deal line | C4: six variants (8, 10 and 13-week windows, the recap's 8 weeks ending two before, mean of cycles) keep the pick and all 25 graded cells in their bins (worst margin 0.0112); the 26-week window reads the previous crossing cycle's own-label weeks into the base (share 0.727) and moves the five half-price cells only; the own-label loss read one for one is rung 3 |
| 9 | Boundary inclusivity | at or below | C1: no store-week within EUR 0.10 of the boundary, history and March |
| 10 | Rounding path | deal price rounded down to the cent | brief; margins of 0.10 make the path irrelevant (C1) |
| 11 | Tie-break | cheapest among clearing deals | only Save 40% and half clear; half funds 1.98 times Save 40% |
| 12 | Maturity | n/a (closed events complete) | C1 |
| 13 | Order of operations | lift and switch additive per store | C1 (one composition reproduces every event) |
| 14 | Row order | n/a | C1 |
| 15 | Duplicate resolution | n/a on the main path (devices off it) | separation zero-counts |
| 16 | Identity normalisation | store numbers summed; re-numbered and reissued stores inert on chain totals | C1, asserted |
| 17 | Netting | n/a | |
| 18 | Dimensional units | packs | feed spec |
| 19 | Code semantics | deal_code marks central deals only | feed spec |
| 20 | Integerisation | forecast packs to the nearest thousand, base in whole packs | prompt; worst variant margin 290 packs; regional bases in whole packs add to the whole-pack total (4,444) |
| 21 | Scope of a clause | the floor governs the line chain-wide, not each region | brief |
| 22 | Forward window contents | three weeks, participating scanning stores, March prices | brief, Appendix B, price hold to 5 April; C1 on the two island stores: a returns-based Save 40% forecast for them adds 155 to 163 packs and leaves the chain and West & North West packs in their thousand bins (West & North West margin 156), asserted |

## ASK SHEET (supplemental-stumping; pair ceiling at the end)

Files: `march_offer_paper.pdf` (commits; leadership team) and `march_offer_workings.xlsx`
(Tullan's offer form and finance). Shape 07: rows are Tullan's four trading regions, columns the
four deals.

| Ask | Figures | Layer | Primary device | Hazards | Use |
|---|---|---|---|---|---|
| A. every deal's forecast multiple chain-wide and by trading region, one decimal | 20 | construction x region | D2 region vintage: the Jan 2026 member list against the July 2026 area changes (21 moves), with nine moves dated May 2027 that must not be applied | H1 re-numbered store 0147 to 0388; H2 reissued store number 0119 | leadership reads the grid; the offer form needs the offered deal by region |
| B. base packs a week by region and in total as Tullan measures it; the offered deal's packs by region to the nearest thousand | 9 | base: off the trap; packs: construction x region | D5 participation (Appendix B, 11 stores) | D4 missing store-weeks are no record, never zero (feed spec), H1, H2 | Tullan's offer form |
| C. the two 2026 deals: invoiced, the amount the deal terms support, difference, ex VAT, whole euro | 6 | decoupled audit of the funding input | D1 a re-issued September debit note replacing part of the original, with three week-1 top-up lines that are genuine | D4 non-scanning stores claim from monthly returns (genuine), H2 reissued 0119, a March claim for a store on refit (not participating) | finance disputes the overcharge before signing |

Main-call row population: scan rows of all tea lines for participating scanning stores, all weeks;
it reads no region, no claim, no debit note and no manual return. Zero-counts asserted in stage 3:
device rows inside it 0 (region and claims devices live in other files); the H1/H2 and D4 rows that
do sit in the scan feed are asserted inert on the main call (pick and multiple unchanged under every
mishandling).

Device bite as built (asserts.py section 9): the January list alone moves 9 of 25 cells and all four
regional bases; the May 2027 moves applied move 6 cells and two bases; missing store-weeks read as
zero move the Dublin, Midlands and total bases; ignoring Appendix B moves every base and the chain
packs (38,740 against 36,155); dropping 0388 moves the Dublin base. Every one leaves the pick and the
2.7 untouched. Claims wrong paths: re-issue assumed credited (difference 0), original note only
(-612), returns left out (4,773), gross of VAT (14,130), Finglas kept (0). Cells a wrong rung still
earns: rung 2 shares the five Save a third and five half-price cells with the golden (no crossing
difference at those depths); rung 0 shares none on the linear fit, the five Save a third cells on
the proportional fit.

Pair arithmetic (planning weights 38 / 7 / 55): Ask A about 20 of 35 ask criteria, B 9, C 6. A
response that lands Save 40% and takes the region vintage at face value keeps the chain-wide four
and loses most of the regional sixteen; a response off the call loses A and the packs in B
entirely. Target leakage: cracker about 0.35, mirror about 0.15, so 55 x 0.50 = 27.5 against the
28 - r ceiling with r about 5. Tight; the device density in C and B is where the margin is bought,
and the pair simulation in stage 3 decides whether a further hazard is needed.

## STOPPING RULE

Two consecutive portal results where both top responses file Save 40% re-root the decision. One
response on Save 40% with the pair above 40 licenses one ask-layer repair. A result where no
response files Save 40% and the pair sits under 40 files the build as at-ceiling.

## PORTAL LOG

- P1, 2026-10-09: "the model found 1/2 ground truth answers", read as one of the two top responses
  filing Save 40%; route not recorded. Changed one mechanism: the own-label loss halved to 0.35 with
  the deal line's gain kept at 0.70, so a one-for-one reading of the own-label drop lands on half
  price. The prompt was also replaced by the author's humanised version (P2 presupposition leaks
  fixed: no ask presupposes a deal is picked or that the billing differs).

## BUILD RECORD (stage 3)

Generator: world, stores, simulate, claims, pack, docs, build (pack), golden (figures from target/
only), deliver (goldens), seal (container metadata, file times, archives), asserts (86 checks, two
rebuilds byte-identical), tune (solver for the per-region multipliers); verify_pack.py at the task
root (57 checks, shares no code with the generator). Order: build, deliver, asserts, seal, verify.

**leak.py REVIEW lines, each harmless.** RRP PDF carries 3.79: it is the own-brand RRP, the anchor
of rung 2, filed where an RRP belongs. Brief, recap and thread carry the committed call's words: the
menu, the line and the month are the brief's own subject, and none of the three names Save 40% as
the pick. Brief, recap and area notice carry stump-paragraph words (stores, closed, measured,
mechanic, question, forecasting): Appendix B's refit dates, the base clause, the recap's note and the
notice's "supplier forecasting from that date", which is the D2 device's filed rule; none names the
own-label crossing. Area notice and member list name three answer-set candidates beside numbers:
the candidates are trading regions, listed per store, not ranked on any question. The feed CSV carries "26,155": a field boundary (26 units, then EUR 155.74 sales), not the golden's EUR 26,155.

**House fixes applied before ship.** H1: seal.py writes each file's in-fiction author and date into
the container, blanks the writer's comment lines, pins zip entry times, sets file times; audit
clean. H5: the claims ask read "what our scan data and the deal terms support", which a reader can
take as excluding the island stores' manual returns; now "the amount the deal terms support". H6:
the golden's switching rule now says "another brand's 160s" (same bag count), since an 80s or herbal
deal priced under own-label 160s moves nothing. H16: the recap was dated before BD26-13 closed. H21:
two invented brands sat on real Irish names. Persona: the area notice's contact is drawn and carded.

**Ask C and H18.** The 2026 billing check audits the funding input the cheapest-deal test consumes
(what Delahunt actually pays per deal pack under Tullan's terms), and the prompt makes it the sign-off
condition for the offer. H18's ledger test names a different window (2026) for it; recorded here so
the author weighs it at /approve.

## Tried and rejected

- Draw candidate, spot-TV plan (per-market concave response times distribution): the identity closes
  over a filed response curve, a filed plan and a filed distribution table, so the forward window has
  every input filed and the per-market sum is a computation.
- Draw candidate, range-review demand transfer by store-cluster availability: availability of the
  alternative is the first question any transfer analysis asks, so the decisive question is asked,
  and household duplication already encodes it for the stores that never ranged the alternative.
- Draw candidate, coupon-acquired triers repeating less: the class is the unit's own history read
  through a separate log with a zero-yield outcome, task76's and task83's structure, so the driver
  sits too near a spent one.
- Draw candidate, TV audience flow after a lead-in change: the law is a respondent-level viewing
  model (noisy, so Gates A to E split), and a single-panel world cannot carry eight-file ask paths.
- Draw candidate, loyalty-price promotions reaching only carded sales: the member-only mechanic is
  the forcing event itself, so the solver is told what changes and asks the decisive question first.
- First cut of this draw as shape 04 with a depth dial, a counterparty forum, a purchase-order event
  and a prior-period close-out: all four blocked by task114, registered the same day; redrawn to
  shape 07, a mixed-mechanic pick, executive_team, vote_or_meeting and existing_book_actuals.
- Tuning every graded multiple onto its round value (all within 0.003): a receipt, because a solver
  comparing its rung 2 and rung 3 grids could pick the method whose figures land round; retuned to
  off-centre targets whose worst variant margin is 0.0088.
- Delahunt's own lift at 0.42 and 0.55 (Save 20% and 25%): its curve then carried Save a third to
  1.73, the golden's 1.7 bin, so rung 0 earned the five Save a third cells; steepened to 0.40 and
  0.56 (rung 0 third 1.80), which moves no menu figure.
- Forecast packs to the nearest 500: the gain-side and 26-week estimators moved regional packs across
  500-pack edges; graded to the nearest thousand instead (worst variant margin 191 packs).
- Claims ask worded "what our scan data and the deal terms support": the scan-data-only reading
  leaves the island returns unsupported and files 302 and 4,750; reworded to the deal terms alone.
- Brand names Oatfield (calendar) and Abbeyfield (tea): real Irish organisations; renamed Ardfin and
  Carnmore in the generator. Kilbrin also rejected (a real Irish whiskey).
- Recap dated 2 October 2026: it reports BD26-13, which closed on 4 October; dated 6 October.
- v1, own-label loss equal to the deal line's gain (0.70 each): one of the two portal responses
  landed Save 40% (route not recorded); with loss equal to gain, the switch read off the own-label
  drop and credited one for one was already the right forecast, so finding the drop was the whole
  climb. Halved the loss and kept the gain, so that reading now offers half price.
