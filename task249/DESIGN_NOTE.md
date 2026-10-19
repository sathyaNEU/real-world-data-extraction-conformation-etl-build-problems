# task249 design note

## Draw

Card `cards/task249.json`, architecture 4 (v1 to v3 in lineage), re-rooted 2026-10-19 at the author's request: after
architecture 3 was spent at stage 4, four candidates were written (handoffs/perssathya.md) and the author chose the
first, Product Analytics on a browser's cookie cap. Verdict: WARN, no BLOCK. Each WARN, answered: repeat.gate_g and
overuse.gate_g (method_or_model_selection, after task269 v2 and in 7 of the last 12): it is the honest label, the
decisive step chooses the comparison pool a replayed rule is applied to; statistical_rigor alone is not legal and no
other mechanism is true of this step. The structural tests are differentiated in the card against task233 (v1, v2),
task458, task256, task262, task267, task465 and task54, each a transported or conditioned rate with another
mechanism. The axis bans were redrawn once before filing, and each replacement is the truer label rather than merely
the passing one: the forcing event from launch_or_rollout (task268) to period_close, because what forces the call now
is the fourth quarter's close (the kit quotes the quarter just closed), not the kit's printing; the decisive pattern
from E to none with G14 first, because G14 (does the pooled rate apply to this pool) is the move itself and pattern E
is G14's own form. Nearest driver 0.04.

- **Pairing.** Product Analytics / metric-definition-measurement-science, a task type serving Data Quality
  Monitoring, the lane's least used cell (two builds). The object is the health of a published audience metric, each
  local edition's monthly unique browsers counted by the analytics tag's cookie; the call is a monitoring decision:
  which editions' figures go into the 2029 media kit with the measurement note the group's audience policy requires
  when a figure overstates the edition's browsers by more than a fifth.
- **The seed.** DQ22 gave only the objective (which monitored units fail a quality tolerance); its world and its
  pitfall are not carried.
- **Niche.** A German regional newspaper group publishes twelve local editions on one website with a metered
  paywall: five metered articles a calendar month free, then a registration wall for a free reader account; print
  subscribers activate digital access with their subscriber number. The analytics tag keeps its identifier in a
  first-party cookie written from the page's script and refreshed on every page view. WebKit browsers (Safari on a
  Mac, and every browser on an iPhone or iPad) shorten a script-written cookie to seven days from its last write, so a
  reader who comes back after more than seven days arrives with a new identifier and is counted again that month. The
  paywall keeps its meter in the same kind of storage.
- **The call.** Which editions' average monthly unique browsers for October to December 2028 carry the measurement
  note in the 2029 media kit (the policy's tolerance: the reported figure above the edition's browsers by more than
  20 per cent).
- **Shape.** 10, a scorecard: each of the twelve editions' estimated browsers and overstatement against the
  tolerance, the list, the count, and the asks; over 25 criteria. Decision designation_set, answer set_of_items,
  question form which.
