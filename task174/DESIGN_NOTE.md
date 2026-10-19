# task174 design note

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** Wave 8, new, Forecasting. Two worlds have
been screened on this number and neither yields a draw that holds. The first is seed FC45's: a north-east
Pennsylvania gas producer committing, in a 2027 incremental firm-sale agreement with an LNG feedgas buyer, the
gas from wells first turned in line on or after 1 January 2027 and delivered in calendar 2027. Two mechanisms in
that world were screened on code, the second at the coordinator's call, and neither held on measurement (its
prototypes stay in the session scratchpad, b174/proto). The second is the redraw of 2026-10-19 in the cell the
coordinator allocated, education-learning-sciences with the task type learning-analytics-early-warning-models
(it serves Forecasting): twenty-one candidates, two screened on code (`proto13.py` and `proto21.py`, scratchpad
r174) and the rest on the structural screens (a spent driver, the WHAT screen, the swap test, the readability
screen, the library test). No architecture is live. This note holds the screen record only; it carries none of
the `precut.py` sections, because no design exists.

**The structural sentence, and the first thing to read.** Calendar-2027 gas from wells first turned in line
in 2027 is mostly each well's first four to six months. Any difference between the coming wells and the
record therefore either arrives after those months, where it moves the figure by less than the bin the noise
allows, or shows inside them, where the youngest wells of the same design already measure it by a filter and
a divide. The one input with a large lever, each pad's turn-in-line date, rides on a delay process noisy
enough that the cheap routes (a flat two-month slip, the slip pooled over every schedule issue) sit within a
bin of the golden. A draw on this quantity needs a difference between the coming year and the record that is
large in the first months, invisible in the young wells' own months and measured in full somewhere else in
the record; none was found in this world.

**The taxonomy finding.** Upstream production forecasting has no client task type of its own. Energy Systems
& Utilities offers load-forecasting (demand on the system), asset-condition-maintenance (equipment health)
and generation-capacity-planning (Opportunity Sizing only), and none of them is a producer's supply forecast.
Economics & Econometrics' forecasting-forecast-evaluation is a home only where the decisive step is itself a
forecast-evaluation judgment (the spacing driver's rejection of the rival at the depth that matters, or the
as-issued evaluation of a schedule), and the domains README keeps Economics to macro, labour, trade and
fiscal reads, which a producer's own operations are not, so even that home is contestable.

