# task174 design note

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** Wave 8, new, Forecasting, seed FC45: a
north-east Pennsylvania gas producer committing, in a 2027 incremental firm-sale agreement with an LNG
feedgas buyer, the gas from wells first turned in line on or after 1 January 2027 and delivered in calendar
2027. Two mechanisms in this world were screened on code, the second at the coordinator's call, and neither
held on measurement. No architecture is live. This note holds the screen record only; it carries none of the
`precut.py` sections, because no design exists. The prototypes stay in the session scratchpad (b174/proto).

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
