# task163 design note

Architecture 1, drawn 2026-10-18 (wave 6, Forecasting lane, sathya8571), numbered from seed FC34. The seed (a payroll
company sizing its 2027 sales plan on first-time employers in its twelve core states, from business-application and
formation statistics by state, after three states opened one-stop filing) was read at its header and Situation only.
Its world, decision and quantity are kept. Its decoy-era mechanism (a channel field and a change-log entry that hand
over the conversion adjustment) is not shipped: no field marks an application as added by a reform, and the change
log states what each state's system does and when, never what it does to formations. The pitfall is re-found from how
a filing reform changes who applies.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task163.json`, architecture v1. `guard.py check` WARN (answered below).
2. Pairing: Economics & Econometrics (client domain) / `forecasting-forecast-evaluation` / Forecasting & Predictive
   Modeling. The deciding analysis is a policy effect on business formation (the employer yield of the applications a
   filing reform added, identified by a difference-in-differences across states) feeding a formation forecast. The
   domains README files a platform's own funnel under Product Analytics; that rule would bind if the decisive step were
   the company's conversion of its own leads. It is not: the company's share is a filed multiplier and the decisive
   quantity is the market's formation yield, an economist's quantity.
3. Niche: a Columbus payroll services company sizing the first-time-employer line of its 2027 sales plan across twelve
   Great Lakes, Ohio Valley and Mid-Atlantic states, when Ohio, Pennsylvania and Michigan (its three largest markets)
   put the IRS employer identification number application inside the state's online business formation filing in 2024
   and retired their older filing routes in 2025 and 2026.
4. Call and shape: Kilbourne's new first-time-employer customers in the twelve states in 2027, to the nearest 100
   (`quantity_figure`, count, question form how-many). Shape `other`: the call with its critical components (the
   three reform states' 2027 formations and the added applications' yield) and decoupled ask tables in the workbook,
   with a one-page note; criteria counted in `## Ask sheet`.
5. Mechanism keys: gap population (which applications go on to employ: the ordinary filer or the filer a cheaper
   filing added) with time (the closed cohorts are a statement about a window whose added share was far smaller than
   the plan's); decisive generator G6 (the population of applications shifted under the formation rate), then G14 (the
   pooled or latest rate does not apply to this pool) and G13 (the plan window's added share against the closed
   window's); Gate G `forecasting`; strategy `causal_design` (stumping F9: a rate that depends on the pool, read off
   the comparison the design implies). `composition_mix` (F5) is the neighbouring key and is not used: no record classes
   an application as added, so the mix exists only through the comparison against untreated states.
6. Layer 2: `estimand_identification`, pattern `own:marginal-applicant-employer-yield-read-against-untreated-states`.
   Library neighbours: economics-econometrics/causal-identification-did-iv-rd-synthetic-control/1 (staggered adoption
   read against not-yet and never-treated units); this build reads three staggered reforms against nine untreated
   states, but the estimand of the comparison is a yield per added application, carried into a forecast, not an ATT.
7. Furniture: forum `executive_team` (the CFO signs the 2027 operating plan on Friday); forcing event
   `budget_or_appropriation` (the annual operating plan and the sales capacity it funds); organisation family
   `professional_services` (Kilbourne is a payroll services company, NAICS 541214, which runs clients' payroll and files
   their payroll taxes on its own platform; `software_or_platform` was the seed's wording and was banned by task162 at the
   check, and the industry classification's own home for a payroll services firm is professional services); role
   family `finance_controller` (the revenue planning lead in FP&A); context artifact `filed_standard` (the 2027 plan's
   market sizing standard); calibration `censored_or_lagged_release` (the formation statistics publish a cohort's
   formations only once four or eight quarters have closed).
8. Spine: the payroll platform's new-account onboarding export (one row per account opened, January 2022 to December
   2025, about 30,000 rows, two layouts across the 2024 account-system migration), constructed in the layout of a payroll
   platform's onboarding export. The formation statistics file is the main call's evidence; the spine carries the asks.
9. Deliverables: `first_time_employer_plan_2027.xlsx` (the call, its components and the ask tables) and
   `first_time_employer_plan_2027_note.docx` (a one-page note with the chart of the reform states against the nine);
   the format set xlsx and docx is in none of the last three builds.
10. People, drawn with `guard.py names --geo "United States" --seed 163`: Dominique Thomas (revenue planning lead,
    FP&A, the requester, in no file the prompt names and not in the prompt), Charles Fernandez (market research analyst,
    keeps the research team's change log and the statistics extract), Cheryl Mitchell (sales operations, the onboarding
    export and the 2025 share table), Calvin Garrett (CFO, the plan sign-off). Invented name: Kilbourne Payroll (checked
    against real payroll firms: no match); further names are checked the same way when the pack is cut.

