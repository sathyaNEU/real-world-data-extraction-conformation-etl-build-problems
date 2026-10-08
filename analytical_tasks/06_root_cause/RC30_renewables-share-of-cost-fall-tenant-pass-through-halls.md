# RC30 — How much of the data-centre operator's fall in power cost the renewables build-out delivered, when two-fifths of its metered load is a tenant's

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · wholesale power and energy procurement |
| Mirrors | Input-cost attribution at hyperscale and colocation operators (Google, Meta, Microsoft and Equinix energy procurement), where tenants' pass-through load sits inside the operator's meters and changes what the market's cheaper hours did for the operator's own bill |
| Decision shape | One figure committed at a date (a component): the renewables build-out's share of the fall in the operator's own cost of power, filed in the solar PPA business case at signing |
| Committed call | The euros per megawatt-hour, to one decimal, by which the renewables build-out lowered the operator's own cost of power between the two years |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S1 (the operator's exposure is not its meters), reached through a mixed segment that a lease clause splits |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #6 treats a mixed segment all one way · #17 guesses an attribution the data can settle · #12 stops at the first control that passes |
| Calibration form | Parallel-run overlap: eight weeks in which the old site-tagged meter feed and the new feed ran side by side, with the supplier's invoices for the same weeks |
| Driving force | A cloud tenant leases one hall at each of three sites, and the lease re-bills each hall's power to the tenant at the operator's hourly cost. The halls are 40% of the operator's metered consumption, and the tenant schedules its training into the midday price dip. The supplier invoices reconcile to the site meters exactly, so the gross metered profile reads as the operator's own, with a midday hump the operator's own flat load lacks. On the gross meters the build-out is worth 14.0 €/MWh. On the operator's own exposure it is worth 10.5. |

## 1. Situation

A data-centre operator with six German sites saw its cost of power fall from 168 to 104 €/MWh between two years, a fall of 38%. The head of
sustainability says the renewables build-out did it and wants a long-term solar PPA. Procurement says cheaper gas did most of the work.
The PPA business case template asks for one figure, the build-out's part of the fall in the company's net cost of power, and the CFO signs
it with the PPA. At the start of the second year a cloud tenant moved into newly fitted halls at Mainzer Ufer, Ostkreuz and Neckarau.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the market price and generation series, the supplier invoices, the meter feeds, the lease
  and the re-billing ledger. Procurement's reading is confirmed: gas did most of the work, and the build-out's real part is quantified. No
  one's figures are overturned. The difficulty is whose load the build-out is measured on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice. The overlap still certifies that cost equals metered load at the hourly price, and the natural
  pipeline still prices the build-out on the gross meters.
* **Instrument repair.** Give every meter a perfect clock and a site tag. The halls' kWh are still inside the site meters, and the lease, not
  a better meter, decides whose they are.
* **Lens swap.** The naive figure prices the build-out on all metered consumption. The answer prices it on the 60% the operator bears, which
  has a different hourly shape. These are different populations.

## 3. The driving force

A strong solver fits the merit-order model, attributes the price change by Shapley across gas, carbon and residual load, and weights it by the
operator's own metered load rather than the market's. Along the way it recovers the clocks of nine meters that stamp UTC, as their
daylight-saving signature shows. The overlap then confirms the construction: in every week, metered load at the hourly price reproduces the
supplier's invoice to the cent. The result is 14.0 €/MWh. But the tenant's training runs follow the midday dip that solar now carves into
prices, and its halls' power is re-billed to it at hourly cost under the lease's power clause. Most of the build-out's midday saving was
the tenant's. The operator's own load is flat, and it gained 10.5 €/MWh. The halls' sub-meters link to the lease only through the
sub-meter register.

## 4. The ladder

