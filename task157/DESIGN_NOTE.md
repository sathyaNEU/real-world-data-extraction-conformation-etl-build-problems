# task157 design note

Architecture 1, drawn 2026-10-17 (wave 5, Forecasting lane, sathya8571), numbered from seed FC28. The seed (a Midwestern
ride-hail operator's January winter guarantee, $350 to every driver completing 40 trips in four weeks, pre-funded by
finance as one figure) was read at its header and Situation only. Its world, decision and quantity are kept. Its two
banned features are not shipped: no file reveals the returning drivers on its own (the insurer's roster acknowledgement
is not in the pack; the returners are in the same activity extract as every other driver), and no document files a
method for the payout. The pitfall is re-found from how the returning drivers come back: Larch Rides' first winter
recruitment campaign (first trips February and March 2026) took on mostly workers laid off for the winter, who went
back to their trades in April and come back as their trades shut down, a wave that began in mid-November 2026 and peaks
when the guarantee goes live on Monday 4 January 2027.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task157.json`, architecture v1, registered 2026-10-17T11:55:39Z;
   `guard.py check` PASS (one NOTE: the older signature gap time, G12, Gate G forecasting is differentiated against
   task231). Nearest driver 0.05 (task116 v1 lineage, task143, task264).
2. Pairing: Product Analytics (client domain) / `retention-cohort-lifetime-value-modeling` / Forecasting & Predictive
   Modeling. The seed's house label was Economics (platform labour supply); the client taxonomy files a platform's own
   user analytics under Product Analytics ("a platform selling into a sector is Product Analytics", domains README), and
   the deciding analysis here is a supply-side user cohort's reactivation forecast (resurrected users in growth
   accounting), not a labour-supply elasticity, an incentive response or a labour-market read. Economics &
   Econometrics would be the honest home only if the decisive step were an elasticity or a behavioural response to the
   guarantee; it is not, so the ban on economics-econometrics x forecasting (task155) does not bind and is not dodged.
3. Niche: a regional ride-hail operator in the Twin Cities funding its January 2027 winter guarantee at go-live, when
   last winter's recruitment campaign put about 2,200 drivers on the road in February and March 2026, most of them
   seasonal workers whose return wave straddles the funding date.
4. Call and shape: the guarantee's expected total for the four weeks from Monday 4 January 2027 (`quantity_figure`,
   currency, question form how-much), to the nearest $50,000 (finance funds the account in $50,000 steps), with the
   drivers expected to qualify to the nearest 100. Shape `other`: the fund and the drivers with four critical components,
   two ask tables on files the call never reads (6 and 15 figures), and a two-slide deck; criteria counted in
   `## Ask sheet`.
