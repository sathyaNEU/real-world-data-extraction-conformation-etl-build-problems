# task188 design note

Architecture 2 (re-root 2026-11-03). Architecture 1, the West Nile virus spray zone, is spent and stays at the portal
as shipped on 2026-10-13; its record is under `## Architecture 1 record` and every screen since is in
`## Tried and rejected`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task188.json`, architecture v2, drawn and filed 2026-11-03; v1 moved to
  the card's lineage as spent. `guard.py check`: PASS, no WARN, nearest drivers 0.06 (task27, task66, task120 v3) and
  0.05 (task196 v2, task89 v12).
- **Pairing:** Banking, Credit & Financial Risk, task type `fraud-aml-detection` (serves AD), a cell holding one live
  card (task196, scam incidence by two capture channels). The draw moved here after three passes on 2026-11-01 and a
  fourth on 2026-11-03 screened every other Anomaly Detection cell dead (`## Tried and rejected`).
- **Niche:** Harlow Reach Credit Union, a fictional credit union in the Lower Mainland of British Columbia. Its
  Financial Intelligence Unit (the Unit) monitors the business members its AML/ATF compliance programme classes as
  cash-intensive (full-service and limited-service restaurants, cafes, convenience and grocery retailers, bars, nail
  and beauty salons, car washes, coin laundries, mobile food vendors). Each January the Unit selects the members it
  takes into enhanced investigation for the quarter, under the programme's case acceptance test: the cash a member paid
  into its accounts over the calendar year against the cash its trade with its customers produced.
- **Forcing and forum:** the AML compliance committee's January meeting approves the quarter's investigations
  (`vote_or_meeting`, `committee_or_panel`); a credit union (`financial_institution`); the requester is the Unit's lead
  (`compliance_or_audit`).
- **Call:** which cash-intensive business members the Unit opens enhanced investigations on in the first quarter of
  2027, with each one's 2026 cash paid in, the cash its trade produced and the difference.
- **Shape `other`:** a designation over the segment. Criteria arithmetic before the asks: the designated set (each
  referred member, 2), each referred member's three figures (6), the largest non-qualifier and its three figures (4),
  each referred member's unexplained cash by month (24), the chart with its parts (5), the files (3): 44.
