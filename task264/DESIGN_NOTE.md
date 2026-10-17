# task264 design note

Architecture 2, re-rooted 2026-10-17 (wave 3, Descriptive lane, sathay3012), after architecture 1's determinism SEND_BACK (`## Tried and rejected`). Seed DA14's world is spent with architecture 1; this draw takes a new world. The Daskbeck Valley Regional Park Authority, a statutory joint body funded by a levy on its nine member councils, sets its 2027-28 levy at its members' budget meeting in January 2027. By the members' resolution of July 2026 the levy is apportioned among the member councils in proportion to the number of each council's residents aged 16 and over who visited at least one of the Authority's six parks in the 2025-26 survey year (1 April 2025 to 31 March 2026), each resident counted once however often they came, as estimated from the Authority's visitor survey. Every file predates the build; the call (a levy for a year not yet begun) faces forward, and the quantity it rests on is the closed 2025-26 survey year because the resolution fixes that year.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task264.json`, architecture v2, registered 2026-10-17; architecture 1 is in its lineage with its fate. The Authority is a joint body of councils (`local_government`); its members decide the levy at the budget meeting (`committee_or_panel`, `budget_or_appropriation`); the requester is the Authority's head of finance (`finance_controller`); the context artifact is the members' resolution (`filed_standard`); no calibration organ. `guard.py check`: WARN only. `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection against task235 and task465, five of the last twelve): the label is shared, the mechanisms are not (task235 a tracking loss conditioned on a delivery chance, task465 a fused two-trait count; here a person count from a visit sample). `test.same_driver_older` is differentiated on the card against task131 v1 (a randomised lift read at the parent unit), and the card also differentiates task452 (design weights from strata drawn before a map revision) and task253 (a count as a sum of probabilities under shrinkage).
2. Pairing: Survey Research & Official Statistics (client domain) / sample-design-allocation-weighting / Descriptive & Distribution Analysis. The task type's own object, the estimator a probability sample's design implies, decides the call; the setting is a regional park authority's funding formula.
3. Niche: an on-site exit survey run by a contractor at the six parks on sampled days, stratified by park, season and weekday or weekend; at the survey point the interviewer approaches every eighth adult leaving (adults in a group each eligible, each answering for themselves); about six thousand interviews; each records the respondent's home town or village, age band and how many times in the last 12 months, including that day, they visited any of the Authority's parks. The contractor's weights expand each interview to the adult visits it represents in its stratum. Residents of the three valley councils walk, run and take dogs into the parks every week or every day; residents of the six outer councils come a few times a year.
4. Call and shape: each member council's 2027-28 levy (`allocation_to_total`, question form how much). Shape 05 (allocation to a fixed total): nine councils, each with its estimated adult residents who visited and its levy, the valley councils' combined share, and the change from the 2026-27 population basis as context only.
5. Gate G `method_or_model_selection`, strategy key `population_selection` (the sample is selected in proportion to how often each person visits), decisive generator G10 (one person stands behind many sampled visits), then G14 (a respondent mix conditioned on being in the park on a sampled day).
6. Data-native sentence: an exit survey meets people as they leave, so a resident who walks the dog in Brathden Woods every morning passes the survey point about two hundred times a year and a resident of an outer council who comes twice passes it twice; the interviews, expanded by the survey's weights, are a sample of visits in which every adult appears in proportion to their own visit count, and the resolution counts people.
7. Sources, one line each:
   - The two-layer design reference's `estimation_fit` family (weighting and post-stratification; estimation that fits the data): the estimator of a person total from a sample of visits weights each interview by its design weight over the person's own visit count.
   - The Survey Research library's sample-design patterns (a base weight multiplies every stage's probability; realised cluster sizes break self-weighting; optimal allocation): this build's pattern is `own:visit-intercept-to-person-weights`, the inclusion probability made proportional to frequency by the intercept design itself.
   - task452 (stratified reference points after a map revision): weights by the strata the sample was drawn from; here the weight is set by each person's own visit count, which no stratum carries.
   - task253 (schools past a floor as a sum of probabilities) and task262 (a slope on long-run income from single-year readings) in this lane: noise in a measurement; here the selection itself is proportional to the quantity, and no reading is noisy.
8. People, drawn with `guard.py names --geo "united kingdom" --seed 264`: Claire Foster (the Authority's head of finance, author of the levy report), Toby Houghton (the survey contractor's project manager, author of the fieldwork and weighting note). Invented names (the Authority, its parks, the nine councils, their settlements and the contractor) are screened against 5,808 United Kingdom place, NHS and park names at three edits or containment (H21), in the generator's checks.

## Default path

