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
   put the IRS employer identification number application inside the state's online business formation filing in 2023
   and retired their older filing routes between January and March 2026.
4. Call and shape: Kilbourne's new first-time-employer customers in the twelve states in 2027, to the nearest 100
   (`quantity_figure`, count, question form how-many). Shape `other`: the call with four critical components (the
   added applications in the twelve months, their yield against the ordinary rate, the formations the twelve months
   will produce, the three states' part of the line) and two decoupled ask tables in the workbook (each sales
   territory's 2024 first-time employers: signed, still with us in the fourth quarter of 2025, gross wages in the
   first quarter on payroll and in 2024; the 2024 first-time employers by signup channel), with a one-page note
   charting the territories; 1 call, 4 components, 29 ask figures, 4 chart criteria and 2 files make 40 criteria.
5. Mechanism keys: gap population (which applications go on to employ: the ordinary filer or the filer a cheaper
   filing added) with time (the closed cohorts are a statement about a window whose added share was much smaller than
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
8. Spine: the current account system's onboarding export (`onboarding_accounts_2022-2025.csv`, one row per account
   with a first pay date from January 2022 to December 2025, 37,103 rows, two layouts across the June 2024 migration),
   with the quarterly wage files of both systems (178,829 legacy rows, 167,168 current rows). The formation statistics
   pull (applications January 2021 to September 2026) is the main call's evidence; the spine and its companions carry
   the asks. 16 files in four formats (JSON, CSV, XLSX, DOCX); distractors `bfs_monthly_states_2026-04-15.csv` (the
   April release) and `nonemployer_statistics_2023_states.csv`, named in `metadata.json` only.
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
report rose about a quarter while filers could still use the older routes and by about two thirds once each state
retired them (January to March 2026), while every state, the nine others included, rose about a tenth into the twelve
months on a common rise from early 2026 that nothing in the record explains; an application the reform added looks like
any other in every field the statistics publish (as often high-propensity, as often with planned wages), but its owner
was forming an LLC anyway and seldom hires, so the formations the closed cohorts show are a blend whose added share
(about a fifth) is a little over half of what the plan's twelve months hold (about a third), and only the reform states
set against the nine before and after separate the blend.

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
  filers carried onto a forward volume whose added share has nearly doubled.
- task137 rebuilds, unit by unit, which deposits a temporary premium won, from each unit's price against its entry
  cohort's floor. Here no unit can be classed; the two kinds exist only as an aggregate counterfactual.
- task95 recovers a fixed class weight by differencing two dated events on each unit across two registers. Here there
  is no unit-level class and the added share is a gap between states, not a register field.
- task157 sizes a returning cohort from its own early arrivals at a timing ratio earlier cohorts kept. Here no cohort is
  completed from its leading edge; closed cohorts are read as they are.
- task446 backs a moved base rate out of a screen's flagged share through stable error rates. Here the propensity flag
  misclassifies the added filers and the yield comes from the reform's natural experiment.
None shares the latent structure, the default path and the correction.