**Data-native sentence.** The three reform states' online formation filings now file the IRS application for an
employer identification number for any new business that ticks the box, so the business applications those states
report rose first as filers took up the new system and again as each retired its older route, while the nine other
states rose about a fifth on a wave every state shared; an application the reform added looks like any other in every
field the statistics publish (it is as often high-propensity, as often with planned wages), but its owner was forming an
LLC anyway and seldom hires, so the formations the closed cohorts show are a blend whose added share was a fraction of
what the plan's twelve months hold, and only the reform states set against the nine before and after separate the blend.

**Guard and similarity.** `guard.py check` WARN at the draw. The ban window held task182, task164 and task162. WARNs
answered: `repeat.gate_g` (forecasting, task162) is the honest key for a call whose difficulty is a forward quantity;
`repeat.decision` (quantity_figure, task162) and `repeat.question_form` (how-many, task164 and task162) are what a count
of customers is. NOTE `test.same_driver_older` (gap population, G6, Gate G forecasting) is differentiated on the card
against task124, task132, task144 and task465. Nearest driver 0.06 (task136).

**Abstraction test.** Stripped of nouns: a cut in the cost of entering a leading count draws in marginal entrants who
seldom go on to the outcome; a common rise over the same months is ordinary; only treated regions against untreated
ones, before and after, separate the two, and the added entrants' yield, carried per added entrant onto a forward period
holding more of them, sets the outcome. The nearest by mechanism, read for latent structure:
- task136 nets out enrolments a scheduled campaign drew from households about to install anyway, sites read against
  sites whose campaign had not yet run. Here nothing is pulled forward: the reform adds filers who mostly never hire,
  the outcome is a lagged conversion of a leading count, and the decisive quantity is the conversion yield of the added
  filers carried onto a forward volume whose added share has more than doubled.
- task137 rebuilds, unit by unit, which deposits a temporary premium won, from each unit's price against its entry
  cohort's floor. Here no unit can be classed; the two kinds exist only as an aggregate counterfactual.
- task95 recovers a fixed class weight by differencing two dated events on each unit across two registers. Here there
  is no unit-level class and the added share is a gap between states, not a register field.
- task157 sizes a returning cohort from its own early arrivals at a timing ratio earlier cohorts kept. Here no cohort is
  completed from its leading edge; closed cohorts are read as they are.
- task446 backs a moved base rate out of a screen's flagged share through stable error rates. Here the propensity flag
  misclassifies the added filers and the yield comes from the reform's natural experiment.
None shares the latent structure, the default path and the correction.

**Sources, one line each.**
- Seed FC34 header and Situation (`status.py task163`): the world, the twelve states, the 2027 first-time-employer plan,
  the statistics with high-propensity splits, the rise in applications, the three states' filing changes; nothing else
  of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: the formation and conversion ground on file is a cohort sized from its
  own leading edge (task157), a conversion hazard by time since entry after a surge (task134 round 1), a development
  speed that changed mid-period (task451), a screen's yield moving with the base rate (task446) and an intervention's
  additionality against not-yet-treated sites (task136); none reads a reform-added leading count's conversion yield
  against untreated regions.
- `stumping/references/client/layer2-rigor-patterns.md`, economics-econometrics causal-identification pattern 1
  (staggered adoption against not-yet and never-treated units): the comparison here is used for a yield per added
  application inside a forecast, not for an average treatment effect.
- `stumping/references/strategies.md` F9 (causal design: a rate that depends on the pool) and F5 (composition, the
  neighbouring key): the property that splits the pool is named by no record and rebuilt only through the comparison.
- `two-layer-task-design.md`: the client's example of comparing against the right group in a staggered rollout, not a
  simple before and after, and of a forecast validated on data it was not built on (the rival rates fail the closed
  post-reform cohorts month by month).
- The economics of entry costs: one-stop registration reforms raise registrations mostly through marginal entrants who
  rarely grow or hire (Branstetter et al. on Portugal's "On the Spot Firm"; Kaplan, Piedra and Seira on Mexico's SARE),
  which is the behaviour the generator gives the added filers.

## Default path

1. Read the 2027 plan's market sizing standard: the plan sizes each state's first-time employers as the business
   formations within four quarters that a year of applications at the level of the twelve months to September 2026
   will produce, times the state's 2025 share in the plan workbook.
2. Stack the Census business formation statistics by state (seasonally unadjusted rows), keeping only the cohorts whose
   formations within four quarters have closed (applications to June 2025).
3. Take each state's formation rate as its formations within four quarters per application over its latest four closed
   quarters (July 2024 to June 2025 applications).
4. Multiply by each state's applications in the twelve months to September 2026 and by its 2025 share; add the twelve.

Ends on: 2,600 (prototype figure; the built figure replaces it)
Golden: 2,250 (prototype figure; the built figure replaces it)

## Stump sentence

Carrying each state's latest closed formation rate per application onto the twelve months of applications to
September 2026 at the plan's 2025 shares files 2,600; the step that lands it there is treating the reform states'
latest closed rate as theirs, when it blends ordinary applications with applications the reform added, whose share of
the reform states' applications has more than doubled since the closed cohorts, so only the added applications' own
yield, read against the nine other states before and after and carried per added application, files 2,250.

