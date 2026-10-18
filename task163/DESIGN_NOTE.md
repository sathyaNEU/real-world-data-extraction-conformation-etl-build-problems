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
   (`quantity_figure`, count, question form how-many). Shape `other`: the call with four critical components (the
   added applications in the twelve months, their yield against the ordinary rate, the formations the twelve months
   will produce, the three states' part of the line) and two decoupled ask tables in the workbook (each sales
   territory's 2024 first-time employers: signed, still with us in the fourth quarter of 2025, gross wages in the
   first quarter on payroll and in 2024; the 2024 first-time employers by signup channel), with a one-page note
   charting the territories; 1 call, 4 components, 29 ask figures, 4 chart criteria and 2 files make 40 criteria.
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
8. Spine: the current account system's onboarding export (`onboarding_accounts_2022-2025.csv`, one row per account
   with a first pay date from January 2022 to December 2025, 31,912 rows, two layouts across the June 2024 migration),
   with the quarterly wage files of both systems (136,597 legacy rows, 144,043 current rows). The formation statistics
   pull is the main call's evidence; the spine and its companions carry the asks. 16 files in four formats (JSON, CSV,
   XLSX, DOCX); distractors `bfs_monthly_states_2026-04-15.csv` (the April release) and
   `nonemployer_statistics_2023_states.csv`, named in `metadata.json` only.
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
report roughly doubled, first as filers took up the new system and again as each retired its older route, while the nine other
states rose about an eighth on a wave every state shared; an application the reform added looks like any other in every
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

