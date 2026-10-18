# task202 design note

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** Three grounds screened to death
(human-factors thinned-count and time-on-task, multiple-testing selective inference), and on 2026-10-18 the
designation-set device carried over from task194's architecture 6 was screened against task181 on
human-factors-ergonomics / safety-incident-error-analysis. Six candidate drivers, six kills, all at the
first screen. No architecture is live. This note holds the screen record only; it carries none of the
eleven `precut.py` sections, because no design exists.

## Tried and rejected

### The designation-set device on task181's ground: six candidate drivers, all six already on file (2026-10-18)

The device carried over intact from task194's architecture 6, where it passed the sixth screen twice,
uniqueness on five estimator variants (one set, printed rates 28.4 / 28.6 / 28.7) and all three Gate B
tests. The assignment was to put it on human-factors-ergonomics / safety-incident-error-analysis, screening
against task181 first because task181 holds that domain, that subdomain, that objective and that decision
type. The screen was run as code (`guard.py nearest` on each candidate driver) and then as the abstraction
test on latent structure, default path and correction.

| Candidate driver for the designation set | guard nearest | Killed by |
|---|---|---|
| C1 the rate's real exposure is an opportunity count the pack never publishes, and a forward change multiplies it | **0.11** vs task181 v4 | abstraction: it IS task181 v4, in other nouns |
| C2 the tolerance is crossed by the busiest short window, set by within-period clustering | 0.06 | the dichotomy: a peak is a records-fixed statistic, so computing it is rule application and projecting it returns to C1; and clustered arrivals on an event log is task181 v3's data structure |
| C3 the chance two checks on one item both miss is not the product of their own miss rates | 0.07 | readability test 6: the joint rate is escaped over committed, one group-by; the unobserved version is the banned dark figure |
| C4 a unit's forward count follows its people's experience along a practice curve, not its own history | 0.08 | abstraction: task183 (the unit's events arise in its parts and the parts' own histories beat the unit's rate); and tenure is a visible attribute, which is this number's own earlier death |
| C5 the count is short by a classification lag the record measures about itself | **0.36** vs task181 v2 | a `driver.text` BLOCK, and task181 v2's recorded fate is that no filed criterion choosing the delay history leaves the step silent |
| C6 each candidate's marginal contribution to a set functional, overlapping in the same windows | 0.06 | abstraction: task106 (a set drawing on a shared finite pool, so summing individual sizings overstates the set and admits the wrong members) |

**The guard passes two of the six clones.** C1 scores 0.11 against task181 and C6 scores 0.06 against
task106, both under the 0.12 WARN line, and both are the same driver under the abstraction test on all
three elements. This is the blind spot the skill names (two task500 re-roots passed at 0.05 and 0.08 and
still repeated earlier drivers), measured twice in one pass on this ground. The lexical score cannot see a
mechanism told in other nouns, and on this ground the nouns are very far apart (aircraft levels, hospital
handovers, alarm floods, check failures).

**What the device does and does not supply.** The designation set discretises a free weighting away, which
is real and still holds. It does not supply a driver. The driver still has to come from the data's own
structure, and on this cell every driver a tolerance-exceedance call can carry is on file: three of them
inside task181's own slot (v2 the classification lag, v3 the self-exciting burst, v4 the unpublished
exposure) and the rest in the wider anomaly-detection corpus (task183's parts with their own histories,
task106's overlap under a shared pool, task195's paired screens on shared units).

**I nearly filed a third over-general law tonight and the corpus refused it before I reported it.** The
claim forming was that a designation set against a filed tolerance must decide a forward rate, so the
ground's furniture of counts and hours closes it. Counted on both sides: there are 32 `designation_set`
builds on file, and only 4 are on anomaly-detection (task48, task180, task181, task193). **13 are
data-quality-monitoring and 8 are ETL**, and what they designate is mostly a property rather than a
forward rate: which estimates carry a reliability warning (task230, task240), which series carry a
misclassification flag (task236, task242), which rates get suppressed (task233), which items stay in an
index (task237, task239, task463), which units qualify (task451, task462, task470), which campaigns repeat
another (task84). So the device does not force a rate, and the wall is not the device.

