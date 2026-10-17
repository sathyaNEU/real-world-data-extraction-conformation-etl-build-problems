# task465 design note: Callowmere Electric's 2027 medical energy assistance caseworkers

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: the slot's seed
world (a drought cover) was spent across a rainfall draft and architecture 1 (area-yield covers with withheld drought
years, sent back by the determinism judge on Gate H), and architecture 2 is drawn afresh in the ETL objective.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task465.json`, architecture v2, re-registered 2026-10-17 after
  architecture 1's SEND_BACK; architecture 1 and the rainfall draft are in its lineage with their fates. `guard.py
  check`: WARN only, answered below.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL. The task
  type's own work here is statistical matching: two surveys of the same households, each measuring one of the two
  eligibility traits, fused through the variables they share, with an auxiliary sample that measured both. The
  conformed division-by-income-band table is the ETL deliverable the staffing is set on.
- **Why this mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457), capture and coverage
  of registers (448, 454, 455), links and continuity (449, 455), a link through shared items (450), a rotating panel's
  measurement change (453), a stratified sample on a revised map (452), latent classes (456), observation selected on
  the trait (458), an operating level (459), a dispatch margin (460), an overlap extension (461), detection-weighted
  snapshots (462), a drift-free price index (463), a change in each unit's own record (464 v1) and withheld cells
  recovered from totals (465 v1). None fuses two sources that never observed the decisive pair of variables together.
- **Shape:** 07, a grid of cells: nine service divisions, each with its eligible households and its caseworkers (18
  cells), the total, the chart's named parts and the two files (24 before the asks); the asks add a figure per
  division each.
- **Strategy:** composition_mix (F5): the health survey's equipment rate is correct for each division and income band
  but does not fit the pool of energy-burdened households inside the band, whose rate is higher; the pool's rate is
  rebuilt from the screening pilot, which observed both traits. Gap population (the eligible households are the joint
  of two traits; the default path counts independent coincidences). Generators G14 (decisive) and G16 (which fusion
  the data entitles). Gate G method_or_model_selection. Layer 2 family estimation_fit.
- **World:** an unnamed state. Callowmere Electric Company, its investor-owned electric utility, runs the Home Energy
  Medical Assistance programme (HEMA) for low-income customers in whose homes someone relies on electrically powered
  medical equipment (oxygen concentrators, home dialysis, ventilators, powered wheelchairs, feeding pumps). Its
  caseworkers enrol eligible households in the medical baseline rate, arrange payment plans and place backup
  batteries. The utility files its 2027 HEMA plan with the State Utility Commission by 1 December 2026; the plan sets
  one caseworker for every 1,200 eligible households in a service division, or part of that number. No survey asked
  both eligibility questions: the State Energy Office's Household Energy Affordability Survey 2025 measured energy
  burden, the State Department of Health's State Health Survey 2025 measured the equipment, both weighted to the State
  Demographer's household estimates by county and income band, and Callowmere's 2025 HEMA screening pilot asked both
  questions of a random sample of residential service addresses.
- **Data-native sentence:** the equipment that makes a household eligible also runs up its electricity bill (a
  concentrator or a dialysis machine runs for hours every day), so inside every income band the two traits go
  together; the state measured them in two surveys of the same households, and only the utility's screening pilot
  asked both questions of the same homes.
- **Forum and forcing event:** regulator_or_inspector (the State Utility Commission receives the plan),
  statutory_or_regulatory_filing (the 2027 plan, due 1 December 2026); organisation utility_or_infrastructure; role
  capacity_planner. Personas from `guard.py names --geo us --seed 465`: Stacy Williams (HEMA programme manager, who
  sets the staffing), Shawn Taylor (vice president, customer programmes). As-of date 16 November 2026.
- **Sources (one line each):** the client's data-integration pattern (propagate linkage error) teaches that a
  combined estimate inherits the integration's error; here the integration error is the matching assumption, not a
  link. task256 carries a reference survey to members through a conditional distribution; here two surveys measure
  different traits of one population. task233 transports a departure on the odds scale; here nothing is transported
  across levels, the odds ratio is the pilot's within-band association kept inside each cell.
- **WARN answers:** `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection after task235 and task264): the
  method chosen here is the fusion of two surveys, a data-integration estimate the other builds do not make;
  `repeat.question_form` (how-many after task264): the decision is a count of caseworkers per division.