- **Strategy and mechanism:** `population_selection` (the exposure the cash is measured against: the counter trade a
  third party settles, not a peer group, a declaration or the account's own turnover); gap objective then population
  (the declared activity, the peer means and the turnover shares are correct records and are not what the test is
  scored on); decisive generator G14 (the trade's cash-to-card relation carried onto each member's own card trade),
  G3 beside it (the record of cash against the trading operation behind it); Gate G `decomposition_attribution` (each
  member's cash split into what its trade produced and the rest); calibration `none`; context `monitoring_export`.
- **Data-native sentence:** a member's cash comes only from its walk-in customers, whose other payments reach the
  account as its card acquirer's daily settlements under the acquirer's own narrative, while its declared expected
  activity, its peer band and its account's other credits are all things a front's owners set or supply, so the
  settled counter trade is the only measure of the member's business that the laundered money cannot move.
- **Abstraction sentence (the test of Part 6):** "one kind of inflow is judged against what the unit's own activity
  produces, and every benchmark taken from the unit's peers, its declarations or its other inflows moves with the
  anomaly, so only the activity a third party records in a separate channel, carried through the population's
  relation between that channel and the inflow, separates the anomaly from size." Held against every approved and
  shipped build, no reviewer would say it of one: task236 divides a count by an independent estimate of the same
  latent count (no relation between channels is estimated); task196 corrects a dependence between two capture
  channels; task199 reads a count against the effort that produced it; task310 (OPP) reads output a limit held back.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 35 builds, one line each on what bears on
  this cell): 103 a contact fanned out through authorisations; 104 a self-adapting scorer replayed; 119 waits a unit
  could have shortened; 182 each unit's lagged response to a shared driver; 196 two capture channels, the second made by
  the firm's own follow-up; 199 a count against the watchers' filing effort; 184 an indicator saturating with container
  size; 186 an own-history null under shared local cycles; 187 a capped curve averaged over a spread; 189 bounds from
  two laboratories' limits; 191 an extremum against a null extremum; 192 a classifier's transport; 193 sequence
  symmetry from first-receipt dates; 195 a paired interval; 197 a programme traverse; 204 an unsteady balance; 125 a
  first-visit cap; 180 detection in quiet hours; 181 crossings; 183 repeat failers; 185 a reading-dependent
  conversion. None benchmarks an inflow against a separately settled channel, and none in the banking cell.
- **People** (`guard.py names --geo canada --seed 188`): Kristine Kirby (the credit union's Chief Anti-Money
  Laundering Officer, who chairs the committee) and Jeffrey Melendez (the Unit's lead). Neither appears in the prompt.
- **Sources:** FINTRAC's large cash transaction reporting (CAD 10,000 or more in one transaction or within 24
  consecutive hours by or on behalf of one person or entity) and its money laundering indicators for cash-intensive
  businesses (cash takings inconsistent with the business's size and sales pattern; expected activity declared high at
  account opening); card acquiring practice (daily settlement of card sales net of the discount fee, one or two business
  days after the sale, under the acquirer's own narrative and merchant number); delivery platforms paying restaurants
  weekly, net of commission, for orders paid online. Every organisation, member, acquirer and platform in the pack is
  fictional.

## Default path

The pipeline a competent AML analyst builds from the question's words, the programme and the files' grain.

1. Read the programme's case acceptance section: the test is on the cash a member paid in during 2026 against the cash
   its trade with its customers produced, an excess of CAD 100,000 or more and at least twice the produced cash.
2. Total each cash-intensive member's 2026 cash paid in from the postings: the cash portion of counter deposits, ATM
   deposits and night deposits, on branch-local days, across every account the member holds.
3. Take the cash its trade produced as what the member told the credit union its trade would produce, its CDD
   profile's expected monthly cash deposits times twelve: the field's standard measure of activity consistent with the
   customer's profile.
4. Cross-check against the peer route the monitoring scenarios use: the mean 2026 cash of the member's trade and
   declared turnover band.
5. Apply the test and file the members it refers.

**Ends on:** refer Kingsway Pho House and Bright Spark Car Wash, two honest members whose 2026 cash is more than three
times the expected activity they declared at onboarding in 2018 and 2019, and clear Pacifica Donair & Pizza and Lumen
Nail Bar, whose declarations cover what they paid in (figures fixed by the generator at stage 3).

**Golden:** refer Pacifica Donair & Pizza and Lumen Nail Bar, each of whom paid in more than three times the cash its
counter trade produced, that trade read from its card acquirer's settlements through its own trade's cash-to-card
relation across the credit union's book (figures fixed by the generator at stage 3).

## Stump sentence

The solver refers Kingsway Pho House and Bright Spark Car Wash because it judges each member's 2026 cash against the
expected activity the member declared, or against its peers or the account's own turnover, and clears Pacifica Donair &
Pizza and Lumen Nail Bar, whose declarations were set high at onboarding and whose network's business payments swell
their turnover, when only the walk-in trade their card acquirers settle shows that each paid in more than three times
the cash its counter trade produces.

## Three rules

- **Task type:** banking-credit-financial-risk / fraud-aml-detection, which serves Anomaly Detection: separating
  laundered cash from the ordinary takings of a cash-intensive business is that task type's own work.
- **Domain test:** the deciding quantity is each business member's cash paid in beyond the cash its trade with its
  customers produced, the core quantity of cash-intensive business monitoring in anti-money-laundering work, estimated
  the way the field estimates a customer's expected cash: from the business's own trade and what that kind of trade
  pays in cash; with hospitals or megawatt-hours in place of takeaways and salons there are no tills, card terminals,
  acquirer settlements or placement of criminal cash, so the task stops making sense.
- **Swap:** "which hospitals should the inspectorate investigate for megawatt-hours beyond what their patient trade
  produces" has no tills, no card terminal settling the same counter's sales, no criminal cash to place and no
  declaration a front could inflate; the call does not survive the swap.
- **Layer 1:** postings coded by the core banking system with each processor's own narrative (two card acquirers, two
  delivery platforms, business payments, owner and loan transfers); counter deposits that mix cash and cheques, cash
  portion in its own field; timestamps in UTC against Pacific branch days; members holding more than one account;
  CDD profiles of different review vintages; an acquirer's monthly merchant statements in PDF carrying gross sales
  against the net daily settlements; an LCTR filing log keyed by report number. Each comes from the system that makes
  it; none is placed to be caught.
- **Layer 2:** estimand_identification: the right counterfactual for a member's cash, the cash its own counter trade
  produces, measured through a channel the laundered money cannot reach, against the declared, peer and turnover
  benchmarks that all move with it.
- **Decisive step:** judging each member's cash against the cash its counter trade produces, that trade taken from the
  card acquirer settlements, the one record of the member's walk-in sales that a third party makes and that neither the
  laundered cash nor the network's payments can inflate, carried through its own trade's cash-to-card relation across
  the credit union's book.
- **Not semantics:** every field, code, narrative and definition read correctly (the cash portions, the channels, the
  settlements, the payouts, the declarations) still leaves the declared-activity, peer and turnover routes on Kingsway
  Pho House and Bright Spark Car Wash, because those routes are computed correctly on correctly read data; no field says
  which benchmark the fronts' own money moves.
- **Not rule application:** no filed rule computes the cash a member's trade produced: the programme sets the test on
  it (CAD 100,000 and twice the produced cash) and leaves the estimate to the Unit, so executing every filed rule with
  the declared activity, the peer mean or the trade's cash share of turnover files the wrong set. Measured on the
  prototype (`scratchpad proto4.py`, to be re-measured by `generator/checks.py` on the build): the enumerated family
  (declared activity, peer mean, turnover share, non-cash credits, all settlements, counter card under six statistics)
  names five different sets; the standing family (counter card under the median, ratio of totals, trimmed median,
  through-origin and log-log fits) names one set in 17 of 20 worlds with the fronts' unexplained cash spread about 3
  per cent; what rules the others out is the data itself (honest members' cash moves with their card trade and not
  with business payments or platform payouts), not a sentence.
- **Analyst test:** a strong analyst who reads every field and the programme correctly takes the produced cash as the
  member's declared expected activity, or its trade-and-band peers, or its trade's cash share of everything else the
  account received, and refers Kingsway Pho House and Bright Spark Car Wash while Pacifica Donair & Pizza and Lumen
  Nail Bar pass, because their laundered cash and their network's business payments inflate exactly the measures those
  routes divide by.
- **Estimand:** filed in `hrcu_aml_atf_programme_2026.pdf` section 7.3 (case acceptance): population, the business
  members in the cash-intensive segment at 31 December 2026; outcome, the cash paid into the member's accounts in 2026
  beyond the cash its trade with its customers produced in 2026; window, calendar 2026 on branch-local days; unit, CAD
  per member; comparison, the test's CAD 100,000 and twice the produced cash.
- **No decoy:** nothing is planted to be caught: the declarations are the members' own onboarding statements, the
  network payments are the fronts' ordinary layering, and no memo, draft, briefing or stakeholder figure argues for any
  member.
- **No certified replay:** no certified or published figure is reproduced to recover a method; the pack holds no
  control total of produced cash and no prior referral whose figures a method must match.
- **Lesson:** an anomaly's benchmark must be one it cannot move: a front's declarations, peers and turnover all rise
  with its laundered cash and its network's payments, so only the trade a third party settles in a separate channel,
  carried through the population's relation between that channel and cash, separates laundering from size; no build on
  file teaches it (the nearest, task236, divides by an independent estimate of the same latent count).

## Survivor anatomy

- **Actor:** the deciding property, how much cash a member's counter trade produces, has no column: the postings
  carry each credit's amount and narrative, the counter card trade is a sum of acquirer settlements recognised by their
  narrative, and a trade's cash-to-card relation exists only across the population.
- **Link:** the step reads each member's cash through its card acquirer's settlements, a comparison across payment
  channels that monitoring of cash never asks for, and keyed by nothing: the settlements carry the acquirer's own
  merchant number and wording, not the member's.
- **Reflex:** the field's own routes, the CDD profile's expected activity and the monitoring scenarios' peer group, sit
  at rungs 0 and 1 and refer Kingsway Pho House and Bright Spark Car Wash.
- **Back-test:** the textbook route validates on the pack's own record: the members the declared-activity route refers
  on 2026 it refers in each half-year, the peer route agrees on them, and the fronts sit inside their declarations in
  every quarter, so a solver checking the route for stability finds it stable.
- **Second use:** every file the decisive step reads has its own reason to be in the pack: the postings are the spine of
  every figure and ask, the member register gives every route its trades and accounts, and nothing ships only for the
  card benchmark.
- **Shock:** the fronts are ordinary on every shipped statistic: mid-pack on cash paid in within their trades, inside
  their declarations, under two standard deviations of their peer bands, and neither is the largest receiver of
  business payments in its trade.
- **Pins:** the WHAT is filed once, in the programme's case acceptance section in the credit union's own voice; no
  sentence names card trade, a channel, a ratio, a peer group or a declaration as the measure, so no filed sentence names
  what the stump rides on.

## Architecture 1 record

Architecture 1 (drawn 2026-10-13, shipped 2026-10-13, at the portal and pending): Rindal County Vector Control
District's one aerial adulticide zone for Thursday 20 August 2026, judged by the estimated West Nile virus-infected
Culex females per CO2 trap-night in week 32; golden Westbrook at 2.3 by maximum likelihood on the CO2-trap pools
against the minimum infection rate's Riverside South. Judge: DETERMINISTIC, APPROVE (pass 3,
`determinism_check_report_pass3.md`, kept as evidence). Spent on measurement on 2026-10-21 and confirmed 2026-11-01:
the decisive estimator family names one zone of 12 licensed constructions, so the step is a reflex (the full
re-screen is in the git history of this note at commit 0c21d67 and in the card's lineage).

## Tried and rejected

- Seed AD11's own world (route-origin paging at a cloud platform, RPKI invalid against not-found): no client domain's
  Anomaly Detection task type does routing analysis, and General Statistics' multiple testing would make network
  operations a backdrop; rejected at the draw on the domain rule.
- Political science conflict event data (attacks on civilians estimated from the overlap of the commission's monitors
  and the media, multiple systems estimation): capture-recapture reads the same in epidemiology with two surveillance
  lists, so the swap test survives; rejected at the draw.
- Pharmacovigilance signal triage (co-reporting and masking in disproportionality): the comparison has to be filed for
  determinism and filing it names the decisive step; rejected at the draw.
- Legionnaires' source attribution (plume touchdown and where cases were exposed): root cause, not anomaly detection,
  and practice disinfects every tower in the area at once; rejected at the draw.
- Influenza positivity standardised by days from onset to swab: a measurement-condition normalisation, the lane's third
  after task180 (noise) and task187 (turbulence); rejected at the draw.
- A resident-weighted index (traps sited on the marsh rather than among residents): an estimand that names residents
  makes the solver ask where they live (readability test 1); rejected as the decisive step at the draw.
- Westbrook with eleven CO2 sites (22 trap-nights a week): the likelihood estimate's own bias put the likelihood,
  bias-corrected and Jeffreys-penalised figures up to 2.4 per cent apart, straddling a one-decimal bin in most draws;
  four sites added in the zone's untrapped sections (30 trap-nights) and the draw chosen with every variant inside one
  bin, asserted.
- A second load that re-entered every 1 to 14 June night (432 records, keyed by the pickup morning): half of them
  landed on a night the site had already run, with that night's own status and catch, so the ask had three defensible
  readings (keep the first entry, keep the second, keep both) and the leak reader found the fork. The load now brings
  back the June Tuesday nights only (206 records), every one on a Wednesday the protocol schedules for no zone but
  Maple Ridge's enhanced fortnight.
- Resuming architecture 1 after the wave 8 Gate F failure by moving the protocol's filed definitions (the plan in `pipeline.json`'s resume line): refused on measurement before any design work. The decisive step's estimator family returns 1 distinct designated zone of 12 licensed constructions on the shipped draw and 1.15 over 20 redraws, so the step is a reflex whatever the protocol says and rewording 3.1, 3.2, 3.6 and 4.1 cannot put content into it; the same family spreads the printed call figure 3.5 printed units, so the clauses were load-bearing for Gate C and not for Gate F (`generator/family_screen.py`, `## Gate F re-screen`).
- Re-siting the decisive step onto which pools stand for the CO2-caught females, or onto which trap-nights count: each settles a part of the estimand (the population, the denominator and unit), which `determinism-check` section 1 requires filed, so filing it is rule application and leaving it unfiled forks the main call; dead on the WHAT screen with no hardening available.
- Keeping the unequal-pool-size likelihood as the decisive construction on any redraw of this world: the lever and the ceiling are one quantity. Over 20 redraws the family splits on the designation in 3, and in those 3 the separation is 0.11 and 0.13 of the family's own spread; in the other 17 the family is unanimous. No setting makes the estimator choice both matter and be determinate, so the architecture is spent rather than mistuned.
- **(2026-10-25, measured) A blind reader landed the call and took 74.0 per cent of the ask figures.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **Westbrook on Thursday 20 August 2026 at 2.328 infected Culex females per CO2 trap-night**, with South Prairie at 1.811 as runner-up and a flip at 18.29 per 1,000, and hit **16 of 18 call figures and 71 of 96 ask figures**. It took the decisive step by naming the maximum-likelihood pooled-sample estimate over the minimum infection rate in one line, because pool size differs between the two laboratories, and it enumerated the rungs it had refused: MIR picks South Prairie, including gravid traps picks Old Town at 5.6, counting failed trap-nights changes nothing. It also parsed all 1,155 pools out of the county laboratory PDF because week 32 was not yet keyed into the database, and re-derived every case's zone from its residence section against the 2026 sections, finding the case log's own zone column disagrees on 8. Readability test 3: the pooled-sample MLE is the standard estimator in arbovirus surveillance, so refusing MIR is the reflex and not the insight.
- **(2026-11-01) Architecture 1 marked spent and a re-root to architecture 2 opened at stage 1; no candidate cleared the screens on paper, so nothing was carded.** Each was screened against `guard.py mechanisms --objective anomaly-detection`, `guard.py slots` on mechanism and setting nouns, and the neighbouring slots' notes:
  - Crime incidence hotspots (a force's burglary alert triage, each beat's excess read against its prolific offenders' periods at liberty, linked across the prison release list and the court remand list with no key): task182's architecture 8 screen already closed it (the custody nights are a clean subset, so a filter and a divide estimates the same quantity, and the swap reads the same with super-spreaders), and its section 8 closes the cell's other fifteen candidates; the forward form ("which beat records most over the squad's four weeks") is Forecasting, not this number's objective.
  - Pharmacovigilance, a self-controlled case series biased by event-dependent exposure: task180's landing record (the plain SCCS was enough); masking in disproportionality: task193's judge SEND_BACK and this slot's own earlier line.
  - Card fraud common point of purchase with the exposure window ending at the fraudster's first test transaction: task181's architecture 1 died on the co-visit subset check, and recognising card testing is a payments analyst's reflex (readability test 3).
  - Electricity theft by feeder energy balance with a stale connectivity model mirroring one feeder's excess as its neighbour's deficit: no client task type carries non-technical loss detection as Anomaly Detection (grid-reliability-outage-analysis is outages); the outage form normalises by faults per 100 km, the field's own metric, which no customer transfer moves.
  - River load against concentration below a discharge (dilution at low flow): load is the field's first move, a reflex.
  - Rail SPAD risk per approach at danger from the train describer and aspect logs: once the WHAT is filed per approach at danger the time-overlap join is the literal construction (rule application); left unfiled the denominator is the WHAT screen.
  - A GWAS locus inflated by cryptic relatedness: kinship QC is the field's standard step; a surgeon outlier attributed through the theatre log: a join on a shipped key.
  What is left for the next draw: a quantity forced by arithmetic from a file at another grain whose correction touches every record (task182 section 9's finding, which this pass reproduced on four more grounds), in an Anomaly Detection cell other than disease surveillance (banned against task232) and crime hotspots (enumerated closed).
- **(2026-11-01, second pass) The four Anomaly Detection cells left open by the first pass, four or more candidates each, every one drawn from what that cell's own systems do to the records and screened on paper (default path, swap, survivor anatomy, bin test); none clears, so nothing is carded.**
  - provider-quality-risk-adjustment. (1) Comorbidity coding depth, each hospital coding its own case mix, corrected by a look-back through the patient's admissions elsewhere: default path, the index-coded SMR, ends on the under-coding hospital; swap holds (coding, Charlson, 30-day deaths); dies on `Reflex:` and `Actor:`, the look-back is the field's own comorbidity practice and a self-join on the person key, task271 architecture 1 landed by both stage 4 readers and task273's architecture 4 screen. (2) Thirty-day deaths found only through the death register link: `Actor:` holds, but it is task468's linker-error driver. (3) Deaths credited to the hospital of first admission across transfers: the superspell is the published indicator's own construction, a reflex. (4) Expected deaths from last year's national model while mortality falls: the step rescales the comparison, which the WHAT screen makes rule application once filed and a fork when not; bin test fails, the rescaled SMRs move 0.04 to 0.06 against a 0.1 bin. (5) Observer-sampled compliance: task269's driver.
  - payment-claims-health-plan-analytics. (1) Void-and-replace adjustments inflating gross paid: the replacement carries the original claim number, a shipped key (`Link:`). (2) A member's other coverage ending, so the plan turns primary and paid rises: allowed amount, the field's first view, is untouched by primacy (a reflex). (3) A practice absorbing a retiring colleague's panel, new-patient visits billing higher: new against established is in the procedure code (`Actor:`, a column). (4) Time-based office visit levels against the appointment system's check-in and check-out times: the code's time threshold is a published rule, rule application. (5) Drug units against weight-based dosing: the plan holds no weights (Gate B, the input absent). (6) The lesser-of allowance: task198's driver.
  - exploratory-data-analysis-distribution-assessment. (1) Release results retested into compliance, a deficit just past the specification limit: the decisive evidence is the chromatography audit trail's unreported injections, a planted behaviour (rule 3), and without it the true batch distribution has to be deconvolved, an open family (Gate C). (2) Digit preference after an instrument change: task185's device conversion. (3) Results above the range reported as greater-than: task188-era censoring by instrument limit, spent. (4) Snapshots of work in progress: task182's length bias. (5) A mixture of two production routes: the route is on the batch record (`Actor:`, a column).
  - safety-incident-error-analysis. (1) Pressure ulcers first recorded on the ward a patient was transferred to: the national 72-hour attribution rule makes it rule application, and without it the stage-to-onset time is a free parameter (bin test fails). (2) Medication errors at night with no pharmacist to intercept them: rebuilding the unintercepted errors from the day's intercepts per order, raised to night orders, is task275's approved driver. (3) Incidents per dose from the administration record: a denominator, the WHAT screen. (4) Several staff reporting one event: task103's fan-out. (5) Severity regraded after review: task194's vintages. (6) Blood units travelling with transferred patients, unaccounted at the issuing site: the donation number is a universal key (`Link:`). (7) Falls per midnight-census bed-day on a ward turned short-stay: the answer flips on the denominator's definition, data semantics.
  The cell occupancy behind this: every Anomaly Detection task type in the taxonomy now has its native recording processes either spent on a card or slot note, closed by task182 section 8, or barred by the three rules. The next draw for this number needs an author's ruling (a cell outside the four named, such as environmental-monitoring-exceedance or conflict-protest-event-data-analysis, or the objective's quota reconsidered).
- **(2026-11-01, third pass) The last two Anomaly Detection cells, each candidate drawn from what the organisation's monitoring or event-coding systems do to the records; none clears, so nothing is carded.**
  - environmental-monitoring-exceedance. (1) A trade discharger's daily mass load from 24-hour time-proportional composites, where concentration and flow move together within the day and an online analyser's hourly profile rebuilds the flow-weighted load (default path, composite times daily flow, ends on the night-dumping discharger; `Actor:` and `Link:` hold, a time join of two process-control logs no clause invites, and the regulator's audit composites agree on the wrong reading): the strongest candidate of the pass, and already measured dead on record, task190 architecture 9 candidate P3 (the per-day flow-weighted mean rebuilt from the autosampler's aliquot log, dead on the floor's other horn), task204 (flow-weighted and diurnally weighted loads killed on the swap test, each reading the same in any field's nouns) and task198 (load estimation as a ratio of totals against a mean of ratios, task200's estimand death). A recorded measured death outranks a fresh prototype, so no prototype was run. (2) Storm-triggered autosampling, events sampled only once flow passes a trigger: the trigger setting sits in the sampler configuration (`Actor:`, a column), and the selection it makes is task180's detection threshold. (3) Passive samplers whose two- to four-week exposure periods straddle the compliance year: apportioning them is the periods-complete filter and divide task198 closed, and the bin test fails on the annual mean's first decimal. (4) A fenceline monitor's exceedances read by wind sector against a regional background: the nuisance estimated where the signal vanishes, closed by task201. (5) An analyser dropping out on its heaviest days: task245's informative outage. (6) Gaps filled by decay toward normal: task247.
  - conflict-protest-event-data-analysis. (1) Fatalities coded at the lowest credible estimate: a filed coding rule, rule application. (2) Events of unknown place coded to the province capital: the precision code is a column, data semantics. (3) A multi-day protest coded as one event per day: the unit of count, the WHAT screen and task103's fan-out. (4) Coverage driven by the watchers' own filing volume: task199. (5) Two monitoring lists overlapping, capture-recapture: this slot's own earlier line (the swap reads the same with two surveillance lists). (6) A machine-coded event classifier validated only on the opening months: task192. (7) Events backfilled into earlier weeks as reports arrive: task194's vintages.
  With this pass every Anomaly Detection task type in the taxonomy has been screened: 37 candidates across eight cells on 2026-11-01, each dead on a recorded measurement, the three rules, the WHAT screen, a column or key, a filed rule or a spent driver. What remains open for this number is the author's call: a waiver for a cell repeat (disease surveillance against task232's ban, or a spent driver re-sited), or the slot handed on.
- **(2026-11-03, fourth pass, under the author's instruction to proceed)** Eight candidates screened on paper before
  the draw, each with its default path, swap, anatomy and bin test; seven dead, the eighth carded:
  - A GWAS meta-analysis whose contributing cohorts share a control panel, so inverse-variance pooling as if
    independent inflates the loci the shared controls deviate on: the abstraction is task195's paired difference on
    shared units (shipped 10-17), and task200's slot killed it on the same test.
  - Fast-trip protection on fire-season days turning transient faults into sustained interruptions: the artifact is a
    policy counterfactual, and once the estimand is a fault count the step is reading the estimand (faults against
    interruptions), data semantics.
  - A drug's disproportionality inherited from a co-prescribed cause (the innocent bystander): task181 v1's pooled
    sources in other nouns, a pharmacovigilance reflex, and the comparator background is the estimand's comparison.
  - A business survey's ratio imputation under nonresponse that a flood made informative, read from later VAT returns:
    task275's re-imputation of the unobserved from a record about them (approved).
  - Estuarine sampling locked to a tidal phase: dead on the physics, since fortnightly fixed-time sampling drifts about
    37 minutes of tidal phase a visit and spreads over the whole cycle within a year; only a protocol cutover makes the
    artifact, which is the dated-cutover family.
  - Lightning outages normalised by strokes near each feeder's route: task182's own response to a shared driver, and the
    corridor radius is a free parameter the bin test fails on.
  - Restoration time inflated by a shared crew pool: the outage system records dispatch, so the queue is a column
    subtraction, and single-server queueing reads the same in any field (the swap fails).
  - Carded: a cash-intensive business member's cash judged against the counter trade its card acquirer settles.
- **(2026-11-03) Prototype iterations of the carded draw, each dead as built:** proto1 and proto2 put the fronts at
  their own trade's typical size, so the peer route flagged one of them (z 2.9) and large honest members' absolute
  excess (to CAD 385,000 at a 30 per cent cash share) beat the second front; the fronts were redrawn as small genuine
  traders whose total cash matches the band they declared. proto3 tested the absolute CAD threshold alone and let large
  honest members through, so the programme's test carries a relative arm (at least twice the produced cash). proto4
  held 17 of 20 worlds; the three that failed had a front whose own genuine cash-to-card ratio sat below its trade's, so
  laundering set as a multiple of its own cash fell near the relative arm; the generator sets each front's laundering
  against its trade's relation and asserts the margin. In every prototype a cash-intensity ranking within the trade
  put the takeaway front first while the test computed on turnover shares referred nobody: the call is the test's
  designation, never a ranking, so that ranking is no route to it.