| Rung | Construction | Lands on (renewables component, €/MWh) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Merit-order model with Shapley over gas, carbon and residual load, on the market's time-weighted average price | 9.0 (−14%) | The textbook attribution on the published annual average | The PPA template prices the company's cost of power, which follows its load, not the clock |
| 1 | The same attribution, load-weighted by the market's demand | 12.0 (+14%) | The procurement-relevant average | The operator's cost is its own metered load at the hourly price, and its profile is not the market's |
| 2 | Hygiene of the meter clocks: own metered profile, nine UTC meters recovered by their daylight-saving signature | 14.0 (+33%) | Reproduces the supplier's invoice in every overlap week to the cent | The lease's power clause: the three tenant halls are re-billed at hourly cost, and their sub-meters sit under the site meters |
| 3 | **Decisive:** tenant hall sub-meters (via the sub-meter register) netted out, the attribution run on the operator's own exposure | **10.5** | — | — |

* **Figure shape.** The corrections walk the component up from 9.0 to 14.0, and the decisive move reverses them to 10.5. Gas carries most of
  the fall in the operator's own cost. The gross 64 €/MWh headline overstates that fall, because the tenant's load sits in the cheapest
  hours.
* **Partial correction priced (L3).** Rung 2 sits 3.5 from the answer. A solver who removes each hall at its contracted capacity as a flat
  block takes out flat load and leaves the midday hump in, landing at 15.2. One who nets the re-billed euros but keeps the halls' kWh in the
  denominator lands at 6.3. One who looks for the split in the billing system finds every site on supply contract SC-14 and lands back on
  14.0.
* **Grid.** Price weighting (time, market load, own metered) × clocks (as delivered, recovered) × halls (gross, net) gives 8 feasible cells.
  The nearest wrong cells are 9.0 and 12.0 (14% each) and the net reading with UTC clocks unrecovered (12.1, 15%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The lease's power clause sits in a tenancy document. The PPA template says "net cost". No document joins the two or
   names the sub-meters.
2. **Corpus blind for a computable reason.** *In every overlap week the tenant halls stood empty, because the tenant's fit-out finished on 31
   December, the overlap's last day, so gross and own consumption were the same kWh.* The overlap certifies "metered load × hourly price" at
   8 of 8 weeks to the cent.
3. **No arithmetic symptom.** Invoices tie to meters, meters tie to site totals, and the re-billing ledger ties to the hall sub-meters.
   Every reconciliation passes under the gross reading.
4. **Not a row predicate.** Own exposure is each site meter's hourly series minus the sub-meters the register places under a re-billed hall.
   The attribution is then rerun on that profile.
5. **The enumeration is arithmetic.** No field marks load as the tenant's. The halls' share of each hour is computed.
6. **No cutover date.** The tenant's arrival is the year boundary itself, so there is no within-year step to align on.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Eight weeks at the end of the first year in which the old feed (site-tagged, local time) and the new feed (31 meters, mixed
  clocks, no site tags) ran together, with the supplier's invoices for those weeks.
* **What it certifies.** The clock recovery and the cost construction. Each of the nine UTC meters aligns with its old-feed counterpart only
  after the shift its daylight-saving signature implies. Metered load at the hourly price reproduces all eight weekly invoices exactly.
* **What it is blind to.** The tenant halls (property 2).
* **Twin pair.** Ostkreuz and Rheinhafen are identical on metered consumption (142 GWh), contracted capacity, region and invoiced total.
  Their net power cost fell €4.1M and €8.3M (2.02×). Half of Ostkreuz's metered load is a re-billed tenant hall, which only the sub-meter
  register reveals.
* **Resemblance points at the decoy.** Ostkreuz's gross midday hump matches the interactive profile at Spreebogen, an own-load site, so the
  hump reads as the operator's own.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The PPA template: "The case is priced on the company's net cost of power." The lease's power clause: "Power to the leased
  hall is re-billed to the tenant at the landlord's hourly cost." The procurement memo fixes the merit-order specification and the Shapley
  drivers.
* **Empirical pins.** Meter clocks come from the daylight-saving signature, corroborated by the overlap. Hall sub-meters come from the
  sub-meter register.
