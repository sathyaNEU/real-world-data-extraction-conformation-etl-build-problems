# OS12 — How to split 2,400 retrofit batteries across four regions, when 12,500 homes that look closed to us are still buying through the leasing programme's successor

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · residential battery distribution |
| Mirrors | Allocating constrained device supply across markets when a closed channel's customers carry on through a successor (Apple and Google device allocations after a carrier partner exits and its subscribers move to an MVNO, Amazon inventory after a marketplace seller's book is transferred, equipment upgrades after a reseller's customer base is acquired) |
| Decision shape | An allocation under a cap: 2,400 batteries from the manufacturer split across four regions in pallets of 20 |
| Committed call | The units shipped to each region, and each region's expected retrofit sales next year |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · continuity across a closure (#23), recovered through a referral manifest joined to the solar register, with a rate validated on one population and applied to another (#13) below it |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #23 reads a closure notice as a market exit · #13 validates on one population, applies to another · #18 joins only on the visible key |
| Calibration form | Pilot log: every owner household contacted in last year's retrofit pilot in Harbour and Metro, with its feed-in tariff contract and outcome |
| Driving force | The leasing programme's closure reads as 12,500 Eastern Hills systems leaving the market: the lessor owns them, and the solar register flags them so. But the leases passed to a successor servicer, whose customers' battery referrals reach us as one bulk business account with an address manifest. Joined address by address to the solar register, the manifest shows those same households buying at 6.2% a year, and nothing in the regional sales or the register counts them as Eastern Hills demand. |

## 1. Situation

A solar installer has 2,400 batteries confirmed by its manufacturer for next year's retrofit campaigns and must tell the manufacturer how to
split them across its four regions: Valley, Metro, Harbour and Eastern Hills. The allocation rule ships each region units in proportion to
its expected retrofit sales, in pallets of 20. The solar register lists every rooftop system with its owner type; the storage register
links every battery to the system it serves; the tariff register gives each system's feed-in contract and end date. Last year's pilot
contacted every owner household in Harbour and part of Metro. In March the utility's SunLease programme closed, and its leases passed to
Brightpath Energy Services for servicing.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the registers, the pilot's outcomes, the closure notice and the business account's invoices and
  manifest. The register is right that the lessor still owns the SunLease systems. No stakeholder read is overturned. The difficulty is
  that a closed programme's customers carry on through a successor, and only the successor's records show it.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the closure notice. The register still marks 12,500 Eastern Hills systems as lessor-owned,
  and the natural pipeline still sizes owners only.
* **Instrument repair.** Make every register perfect; it already is. The systems remain lessor-owned, and only the referral manifest
  connects their households to battery orders.
* **Lens swap.** The naive read is owner households. The answer adds a population the owner view excludes, lessee households buying
  through a successor.

## 3. The driving force

A strong solver drops the deck's new-install attach rate for the pilot's retrofit conversion and removes systems that already have a
battery. It sees the pilot ran where most feed-in tariffs had expired, joins the tariff register, and converts at 7.0% for expired
contracts and 1.5% for live ones. It excludes the SunLease systems: the register says the lessor owns them, and the closure notice says
the programme ended. Harbour wins. But the leases did not end; their servicing passed to Brightpath, and Brightpath refers its customers'
battery requests to us. Those orders arrive as one business account with an address manifest, 580 in nine months. Joined to the solar
register, every address is a SunLease system in Eastern Hills: 12,500 households buying at 6.2% a year, which lifts Eastern Hills from third
to first.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Owner systems × the 35% attach rate on new installs | Valley leads (840 units); 34,055 sales (+833%) | The strategy deck's market sizing on the register | The pilot log: retrofit conversion is 5.9%, and the storage register shows 50% of Valley's owner systems already have a battery |
| 1 | Owner systems without a battery × the pilot's 5.9% | Metro leads (760, 1.20× over Harbour); 4,151 (+13.7%) | The pilot's own rate on the right base | The tariff register: the pilot's households were 80% past their feed-in contract; conversion is 7.0% past it and 1.5% before |
| 2 | Owner systems without a battery × conversion by tariff status | Harbour leads (900, 1.33× over Metro); 2,875 (−21.2%) | Calibrated to the subgroup that drives conversion, every pilot group reproduced | The business account's manifest: its 580 referrals in nine months are all SunLease households in Eastern Hills |
| 3 | **Decisive:** rung 2 plus the SunLease households continuing under Brightpath, at the 6.2% the manifest shows | **Valley 260 · Metro 540 · Harbour 720 · Eastern Hills 880; 3,650 sales** | — | — |