5. Mechanism keys: gap time (the evidence is December's roster and last winter's return; the window holds the rest of a
   wave already arriving) with population (who is in January's population: returning seasonal drivers on no roster);
   decisive generator G12 (a summer of blanks is not churn: the campaign recruits' empty months are a return not yet
   made), then G13 (the window holds the wave's remainder) and G16 (the leading-edge method against the pool rate, chosen
   out of sample on January 2026); Gate G `forecasting`; strategy `maturity_censoring` (the wave is incompletely arrived
   at the as-of and is completed from its own arrivals, the return share a property of the cohort and the return
   timing common to every wave).
6. Layer 2: `estimation_fit` (censoring), pattern `own:returning-seasonal-wave-sized-from-its-leading-edge`. Library
   neighbour: product-analytics/retention-cohort-lifetime-value-modeling/1 (young cohorts are censored, not churned);
   this build's version differs in that the censored cohort's size is read off the part of its own return already
   arrived, at a timing ratio earlier cohorts kept, rather than from cohorts observed that long.
7. Furniture: forum `executive_team` (Larch's finance director funds the guarantee account); forcing event
   `launch_or_rollout` (the 2027 guarantee goes live in the drivers' app at 00:00 on Monday 4 January and is funded in full
   at go-live; `season_or_peak` was the other honest key and was banned by task155 at the draw, so the call is forced
   by the programme's go-live, which is what the email and the terms name); organisation family `software_or_platform`;
   role family `operations_director` (the head of driver supply sends the figure); context artifact `published_series`
   (the supply team's monthly KPI report, published through November); calibration `prior_period_close_out` (the
   payments system's payout files for the 2025 and 2026 windows, the closed outcomes the rates and the back-test read).
8. Spine: the warehouse's monthly driver activity extract (driver x month: completed trips and online time), from Larch's
   launch in May 2021 to the extract run on Sunday 3 January 2027, in two layouts across the July 2024 dispatch
   migration; constructed in the layout of a ride-hail data warehouse export.
9. Deliverables: `guarantee_fund_jan2027.xlsx` (the fund, its critical components and the two ask tables) and
   `guarantee_fund_jan2027.pptx` (two slides: the fund, and the last two windows' cost from gross to net); the format set
   (xlsx and pptx) is in none of the last three builds.
10. People, drawn with `guard.py names --geo "United States" --seed 157` and checked clean: Gary Mathews (head of driver
    supply, the requester, in no file the prompt names and not in the prompt), Kathy Sherman (finance director, the
    funding email), Jesse Velasquez (supply analytics, the KPI report's owner and the warehouse extract log), Melvin
    Harrell (payments operations, the payout files and the returns log). Invented names: Larch Rides (checked against
    real ride-hail and Minnesota firms: no match); further names (the rental partner, the campaign's name) are checked the
    same way when the pack is cut.

**Data-native sentence.** Larch's records show every driver's month on the road, so last winter's campaign recruits are
not hidden anywhere: they drove from February to April 2026 and then took no trip from May to October, which reads as
churn; but most of them were laid off for the winter and went back to their trades in April, and they come back as their
trades shut down, in a wave whose timing (a run of returns from mid-November, a lull over the holidays, the largest week
the week the guarantee goes live) has been the same in every winter on Larch's record, while how many of a winter's
drivers come back is the group's own; so the part of the wave already back on the Sunday before the window gives the
part still to come, and no rate on the drivers away or by the month each left can.

**Guard and similarity.** `guard.py check` PASS at registration. The ban window held task155, task464 and task265 (the
re-pull before the check brought task265 in and moved task237 out, which freed `launch_or_rollout`). WARN answered at an
earlier check: `repeat.gate_g` (forecasting, task155) is the honest Gate G key for a call whose difficulty is the forecast
of a forward quantity; the xlsx and docx set (task265) was replaced by xlsx and pptx. Same-puzzle and same-driver tests:
gap time, decisive G12 and decision `quantity_figure`, Gate G `forecasting`: task231 only (older, differentiated on the
card: a lagging exit register read from mature rounds, not a returning wave read from its own leading edge).

**Abstraction test.** Stripped of nouns: members of a group that stopped together come back in a wave that begins before
the forecast date and peaks inside the forward window; how many come back is the group's own and when each comes back
follows a calendar every earlier wave kept, so the members still to come are the members already back times the ratio
earlier waves showed between the window and the same date. The nearest by mechanism, read for latent structure:
- task146 weighs a pool built in the closing quarter by the month each claimant was refused, each region at its own
  refiling share; there the timing of the refusal is the rate. Here timing carries no rate (it is common to every wave),
  the group's return share is unknowable from when its members left (the campaign's bonus drivers and its seasonal
  workers both stopped in April), and the move is reading the group's size off its own arrivals.
- task151 sums a unit's chances of clearing stepped lines from a resampled distribution of comparable seasons; here there
  is one line, priced at last year's observed rates, and the decisive quantity is how many members of a returning cohort
  enter the window at all.
- task156 projects a shrinking volunteer pool against arrivals of work; here the cohort is coming back, and the forecast
  reads its size from the leading edge of the return.
- task133 starts loans at their age at a takeover (delayed entry) and task265 starts hips at their registry enrolment;
  here nothing is truncated: the cohort's churn is right-censored by a winter not yet over.
- task134's round-1 architecture converted a pool by months since admission, and task231 reads silent units' exits
  from mature rounds; here no hazard is fitted, and the pool rate is the rival the out-of-sample check rejects.
- task181 (the record's nowcast family, F4) completes an arrived count by each route's own delay; here the delay
  profile is common and known, and what differs between groups is the share that ever comes back, which only the arrived
  part reveals.
None shares the latent structure, the default path and the correction.

**Sources, one line each.**
- Seed FC28 header and Situation (`status.py task157`): the world, the $350 guarantee at 40 trips, the January pre-funding,
  the first winter campaign whose recruits had mostly stopped by May; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting` (68 builds): reactivation and return ground on file is a quarter-turn
  refiling pool weighted by refusal month (task146), a hazard by time since admission (task134 round 1), mature-round exit
  shares (task231) and a dormant residue among recirculating stock (task91); none reads a returning group's size off its
  own arrivals.
- `stumping/references/client/layer2-rigor-patterns.md`, product-analytics retention-cohort pattern 1 (young cohorts are
  censored, not churned): the cohort here is censored by a winter that has begun, so the estimator is its own early
  returns developed at the earlier cohorts' timing, not a survival curve from cohorts observed that long.
- `stumping/references/strategies.md` F4 (maturity and censoring; vary what is censored, whose speed differs) and F6
  (method selection out of sample): what is censored is a cohort's return, its speed is common, its size is not.
- `two-layer-task-design.md`: the client's example of the data's real structure (time to an event with people who left
  early treated as censored) and of validating a forecast on data it was not built on (the rival rejected on January
  2026).
- task156 in this lane (the same pairing, four builds back): a volunteer pool's retained capacity; this build's cohort is
  a supply-side user cohort's resurrection, and the stump is the leading edge, not a binding capacity.

## Default path
1. Read finance's email and the guarantee terms: the expected total for the window, $350 to every eligible driver who
   completes 40 trips between 00:00 Monday 4 January and 23:59 Sunday 31 January 2027 (Central time), accounts approved
   by Sunday 3 January, drivers who are not on the road today included.
2. Stack the warehouse extract's two layouts (legacy driver numbers through the crosswalk), and take December 2026's
   roster: every account with a completed trip in December 2026, banded by December trips.
3. Join the 2026 payout run and its late credits (less the fraud recoveries) to December 2025's roster and read each
   band's share of accounts paid; carry each band's share onto December 2026's roster.
4. Add new drivers: the onboarding app's accounts approved by 3 January 2027 (within the 90 days) with no first trip, at
   the share of last year's such accounts the 2026 guarantee paid.
5. Add the drivers away: every account with a trip from January to November 2026 and none in December, at the share of
   last year's drivers away who came back and were paid.
6. Multiply by $350 and round to the nearest $50,000.

Ends on: $1,450,000 (built: expected total $1,444,669, 4,128 drivers, 4,100 to the nearest 100).
Golden: $1,650,000 (built: expected total $1,644,850, 4,699.6 drivers, 4,700 to the nearest 100).

## Stump sentence
Carrying December's roster at last January's qualification shares, adding the onboarding app's approved drivers and
the drivers away at last January's return rate files $1,450,000; the step that lands it there is pricing last winter's
drivers who are not yet back as a pool at last year's return rate, when they are the rest of a wave whose size is the
group's own and whose timing every earlier winter kept, so the part already back on 3 January (1,087 drivers) gives the
part still to come: about 1,200 more drivers inside the window, the wave priced at its own January qualification, and
a fund of $1,650,000.

## Three rules

Task type: retention-cohort-lifetime-value-modeling (Product Analytics), which serves Forecasting & Predictive Modeling in the taxonomy; the setting is a ride-hail platform's supply-side users and its winter guarantee.
Domain test: the deciding quantity is how many of last winter's seasonal drivers come back inside the window, forecast the way product analytics forecasts a resurrecting cohort: the cohort's own early returns developed at the return-timing ratio earlier cohorts showed, rather than a churn or reactivation rate on the users away or a cohort's size at another cohort's rate.
Swap: "how much will a hospital's flu-season retention bonus pay nurses who work ten shifts" keeps a bonus and a threshold but loses the platform's supply-side user cohort recruited through an app campaign one winter, away through the summer in its own trades and resurrecting on those trades' calendar, so the growth-accounting quantity the call turns on (resurrected users by cohort) has no record to be read from.
Layer 1: the dispatch platform migration of July 2024 (legacy driver numbers and online hours to Sunday 14 July, new driver ids and online minutes after, July 2024 in both exports), the migration crosswalk with 38 drivers registered twice on the old platform mapped to one id, months in which a driver went online without completing a trip, the payments system's two payout layouts (the 2025 run in cents from the old payout report), the bank's ACH return report covering every payout from the account (weekly earnings included), the guarantee window on local time over four Monday-to-Sunday weeks against the warehouse's calendar months, an extract run on the Sunday before the window (its January 2027 holds 1 to 3 January), the KPI report published through November on its own definitions, onboarding and payments timestamps in UTC; each is how those systems write their files, and none carries the call (each asserted neutral in checks.py, R2).
Layer 2: estimation_fit, censoring: last winter's seasonal drivers look churned and are a return not yet complete; the choice that flips the call is completing the return wave from its own arrived part at the timing ratio earlier waves kept, not pricing the drivers away at last year's return rate.
Decisive step: size the remainder of the returning seasonal wave inside the window from the part of the wave already back by the funding date, at the ratio of window returns to returns by the same date that the earlier winters' waves showed, and price the wave at its own January qualification.
Not semantics: every field is read correctly on the default path (each driver's months, trips, the crosswalk, the payout file's paid drivers, the terms' window and threshold, finance's estimand); the campaign recruits' empty summer months are complete and correct, and reading them correctly as no trips still leaves the analyst choosing how to price drivers who are away, which the pool rate does wrong.
Not rule application: the terms and the email file the estimand (who is paid, for what, in which window, in expected dollars, to the nearest $50,000); no filed rule says how to forecast who comes back, and executing every filed rule on the default path files $1,450,000.
Analyst test: a strong analyst who stitches the two activity layouts through the crosswalk, reads the terms and finance's email correctly, carries December's roster at last January's qualification shares by December trips, adds the approved drivers without a trip at last year's share and the drivers away at last January's return rate files $1,450,000; only sizing the returning wave from the part already back, at the ratio earlier winters showed, and pricing the wave at its own January qualification files $1,650,000 (executed in checks.py on the generator's clean truth: R3a $1,450,000, R3b $1,650,000, every single lower correction wrong).
Estimand: finance's funding email (Kathy Sherman to Gary Mathews, 30 December 2026) and the 2027 guarantee terms file the population (every eligible driver who completes 40 trips in the window, eligible meaning an account approved by 23:59 on Sunday 3 January 2027, whether or not on the road at the as-of, returning and new drivers included), the outcome ($350 each), the window (4 to 31 January 2027, Central time), the unit (the expected total in dollars, returns and recoveries left out) and the rounding ($50,000 steps); there is no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or prior funding request states a fund figure or argues a method; the KPI report answers its own question (monthly supply to November) and ranks nothing; the 2025 rental programme is a real event in the history, there as history.
No certified replay: no shipped figure is reproduced to recover a method; the payout files are closed outcomes that every method reads alike, and the back-test on January 2026 is the analyst's own validation, not a published control set.
Lesson: a model learns that a reactivation wave already under way at the forecast date carries its own size in its leading edge, that a return rate measured on last year's away pool does not transfer to a pool whose makeup changed, and that a cohort recruited for a season is censored, not churned, until its season comes round; no build on file reads a returning group's size off its own early returns at a stable timing ratio.

## Readability screen
Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Figures are built (generator/calc.py, asserted in checks.py).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 December's roster at last January's shares by December trips, the approved drivers without a trip, every account with a trip from January to November and none in December at last January's return-and-qualify share ($1,450,000) | the terms and the email name the window and the drivers paid, which invites carrying last January | the activity extract and the 2026 payout file carry December trips and last year's paid drivers | yes, the default | the analyst's own back-test: the pool's rate carried a year forward missed January 2025's returns by 19 per cent and held January 2026's within 1 per cent, a rate that moves with who sits in the pool; on last winter's drivers alone it missed by 14 and 16 per cent | no | yes, one rate | readable |
| R1 the same with the pool held to last winter's drivers away ($1,500,000) | no | the extract's months | yes, holding the pool to a visible attribute | the same back-test | no | yes | readable |
| R2a the campaign's recruits at the share of the organic first-winter recruits who came back the next January ($1,450,000) | no | the accounts file's signup channel names the campaign | yes, the analog | the campaign's own December returns run well above the organic recruits' at the same date | no | yes | readable |
| R2b each driver away at the return rate of drivers who last drove in the same month ($1,500,000) | no | the extract's last month before the summer | yes, a rate by a visible attribute | the campaign's bonus drivers stopped in April with its seasonal workers, so the stop month's rate from earlier drivers misprices the campaign | no | no | readable |
| R2c a logistic propensity fitted on the 2026 lapsed pool (recency, tenure, lifetime trips, last January's trips) ($1,450,000) | no | the obvious covariates | yes, the modeller's reflex | the campaign's recruits have no last-January history and sit where the 2025 rental drivers, who never came back, taught the fit | no | no | readable |
| R2d one ratio of January returners to November and December returners over every driver back after a break ($1,550,000) | no | the extract's months | a half-step from the decisive move | its own back-test misses by 10 and 6 per cent in opposite directions (the occasional returners keep no seasonal timing) | no | yes | readable |
| R2e the rest of the wave developed, but the drivers already back priced by their December trips like the rest of the roster ($1,600,000) | no | December trips | a half-step | at the 2026 funding date December-trip bands put the back-by-December drivers' qualifiers at 295 against 350, where their own share a year earlier put them at 354 | no | no | readable |
| R3 (decisive) the returning wave's remainder sized from the part already back by 3 January at the ratio of January returns to November and December returns that the 2024 to 2026 winters kept, the wave priced at its own January qualification ($1,650,000) | no sentence names a wave, a return share, a timing ratio or seasonal workers; the terms define who is paid, not who comes back | no column marks a seasonal driver, a return or a leading edge: the extract carries months and trips, the accounts file a signup channel shared by the campaign's bonus drivers and its seasonal workers alike | no: the reflexes are a pool rate, an analog, a rate by attribute, a fitted propensity | none ships: the payout files are closed outcomes every method reads alike, and no document scores a method | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a group's own arrivals developed at a timing ratio read from earlier groups, then priced segment by segment | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "how much ... need in its account" | the guarantee's expected total for the window (finance's email: the expected total, funded in $50,000 steps) | a cover figure at a high percentile; the main run's cash only | a larger fund; a smaller one | finance's email ("the expected total the guarantee will pay") |
| SF2 | "every driver who completes 40 trips" | each person once, on completed trips in the window (the terms: one guarantee per driver, merged accounts count once) | each account | same call (merged accounts are a handful; asserted) | the terms; same call, asserted |
| SF3 | completed trips | trips the rider completed and paid, net of trips refunded for fraud (the terms) | trips accepted, cancellations included | same call (the golden prices on last year's paid drivers, which the payments system counted on the terms) | the terms |
| SF4 | the window | 00:00 Monday 4 January to 23:59 Sunday 31 January 2027, Central time (the terms) | calendar January; ISO weeks 2 to 5 as in 2025 and 2026 | same call (the golden reads last year's paid drivers, not trip counts; asserted) | the terms |
| SF5 | drivers not on the road today | in: returning drivers and approved drivers who take their first trip during the window are paid on the same terms | December's roster only | $1,350,000 (asserted) | the terms ("open to every driver whose Larch account is approved by 23:59 on Sunday 3 January 2027 ... including drivers returning to Larch after time away and approved drivers who take their first trip during the guarantee") and the email |
| SF6 | the as-of | the extract run on Sunday 3 January 2027, every file pulled that day; the extract's January 2027 holds the 1st to the 3rd | data through 31 December | same call (asserted: the 1 to 3 January returns moved to the window file the same fund) | the extract log; same call, asserted |
| SF7 | the rounding path | the expected total, unrounded, to the nearest $50,000 | each segment rounded first; a ceiling to the next $50,000 step | same call (asserted) | finance's email ("to the nearest $50,000"); same call, asserted |
| SF8 | who qualified last year | the drivers the 2026 guarantee paid in its main run, late credits added and fraud recoveries removed | the main run alone | same call (asserted: the late credits and recoveries are a few dozen drivers and move no bin) | the payments notes; same call, asserted |
| SF9 | "drivers you expect to qualify" | the expected number of persons who complete 40 trips | accounts paid | same call | the terms (SF2) |
| SF10 | the guarantee's terms across years | $350 at 40 completed trips over the four weeks from the first Monday of January, unchanged in 2025, 2026 and 2027 | a change between years | none on file | the 2025 and 2026 payout files and the 2027 terms |
| SF11 | last winter's drivers | drivers with a trip in January to March 2026 and none from May to October 2026 | trips in December to March; trips in January to April; no trip June to October; a row rather than a trip | same call (asserted: the definitions select the same wave within eight drivers and file the same fund and drivers) | C1, asserted |
| SF12 | the drivers the guarantee can pay | accounts approved by 23:59 on Sunday 3 January 2027 (the terms, as in 2025 and 2026; 73 drivers who completed 40 trips in the 2026 window on accounts approved later were not paid) | every driver who completes 40 trips, however late approved | about 80 more drivers, 4,800 to the nearest 100 | the terms ("Accounts approved from Monday 4 January take part in the next guarantee.") and the prompt's "every eligible driver" |

## Ladder
Built figures from `generator/calc.py`, every row asserted in `generator/checks.py` (LADDER, OOS, R3b). Each fund is
the expected total at $350 a qualifying driver, to the nearest $50,000.

| Rung | Construction | Fund | Dies to |
|---|---|---|---|
| R0 default | December's roster at last January's shares by December trips, the approved drivers without a trip at last year's share, every account with a trip from January to November and none in December at last January's return-and-qualify share | $1,450,000 (expected $1,444,669) | its own back-test (the pool's rate carried a year forward missed January 2025's returns by 19 per cent, held January 2026's within 1 per cent: it moves with who sits in the pool); on last winter's drivers alone the rate missed by 14 and 16 per cent; the campaign's returns already in hand |
| R0b one ratio, last January's paid accounts over December 2025's roster, on December 2026's roster | $1,350,000 | the returning wave is not on any December roster in proportion; the terms pay drivers not on the road |
| R1 the pool held to last winter's drivers away | $1,500,000 | the same back-test |
| R2a the campaign's recruits at the organic first-winter recruits' next-January share (0.204 against 0.221 for the pool) | $1,450,000 | the campaign's own December returns |
| R2b a return rate by the last month driven before the summer | $1,500,000 | the campaign's bonus drivers stopped in April with its seasonal workers |
| R2c a fitted propensity on recency, tenure, lifetime trips and last January's trips | $1,450,000 | the campaign's recruits sit where the rental drivers taught the fit |
| R2d one January-to-November-and-December ratio over every driver back after a break | $1,550,000 | its own back-test misses by 10 and 6 per cent in opposite directions |
| R2e the rest of the wave developed, the drivers already back priced by December trips | $1,600,000 | the back-test of the back-by-December drivers' qualification (bands 295, own share 354, actual 350) |
| R3 decisive | the returning wave's remainder sized from the 1,087 back by 3 January at the ratio the 2024 to 2026 winters kept (1.086: 923 January returns for 850 back by December), the wave priced at its own January qualification (92.8 per cent back by December, 82.0 per cent of January's returners), everyone else on December's roster by December trips, the other returners (26) and the approved drivers (195 at 14 of 174) at last year's | $1,650,000 (expected $1,644,850; 4,700 drivers) | golden |

**Position and margins.** The golden is the extreme cell: every rung files less. The default path is 4.0 bins of
$50,000 under; the nearest rung that skips the leading edge, R2d, 1.96 bins under; every other such rung 3 bins or
more. The half step R2e (the decisive development without the wave's own pricing) is 0.58 bins under and rounds one bin
down, $1,600,000; it dies to its own back-test.

**Convergence (C1, asserted).** Fourteen constructions of the golden file $1,650,000 and 4,700 drivers (4,688 to
4,703 drivers): the timing ratio read from 2026 alone, 2025 and 2026, 2024 to 2026 pooled or as the mean of the three;
the wave on January to March, December to March or January to April trips, May to October or June to October blanks,
trips or rows; December's non-wave roster in tens, in the six golden bands or in twenties; the wave's January
qualification from 2026 or 2025 and 2026 pooled; the other returners as a count or a rate; the new drivers as last
year's count or on every new qualifier; second accounts dropped. The golden sits 0.40 of a bin from the fund's edge
and 0.49 from the drivers'; one sigma of the timing ratio (0.0516, binomial on the 1,773 earlier returns) moves 46
drivers and leaves both rounded figures unchanged; the stated components (about 1,100, about 1.1, about 1,200, about
2,000) hold across every construction and the winters' own spread of the ratio (sd 0.0127). The campaign's size (2,215
recruits) placed the golden mid-bin, a design parameter; the seed was fixed by rule and never searched.

**Worth on the graded quantity.** Seeing the returning drivers at all is worth about $90,000 (R0b to R0); sizing the
wave from its own leading edge rather than from a pool rate, an analog, a stop month or a propensity is worth $150,000
to $220,000 more; pricing the wave at its own January qualification another $29,000.

**Out of sample.** At the 2025 and 2026 funding dates the leading-edge ratio predicted the January returns of each
winter's drivers within 2 per cent (308 against 306, 413 against 405); the previous January's share on the drivers
still away missed by 14 and 16 per cent in opposite directions (263, 469), the 2025 rental programme's drivers sitting
in the 2026 pool and never coming back; the one ratio over every driver back after a break missed by 10 and 6 per
cent. The realised window (simulated past the run, never shipped) holds 4,704 eligible qualifiers: the golden is 0.1
per cent from it, the default path 12.3 per cent under.

**Strength.** P(one strong solver lands) about 0.12: it must see that last winter's campaign recruits are a return not
yet complete rather than churn, that the wave's size is the group's own and cannot be read from a pool rate, an analog,
a stop month or a propensity, that the part already back gives it at the timing ratio earlier winters kept, and that the
wave prices at its own January qualification rather than at December's bands. P(both land) about 0.02 if independent,
under 0.1 with any plausible correlation. The seed was fixed by rule (task number, then the as-of month and day:
1570103) before any data was generated and is never searched.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every driver who completes 40 trips in the window, drivers not on the road at the as-of included | filed (the terms and the email); SF5 |
| 2 | Unit of account | the person, one guarantee each; the expected total in dollars | filed (terms); SF2, SF9 |
| 3 | Attribution window | 4 to 31 January 2027, Central time | filed (terms); SF4 same call asserted |
| 4 | As-of dating | the extract run on Sunday 3 January 2027 | filed (the extract log, every export's run date); SF6 |
| 5 | Version basis | the 2026 payout file as paid, late credits and fraud recoveries applied | SF8 same call asserted |
| 6 | Denominator | each segment's rate over its own drivers on last year's equivalent date | C1 across segment definitions (asserted) |
| 7 | Weighting | none: counts priced at $350 | n/a |
| 8 | Window length | the winters the timing ratio is read from | C1: 2026 alone or 2024 to 2026 the same fund (asserted) |
| 9 | Boundary inclusivity | 40 trips or more | filed (terms) |
| 10 | Rounding path | the unrounded expected total to the nearest $50,000 | filed (email); SF7 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | the returning wave incomplete at the as-of; the extract's January 2027 partial | the decisive step itself (the method, open and forced by the data); SF6 for the partial month |
| 13 | Order of operations | segments priced and summed, then multiplied and rounded | C1 (asserted) |
| 14 | Row order | sums and set membership | C1 |
| 15 | Duplicate resolution | July 2024 in both activity layouts (each holds its own half of the month) | C1: the call's sets read trips as present or absent, the same under either handling (asserted) |
| 16 | Identity normalisation | legacy driver numbers to driver ids through the crosswalk; merged accounts | C1: the wave and rosters read post-migration months; pooled variants the same fund (asserted) |
| 17 | Netting against gross | none on the call (bank returns are Ask A's) | n/a |
| 18 | Dimensional units | trips and dollars; online hours in hours and minutes by layout (not read by the call) | n/a for the call |
| 19 | Code and status semantics | account status and sign-up source | the dictionary; C1: no status read by the golden (asserted) |
| 20 | Integerisation | none before the total | the golden mid-bin with one sigma (asserted) |
| 21 | Clause scope | the terms apply to the 2027 window | filed (terms) |
| 22 | Forward window contents | the drivers who will drive in the window | forecast from the records (the decisive step); no driver file covers the window |

## Literal reader
Executing the prompt, finance's email and the 2027 terms word for word gives the expected total of $350 for every
eligible person (account approved by 23:59 on 3 January) who completes 40 completed trips between 00:00 on 4 January and
23:59 on 31 January 2027, Central time, drivers not on the road on 3 January and approved drivers who start during the
window included, to the nearest $50,000; no shipped sentence says how many drivers will come back or start, so a literal
reader must forecast them; the easy method on the same literal estimand (December's roster and the drivers away at last
January's rates) files $1,450,000, and the fork table leaves no reading under which any rung is the golden.

## Oracles

- The 2025 and 2026 payout files: closed outcomes (who was paid) that every method reads alike; on the wrong path they
  supply last January's rates, and the analyst's own back-test on them rejects the pool rate. No closed window carries
  a 2027 figure.
- The KPI report (monthly supply to November 2026): answers its own question on its own definitions, consistent with
  every method; it holds no December and ranks nothing.
- The onboarding pipeline: the new drivers' base, read alike by every method.
- No control ties only under the golden.

## Ask sheet
**Main call's declared row population:** the warehouse extract's completed-trip column (both layouts, through the
crosswalk), the 2026 main run's and late credits' paid accounts less the fraud recoveries, the onboarding app's
approvals by 3 January 2027 and by 4 January 2026 with their first trip times, the 2027 terms and finance's email.
Device and hazard rows in it: 0 (asserted, DEVICE: the fund computed with the payout events, the bank's return report,
the screening orders and the 2025 run deleted is unchanged to the driver; the call reads no submitted time).

**Ask A. For each of the 2025 and 2026 guarantees: how much of what it paid out never reached a driver, what it cost
net of later runs, bank returns and recoveries, and how many drivers it paid** (6 figures, whole dollars and whole
drivers; the main run and later runs are not asked, they carry no device).
- H18 home: an audit trail of the call's reference outcome, what last year's guarantee actually paid out and whom; the
  fund prices qualifiers, never cash flows.
- Use: the workbook's guarantee table and the deck's second slide (each guarantee from main run to net cost).
- Basis (filed in Payments Operations' payout notes, the owner's voice): "A guarantee's cost is what its runs paid,
  less payouts the bank returned that were never paid out again and less what was recovered; returns and recoveries
  are booked to the guarantee of the payout they reverse, whatever run they land in." and "The drivers a guarantee paid
  are the people who kept a payment: one per person however many accounts, none for a payout returned and never paid
  out again or recovered."
- Primary A1 (D2, the record is the latest accepted): the payments system sends a returned payout again under the same
  payout id once the driver updates their payout details; the bank's return report still lists the return, and the only
  record of the second send is the payout's events (a second `submitted` after `returned`, then `settled`); 104
  guarantee payouts were sent again. Fair: the events log carries every send in order. Silent: the return report is
  complete and true as a list of returns, no adjustment run carries a repayment, and no shipped sentence mentions a
  second send (asserted).
- Hazards: HA1 the 2025 run's amounts in cents (the old payout report; the notes say so), HA2 a 2025 fraud recovery
  booked in the March 2026 run (the basis books it to 2025), HA3 a driver's second account paid in 2026 and merged in
  December, its recovery not yet booked (people through merged_into), HA4 the bank's report covers every payout from
  the account (the guarantee's carry the GUARANTEE entry description and the guarantee's payout ids).
- Stops (built and asserted): S1/S2 every bank return on a guarantee payout netted, the battery's work otherwise right:
  all 6 miss (2025 $28,350 / $873,950 / 2,500 drivers, 2026 $37,100 / $1,017,450 / 2,910, against the golden $12,950 /
  $889,350 / 2,541 and $16,100 / $1,038,450 / 2,966); S3 recoveries booked by run date: both nets miss ($889,700,
  $1,038,100); HA3 accounts for people: the 2026 drivers paid miss; S4 the golden.
- Span: the 2025 and 2026 main runs, the adjustment runs, the bank's return report, the payout events, the accounts
  file, the payout notes (7 files).
- Realism: payment systems send a returned transfer again under its original id after the payee updates their bank
  details, and a bank's return report lists each return as it happened.

**Ask B. For each month from June to October 2026, how many people applied to drive, how many of them were approved and
how many had taken a first trip by 3 January 2027** (15 figures, whole people).
- H18 home: a component of the call's case, the onboarding pipeline that feeds the window's new drivers, read on
  months the call never reads.
- Use: the workbook's onboarding table.
- Basis (filed in Driver Onboarding's counting notes): "A person is counted once, in the month (Central time) of their
  first submission; approved means approved on any of their applications; a first trip is any completed trip on their
  account by the date of the count." and "Someone who applies again after a rejection has a second application but
  stays one candidate with the screening vendor."
- Primary B1 (D8, an anchor on the current record, not the first): the onboarding app keeps one application per
  applicant and overwrites its submitted time when the applicant resubmits after a document is sent back; 2,392
  applications show a submitted time more than a day after the screening order their first submission placed. Fair: the
  screening vendor's order export carries the order placed at each first submission ("Submitting an application places
  the background check order with our screening vendor", the counting notes). Silent: every submitted time is
  complete, valid and earlier than its decision, and nothing shipped says it moves (asserted).
- Hazards: HB1 times in UTC (the basis counts Central time), HB2 people who applied again after a rejection (two
  application ids, one screening candidate).
- Stops (built and asserted): S1 application rows by their UTC submitted month (15 miss); S2 the battery's work
  (Central time, people through the vendor's candidates) on the app's submitted time (15 miss: June 454 / 322 / 274
  against the golden 446 / 313 / 263); S3 the golden.
- Span: the applications export, the screening orders, the activity extract or the applications' first trips, the
  counting notes (4 files).
- Realism: onboarding tools keep one record per applicant and stamp the latest submission; a screening vendor keeps
  each order with its own time.

**The chart** (`guarantee_fund_jan2027.pptx`, slide 2): each guarantee's steps from main run to net cost (main run,
later runs, never reached a driver, recovered, net cost), graded on its content (Ask A's figures) and its parts (both
years, each step labelled with its value, the net marked).

**Hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| Clocks (UTC in the onboarding app, the screening orders and the payout events, Central time in the terms and the notes) | B | B: applications made after 19:00 Central on a month's last day move a month |
| Identity (merged second accounts, people with two applications) | A, B | A: 2026 drivers paid by one; B: people applied |
| Units and layouts (cents in 2025, a return report for every payout from the account) | A | A: the 2025 main run read as dollars; earnings returns netted |

**Referee.** The payout notes' basis and the payout events (Ask A), the screening orders (Ask B); neither hands over a
level.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, both guarantees' never reached, net cost and drivers paid (6) | every bank return on a guarantee payout netted per the basis, recoveries booked to their payout's guarantee, people through merged_into, cents converted | A1 the payouts sent again under the same id | miss |
| B, five months' people, approvals and first trips (15) | Central time, people through the vendor's candidates, the first submission read from the app's submitted time | B1 the overwritten submitted time | miss |

**Mirror sheet.** The mirror stops at R0 or R2d and meets the same devices; it keeps the chart's parts and no Ask A or
B figure unless it cracks a device.

Mirror leakage: 8 per cent of ask weight (design: the chart's parts, about 2 of 25 ask criteria).

Pair ceiling: 32.0 (design: the cracker at 38 + 7 + about 4 of 55 ask points; the mirror at about 5 + 7 + 3). Rerun
from the generated rubric at stage 4.

## Surface screen

`guard.py surface task157` promotes two pairs for adjudication; neither carries a hard tell (no shared file name,
schema, same-seed table or invented name), and `guard.py heart` passes (nearest driver 0.07, task146). For the author,
who alone runs the adjudicated `/clone-check`:
- task156 vs task157 (consecutive numbers): the coarse card axes match (product-analytics x forecasting, decisive gap
  time, `quantity_figure`), each the honest key here; the drivers share nothing (task156 projects a volunteer pool's
  capacity falling below its arrivals of work; task157 sizes a returning cohort's remainder from the part already back
  at a timing earlier cohorts kept). task156 was registered and shipped before this draw, `guard.py check` passed at
  registration with the pairing outside the ban window, and the keys are not relabelled.
- task231 vs task157: gap time, G12 and Gate G forecasting, the same-driver signature, differentiated on the card at the
  draw (task231 reads silent units' exits from mature rounds of a register; here no hazard is fitted, and a returning
  group's size is read off its own leading edge).

## Leak sweep

`leak.py task157 --asof 2027-01-03` returns REVIEW (no LEAK); every line answered:
- Sweep 3, golden figures in the pack (16,100 in a legacy row's online hours; 100, 274, 311, 446 and 500 inside the KPI
  report's columns): coincidences of digits in data cells, none labelled or near a guarantee figure.
- Sweep 3, the call's words in the data notes and the terms: the terms define the guarantee the call funds and the
  notes list the files; neither states a fund, a count or a method.
- Sweep 4, design-note vocabulary in the KPI report, the data notes, the payout notes and the terms (december, return,
  campaign, payout, accounts): the files' own subjects (a month, a bank return, the campaign's signup channel, payouts);
  none names a wave, a return share or a timing ratio (asserted in checks.py, HOW).
- Sweep 9, dates after the as-of: two submitted times in the onboarding export are UTC on 4 January, Central evening on
  3 January before the run; the demand plan's weeks are Q1 2027, a forward plan issued 4 December 2026 (allow-listed in
  checks.py, H16).

## Build record

Stage 3, 2026-10-17. `build.py`: checks 73 run, 0 failed (the three-rules block R1 to R3c on the generator's clean truth,
every SF row SF1 to SF12, the closure axes that can move, the ladder and its back-tests, both asks with stops and
devices, the realism sweep, the input gates and the distractors' deletion test); `verify.py` (pandas, no generator
import) 18 passed, 0 failed; two consecutive builds byte-identical (target, golden, figures.json, submission.md);
`figures_check.py` 0 absent; `voice-check.py` PASS (955 characters); H1 audit clean on the pack and the goldens;
`leak.py` REVIEW, no LEAK; `guard.py validate` clean, `heart` PASS, `surface` two card-level promotions (above);
20 files in 7 formats, the largest the warehouse activity extract at 165,826 rows; distractors
`rider_demand_plan_q1_2027.xlsx` and `driver_referral_bonuses_2026.csv` in `metadata.json`. Invented names checked:
Larch Rides matched no ride-hail or Minnesota operator in a web search; the rental partner, the campaign and the
screening vendor are left unnamed; personas from `guard.py names`.

## Tried and rejected

- Market dilution (riders' January demand is fixed, so returning drivers split a fixed pool of trips and fewer clear 40), worked at the draw: the qualification count needs the hours distribution and a demand forecast stacked on the supply forecast, and the defensible constructions spread wider than any graded bin; dropped before registration.
- A moved threshold with bunching at the old and new lines (the notch response estimated from past windows), worked at the draw: the deciding analysis is a labour-supply response to a notch, honestly economics-econometrics, whose pairing with forecasting task155 holds in the ban window; dropped rather than relabelled.
- The trips-per-driver distribution against the threshold as the decisive step: task151's driver (a stepped payout as the sum of chances from a resampled distribution); kept only as last year's observed rates, never decisive.
- The campaign recruits' type read from when each stopped (an exit-timing reference class): task146's lesson, and the campaign's bonus drivers stopped in April with its seasonal workers; kept only as a rival that misses.
- Holiday drivers (December-only drivers) inside the wave, prototyped: they separate the aggregate KPI route but their share inside each December band changes year to year, which moved every band-priced construction of the golden by up to $140,000 in the prototype; left out of the world.
- A wave timed by each driver's own anniversary, or by weather: neither is what seasonal trades do, and either would make the timing ratio a property of the group; the timing is the trades' common calendar.
- Each seasonal driver's return week fixed once for life (dealt from a profile at entry), built at stage 3: each winter's returners then kept their own mix of weeks, and the January-to-December ratio ran 1.11, 1.01 and 0.97 across the three winters, wider than the fund's bin; replaced by the trades' calendar dealt afresh each winter (which driver returns which week changes, the calendar does not), after which the winters read 1.098, 1.093 and 1.074.
- New drivers priced from the onboarding app's approvals at the as-of, built at stage 3, while drivers approved during the window could still reach 40 trips: the pool-only and every-new-qualifier constructions differed by about $25,000; closed by the terms' eligibility clause (accounts approved by the Sunday before the window, as in 2025 and 2026; 73 drivers who completed 40 trips in the 2026 window on later accounts were not paid), with "every eligible driver" in the prompt.
- Ask A as twelve figures (main run, later runs, returns, recoveries, net, drivers, both years): the main runs and later runs carry no device and hand the strongest response free points; cut to the six device-bearing figures, the chart keeping the full bridge.
- HB3 (an approved applicant whose account was opened under a second email): the applications export carries the driver id an approval opened, so the hazard had no record to live in; dropped.
- Occasional drivers coming back on at 6 per cent a week: they sat in last winter's drivers often enough to swing the June-to-October-blank construction by $13,000; raised to 15 per cent a week (shorter breaks, fewer in the winter group), the construction now within $4,000.
- Approvals stamped at any hour, and Sunday decisions moved back to the Saturday: 24 decisions fell before their own resubmission; decisions are now taken on working days in office hours, a Sunday's on the Monday.