1. Read the members' resolution: the 2027-28 levy is apportioned in proportion to each member council's residents aged 16 and over who visited at least one of the parks in the 2025-26 survey year, each counted once.
2. Stack the survey's two deliveries; code each respondent's 12-month visit count with the codebook; place each home town or village in a council through the Authority's settlement gazetteer; keep the residents of the nine member councils.
3. Join the contractor's expansion weights and sum them by council: the adult visits each council's residents made in the survey year.
4. Turn each council's visits into residents by dividing them by its respondents' average 12-month visit count (the expansion-weighted mean).
5. Apportion the levy in proportion to those residents.

Ends on: the three valley councils pay about 42 per cent of the levy between them (design target, to be replaced by the built value).
Golden: the three valley councils pay about 56 per cent (design target, to be replaced by the built value).

## Stump sentence

The default path charges the three valley councils about 42 per cent of the levy instead of about 56 because it turns each council's expanded visits into residents with its respondents' average 12-month visit count, and in an exit survey that average is visit-weighted (a resident who comes two hundred times is two hundred times as likely to be interviewed), so it overstates how often the valley councils' residents come and undercounts them most; the survey's weight over each respondent's own visit count counts each resident once and gives the golden split.

## Three rules

Task type: sample-design-allocation-weighting (Survey Research & Official Statistics), which serves Descriptive & Distribution Analysis in the taxonomy; the setting is a regional park authority's funding formula.
Domain test: the deciding quantity is a population total, each member council's adult residents who visited at least once in 2025-26, estimated from a probability sample of visits by the design-based estimator that weights every interview by the inverse of its person's inclusion probability, which an exit survey makes proportional to that person's visits; replacing it with the visit total, or with visits over a visit-weighted average frequency, moves every council's levy.
Swap: "how should a hospital trust's patient-experience budget be split among its nine clinics by the patients each saw" keeps an exit survey and a split, but loses the intercept design that draws each adult in proportion to how often they come, the expansion strata of park, season and day type and the 12-month visit count that set each person's chance of selection, so the estimator the call turns on has nothing to attach to and the task no longer reads the same.
Layer 1: the survey in two contractor deliveries (an autumn and winter workbook and a spring and summer CSV with renamed columns and a recoded age band), home places written as said (spellings, abbreviations, an old parish name) placed through the Authority's settlement gazetteer, 12-month visit counts given as numbers with a few band answers coded by the codebook, the contractor's weights in a separate file keyed to interview numbers written differently in the two deliveries, the survey year (April to March) against calendar-year counter files, and hourly car-park and trail counters with outages, a mid-year counter swap and a logger clock kept on GMT; all of it is how the contractor and the Authority's systems hold their records, and nothing is placed to be caught.
Layer 2: the estimation_fit family; a person total estimated from a sample of visits needs each sampled person weighted by the inverse of their own inclusion probability (the design weight over their visit count), because the exit survey's selection is proportional to how often each person comes.
Decisive step: weighting each interview by its expansion weight divided by the respondent's own 12-month visit count, so each resident counts once, instead of apportioning by expanded visits or dividing each council's visits by its respondents' average visit count.
Not semantics: every field and document read correctly (the resolution's residents counted once, the weights' adult visits, the visit-count question, the gazetteer) still leaves the analyst choosing how to turn visits into residents, and the natural conversion, visits over the respondents' average visits, is a size-biased average; no field, code or definition says how a sample of visits becomes a count of people.
Not rule application: the resolution fixes what is counted (residents aged 16 and over of each member council who visited at least once in the survey year, each once) and the contractor's note fixes how interviews were drawn and weighted; no filed rule says how to estimate a count of people from them, so executing every stated rule still files the default path's split.
Analyst test: a strong analyst who codes every answer, places every respondent, reads the resolution correctly and expands the interviews by the contractor's weights divides each council's visits by its respondents' average visit count and charges the valley councils about 42 per cent (Ends on: the three valley councils pay about 42 per cent of the levy between them); weighting each interview by its weight over its own visit count charges them about 56.
Estimand: the members' resolution of July 2026 (in the Authority's levy papers) fixes the population (residents aged 16 and over of each of the nine member councils who visited at least one of the Authority's six parks between 1 April 2025 and 31 March 2026, whether or not the survey met them), the outcome (the number of such residents, each counted once), the unit (the member council) and the comparison (each council's levy in proportion to its number).
No decoy: nothing is planted; no memo, draft, briefing or stakeholder figure argues a split, the old population basis is the 2026-27 levy as invoiced, and the survey is the Authority's routine visitor survey.
No certified replay: the method is not recovered by reproducing published or certified figures; no file publishes a resident count, a share or a split on the new basis.
Lesson: an on-site intercept survey samples visits, so each person's chance of selection rises with how often they come, and a count of people weights each respondent by the inverse of their own visit count; the respondents' average visit count is a visit-weighted average that overstates frequency, so dividing visits by it undercounts the most frequent visitors; no build on file teaches frequency-proportional selection.