**The structural fact about the cell itself, which is worth more than the six kills.** The assigned cell is
the one spent pairing in this domain. `human-factors-ergonomics` has two builds on file in total
(task181 on anomaly-detection, task256 on descriptive-distribution) and **six never-built pairings**:
forecasting, root-cause, experiment-causal, ETL, opportunity-sizing-decision and data-quality-monitoring.
It also has **four never-drawn subdomains**: usability-task-performance-studies,
workload-fatigue-shift-analysis, human-reliability-assessment and alarm-interface-evaluation. The
compatibility proof that recommended this cell (task181 ships a designation set here) and the clone risk
that killed all six candidates are therefore the same fact: the incumbent is a designation set on this
ground, and it took the natural driver.

**Not run, and why.** The published-adjustment sweep, the sixth screen and the four unspent screens all
take a candidate, and no candidate survived the first one. Screening a driver already on file would spend
the pass on a build that cannot be registered.

### The serial-dependence ground: both channels dead on sign and on a single dial (2026-10-18)

Moved off the human-factors ground entirely (none of the six designation-set kills binds this pass).
New ground: `physical-environmental-sciences` / `environmental-monitoring-exceedance`, the cell task189
holds with censoring at instrument-specific limits. The direction screened was the one an exceedance
call actually turns on in the field: how often a compliant site looks like this by chance, when the
monitored readings are not independent, so the effective number of observations behind a mean, a run or
a control limit is a fraction of the row count. Near neighbours, one line each: task189 spends what each
observation's VALUE is when it is known only as a bound; task186 spends WHICH VARIANCE COMPONENT a test's
reference distribution comes from when units swing in shared local cycles; task191 spends the fact that
SELECTION for being extreme changes the reference distribution, so the family's maximum is the bar.
Mine would have spent how many independent observations one series contains. It does not survive.

