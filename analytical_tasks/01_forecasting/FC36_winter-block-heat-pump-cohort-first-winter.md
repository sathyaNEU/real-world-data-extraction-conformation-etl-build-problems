# FC36 — How big a winter supply block the city utility buys above its rolled-over contract, when twelve thousand heat pumps installed since last winter have no winter in the billing history

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · municipal utility power supply |
| Mirrors | Committing capacity ahead of a cohort whose load has not shown up yet (cloud capacity for workloads migrated in the off-season, energy contracts for newly electrified fleets or stores, utilities buying winter energy after heat-pump incentive waves) |
| Decision shape | One figure committed at a date: the incremental winter block bought by 15 October above the contract that rolls over at last winter's volume |
| Committed call | The incremental residential winter block for October to April, in GWh to the nearest whole number |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · maturity (the cohort's first winter crystallises after the extract, and only a registry holds it), with a latent attribution marker (measured #17) at rung 2 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #17 guesses an attribution the data can settle · #13 validates on one population, applies to another · #4 never tests its reading against the control |
| Calibration form | Revision log: the rebate programme's measurement-and-verification log, each cohort's per-install winter load as installer-reported, inspection-revised and confirmed against the following winter's bills |
| Driving force | A home converted from gas to a heat pump adds its heating load only from its first winter. The 2026 rebate tranche paid for 12,000 conversions between April and August, after the last winter closed, so not one of them has a heating month in the bills; every closed winter is fully developed and every model fitted to them ties. Their first-winter load is in the rebate registry, inspection-revised at 6.0 MWh a home, and the revision log shows inspection-revised values confirmed by the following winter's bills since 2023. The billing data carries no conversion flag; converted homes show only as a bill credit of exactly the rebate amount. |

## 1. Situation

A municipal electric utility in a cold northern city buys its winter energy under a supply contract that rolls over each October at
last winter's delivered residential volume, 405 GWh for October to April. Anything above that must be bought as a separate block by 15
October. The city's heat-pump rebate, $1,500 a home since 2019, rose to $6,000 for a tranche that closed on 31 August, and 12,000 homes
converted from gas between April and August. The pack holds residential billing history by premise, daily weather, the rebate registry
of every installation with its revised winter load, the programme's verification log, and the forecasting team's model and back-tests.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the bills, the weather, the registry and the verification log. The forecasting team's model really
  has back-tested within 1% for five winters. No reported number is overturned; the difficulty is load that belongs to the coming winter
  and that no closed winter contains.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the forecasting team's confidence and every voice. A weather-and-trend model on the bills still ties every
  closed winter, and still sees nothing of the 2026 cohort.
* **Instrument repair.** Imagine interval meters on every home with perfect reads. The 2026 cohort's heating load still has not happened;
  no instrument of the past can observe a winter that has not come.
* **Lens swap.** The naive read and the answer are different moments for the same homes: the 12,000 converted homes as they were last
  winter, heated by gas, against the same homes this winter, heated electrically.

## 3. The driving force

A strong solver weather-normalises last winter, selects the model whose twelve-month totals back-test best, and forecasts the coming
winter. Seeing that the total's growth has come from conversions rather than from homes in general, it separates converted homes from the
rest, projects each group, and finds the organic load slightly falling. Every step is correct, and every closed winter reproduces. The
conversions it separates are the ones whose winters are already in the bills. A converted home's heating load first appears in its first
winter, so a cohort installed between April and August is invisible in every bill it has produced: those bills cover a gas-heated home in
its last winter and a heat-pump home in a summer. The registry holds every 2026 installation with its inspection-revised winter load, and
the verification log shows that since inspection revisions began in 2023 those values have matched the next winter's billed increase to
within 1%. The coming winter adds 72 GWh that no model fitted to bills can produce.

## 4. The ladder

| Rung | Construction | Lands on (block) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The forecasting tool's one-month winner: seasonal naive with drift (+4.5%) on last winter's actual | 18 GWh (−64%) | The tool's own model choice, and it tracks the series month to month | The tool ranks models on one-month error; the block is a seven-month total, and on seven-month totals the weather-and-trend regression wins every back-test |
| 1 | Weather-and-trend regression selected on seven-month totals, at normal weather | 12 GWh (−76%) | Horizon-matched selection and weather normalisation: back-tests within 1% on all five closed winters | The bills carry a $1,500 credit on converted homes, and with them identified the total's trend (+7.5% a year) is conversions; homes that never converted fall 1.5% a year |
| 2 | Converted and never-converted homes separated by the rebate credit, each projected on its own history | −22 GWh (no block) | Attributes the growth to its source; the organic decline is real and the converted homes' load is carried | The rebate registry: 12,000 homes converted after the last winter closed, every one with a revised winter load and none with a heating month in its bills |
| 3 | **Decisive:** plus the 2026 cohort's first winter from the registry's inspection-revised loads (12,000 × 6.0 MWh) | **50 GWh** | — | — |

* **Figure shape.** The corrections walk the block down (18, 12, −22) and the decisive rung reverses past rung 0, so a solver who stops
  anywhere short under-buys and covers the gap at the winter spot price.
* **Partial correction priced (L3).** A solver who finds the registry but uses installer-reported loads (7.3 MWh a home, the figures the
  verification log revised down by 18% before 2023) buys 66 GWh (+32%). One who adds only the 2,000 conversions whose $6,000 credits have
  already posted, the ones the marker can see, buys −10 GWh: still no block.
* **Grid.** Selection (one-month, seven-month) × attribution (total trend, converted and organic separated) × cohort (none, credited only,
  registry) × load source (installer, revised) = 16 feasible cells, landing between −22 and +118 GWh. Every wrong cell sits at least 16
  GWh (32%) from 50; the nearest is the registry cohort at installer-reported loads (66).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rebate rules and the registry describe installations and payments. No document links the registry to supply
   planning or says a conversion's load starts with its first winter.
2. **Corpus blind to the cohort.** *In every closed winter the homes converted since the winter before numbered at most 4,500, because the
   rebate was $1,500 until the 2026 tranche quadrupled it; each such cohort sat inside the trend the model back-tests on.* Every closed winter
   is fully developed, and none holds a cohort of 12,000.
3. **No arithmetic symptom.** Bills reconcile to metered energy, weather normalisation reproduces each closed winter, and the registry's
   installation count matches rebate payments.
4. **Not a row predicate.** The forward load is a sum over a registry the billing pipeline never joins, by installation date against the
   last closed winter, at each installation's revised load.
5. **The enumeration is arithmetic.** No billing column marks a 2026 conversion; 10,000 of the 12,000 have no credit posted yet.
6. **No cutover date in any outcome series.** The tranche's deadline is dated, but nothing it caused has reached a bill: the cohort's
   heating load starts with the coming winter.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The verification log for cohorts 2019–2025: per-install winter load as reported by the installer, as revised at inspection
  (from 2023), and as confirmed by the following winter's billed increase.
* **What it certifies.** That inspection-revised loads match the next winter's billed increase within 1% for the 2023, 2024 and 2025
  cohorts, so the registry's revised 2026 values are the ones to use; and that before 2023 installer-reported loads ran 18–22% high.
* **The settled attribution case (E19).** The 2025 cohort's billed first-winter increase (27.0 GWh) reproduces only when converted homes
  are identified by the rebate credit; the all-electric baseline code, which many converted households never request, finds 61% of them.
* **Twin pair.** Premises 40817 and 40944 are identical on every billing column through September 2026: last winter's load, the summer's
  load, rate, baseline code and account age. Their forecast winter loads differ 2.1×, because 40817 converted in May under the 2026 tranche
  and 40944 did not. Only the registry separates them.
* **Resemblance points at the decoy.** By weather and customer count, the coming winter most resembles the 2023–24 winter, which the
  regression reproduced to 0.4%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The supply contract: it rolls over each October at last winter's delivered residential volume (405 GWh), and any
  increase is bought as a separate block by 15 October. The block is set at the forecast residential winter load at normal weather, less
  the rolled-over volume. Normal weather is the thirty-year normal the utility files with its rates.
* **Empirical pins.** The 2026 cohort's load, from the registry's inspection-revised values validated by the verification log. Converted
  homes, from the rebate credit in the bills. The organic trend, from never-converted homes.
* **Voices.** The forecasting lead: "Our model has the winter nailed; it has never been more than 1% out." The energy-services manager:
  "Conversions just tip the trend along, as they always have." The finance director: "If the model says twelve, buy twelve."
* **Licensed wrong basis.** The supply contract records that the wholesale supplier sizes its offer on the utility's filed load forecast,
  produced by the forecasting team's regression, and will quote against it.

## 8. Determinism by construction

* **Install timing.** Every 2026 installation is dated April to August, after the last winter's final heating month, so no part of any
  cohort member's heating load is in the bills under any reading of the season.
* **Season share.** Each revised load is a winter (October to April) figure, so no allocation of annual load across months is needed.
* **Organic trend.** Never-converted homes' normalised winter use falls 1.4–1.6% a year in each of the last five winters, so window choice
  does not move it.
* **Weather.** The thirty-year normal is filed; a twenty-year normal moves the block by under 1 GWh.
* **Maturity.** The registry is complete for the tranche, which closed on 31 August; credits post 60–120 days after inspection, which is
  why most are not yet in the bills.
* **Rounding.** The block lands at 50.0 GWh, half a unit from either rounding boundary.

## 9. Prompt sketch and deliverables

> Our winter supply contract rolls over at last winter's 405 GWh on 1 October, and anything above that has to be bought as a separate block
> by the 15th. The forecasting team is confident its model has the winter nailed. Tell me how big a block to buy, in GWh to the nearest whole
> number, in a line I can take to the supply committee, and send `winter_block.xlsx` with the build and the sheets below, a chart
> `winter_load_build.png`, and a one-page `block_memo.pdf`.

* `winter_block.xlsx` — the winter load build by component, the estimated-reads sheet (ask A) and the budget-billing sheet (ask B).
* `winter_load_build.png` — stacked bars for the last five winters and the coming one: never-converted homes, earlier-converted homes and
  the 2026 cohort, with the 405 GWh rolled-over line, the regression's forecast as a marker, and the block annotated as the gap.
* `block_memo.pdf` — the committed block and why the back-tested model cannot see it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six rate classes and each quarter of the last fiscal year, the share of bills
  issued on estimated reads. *Device:* interval meters with communication gaps post estimated intervals that the meter-data system later
  replaces from the meter's memory, under a validation code the meter-data guide documents; counting the first posting as an estimated bill
  overstates estimation in every class. Replaced intervals change no billed energy.
* **Ask B (device-carried).** For each rate class and quarter, energy billed to customers on budget billing. *Device:* budget-billing
  accounts are charged a levelised amount while their billed energy is actual consumption, as the billing guide documents; deriving energy
  from the amount charged misstates it in every quarter.
* **Ask C (validity).** The block under each of the four rung constructions, and each construction's back-test error on the five closed
  winters.
* **Decoupling.** Clearing the 2026 cohort changes no figure in asks A or B.

## 11. Rubric arithmetic

6 rate classes × 4 quarters (ask A) + 6 × 4 (ask B) + 4 constructions × 2 (ask C) + the committed block, the 2026 cohort's winter load and
the organic trend + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Last winter: 405 GWh actual (4% colder than normal), 388 GWh normalised: never-converted homes 330, earlier-converted homes 58. The
  coming winter at normal weather: 325 + 58 + 72 = 455 GWh, a block of 50.
* Cohorts: at most 4,500 a year before 2026; 12,000 in 2026, installed April to August; 2,000 credits posted by the extract.
* Block by rung: 18 / 12 / −22 / 50; installer-reported loads 66; credited conversions only −10. Every wrong cell at least 16 GWh away.
* Verification log: inspection-revised loads within 1% of the following winter's billed increase for 2023–2025; installer loads 18–22%
  high before that.
* The twin premises are identical on every billing column through September 2026.
* Estimated-interval replacements and budget-billing amounts touch no billed energy used in the build.