* **Shape.** The graded objects are the unit vector and each region's expected sales. The leading region changes at every rung (Valley,
  Metro, Harbour, Eastern Hills), and the total walks down then reverses: +833%, +13.7%, −21.2%, answer.
* **Partial correction priced (L3).** A solver who finds the continuing households but keeps the pooled 5.9% names Eastern Hills with 740
  units and 4,926 sales (+35%). One who finds them but forgets systems that already have a battery names Eastern Hills with 820 units and
  overstates its sales by 14%. One who reads the manifest as Brightpath's own business and leaves it out stays at rung 2.
* **Grid.** Base (all owners, owners without a battery) × conversion (pooled, by tariff status) × lessee households (out, continuing)
  gives 8 cells, each leader at least 1.15× clear. The cell whose total lands nearest (+1.5%) needs two refuted readings at once, names
  Harbour, and ships 380 units to the wrong regions.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The closure notice says leases pass to Brightpath for servicing. Brightpath's letter says it may refer
   customers' battery requests to approved installers. Neither says those households are our retrofit demand or in which region.
2. **Corpus blind for a computable reason.** *No pilot household was a SunLease lessee, because SunLease operated only in Eastern Hills
   and the pilot ran in Harbour and Metro.* The pilot reproduces every group from owner households alone.
3. **No arithmetic symptom.** Regional retrofit sales tie to homeowner invoices, and Brightpath's orders sit under one business account
   with no region, so no regional back-test shows an excess.
4. **Not a row predicate.** The population needs the manifest's addresses joined to the solar register, the matched systems grouped by
   region, and a rate taken from referrals over the months since the transfer.
5. **The enumeration is arithmetic.** No column marks a lessee household as reachable; the register's owner type says the opposite.
6. **No cutover date.** The closure is the decoy. No regional sales series steps on it, and the decisive population is found by a join,
   not by aligning a series.
7. **Survives deletion.** Removing the voices leaves the register's owner flag excluding the households on its own.

## 6. The calibration corpus

* **Form.** The pilot log: 9,600 owner households contacted in Harbour and Metro, each with system age, tariff contract and outcome.
* **What it certifies.** Retrofit conversion of 7.0% past the feed-in contract and 1.5% before it, reproducing all 14 neighbourhood
  groups within 0.3 points. The pooled 5.9% reproduces the 8 groups whose expired share sits near the pilot's 80% and misses the other 6.
* **What it is blind to.** Lessee households (above).
* **Twin pair.** Pilot neighbourhoods Larkfield and Oxbow are identical on household count, system size, install years (2010–2012) and
  region. All of Larkfield's systems connected under the 15-year tariff scheme and have expired; 65% of Oxbow's connected under the 20-year
  scheme and have not. Larkfield converted at 7.0% and Oxbow at 3.4%, 2.0× apart, separated only by the tariff register's contract dates.
* **Resemblance points at the decoy.** The pilot's expired-contract households most resemble Harbour's, the rung-2 leader.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The allocation rule: units go to regions in proportion to expected retrofit sales next year, in pallets of 20 by largest
  remainder. The sales definition: a retrofit sale is the first battery added to an existing solar system. The closure notice: SunLease
  closes on 31 March and its leases pass to Brightpath Energy Services for servicing. Brightpath's letter: it may refer customers' home
  battery requests to approved installers.