## Readability screen

To be written at stage 2.

## Semantic fork table

To be written at stage 2.

## Ladder

To be written at stage 2.

## Closure table

To be written at stage 2.

## Literal reader

To be written at stage 2.

## Oracles

To be written at stage 2.

## Ask sheet

To be written at stage 2.

## Tried and rejected

- The seed's reliability as a matched-pair minimum (every pair of weeks sharing a set share of spending): filed literally it is a rule's execution, and left vague it is a fork; dropped at the draw.
- Reliability as the sampling error of each format's index (stores or chains resampled): the decisive move would be the resampling unit, the lesson task260 and task261 already teach in this lane; dropped at the draw.
- Each format's change on items pooled across chains as the decisive step: binary, and its insight (read the change within each seller) is task259's lower rung; kept only as rung 0 and rung 1.
- Linking relaunched packs (a smaller pack under a new code) to price shrinkflation: the link reads an item master's attributes, an identity resolution the record says never held; dropped at the draw.
- Promotions drawn at random by line and week: the four-week ends carried about two points of promotional noise in every category and format, swamping the designed gaps; replaced by each chain's weekly catalogue, one line a category a week in a sixteen-week rotation (a second, eight-week rotation for heavier programmes), so the window's first and last four weeks carry the same specials.
- The promotion calendar started at the window's first week: that week carried a quarter of the usual specials and every change fell by about a point; the calendar now starts twenty weeks before the window.
- Four chains repeating the store's weekly total on each of six to eight department rows: an eightfold over-count shows in any per-store sanity check; they now report two department groups, beside two chains reporting the same groups as a true split.
- First-draft banner and firm names (Pellwick, Penhallow, Varnley, Corbel, Tovell, Hollin, Dunstar, Wenlow, Tallen, Marrin and others) sat within two edits of Australian places; renamed after the H21 screen, figures unchanged.
- Random streams keyed to store codes: giving the July chain a refit re-numbered every later code and reshuffled the world; streams are now keyed by chain, site and segment, and the ladder was refitted once.
- Gaps asked as distances ("how far its change sits from that"): a literal reader could give them unsigned; the ask now says above or below.
- A delivery-log note on the convenience chain's till release beside its first TPR week: the first reader took it for a planted hint; the code list's in-use dates carry the record instead.
- The PC rows before 2 August 2026 left to inference from the data's pattern: the first judge read the code list literally (PC never a special, every share 0.2 to 0.6 points lower); the in-use dates now force the reading.
- The gap ask's rounding path and the continuity ask's window left to the prompt's grammar: the first judge found both open (rounded changes subtracted; each store's own panel weeks); the methodology now files the rounding path and the prompt names the chain's weeks.
- The store sales file described as takings by department: a literal reader sums the four chains' repeated rows; the dictionary now describes the rows as the chain's export lays them out, and the repetition to the cent decides it.
- Architecture 1 (2026-10-17, a grocery scanner price index's 2027 sub-index structure, each line followed at the chain that prices it): spent at stage 4. The first judge found the call deterministic (FIX_NOW on four ask forks); the one re-judge returned SEND_BACK (competing_defensible_answer) because the methodology never said what a product is, so a literal reader priced each line store by store (7 categories) and the golden's line at its chain (10) held only under an unfiled product definition; filing it would have made the decisive step rule application. The world's index-construction choices are all definitional, so the slot re-roots to a new world.
- Architecture 2 draw, partial verification of a laboratory's urine screen-out cut-off (culture only above the cut-off plus a random quality-assurance pull of screened-out specimens): the verified subsample is a gold-standard subsample, the calibration form task465 used in the last three builds (`ban.calibration`); dropped at the draw.
- Architecture 2 draw, a duration distribution read from a stock sample (people in emergency accommodation on a census night, stays weighted by the inverse of their length): the delayed-entry lesson task133 teaches and the truncation family task255 spends in this lane; dropped at the draw.
- Architecture 2 draw, competing exits treated as censoring (a cumulative incidence against one minus Kaplan-Meier): needs right censoring to tempt the survival route, so honestly `maturity_censoring`, banned against task235 in the last three; dropped at the draw.
- Architecture 2 draw, top income shares from tax tabulations by Pareto interpolation inside the band holding the 99th percentile: analytically clean, but no natural decision rests on a top share computed from tabulations by the body that sets it, and the subdomain repeats task262 in this lane; dropped at the draw.
- Architecture 2 draw, respondent-driven sampling weighted by the inverse of each recruit's network size: the design's name hands over its estimator and RDS-I, RDS-II and the successive-sampling estimator compete; dropped at the draw.