* **Voices.** Head of sustainability: "Renewables set the price now; that is why our bill fell." Procurement lead: "Gas fell by two-thirds;
  everything else is noise." Mainzer Ufer site manager: "Our midday load has never been higher."
* **Licensed wrong basis.** The procurement memo records that the group sustainability report states power cost on gross metered
  consumption, and that the board's sustainability committee will read the PPA case against it.

## 8. Determinism by construction

* **Clocks.** Local-clock meters show a 23-hour day in March and a 25-hour day in October, and UTC meters never do. The identification is
  exact, and the overlap agrees on all nine.
* **Sub-meters.** Each hall has one sub-meter under one site meter, and no sub-meter carries own load.
* **Shapley.** Three drivers, eight combinations, fixed by the memo. Swapping LMDI for Shapley moves the component by under 0.1.
* **Hall load.** The halls drew power from the first day of the year, so no partial-year convention arises.
* **Prices.** The supplier bills hourly day-ahead prices. The market's switch to quarter-hour products falls outside both years.

## 9. Prompt sketch and deliverables

> I sign the solar PPA business case on the 14th, and it needs one number from me: how many euros per megawatt-hour of the fall in our cost of
> power came from the renewables build-out, to one decimal. Our head of sustainability is convinced renewables did most of the work. Give me
> the figure in a sentence I can put in the case, with `cost_attribution.xlsx`, a chart `cost_bridge.png`, and a one-page `ppa_figure_note.pdf`.

* `cost_attribution.xlsx` — the attribution on every basis, the guarantees-of-origin sheet (ask A), the imbalance sheet (ask B) and the
  overlap back-test (ask C).
* `cost_bridge.png` — a bridge from 168 to 104 €/MWh with bars for gas, carbon, renewables and other, and an inset of the average daily
  profile of own and tenant load against the second year's hourly price. The renewables bar is labelled with its €/MWh, and the title states
  the figure.
* `ppa_figure_note.pdf` — the committed figure and the basis it rests on.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each site and quarter, the share of own consumption covered by cancelled guarantees of origin.
  *Device:* the registry export dates each cancellation by its transaction, while the certificate's consumption period sits in a separate
  field, as the registry guide states. Assigning by transaction date moves about a fifth of cover between quarters. The registry never
  enters the cost attribution.
* **Ask B (device-carried).** Monthly imbalance charges for the operator. *Device:* imbalance prices are published provisional and replaced by
  final values about eight weeks later. The price file keeps both, flagged, and using provisionals misstates four months by more than 10%.
  Imbalance never enters the day-ahead attribution.
* **Ask C (validity).** For each of the eight overlap weeks, the invoiced cost beside metered load at the hourly price under your recovered
  clocks.
* **Decoupling.** Clearing the hall netting changes no figure in asks A or B. Ask C runs on weeks when the halls were empty.

## 11. Rubric arithmetic

6 sites × 4 quarters (ask A) + 12 months (ask B) + 8 weeks (ask C) + the committed figure, the gas, carbon and other components and the tenant
share + 5 named chart parts + 3 files ≈ 65 criteria.

## 12. World-building constraints

* In the first year own consumption is 520 GWh and the halls are empty. In the second year gross is 860 GWh, of which 344 GWh (40%) is the
  tenant's.
* Cost per MWh is 168 in the first year and 104 in the second. The renewables component is 9.0 / 12.0 / 14.0 / 10.5 by rung, and the tenant
  profile's own component is 19.25.
* Nine of 31 new-feed meters stamp UTC. The overlap runs eight weeks to 31 December, with every hall empty.
* Ostkreuz and Rheinhafen are identical on every site-table column, and Ostkreuz's hall carries half its load.
* Partials sit at 15.2 and 6.3, and every non-answer cell sits at least 14% from 10.5.
* Registry periods and imbalance flags never touch the meters, the halls or the day-ahead prices.
