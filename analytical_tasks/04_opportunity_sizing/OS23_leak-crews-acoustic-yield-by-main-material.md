# OS23 — How to place 100 leak-detection crew-weeks across five utilities, when the listening survey hears leaks in metal mains and almost none in plastic

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · water infrastructure programmes |
| Mirrors | Allocating inspection capacity across sites by a detection yield measured on one asset mix, when detection splits absolutely on a property of the asset (acoustic leak detection on metallic and plastic pipe at water utilities, ultrasonic inspection of metal and composite parts at airlines, code scanners at Google and Meta that read only some languages, Amazon cycle counts that see only scannable stock) |
| Decision shape | An allocation under a cap: 100 contracted acoustic crew-weeks placed across five utilities in whole weeks |
| Committed call | The crew-weeks each utility receives, and the real losses recovered next year, to the nearest 50 million gallons |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E, a conditioned yield (the pilot's found share splits absolutely on main material, reached through the GIS), with two flawless grains, per connection and per mile, separated by the unit of work below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Pilot log: last year's 600-mile acoustic pilot, every surveyed main segment with the leaks found on it and their measured flows |
| Driving force | A listening survey hears leaks in metal mains and almost none in plastic: joined to the GIS, the pilot found 92% of the recoverable leakage on metallic mains and 5% on plastic. The pooled 60% is right for the pilot, whose mains were 63% metallic, and applies to no network on the list. The networks that lose most per mile are the plastic ones, so the pooled rate sends crews to Exe and Brent; conditioned on each network's own main material, Exe recovers least per week and Avon most. Every pilot week surveyed the same mix, so no weekly check could see the split. |

## 1. Situation

A state revolving fund has contracted 100 acoustic leak-detection crew-weeks for next year and must place them across five member
utilities: Avon, Brent, Colne, Derwent and Exe. A crew-week surveys 25 miles of main, and no network is surveyed twice in a year. The
programme rules place weeks where they recover the most water. Each utility files a validated AWWA water audit, and each keeps a GIS of
its mains. Last year's pilot surveyed 600 miles in three other utilities' districts and logged every segment it covered and every leak it
found. The fund's draft ranked the five by non-revenue water. The fund's director wants the crews where the most water is lost per
mile.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the audits, the GIS, the pilot's found leaks and its pooled 60%. Exe really does lose the most
  water per mile. No stakeholder read is overturned. The difficulty is how much of that loss a listening crew can find, and that is fixed
  by what each network's mains are made of.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the draft. The audits and the pilot's pooled yield still send 36 weeks to Exe and 32
  to Brent, every number reconciling.
* **Instrument repair.** The only candidate is the audits' real losses, a water-balance residual. Replace them with each utility's
  district night-flow measurements: they match to the million gallons, so rung 0 still funds Derwent, Avon, Exe and Brent, rung 1 Colne,
  Exe and Brent, and rung 2 Exe, Brent, Derwent and Avon, and the material split is still needed. The GIS gives every segment's material
  and the pilot log every surveyed segment, so neither needs repair.
* **Lens swap.** The naive read is water lost per mile. The answer is water a crew can find per mile, a different quantity fixed by a
  property in a different file.

## 3. The driving force

A strong solver drops non-revenue water, because it carries meter and billing losses and an unavoidable floor, and works from recoverable
real losses. It ranks networks per mile rather than per connection, because a crew-week is 25 miles of main, and it applies the pilot's
yield: crews found 60% of the recoverable leakage on the miles they surveyed, a rate that fits every pilot week. Exe and Brent, with 1.8
and 1.6 million gallons recoverable per mile, take 68 weeks. But a listening survey hears leaks in metal pipe; in PVC and polyethylene the
sound dies within metres. Joined to the GIS, the pilot found 92% of the recoverable leakage on metallic mains and 5% on plastic, and its
mains were 63% metallic. Exe's are 10% metallic and recover 0.25 million gallons a mile surveyed; Avon's are 85% metallic and recover 0.63.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Weeks in order of non-revenue water as a share of production, each network filled to its cap, sized at real losses on the miles surveyed | Avon 20 · Brent 20 · Colne 0 · Derwent 24 · Exe 36; 4,550 MG (+332%) | The fund's draft, on the audits' headline figure | The audits: non-revenue water includes apparent losses and the unavoidable floor; only real losses above it are recoverable |
| 1 | Weeks in order of recoverable real losses per connection, the audits' standard indicator | 0 · 24 · 40 · 0 · 36; 3,080 MG (+193%) | The industry's own indicator, apparent losses and the floor removed | The programme rules: a crew-week surveys 25 miles of main, and Colne's sparse network ranks first per customer and last per mile |
| 2 | Weeks in order of recoverable losses per mile × the pilot's pooled 60% found | 8 · 32 · 0 · 24 · 36; 2,196 MG (+109%) | The unit of work and the pilot's own yield, which fits every pilot week | The pilot log joined to the GIS: 92% found on metallic mains, 5% on plastic |
| 3 | **Decisive:** weeks in order of recoverable losses per mile × each network's found share by main material (0.92 metallic, 0.05 plastic, at its own mix) | **Avon 20 · Brent 32 · Colne 24 · Derwent 24 · Exe 0; 1,050 MG** | — | — |

* **Shape.** The graded objects are the five-way split and the recovered volume. The funded set changes at every rung, Exe's 36 weeks at
  rungs 0 to 2 fall to none, and every rung's figure is more than double the answer.
* **Discriminator dominance.** Exe carries 2.25× Avon's recoverable loss per mile into rung 3 (1.80 against 0.80 million gallons). Its
  mains are 10% metallic and Avon's 85%, so a crew finds 0.137 of Exe's and 0.790 of Avon's, an edge of 5.76×, 2.13 times the 2.70× floor.
  Product: 5.76 / 2.25 = 2.56.
* **Partial correction priced (L3).** No half-applied construction reaches the split. A solver who conditions on material but ranks per
  connection ships 4 · 32 · 40 · 24 · 0 and recovers 922 MG (−12%). One who joins the pilot's leaks to the GIS's service-line layer
  instead of the mains ships rung 2's split. One who conditions real losses rather than recoverable ones, keeping the unavoidable floor,
  ships 20 · 16 · 40 · 24 · 0 and claims 1,784 MG.
* **Grid.** Grain (per connection, per mile) × yield (as audited, pooled, by material) gives 6 cells: rung 1's split at 3,080 and 1,848
  MG, the per-connection material split at 922 MG, rung 2's split at 3,660 and 2,196 MG, and the answer. Only the answer cell leaves Exe
  out and funds Avon, Brent, Colne and Derwent.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot report gives one found share, 60%. No document says acoustic detection depends on pipe material, or
   points from the pilot log to the GIS.
2. **Corpus blind for a computable reason.** *In every pilot week the surveyed mains were 63% metallic within two points, because the crews
   worked a few miles of each of the nine pilot districts every week, so the pooled 60% fits every week's found volume.* Only the
   segment-level join to the GIS shows two rates.
3. **No arithmetic symptom.** Found volumes reconcile to the pilot's totals, the audits balance, and every rung's weeks sum to 100.
4. **Not a row predicate.** Each surveyed segment needs its material from the GIS, the found volume split by material, and then each
   network's own mix applied to its recoverable losses.
5. **The enumeration is arithmetic.** No column marks a main as audible; 3,800 miles of the five networks' mains are classified.
6. **No cutover date.** Materials and mixes are standing properties of the networks, and no series steps.
7. **Survives deletion.** Removing the draft and the director's view leaves the pooled pilot rate certifying rung 2.

## 6. The calibration corpus

* **Form.** The pilot log: 600 miles in nine districts of three utilities, every surveyed segment's ID, every leak found with its location and
  measured flow, and the audited recoverable losses of the districts surveyed.
* **What it certifies.** A found share of 60% of recoverable leakage on the miles surveyed, in every one of the 24 pilot weeks within
  two points.
* **What it is blind to.** The split by material (above).
* **Twin pair.** Pilot districts P2 and P5 are identical on every pilot-log column: 40 miles surveyed, 1.2 million gallons recoverable a
  mile, connection density and pressure. P2's mains are 95% metallic and P5's 45%, so crews found 88% and 44% of the recoverable leakage,
  2.0× apart. Only the join to the GIS separates them.
* **Resemblance points at the decoy.** By losses per mile and pressure, Exe most resembles the pilot districts, where the pooled rate
  was measured.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rules: 100 crew-weeks next year; a crew-week surveys 25 miles of main in the network's district rotation;
  no network is surveyed twice in a year, so each takes at most its mains ÷ 25 weeks; weeks go to networks in order of real losses
  recovered per week, each up to that cap; leaks found are repaired within 30 days. The AWWA audit method: recoverable real losses are
  real losses above the unavoidable floor.
* **Empirical pins.** The found share by material, from the pilot log through the GIS. Each network's metallic share, from its GIS.
* **Voices.** The fund's director: "Exe and Brent lose more water per mile than anyone. That is where the crews go." Avon's operations
  manager: "Our town centre is cast iron from the 1920s. It leaks, but we fix what we hear."
* **Licensed wrong basis.** The programme rules record that the state drinking-water board compares allocations with each network's
  non-revenue water percentage and will present that comparison.

## 8. Determinism by construction

* **Districts.** Every district of a network carries the network's material mix within three points, and crews survey districts in
  rotation, so any number of weeks covers the network's mix.
* **Found shares.** 0.92 on metallic and 0.05 on plastic mains in every pilot district within 0.01.
* **Order.** Consecutive networks' recovery per mile differ by at least 1.16×, so the fill order holds under any rounding.
* **Caps.** Avon 20, Brent 32, Colne 40, Derwent 24 and Exe 36 weeks, whole weeks from whole 25-mile multiples.
* **Rounding.** The answer recovers 1,052 million gallons, which rounds to 1,050.

## 9. Prompt sketch and deliverables

> Our 100 leak-detection crew-weeks for next year have to be placed across the five member utilities before the board meets on
> 3 December, and I need the weeks for each and the real losses they will recover, to the nearest 50 million gallons. Our director's view
> is that the crews belong where the most water is lost per mile. Give me the split and the figure in two sentences for the board, with
> `crew_allocation.xlsx`, a chart `found_share_by_main.png`, and a one-page `board_note.pdf`.

* `crew_allocation.xlsx` — each network's weeks and recovered volume on the four bases, the material build, the repair sheet (ask A)
  and the meter sheet (ask B).
* `found_share_by_main.png` — a script-rendered two-panel chart: left, found share against metallic share for each pilot district with
  the metallic and plastic rates as reference lines and P2 and P5 labelled; right, each network's recoverable loss per mile and the share
  a crew can find, stacked, with its weeks printed and the 63% pilot mix marked.
* `board_note.pdf` — the split, the recovered volume, and why Exe receives no weeks.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each utility, last year's median days from a reported main break to its repair and the share
  over three days. *Device:* a break that reopens after repair is logged as a new work order carrying `reopens`, and the maintenance guide
  times a break from its first report to its final repair. Timing reopened orders from their own start understates repair days at two
  utilities.
* **Ask B (device-carried).** For each utility, the share of customer meters older than 15 years, for small and for large meters.
  *Device:* a meter swapped under warranty gets a new serial carrying `replaces_serial` and keeps the original install date, which the
  metering guide ages from. Ageing from the swap date understates old meters at three utilities.
* **Ask C (validity).** Each network's weeks and recovered volume under each of the four rung bases, and pilot weeks reproduced (of 24) by
  the pooled rate and pilot districts (of 9) by the material rates.
* **Decoupling.** Pooling the pilot's yield changes no figure in asks A or B. Work orders and meter records touch neither the audits,
  the GIS nor the pilot log.

## 11. Rubric arithmetic

5 utilities × 2 (ask A) + 5 utilities × 2 meter sizes (ask B) + 5 networks × 4 bases × 2 and 2 reproduction counts (ask C) + the five
allocations and the recovered volume + 5 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Networks (Avon, Brent, Colne, Derwent, Exe): mains 500 / 800 / 1,000 / 600 / 900 miles (caps 20 / 32 / 40 / 24 / 36 weeks);
  connections 40,000 / 32,000 / 8,000 / 24,000 / 30,000; non-revenue water 28% / 18% / 15% / 32% / 22%; real losses 700 / 1,600 / 1,100 /
  850 / 2,000 and recoverable 400 / 1,280 / 500 / 600 / 1,620 million gallons a year; metallic share 85% / 20% / 65% / 45% / 10%.
* Found share 0.92 metallic, 0.05 plastic; pilot mix 63% metallic, pooled 0.60. Recovery per mile surveyed 0.632 / 0.358 / 0.308 /
  0.442 / 0.247 million gallons.
* Splits: rung 0 20 / 20 / 0 / 24 / 36; rung 1 0 / 24 / 40 / 0 / 36; rung 2 8 / 32 / 0 / 24 / 36; answer 20 / 32 / 24 / 24 / 0.
* P2 and P5 match on every pilot-log column.
* Work orders and meter records never touch audits, the GIS or the pilot log.