**The early-warning cell finding.** A forward question an early-warning lead faces changes one of three
things, and under this round's constraints each is closed. A change in who is coached (a capacity cut, a
retired alert, a coaching contract that ends) is causal: its lever is large only on the band that loses or gains
coaching (29 to 40 per cent there, 6 to 13 per cent on a cohort's total), a call about that band names the change
and its counterfactual, and the band's uncoached rate from a realistic no-contact holdout carries a sigma of 2 to
3 per cent. A change in what the alert outputs (its cadence, its week, its threshold, its model) replays exactly
on the history's own scores, or, where the history's later scores were themselves lifted by the old alert's
coaching, shows that as a step of five to eight sigma in the faculty-by-year series and moves the figure only 11
to 17 per cent. A change in who arrives is composition, out for this round. The shapes that held in today's blind
reads (a cap that truncates waits, a calendar-locked wave, a gain on each unit's own baseline) have their nearest
early-warning forms already spent (task172, task162, task165, task170), and each of the cell's four cards is the
textbook route those readers take.

## Tried and rejected

- **Spacing interference as the decisive step** (the seed's eight-well pads at 660 ft against the 1,000-ft
  type curve), killed at stage 1 on measurement (prototypes `lever.py`, `screen_common_exposure.py`). The
  prototype is self-similar drainage between parallel laterals: a mixture of slab solutions over a spread of
  diffusivities, a managed 60-day plateau, and EUR at 660 ft between 0.63 and 0.73 of 1,000 ft. It ran on
  three 2027 turn-in-line schedules (front-loaded, even, late). The lever and the common-exposure subset are
  one dial. When the onset is late enough that the 2026 eight-well pads' four observed months show under
  2 per cent (S(4) of 0.98 or more), the 1,000-ft curve over the 660-ft curve on calendar-2027 volume is
  only 1.01 to 1.065. A lever of 1.08 to 1.17 needs S(4) between 0.72 and 0.92, which those pads show in
  their own months. Their own months, filtered and divided with the last month's ratio held, then land at
  1.024 to 1.072 of the golden with four observed months and 0.995 to 1.016 with six, and a linear
  extension of the trend lands inside the bin. Where the lever is buildable (1.08 to 1.14), golden over
  default is 0.88 to 0.93, so a flat 10 per cent haircut lands. Clearing 10 and 20 per cent together needs
  about 0.85, which only comes with S(6) near 0.57, not a plausible Marcellus first year. Older 660-ft
  pilots made unrepresentative by a different completion design do not escape: they change which subset the
  filter reads, not the lever that dial caps. Parent-child moves only the one or two edge wells of an
  eight-well pad, 3 to 10 per cent at pad level.
- **The turn-in-line forecast read against the completion group's schedule as issued, at each pad's lead
  time, against the slip read off the revised schedule** (economics-econometrics
  forecasting-forecast-evaluation, the client's real-time-vintage technique), screened at stage 1 and not drawn (prototypes
  `vintage_proto2.py` to `vintage_proto5.py`, seeds 174 to 176 fixed before outcomes).
  - It passes three screens:
    - the repeat screen: no card spends an as-issued evaluation, and the nearest precedent is the client's
      capital-grant drawdown exemplar (trap 13, a re-aligned schedule validating itself), whose fix was a
      recovered rule;
    - the method screen: lead windows of half a month to a month and a half, a piecewise or straight
      regression on lead, and the volume at the mean slip against the expected volume all sit within 0.3 to
      1.1 per cent of the golden;
    - the estimand screen: the expected volume against the volume at the mean slip is 0.1 to 0.3 per cent,
      with the last planned date by early September.
  - It fails on the margins the noise allows, and the dial is the same as the spacing driver's. With delays
    accruing 10 days a month beyond four months' lead and 2 inside, the golden's equivalent flat slip is 69
    to 80 days across seeds, and the cheap routes sit close to the golden:
    - a flat two-month slip: +3.7 to +9.0 per cent;
    - a flat three-month slip: -6 to -11 per cent;
    - the slip pooled over every issue: +6.8 to +17 per cent.
  - Sigma over pads is 1.3 to 2.3 per cent, so no bin both clears those routes by a bin and holds the golden
    within one sigma, a quarter-bin from its edges.
  - Only a delay process with gamma shape 4, more regular than drilling and frac delays run, brings sigma to
    0.9 per cent. More long-lead history lowers sigma but pulls the pooled route toward the golden (+2.4 to
    +3.8 per cent at 14 days a month).
- **Redraw of 2026-10-19, education-learning-sciences / learning-analytics-early-warning-models.** Each line is
  one candidate, written when it died; the two measured ones first.
- **An earlier alert this year pulling withdrawals forward without changing the year's total** (loss-reserving
  card 1's settlement speed-up transplanted), measured on `proto13.py` (seeds 174 to 193, 30,000 entrants a
  year, no alert in 2019 and 2020, a week-6 alert from 2021, a week-3 alert in 2026). Development on withdrawals
  to date overstates the year by 43.6 to 85.8 per cent at forecast weeks 5 and 6 (6.4 at week 8). But the field's
  own landmark model at the forecast week (logistic on the entry profile and current engagement, trained on the
  week-6 cohorts' survivors) lands within +4.0 to +7.5 per cent (sd 0.9), the week-6-era Bornhuetter-Ferguson
  within +10 to +16, and the golden is the plain entry-model sum of probabilities (-0.2 per cent, sd 1.3), the
  cell's most textbook route. The claim that re-timing leaves the total alone rests on one past event (the 2021
  introduction, post over pre 0.998, sd 0.009). The library test fails: the golden is card 1's stable-basis
  projection and the cell's own risk model.
- **The week-6 rule replayed on a history whose week-6 engagement the retired week-3 alert's coaching lifted**
  (the 2027 plan retires the week-3 alert; six faculties went live from 2022 to 2025), measured on `proto21.py`
  (seeds 174 to 193, 30,000 a year). The latest-cohort replay undercounts the 2027 referrals by 11.2 to 17.2 per
  cent (the fitted trend by 13 to 20, the last three years by 10 to 15, every year pooled by 5 to 7), short of the
  lever the bar asks. Each faculty's step at go-live is 2.7 to 4.2 points against a year-to-year sd of 0.5, so an
  event study finds it. With a drift of 0.02 a year the golden constructions split (+7.6, +10.7 and +3.9 per
  cent). The golden is the staggered-rollout card's not-yet-treated comparison.
- **The incumbent model's coached referrals depressing its measured precision against a challenger's** (a pick
  between two models at capacity): causal, and the estimand that makes the call determinate has to name the
  uncoached outcome, which sends the reader to the no-contact holdout (readability test 1); a 10 per cent holdout
  puts sigma near 2 to 3 per cent on the band's uncoached rate. On paper.
- **A coaching capacity cut or a coaching contract ending** (the referred band loses coaching): the lever is 29 to
  40 per cent on the band's withdrawals and 6 to 13 per cent on the cohort's total unless the effect is
  ASAP-sized, and a call about the band names the change. On paper.
- **Lead time** (the registry's withdrawal dates trail the LMS last activity, so many hits are flagged after
  disengagement): the step settles the population, withdrawers still active at the flag; filed it is a filter,
  unfiled a fork (the WHAT screen). On paper.
- **Distinct students flagged once scoring goes weekly** (a noisy score, more looks): task170's driver, and a daily
  score history replays the new cadence exactly. On paper.
- **Precision and recall at capacity carried onto a cohort whose base rate moved**: task446's invariant (error
  rates carry, the yield moves). Spent.