## Three rules

Task type: forecasting-forecast-evaluation (Economics & Econometrics), which serves Forecasting & Predictive Modeling in the taxonomy; the setting is a payroll company's 2027 plan sized on employer business formations from the Census business formation statistics.
Domain test: the quantity that decides the call is the employer yield of the business applications a filing reform added, estimated the way econometricians estimate a policy's effect on business formation (a difference-in-differences of applications and of closed formation cohorts against the states the reform did not reach, before and after) and carried into the formation forecast.
Swap: "how many new depositors will a credit union sign in 2027 after three branches added online account opening" keeps a funnel and a surge but loses the federal application register whose filings become employers only after a four-quarter window, the high-propensity classification the marginal filer inflates, and the filing cost whose cut changes who applies, so nothing it holds is a business formation the field would forecast.
Layer 1: the statistics' release layout (state by month, seasonally adjusted and unadjusted rows flagged, formations published only once a cohort's window closes), a revised release overlapping the research team's earlier extract, FIPS codes against postal abbreviations, each state's registration report in its own layout, the onboarding export's two layouts across the 2024 migration with UTC timestamps, employer identification numbers with and without hyphens and with leading zeros dropped, the fiscal year from February, test and void payroll runs; each is how those systems write their files and none carries the call.
Layer 2: estimand_identification, the right counterfactual: the reform states' applications split into the ordinary and the added only against the nine untreated states before and after, and the added applications' yield read from the closed post-reform cohorts on that split, not the average, the propensity split or each state's latest blended rate.
Decisive step: identify the applications each reform added as the reform states' applications less their counterfactual from the nine other states' path, estimate the added applications' formation yield from the closed post-reform cohorts against that counterfactual, and carry it per added application onto the plan's twelve months, the common wave at the ordinary rate.
Not semantics: every field is read correctly on the default path (applications, high-propensity and planned-wage counts, formations within four quarters, the cohorts not yet closed, the plan's estimand and shares); no field marks an added application, and reading the statistics perfectly still leaves the analyst choosing a rate for applications whose mix the closed cohorts do not share.
Not rule application: the standard files the estimand (whose formations, which window, which volume, which share) and no rule says how to turn a reform state's applications into formations; executing every filed sentence on the clean data files the default figure.
Analyst test: a strong analyst who stacks the statistics by state, keeps only closed cohorts, reads the standard correctly and carries each state's latest closed formation rate per application onto the twelve months to September 2026 at the plan's shares files 2,600; only splitting the reform states' applications against the nine other states and carrying the added applications' own yield files 2,250 (executed in checks.py on the generator's clean truth).
Estimand: the 2027 plan's market sizing standard (Dominique Thomas, revenue planning) files the population (first-time employers in the twelve core states), the outcome (business formations within four quarters, the Census measure), the volume (a year of applications at the level of the twelve months to September 2026), the unit (Kilbourne's new first-time-employer customers, each state's formations times its 2025 share in the plan workbook) and the rounding (nearest 100); there is no comparison.
No decoy: no memo, draft, forecast, prior plan figure or stakeholder estimate states a 2027 figure or argues a method; the change log states each system's go-live and the date each older route closed and nothing about formations; the prior plan workbook carries 2026's plan figures, which rank nothing and argue nothing.
No certified replay: no published or certified figure is reproduced to recover a method; the closed formation cohorts are the outcome data every method reads alike, and the out-of-sample check (each rival rate on the later closed post-reform months) is the analyst's own validation.
Lesson: a model learns that a leading indicator inflated by a cut in filing cost carries marginal filers whose conversion is a fraction of the average, that the fraction has to be identified against units the cut did not reach rather than assumed (zero or full) or read from a blended latest rate, and that it must be carried per added unit onto a forward volume whose added share differs; no build on file reads a reform-added leading count's conversion yield against untreated regions.

## Tried and rejected

- Completing the surge cohorts' formations from their own early formations at the closed cohorts' development pattern (a chain ladder on the formation triangle): rejected at the draw, the same latent structure as task157 (a cohort's size from its leading edge at a timing ratio earlier cohorts kept).
- A first-payroll hazard by months since registration applied to a pool the surge filled: rejected at the draw, task134 round 1's driver.
- A formation lag that lengthened after the reforms, so the closed cohorts' four-quarter rate reads a delay as a loss: rejected at the draw, the development-speed change task451 spent.
- The high-propensity flag as a screen whose yield moves with the base rate of genuine employers: rejected at the draw, task446's driver.
- A one-time formalisation wave at each launch that will not recur in 2027: rejected at the draw, a dated cause whose effect steps a series is found by an event study.
- A timely calendar formation series in the pack (state new-employer registrations or the company's 2026 first-timers): rejected at the draw, carrying the latest twelve months forward lands within a bin of the golden.
- Two more states opening the integrated filing inside 2027 as the forward change: rejected at the draw, the formation effect of a launch inside its first year is under a bin of the call.
