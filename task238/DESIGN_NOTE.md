# task238 design note

Architecture 1, wave 3, seed DQ11 (whether a new survey mode's data can be pooled into the tracker): the seed's world
and quantity only, the pitfall re-found from the data under the 10/10 rules. Survey Research & Official Statistics,
nonresponse, calibration and measurement-error adjustment, Data Quality Monitoring & Alerting. The Morvenna Statistics
Office runs the Morvenna Wellbeing Tracker, a quarterly household survey of one adult per sampled address, collected
telephone-first since 2019 (an advance letter, interviewer calls, a web link in the reminder for households the calls
do not reach). From the fourth quarter of 2027 every sampled address gets a web-first letter instead (complete online,
telephone follow-up for households that have not). Before choosing, the office ran a contact strategy test through
the second and third quarters of 2027: each quarter's issued addresses were allocated at random to the web-first
letter (A) or the telephone-first letter (B), to compare response and cost per complete under the two designs. Once
the tracker is web-first, each quarter's indexes pool online and telephone completes, and an index whose answers
differ by mode moves whenever the quarter's share of completes made online moves. The office's continuity standard
for the web-first tracker sets a mode-mix monitor: when a quarter's web share departs from the reference share by
more than the monitor's band, that quarter's indexes are recalibrated to the reference mix before release. The band
is the widest whole-point departure that moves no headline index by more than its continuity tolerance. The head of
survey methodology sets it before the fourth-quarter estimates are processed.

## Draw

Card `cards/task238.json` (architecture 1, registered 2026-10-17). Guard verdict WARN: overuse.objective (the
objective in 4 of the last 12 builds) is this lane's own objective, the backlog wave being Data Quality Monitoring &
Alerting by assignment.

- **Pairing.** Survey Research & Official Statistics / nonresponse-calibration-measurement-error-adjustment, serving
  Data Quality Monitoring & Alerting. Not banned against the last three builds (task237, task155, task464). The object
  is the health of the tracker's published series through a change of collection mode (whether a quarter's mode mix
  has moved its indexes), the call a monitoring setting.
- **Niche.** Mode effects in a mixed-mode household survey: an interviewer's presence moves self-reports (binge
  drinking and loneliness reported less, volunteering and life satisfaction more), and who completes online is
  self-selected on traits the same questions measure, some of which no field records.
- **The call.** The band, in whole percentage points of the web share, at which the mode-mix monitor runs from the
  fourth quarter of 2027.
- **Shape.** 04, setting one dial: the allowed settings are the whole-point bands, and each headline index's mode
  effect and widest band within tolerance stand behind the setting. Decision dial_setting, answer rate_or_share,
  question form what.
- **Strategy.** causal_design with G14 decisive (the telephone completes' level is not what the web completes would
  have answered by telephone), G16 (the estimator the random letter allocation entitles) and G6 (the two answerer
  groups' mix) supporting; Gate G decomposition_attribution (the web-telephone difference split into the mode's
  measurement effect and who chose the web); calibration none; context artifact close_out_summary (the test's
  close-out); layer 2 family estimand_identification, pattern own:mode-effect-through-a-randomized-contact-strategy.