- **Strategy.** causal_design: the conditioning set of a transport, attributes the cap cannot change in, the cap's
  own consequence out. G14 decisive (does the replayed reset rate of browsers whose cookies persist apply to the
  capped pool), G6 supporting (print subscribers, who read online weekly and skew to Apple devices, shift the pools'
  composition), G16 supporting (which comparison pool the replay runs on); gap population (which browsers stand in for
  the capped ones); Gate G method_or_model_selection; calibration gold_standard_subsample (the reader-account service's
  device register, exact browser identity for signed-in readers); context artifact monitoring_export (the analytics
  platform's monthly report); Layer 2 family estimand_identification, pattern
  own:transporting-revisit-behaviour-across-a-cookie-cap-conditioned-only-on-what-the-cap-cannot-change.
- **Forum, event, organisation.** customer_or_counterparty (advertisers buy on the kit's figures), period_close (the
  quarter just closed), media_or_publishing. Role compliance_or_audit (the head of audience data certifies the kit's
  figures).
- **People** (`guard.py names --geo Germany --seed 249`, locale de_DE): Nadin Schleich, head of audience data, who
  asks; Karl-Hans Schenk, web analytics engineer; Eugenia Oderwald, paywall and reader accounts; Almut Ladeck, ad
  sales. None appears in the prompt.
- **Data-native sentence.** The tag counts identifiers, not browsers, and on WebKit an identifier lasts only until
  the reader stays away for more than seven days, so the overcount is set by how readers space their visits, which the
  capped browsers cannot show and the other browsers record in full; but the paywall's meter sits in the same
  capped storage, so on WebKit it resets with the cookie and spares the weekly and occasional readers the
  registration wall their counterparts on other browsers meet, and sign-in, the status that looks like the obvious
  thing to hold fixed, is itself a product of the cap.
- **As-of.** Monday 15 January 2029, after the quarter's close and before the kit goes to advertisers on
  1 February 2029.
- **Sources.** The client's Layer 2 patterns for metric definition (a metric validated against its own measurement
  process; mix shift masquerading as behaviour change); WebKit's tracking prevention (script-written cookies capped at
  seven days since 2019), the measurement practice of replaying an identifier rule on persistent histories, and the
  causal rule against conditioning on a consequence of the exposure. No build on file carries an identifier cap or
  conditions a transport on what the cap leaves untouched (nearest drivers 0.04); task127's unshipped second layer
  and a task194 rejection condition a hospital cohort on an outcome, another construction.

## Default path

Provisional at the draw, measured and named at stage 2 from the simulator.

1. Read the audience policy (unique browsers, the 20 per cent tolerance), the tag's notes (the WebKit cap), the
   monthly platform report and the session export.
2. Count each signed-in WebKit browser once from the reader-account device register.
3. For the signed-out WebKit identifiers, replay the seven-day expiry on the signed-out visitors of other browsers in
   the same edition and device class, and divide.
4. Add the other browsers, average the three months, compare with the reported average.

Ends on: (stage 2).
Golden: (stage 2).

## Stump sentence

