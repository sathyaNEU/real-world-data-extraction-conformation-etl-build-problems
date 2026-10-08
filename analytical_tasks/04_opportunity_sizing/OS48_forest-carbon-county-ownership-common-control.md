# OS48 — Which county gets the first forest-carbon aggregation project, when eligibility belongs to an ownership no file stores

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · carbon markets and land use |
| Mirrors | Eligibility and sizing on a unit defined by common control rather than by the record that holds the data (marketplace seller programmes whose thresholds apply across a merchant's linked storefronts, cloud discount tiers that aggregate an enterprise's linked accounts, advertising spend tiers summed across an advertiser's related accounts) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the developer's first aggregation project, and its forester team for two years, goes to one of six counties |
| Committed call | The county for the first project, and the credits it should generate a year, in tonnes of CO2e to the nearest 1,000 |
| Gap · Pattern | Gap 2 (population) · E02 (the unit the standard makes eligible is the ownership under common control, which no file stores: a family's forest sits in many parcels held by its members, their LLCs and their trusts), with E15 below it (acres already under conservation easements, the quiet contamination behind the loud gross-versus-additional trap, with the easement registry as its control) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #2 counts file rows instead of the real unit · #11 beats the headline trap, misses the quiet one · #15 follows the requester's hunch over the rule |
| Calibration form | Gold-standard verification subsample: 600 family-forest parcels drawn at random and verified by consulting foresters, with forest condition, measured acres, easement status and the ownership under common control from deeds and registries |
| Driving force | The crediting standard admits a landowner whose forest under common ownership or control totals 40 acres or more, and then every parcel of that ownership counts. Sassafras families hold their land in many small parcels under members, LLCs and family trusts: 25% of its family-forest acres sit in parcels of 40 acres or more, but 80% sit in ownerships of 40 or more once title holders are linked through the business-entity and trust registries. Tamarack's land sits in large single parcels, so its eligible share barely moves. The parcel file holds title holders, and the ownership is two registries away. |

## 1. Situation

A carbon developer will launch its first improved-forest-management aggregation project, which pays family forest owners to defer harvest,
in one of six counties. The investor underwriting it wants the county and the credits a year it should generate. The crediting standard
credits sequestration above business as usual, deducts 20% for leakage and 15% for the buffer pool, and admits landowners with at least
40 acres of forest under common ownership or control. The developer's last project enrolled 15% of eligible acres in its first two years.
The investor's view is that Laurel, with the fastest-growing forests in the state, is the obvious place.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the forest inventory plots and their remeasurements, the parcel file, the easement registry, the
  entity and trust registries and the verification subsample. Laurel's forests do grow fastest. Nothing reported is overturned. The
  difficulty is that the standard's eligible unit is an ownership, and the files hold parcels and title holders.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the investor's view and every voice. Additional sequestration on easement-free parcels of 40 acres or more,
  the standard's test read at parcel grain, still names Tamarack.
* **Instrument repair.** No file is suspect. The parcel file's owner column records each parcel's title holder exactly, which is a
  different attribute from who controls the land, and no file claims to record control. The easement, entity and trust registries are
  complete and current, and the inventory carries its expansion factors. With nothing to repair, rungs 0, 1 and 2 name Laurel, Chestnut
  Hill and Tamarack. An ownership under common control is a unit no row claims to record, built by linking title holders through two
  registries, so the construction is still needed for Sassafras.
* **Lens swap.** The answer counts acres in ownerships of 40 or more, a different population from parcels of 40 or more, and Sassafras's
  two differ by a factor of 3.2.

## 3. The driving force

A strong solver refuses the prospectus's gross carbon gain and credits only sequestration above business as usual, the harvest removals a
project avoids, from the inventory's remeasured plots. It removes acres already under conservation easements, whose business as usual is no
harvest and which the registry lists by county. It then applies the standard's 40-acre test to the parcel file, because each row there is a
property with an owner. That names Tamarack. But the standard's test is per landowner under common ownership or control, and once an
ownership qualifies, every parcel in it counts. In Sassafras, land has passed down through families and is held in parcels of 5 to 30 acres
by siblings, their LLCs and family trusts. The parcel file names each title holder, the business-entity registry names each LLC's members,
and the trust registry names each trust's trustees and beneficiaries. Linked, 80% of Sassafras's family-forest acres sit in ownerships of 40
acres or more, against 25% in parcels of that size. In Tamarack the same link moves the share from 80% to 84%.

## 4. The ladder

| Rung | Construction (credits a year: acres × tonnes per acre × 15% uptake × 0.68 after leakage and buffer) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The prospectus: gross carbon gain per acre on family-forest acres in parcels of 40 acres or more | A, Laurel, 146,880 (1.51× Chestnut Hill) | The inventory's own growth figures and the standard's size test | The standard credits only sequestration above business as usual, the removals a project avoids |
| 1 | Additional sequestration (avoided removals from the remeasured plots) on the same acres | B, Chestnut Hill, 85,680 (1.94× Tamarack) | The headline trap beaten with the standard's own baseline | The easement registry: 45% of Chestnut Hill's family-forest acres are already under conservation easements, whose business as usual is no harvest |
| 2 | Easement acres removed (E15), matching the registry's county totals | C, Tamarack, 42,962 (1.40× Chestnut Hill) | Both traps beaten, each against its own control | The verification subsample: ownership under common control, linked through the entity and trust registries, reproduces all 600 verified ownerships |
| 3 | **Decisive:** eligible acres = every parcel of an ownership under common control with 40 acres or more | **E, Sassafras, 71,986 (1.59× Tamarack)** (5th of 6 on rung 0) | — | — |

* **The answer.** Sassafras, generating 71,986 tonnes of CO2e a year, committed as 72,000.
* **Position table.** Sassafras ranks 5th on rungs 0, 1 and 2, and leads only rung 3. It is never 2nd. Rung leaders beat their runners-up
  by 1.51×, 1.94×, 1.40× and 1.59×.
* **Discriminator dominance.** Tamarack carries a 2.02× lead into rung 3 (42,962 against 21,227). The ownership unit multiplies Sassafras's
  credits by 3.39 and Tamarack's by 1.05, an edge of 3.23×, which is 1.33 times the required 1.2 × 2.02 = 2.43.
* **Partial correction priced (L3).** Every half-built ownership names Tamarack. Grouping parcels by identical title holder, without the
  registries, gives Tamarack 43,513 against Sassafras's 33,916 (1.28×). Linking through the registries but only within a township gives
  Tamarack 43,623 against 36,454 (1.20×).
* **Grid.** Basis (gross, additional) × easements (kept, removed) × unit (parcel, ownership) = 8 cells. Every non-answer cell names Laurel,
  Chestnut Hill or Tamarack. The nearest is the ownership unit with easement acres kept, Chestnut Hill at 91,800 against Sassafras's
  73,832 (1.24×), reached by crediting land whose business as usual is already no harvest.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "landowner" and "common ownership or control" in a definitions section. No document says how to
   find an ownership, and the parcel file's owner column looks like the answer to that question.
2. **The corpus pins the unit by reproduction (Pattern B).** Common control through the entity and trust registries reproduces 600 of 600
   verified ownerships. Grouping by identical title holder reproduces 348 (58%) and township-bound linking 396 (66%), and every miss splits
   an ownership, so both rivals also miss the published county counts of ownerships of 40 acres or more. The link is two joins deep,
   title holder to LLC member or trustee to person, not a column a solver can sweep.
3. **No arithmetic symptom.** Parcel acres sum to the county totals and to the inventory's expanded family-forest area under every unit,
   because an ownership only partitions parcels.
4. **Not a row predicate.** The 40-acre test applies to a sum over an ownership's parcels, and the ownership exists only after the links.
5. **The enumeration is arithmetic.** No column holds an ownership or its acres. They are computed for 41,000 parcels in six counties.
6. **No cutover date.** Family land has been subdividing among heirs for decades, and no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** 600 family-forest parcels drawn at random across the six counties, verified by consulting foresters: forest condition and
  stocking, measured acres, easement status, and the ownership under common control from deeds and the entity and trust registries.
* **What it certifies.** The assessor's acres (within 2% on every parcel), the easement registry (600 of 600) and the inventory's
  avoided-removal rates by county. A solver who back-tests rungs 1 and 2 is confirmed.
* **What it pins.** The ownership unit (above), and with it the published National Woodland Owner Survey counts of family ownerships of 40
  acres or more, which common control matches within 3% in every county.
* **Twin pair.** In the verification subsample, the 18 parcels sampled in Polk Township (Sassafras) and the 18 in Union Township
  (Tamarack) are identical on every column of the parcel file a lookup reaches: parcel-size bands, family-forest acres and avoided-removal
  rates. The foresters verified 72% of Polk's sampled acres and 36% of Union's as lying in ownerships of 40 acres or more, 2.0× apart,
  because Polk's small parcels belong to a few family LLCs and trusts. Only the links through the entity and trust registries separate
  them.
* **Resemblance points at the decoy.** By parcel sizes, growth and harvest, Tamarack resembles the county of the developer's last project,
  so a solver transferring that project's enrolment by resemblance lands on Tamarack.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The standard credits sequestration above business as usual, excludes land already under a conservation easement,
  deducts 20% for leakage and 15% for the buffer, and admits landowners with 40 acres or more of forest under common ownership or control.
  Uptake is 15% of eligible acres, from the developer's last project.
* **Empirical pins.** Avoided-removal rates by county, from the inventory's remeasured plots with expansion factors; the ownership links,
  from the verification subsample's rule.
* **Voices.** The investor: "Laurel has the fastest-growing forests in the state; that is where the carbon is." The developer's field lead:
  "Big parcels mean fewer signatures."
* **Licensed wrong basis.** The underwriting memo records that the investor's credit committee screens counties on parcels of 40 acres or
  more and will see that basis.

## 8. Determinism by construction

* **Links.** Every LLC member and trustee in the registries resolves to one person ID, so the links are exact, with no probable matches.
* **The 40-acre test.** No ownership in the six counties has between 38 and 42 acres, so measured and assessed acres agree on every test.
* **Easements.** The registry's acres match the subsample on every sampled parcel, and no easement covers part of a parcel.
* **Rates.** Avoided-removal rates use the inventory's latest full remeasurement cycle and its expansion factors, as the standard requires.
* **Rounding.** 71,986 tonnes sits 486 from the nearest 1,000-tonne rounding boundary.

## 9. Prompt sketch and deliverables

> Our investor wants to know where the first aggregation project goes and what it will generate, and she thinks Laurel, with the
> fastest-growing forests in the state, is the obvious choice. Tell me which county gets the project and how many credits a year it should
> generate, to the nearest thousand tonnes, in a sentence for the investment memo. Send `county_credits.xlsx`, a chart
> `eligible_acres.png`, and a one-page `investment_memo_note.pdf`.

* `county_credits.xlsx`: the six counties under the four rung bases, the ownership build, the stumpage sheet (ask A) and the fire-season
  sheet (ask B).
* `eligible_acres.png`: for each county, family-forest acres split into easement land, parcels of 40 acres or more, and smaller parcels that
  ownerships of 40 acres or more bring in, as stacked horizontal bars, with credits a year printed on each bar and the chosen county
  highlighted.
* `investment_memo_note.pdf`: the committed county, its credits a year and why Tamarack is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each county, last year's median stumpage price per thousand board feet of sawtimber and the
  number of timber sales. *Device:* a sale re-advertised after no bids keeps its sale number with a new bid-opening row, and a sale's price
  is its awarded bid, per the state timber sale guide. Counting rows overstates sales by 20% in the two counties with many re-advertised
  sales.
* **Ask B (device-carried).** For each county, the average number of days a year under high fire danger over the last five years. *Device:*
  each weather station reports one danger rating per day, and a county's day counts as high when its station-weighted rating crosses the
  threshold, per the fire agency's guide. Counting station-days overstates days in counties with several stations.
* **Ask C (validity).** Each county's credits under the four rung bases, and the subsample reproduction under title-holder grouping,
  township-bound linking and common control (348, 396 and 600 of 600).
* **Decoupling.** Clearing the ownership construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 counties × 2 (ask A) + 6 (ask B) + 6 × 4 bases + 3 reproduction counts (ask C) + the committed county, its credits and its margin + 5
named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Counties (family-forest acres / share in parcels of 40+ / share in ownerships of 40+ / easement share / gross gain / avoided removals,
  tCO2e an acre a year): Laurel 450,000 / 0.80 / 0.86 / 0.06 / 4.0 / 0.8; Hemlock 250,000 / 0.75 / 0.81 / 0.04 / 2.8 / 1.6; Tamarack
  225,000 / 0.80 / 0.84 / 0.02 / 3.2 / 2.4; Walnut Creek 150,000 / 0.60 / 0.70 / 0.05 / 3.3 / 1.6; Sassafras 377,000 / 0.25 / 0.80 / 0.02
  / 3.2 / 2.4; Chestnut Hill 400,000 / 0.70 / 0.75 / 0.45 / 3.4 / 3.0.
* Uptake 15%; leakage 20%; buffer 15%. Title-holder grouping recovers a quarter of the ownership uplift and township-bound linking 30%.
* Rung leaders Laurel, Chestnut Hill, Tamarack and Sassafras with margins of 1.51×, 1.94×, 1.40× and 1.59×; both half-built ownerships name
  Tamarack; all eight grid cells name as stated.
* The 18 sampled parcels in Polk and in Union townships are identical on every parcel-file column, at 72% and 36% of acres verified in
  ownerships of 40 acres or more.
* Re-advertised sales and station-days never touch parcels, ownership links or easements.
