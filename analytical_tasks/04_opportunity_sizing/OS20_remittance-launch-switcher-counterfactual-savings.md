# OS20 — What the Kenya launch saves senders in its first year, when the people who switch to a 1.8% app are mostly already on a 3% one

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · cross-border remittances |
| Mirrors | Stating the customer savings or consumer surplus a low-price entrant creates, when the customers it wins are mostly switching from other low-cost options (Wise and Remitly impact claims, neobank fee-savings reports, Amazon or Google price-comparison claims, telecom challenger "savings vs your current plan" figures) |
| Decision shape | One figure committed at a date: the year-one savings to senders in the launch report due to the impact investor on 15 December |
| Committed call | The savings the service brings senders in the Kenya corridor's first year, to the nearest $10,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S10, a constructed counterfactual for the covenant's causal verb, built from the senders who actually switch, with a firm-wide registration limit applied in the figure (#10) below it |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #13 validates on one population, applies to another · #10 notes a binding limit as a risk · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: the two corridors launched last year, with monthly volumes against the capture model, the firm's monthly totals against its registration limit, and the savings reported to the investor |
| Driving force | The covenant counts what the service's senders pay less than they otherwise would, and a sender's "otherwise" is the provider they used before. The senders who move to a 1.8% app are mostly already on a 3% app: the waitlist's linked-account histories put 80% of its volume with digital money-transfer apps, which carry 50% of the corridor. The market-weighted cost the existing book confirmed is right for the corridor and wrong for the switchers, and the launched corridors could not show the difference, because no digital app paid out in either. |

## 1. Situation

A UK money-transfer start-up launches its Kenya corridor in January. Its covenant with a development-finance investor requires the launch
report, due on 15 December, to state the savings the service will bring senders in the corridor's first year. The deck took the corridor's
$1.2 billion annual flow, the year-one capture model and the World Bank RPW simple average cost. The pack holds the RPW quotes by
provider type, the Kenyan central bank's inbound shares by provider type, the firm's registration as a small payment institution, the
existing book from its two launched corridors, and a waitlist of 11,800 UK senders who signed up for Kenya and linked a bank account.
The CEO says every dollar moved instead of through a bank saves senders nearly eight cents.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the RPW quotes, the central bank's shares, the capture model, the registration limit, the existing
  book and the waitlist histories. The market-weighted cost really is what the corridor pays. No stakeholder read is overturned. The
  difficulty is whose costs the covenant's "otherwise" refers to.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CEO's view and the deck. The central bank's shares, the RPW quotes and the registration limit still give a
  clean, certified $0.77M.
* **Instrument repair.** The suspect file is the waitlist, 11,800 sign-ups standing for every year-one sender. Fill it with every year-one
  sender's prior provider: in the launched corridors the waitlist sent 96% of year-one volume with the same mix, so the answer holds; rung 0
  still returns $1.55M, rung 1 $1.15M and rung 2 $0.77M, none of which reads the waitlist, and the switchers' counterfactual is still
  needed.
* **Lens swap.** The naive read prices the corridor's senders. The answer prices the senders who will switch, a different population with
  its own prior costs.

## 3. The driving force

A strong solver replaces the RPW simple average (6.1%) with the cost weighted by the central bank's provider shares (5.0%), because
banks quote high and carry little volume. It finds that the firm's registration caps its total payment volume at an average of $3.25M a
month, of which the two running corridors use $1.25M, so Kenya can carry $24.0M in year one, not the $36.0M the capture model projects.
That gives $0.77M, and the existing book agrees: last year's reported savings, priced on market shares, matched what switchers had
paid before. But in those corridors no digital app held a payout licence, so switchers came from banks and cash agents in proportion. In
Kenya, apps carry half the flow and they are where switchers come from. The waitlist's linked accounts show 80% of its volume going
through apps at 3.0%, so the senders' own prior cost is 3.8%, the saving is 2.0 points, and the figure is $0.48M.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Projected year-one volume × (RPW simple average − 1.8%) | $1.55M (+223%) | The deck's sizing, on the World Bank's published figure | The central bank's provider shares: banks quote 9.4% and carry 10% of the flow; apps quote 3.0% and carry 50% |
| 1 | Projected volume × (cost weighted by provider shares − 1.8%) | $1.15M (+140%) | Volume-aware pricing, and the existing book's reported savings used exactly this weighting | The registration: the firm's volume may average no more than $3.25M a month, and the running corridors use $1.25M |
| 2 | Volume capped at the registration headroom ($24.0M) × the market-weighted saving | $0.77M (+60%) | The binding limit applied, and the existing book certifies the market-weighted saving | The waitlist's linked-account histories: 80% of its volume goes through apps, against their 50% share |
| 3 | **Decisive:** capped volume × (the switchers' own prior cost, from the waitlist histories by volume − 1.8%) | **$480,000** | — | — |

* **Figure shape.** Every correction walks the figure down and the answer is the minimum cell; the decisive move removes 38% of the
  rung-2 figure.
* **Partial correction priced (L3).** A solver who takes the waitlist's mix by senders rather than by dollars sent (70% apps) lands at
  $0.60M (+24%). One who applies the switchers' mix only to the volume the waitlist pledged (half of year one) and the market mix to the
  rest lands at $0.62M (+30%). One who checks the registration against Kenya's projection alone finds $39.0M of room, never binding, and
  lands at $0.72M (+50%).
* **Grid.** Cost (simple average, market shares, switchers' mix) × volume (projected, capped at the headroom) gives 6 cells: $1.55M,
  $1.03M, $1.15M, $0.77M, $0.72M and the answer. The nearest wrong cell is $0.72M (+50%), and it ignores a limit the policy says must
  hold.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The covenant defines savings as what the service's senders pay less than they would have paid without it. No
   document says who those senders are or where their prior costs live.
2. **Corpus blind for a computable reason.** *In both launched corridors the switchers' own prior cost equalled the market-weighted cost,
   because no digital app held a payout licence in either receiving country, so switchers came from banks and cash agents in proportion to
   their shares.* Last year's reported savings reconcile to the switchers' histories in both corridors.
3. **No arithmetic symptom.** The weighted cost ties to the RPW type averages and the central bank's shares, the headroom to the
   registration and the running corridors' totals, and the waitlist's volume to its linked accounts.
4. **Not a row predicate.** The switchers' cost needs every waitlist account's twelve-month payments classified by provider type through
   the payments taxonomy, weighted by dollars sent, and priced at each type's RPW cost.
5. **The enumeration is arithmetic.** No column gives a sender's prior cost; 11,800 linked-account histories are classified and summed.
6. **No cutover date.** The waitlist histories cover a stable year, and no series steps.
7. **Survives deletion.** Removing the deck and the CEO's view leaves the existing book certifying the market-weighted saving.

## 6. The calibration corpus

* **Form.** The existing book: the two launched corridors' monthly volumes for their first year, the firm's monthly totals against the
  registration limit, the savings reported to the investor, and the switchers' linked-account histories.
* **What it certifies.** The capture model's ramp, 24 of 24 months within 3%; and market-weighted pricing, whose reported savings
  reconcile to the switchers' own prior costs in both corridors. Waitlist sign-ups sent 96% of each corridor's year-one volume.
* **What it is blind to.** Selection into switching (above).
* **Twin pair.** The waitlist's London and Birmingham sign-ups are identical on count (2,400), pledged monthly send ($210), funding method
  and recipient regions. London's prior volume went 95% through apps and Birmingham's 50%, with the rest through cash agents, so they
  save 1.36% and 2.80% of each dollar sent, 2.1× apart. Only the payment histories separate them.
* **Resemblance points at the decoy.** By flow, send size and sender count, Kenya most resembles the larger launched corridor, where the
  market-weighted saving was confirmed to the dollar.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The covenant: savings are what the service's senders pay less, in fees and exchange margin, than they would have paid
  without it, over the corridor's first twelve months, in US dollars. The firm's registration: its payment volume may average no more than
  €3 million ($3.25M at the regulator's rate) a month, and the compliance policy declines volume beyond it until authorisation, which is
  not expected in year one. The price list: 1.8% all-in at every send size. The payments taxonomy: merchant codes to provider types.
* **Empirical pins.** Type costs, from the RPW quotes at the corridor's $200 band. The capture model, from the existing book. The
  switchers' mix, from the waitlist histories.
* **Voices.** The CEO: "Every dollar we move instead of a bank saves our senders nearly eight cents." The head of growth: "Kenya will be our
  fastest launch yet."
* **Licensed wrong basis.** The covenant records that the investor's verification agent checks reported savings against corridor flow ×
  the RPW average cost gap and will present that comparison.

## 8. Determinism by construction

* **Classification.** Every remittance payment in the waitlist histories carries a merchant code the taxonomy maps to one provider type;
  none is unmapped.
* **Weights.** Shares are by dollars sent, the covenant's unit; the waitlist's dollar mix is 80% apps, 15% cash agents and 5% banks.
* **Costs.** The RPW type averages (apps 3.0%, cash agents 6.2%, banks 9.4%, post 7.2%) are unchanged across the last four quarters.
* **Headroom.** The running corridors carry a steady $1.25M a month, so the twelve months of year one are the binding window and Kenya's
  headroom is $24.0M under any month-by-month throttle.
* **Coverage.** In both launched corridors the 4% of year-one volume sent by senders outside the waitlist had the waitlist's prior-provider
  mix within one point.
* **Rounding.** $24.0M × 2.0 points is exactly $480,000.

## 9. Prompt sketch and deliverables

> The Kenya launch report goes to our impact investor on 15 December and has to state what the service will save senders in the
> corridor's first year, to the nearest $10,000. Our CEO's view is that every dollar we move instead of a bank saves senders nearly eight cents.
> Give me the figure as a sentence for the report, with `savings_bridge.xlsx`, a chart `who_switches.svg`, and a short `covenant_note.md`.

* `savings_bridge.xlsx` — the figure on each of the four bases, the headroom build, the cost by provider type and mix, the payout sheet
  (ask A) and the retention sheet (ask B).
* `who_switches.svg` — a script-rendered pair of stacked bars, the corridor's flow and the waitlist's flow by provider type, each segment
  labelled with its RPW cost, the weighted cost of each bar marked against the 1.8% price line, and the gap between them shaded as the
  saving.
* `covenant_note.md` — the committed figure and the bridge from the deck's $1.55M.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each launched corridor and quarter, the share of transfers paid out within ten minutes and
  the median minutes to payout. *Device:* a payout retried after a recipient-side failure is logged as a new payout carrying `retry_of`,
  and the operations guide times a transfer from its first attempt to its successful payout. Timing retries from their own start
  understates payout time in the four quarters with the most wallet failures.
* **Ask B (device-carried).** For each launched corridor, the share of month-one senders still sending in months three, six and twelve.
  *Device:* a sender who re-verifies identity after a document expires gets a new customer number carrying `supersedes`, and the growth
  guide follows the original number. Following new numbers as new senders understates retention in the corridor with most expiries.
* **Ask C (validity).** The figure under each of the four rung bases, the cost under simple, market and switcher weighting, and the
  launched months reproduced (of 24) by the capture model.
* **Decoupling.** Pricing savings on the market mix instead of the switchers' changes no figure in asks A or B. Payout logs and customer
  records touch neither the waitlist histories nor the RPW quotes.

## 11. Rubric arithmetic

8 corridor-quarters × 2 (ask A) + 2 corridors × 3 months (ask B) + 4 bases, 3 costs and the reproduction count (ask C) + the committed
figure, the headroom and the switchers' cost + 5 named chart parts + 3 files ≈ 41 criteria.

## 12. World-building constraints

* Corridor flow $1.2B a year; year-one capture 3% ($36.0M), ramping from $1.0M in month 1 to $5.0M in month 12. Registration limit
  $3.25M a month on average; running corridors $1.25M a month; Kenya headroom $24.0M.
* Provider types (apps, cash agents, banks, post): RPW cost 3.0% / 6.2% / 9.4% / 7.2%, simple average of quotes 6.1%; corridor shares 50%
  / 32% / 10% / 8% (5.0%); waitlist dollars 80% / 15% / 5% / 0% (3.8%); waitlist senders 70% / 20% / 10% / 0%.
* Rung figures $1.548M / $1.152M / $0.768M / $0.480M.
* London and Birmingham sign-ups match on every waitlist column outside their payment histories.
* Payout logs and customer records never touch the waitlist, the RPW quotes or the registration totals.