(stage 2: the default path's named editions and the step that lands them.)

## Three rules

Task type: metric-definition-measurement-science (Product Analytics), which serves Data Quality Monitoring.
Domain test: the deciding quantity is how many distinct browsers an analytics identifier count represents when one browser family caps the identifier's life at seven idle days, estimated the way audience measurement estimates it: the identifier rule replayed on the visit histories of browsers whose identifiers persist, matched on what the cap cannot change and pooled over what it changes.
Swap: "which of our twelve hospitals' monthly patient counts overstate their patients by more than a fifth" stops making sense: no wristband expires after seven days away while a visit quota stored in the same wristband decides who registers.
Layer 1: the session export's UTC start and end against calendar months in Europe/Berlin across the clock change of 29 October 2028; raw user-agent strings beside the platform's parsed browser field (Chrome on an iPhone parsed as Chrome though it runs on WebKit); a replayed upload batch re-sending sessions under new session ids; the platform's bot and internal-traffic flags and the newsroom's own address range; one edition re-coded on 1 November 2028; account references hashed differently in the device register and the session export; the platform's monthly report for the whole year beside the quarter's export; dates typed as text in the paywall workbook. Each is written by the system named and is neutral to the call (asserted at stage 3).
Layer 2: estimand_identification: browsers counted through a capped identifier are recovered by replaying the cap on persistent histories, and the replay's comparison pool has to be matched on what the cap cannot change (edition, device class, a print subscription activated before any meter ran) and pooled over what it changes (sign-in produced by the meter in the same capped storage).
Decisive step: replaying the seven-day expiry on the other browsers' histories within edition and device class with print subscribers held apart and every other browser pooled whether signed in or not, rather than conditioning on sign-in (or using the signed-in readers' own identifier counts, or ignoring print subscribers).
Not semantics: every field, browser string, clock and rule read correctly (the cap, the meter, the tolerance, which browsers are WebKit) still leaves the choice of comparison pool; the step is that a status the cap itself produces cannot be held fixed, which no field, code or definition states.
Not rule application: the policy files the estimand (distinct browsers per edition and calendar month, averaged over the quarter) and the tolerance, the tag's notes file the cap; nothing files how the capped browsers are estimated, and executing every stated rule leaves the comparison pool open.
Analyst test: a strong analyst who reads everything correctly counts the signed-in WebKit browsers from the device register and replays the cap on the signed-out visitors of other browsers, which understates every WebKit overcount and drops editions from the note (the default path's Ends on, named at stage 2 and asserted in checks.py as R3a).
Estimand: the audience policy's section on unique browsers: for each edition and calendar month (Europe/Berlin), the number of distinct browsers that loaded at least one of the edition's pages, a browser counted once however many analytics identifiers it carried, averaged over October, November and December 2028, against the reported average (distinct identifiers) with a tolerance of 20 per cent.
No decoy: nothing is planted; the platform's report is a correct count of identifiers and says so; no memo, draft or figure argues for a comparison pool.
No certified replay: no published estimate of browsers per edition ships; the note is new in the 2029 policy, so no earlier kit carries one to reproduce.
Lesson: when a measurement cap also changes who ends up in a status, holding that status fixed compares unlike pools; condition the transport only on what the cap cannot touch. No build on file teaches it (task233 transports a nonresponse departure as odds, task458 corrects a trait-selected observation window, task262 a level-selected reliability).

## Tried and rejected

- Drift forecast from the cumulative particle load through an optical PM sensor (drift accrues with dose, not calendar
  time): the lesson is task46's (a rate law stationary only in cumulative service exposure), so the driver is spent.
- Seasonal confounding of a PM sensor's gain by humidity growth or aerosol type: the shape of task248's driver (a
  covariate moving over the year against a level comparison), one build earlier.
- An analyser ask (each analyser's 2027 days over 120 micrograms on the EU maximum daily 8-hour mean): every device it
  carried (span-check hours flagged N, the old analyser's parallel rows) is adjudicated by the station sheet, so the call-landing
  response executes it and keeps every figure; dropped for the node quarter's single silent device.
- Architecture 1 (each node's span read from its spread against the four distant analysers, the paired slope
  attenuated by the sites' partial hourly agreement): the stage 4 reader (medium effort, about two minutes) landed the
  call with an errors-in-variables slope instrumented by the other stations' mean, cued by plan 4's "true ozone
  concentration at its inlet", and kept all 36 ask figures after reading the vendor's firmware note. Regression dilution
  is textbook statistics, so the decisive step is readable to a strong model; and an ask one device deep falls to one
  document read. Realism tells it named: firmware dates cycling in ten-day steps, installation dates on a fixed
  five-week pattern, visit slots on a fixed cadence, the ES4104A analyser's model against its serial (T400 and API400E),
  head serials stepping by 37. The judge's pass on the same bundle: DETERMINISTIC (write-up wording only); its residual
  reading F1, the spread of the four stations' averaged series, gives 10 nodes, so architecture 2's write-up says the
  analysers' hours are pooled.
- Ask A on firmware 4.2's renumbered codes alone, the release note carrying a table of the codes up to 3.7 and from
  4.2: architecture 1's stage 4 reader read the note and kept 36 of 36. The note now gives 4.2's codes only (the records
  show the old meaning: before each node's update its status-1 records are the two warm-up hours after a restart), and
  the restart clocks stand beside it as a second primary, each moving all 36 figures alone.
- The firmware table without a date for OZ19 read as OZ19 never reaching 4.2: the spare's records after the 25 January
  rename lost their humid hours (OZ19 +89 against +18 to +24 elsewhere); OZ19 runs 4.2 from the spare's start at 11:00
  on 9 January, in the solver, the verifier and A1.
- Architecture 2 (each node's span read on the mixed afternoon hours, the hill villages above the night's surface
  layer): the stage 4 reader (Sonnet, medium, about four minutes) landed the call with a regression on the four
  analysers, the 900 m sites' night-time intercepts and the register's altitudes pointing it to the midday hours;
  the judge's pass on the same bundle was DETERMINISTIC, APPROVE, and Ask A held (0 of 36). A site's night-time
  decoupling shows in any residual by hour of day, so the decisive step is readable to a strong model.
- Architecture 3 draw, 2026-10-19, candidates that died before the card was filed: register coverage by dual-system
  estimation within post-strata after erroneous enumerations (task448 already runs capture estimated within route
  strata in the same task type); an adaptive item bank's drift under compromise read with purified anchors (filed as
  drift on the bank's scale, its literal reading is the contaminated thetas, so the estimand forks unless it names
  the purification, which files the method); rapid guessing read from item-specific response-time thresholds (the
  decisive step is a threshold choice, a coin flip in the client's measured runs); this world's forward referral rate
  under the SE-scaled rule (1.645 times the standard error of the difference: the rule's own scaling compresses every
  account into 2 to 9 per cent, too thin for a cap) and a fixed eight-point band (elite accounts at 40 to 60 per cent,
  no firm would adopt it, and a 2028 verification record would let a solver carry each account's empirical shortfall
  forward). The confidence-band rule on the verification score, with the check new in 2029, keeps the spread
  realistic and leaves no per-account history to carry.
- Ask A's highest weekly exposure of any item (four figures): any response that checks the attempts against the
  register keeps it whole, so the ask's weight sat on the one device a careful response can find; replaced by the
  count of items rested for 2029, which the suite moves as well, and the ask cut to five figures.
- Appeal outcomes recorded as later rows of the original case: each case's latest row, the habitual read of a decision
  log, filed the golden, so the impersonation ask carried no device. The desk now logs an appeal as a case of its own,
  as its own sheet would, and a sitting's standing is the latest decision across the candidate's cases.
- The synthetic suite's sittings labelled release 5.3.2 in the week of 3 July, before the release went live: a marker
  isolating the device rows in one week. They now carry the release in service, as the platform stamps every attempt.
- Shrinkage of each pool's top share with each candidate's reported error (Kelley's formula at the estimate) taken as a
  competing reading: it adds NVK, UJB and OJS, but the study's own top tenth of MAT-R scorers refutes it (it predicts
  their MAT-V a tenth of a logit lower than scored) while the shrinkage at the ability, the full posterior and the
  world's own truth all file the 15. Kept as a rung and stated in the write-up's critical components, so a judge sees
  the refutation in the shipped data.
- Architecture 3 (each account's 2029 referral share read through its shortlist's regression to the mean, MAT-R's
  error at the ability and the retest gain at the interval): the stage 4 reader (Sonnet, medium, about eleven
  minutes) landed the call with a latent-ability model (a tier prior deconvolved from the 2028 pool, Table 4.3's
  errors, the study's fitted gain), checked against the study's referral rates by interval and by MAT-R level, and
  kept all 19 ask figures, finding the 6,400 Monday-night identities outside the register, each candidate's latest
  case decision and the fresh booking references from release 5.3.2; the judge's pass on the same bundle was
  DETERMINISTIC, APPROVE. Selection on a noisy score is the textbook regression to the mean, a shrink the author file
  names as a reflex, so the decisive step is readable to a strong model, and three devices one cross-file check deep
  each fall to the hygiene battery. Realism tells it named: round plan counts and shortlist ratios, the suite's
  identical early-Monday timing and short sittings, uniform selection-day spreads, the study's fixed interval grid.
- Candidate 1 as offered to the author (signed-out visitors on other browsers as the comparison for signed-out WebKit identifiers): in a world without a meter it is the golden, and holding every visible status fixed is the careful opponent's reflex, so it would be landed by the first thorough reader; prototyped at the draw (proto3 and proto4 in the session scratchpad), the decisive step moved to what that reflex gets wrong, the sign-in the capped meter produces. A first cut of the print-subscriber skew modelled print readers as daily readers and moved nothing (the skew shifted the device-only route by 0.5 points): daily readers never reset, so print subscribers are drawn as the weekly and occasional online readers a print household is.