**WHAT screen (stumping 1.2).** The decisive step settles none of the estimand's five parts, each filed by the
standard: the population (the twelve core states' business applications in the twelve months to September 2026), the
outcome (business formations within four quarters, October release), the window (those twelve months), the unit
(Kilbourne's first-time employers, each state's formations times its 2025 share) and the comparison (none: the line
compares nothing). The nine states enter only as the identification of the added applications' yield, which is HOW the
filed quantity is estimated; every identification the data admits files 2,300 (630 constructions), and the data's own
structure (the rise every state shared from mid-2023 to mid-2024) rules out the reform states' own before-and-after
level.

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

1. Read the 2027 sizing standard: each state's line is its 2025 share in the plan workbook times the business
   formations within four quarters that a year of applications at the level of the twelve months to September 2026 will
   produce; the twelve states add up, to the nearest 100.
2. Stack the October release's state rows (unadjusted), keeping only the cohorts whose formations within four quarters
   have closed (applications to June 2025).
3. Take each state's formation rate as its formations within four quarters per application over its latest four closed
   quarters (July 2024 to June 2025 applications, the share tab's own base window).
4. Multiply by each state's applications in the twelve months to September 2026 and by its 2025 share; add the twelve.

Ends on: 2,800 (2,836.7 unrounded)
Golden: 2,300 (2,305.5 unrounded)

## Stump sentence

Carrying each state's latest closed formation rate per application onto the twelve months of applications to September
2026 at the plan's 2025 shares files 2,800; the step that lands it there is treating Ohio's, Pennsylvania's and
Michigan's latest closed rate as theirs, when it blends ordinary applications with applications the integrated filing
added, which were about a fifth of the closed cohorts and are nearly half of the twelve months, so only the added
applications' own yield, read against the nine other states before and after go-live and carried per added
application, files 2,300.

## Three rules

Task type: forecasting-forecast-evaluation (Economics & Econometrics), which serves Forecasting & Predictive Modeling in the taxonomy; the setting is a payroll company's 2027 plan sized on employer business formations from the Census business formation statistics.
Domain test: the quantity that decides the call is the employer yield of the business applications a filing reform added, estimated the way econometricians estimate a policy's effect on business formation (a difference-in-differences of applications and of closed formation cohorts against the states the reform did not reach, before and after) and carried into the formation forecast, then validated out of sample on the later closed cohorts.
Swap: "how many new depositors will a credit union sign in 2027 after three branches added online account opening" keeps a funnel and a surge but loses the federal application register whose filings become employers only after a four-quarter window, the high-propensity classification the marginal filer shares, and the filing cost whose cut changes who applies, so nothing it holds is a business formation the field would forecast.
Layer 1: the Census API pull in its long layout with FIPS codes and adjusted and unadjusted rows, the April download in the wide bfs_monthly layout with postal codes and preliminary latest months, formations published only for closed cohorts (the statistics' own lag); the onboarding export's two layouts across the June 2024 migration (legacy client-since stamps in Eastern month/day/year text and upper-case names against UTC ISO stamps), EINs hyphenated, plain and with the leading zero lost; legacy quarterly wages in cents by pay group with a company-level group, current wages in dollars with no state; the crosswalk join, state registrations keyed by account, the successor register keyed by EIN; product changes, relocations, cancellations and returns; every item is how those systems write their files and none carries the call.
Layer 2: estimand_identification, the right counterfactual: the reform states' applications split into the ordinary and the added only against the nine untreated states before and after, and the added applications' yield read from the closed post-go-live cohorts on that split, not the reform states' latest blended rate, their own before-and-after level, a propensity split or the filing's effect carried as a level.
Decisive step: identify the applications each integrated filing added as the reform state's applications less its counterfactual from the nine other states' path, estimate the added applications' formation yield from the closed post-go-live cohorts against that counterfactual, and carry it per added application onto the twelve months, whose added share has more than doubled, with the common rise at the ordinary rate.
Not semantics: every field is read correctly on the default path (applications, high-propensity and planned-wage counts, formations within four quarters, which cohorts have closed, the standard's estimand, the share tab); no field marks an added application, and reading the statistics perfectly still leaves the analyst choosing a rate for applications whose mix the closed cohorts do not share.
Not rule application: the standard files the estimand (whose formations, from which year of applications, at which share, rounded how) and no filed sentence says how to turn a state's applications into formations; executing every filed rule on the clean data files 2,800 (asserted in checks.py, R3a).
Analyst test: a strong analyst who stacks the statistics by state, keeps only closed cohorts, reads the standard correctly and carries each state's latest closed formation rate per application onto the twelve months to September 2026 at the plan's shares files 2,800; only splitting the reform states' applications against the nine other states and carrying the added applications' own yield files 2,300 (executed in checks.py on the generator's clean truth).
Estimand: the 2027 sizing standard (Dominique Thomas, FP&A, plan_2027_sizing_standard.docx) files the population (the twelve core states, named), the outcome (business formations within four quarters, the Census measure, October release), the volume (a year of business applications at the level of the twelve months to September 2026, whose formations are not yet observed), the unit (Kilbourne's first-time employers, each state's formations times its 2025 share in the plan workbook) and the rounding (the twelve states added, to the nearest 100); there is no comparison in the estimand.
No decoy: no memo, draft, forecast, prior plan figure or stakeholder estimate states a 2027 figure or argues a method; the change log states what each state's system does and when, never what it does to formations; the share tab is sales operations' 2025 count over the release's own base and ties under every reading.
No certified replay: no published or certified figure is reproduced to recover a method; the closed formation cohorts are the outcome data every method reads alike, and the out-of-sample check (the split fitted to December 2024 predicting January to June 2025 formations within 1.1 per cent, the blended rate missing by 16.8) is the analyst's own validation.
Lesson: a model learns that a leading indicator inflated by a cut in filing cost carries marginal filers whose conversion is a fraction of the average, that the fraction has to be identified against units the cut did not reach rather than assumed (zero or full), read from a blended latest rate or measured as a level, and that it must be carried per added unit onto a forward volume whose added share differs; no build on file reads a reform-added leading count's conversion yield against untreated regions.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 1: the latest closed quarter's rate, the rate having fallen | no | no | yes, recency | no | no | yes, one ratio per state | readable |
| Rung 2: the split before and after against each reform state's own 2022-2023 level | the log's go-live dates invite a before-and-after | no | yes, the event study | no | no | no | readable |
| Rung 3 (decisive): the split against the nine states' path, the added applications' yield from the closed cohorts since go-live, carried per added application onto the twelve months | no sentence names a comparison, a yield or a split | no column marks an added application; the high-propensity, planned-wage and corporate flags carry them at much the same rates | no: the reflex comparison measures the filing's effect on formations as a monthly level and carries the level (2,200) | no control scores a split; the closed cohorts are counts every method reads alike | nothing to find | no: a counterfactual, a ratio of excess formations, then a carry by volume | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | applications at the level of the twelve months | the unadjusted twelve-month total | the seasonally adjusted total | 2,300 (2,302.9) | same call |
| SF2 | the 2025 share | the tab's stored ratio | the displayed two-decimal percentage | 2,300 (2,304.0) | same call |
| SF3 | business formations within four quarters | BF_BF4Q | BF_BF8Q, formations within eight quarters | not the measure | the standard: "business formations within four quarters" |
| SF4 | the twelve core states | the twelve the standard names | other geographies in a release | not in the pull | the standard names them; the pull holds exactly those twelve |
| SF5 | the release | the October 2026 release | the April 2026 download | cannot form the twelve months (applications end March 2026) | the standard: "The plan uses the October release" |
| SF6 | a year at the level of the twelve months to September 2026 | the twelve-month total | the latest quarter times four | 2,317 | the standard: "at the level of the twelve months to September 2026" |
| SF7 | rounding | the twelve states added, then the nearest 100 | each state rounded first | not the line | the standard: "The twelve states add up to the line, which goes into the plan to the nearest 100"; 2,305.5 sits 0.45 of a bin from an edge |
| SF8 | the formations a year of applications will produce | formations within four quarters of those applications | first payrolls falling in calendar 2027 | not the measure | the standard's sizing sentence names the applications' formations |
| SF9 | a first-time employer signed in 2024 | a business whose first payroll ever ran with us, first pay date in 2024 | an account flagged first-time | the flag counts 2,847 | the counting notes: "first payroll ever runs with us"; "re-forms as a new entity and carries on, is the same business" |
| SF10 | the state it counts in | the state it first employed in (earliest registration) | the address state at the extract | moves movers | the counting notes: "in the state it first employed in" |
| SF11 | still with us in the fourth quarter of 2025 | wages we paid with a pay date in the quarter, on any of its accounts | the first account's own fourth-quarter row | misses returners and successors | the counting notes' still-with-us sentence |
| SF12 | the first quarter on payroll | the calendar quarter of the first pay date | the first full quarter | other quarters | the counting notes: "the calendar quarter of its first pay date" |
| SF13 | gross wages we ran | gross wages we ran on our payroll | wages on the returns, tax filing only included | adds filed wages | the counting notes: "the gross wages we ran on our payroll" |
| SF14 | a legacy client quarter's wages | group 00, the client's total | every group summed | doubles two-group clients | the identity 00 = 01 + 02 in every two-group client quarter, to the cent (asserted) |
| SF15 | a migrated account's signup channel | the channel of its legacy source code | the export's channel | moves four channels | the field guide: the load carried the legacy source as it mapped it; the code list; the export disagrees with the code only where the load used the default (asserted) |

## Ladder

| Rung | Construction | Figure | Rounded | Dies to |
|---|---|---|---|---|
| 0 (default path) | each state's latest four closed quarters' rate carried onto the twelve months | 2,836.7 | 2,800 | the added share of the reform states' applications: about a fifth in the closed cohorts (Ohio 0.22, Pennsylvania 0.21, Michigan 0.18), nearly half in the twelve months (0.47, 0.45, 0.40) |
| 1 | the latest closed quarter's rate, April to June 2025 | 2,703.4 | 2,700 | the same: the latest closed quarter still holds the voluntary phase |
| 2 | the split against each reform state's own 2022-2023 level, the added yield from the closed cohorts | 2,517.6 | 2,500 | the nine states rose 12.9 per cent from July 2022 to June 2023 to July 2024 to June 2025 with no filing change, so the own level counts the common rise as added applications |
| 3 (decisive) | the split against the nine states' path, the added yield pooled over the closed cohorts since go-live (0.163 of the ordinary rate), carried per added application | 2,305.5 | 2,300 | the golden |

Single-error cells off the ladder, each a full bin or more from the golden (checks.py RIVALS): the filing's effect carried
as a level 2,159.3 (2,200); the added applications never forming 2,092.8 (2,100); the pre-go-live rate on every
application 3,398.3 (3,400); every closed cohort's rate 3,177.7 (3,200); formations per high-propensity application
2,943.2 (2,900); per planned-wage application 2,985.2 (3,000); 2025's first-time employers carried 2,153.0 (2,200);
2025 grown with the twelve states' applications 2,461.9 (2,500), with the prior twelve months 2,536.4 (2,500), with
the base window 2,600.3 (2,600), year to date 2,562.3 (2,600), over six quarters adjusted 2,717.2 (2,700); each
state's closed formations on a straight line 2,440.3 (2,400), the nearest at 1.35 bins. Each correction on the ladder
walks the figure down one way; the decisive move is the only one that lands. Worth on the graded figure: rung 0 to 3 is
531 (5.3 bins); the decisive step alone, applied to the default path, moves 2,800 to 2,300 (R3b).

Construction family (630 constructions: six counterfactuals, three ordinary-rate windows, seven added-yield estimators,
the nine states' rate over every closed cohort or the latest four quarters, unadjusted or adjusted volume, the nine or
six controls): 2,286.0 to 2,319.6, every one 2,300, the nearest 0.304 of a bin from an edge. One sigma of the release's
counts (Poisson redraws): 26.0, and the family's ends plus or minus one sigma stay 2,300. Out of sample: the formations
the twelve months' applications go on to produce price at 2,308.5 in the generator's truth; the default path is 528
over it. Back-test on the closed cohorts: the split fitted to December 2024 predicts January to June 2025 formations in
the three states within 1.1 per cent; the latest blended rate misses by 16.8, the pre-go-live rate by 28.4.

P(one top response lands the call): about 0.2, since the decisive step needs both the comparison against the nine and
the carry per added application, and the reflex comparison carries a level (2,200). P(both): about 0.04.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the twelve core states' applications in the twelve months to September 2026, whose formations are not yet observed | filed literally (the standard), C1 |
| 2 Unit of account | Kilbourne's first-time employers, each state's formations times its share | filed (the standard) |
| 3 Attribution window | formations belong to the application month (the statistics' cohort) | C1: every reading uses the release's cohorts |
| 4 As-of dating | the October 2026 release, pulled 14 October 2026; the share tab refreshed from it | filed (the standard, the workbook note) |
| 5 Version basis | October release, not April | filed (the standard); C1 for the months both hold (R2, 2,302.1) |
| 6 Denominator | a state's formation rate per application; the added yield over the added applications at the ordinary rate | C3: absolute and relative yields both in the family |
| 7 Weighting | the added yield pooled over the three states or per state | C3: pooled, per state and regression estimators all 2,300 |
| 8 Window length | the ordinary rate's window (all before go-live, 2022-2023, the last twelve months before go-live); the counterfactual's base | C3: every window in the family, 2,300 |
| 9 Boundary inclusivity | Michigan's part-month go-live counted or left out | C1: 2,303.2 either way |
| 10 Rounding path | the twelve states added, then the nearest 100 | filed (the standard) |
| 11 Tie-break | none, a single figure | nothing to break |
| 12 Maturity and censoring | only cohorts whose four quarters have closed (to June 2025) | the field guide's release sentence; the release publishes nothing else |
| 13 Order of operations | share times formations per state, then added | commutes; C1 |
| 14 Row order | sums only | C1 |
| 15 Duplicate resolution | one row per series, adjustment, month and state | asserted unique; nothing to resolve |
| 16 Identity normalisation | FIPS codes to the twelve states | C1: the twelve codes, the standard's twelve names |
| 17 Netting against gross | counts, nothing to net | none |
| 18 Dimensional units | applications and formations as counts, adjusted or not | C1: adjusted volume 2,302.9 |
| 19 Code and status semantics | data type codes and the adjustment flag | the field guide; never the stump |
| 20 Integerisation | none before the rounding | none |
| 21 Clause scope | "a year of applications at the level of the twelve months to September 2026" | filed scope (the standard) |
| 22 Forward window contents | the twelve months' applications are all observed; the older routes closed inside them; the log files no further change to formation filings | shipped (the pull and the log) |

## Literal reader

Executed word for word, the standard asks for each state's 2025 share times the business formations within four
quarters that the twelve months of applications to September 2026 will produce, added and rounded to the nearest 100;
the pack holds those applications and the shares but no formations for those cohorts, so every literal reading must
forecast them; every reading of each term in the fork table gives 2,300 or violates a quoted sentence, and the easy
answer (2,800) comes from an easy method on the same literal estimand, not from another reading.

## Oracles

- The share tab's formations base: it is the October release's own sum for July 2024 to June 2025 and ties under every
  handling; it confirms the share, not a forecast.
- The share tab's 2025 counts: they tie to the onboarding export read by the flag and read by the counting notes,
  because the 2025 first-time employers carry no ask device (asserted); they confirm nothing about the line.
- The closed formation cohorts: published counts every method reads alike; the back-test on them is the analyst's own.
- The April release: an earlier vintage with formations closed to December 2024 and no forecast; nothing ties to the
  golden.
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
- A primary, D2 an attribute at the wrong vintage: until 18 November 2024 the onboarding form asked whether it was the
  client's first payroll, and businesses that had run their own payroll answered yes; their state registrations carry
  liability dates years before their first pay date with us, the only trace; silent (no column or document dates the
  change).
- A still primary, D5 a category crossed by label: an account on tax filing only still files wages on the quarter's
  returns but we no longer pay them; the export's product and product_since say so; the over-cleaning twin: 15
  accounts moved to tax filing only from 1 January 2026, which we still paid in the fourth quarter of 2025.
- B primary, D9 a rollup above its parts: a two-group legacy client's company-level group 00 holds the client's totals,
  so the plain sum of a client quarter's rows doubles its wages; found only by reconciling 00 against 01 and 02.
- C primary, D7 the true key elsewhere: the migration load gave the legacy codes CPA, BP, TEL and APX the default
  channel web sign-up; the crosswalk keeps the code, the field guide's code list gives its channel.
- Shared hazards, documented (the mirror's bar): successors through the payroll tax team's register (the counting
  notes' re-formed entity rule), returning clients under the old EIN in three formats, the state first employed in
  against the address state, legacy cents, legacy numbers through the crosswalk, the migration quarter split across
  both wage files.

Spans: A reads the export, the registrations, the successor register, the territory map, the current wages, the
counting notes and the field guide; B adds the crosswalk and the legacy wages (nine files, fourteen columns); C reads the
export, the crosswalk, the registrations, the register, the field guide and the counting notes.

| Ask figure | Golden | Cracker | Verdict |
|---|---|---|---|
| Indiana-Kentucky signed | 197 | 246 | miss |
| Indiana-Kentucky still | 153 | 203 | miss |
| Indiana-Kentucky first-quarter wages | 1,702,845.52 | 2,640,650.14 | miss |
| Indiana-Kentucky 2024 wages | 6,565,923.84 | 9,487,383.24 | miss |
| Michigan signed | 419 | 492 | miss |
| Michigan still | 334 | 418 | miss |
| Michigan first-quarter wages | 3,839,377.24 | 5,532,917.56 | miss |
| Michigan 2024 wages | 14,092,742.08 | 19,937,340.20 | miss |
| Ohio signed | 724 | 862 | miss |
| Ohio still | 594 | 737 | miss |
| Ohio first-quarter wages | 6,303,064.11 | 9,152,732.67 | miss |
| Ohio 2024 wages | 24,995,811.51 | 33,669,438.39 | miss |
| Pennsylvania signed | 410 | 501 | miss |
| Pennsylvania still | 341 | 439 | miss |
| Pennsylvania first-quarter wages | 3,448,677.54 | 5,222,086.51 | miss |
| Pennsylvania 2024 wages | 12,317,539.17 | 18,273,091.12 | miss |
| South and Plains signed | 157 | 179 | miss |
| South and Plains still | 128 | 151 | miss |
| South and Plains first-quarter wages | 1,090,881.60 | 1,522,193.97 | miss |
| South and Plains 2024 wages | 4,049,158.45 | 5,434,535.03 | miss |
| Upper Midwest signed | 134 | 161 | miss |
| Upper Midwest still | 108 | 133 | miss |
| Upper Midwest first-quarter wages | 1,086,114.72 | 1,692,419.30 | miss |
| Upper Midwest 2024 wages | 4,391,458.26 | 6,117,698.20 | miss |
| channel accountant referral | 481 | 549 | miss |
| channel bank partner | 241 | 211 | miss |
| channel outbound | 277 | 240 | miss |
| channel partner marketplace | 242 | 217 | miss |
| channel web sign-up | 800 | 1,224 | miss |

The cracker lands the call, reads the field guide and the counting notes and executes every rule they point at (EINs
normalised, returning clients and successors as one business through the register, the earliest registration's state,
territories, cents, the crosswalk, both wage files summed by quarter); it trusts the onboarding answer, every wage row,
every row of a legacy client quarter and the export's channel. Single-device cracks: the prior liability dates
(37.7), tax filing only handled by date (31.8) or every tax-only account dropped (31.8), group 00 (31.8), the legacy
codes (31.8); two at once, the prior liability dates with tax filing only, 43.5; every device cracked at once 57.7, the genuinely unstumped response.

Pair ceiling: 31.8 for the cracker, 37.7 for the strongest single-device crack (both 40 or under)
Mirror leakage: 6.1
Measured by: generator/cracker.py on the cut pack (target/), re-run by checks.py on every build

## Leak sweep

`leak.py task163 --asof 2026-10-16`: REVIEW, no LEAK. Each REVIEW line and why it is harmless:
- The standard carries the golden figure 100: it is the filed rounding ("to the nearest 100"), stated once at authority.
- The standard carries most words of the committed call: it is where the first-time-employer line is defined; it
  states no figure for it and names no rate, ratio, window or method (verify.py asserts the sizing section is free of
  them).
- The standard carries ten stump-paragraph terms: they are the estimand's own nouns (applications, formations,
  months, business); none names the comparison, the yield or the split.
- The surface screen promotes task124, task132 and task144 on the shared card keys (gap population, pattern G6, Gate G
  forecasting), the same-driver signature the card's differentiation answers at the draw; surface similarity 0.08,
  heart WARN on the draw's three repeats (Gate G, decision, question form), answered in `## Draw`.

## Tried and rejected

- Completing the surge cohorts' formations from their own early formations at the closed cohorts' development pattern (a chain ladder on the formation triangle): rejected at the draw, the same latent structure as task157 (a cohort's size from its leading edge at a timing ratio earlier cohorts kept).
- A first-payroll hazard by months since registration applied to a pool the surge filled: rejected at the draw, task134 round 1's driver.
- A formation lag that lengthened after the reforms, so the closed cohorts' four-quarter rate reads a delay as a loss: rejected at the draw, the development-speed change task451 spent.
- The high-propensity flag as a screen whose yield moves with the base rate of genuine employers: rejected at the draw, task446's driver.
- A one-time formalisation wave at each launch that will not recur in 2027: rejected at the draw, a dated cause whose effect steps a series is found by an event study.
- A timely calendar formation series in the pack (state new-employer registrations or the company's 2026 first-timers): rejected at the draw, carrying the latest twelve months forward lands within a bin of the golden.
- Two more states opening the integrated filing inside 2027 as the forward change: rejected at the draw, the formation effect of a launch inside its first year is under a bin of the call.