**Channel 1, variance inflation (the brief's candidate 1). Dead three ways, measured in
`screen_A_ess.py`.** (a) The pricing test `stumping` Part 3 names fires: of the 36 (rho, m) settings
where the row-count standard error is at least 1.5x too tight, the unit's own level spread is within a
factor of two of the correct standard error in 23, share 0.64, and at every setting that could carry a
ladder (rho 0.8 to 0.95, m 6 to 24, naive 2.0x to 4.1x too tight) the ratio runs 1.05 to 1.81, so the
decisive rung is readable off the series. The escape condition solves exactly: R in [0.5, 2] means
VIF >= m/4, so a naive factor f escapes only beyond m = 4f^2 periods, which is 36 assessment periods at
f = 3. The dial fails at both ends: at rho 0.3 the naive route is only 1.5x wrong, at rho 0.9 the level
spread is right. (b) The run-length form is published at a glance: a compliant pre-change record of 16
periods at rho 0.8 already contains a run of 4 above its own baseline with probability 0.68 (0.79 for a
run of 3), and shape 17's own deliverable prints that table. (c) The sign is wrong and structurally so.
A dependence correction leaves the point estimate identical (+0.006 against +0.006 compliant, +0.977
against +0.977 shifted) and only widens, so it moves a call one way, exceedance to clear: at m 12,
rho 0.8 the naive route calls exceedance in 0.32 of compliant series against the ESS route's 0.14. The
golden is therefore always the hold, and every conservative reflex lands it without the analysis.

**Channel 2, variance bias (the one variant whose sign is right). Dead on the single dial, measured in
`screen_B_percentile_bias.py`.** Under positive autocorrelation the sample spread understates the
process spread, so an upper percentile computed on the record's own spread understates the site's true
percentile and the site looks compliant when it is not: at quarterly sampling and a correlation time of
2.5 years (rho 0.905), E[s]/sigma is 0.574 at n 12 and the percentile lands at 0.704 of the truth. But
the lever (the bias in s) and the noise the same graded percentile carries through the mean of the logs
are both functions of VIF/n alone, and the ratio never reaches 1 anywhere on the range: 0.19 at
VIF/n 0.05, 0.59 at 0.40, 0.89 at 0.70. Over 40 seeds at the most favourable setting the intended
separation (naive below the limit, honest above it) holds in 11/40 at n 12, 10/40 at n 20 and 7/40 at
n 32, and the golden itself runs 0.64 to 2.75 times the limit while the design's truth never moves.
That is task200's death on a different ground.

### Candidate 2, a long-term average over an averaging period the monitors do not produce (2026-10-18)

Dead on the WHAT screen, measured in `screen_CDE.py` section C. On one cut of 30 samples whose spacing
follows a wet-season programme, "the average over the period" reads 45.88 as the mean of samples, 38.61
as the mean of monthly means and 38.64 day-weighted, a spread of 7.27. Those three numbers are three
readings of the estimand's UNIT, which is one of the five parts a decisive step may not settle: name the
unit and the computation follows from the clause (rule application), leave it unnamed and it is a
semantic fork on the main recommendation. task200 measured the same three readings at 12.22, 12.22 and
9.20 and found no third position. It is also task189's shape on task189's own cell, a per-unit average
over measurements against a limit where naive averaging is wrong.

### Candidate 3, a forward exceedance probability from a declustered tail (2026-10-18)

Dead on the estimator family and on sign, measured in `screen_CDE.py` section D. On three years of
hourly readings at a 12-hour correlation time, 789 readings sit above the 97th percentile. The
declustered event rate runs 78.0, 58.7, 48.0, 42.3, 38.7, 34.3 and 29.7 a year across runs declustering
at 1, 3, 6, 12, 24, 48 and 72 hours, a factor of 2.6, and no filed criterion and nothing in the data
separates the run lengths: that is task194's chain-ladder death, several standard variants fitting the
record equally. The graded figure collapses besides, 0.000 expected exceedances of the limit under every
declustering choice against 2.636 undeclustered, so declustering only ever lowers the rate and the golden
is again the clear that every conservative reflex lands.

### Candidate 5, a consented load carried by the complete record (2026-10-18)

The three kills above all pointed the same way, so the fourth mechanism was drawn from what they leave:
a quantity whose estimator is forced by the data rather than by a variance. A works' consented monthly
load, concentration on a routine grab programme, flow and turbidity logged every 15 minutes, the mass
carried in wet-weather events the schedule never sees. The sign is right and the lever is large: across
40 simulated years the grab mean times the volume files 0.510 of the true load (sd 0.240) and on the cut
year 0.376, with 32 to 63 per cent of the load in the wettest 1 to 5 per cent of the record. It dies on
the same dial at both ends, measured in `screen_E2_ladder.py`, `screen_E3_ladder.py` and
`screen_E4_ladder.py`.

- With the calibration window narrow (campaign turbidity 3.8 to 30.2 NTU against a record reaching 272),
  the honest variants are extrapolating by a factor of nine and spread 910.5 kg in the decisive month,
  cross the consent in 2 of 18 months, and name the qualifying run's start month as 13 under one variant
  and None under three. Fitted on daily composites and applied to 15-minute values the "honest" route
  lands at 0.567 of the truth, BELOW the rung above it (turbidity calibration on the grabs, 0.748).
- With the campaign placed in the record's wettest six weeks so the calibration interpolates, the fork
  closes and the decisive rung becomes worthless: the turbidity calibration fitted on the ordinary grabs
  lands at 0.961, 0.968, 0.995 and 0.935 of the truth against the campaign-fitted route's 0.964, 0.944,
  0.988 and 0.917 over four seeds. A surrogate calibration does not care which subset of the record it is
  fitted on, because it is a physical relationship and not a schedule artefact. 0/5 seeds satisfied all
  four pass conditions (honest variants within 8 per cent, no month straddling the consent, one run-start
  month across variants, every other route naming something else).
- The corpus had it already, and `driver.near` could not see it: **task452 architecture v1** is this
  driver verbatim in other nouns ("a period total of the product of two series, one recorded at every
  interval and one sampled on a few intervals that mostly catch the quiet state"), in this same domain,
  shipped 2026-10-13 and re-rooted at the author's request with the recorded reason that "the decisive
  step (a concentration-discharge rating curve applied to every day of the gage record) is the field's
  standard load method, which careful solvers reach for", its two rejected hardening prototypes being "a
  dense automated sampler, a kinked relation", which is the campaign device above. It scores **0.07**,
  under the 0.12 WARN line, and fires no rule: `guard.py check` BLOCKed the card on `ban.artifact`,
  `ban.org_family` and `test.same_driver_older` and never mentioned the clone. That is the third measured
  instance of this blind spot inside this slot.

### The ground-level finding, which is worth more than a sixth candidate (2026-10-18)

Four structurally distinct Layer 2 mechanisms, five candidates, every one killed with a number, and they
fail in one pattern. On an exceedance call the decisive step is either records-fixed (it decides a
selection, a threshold crossing or which recorded quantity the comparison runs on) or it is an
estimator's output. The records-fixed branch on this cell is held: task189 took censoring at
instrument-specific limits and task245 took non-random gaps in a monitoring record ("a count of periods
above a level over a whole cycle, read from records whose gaps are not random: a recorder fails"), which
was the fifth idea in reserve and is spent by the incumbent. Every estimator-output branch fails on one
of three measured grounds: a dependence correction only widens, so the golden is a hold and conservative
reflexes land it; a correction that moves a point estimate is financed by the same VIF/n that randomises
the graded figure; and a correction forced by a fitted transfer is either extrapolating (the variants
fork) or interpolating (the rung below it lands the golden). The axis reservations do not survive the
window either: `org_family government_agency` and the cell's natural `monitoring_export` artifact both
BLOCK against task170, `gate_g signal_vs_noise_or_hold` is honest only for a hold, and the honest
`method_or_model_selection` on gap `rule` with pattern `none` fires `test.same_driver_older` against
task240. The live question for the next pass is the cell, not the device: this cell needs a records-fixed
decisive step and its two incumbents hold the two that the data supply.

### The pincer test written out, on the coordinator's instruction of 2026-10-18

The instruction arrived addressed to a `grid-reliability-outage-analysis` draw (a restoration-time
distribution, a major-event-day threshold, an index with a definable population, window and unit), which
is `energy-systems-utilities`, not this cell; task202's ground is
`physical-environmental-sciences` / `environmental-monitoring-exceedance` and no restoration time or
major-event rule appears anywhere in its brief or its screens. The pincer test itself is general, so it
is run here on all five candidates. It changes one verdict and hardens four.

| Candidate | The decisive quantity | Estimated, or one of the five parts | Pincer |
|---|---|---|---|
| C1a variance inflation | the number of independent observations behind a mean or a run | **estimated** (a standard error) | passes |
| C1b variance bias | the process spread behind a short record | **estimated** | passes |
| C2 long-term average | whether the average runs over time or over samples | the **unit** | **fails** |
| C3 declustered tail | the rate of independent exceedance events | the **unit**: the run length defines what counts as one event | **fails** |
| C5 load by fitted transfer | the mass discharged past the point in the month | **estimated**; the estimand files to the letter (determinand, point, month, kg) while the transfer stays open | passes |

**The one verdict that changes is C3's, and it hardens the kill.** I had filed C3 as dead on the
estimator family (the declustered rate running 78.0 to 29.7 events a year across runs declustering at
1 to 72 hours, a factor of 2.6) and on sign. The pincer says that fork is a *symptom*, not the disease:
the declustering run length is what fixes the unit of the count, no parameter-free reading fixes it, and
task192 architecture v1 is the recorded death on exactly that shape ("count the processes behind the
bursts, not the bursts", the unit of the count). So C3 is not revivable by filing a selection criterion
for the run length: filing it makes the step the execution of a filed clause, and leaving it unfiled
forks the main call, which is the pincer's own both-ends.

**The other direction is just as useful.** C1a, C1b and C5 all pass the pincer, so none of them died on
estimand filing and none is revivable by filing the estimand better. They died on arithmetic the pincer
does not reach: C1a on sign (a dependence correction only widens, so the golden is a hold that
conservative reflexes land) and on the level-spread reflex at 0.64 of live settings; C1b on the single
dial, lever/noise never reaching 1 anywhere on the VIF/n range and the intended separation holding in
11/40 seeds at best; C5 on the same dial at both ends plus task452 architecture v1, which is its driver
in other nouns in this same domain, re-rooted for the reason the screen independently measured.

**No client rigor pattern block on this ground either.** `layer2-rigor-patterns.md` carries 14 domain
sections and `physical-environmental-sciences` is not among them (nor are `energy-systems-utilities` or
`human-factors-ergonomics`), and `environmental-monitoring-exceedance` appears in no block, so
`layer2_pattern` here takes `own:<name>` as task189's card does
(`own:left-censored-results-with-several-reporting-limits`). The warning that travels with that freedom
is the swap test, and the swap was never this cell's problem: every candidate's deciding quantity broke
cleanly on a noun swap. What broke was the decisive step's arithmetic.

**The stop rule stands.** The correction revives nothing. The screen's conclusion is unchanged: this cell
needs a records-fixed decisive step and its two incumbents, task189 and task245, hold the two the data
supply.
