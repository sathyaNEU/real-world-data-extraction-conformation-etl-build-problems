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
   last winter's recruitment campaign put about 2,100 drivers on the road in February and March 2026, most of them
   seasonal workers whose return wave straddles the funding date.
4. Call and shape: the guarantee's expected total for the four weeks from Monday 4 January 2027 (`quantity_figure`,
   currency, question form how-much), to the nearest $50,000 (finance funds the account in $50,000 steps). Shape
   `other`: the fund with three critical components, two ask tables on files the call never reads, and a two-slide deck;
   criteria counted in `## Ask sheet`.
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

1. Read finance's email and the guarantee terms: the expected total for the window, $350 to every driver who completes 40
   trips between 00:00 Monday 4 January and 23:59 Sunday 31 January 2027 (local time), drivers who are not on the road
   today included.
2. Stack the warehouse extract's two layouts (legacy driver numbers through the crosswalk), and take December 2026's
   roster: every driver with a completed trip in December 2026, banded by December trips.
3. Join the payments system's 2026 payout file to December 2025's roster and read each band's share of drivers paid;
   carry each band's share onto December 2026's roster.
4. Add new drivers: the onboarding pipeline's applicants approved by 3 January 2027 with no first trip, at the share of
   last year's approved-not-started applicants who were paid.
5. Add the drivers away: every driver with a trip in the twelve months to December who took none in December, at the
   share of last year's drivers away who came back and were paid.
6. Multiply by $350 and round to the nearest $50,000.

Ends on: about $1.55 million (design target, replaced by the built figure at stage 3).
Golden: about $1.70 million (design target).

## Stump sentence

Carrying December's roster at last January's qualification rates, adding the onboarding pipeline's approved drivers and
the drivers away at last January's return rate files about $1.55 million; the step that lands it there is pricing last
winter's seasonal drivers who are not yet back as a pool at last year's return rate, when they are the rest of a wave
whose size is the group's own and whose timing every earlier winter kept, so the part already back on 3 January gives
the part still to come: about 1,100 more drivers inside the window and a fund of about $1.70 million.

## Three rules

Task type: retention-cohort-lifetime-value-modeling (Product Analytics), which serves Forecasting & Predictive Modeling in the taxonomy; the setting is a ride-hail platform's supply-side users and its winter guarantee.
Domain test: the deciding quantity is how many of last winter's seasonal drivers come back inside the window, forecast the way product analytics forecasts a resurrecting cohort: the cohort's own early returns developed at the return-timing ratio earlier cohorts showed, rather than a churn or reactivation rate on the users away or a cohort's size at another cohort's rate.
Swap: "how much will a hospital's flu-season retention bonus pay nurses who work ten shifts" keeps a bonus and a threshold but loses the platform's supply-side user cohort recruited through an app campaign one winter, away through the summer in its own trades and resurrecting on those trades' calendar, so the growth-accounting quantity the call turns on (resurrected users by cohort) has no record to be read from.
Layer 1: the dispatch platform migration of July 2024 (legacy driver numbers and online hours to mid-July, new driver ids and online minutes after, July in both exports), the migration crosswalk with two-account drivers merged, the payments system's two payout layouts (2025 and 2026), the guarantee window on local time over four Monday-to-Sunday weeks against the warehouse's calendar months, an extract run on the Sunday before the window (its January 2027 holds three days), the KPI report published through November on its own definitions, onboarding timestamps in UTC; each is how those systems write their files, and none carries the call.
Layer 2: estimation_fit, censoring: last winter's seasonal drivers look churned and are a return not yet complete; the choice that flips the call is completing the return wave from its own arrived part at the timing ratio earlier waves kept, not pricing the drivers away at last year's return rate.
Decisive step: size the remainder of the returning seasonal wave inside the window from the part of the wave already back by the funding date, at the ratio of window returns to returns by the same date that the earlier winters' waves showed, and price the wave at its own January qualification.
Not semantics: every field is read correctly on the default path (each driver's months, trips, the crosswalk, the payout file's paid drivers, the terms' window and threshold, finance's estimand); the campaign recruits' empty summer months are complete and correct, and reading them correctly as no trips still leaves the analyst choosing how to price drivers who are away, which the pool rate does wrong.
Not rule application: the terms and the email file the estimand (who is paid, for what, in which window, in expected dollars, to the nearest $50,000); no filed rule says how to forecast who comes back, and executing every filed rule on the default path files about $1.55 million.
Analyst test: a strong analyst who stitches the two activity layouts through the crosswalk, reads the terms and finance's email correctly, carries December's roster at last January's qualification rates by December trips, adds the pipeline's approved drivers at last year's start rate and the drivers away at last January's return rate files about $1.55 million; only sizing the returning seasonal wave from the part already back, at the ratio earlier winters showed, files about $1.70 million (to be executed in checks.py on the clean truth and the pack).
Estimand: finance's funding email (Kathy Sherman to driver supply, 2 January 2027) and the 2027 guarantee terms file the population (every driver who completes 40 trips in the window, whether or not on the road at the as-of, new drivers included), the outcome ($350 each), the window (4 to 31 January 2027, local time), the unit (the expected total in dollars) and the rounding ($50,000 steps); there is no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or prior funding request states a fund figure or argues a method; the KPI report answers its own question (monthly supply to November) and ranks nothing; the 2025 rental programme is a real event in the history, there as history.
No certified replay: no shipped figure is reproduced to recover a method; the payout files are closed outcomes that every method reads alike, and the back-test on January 2026 is the analyst's own validation, not a published control set.
Lesson: a model learns that a reactivation wave already under way at the forecast date carries its own size in its leading edge, that a return rate measured on last year's away pool does not transfer to a pool whose makeup changed, and that a cohort recruited for a season is censored, not churned, until its season comes round; no build on file reads a returning group's size off its own early returns at a stable timing ratio.

## Tried and rejected

- Market dilution (riders' January demand is fixed, so returning drivers split a fixed pool of trips and fewer clear 40), worked at the draw: the qualification count needs the hours distribution and a demand forecast stacked on the supply forecast, and the defensible constructions spread wider than any graded bin; dropped before registration.
- A moved threshold with bunching at the old and new lines (the notch response estimated from past windows), worked at the draw: the deciding analysis is a labour-supply response to a notch, honestly economics-econometrics, whose pairing with forecasting task155 holds in the ban window; dropped rather than relabelled.
- The trips-per-driver distribution against the threshold as the decisive step: task151's driver (a stepped payout as the sum of chances from a resampled distribution); kept only as last year's observed rates, never decisive.
- The campaign recruits' type read from when each stopped (an exit-timing reference class): task146's lesson, and the campaign's bonus drivers stopped in April with its seasonal workers; kept only as a rival that misses.
- Holiday drivers (December-only drivers) inside the wave, prototyped: they separate the aggregate KPI route but their share inside each December band changes year to year, which moved every band-priced construction of the golden by up to $140,000 in the prototype; left out of the world.
- A wave timed by each driver's own anniversary, or by weather: neither is what seasonal trades do, and either would make the timing ratio a property of the group; the timing is the trades' common calendar.
