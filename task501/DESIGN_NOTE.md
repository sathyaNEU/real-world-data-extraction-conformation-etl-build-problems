# task501 design note (architecture 4)

Private, never ships. Architecture 4 of the slot, re-rooted at stage 1 on 2026-10-12 after architecture 3 (the 2027
standby facility a Swiss pension foundation elects from expected capital calls) was spent at stage 4 on two failed judge
passes, both model-choice splits under the call (an unfiled fit window, then the remaining funds' call-rate base).
Architecture 2 had landed on the portal (a filed walk-forward executed by both responses) and architecture 1 was retired
on the client's rules (a hidden recycling term). Their records are the lines of `## Tried and rejected`; their files are
gone from the folder and live in git history. Carried forward from all three: the method that decides is forced by the
data's structure and never filed, every competing model is computed at design time and either lands on the golden bin or
is refused by a shipped sentence, and nothing in the pack names the step that decides. The re-root is a new domain, world
and driver (Epidemiology & Public Health); the author's brief asked for a fourth architecture rather than retirement
(precedent task130 and task180).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task501.json` (v4), registered 2026-10-12. `guard.py check`: WARN
  overuse.shape (07 in three of the last twelve: task447, task180 and this slot's own v3), answered: the grid here is
  scenario by winter figure, the native unit of a catch-up appraisal, where task447 graded claim cells and task180 plant
  quarters. NOTE test.same_driver_older (gap population, G16, method_or_model_selection) differentiated in the card
  against task104 (a self-adapting scorer replayed), task134 v1 (a competing-exit horizon probability) and task70 v2 (a
  per-record date under a class-conditional cut). Nearest driver 0.05 (task95).
- **Pairing:** Epidemiology & Public Health, task type `infectious-disease-transmission-modeling`, objective Forecasting &
  Predictive Modeling. The call is which one autumn 2027 MMR catch-up keeps measles' reproduction number in the region
  below one through winter 2027-28, a window not yet open, or whether none is needed: a forward value the field computes
  from the supplied immunity, population and contact data. Client rigor pattern
  `epidemiology-public-health/infectious-disease-transmission-modeling/2` (R is the next-generation matrix's dominant
  eigenvalue and interventions act on it; the client's pin is a contact matrix, age parameters and R per scenario).
- **Stakeholder, forum, forcing event:** Oriel Health Region's regional immunisation manager (role `programme_officer`,
  org `hospital_or_health_provider`) prepares the director of public health's recommendation to the executive management
  team (forum `executive_team`), which on 21 July 2027 funds at most one catch-up for September to November 2027.
  Forcing event `incident_or_complaint`: an imported measles case in April 2027 (a 31-year-old who attended a GP surgery
  and the emergency department in Navan) with two secondary cases in adults, after which the director asked for options.
  The incident points at adults, a reflex that lands wrong, and ranks no option.
- **People** (`guard.py names --geo Ireland --seed 501`): Eadaoin Bonner (regional immunisation manager, author of the
  options paper), Nigel Macmillan (director of public health, signs the planning standard), Therese McGann (surveillance
  scientist, the case export), Karl McLoughlin (register data manager, the extract notes). None is in the prompt.
- **Shape 07 (grid of cells):** six scenarios (no catch-up, options A to E) by the winter's reproduction number, the call
  on top (1 + 6); the deck's call slide and its chart of the six reproduction numbers against one (3); the asks per option:
  the register's residents born in its years, how many of them have no valid MMR dose and how many exactly one, the
  confirmed measles cases since 2019 in its years and the imported among them (5 options by 5 = 25); the two files (2).
  About 37 criteria, none stacked from simple asks.
- **Gap and generators:** gap population first (the region is not one pool; who meets whom decides the threshold), then
  time (the cohort the 2010-12 scare left exposed reaches the teenage band by the winter). G16 (the method the contact
  data forces), G13 (the cohort ageing into the band where mixing is densest), G6 (the composition of the susceptible pool
  by age). Gate G `method_or_model_selection`: two methods turn the same immunity into a reproduction number, and the
  survey's structure forces the eigenvalue. Strategy `other` (transmission structure); none of the listed strategies is
  honest. Calibration organ none.
- **Mechanism:** R = rho(q diag(s) C), where C is the national survey's contact matrix (mean daily contacts by participant
  age group and contact age group, corrected for reciprocity), s each five-year group's susceptible share on 1 January
  2028 (the national profile's per cent immune by year of birth, weighted by the department's projection of residents by
  year of birth), and q = 15 / rho(C), so that a wholly susceptible region has the standard's R0 of 15. Each option takes
  the options paper's expected people made immune off the susceptibles of its birth years. Prototype (scratch world2 and
  tune3): 94.7 per cent immune, R0 times the susceptible share 0.80, the contact-weighted share 0.89, the eigenvalue 1.30;
  options A 1.28, B 0.89, C 1.30, D 1.30, E 1.30.
- **Data-native sentence:** the 2008-2012 birth cohort, whose MMR uptake fell in the region's 2010-12 scare, is 15 to 19
  years old on 1 January 2028, the ages whose contacts the national survey shows falling mostly on each other, so the
  winter's reproduction number is set by how susceptible that group is and not by the region's average immunity.
- **World:** Oriel Health Region (counties Louth, Meath, Cavan and Monaghan; about 522,000 residents projected at 1
  January 2028; EUR). Its regional immunisation register holds MMR records from 1993; GP returns, the school
  immunisation team's sessions, hospital clinics and records from abroad feed it. A 2010-12 scare cut MMR uptake in the
  2008-12 births to 89 to 92.5 per cent immune; the 1990-97 births, schooled before the second dose moved to junior
  infants, sit at 86 to 93 per cent; the 2013-17 births recovered to 92.5 to 94.5 per cent. The national immunisation
  office's profile (May 2027) gives per cent immune by year of birth projected to 1 January 2028; the National Social
  Contact Survey 2023 gives the contact matrix; the national notifiable disease system (NDS, live from March 2021)
  holds the region's measles cases, including the 2019 outbreak's.
- **As-of:** the options paper is dated 9 June 2027; the register extract is at 30 June 2027 (run 3 July); the case
  export runs to onsets on 30 June 2027 (5 July); the executive team sits on 21 July 2027.
- **Sources read, one line each:** the client pattern /2 teaches that interventions act on the eigenvalue; here the
  intervention removes susceptibility from one cohort and the shortcut is the population-average susceptibility, not a
  population-weighted contact cut. `guard.py mechanisms --objective forecasting --gate-g method_or_model_selection` (11
  builds): corpus-recovered rules (27, 29, 30, 78), censored delays (99, 31), a slowest sub-unit (52), an anchor
  convention (55), rationed demand resubmitted (108), a conversion hazard by time since entry (134), a variance under
  asynchronous timing (135); none uses a transmission structure, and this draw spends the dominant eigenvalue of a
  who-infects-whom matrix. `guide-to-prompt` exemplars for depth only.
- **Abstraction test:** without nouns the driver is a chain process whose threshold is set by the dominant eigenvalue of
  a structured transfer matrix, so removing propensity where the structure concentrates moves the system across it while
  every average says it is already below; the three nearest drivers (task95, a two-class weighted conversion; task15, two
  corrections to a hold; task87, a cohort rebuilt from a second record) share no latent structure, default path or
  correction.
- **Same-puzzle test:** gap population, pattern none, decision pick_one_of_n: no build in the last twelve carries all
  three (guard PASS), and against the slot's lineage v1 (rule, B, binding_constraint), v2 and v3 (time-first forecasts
  of capital calls) differ in gap, mechanism and domain.

## Default path

1. Read the planning standard: the aim is a reproduction number below one through the winter, R0 is 15, the winter is
   assessed on 1 January 2028, immunity comes from the national profile, and an option counts for the people the options
   paper expects it to make immune.
2. Join the profile (per cent immune by year of birth) to the projection (residents at 1 January 2028 by county, age and
   year of birth): about 522,000 residents, 27,800 susceptible, 94.7 per cent immune.
3. Compare with the herd immunity threshold for R0 15 (1 - 1/15 = 93.3 per cent), or equivalently take the reproduction
   number as R0 times the susceptible share: 15 x 0.053 = 0.80.
4. Apply the standard's choice rule (no catch-up when the reproduction number without one is below one): no catch-up is
   needed, and every option lowers the figure further (A 0.78, B 0.77, C 0.79, D 0.77, E 0.75).

Ends on: no catch-up needed (reproduction number 0.8 without one)
Golden: option B, the catch-up for those born 2008-2012 (reproduction number 1.3 without a catch-up, 0.9 under B, 1.3 under every other option)

## Stump sentence

A competent solver joins the immunity profile to the population projection, finds the region 94.7 per cent immune on 1
January 2028 against the 93.3 per cent measles at R0 15 needs, puts the reproduction number at 0.8 and files that no
catch-up is needed; the step that lands it there is treating the region as one well-mixed pool, when the national contact
survey shows the 15-19-year-olds' contacts falling mostly on each other, so the next-generation matrix's dominant
eigenvalue is 1.3 and only the catch-up for those born 2008-2012 brings it below one (0.9).

## Three rules

- **Domain test:** the deciding quantity is measles' reproduction number for winter 2027-28 under each option, which
  infectious-disease epidemiology computes as the dominant eigenvalue of the next-generation matrix built from
  age-specific susceptibility and a social contact matrix; with another field's nouns there is no transmission between
  age groups, no contact survey and no susceptibility left by a vaccine history, so the task stops making sense.
- **Analyst test:** a strong analyst who reads every dose, validity rule, profile basis and survey table right and
  compares the region's immunity with the herd immunity threshold, or computes R0 times the susceptible share (0.8), or
  weights each group's susceptible share by its contacts (0.9), files that no catch-up is needed; one who ranks cohorts by
  their immunity gap targets the 30-34-year-olds (D), or the most people made immune (E); none of them brings the
  reproduction number below one.
- **Layer 1:** realistic mess across the pack, none of it on the call's path as a decider: immunity by year of birth
  against contacts by five-year group, joined through a projection that carries both; a survey matrix published by
  participant row and contact column, corrected for reciprocity on the national population; options by birth years and
  setting; a register extract loaded as received from GP returns, school sessions, hospital clinics and records from
  abroad; GP return lines queried and corrected or withdrawn in a separate log; local health office codes revised on 1
  July 2024 with one retired code reassigned to another region; a surveillance system migrated in March 2021 with the
  2019 outbreak back-entered to its outbreak module; laboratory results keyed to case numbers; an extract run three days
  after its as-of date.
- **Layer 2:** the field's method for a structured population's reproduction number (client pattern /2): the shortcut a
  capable analyst takes is the population-average immunity against the herd immunity threshold (R0 times the
  susceptible share, or a contact-weighted share), which an expert rejects because the survey shows the region does not
  mix at random; the rigorous method, the dominant eigenvalue, is the only one consistent with every shipped fact.
- **Stump class:** analytical. The decisive step is choosing the estimator the data's structure requires; no plant, no
  field read, no filed rule decides, and every rule in the pack (R0, the aim, the assessment date, the immunity source,
  an option's effect, the choice rule) is executed the same way on the default path and the golden.

## Tried and rejected

- v2 architecture (2026-10-11): the walk-forward selection with its mechanics filed in s.5.3 and the buffer as the largest end-of-horizon shortfall; both portal responses executed the filed test and landed CHF 250 million. Retired the same day: a validation whose mechanics are filed is a computation to a strong solver. v3 keeps the test and moves the deciding quantity to the buffer's estimand.
- Candidate set including a trailing twelve-month basis at v3: persistence won the honest test whenever recent vintages paced faster than history; left out.
- Seasonality at 1.35 to 0.65 (first half to second half): the path and end-of-horizon buffers sat 5 to 20 million apart, inside one tranche; set at about 70:30, which puts them 35 million apart.
- Seed sweep 118 to 149 under the sharper seasonality: nine seeds meet the honest margin, the leaky margin and the path separation; 118 kept (the persona draw's seed).
- Reserve at 50, 60 and 70 million with the 25-million menu: the fit-once path-buffer cell or the end-of-horizon cell sat within three million of the answer bin's edges; 75 million puts the answer 12 from both edges and every single-error cell at least 4 from them.
- v1 architecture (2026-10-10): the unfunded commitment restored by recallable proceeds under a term no document stated, pinned by reproducing 180 audited cells; retired 2026-10-11 under the client's 10/10 rules as data semantics and a hidden rule deciding the call (rule 3), and as a backdrop domain under the noun-swap (rule 1). The world, the pack and asks B and C were kept; the recycling term is now filed in the register and the stump moved into the validation.
- Candidate set with a trailing twelve-month basis: persistence won the honest test whenever the recent vintages paced faster than history and landed on the answer tranche; dropped, the three bases are band, strategy and band, manager's own.
- Strategy-coherent pacing shifts in the recent vintages: the strategy-and-band basis then won honestly by 11 per cent and the full-window fit tied the pooled bases, so the leak crowned nothing; replaced by manager-level and fund-year noise, under which the manager's-own basis memorises the past (full window 2.9 per cent against 6.0) and loses forward (17.2 against 9.1).
- Buffer as the second-largest shortfall: the truth and the leaky cell sat within three million of tranche edges at every reserve from 55 to 80; the largest shortfall with a CHF 60 million reserve puts the truth 10.8 and 39 from its edges and every wrong cell at least 4 from its own.
- Pooled rates as the mean of per-fund-month ratios: a fund in run-off with a small audited NAV and one large exit produced ratios above one and dominated the band; replaced by the ratio of sums at the plan-date rate (RL-PM-04 s.5.2, 5.3), which is also what a treasury would write.
- Estimator as rate on unfunded commitment (the Takahashi-Alexander form): the naive and true rates partly cancel because the naive denominator is smaller by the same recallables, and the Gate G label would have moved off binding_constraint; kept the cap form, where the construction is inert unless the cap bites, and built heterogeneous pacing so the recycling funds are the fast deployers whose cap bites.
- Uniform fast pacing: every fund fully drawn by month 24, the later age bands carried no history and the cap never bit under any construction (all constructions on one tranche); replaced by per-manager pacing (fast credit deployers, slower buyout and infrastructure).
- Distributions credited at one half: the programme's run-off distributions swamped the calls and the required facility sat at one tranche for every construction; the directive credits one quarter.
- Age bands 37 to 48 and 49 to 72: the recycling funds straddled the thin fourth band in 2027 and the band rate was too small for the restored commitment to matter; bands set to 37 to 54 and 55 to 78.
- The 2026 prepayment wave drawn from loans funded from January 2024: a third of the wave exited in 2025 and sat inside the audited cells, so the audited roll-forward reproduced most of the answer; the wave is drawn from loans funded in 2025 and exits in 2026 only.
- Short holds from the ordinary hold distribution: the normal draws put exits under eighteen months in half the funds, so commitment less calls missed 96 of 178 audited cells and was not the empirically excellent basis L7 requires; ordinary holds now start above the convergence gap and only the designed quick exits, the two historical flippers and the 2026 wave are short.
- Recallable proceeds attributed to the audited year by realisation date: an exit on 28 December with a January notice put the proceeds in different years under the two readings (one cell unreproduced); attributed by notice date, and no realisation now falls after the 15th of December.
- Reserve at CHF 30, 45 and 55 million: the truth or a wrong construction sat within five million of a tranche edge; CHF 65 million puts the truth 11.1 and 13.9 from its edges and the three wrong bases 8 to 15 from theirs.
- Producer string "Treasury & Liquidity" on the board paper's container: the raw ampersand broke the core-properties XML and the file no longer opened; the deliverables are stamped with the organisation's name.
- Context artifact as the H2 2025 semi-annual report (30 June to 31 December 2025): its closing NAV column is the opening column of ask B, five golden figures in a shipped document (leak.py LEAK); replaced by the H1 2025 report, which shares no figure with any ask.

- Signature rule / B / method_or_model_selection (any decision type): guard BLOCK, spent in 12 earlier builds (test.same_driver_older) and task71 (test.same_puzzle_older). Relabelled honestly: the forward regime is the decisive gap (time first) and the cap at remaining commitment is the Gate G mechanism (binding_constraint).
- Driver variant "late-close equalisation" (a midway entrant's first draw equals the process's draw-to-date on its own size): nearest driver task107 at 0.09, kept out because the catch-up is stated on every real notice and the rule reduces to a readable term.
- Driver variant "notices netted by some counterparties": kept out because the gross lines exist on the notice file and the move collapses to a file choice.
- v3 first decisive step (2026-10-11 to 10-12): the walk-forward kept as a filed execution layer and the buffer read on the month-end path ("at any point in a horizon", s.5.6) instead of the horizon totals; replaced on paper at the 2026-10-12 redesign before any portal test: s.5.3 filed the whole method (rule application, the step v2's responses executed) and s.5.6 named the decisive quantity (readability test 1), and the v3 world also carried a CIO and a portfolio manager each arguing a wrong basis (licensed voices). The redesign files the estimand only.
- Decisive step candidates weighed at the redesign (2026-10-12): a subscription-line overhang (investments closed but not yet called) died on the battery (an unmatched join between holdings and calls is a work order); a quantile of the year's calls with cross-fund dependence died on determinism (a quantile from eleven years of programme history straddles bins under reasonable estimators); a curve conditioned on each fund's position died as task133's driver; seasonality of calls inside the year died as task32's and the first v3's. The deadline drawdown kept: silent, analytical, and forced by every closed fund's path.
- Prototype with the deadline group's investment periods ending April to August 2027 (scratch proto2): the group started drawing down inside 2026, so the default's 2026 back-test missed by 17 per cent on some seeds and a fund's own recent rate reached half the drawdown; the group's deadlines moved to September to December 2027 and the six-month drawdown now starts inside the facility year.
- Card codings with pattern E (time, E, forecasting) and with G14 or G7 decisive: guard BLOCK (spent in task117, task37, task44, task97; G14 in task124; G7 in task229); coded G6 (the composition shift on the deadline position), which the strategy (composition_mix) names.
- Commitment wave of 2024-26 vintages at up to CHF 170 million each (prototype 3): the programme's 2026 calls ran so far above 2027's that the run rate landed inside the golden's bin on one seed in two; the later vintages were cut to a steady CHF 60 to 120 million a year.
- An expected-calls figure, or the next amount down's uncovered amount, as a graded ask: both are method figures that move by several million across the golden family; the prompt asks for the fees at the two amounts, which are exact.
- The look-through holdings as the pack's only 25,000-row file (stage 3): it is a distractor, so the bulk file did no work for the solution; the reference rates now ship in the custodian's long form for every currency it quotes (33,968 rows), which the call and the ask both read.
- Composed-mishandling target "nothing that includes P1 keeps a figure": the parallel run ended in September, so a response that dates by the custodian's credits but keeps both records is right in the five Q4 items; extending the parallel run into the fourth quarter would need a portal manager's fourth-quarter notice in every strategy, which the quarterly income pattern does not give; accepted at 5 of 25 ask items and priced into the pair ceiling.
- One random stream for every observation draw: the year totals of the ask then disagreed with the sums of their rounded quarters (Buyout 95,971 against 95,972), a rounding-path fork; the 2025-26 distribution timings got a stream of their own and streams 0 to 39 were scanned with every assertion plus the one-rounding-path test; 11, 12 and 23 pass, 12 kept (largest stop misses).
- Term sheet with the commitment fee "per annum ... quarterly in arrears" and the 2026 amount running until the election: a day count and a pro-rata January each gave another year's fee; the fee is now a share of the amount for the availability period and the elected amount runs for the whole period.
- The custodian statement's columns glossed only as "booking date" and "value date": reading the day the cash arrived as the booking date moved 19 of the 24 ask figures (credits booked a business day late, six across quarter or year ends); the field notes now say what Valuta is.
- Names within a word of real organisations (a growth manager named after a real biotech's brand, an infrastructure manager sharing a common corporate name, a real fund administrator as a paying agent): renamed Gosford Growth Partners, Juneau Infrastructure Partners and Corvisart Equity Gestion SAS; no figure moved.
- Container times left to the writer and the house scrub: openpyxl stamps the build clock, which sits inside the fiction's band and changed every build (two builds were not byte-identical), and every PDF carried the extract's date and reportlab's "(unspecified)" creator; each document now carries its own created and modified times.
- The v3 world as first built (stage-4 judge, 2026-10-12, NOT_DETERMINISTIC on margin_or_boundary_fragility): the golden's CHF 326.6 million of expected calls sat 8.4 million (2.6 per cent) above the floor of the CHF 225 million bin while RL-PM-05 left the estimation period unfiled, so rates fitted from 2024 gave the judge CHF 312.3 million and CHF 200 million, and the closed funds' drawn-share range (91.8 to 93.8 per cent) alone moved the total 13 million. Repaired by filing the period in s.5.2 (the programme's whole history since 2015) and tightening the world: each fund's spread around the managers' aim at a period end from 0.45 to 0.15 points of commitment, the four funds' pace from 0.38 to 0.36 (Tessin 0.35), which centres the golden at CHF 329.3 million against a bin midpoint of 329.5.
- Closing the fit windows by the world alone (no filed period): the 2024-onward fit stayed under the bin's floor in every world tried, because from 2024 the four slow funds carry 45 to 61 per cent of the unfunded commitment in the age bands of one to three years; milder 2023-24 market factors (0.85 and 0.90) moved it by under a million and pushed the 2026 back-test past 5 per cent. The period is filed instead; the recent windows are recorded, not family members.
- The six on-schedule funds moved out of 2027 (vintages a year earlier, closed by the plan date): the post-deadline and catch-up-set spreads fell under 2 million, but the 2025 back-test of the default went to +11 per cent and the golden fell to 323.9; the six were kept. Shrinking them to 0.5 or 0.7 of their commitments, or moving their deadlines to May to August 2027, lowered the golden 5 to 9 million or took the 2025 back-test past 7 per cent; kept as they were.
- The four funds' paces swept from 0.33 to 0.38 with Tessin's commitment at 170, 174 and 178: 0.34 and lower pushed the 2026 calls (R0) above CHF 317 million, inside 7 million of the golden bin; 0.36 with Tessin at 0.35 keeps R0 9.0 million below the floor and the family's narrowest careful member 2.23 per cent inside.
- The post-period rate as the canonical treatment after a deadline: kept as a family member (2.49 per cent inside), because as the canonical it would leave the lowest drawn share and the 24-month bands 1.6 and 1.5 per cent above the floor.
- Restoring the September 2026 facility draw (the new world's calls left the account CHF 3.3 million above zero) by cutting the pre-October reserve level from CHF 35 to 30 million: it changes a figure the minutes state; replaced by an operating minimum of CHF 5 million below which the treasury draws the facility (drawn CHF 6 million on 18 September). The minutes no longer report the October repayment, which the 24 September sitting could not know.
- The timing-stream rescan on the old arrival draws (streams 0 to 39 with the full checks): the Growth Q2 cell sat 12 francs from a rounding edge in 16 of the 18 streams run because the stream never touched its credits, and none passed. The 2025-26 distributions' arrivals are now drawn on the timing stream; 2,000 streams were screened in memory for the one-rounding-path constraints, six passed, four of them the full checks, and 360 was kept for the largest stop misses (s2 97.6, s3 26.6).
- Architecture after the portal landed v2 (facility election from expected 2027 calls; period-end completion for the four slow funds): spent at stage 4. Pass 1 found margin fragility (a 2024-onward fit window gave 200); the repair filed the whole-history period and tightened the world. Pass 2 found a fork under the call that the period does not close: once the ten funds complete to 92.6 per cent at period end, the remaining funds' base (call rate on unfunded, 329, 225; on commitment, 349, 250) is not separated by the filed records or by back-tests. Two judge passes failed, so the architecture is spent.

- Re-root candidates weighed at the 2026-10-12 draw (architecture 4): a screening programme's second-round yield (task132's reset and the v3 abstraction of a stage reached), an excess-of-loss frequency leveraged by trend (task446's driver in other nouns, and its predicate reads), a left-truncated stock forecast (the default passes the solver's own back-test), multiregional gross migration flows (forks between flow definitions, a nowcast, a small effect), a rule-of-85 retirement forecast (a filed rule read, the death of v3), saturable binding in a PK model (a table lookup), correlated polling errors and swing models (forks), regression dilution (a magnitude, and the tag drifts to causal), a survey design effect (the Kish reflex lands it). Kept: the next-generation matrix for a measles catch-up, where the default herd-immunity comparison files no catch-up and every reflex lands wrong.
- First next-generation prototype (scratch ngm1): infants under one dominated the dominant eigenvector, so the deciding group was the routine programme's and no catch-up option mattered; the under-ones are folded into 0-4 at the profile's maternal-antibody share and infant contacts follow the survey's 0-4 row.
- World prototype 2 with the 2013-17 cohort at 92 to 93 per cent immune: the 10-14 and 15-19 groups carried the eigenvalue together and no single option brought it below one (B 0.95); with teenagers' contacts concentrated within about two and a half years of their own age and the 2013-17 cohort recovering to 92.5 to 94.5 per cent, B alone takes it to about 0.89 and A, the next, leaves 1.28.
- Reproduction numbers graded to two decimals: the reasonable treatments of the survey matrix (as published, transposed, re-corrected for reciprocity on the region's population, density-adjusted to the region) and of each group's susceptible share (population-weighted or a plain mean of its years) move them by up to 0.005, inside a two-decimal bin; graded to one decimal with every value at least 0.03 from a rounding edge.