## Default path

1. Read the energy survey's household file: annual home energy cost (electricity annualised where it was reported as
   a monthly average, plus gas and delivered fuels) over household income, high burden above 6 per cent; income band
   from income; service division from county; the weighted share with high burden in each division and band.
2. Read the health survey's household file: service division from the county code, income band from its eight income
   categories, the equipment item without don't-know and refused answers; the weighted share with equipment in each
   division and band.
3. Households in each division and band from the household estimates (the surveys' weights total the same).
4. Eligible households in each division and band: households times the burden share times the equipment share;
   summed by division.
5. Caseworkers: each division's eligible households over 1,200, rounded up.
- **Ends on:** staffs 14 caseworkers.
- **Golden:** staffs 25 caseworkers, the eligible households in each division and band fused from the two surveys'
  rates with the screening pilot's within-band odds ratio between the two traits, each cell keeping both surveys'
  rates.

## Stump sentence

The default path aligns the two surveys and multiplies each division-and-band cell's burden rate by its equipment rate,
treating the two traits as independent inside the cell, so it counts about half the eligible households and staffs 14
caseworkers where the programme needs 25; carrying the screening pilot's within-band association into each cell, with
both surveys' rates kept, counts them, while the pilot's own shares or one survey's rate times the pilot's conditional
rate keep only one survey's estimates and staff other wrong numbers.

## Three rules

- **Task type:** data integration (data-integration-record-linkage-entity-resolution): statistical matching of two
  surveys of the same households with an auxiliary sample that observed both variables; the ETL objective's conformed
  division-by-band table is the dataset the staffing is set on.
- **Domain test:** the deciding quantity is each division's count of households carrying both traits, a joint
  distribution no large survey observed; the field's method is statistical matching with auxiliary information, the
  auxiliary sample's within-cell association carried into tables calibrated to both surveys' estimates.
- **Swap:** General Statistics, so the swap is of the method: replace the fused joint with the product of the two
  surveys' rates (conditional independence) and most divisions' staffing changes; replace it with the pilot's own
  shares and it changes again. A noun swap (clinics for divisions, smoking for burden) keeps the same fusion, because
  the domain here is the method.
- **Layer 1:** the two surveys on different geographies (county names and service divisions in one, county codes and
  public health districts in the other: the agencies' own sampling frames); income in dollars in one and in eight
  categories in the other (each survey's questionnaire); energy costs as annual totals or monthly averages (how
  respondents answered); a base and a final weight in one survey and a person and a household weight in the other
  (their weighting files); don't-know and refused codes (the questionnaire); pilot screens duplicated where an address
  answered by mail and by phone (the utility's screening system); household estimates published with division
  subtotals and a state total among the county rows (the demographer's release). Nothing is placed to be caught.
- **Layer 2:** estimation that fits the data: statistical matching beyond conditional independence. The choice that
  flips the call is how the joint of the two traits is built from sources that never measured them together.
- **Decisive step:** fuse the two surveys' division-and-band rates with the screening pilot's within-band odds ratio,
  an association-preserving fusion that keeps both surveys' rates, instead of multiplying the rates.
- **Not semantics:** every field read correctly (burden from annualised costs, the eight categories nested into the
  four bands, the household weight, don't-know and refused left out, county codes to divisions) still leaves the
  product of the two surveys' rates; what moves the call is the analysis that the two traits go together inside the
  cells, which no field, code or definition states.
- **Not rule application:** no filed rule says how the two surveys combine into the eligible count; the plan's data
  annex requires the conformed table to agree with the household estimates and both surveys' weighted estimates, which
  the product of the rates satisfies as well as the fused table, so executing every filed rule still files the default.
- **Analyst test:** a strong analyst who aligns both surveys' geographies and income bands, annualises costs, uses the
  right weights, drops don't-know and refused answers and reads the plan's caseload standard joins the two surveys'
  rates on division and income band and multiplies them, and staffs 14 caseworkers (the default path's `Ends on:`).
- **Estimand:** the HEMA plan's eligibility and data annex (`callowmere_hema_plan_2027_draft.pdf`): eligible households
  are households in the territory whose annual home energy costs exceed 6 per cent of income and in which someone
  relies on electrically powered medical equipment at home, counted for each service division for 2025; the conformed
  table by division and income band agrees with the household estimates and with each survey's weighted estimates;
  one caseworker for every 1,200 eligible households in a division, or part of that number.
- **No decoy:** nothing is planted: the pilot is the utility's own test of its screener, its association is the
  equipment's electricity use, no memo argues for independence, and no file states an eligible count.
- **No certified replay:** no certified figure is reproduced to recover a method; the surveys' published estimates are
  inputs the fused table keeps, never a key to the method.
- **Lesson:** two sources that each measured one trait cannot be joined on the attributes they share and multiplied
  when a third source shows the traits go together inside those attributes; the joint has to carry that within-cell
  association into tables that keep both sources' estimates. No build on file teaches statistical matching's
  conditional-independence assumption.

## Tried and rejected

- A rainfall index on cooperative-observer gauges with dormant seasons rebuilt from the airport, the decisive move
  averaging the kinked payout over the rebuilding's error: the expectation-of-a-nonlinear-payout lesson is already
  task151's (a stepped payout over the season total's distribution), task187's and task229's; superseded before any
  data was cut.
- A district index averaged over a network that grew from three gauges to seven: the variance of a three-gauge mean
  exceeds a seven-gauge mean's by only 5 to 15 per cent at the region's inter-gauge correlations, and in a prototype the
  burn's sampling noise swamped it in half the draws; no stable call.
- Station breaks (a gauge moved, an instrument changed): the change found in a unit's own record is task464's spent
  architecture.
- Carrying a short gauge record through a long airport record by the overlap's ratio: task461's driver.
- Withholding framed as a disclosure rule (fewer than three farms, to protect individual operations): a confidentiality
  rule needs complementary suppression, which would stop the single-county subtraction and make the design read as a
  leak engineered for the solver; re-framed as the service's publication standard for reliability (fewer than five
  reports or a coefficient of variation above 30 per cent), which needs none (stage 2, 2026-10-17).
- Two sandy counties in two districts with a golden buying both their covers (the drawn calibration): a reading of
  every withheld mark as a total crop failure buys the same pair, and with the other three counties' calls the same on
  every route the grid left a wrong call four of five covers right; re-laid at stage 2 with four sandy counties in four
  districts, three bought on recovery, one (Tresham) dear even with its years back so the total-failure reading files
  another set, and Corvin, with every year published, dear on every route.
- Re-rooting the decisive step on the same world was weighed at stage 2 and dropped: carrying past shortfalls forward
  in proportion to the trend level (a regression diagnostic, not this task type's analysis, and additive against
  proportional reads as a convention to a literal judge); allocating district counts by an ancillary density, a stop-loss
  layer's leveraged trend and pooled medians against averaged ones (each a weaker default path in another world).
- Architecture 1, the withheld drought years recovered from the district totals as the decisive step (selection on the
  outcome): judge SEND_BACK at stage 4 (2026-10-17), Gate H `decisive_step: rule_application`. The recovery is an
  identity the methods note files (2.1), and with the cells restored the call is the policy's filed formula, so the
  stump sat in Layer 1 (suppressed cells) and the term sheet's filed additive rating basis left no estimation choice.
  The world, the pack and the recovery stay usable as Layer 1 cleaning for architecture 2.
- Architecture 2 candidates on the area-yield world, weighed at the re-root and dropped: past shortfalls scaled with
  the trend level (heteroscedastic burn), the transport-scale lesson task233 and task258 already teach; a trend that
  plateaued, chosen out of sample (every plateau-aware fit gives a different expected loss, no unique figure); the
  expected loss conditioned on the La Nina outlook or on the 2026 drought (the conditional and unconditional estimands
  both defensible on the policy's wording); credibility weighting toward the district (only by filing the method);
  monthly series benchmarked to annual totals in a new world (the extrapolation turns on an assumed ratio path).
- The fused-survey card first checked without a registration stamp: the guard sorted it before every card drawn the
  same day and compared it with the wrong batch (G14 against task233, G16 against task463); stamped, the honest G14
  signature is clear of the batch and differentiated against the older builds that share it.
