# task146 design note (architecture 3)

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task146.json`, architecture v3, registered 2026-11-01 on a freshly pulled
  tree (guard check PASS; the differentiation lines answer task171 v5, task168, task260 and task464 v8). The axes
  were redrawn at the draw-time checks: the role family, forum, context artifact, decisive pattern and organisation
  family the last three live builds hold (task231 v2, task445 v3, task468 v6, task456 v2) are not used.
- **Pairing:** Biomedical & Clinical Research, task type `dose-response-pk-pd-modeling`, objective Forecasting &
  Predictive Modeling; the task type has never been drawn.
- **Niche:** Hvidore Biologics A/S, a clinical-stage biotech in Copenhagen, develops HB-231, a subcutaneous
  anti-IL-23p19 monoclonal antibody, in moderate-to-severe plaque psoriasis. Its phase 2b trial VELA-2 (HB231-201)
  randomised adults at Nordic sites to placebo or HB-231 25, 50, 100 or 200 mg every four weeks; the primary endpoint
  is PASI 75 at week 16. The phase 3 programme (VELA-3A and VELA-3B) starts in 2027 at North American sites. The
  clinical development plan takes forward the lowest of 50, 100 and 200 mg whose expected week-16 PASI 75 response in
  the phase 3 population is at least 70 per cent; Hvidore's board approves the phase 3 plan in December 2026.
- **Quantity:** each candidate dose's expected week-16 PASI 75 response in the phase 3 population, the patients the
  phase 3 sites will enrol as the feasibility survey lists them, response defined as in the phase 2b SAP. Forward
  facing: phase 3 has not enrolled a patient.
- **Decision:** the phase 3 dose, one of 50, 100 and 200 mg (golden 200 mg).
- **Shell:** question form what, second-sentence opener "The", rounding opener "Responses", deliverables docx+csv.
- **Setting:** VELA-2 randomised its first patient on 1 September 2025 and its last on 27 February 2026; the last
  week-16 visit fell in June 2026 and the database locked on 18 September 2026; the feasibility survey of the phase 3
  sites closed on 30 October 2026; the request is dated 16 November 2026 and the board meets on 9 December 2026.
- **Personas:** drawn with `guard.py names --geo dk --seed 1463`: Villads Kjær (HB-231 programme lead, the request's
  author), Helle Carlsen (chief medical officer), Bodil Lauritsen (head of biostatistics).
- **Data-native sentence:** an antibody's clearance rises with body weight, so a fixed dose leaves a heavier patient
  with a lower trough concentration; the phase 2b trial measured response at each dose in a lighter population than
  phase 3 will enrol, and response follows the concentration, not the dose on the label.

## Survivor anatomy

Actor: the deciding property is each phase 3 patient's trough concentration at a dose, which no file holds: the feasibility survey lists candidates' weights (in pounds at the US sites), the VELA-2 troughs belong to lighter patients, and the response the plan's bar is read on follows the trough, not the dose on the label.

Link: the signal is read through a relation no key invites: log trough per milligram against log body weight across the VELA-2 troughs (exponent 1.17 on the cut pack), joined to the composite PASI 75 through each patient's typical trough, then carried to the feasibility candidates' weights; no column crosses a dose with a weight.

Reflex: the field's dose-response method sits at rung 0 and files a wrong answer here: the arms' week-16 PASI 75 rates (100 mg at 81.0), a logistic on log dose (75.4) and an Emax fit on dose (76.8) all put 100 mg over the 70 per cent bar.

Back-test: the textbook route validates on the checks a dose-response analyst runs: the Emax curve on dose fits the five arms, the arms' rates rise monotonically with dose, and 100 mg is the plateau's shoulder; nothing in the VELA-2 data alone says the dose transfers badly.

Second use: every file the decisive step reads sits in the pack for a reason of its own: the trough samples are the trial's PK record (the SAP's section 5), the subject listing carries each patient's weight as a baseline characteristic, and the feasibility survey is the plan's own definition of the phase 3 population (section 7.2).

Shock: the movement the step recovers reads as ordinary: the VELA-3 candidates average 107 kg against VELA-2's 84 kg, a difference a reader expects between North American and Nordic adults with psoriasis, and within each VELA-2 arm the heavier patients' lower response is buried in the arm's noise.

Pins: the plan files the WHAT in its own genre (section 7.2: the lowest of 50, 100 and 200 mg whose expected week-16 PASI 75 in the phase 3 population is at least 70 per cent, the phase 3 population being the patients the feasibility survey lists, response as the VELA-2 SAP defines it); no document names weight, clearance, exposure or a model.

## Default path

A competent solver conforms the VELA-2 exports (the Lund laboratory's ng/mL, the samples below the limit, the
dd.mm.yyyy dates at the Finnish and Norwegian sites, the SAP's composite with rescue and missing week-16 PASI as
non-response), reads section 7.2 and computes each arm's week-16 PASI 75: 43.0 at 50 mg, 81.0 at 100 mg, 89.0 at
200 mg. Section 7.2 asks for the lowest dose at or above 70 per cent, and 100 mg is it; an Emax curve on dose or a
logistic on log dose says the same (76.8, 75.4). It files 100 mg. Wrong: the phase 3 population weighs more, HB-231's
troughs fall with weight, and the expected response at 100 mg in the phase 3 population is 64.4 per cent.

## Stump sentence

A competent solver reads the VELA-2 dose-response and takes 100 mg, whose arm cleared the 70 per cent bar at 81.0 per
cent; the VELA-3 candidates weigh more (107 kg against 84 kg) and HB-231's troughs fall with body weight (exponent
1.17), so at 100 mg the phase 3 population is expected at 64.4 per cent and only 200 mg (84.9) clears the bar.

## Three rules

Task type: dose-response-pk-pd-modeling in biomedical-clinical-research, which serves forecasting: the expected week-16 PASI 75 of each candidate dose in a population phase 3 has not yet enrolled, forecast from the phase 2b trial's exposure and response.

Domain test: the deciding quantity is a dose's expected response in a target population, worked the way clinical pharmacology works a dose choice: a population PK model of the troughs on body weight, an exposure-response model of the responses, the target population's covariates carried through both; in another field's nouns (a school's pupils, a retailer's stores) there is no trough, no clearance and no dose, and the quantity stops making sense.

Swap: "which store format should the retailer roll out, judged on its pilot stores' sales?" keeps the sentence's shape and loses its substance: a store format has no exposure that falls with a customer's size and no dose whose effect is carried by a concentration, so the deciding quantity stops making sense.

Layer 1: the Lund laboratory's troughs in ng/mL against the central laboratory's ug/mL; samples below the limit as text; PASI recorded as integers at some sites and with one decimal at others; dd.mm.yyyy dates at the Finnish and Norwegian sites; the Finnish eCRF build's labels (its screening record labelled Baseline, its first-dose record Day 1); the Norwegian pharmacies' first doses a few days after randomisation; ePRO entries in UTC with after-midnight entries belonging to the evening before; US weights in pounds.

Layer 2: the data's real structure in a dose choice carried to a new population: response follows exposure, exposure at a dose falls with body weight, and the population the bar is read on is heavier than the one the dose-response was measured on, so the expected response is a transport of the exposure-response through a population PK model to the target population's weights.

Decisive step: fit the troughs' log concentration per milligram on visit and log body weight, read each VELA-2 patient's typical week-16 trough, fit the composite PASI 75 on its log, and average the fitted response over every feasibility candidate at each dose; 100 mg falls to 64.4 per cent and 200 mg holds at 84.9.

Not semantics: every field, code and definition read correctly (the units, the limit, the composite, the labels, the dates, the pounds) still leaves the arm rates at 81.0 per cent for 100 mg, because how a dose's response moves with a population's weight is not a field: it is a relation the analyst has to model.

Not rule application: no filed rule names weight, clearance, exposure or a model; executing section 7.2 word for word on the arm rates files 100 mg; the enumerated family (the arm rates, a logistic on log dose, an Emax on dose, the same routes on the Finnish labels) spreads 75.4 to 81.0 at 100 mg, all over the bar; the standing family (exposure-response through the weight model, logistic or Emax, the exponent fitted or fixed at 1.0, the prior-biologic covariate, the observed week-16 trough with the between-patient spread, a logistic on log dose and log weight) spreads 64.0 to 67.2, all under it; the ruling-out is loud: the troughs fall with weight at an exponent of 1.17 (the PK model's own fit).

Analyst test: a strong analyst who reads every field and rule correctly computes the composite by arm, reads section 7.2 and files 100 mg (81.0 per cent); carried through the weight model and the exposure-response to the VELA-3 candidates, 100 mg is 64.4 and only 200 mg clears 70.

Estimand: the plan files it: the expected week-16 PASI 75 response, as the VELA-2 SAP defines it, of each of 50, 100 and 200 mg in the phase 3 population, which is the patients the VELA-3 sites will enrol as the feasibility survey lists them; the call is the lowest dose at or above 70 per cent.

No decoy: nothing is planted to be caught: no memo, briefing or stakeholder states a response, a dose or a model; the email names the rule and the files; the adverse event and DLQI listings are distractors named in metadata.json that rank nothing.

No certified replay: no published or certified figure is reproduced: no table in the pack carries an arm's response rate, a trough summary or an expected response, and every figure is rebuilt from patient-level records.

Lesson: a dose-response measured in one population answers a dose question in another only through the exposure the dose produces there; no build on file carries a response across populations through a model of how the input's uptake falls with a property the target population carries more of.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the arms' week-16 PASI 75 rates | section 7.2 invites the arm rates | `arm`, `pasi_total` | the dose-response reflex | the composite as filed | the units and the dates | one share per arm | none | readable |
| R0b a logistic on log dose | none | `arm` | the dose-response model reflex | validates with R0 | none | one regression | none | readable |
| R0c an Emax fit on dose | none | `arm` | the MCP-Mod reflex | validates with R0 | none | one curve | none | readable |
| R2 (decisive) the exposure-response carried to the candidates' weights through the trough model | silent: no sentence names weight, clearance, exposure or a model (asserted on both PDFs and the email) | silent: no column crosses a dose with a weight | silent: no reflex reads a dose's response in a heavier population | silent: none | silent: none | two models joined | none | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "baseline" | the last PASI on or before the first dose (SAP section 2) | the record labelled Baseline | 100 mg on the arm rates (80.0): same easy call; the golden's composite unchanged | SAP section 2 (asserted C4) |
| SF2 | rescue therapy | ATC D07AC or D07AD, or phototherapy, after the first dose and on or before the week-16 assessment (SAP section 3) | any topical corticosteroid | same call | SAP section 3 |
| SF3 | a patient with no week-16 PASI | non-responder (SAP section 3) | excluded | same call | SAP section 3 |
| SF4 | the troughs used | weeks 4 to 16, below-limit samples out (SAP section 5) | week 16 only | same call (asserted, the observed-trough member) | same call |
| SF5 | the trough units | ug/mL, the Lund ng/mL divided by 1,000 | taken as written | another exponent | the unit column |
| SF6 | the weight model | log trough per mg on visit and log weight | exponent fixed at 1.0 | 66.3 at 100 mg: same call | same call (asserted C2) |
| SF7 | the exposure-response form | logistic on log typical trough | Emax; the observed week-16 trough with the spread; a logistic on log dose and log weight | 65.7, 67.2, 67.1 at 100 mg: same call | same call (asserted C2) |
| SF8 | the phase 3 population | every feasibility candidate (CDP section 7.2) | the median candidate | same call | CDP section 7.2 |
| SF9 | the US weights | pounds times 0.45359237 | taken as kilograms | another population | the sheet's header |
| SF10 | "at least 70 per cent" | inclusive | exclusive | same: 64.4 and 84.9 are far from 70 | same call |
| SF11 | prior biologic use | no term (the plan's population is everyone listed) | a covariate | 64.0 at 100 mg: same call | same call (asserted C2) |
| SF12 | ask A's baseline | as SF1 | the labelled record | other rates | SAP section 2 |
| SF13 | ask B's study days | from the first dose in the dosing log (SAP section 2) | from randomisation | other shares | SAP section 2 |
| SF14 | ask B's diary day | local time, after-midnight entries to the evening before (SAP section 4) | the UTC date | other shares | SAP section 4 |
| SF15 | ask B's weekly score | at least four of the seven days (SAP section 4) | any entry | other shares | SAP section 4 |

## Ladder

| Rung | Route | 50 mg | 100 mg | 200 mg | Call |
|---|---|---|---|---|---|
| R0 | the arms' week-16 PASI 75 (VELA-2) | 43.0 | 81.0 | 89.0 | 100 mg |
| R0b | logistic on log dose (VELA-2) | 48.9 | 75.4 | 90.8 | 100 mg |
| R0c | Emax on dose (VELA-2) | 47.7 | 76.8 | 90.8 | 100 mg |
| Golden | exposure-response through the weight model, averaged over the VELA-3 candidates | 37.2 | 64.4 | 84.9 | 200 mg |
| Standing | exponent fixed at 1.0, Emax form, prior-biologic covariate, observed trough with spread, log dose and log weight | 34.5 to 41.2 | 64.0 to 67.2 | 84.6 to 86.7 | 200 mg |

Separation: the lowest easy rung at 100 mg (75.4) sits 5.4 over the bar; the highest standing member (67.2) sits 2.8 under it, and every member puts 200 mg at least 14.6 over it; the world's own truth is 65.6 at 100 mg and 83.0 at 200 mg.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the patients the VELA-3 sites will enrol, as the feasibility survey lists them | filed: CDP section 7.2 (SF8) |
| 2 Unit of account | a patient's week-16 composite response | filed: SAP section 3 |
| 3 Attribution window | week 16 | filed: CDP section 7.2 |
| 4 As-of dating | the locked VELA-2 data and the survey of 30 October 2026 | the email and the files' dates |
| 5 Version basis | one locked snapshot | C1 |
| 6 Denominator | the patients randomised to the arm | filed: SAP section 3 |
| 7 Weighting | each candidate once | filed: CDP section 7.2 |
| 8 Window length | weeks 0 to 16 | filed: SAP |
| 9 Boundary inclusivity | "at least 70 per cent" | C1: same call (SF10) |
| 10 Rounding path | rates to one decimal; the expected responses graded by their side of the bar | the prompt |
| 11 Tie-break | none: the lowest qualifying dose | filed: CDP section 7.2 |
| 12 Maturity and censoring | none: week 16 complete for every patient | C1 |
| 13 Order of operations | conform, model, transport | C1 |
| 14 Row order | by subject and date | C1 |
| 15 Duplicate resolution | one assessment per visit | C1 |
| 16 Identity normalisation | the subject id throughout | C1 |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | ug/mL, kg | the unit column and the sheet headers (SF5, SF9) |
| 19 Code and status semantics | ATC classes, visit labels | filed: SAP (SF1, SF2) |
| 20 Integerisation | none | C1 |
| 21 Clause scope | the bar applies to the expected response alone | filed: CDP section 7.2 |
| 22 Forward window contents | the expected response of each dose in the phase 3 population | filed: CDP section 7.2; C2: every standing member keeps the call |

## Literal reader

On paper and on the cut pack: section 7.2 files the quantity and its WHAT (the expected week-16 PASI 75, as the VELA-2
SAP defines it, of each of 50, 100 and 200 mg in the phase 3 population, the patients the feasibility survey lists)
and the rule (the lowest at or above 70 per cent). Executed word for word, the WHAT leaves open only how a dose's
response in VELA-2 becomes an expected response in the phase 3 population, and the record forces it: the troughs fall
with body weight (exponent 1.17), the candidates are heavier, and every member that carries VELA-2's response through
exposure to the candidates' weights lands 64.0 to 67.2 at 100 mg and 84.6 to 86.7 at 200 mg. Every literal reading of
a convention on the call (SF1 to SF11) keeps the golden's call or is ruled out by a quotable sentence. Pass.

## Oracles

- The world's own truth: the expected response with the truth's clearance, spread and exposure-response is 65.6 at
  100 mg and 83.0 at 200 mg (asserted C6); every trough follows dose over clearance (asserted C7).
- The asks: every figure recomputed independently by verify.py (20 of 20).
- No shipped oracle: no file ties only under the golden reading.

## Ask sheet

Pair ceiling: pending (the device redesign below)
Mirror leakage: pending
Measured by: generator/ceiling.py, to be written after the device redesign

| Ask | Primary device | Golden | The cracker's figures | Cracker |
|---|---|---|---|---|
| A, week-16 PASI 75 and PASI 90 by arm (10 figures) | pending: the Finnish label device is defeated by the SAP's date rule | in figures.json | pending | pending |
| B, itch responders at weeks 12 and 16 by arm (10 figures) | pending: the first-dose anchor is defeated by the SAP's day-1 rule | in figures.json | pending | pending |


## Tried and rejected

- The seed's mechanism (an employer-filed block of claims for idled workers that the attention signal cannot see,
  with a model-risk standard certifying the house method on 52 past nowcasts): a hidden bulk filing and a certified
  record built to bless the wrong method, both banned as the decisive step (10/10 rules 3, and the validated decoy).
- The seed's home domain (`economics-econometrics`, forecasting): banned against task145 (the pairing in the last three
  builds); the house alias `economics` would pass the guard by name only and was not used.
- Additive against multiplicative seasonality under a non-seasonal level rise (the seasonal swing fixed in claims while
  a shock lifts the level): rejected at the draw because the solvers' own defaults split both ways (statsmodels'
  `seasonal_decompose` and STL are additive, ratios and year-on-year growth multiplicative), so the stump would be a
  coin flip on a library default, not an analysis a capable analyst skips.
- An attention-signal nowcast fitted on pages chosen by in-sample correlation, validated out of sample: the client's
  own example, but `forecast_method_backtest` is task145's strategy (banned in the last three) and the decisive step
  would need a filed back-test organ two builds running.
- A Labor Day or Christmas holiday misalignment in 52-week ratios: rejected as a calendar reading (time semantics)
  that a capable analyst checks by reflex, and as task102's family.
- A benefit-year anniversary echo of last year's surge (claims filed again 52 weeks on): rejected as too near task134
  v2's driver (an inflow a pool sends a year after entry) and too small at realistic re-employment.
- The national figure at a US scale (about 220,000 a week) or at 40,000: prototyped on 2026-10-15; the golden's
  defensible variants (the estimation sample, the base week, the step's form) spread 2 to 3 per cent, wider than a
  thousand-claim bin; a country of about 9 million (about 12,000 claims a week, the first week about 16,000) keeps
  every variant inside one bin with the rivals two or more bins off (prototype, eight seeds).
- The world prototype's first settings (2026-10-15): a pandemic surge of 4.3 times and holiday weeks at 8.5 per cent a
  day lost biased the rate (0.070 against the world's 0.084) and spread the golden's constructions over 827 claims;
  the surge was softened to 2.35 times and the holiday effects to 3 per cent a day.
- High-ineligibility quarters placed mostly in the third quarter: they lifted the fourth-quarter intercept every rival
  carries and put the level-driven and ratio rivals in the 15,000 bin, one bin from the golden; spread across the year.
- The episodes of 2022 to 2026 as first set: the high pools all fed the April turns and the January turns with the
  largest calendar moves followed the low pools, so the post-2022 construction came out about 650 claims low in every
  world seed; rebalanced, and the January return and shutdown softened, after which it is noise around the others.
- An attention-signal ask (the seed's encyclopedia page views, or search-interest exports each scaled to its own peak):
  its index needs a filed construction a careful solver executes, and its UTC-hour and rename devices are found by
  the battery; dropped.
- An insured unemployment rate ask (continued weeks over covered employment): every device found (fortnightly
  certifications, provisional quarters, an office restructure) is adjudicated by the definition a careful solver
  executes, so none holds the cracker.
- A first-payments ask (payments reissued under fresh ids): the battery's claim-and-week dedupe repairs it.
- The industry classification as a full renumbering: a raw join then gives implausible changes that invite the check;
  kept as partial code reuse with every total tying.
- The refiling at one national rate as the decisive step (the design paused on 2026-10-15): under the strict reading of
  rule 3 the base-period definition, read against the quarter turn, lets a careful reader infer that refused claimants
  can file again, and once inferred the natural sizing (the national determinations at the rate past turns show) is the
  golden, so the decisive step leaned on reading a definition; deepened so the share differs by region and the national
  rate on the national pool files a bin low (2026-10-16).
- A refiling share by the month of refusal (claimants refused late in the quarter come back more): a duration-dependent
  pool too near task134 v2's hazard by time since entry, and three monthly pools too collinear to separate three shares
  from 50 turns.
- A refiling share by the reason for monetary ineligibility: which reasons a base-period move cures can be read off the
  reasons' definitions, the same semantics lean one level down.
- A quarter-end separation bump in every quarter's last claims week (tried so that no-intercept rates miss): it gave the
  October turn a negative step of its own that crude ratios ignore, which carried a crude last-four-turns rate onto the
  golden; replaced by the fiscal year's end in June alone and a summer shutdown spanning the first January week.
- The 2025 boom quarters at the usual regional mix: the last four turns' national rate then sat near the golden; in
  this world the boom regions refused few claimants through 2025 and early 2026, and the latest-period rates read low.
- The national refiling at a steeper level only (re-centring the golden by the rate): the national-pool rival rose with
  it; the golden was re-centred through the late-2026 level, which moves every construction alike.
- Ask A's first-layoff dates stored as UTC stamps of local midnight (the device drafted at the pause): the hygiene
  battery executes UTC conversions (measured in-house), so it would not hold the cracker; the portal's lodgement stamps
  stay in UTC as texture.
- Ask B's week labels against the quarter-of-the-Sunday rule as a device: a filed rule adjudicates it; kept only as the
  cube's label switch at its rebuild, which no sentence states.
- The portal going live on 1 June 2026: the register then held few notices with first layoffs in October to December,
  so the re-keying touched three cells; moved to 1 July 2026, the fiscal year's start.
- Random coverage of the regions' cross-region sites: two cells carried only in-region employers in one draw, so the
  cracker hit them; every region and period now carries a site of an employer registered elsewhere by construction.
- The legacy weekly file's weeks labelled by their Saturday (the drawn Layer 1 item): read at face value for the
  quarter, the label moves the 29 legacy turns a week early and the call from 15,994 to 12,491 on the world, so a mess
  item could flip the call; both claims-system layouts key the week by its Sunday, and the Saturday-to-Sunday switch
  stays only in the cube, as Ask B's ledgered device (2026-10-16).
- The refiled claims and the rest of the week stated to the nearest 500 (4,500 and 11,500): the ratio form puts the
  refiling at 4,889 and the mean of three weeks as base puts the rest at 11,784, so no rounding is shared by every
  construction; stated as 4,000 to 5,000 and 11,000 to 12,000, which every construction and a one-sigma move keep.
- The regional first-week shares stated in whole per cent (about 2 in the Capital, 21 to 27 in Western, Coastal and
  Island): one sigma moves the Capital's 2.1 across 1.3 to 2.9; stated in words (one in five, one in four, fewer than
  one in ten), which every construction and a one-sigma move keep.
- The program statistics published on the fifth working day (7 October), before the weekly release of the month's last
  claims week: the month would make that week public before its advance count; published with the Thursday release,
  the last week at its advance count.
- A bank desk holding Employer Services' register and case notes with no record of how: the desk's data log records
  them as released on its information request, beside where every other file came from.
- "Most of the rise" for construction and accommodation in the preview: they rose 15,963 against a total rise of
  12,604; the sentence now says more than the whole rise, nine of the other twelve groups lower (asserted).
- base-period refiling left to the definitions: data semantics, per the rule 3 audit
- The three tourism and building regions' refusals moving independently of one another (the stage 3 world): their part
  of the pool hardly varied across turns (standard deviation 0.051), so pooling cost the national fit nothing visible
  (leave-one-out 414 against 400) and the national rate sat one bin low; a common quarterly factor for the three regions
  now shows the misfit in the history (2026-10-16).
- Ask B's rounding floor raised to 0.27 of a bin: unreachable for the smallest group, whose change moves about half a
  bin with each claim; kept at the design's 0.23.
- regional sizing alone: both top responses land it once the refiling is filed, per the rule 3 re-audit
- A refusal's weight decaying over four weeks with month swings of 0.22 (the first strengthening world): the month
  model predicted past turns no better than each region's quarter taken whole (leave-one-out 322 against 319), the
  April 2020 turn's pandemic fall swamping the timing; a 2.5-week decay with larger month swings, common to the three
  regions, and timed episodes separates them (303 against 635).
- The September wave on the history as it stood (no late waves): the 2026 last-month refusals over the base week sat
  beyond every past turn and the multiplicative form overshot to about 17,600 (18,000); with late waves in the history
  and September's refused share at 0.55, the multiplicative form lands the golden's bin (17,225).
- Late layoff waves in the recent quarters (Western 2022, Coastal 2024): they lifted the timing-blind constructions on
  the recent windows to about 16,600, inside a bin of the golden; made early waves (2026-10-16).
- The first draw of the month swings' streams: the national step on the three regions' months and the rest's filed
  16,437 (16,000), 460 claims under the golden on a standard error of 220; among forty draws, the one kept holds every
  construction of the golden within 310 claims.
- The week ended 3 October at a round 11,800 (the late-claim share's first range): a round headline count reads as
  made up; the range moved to 0.0023-0.0095 (11,814), which also keeps Ask B's nearest change 0.281 of a bin from its edge.
- Architecture 1 (the Unemployment Insurance Board's first weekly count of the fourth quarter, sized from the refiling
  pool region by region), retired 2026-11-01 by the batch 1 audit before any portal result: it was designed before the
  survivor anatomy gate, its note carries no Actor, Link or Reflex line, and precut.py fails it (no `Measured by:` line
  naming the script that ran the cracker on the cut pack); the refiling share was the part that fell short, a sizing a
  careful reader takes once the base-period definition is read. Re-rooted rather than repaired so the portal sees one
  strong build.
- Re-root draw screens (2026-11-01), each rejected before a card: a vineyard's frost nights under inversions (dead in
  task170's notes, and a probabilistic transfer with the right residual variance lands the count without any regime);
  a reserving triangle's settlement-speed or inception-mix change (Berquist-Sherman is a named correction; task176's
  notes measured the cell); amount-weighted pensioner deaths and a lapse wave at a linked mortgage's fixed-rate end
  (task171's miners' trust died on persistence; the linked-contract clock is task176's driver); scaling laws under
  data repetition and a strategy's borrow costs (task171's screen; task306's participation curve); a delisted brand's
  demand read from stock-outs (a filter and a divide, task171's note); a health plan's default under inertia (the
  opponent's first move once the default is filed); a practice closure dispersed through households (task124's group
  members' records); reactive inspections inflating a fault rate (filing the scheduled programme names the population,
  task269 v4's law).
- Architecture 2 as a whole (2026-11-01, on paper at stage 2, before any reader or judge): spent by the rule
  application lines the skills took from the day's deaths (19c4263b: a filed estimand naming the members one
  source misses, shipped beside a source that lists them, makes linking it rule application; 273af233: an
  inclusion or exclusion over a second source has no safe filing). Following the money across a member's move
  between instant-access issues is exactly that inclusion: policy 7.3 files it and the event log lists every
  move, while dropping 7.3's wording leaves the account cohort as the literal reading. The world, generator and
  goldens stay green (target.zip 06b54fc7) as history; the slot re-roots into another world with the decisive
  step drawn as an estimate no shipped source lists.
- Architecture 3 stage 2 (2026-11-01): the two ask devices first drawn (the Finnish eCRF's labels, the screening record labelled Baseline; the Norwegian pharmacies' first doses after randomisation) move 6 of 10 and 10 of 10 figures for a solver who reads the labels or the randomisation date, but a cracker that executes the SAP's own rules (baseline by date on or before the first dose; study day 1 from the dosing log) keeps every figure; the asks need devices that ride a reconstruction across two systems no sentence states.