- **Forum, event, organisation.** executive_team (the office's executive team confirms the band the head of survey
  methodology sets), cutover_or_migration (the tracker's move to web-first collection), research_or_statistics_office.
- **People** (`guard.py names --geo en_NZ --seed 238`): Tania Nicholas, head of survey methodology, who sets the band;
  Bernard Johnstone, the tracker's fieldwork manager, who wrote the test's close-out; Leonard McMurray, data
  processing lead, who keeps the exports.
- **Deliverables.** `mwt_mode_mix_band_2027q4.xlsx` (the band, each index's mode effect and widest band within
  tolerance, and the asks' figures) and `mwt_mode_mix_band_2027q4.png` (each index's widest band against the band
  set).
- **As-of.** 2027-10-20: the test's fieldwork closed 30 September 2027, the close-out is dated 15 October 2027, the
  fourth-quarter fieldwork is under way and its estimates are processed in January 2028.
- **Data-native sentence.** Households choose their mode (under letter A they complete online if they get round to
  it before the follow-up calls, under letter B online only if the calls never reach them), and the households that
  end up online are younger and more often away from home, which is also what moves their answers on drinking,
  loneliness and volunteering; the one contrast in this dataset that no choice shapes is the one between the two
  letters, allocated at random by address, and it moved the web share by only about sixty points.

Sources, one line each (what it teaches; how this build differs):
- Survey methodology on mixed-mode designs (selection effects against measurement effects; the interviewer's presence
  and social desirability; recalibrating to a fixed mode mix to keep a series comparable): the field's frame for the
  quantity and the monitor; here the effect must be read through a contact strategy test run for response and cost,
  not a mode experiment built for it.
- Causal inference on encouragement designs (the Wald estimator, two-stage least squares with the assignment as the
  instrument): the method the design entitles; here it is never named in the pack, and the respondent comparison
  adjusted for every recorded characteristic is the reflex it has to beat.
- Seed DQ11: the world (a tracker adding a mode) and the quantity (each index's mode effect) only; its pitfall
  (ordinal items and polychoric invariance testing) belongs to psychometrics, which task237 holds.
- Spent on this objective (`guard.py mechanisms`): task229 (a convex conversion of a daily mean), task231 (a rate over
  active units with late exits), task232 (transmission from delayed mixed outcomes), task230 (a late channel's net
  classification bias), task228 (variance at the randomised unit), task233 (a missing-not-at-random departure on the
  logit scale), task234 (a source's output from a share a loss cannot move), task235 (a missing event censored until
  its device's next contact), task236 (a capture share against an independent fixed-protocol sample), task237 (the
  trait's share of a score with a wording factor). None reads a channel's effect through a randomized nudge's shift
  in uptake.

## Default path

1. Read the continuity standard: each headline index's mode effect (the difference answering online rather than by
   telephone makes to a household's answers), the mode-mix artefact of a departure (the departure times the mode
   effect), each index's tolerance and the band's rule (the widest whole-point departure keeping every index within
   tolerance).
2. Build the test's completes from the interview export under the test plan's rules (one complete per address,
   partials and late returns out) and score the twelve indexes as the codebook defines them.
3. Estimate each index's mode effect by comparing web with telephone completes, adjusted for age, sex, education,
   region, household size, tenure and employment (a regression with a web indicator).
4. Divide each index's tolerance by its mode effect, take the smallest widest band and round it down to whole points.

Ends on: 3 points (binge drinking binding, its mode effect overstated by the households that choose the web).

Golden: 4 points (binge drinking binding, from each index's difference between the letters divided by the letters'
difference in web share; to be confirmed on the tuned simulator).

## Stump sentence

A competent analyst estimates each index's mode effect by comparing web with telephone completes adjusted for every
recorded characteristic and sets the monitor at 3 points (Ends on: 3 points, binge drinking binding); the step that
lands it there is reading the mode effect off households that chose their mode, when the randomly allocated letters
give a contrast that, divided by the letters' difference in web uptake, sets the band at 4.

## Three rules

- **Task type:** survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment, which
  serves Data Quality Monitoring & Alerting; the object is whether a quarter's mode mix has moved the tracker's
  published indexes, and the call is the monitor's setting.
- **Domain test:** the quantity that decides is each headline index's mode effect, the measurement difference
  between answering online and by telephone for the same households, which survey methodology separates from the
  selection effect of who answers online; here the field reads it from the randomized contact strategy contrast
  through the shift it causes in web uptake.
- **Swap:** with ward admissions or megawatt-hours for answers there is no interviewer whose presence moves a
  self-report, no household choosing its mode, no contact letter allocated at random to read the effect through and
  no mode mix to monitor on a published series; the call stops making sense.
- **Layer 1:** an issued-sample file at address grain and an interview export at record grain, joined by address;
  telephone interviews stamped in local time by the CATI system against web submissions stamped in UTC by the survey
  platform; web submissions after a quarter's fieldwork close kept in the export; households interviewed by telephone
  after they had already submitted online, or the reverse; web break-offs with answers to the early items only; item
  nonresponse codes that differ by mode. Each is how the system that writes it behaves; none is placed to be caught.
- **Layer 2:** estimand_identification: the mode effect identified from the random letter allocation (an
  encouragement design) rather than from the self-selected mode groups, however adjusted.
- **Decisive step:** dividing each index's difference between the two letters' completes by the letters' difference
  in the share of completes made online (the Wald estimator, or two-stage least squares with the letter as the
  instrument), rather than comparing web with telephone completes or taking the letters' difference as the effect.
- **Not semantics:** reading every field, code, timestamp and definition right (completes built under the plan's
  rules, the indexes scored per the codebook, the standard's definition of the mode effect read as written) still
  leaves the analyst comparing web with telephone completes, and that comparison, computed correctly and adjusted for
  every recorded characteristic, files 3 points.
- **Not rule application:** the standard files what the mode effect is, the artefact, the tolerances and the band's
  rule; no rule names an estimator or a comparison group, and executing every stated rule still leaves the
  estimation, where the adjusted comparison files 3 points and the letters' difference 6.
- **Analyst test:** a strong analyst who builds the test's completes under the plan's rules, scores each index as the
  codebook defines it, reads the continuity standard correctly and estimates each mode effect from web against
  telephone completes adjusted for every recorded characteristic files a band of 3 points (Ends on: 3 points, binge
  drinking binding); one who takes the two letters' difference as the mode effect files 6.
- **Estimand:** the continuity standard (`mwt_continuity_standard_2027.pdf`) fixes the population (the contact
  strategy test's completes, both quarters and both letters), the outcome (each headline index as the codebook scores
  it), the window (the second and third quarters of 2027), the unit (index points; the band in whole percentage points
  of the web share) and the comparison (the same households answering online rather than by telephone).
- **No decoy:** nothing is planted: the close-out summary reports fieldwork, response and cost by letter and never a
  mode effect or a band; no memo, draft or briefing argues a band; the published series are the tracker's own
  releases.
- **No certified replay:** no certified or published mode effect or band exists for a method to reproduce.
- **Lesson:** when respondents choose the mode, a contact strategy allocated at random for another purpose is the
  lever: the mode effect is the arms' difference over the arms' difference in uptake, not the comparison of the
  modes' respondents however adjusted, and not the arms' raw difference; no build on file reads an effect through a
  randomized nudge's shift in uptake (task236 reads capture against an independent sentinel sample, task228 the
  variance at the randomised unit).

## Tried and rejected

- A mode change read across rotation groups (the newest groups moved to web first, a difference in differences
  against time in sample): too close to task453's rotating-panel measurement change and to task236's attribution.
- A parallel run of both modes on split samples: calibration form parallel_run_overlap is banned against task464.
- A censored laboratory panel for the quality alert: the defensible estimators for left-censored data spread across
  the bands, so the call forks.
- A sensor errors-in-variables calibration: the regulator's own method is ordinary least squares, which forks
  against an orthogonal regression.
- A paired-difference standard error for the alert: too close to task228's driver (variance at the randomised unit).
- Each index pooled, flagged or given a new series on the same mode effects: the guard's same-puzzle test blocked it
  inside the batch (task465 v1's gap, pattern and decision type), and a three-way band per member repeats task236's
  and task237's output; the decision is cut as the monitor's band instead.
- The seed's own pitfall (ordinal items, polychoric invariance testing across modes): psychometric invariance is
  task237's pairing, banned against the last three builds, and the estimator choice reads as a convention fork.