* **Empirical pins.** Conversion by tariff status, from the pilot. The lessee rate, from the manifest.
* **Voices.** The sales director: "Valley has the most solar roofs in the state, so it gets the most batteries." The Eastern Hills
  manager: "Since SunLease closed, half my territory is off-limits to us."
* **Licensed wrong basis.** The allocation rule records that the manufacturer's channel team splits supply by installed solar base and
  will propose that split.

## 8. Determinism by construction

* **Lessee rate.** Referrals have run at 64 or 65 a month in each of the nine months since the transfer, so any annualising window gives
  775 and 6.2% of 12,500.
* **Manifest join.** Every manifest address matches exactly one register address after the register's own normalisation; none matches an
  owner system.
* **Battery links.** Every battery in the storage register names its solar system, so the without-battery base needs no matching rule.
* **Tariff status.** Status is taken at 1 January next year; no contract ends within 60 days of that date.
* **Pallets.** No region's quota sits within 0.05 pallets of a remainder tie at any rung.

## 9. Prompt sketch and deliverables

> The manufacturer has confirmed 2,400 batteries for next year's retrofit campaigns, and by Friday I have to tell them how to split them
> across our four regions. Our sales director wants the most where the most solar roofs are. Give me the units per region and the retrofit
> sales each region should expect, as the table I send them, with `battery_split.xlsx`, a chart `region_demand.png`, and a one-page
> `allocation_letter.pdf`.

* `battery_split.xlsx` — expected sales and units by region on four bases, the lessee-household build, the warranty sheet (ask A) and the
  lead-time sheet (ask B).
* `region_demand.png` — a script-rendered stacked bar chart: each region's expected sales split into expired-contract owners, live-contract
  owners and continuing lessees, the unit allocation as a marker on each bar, and the pallet rule noted in the subtitle.
* `allocation_letter.pdf` — the committed split and the expected sales behind it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the three battery models, last year's warranty claims per 100 installed units and the
  median days to resolution. *Device:* a claim escalated to the manufacturer closes and reopens under a return number carrying the
  original in `parent_claim`, as the warranty guide documents. Counting both double-counts claims for the model with most escalations.
* **Ask B (device-carried).** For each region, last year's median days from order to commissioning and the share over 60 days. *Device:*
  orders waiting on network approval carry hold-start and hold-end events, and the service standard measures lead time excluding holds.
  Ignoring them pushes two regions over 60 days.
* **Ask C (validity).** Each region's expected sales and units under each of the four rung bases, and pilot groups reproduced (of 14) by
  the pooled and the tariff-status rates.
* **Decoupling.** Dropping the continuing lessees changes no figure in asks A or B. Warranty claims and order holds touch neither the
  registers nor the manifest.

## 11. Rubric arithmetic

3 models × 2 (ask A) + 4 regions × 2 (ask B) + 4 regions × 4 bases × 2 figures and 2 back-test counts (ask C) + the unit vector (4), the
lessee sales and the total + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Owner systems (with a battery, expired share among the rest): Valley 34,500 (50%, 15%), Metro 26,000 (15%, 40%), Harbour 20,000 (8%, 80%),
  Eastern Hills 16,800 (25%, 55%). SunLease lessees: 12,500, all in Eastern Hills.
* Expected sales by rung (Valley, Metro, Harbour, Eastern Hills): rung 1 1,018 / 1,304 / 1,086 / 743; rung 2 401 / 818 / 1,086 / 570;
  answer 401 / 818 / 1,086 / 1,345.
* Units by rung: rung 0 840 / 640 / 500 / 420; rung 1 580 / 760 / 620 / 440; rung 2 340 / 680 / 900 / 480; answer 260 / 540 / 720 / 880.
* No pilot household is a lessee; Larkfield and Oxbow match on every column outside their tariff contracts.
* Warranty claims and order holds never touch registers, the pilot or the manifest.