**WHAT screen (stumping 1.2).** The decisive step settles none of the estimand's five parts, each filed by the
standard: the population (the twelve core states' business applications in the twelve months to September 2026, in
the release's unadjusted counts), the outcome (business formations within four quarters, October release), the window
(those twelve months), the unit (Kilbourne's first-time employers, each state's formations times its 2025 share) and
the comparison (none: the line compares nothing). The nine states enter only as the identification of the added
applications' yield, which is HOW the filed quantity is estimated; every identification the data admits files 2,500
(544 constructions, the comparison's regression forms among them), and the data's own structure (the early 2026 rise
every state shared, after every go-live) rules out the reform states' own before-and-after level.

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
  simple before and after, and of a forecast validated on data it was not built on (the back-test across the go-live
  change of mix).
- The economics of entry costs: one-stop registration reforms raise registrations mostly through marginal entrants who
  rarely grow or hire (Branstetter et al. on Portugal's "On the Spot Firm"; Kaplan, Piedra and Seira on Mexico's SARE),
  which is the behaviour the generator gives the added filers.

## Default path

1. Read the 2027 sizing standard: each state's line is its 2025 share in the plan workbook times the business
   formations within four quarters that a year of applications at the level of the twelve months to September 2026, in
   the release's unadjusted counts, will produce; the twelve states add up, to the nearest 100.
2. Stack the October release's state rows (unadjusted), keeping only the cohorts whose formations within four quarters
   have closed (applications to June 2025).
3. Take each state's formation rate as its formations within four quarters per application over its latest four closed
   quarters (July 2024 to June 2025 applications, the share tab's own base window).
4. Multiply by each state's applications in the twelve months to September 2026 and by its 2025 share; add the twelve.

Ends on: 2,800 (2,769.0 unrounded)
Golden: 2,500 (2,499.6 unrounded)

## Stump sentence

Carrying each state's latest closed formation rate per application onto the twelve months of applications to September
2026 at the plan's 2025 shares files 2,800; the step that lands it there is treating Ohio's, Pennsylvania's and
Michigan's latest closed rate as theirs, when it blends ordinary applications with applications the integrated filing
added, which were about a fifth of the closed cohorts and are about a third of the twelve months, so only the added
applications' own yield, read against the nine other states before and after go-live and carried per added
application, files 2,500.

## Three rules

Task type: forecasting-forecast-evaluation (Economics & Econometrics), which serves Forecasting & Predictive Modeling in the taxonomy; the setting is a payroll company's 2027 plan sized on employer business formations from the Census business formation statistics.
Domain test: the quantity that decides the call is the employer yield of the business applications a filing reform added, estimated the way econometricians estimate a policy's effect on business formation (a difference-in-differences of applications and of closed formation cohorts against the states the reform did not reach, before and after) and carried into the formation forecast, then validated out of sample across the go-live change of mix.
Swap: "how many new depositors will a credit union sign in 2027 after three branches added online account opening" keeps a funnel and a surge but loses the federal application register whose filings become employers only after a four-quarter window, the high-propensity classification the marginal filer shares, and the filing cost whose cut changes who applies, so nothing it holds is a business formation the field would forecast.
Layer 1: the Census API pull in its long layout with FIPS codes and adjusted and unadjusted rows from January 2021, the April download in the wide bfs_monthly layout with postal codes from January 2022 and preliminary latest months, formations published only for closed cohorts (the statistics' own lag); the onboarding export's two layouts across the June 2024 migration (legacy client-since stamps in Eastern month/day/year text and upper-case names against UTC ISO stamps), EINs hyphenated, plain and with the leading zero lost; a migrated account's first_pay_date carrying its legacy client-since date, and clients the legacy system re-opened under a corrected EIN; legacy quarterly wages in cents by pay group with a company-level group, current wages in dollars with no state; the crosswalk join, state registrations keyed by account, the successor register keyed by EIN; product changes, relocations, cancellations and returns; every item is how those systems write their files and none carries the call.
Layer 2: estimand_identification, the right counterfactual: the reform states' applications split into the ordinary and the added only against the nine untreated states before and after, and the added applications' yield read from the closed post-go-live cohorts on that split, not the reform states' latest blended rate, their own before-and-after level, a propensity or planned-wage split, a line through the closed formations or the filing's effect carried as a level; a regression of formations on applications with state and month effects across the twelve states reads the same comparison in regression form and lands with it.
Decisive step: identify the applications each integrated filing added as the reform state's applications less its counterfactual from the nine other states' path, estimate the added applications' formation yield from the closed post-go-live cohorts against that counterfactual, and carry it per added application onto the twelve months, whose added share is nearly twice the closed cohorts', with the early 2026 rise every state shared at the ordinary rate.
Not semantics: every field is read correctly on the default path (applications, high-propensity and planned-wage counts, formations within four quarters, which cohorts have closed, the standard's estimand, the share tab); no field marks an added application, and reading the statistics perfectly still leaves the analyst choosing a rate for applications whose mix the closed cohorts do not share.
Not rule application: the standard files the estimand (whose formations, from which year of applications in which counts, at which share, rounded how) and no filed sentence says how to turn a state's applications into formations; executing every filed rule on the clean data files 2,800 (asserted in checks.py, R3a).
Analyst test: a strong analyst who stacks the statistics by state, keeps only closed cohorts, reads the standard correctly and carries each state's latest closed formation rate per application onto the twelve months to September 2026 at the plan's shares files 2,800; only splitting the reform states' applications against the nine other states and carrying the added applications' own yield files 2,500 (executed in checks.py on the generator's clean truth).
Estimand: the 2027 sizing standard (Dominique Thomas, FP&A, plan_2027_sizing_standard.docx) files the population (the twelve core states, named), the outcome (business formations within four quarters, the Census measure, October release), the volume (a year of business applications at the level of the twelve months to September 2026 in the release's unadjusted counts, whose formations are not yet observed), the unit (Kilbourne's first-time employers, each state's formations times its 2025 share in the plan workbook) and the rounding (the twelve states added, to the nearest 100); there is no comparison in the estimand.
No decoy: no memo, draft, forecast, prior plan figure or stakeholder estimate states a 2027 figure or argues a method; the change log states what each state's system does and when, never what it does to formations; the share tab is sales operations' 2025 count over the release's own base and ties under every reading.
No certified replay: no published or certified figure is reproduced to recover a method; the closed formation cohorts are the outcome data every method reads alike, and the back-test across the go-live change of mix (the split fitted on the cohorts from a year after each go-live to June 2025 predicting each state's first year after go-live within 0.5 per cent, the rate of the twelve months before go-live missing by 14.6) is the analyst's own validation.
Lesson: a model learns that a leading indicator inflated by a cut in filing cost carries marginal filers whose conversion is a fraction of the average, that the fraction has to be identified against units the cut did not reach rather than assumed (zero or full), read from a blended latest rate, extrapolated from the closed outcomes or measured as a level, and that it must be carried per added unit onto a forward volume whose added share differs; no build on file reads a reform-added leading count's conversion yield against untreated regions.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 1: the latest closed quarter's rate, the rate having fallen | no | no | yes, recency | no | no | yes, one ratio per state | readable |
| Rung 2: the split before and after against each reform state's own pre-go-live level | the log's go-live dates invite a before-and-after | no | yes, the event study | no | no | no | readable |
| Rung 3 (decisive): the split against the nine states' path, the added applications' yield from the closed cohorts since go-live, carried per added application onto the twelve months | no sentence names a comparison, a yield or a split | no column marks an added application; the high-propensity, planned-wage and corporate flags carry them at the ordinary rates | no: the reflex comparison measures the filing's effect on formations as a monthly level and carries the level (2,400, 1.42 bins off) | no control scores a split; the closed cohorts are counts every method reads alike | nothing to find | no: a counterfactual, a ratio of excess formations, then a carry by volume | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | applications at the level of the twelve months | the unadjusted twelve-month total | the seasonally adjusted total | 2,500 (2,495.0) | the standard: "in the release's unadjusted counts"; same call |
| SF2 | the 2025 share | the tab's stored ratio | the displayed two-decimal percentage | 2,500 (2,500.4) | same call |
| SF3 | business formations within four quarters | BF_BF4Q | BF_BF8Q, formations within eight quarters | not the measure | the standard: "business formations within four quarters" |
| SF4 | the twelve core states | the twelve the standard names | other geographies in a release | not in the pull | the standard names them; the pull holds exactly those twelve |
| SF5 | the release | the October 2026 release | the April 2026 download | cannot form the twelve months (applications end March 2026) | the standard: "The plan uses the October release" |
| SF6 | a year at the level of the twelve months to September 2026 | the twelve-month total | the latest quarter times four | 2,800 (2,753) | the standard: "at the level of the twelve months to September 2026" |
| SF7 | rounding | the twelve states added, then the nearest 100 | each state rounded first | not the line | the standard: "The twelve states add up to the line, which goes into the plan to the nearest 100"; 2,499.6 sits 0.50 of a bin from an edge |
| SF8 | the formations a year of applications will produce | formations within four quarters of those applications | first payrolls falling in calendar 2027 | not the measure | the standard's sizing sentence names the applications' formations |
| SF9 | a first-time employer signed in 2024 | a business whose first payroll ever ran with us, in 2024 | an account flagged first-time | the flag counts 2,900 | the counting notes: "first payroll ever runs with us"; "re-forms as a new entity and carries on, ... is the same business" |
| SF10 | the state it counts in | the state it first employed in (earliest registration) | the address state at the extract | moves movers | the counting notes: "in the state it first employed in" |
| SF11 | still with us in the fourth quarter of 2025 | wages we paid with a pay date in the quarter, on any of its accounts | the first account's own fourth-quarter row | misses returners and successors | the counting notes' still-with-us sentence |
| SF12 | the first quarter on payroll | the calendar quarter of its first payroll with us | the first full quarter | other quarters | the counting notes: "the calendar quarter of its first payroll with us" |
| SF13 | gross wages we ran | gross wages we ran on our payroll | wages on the returns, tax filing only included | adds filed wages | the counting notes: "the gross wages we ran on our payroll" |
| SF14 | a legacy client quarter's wages | group 00, the client's total | every group summed | doubles two-group clients | the identity 00 = 01 + 02 in every two-group client quarter, to the cent (asserted, 37,739 client quarters) |
| SF15 | a migrated account's signup channel | the channel of its legacy source code | the export's channel | moves four channels | the field guide: the load carried the legacy source as it mapped it; the code list; the export disagrees with the code only where the load used the default (asserted, 5,376 accounts) |
| SF16 | the window the 2025 share applies to | the share times the formations the twelve months' applications will produce | the share on its own base window (July 2024 to June 2025 applications) | 2,200 (2,155, the 2025 count back) | the standard: the share is the 2025 count "over the state's business formations within four quarters from the applications of July 2024 to June 2025", and the line is that share times the formations a year of applications "at the level of the twelve months to September 2026" will produce |
| SF17 | a business bought by a new owner who carries it on | the same business as the seller, its accounts joined through the register | a new business | counts acquired businesses as first-time | the counting notes: "is bought by a new owner who carries it on, is the same business" |
| SF18 | first-time status | the state's liability record: no liability date before the quarter of the first payroll with us | the onboarding flag | the flag counts 2,900 | the counting notes: "Whether a business has paid wages before is a matter of the state's record, not of its onboarding answer" |
| SF19 | a quarter on tax filing only | not a quarter we paid: neither still with us nor wages | a quarter with wages on the returns | keeps tax-only clients still and adds their filed wages | the counting notes: "A quarter an account spent on tax filing only does not count" and "a quarter on tax filing only adds none" |
| SF20 | a business's channel | its first account's; a migrated account's from its legacy source code through the code list | the export's channel on any account | moves four channels | the field guide: "the legacy source code in the crosswalk is the record of how the client came to us"; the counting notes: "the channel of its first account" |
| SF21 | the year and quarter of the first payroll with us | the first quarter we ran wages, from the wage files | a migrated account's first_pay_date (its legacy client-since date) | January starters in 2023, first quarters a quarter early | the counting notes count "the year its first payroll with us ran"; wherever the field's quarter differs from the first quarter with wages it holds no wages (asserted, 4,885 migrated accounts; no current-system account differs) |
| SF22 | a client re-opened under its corrected EIN | one business with its first account | two businesses | double counts, loses the still and the later wages | the counting notes: "A business is the employer, whatever its account or EIN"; the EIN pairs one adjacent swap apart on accounts with the same names, industry and entity are exactly the 803 clients cancelled and re-opened the next day (asserted) |

## Ladder

| Rung | Construction | Figure | Rounded | Dies to |
|---|---|---|---|---|
| 0 (default path) | each state's latest four closed quarters' rate carried onto the twelve months | 2,769.0 | 2,800 | the added share of the reform states' applications: about a fifth in the latest four closed quarters (Ohio 0.19, Pennsylvania 0.20, Michigan 0.19), about a third in the twelve months (0.35, 0.35, 0.31) |
| 1 | the latest closed quarter's rate, April to June 2025 | 2,763.3 | 2,800 | the same: the latest closed quarter still holds the voluntary phase |
| 2 | the split against each reform state's own pre-go-live level, the added yield from the closed cohorts | 2,436.9 | 2,400 | every state's ordinary applications rose about a tenth into the twelve months on the early 2026 rise with no filing change (the nine 9.9 per cent), so the own level counts the common rise as added applications and prices it at the added yield; 0.63 bins below the golden, it rounds to the neighbouring hundred |
| 3 (decisive) | the split against the nine states' path, the added yield pooled over the closed cohorts since go-live (0.260 of the ordinary rate), carried per added application | 2,499.6 | 2,500 | the golden |

Routes inside a bin of the golden (checks.py `NEAR_ROUTES`, each with its reason; every one rounds to 2,400 and none to
the golden, asserted, and no other route sits inside a bin):
- the own before-and-after (rung 2), 2,436.9, 0.63 bins below: it counts the early 2026 rise every state shared as
  added applications and prices it at the added yield;
- each reform state's formations regressed on its applications with calendar-month terms over every closed cohort,
  2,440.0, 0.60 bins below: one slope through the months before and after go-live mixes the ordinary rate with the
  added yield, so the twelve months' ordinary rise is priced below the ordinary rate;
- 2025's first-time employers grown by the nine states' applications from January to September 2025, 2,429.2, 0.70
  bins below: the nine states' growth leaves out the added applications that do form (the same carry over the six other
  windows sits 1.31 to 1.39 bins below).

Single-error cells off the ladder, each a full bin or more from the golden (checks.py RIVALS): the filing's effect
carried as a level 2,357.5 (2,400, 1.42 bins); the added applications never forming 2,265.7 (2,300); the pre-go-live rate
on every application 3,164.6 (3,200); every closed cohort's rate 2,956.7 (3,000); formations per high-propensity
application over the latest four closed quarters 2,771.7 (2,800) and over every closed cohort 2,956.1 (3,000); per
planned-wage application 2,775.1 (2,800) and 2,957.5 (3,000); each reform state's formations regressed on its
applications without month terms 2,619.9 (2,600, the nearest rival at 1.20 bins); 2025's first-time employers carried
2,155.0 (2,200); 2025 grown with the twelve states' applications from calendar 2025 2,621.6 (2,600), from the prior
twelve months 2,622.7 (2,600), from the base window 2,621.0 (2,600), year to date 2,761.7 (2,800), over six quarters
adjusted 2,889.2 (2,900); each state's closed formations on a straight line from July 2023 2,200.9 (2,200). Each
correction on the ladder moves the figure, and the decisive move is the only one that lands. Worth on the graded
figure: rung 0 to 3 is 269 (2.7 bins); the decisive step alone, applied to the default path, moves 2,800 to 2,500 (R3b).

Bypass battery (checks.py BYPASS, 47 routes that size the line without splitting the applications; every one but the
January-to-September nine-state carry above is a full bin or more off): straight lines through the closed formations,
monthly, adjusted or not, linear or log, from seven start months between January 2021 and July 2024, 1,991.6 to 2,290.4
(2.09 bins or more); annual totals on a line by calendar, fiscal February, fiscal October and July years, 2,262.2 to
2,354.3 (1.45 or more); the rate per application on a line from January 2023, July 2023, January 2024 or July 2024,
2,620.6 to 2,706.3 (1.21 or more); 2025's first-time employers grown by the nine or the twelve states' formation growth,
2,176.7 and 2,153.3; 2025 grown by the nine states' applications over seven windows, 2,360.4 to 2,429.2; by the twelve
states' applications, 2,618.6 to 2,761.7 (1.19 or more); each state's 2025 count grown by its own applications,
2,765.9. They miss on their own merits: the closed cohorts end in June 2025, before the early 2026 rise and before any
older route closed, so a line through their formations or rates prices neither; the nine states' growth leaves out the
added applications that do form, and the twelve states' growth prices them at the ordinary rate.

Construction family (544 constructions: six counterfactuals, every one resting on months before the state's go-live;
three ordinary-rate windows; six added-yield estimators; the nine states' rate over every closed cohort or the latest
four quarters; unadjusted or adjusted volume; the six controls without Indiana, Kentucky and Tennessee; and four
regression forms of the comparison, formations on applications across the twelve states with state and month-of-sample
effects 2,506.3, with state and calendar-month effects 2,506.0, the same in logs 2,480.6, and each reform state's
formations on its applications from go-live with month terms 2,502.1): 2,477.2 to 2,516.2, every one 2,500, the nearest
0.272 of a bin from an edge. The regressions land because state effects learn the slope from the voluntary step at
go-live, the reform states' own variation read against the other states' months, and the full take-up in the twelve
months is the same filers scaled up: the comparison in regression form. The bootstrap (300 Poisson redraws of the
release's formations and of the applications before the twelve months, which are the estimand's own volume and stay as
filed) puts the line's 95 per cent interval at 2,469.0 to 2,530.2, inside 2,450 to 2,550 with 19.0 to spare (sd 15.3);
one sigma with every count redrawn is 15.5, and the family's ends plus or minus one sigma stay 2,500. The added
applications' relative yield rests on 0.260 with a sigma of 0.023. Out of sample: the formations the twelve months'
applications go on to produce price at 2,470.4 in the generator's truth; the golden is 29 over it and the default path
299. Back-test across the go-live change of mix: fitted on the cohorts from a year after each go-live to June 2025
(relative yield 0.251), the split predicts each state's first year after go-live within 0.5 per cent; the rate of the
twelve months before go-live, the default path's move at that change, misses by 14.6 per cent.

P(one top response lands the call): about 0.16, counting the regressions as landings. The decisive split carried per
added application is about 0.10 of strong responses (it needs the comparison against the nine and the carry together);
a panel regression of formations on applications with state and month effects across the twelve states is about 0.05 (a
strong model reaching for a regression on the release's own counts runs the comparison in regression form and lands);
the reform states' post-go-live regression with month terms about 0.01. Nothing else lands: the reflex comparison
carries a level (2,400), the own before-and-after and a regression through every closed month file 2,400, a zero yield
2,300, and no straight line, rate trend or growth carry reaches the bin (outside the three named routes the nearest is
1.19 bins off). P(both): about 0.04, above the 0.026 independence would give, since two top responses tend to take the
same route.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the twelve core states' applications in the twelve months to September 2026, in the release's unadjusted counts, whose formations are not yet observed | filed literally (the standard), C1 |
| 2 Unit of account | Kilbourne's first-time employers, each state's formations times its share | filed (the standard) |
| 3 Attribution window | formations belong to the application month (the statistics' cohort) | C1: every reading uses the release's cohorts |
| 4 As-of dating | the October 2026 release, pulled 14 October 2026; the share tab refreshed from it | filed (the standard, the workbook note) |
| 5 Version basis | October release, not April | filed (the standard); C1 for the months both hold (R2, 2,496.0) |
| 6 Denominator | a state's formation rate per application; the added yield over the added applications at the ordinary rate | C3: absolute and relative yields both in the family |
| 7 Weighting | the added yield pooled over the three states or per state | C3: pooled, per state and the four regression forms all 2,500 |
| 8 Window length | the ordinary rate's window (every month before go-live from January 2021, 2021 and 2022, the twelve months before go-live); the counterfactual's base (the same three, or the state's ratio to the nine) | C3: every window in the family, 2,500 |
| 9 Boundary inclusivity | Michigan's part-month go-live counted or left out | C1: 2,499.6 and 2,502.0 |
| 10 Rounding path | the twelve states added, then the nearest 100 | filed (the standard) |
| 11 Tie-break | none, a single figure | nothing to break |
| 12 Maturity and censoring | only cohorts whose four quarters have closed (to June 2025) | the field guide's release sentence; the release publishes nothing else |
| 13 Order of operations | share times formations per state, then added | commutes; C1 |
| 14 Row order | sums only | C1 |
| 15 Duplicate resolution | one row per series, adjustment, month and state | asserted unique; nothing to resolve |
| 16 Identity normalisation | FIPS codes to the twelve states | C1: the twelve codes, the standard's twelve names |
| 17 Netting against gross | counts, nothing to net | none |
| 18 Dimensional units | applications and formations as counts, adjusted or not | filed (unadjusted counts); C1: adjusted volume 2,495.0 |
| 19 Code and status semantics | data type codes and the adjustment flag | the field guide; never the stump |
| 20 Integerisation | none before the rounding | none |
| 21 Clause scope | "a year of applications at the level of the twelve months to September 2026" | filed scope (the standard) |
| 22 Forward window contents | the twelve months' applications are all observed; the older routes closed inside them (January to March 2026); the log files no further change to formation filings | shipped (the pull and the log) |

## Literal reader

Executed word for word, the standard asks for each state's 2025 share times the business formations within four
quarters that the twelve months of applications to September 2026, in the release's unadjusted counts, will produce,
added and rounded to the nearest 100; the pack holds those applications and the shares but no formations for those
cohorts, so every literal reading must forecast them; every reading of each term in the fork table gives 2,500 or
violates a quoted sentence, and the easy answer (2,800) comes from an easy method on the same literal estimand, not from
another reading.

## Oracles

- The share tab's formations base: it is the October release's own sum for July 2024 to June 2025 and ties under every
  handling; it confirms the share, not a forecast.
- The share tab's 2025 counts: they tie to the onboarding export read by the flag and read by the counting notes,
  because the 2025 first-time employers carry no ask device (asserted); they confirm nothing about the line.
- The closed formation cohorts: published counts every method reads alike; the back-test on them is the analyst's own.
- The April release: an earlier vintage from January 2022 with formations closed to December 2024 and no forecast;
  nothing ties to the golden.
- None ties only under the golden. On the ask side no control total ships for the territory or the channel table.

## Ask sheet

Asks (decoupled from the call: the 2024 first-time employers, a cohort and a year the call never reads; H18, the plan
line's case on retention, first-quarter value and where first-time employers come from):
- A, by sales territory: signed in 2024; still with us in the fourth quarter of 2025 (12 figures).
- B, by sales territory: gross wages we ran for them in their first quarter on payroll; in all of 2024 (12 figures,
  to the cent).
- C, by signup channel: the 2024 first-time employers (5 figures).
- The note's chart: each territory's signed against still with us (4 criteria, two of them structural).

Devices (no row in the call's population: the call reads the release, the share tab and the log, and the 2025 cohort
carries no device, asserted):
- A primary, D8 a date the load wrote for the event's date: the June 2024 migration loaded each legacy client's
  client-since date (the day its account opened, 5 to 37 days before its first payroll) into first_pay_date. The
  counting notes count the year and the quarter the first payroll with us ran, and only the wage files say when that
  was: 4,885 migrated accounts hold no wages in the field's quarter, and no current-system account differs. Trusting the
  field puts January 2024 starters into 2023 (12 to 54 a territory) and moves first quarters a quarter early. Silent:
  the field guide calls the field the first pay date on the account record, and nothing invites the cross-check.
- A and C second primary, D7 the true key elsewhere: the legacy system could not change an EIN, so a client whose first
  quarterly return came back rejected for a mistyped EIN was cancelled and opened again the next day under the corrected
  number (803 clients), with the same legal and trade names, industry and entity and the two EINs one adjacent swap
  apart. Where the state registered the corrected EIN afresh (a business first employing through us) the re-opened
  account looks like a new first-time employer; where the state already held the business under its correct EIN it
  keeps the old liability date, and the business's later quarters fall off its first account. Silent: no field links
  the two accounts, and the counting notes' "whatever its account or EIN" states the principle, not the link.
- B primary, D9 a rollup above its parts: a two-group legacy client's company-level group 00 holds the client's totals,
  so the plain sum of a client quarter's rows doubles its wages; found only by reconciling 00 against 01 and 02.
- Documented, filed at the determinism judge's request and executed by the cracker (the mirror's bar): first-time
  status from the state's liability record, not the onboarding flag, which successors and self-run businesses often
  answered yes on the older form (D2); a quarter on tax filing only is not one we paid, with its over-cleaning twin, accounts
  moved to tax filing only from 1 January 2026, which we still paid in the fourth quarter of 2025 (D5); a migrated
  account's channel from its legacy source code through the code list, where the load gave CPA, BP, TEL and APX the
  default web sign-up (D7); a business bought by a new owner who carries it on is the same business.
- Shared hazards, documented: successors through the payroll tax team's register (the counting notes' re-formed entity
  and new-owner rules), returning clients under the old EIN in three formats, the state first employed in against the
  address state, legacy cents, legacy numbers through the crosswalk, the migration quarter split across both wage files.

Spans: A reads the export, the crosswalk, both wage files (the first payroll), the registrations, the successor
register, the territory map, the counting notes and the field guide; B adds the legacy wages' pay groups (nine files,
fourteen columns); C reads the export, the crosswalk, the wage files, the registrations, the register, the field guide
and the counting notes.

| Ask figure | Golden | Cracker | Verdict |
|---|---|---|---|
| Indiana-Kentucky signed | 207 | 199 | miss |
| Indiana-Kentucky still | 158 | 150 | miss |
| Indiana-Kentucky first-quarter wages | 1,977,871.23 | 1,814,642.41 | miss |
| Indiana-Kentucky 2024 wages | 7,786,220.16 | 7,757,214.93 | miss |
| Michigan signed | 447 | 431 | miss |
| Michigan still | 351 | 335 | miss |
| Michigan first-quarter wages | 4,061,127.70 | 3,462,684.73 | miss |
| Michigan 2024 wages | 15,033,987.82 | 14,358,095.61 | miss |
| Ohio signed | 803 | 761 | miss |
| Ohio still | 659 | 628 | miss |
| Ohio first-quarter wages | 6,772,408.40 | 5,886,823.98 | miss |
| Ohio 2024 wages | 27,328,523.89 | 26,022,389.66 | miss |
| Pennsylvania signed | 478 | 449 | miss |
| Pennsylvania still | 391 | 365 | miss |
| Pennsylvania first-quarter wages | 4,247,739.25 | 3,284,545.81 | miss |
| Pennsylvania 2024 wages | 16,840,397.09 | 14,735,064.27 | miss |
| South and Plains signed | 126 | 115 | miss |
| South and Plains still | 98 | 88 | miss |
| South and Plains first-quarter wages | 1,039,154.06 | 861,504.03 | miss |
| South and Plains 2024 wages | 4,135,224.30 | 3,642,986.38 | miss |
| Upper Midwest signed | 129 | 117 | miss |
| Upper Midwest still | 104 | 92 | miss |
| Upper Midwest first-quarter wages | 1,183,846.12 | 823,727.19 | miss |
| Upper Midwest 2024 wages | 4,529,319.79 | 3,560,338.69 | miss |
| channel accountant referral | 582 | 543 | miss |
| channel bank partner | 271 | 260 | miss |
| channel outbound | 274 | 259 | miss |
| channel partner marketplace | 262 | 253 | miss |
| channel web sign-up | 801 | 757 | miss |

The cracker lands the call, reads the field guide and the counting notes and executes every rule they point at (EINs
normalised, returning clients, successors and new owners as one business through the register, first-time status from
the liability record, tax-filing-only quarters left out, a migrated account's channel from its legacy code, the earliest
registration's state, territories, cents, the crosswalk, both wage files summed by quarter); it trusts the account's
first pay date, an EIN as the mark of a separate business and every row of a legacy client quarter. The two silent
count devices pull the counts the same way (in every territory the January starters the field moves into 2023, 12 to
54, outnumber the accounts a re-key adds, 1 to 13; asserted), so no mishandling composes back. Single-device cracks:
the first payroll from the wage files 33.5 (two still figures land where no re-opened account moves them), the re-keyed
EINs joined 31.8, group 00 31.8. Two at once: the first payroll with the re-keyed EINs joined 47.7 (group 00 then moves
only the wages, so every count lands), the first payroll with group 00 34.3, the re-keyed EINs with group 00 31.8;
every device cracked at once 57.7, the genuinely unstumped response. Two responses that both land the call average 48.3 before any device is
cracked: each banks 45 on the call and the two structural chart criteria, which no device moves, so that pair is held
only by the ladder (P(both) about 0.04).

Pair ceiling: 31.8 for the cracker, 33.5 for the strongest single-device crack (both 40 or under)
Mirror leakage: 6.1
Measured by: generator/cracker.py on the cut pack (target/), re-run by checks.py on every build

## Leak sweep

`leak.py task163 --asof 2026-10-16`: REVIEW, no LEAK. Each REVIEW line and why it is harmless:
- The standard carries the golden figure 100: it is the filed rounding ("to the nearest 100"), stated once at authority.
- The standard carries most words of the committed call: it is where the first-time-employer line is defined; it
  states no figure for it and names no rate, ratio, window or method (verify.py asserts the sizing section is free of
  them).
- The standard carries ten stump-paragraph terms: they are the estimand's own nouns (applications, formations,
  months, release); none names the comparison, the yield or the split.
- The surface screen promotes task124, task132 and task144 on the shared card keys (gap population, pattern G6, Gate G
  forecasting), the same-driver signature the card's differentiation answers at the draw; heart WARN on the draw's
  three repeats (Gate G, decision, question form), answered in `## Draw`.

## Tried and rejected

- Completing the surge cohorts' formations from their own early formations at the closed cohorts' development pattern (a chain ladder on the formation triangle): rejected at the draw, the same latent structure as task157 (a cohort's size from its leading edge at a timing ratio earlier cohorts kept).
- A first-payroll hazard by months since registration applied to a pool the surge filled: rejected at the draw, task134 round 1's driver.
- A formation lag that lengthened after the reforms, so the closed cohorts' four-quarter rate reads a delay as a loss: rejected at the draw, the development-speed change task451 spent.
- The high-propensity flag as a screen whose yield moves with the base rate of genuine employers: rejected at the draw, task446's driver.
- A one-time formalisation wave at each launch that will not recur in 2027: rejected at the draw, a dated cause whose effect steps a series is found by an event study.
- A timely calendar formation series in the pack (state new-employer registrations or the company's 2026 first-timers): rejected at the draw, carrying the latest twelve months forward lands within a bin of the golden.
- Two more states opening the integrated filing inside 2027 as the forward change: rejected at the draw, the formation effect of a launch inside its first year is under a bin of the call.
- The round-1 world (go-lives in 2024, a common rise from mid-2023 to mid-2024, the line at 2,300): retired at stage 4 round 1, the formation-only routes (lines through the closed formations, annual totals, the rate per application from July 2023, 2025 grown by formation or application growth) landed on the golden, because the closed cohorts already carried the common rise at nearly the twelve months' slope.
- The audit's shared autumn 2025 rise (9 to 12 per cent) added to that world with its 2023 to 2024 rise kept: rejected, 12 to 22 of 62 bypass routes stayed within a bin (formation lines from 2023, the rate per application on a line, the nine states' application growth carried).
- The earlier common rise moved to calendar 2022 beside the autumn wave: rejected, the reform states' own pre-go-live level then held the rise, so the before-and-after split (0.15 bins) and a formations-on-applications regression with month terms (0.11 bins) landed within a bin.
- A larger added yield (0.30 of the ordinary rate) with go-lives from August 2023 and slow take-up: rejected, 21 of 62 routes within a bin (the formation lines and the before-and-after split within 0.12 bins), since a larger yield closes the gap between the blend and the split.
- A voluntary take-up of 0.35 to 0.50 before the older routes closed: rejected, the rate per application on a line from January 2023 lands within 0.3 bins (the voluntary plateau sets the closed rate's trend near the twelve months' mix).
- Go-lives from July 2023 to January 2024 at a low take-up (0.25), and go-lives from April 2023 on an extract from January 2022: rejected, the counterfactual rested on too few months before go-live and the bootstrap's 95 per cent interval spilled out of the bin (sigma 22 to 29); the extract from January 2021 and go-lives from January 2023 give 24 to 30 months before go-live.
- Counterfactual and ordinary-rate bases fixed at 2022 to 2023 for every state once go-lives moved into 2023: rejected, the base then held post-go-live months and widened the family past an edge; every base now ends the month before the state's own go-live.
- A per-state joint regression of formations on ordinary and added applications as a seventh estimator: dropped, the two move together inside a state after go-live, so its coefficients are not separately identified and its spread (2,506 to 2,545 in the sweep) is the collinearity, not a reading.
- Later retirements of the older routes (December 2025 to April 2026): rejected, at take-up 0.35 or more four to nine routes fell within a bin, and at 0.30 the nine states' application carry sat at 1.02 bins, too close to hold on another seed.
- Calibrating the company's size to the family's midpoint: rejected, the line sat low in its bin and the bootstrap interval's margin was 1.5; the rule now targets the line at the bin's centre (2,500.5), written before the outcome.
- A calibration stop within 1.5 of the target: rejected, one business added or dropped at the margin moves the line about 3.6, so the rescaling oscillated between 2,499.0 and 2,502.6 without settling; the stop is 2.0.
- EINs drawn at random per business: rejected, two businesses drew the same EIN and the share tab no longer tied to the export; EINs are issued unique.
- Added applications more than doubling the reform states' applications once the older routes closed (full take-up above one added application for every ordinary one, routes closing from October 2025): rejected at stage 4 round 2 on the judge's realism read, since a one-stop filing that more than doubles a state's business applications reads as engineered; full take-up now adds about seven for every ten ordinary applications, the routes close January to March 2026 and the added share of the twelve months is about a third.
- Added applications set apart from the ordinary on the published flags (lower high-propensity and planned-wage shares, so a flag route priced them): rejected at stage 4 round 2 as an engineered tell; the added applications carry the ordinary high-propensity and planned-wage shares, and the flag routes miss on their own (2,800 on the latest four closed quarters, 3,000 on every closed cohort).
- Pushing the two-way fixed-effects panel of formations on applications and the post-go-live regression with month terms a bin off the golden: rejected at stage 4 round 2 after about 45 harness worlds and four seeds, both land within 0.6 bins in every world because state effects learn the slope from the voluntary step at go-live; they read the comparison in regression form, so they sit in the construction family, asserted inside the golden's bin.
- An added share of 0.40 to 0.45 in the twelve months to clear the growth carries and the own before-and-after: rejected at stage 4 round 2, it needs full take-up above one added application per ordinary one (the doubling) or the older routes closing in autumn 2025, which drags the twelve-state carry back in; at a third the own before-and-after, the regression through every closed month and the nine-state January-to-September carry sit 0.6 to 0.7 bins off and round to 2,400.
- The liability record, tax filing only and the legacy code as the asks' silent primaries once the judge's pins filed them: rejected at stage 4 round 2, the pins hand all three to the cracker (its pair measured 48.5); the silent primaries are now the migration load's client-since date in first_pay_date, which only the wage files contradict, and the legacy re-key of a mistyped EIN.
- The legacy re-key with the state registering the corrected EIN afresh for any business: rejected at stage 4 round 2, a business that had employed before is on the state's books under its correct EIN, and re-registering it let the re-key add about as many accounts to a territory's 2024 count as the client-since date took out, so the cracker's Indiana-Kentucky count landed on the golden by offset (207 against 207); a fresh registration is now limited to businesses first employing through us, and the two devices pull every territory's count the same way.
- A third silent count device so that a response cracking both count primaries stays under 45 (47.7 measured, group 00 moving only the wages): not built at stage 4 round 2, since no further mess the company's systems write moves the counts apart from the first payroll and the business's identity, and a contrived one would read as planted; the pair table records it beside the both-on-call floor of 48.3.