- **Withdrawals triggered by first-marks release, re-timed by the next assessment calendar**: a lag timed off an
  event, the class the blind readers landed today, found by an event study and close to task160. On paper.
- **Flags set by each student's phase against their own deadlines** (activity surges before each deadline):
  calendar-locked like task162, and any past alert run at the forward phase is a common-exposure subset. On paper.
- **A withdrawal hazard stationary in teaching weeks, not calendar weeks**: task46's insight (a rate stationary in
  a constructed exposure), and a weekly plot shows the breaks. On paper.
- **Optimistic predicted entry grades plugged into an entry-tariff model**: a field reading; a shift, regression
  calibration and full integration agree within a bin. On paper.
- **Missing at least one of k assessments when k rises from two to four** (heterogeneous miss propensity): the
  common-exposure subset lands it where any history has four assessments, and moments above the second are not
  identified where none does. On paper.
- **Students with at least one fail across their courses** (a student-level frailty): task143's group effect
  shared by the members. On paper.
- **A year-end chronic-absence count in a school district**: task253's and task464's count beyond a cut from noisy
  or regressed values, and a district is local_government. On paper.
- **Spring registration throttled by advising holds** (a booking curve capped by advisor slots): fails the swap test
  (patients and appointment slots read the same), and booking curves landed today. On paper.
- **Real-time against warehouse feature vintages** (courseware events arriving days late): the cell's card 1 plus a
  load-timestamp filter, a field reading. On paper.
- **Distance-learning exam sitters including the previous presentation's deferrers and resitters**: task150's
  members carried plus arrivals plus transfers. On paper.
- **Attendance-rate referrals under a sparser timetable** (a rate over fewer sessions crosses a fixed line more
  often): fails the swap test (staff attendance over fewer shifts reads the same), close to task170, and
  correlation across a student's sessions leaves the noise model open. On paper.
- **Label shift against covariate shift for a mid-year cohort under an outside shock**: the prior correction is the
  robustness card 3 itself, the shock is a dated cause, and the two shifts differ by about 15 per cent. On paper.
- **A retrained vendor model recalibrating to a falling base rate** (fewer referrals at a fixed probability line):
  with the specification filed, refitting replays the retrain exactly (rule application); without it, the
  retrain is a recovered rule. On paper.
- **Mixed-model predictions for new modules at a zero module effect** (the typical module is not the average one):
  the plain pooled logistic already returns the marginal rate, so only a correcting solver goes wrong. On paper.
