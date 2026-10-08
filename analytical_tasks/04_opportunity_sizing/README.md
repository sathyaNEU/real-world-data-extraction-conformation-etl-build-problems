# Opportunity Sizing — 50 tasks (OS01–OS50)

Each file is a stump design note: the driving force, a ladder of defensible wrong answers on correct data, why the decisive move survives a strong solver, the calibration corpus, pins and voices, determinism, the prompt and the ask layer. `analytical_tasks_index.csv` at the repository root carries the header fields for all 300 tasks.

**Upgraded to the v2 stump design:** 1 of 50.

| ID | Task | Domain | Decision shape | Design |
|---|---|---|---|---|
| OS01 | [Summing the lifts of winning experiments: the winners' curse inflates the programme's impact](OS01_experiment-winners-curse-impact-sizing.md) | Digital media / experimentation | 03 · Bridge between two totals | v1 |
| OS02 | [Heat-pump retrofit market: multiplying percentages assumes the conditions are independent](OS02_heat-pump-tam-joint-vs-marginals.md) | Residential energy / HVAC | 09 · Funnel or chain of stages | v1 |
| OS03 | [Treating the worst intersections: last year's crash counts overstate next year's benefit](OS03_hotspot-treatment-regression-to-mean.md) | Road safety / city operations | 03 · Bridge between two totals | v1 |
| OS04 | [Battery arbitrage revenue: hindsight dispatch is not a business case](OS04_battery-arbitrage-perfect-foresight-bias.md) | Electricity markets / energy storage | 03 · Bridge between two totals | v1 |
| OS05 | [Speeding up permits: adding staff anywhere but the bottleneck buys nothing](OS05_permit-pipeline-bottleneck-throughput.md) | Government operations / construction permitting | 09 · Funnel or chain of stages | v1 |
| OS06 | [Retrofit packages: insulation and a heat pump do not save the sum of their separate savings](OS06_retrofit-package-interactive-savings.md) | Building energy / utility programmes | 03 · Bridge between two totals | v1 |
| OS07 | [Sizing a new grocery store: the radius counts people your other stores already serve](OS07_new-store-huff-cannibalization.md) | Retail / food access | 01 · Ranked list under a cap | v1 |
| OS08 | [Replacement market from an installed base: base ÷ mean life ignores the age profile](OS08_ev-battery-replacement-flow-age-hazards.md) | Automotive aftermarket | 02 · Forecast across many periods | v1 |
| OS09 | [Rebate programme savings: customers who would have bought anyway are not savings](OS09_efficiency-rebates-gross-vs-net-savings.md) | Utility energy-efficiency programmes | 03 · Bridge between two totals | v1 |
| OS10 | [Annualising a summer pilot: twelve times July is not a year](OS10_seasonal-pilot-annualization.md) | Urban mobility / bike share | 02 · Forecast across many periods | v1 |
| OS11 | [Toll increase revenue: entries fall when prices rise, and the baseline moved anyway](OS11_congestion-toll-revenue-demand-response.md) | Transportation pricing | 13 · Scenarios and the flip point | v1 |
| OS12 | [Battery add-ons for solar owners: the attach rate on new installs is not the retrofit rate](OS12_battery-attach-rate-new-vs-retrofit.md) | Distributed energy | 02 · Forecast across many periods | v1 |
| OS13 | [New fast-charging sites: count the people newly covered, not everyone within reach](OS13_charger-network-incremental-coverage.md) | EV infrastructure | 01 · Ranked list under a cap | v1 |
| OS14 | [Sizing loss avoided by a security control: the mean breach is driven by a handful of giants](OS14_breach-loss-avoidance-heavy-tail.md) | Cybersecurity / healthcare | 13 · Scenarios and the flip point | v1 |
| OS15 | [Rolling out a readmission programme: a relative reduction means different absolute gains at each hospital](OS15_readmission-program-absolute-vs-relative-effect.md) | Hospital quality / care transitions | 01 · Ranked list under a cap | v1 |
| OS16 | [Which workforce intervention a $2M fund should buy, when the best-measured one runs into seats that are already taken](OS16_workforce-fund-seat-capacity-binding.md) | Policy & Education · workforce development programmes | Which of N gets one scarce thing, with the sizing kept as the graded figure | v2 |
| OS17 | [Child-care supply gaps: tract-by-tract shortfalls ignore that families cross tract lines](OS17_child-care-gaps-floating-catchment.md) | Early childhood services / social infrastructure | 01 · Ranked list under a cap | v1 |
| OS18 | [Selling idle capacity: average idle cores are not cores you can promise for six hours](OS18_harvestable-capacity-duration-aware.md) | Cloud infrastructure | 04 · Setting one dial | v1 |
| OS19 | [More e-book licences, more reading? Net of the print checkouts they replace](OS19_digital-format-cannibalization-net-incremental.md) | Public libraries / digital media | 03 · Bridge between two totals | v1 |
| OS20 | [Remittance savings by corridor: average fees across providers are not what senders pay](OS20_remittance-corridor-savings-volume-weighted.md) | Payments / financial inclusion | 07 · Grid of cells | v1 |
| OS21 | [Time-of-use tariff savings: the average home's profile is nobody's profile, and switchers are not random](OS21_time-of-use-tariff-savings-heterogeneity.md) | Energy retail | 07 · Grid of cells | v1 |
| OS22 | [Fraud model ROI: catching many small frauds is not catching the money](OS22_fraud-model-amount-weighted-net-savings.md) | Payments risk | 04 · Setting one dial | v1 |
| OS23 | [Water loss recovery: not all non-revenue water is leakage, and not all leakage is worth chasing](OS23_water-loss-recoverable-real-losses.md) | Water utilities | 03 · Bridge between two totals | v1 |
| OS24 | [Flexible EV charging: energy delivered is not flexibility at the peak](OS24_ev-charging-peak-shiftable-flexibility.md) | Electricity networks / EV charging | 07 · Grid of cells | v1 |
| OS25 | [Sizing a new state's betting market: launch-month handle is inflated by promotions and novelty](OS25_new-state-betting-market-maturity.md) | Gaming / consumer markets | 02 · Forecast across many periods | v1 |
| OS26 | [Steering patients to lower-priced hospitals: savings are bounded by choice sets and capacity](OS26_outpatient-steering-savings-capacity.md) | Health insurance / provider networks | 05 · Allocation to a fixed total | v1 |
| OS27 | [Which delivery vans can go electric? A van that averages 60 miles still has 140-mile days](OS27_fleet-electrification-tail-day-suitability.md) | Commercial fleets / electrification | 14 · Cuts of a distribution | v1 |
| OS28 | [Which car trips could be e-bike trips? A short trip inside a car tour cannot switch on its own](OS28_micromobility-substitution-tour-based.md) | Urban mobility | 03 · Bridge between two totals | v1 |
| OS29 | [Repowering old wind farms: nameplate added is not energy added](OS29_wind-repowering-energy-uplift.md) | Wind energy | 01 · Ranked list under a cap | v1 |
| OS30 | [Valuing a spectrum holding from auction comparables: average $/MHz-pop across bands mixes apples and oranges](OS30_spectrum-valuation-comparables-by-band.md) | Telecommunications / corporate finance | 07 · Grid of cells | v1 |
| OS31 | [Carbon-cost exposure for a shipping fleet: only part of each voyage's emissions is in scope](OS31_shipping-ets-cost-exposure-scope.md) | Maritime / carbon markets | 02 · Forecast across many periods | v1 |
| OS32 | [Savings from preventable admissions: you will not reach zero, and charges are not costs](OS32_preventable-admissions-achievable-benchmark.md) | Healthcare / population health | 01 · Ranked list under a cap | v1 |
| OS33 | [Converting agency nurses to staff: commit to the base, not the average](OS33_contract-staff-conversion-base-load.md) | Long-term care / workforce | 04 · Setting one dial | v1 |
| OS34 | [Capturing curtailed solar with batteries: a 4-hour battery cannot soak up a 9-hour surplus](OS34_curtailment-capture-battery-limits.md) | Electricity / renewable integration | 07 · Grid of cells | v1 |
| OS35 | [How many lead pipes are there? "Unknown" is not "not lead"](OS35_lead-service-lines-unknown-imputation.md) | Water utilities / public health infrastructure | 03 · Bridge between two totals | v1 |
| OS36 | [Beds freed by fixing delayed discharges: bed-days ÷ 365 is not beds at the winter peak](OS36_delayed-discharge-beds-freed-peak.md) | Hospital operations / social care | 02 · Forecast across many periods | v1 |
| OS37 | [Who can use a transit-pass benefit? Both ends of the commute must be near transit](OS37_commute-benefit-both-ends-eligibility.md) | Employee benefits / urban transport | 01 · Ranked list under a cap | v1 |
| OS38 | [Backyard homes potential: early-adopter neighbourhoods are not the city](OS38_adu-potential-early-adopter-extrapolation.md) | Housing / construction | 13 · Scenarios and the flip point | v1 |
| OS39 | [Crash costs attributable to speeding, alcohol and distraction: the shares add to more than 100%](OS39_crash-cost-attributable-fractions-overlap.md) | Road safety / insurance telematics | 03 · Bridge between two totals | v1 |
| OS40 | [Refinance opportunity: the average outstanding rate hides the loans that would benefit](OS40_refinance-opportunity-rate-distribution.md) | Mortgage lending | 14 · Cuts of a distribution | v1 |
| OS41 | [Water reuse market: withdrawals are not consumption, and return flows are already reused downstream](OS41_water-reuse-consumptive-vs-withdrawals.md) | Water resources / industrial services | 03 · Bridge between two totals | v1 |
| OS42 | [B2B software TAM: a chain with 300 locations buys one contract](OS42_b2b-tam-firms-vs-establishments.md) | Business software / go-to-market | 07 · Grid of cells | v1 |
| OS43 | [Savings from switching to biosimilars: the incumbent cuts its price, so the gap you sized shrinks](OS43_biosimilar-switching-incumbent-price-response.md) | Pharmaceutical pricing / payers | 02 · Forecast across many periods | v1 |
| OS44 | [Cost-down from scale: learning curves run on cumulative volume, not on calendar years](OS44_turbine-cost-learning-curve-cumulative.md) | Wind energy manufacturing | 13 · Scenarios and the flip point | v1 |
| OS45 | [What does auto-enrolment add? Plans that chose it were different to begin with](OS45_retirement-auto-enrollment-within-plan.md) | Retirement plans / HR benefits | 11 · Before and after with a control | v1 |
| OS46 | [Sizing telehealth from 2020: the spike is not the market](OS46_telehealth-steady-state-after-spike.md) | Healthcare delivery / digital health | 02 · Forecast across many periods | v1 |
| OS47 | [Fee revenue at risk under a cap: only large banks report it, and small banks are not small large banks](OS47_overdraft-revenue-at-risk-stratified-ratio.md) | Banking / regulatory impact | 03 · Bridge between two totals | v1 |
| OS48 | [Forest carbon credits: growth that would happen anyway is not a credit](OS48_forest-carbon-additionality-baseline.md) | Forestry / carbon markets | 03 · Bridge between two totals | v1 |
| OS49 | [Invoice-finance market from company accounts: the smallest firms don't report the field you need](OS49_sme-receivables-tam-missing-fields.md) | SME lending / fintech | 07 · Grid of cells | v1 |
| OS50 | [Valuing a salary-sacrifice benefit: the saving depends on the marginal rate, not the average rate](OS50_salary-sacrifice-benefit-marginal-rates.md) | Employee benefits / personal tax | 14 · Cuts of a distribution | v1 |
