# task172 design note (architecture 2)

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task172.json`, architecture v2, registered 2026-10-31 after a guard check
  (WARN only: the question form repeats task191's).
- **Pairing:** Biomedical & Clinical Research, task type `survival-time-to-event-analysis`, objective Forecasting &
  Predictive Modeling; biomedical x forecasting is a pairing no build has drawn.
- **Niche:** TALON-2, a charity-funded, investigator-led phase 3 trial run by the Kesterton University Cancer Trials Unit,
  randomises patients with extensive-stage small cell lung cancer 1:1 to ravolimab (an investigational immunotherapy)
  or placebo, each with platinum-etoposide chemotherapy. The primary endpoint is progression-free survival assessed by
  blinded independent central review (BICR). The Ashgrove Cancer Research Trust funds the trial in two phases and
  releases the second only if the interim analysis at half the final events keeps the final analysis's conditional
  power at or above 20 per cent (the funding agreement's continuation rule, adopted in the DMC charter).
- **Quantity:** the conditional power of the final analysis, the chance that the stratified log-rank test at 330
  BICR-confirmed events rejects at the one-sided 2.5 per cent level, given the interim data and the arms' progression
  over the follow-up still to come as the interim data show it. Forward facing: the final analysis's events have not
  happened.
- **Decision:** continue to the final analysis (golden) or stop for futility.
- **Shell:** question form whether (a gate), deliverables pdf+csv, opener and rounding sentences drawn under the
  corpus quotas at the prompt stage.
- **Setting date:** the interim data cut, 16 November 2026; the DMC meets on 9 December 2026.

## Tried and rejected

- v1 draft A, the decision at the later of the review and the appointment plus the check (2026-10-18, on paper, never
  registered): the officer's review runs while the appointment waits, so the record's post-appointment time is the
  review's remainder and the forward wait is the later of the review and the new appointment plus the check. Sound
  on numbers (golden 5.5, every uncapped rival a bin or more away) but it is task127's lesson, concurrent waits where
  one change moves the total only by its excess over the other; dropped for uniqueness.
- v1 draft B, the quarter's mix of fingerprint reuse and new appointments read from each filer's capture history
  (on paper): the forward pool mostly needing appointments while the record mostly reused. The abstraction is
  task167's (two latent classes read from each unit's own early record, the forward pool dominated by the slow one,
  `test.same_puzzle` in the batch), and composition_mix is task165's; dropped.
- v1 draft C, the processing front (on paper): the wait set by where USCIS's receipt-order front stands and how fast
  it advances. task130 v2's queue rank against cumulative supply, solved on the portal, and the front's speed is
  estimated to only about a quarter of a bin from the company's own decisions; dropped.
- v1 draft D, the expedites stop and the natural wait is recovered by censoring at the request (on paper): task124's
  driver (an intervention held the analogs' values down and the forward units cannot join it), and the closed record
  would bless the naive method until the forward change; dropped.
- v1 draft E, a staggered rollout of a new process across service centres transported by difference in differences
  (on paper): task136's comparison against the sites not yet treated; dropped.
- v1 draft F, a 2025 episode of longer appointments kept in the record (prototype): its own cohort's 80th percentile
  (5.6 months) sat in the golden's bin, a generic analog that lands; the episode is not built, and the additive stage
  structure is shown instead by appointments rescheduled for an applicant's own reasons.
- v1 reschedules of 25 to 80 days (2026-10-18, world prototype): the common-exposure subset screen (stumping 1.2) killed
  it; decided post-rule renewals with appointment leads of 60, 80, 90 or 100 days or more gave 80th percentiles of 5.43
  to 5.57, each in the golden's bin, a filter and a quantile with no model. Reschedules cut to 7 to 21 days, as the
  card's G13 states (no decided renewal met the forward delay), leave none near the forward exposure.
- v1 expedite response of about three weeks (2026-10-18, world prototype): the constructions straddled the 5.25 edge
  (5.20 to 5.40 against a truth of 5.49), because a decision on an expedite and a decision in the normal course are
  indistinguishable in the record and the record's renewals passed their expiry by less than the response, so the
  response time was not identifiable. A response of about a week, short against that excess, makes every construction
  agree (5.46 to 5.53).
- v1 grading the share pending at expiry to the nearest five or ten per cent (2026-10-18): 0.63 under the golden and
  0.60 under the model sit within two points of an edge; the component is stated as more than half.
- v1 names Quillwater Software and Lindqvist Arceneaux LLP (2026-10-18, house fix H21): edit distance 2 from QuikWater
  (utility billing software) and 1 from Lindquist & Vennum (a former Minneapolis law firm); renamed Sallowmere Software
  (nearest real name Sealmere Limited, distance 4) and Marrowby Teale LLP (no firm of that name found).
- v1 the re-centre rule's first pass, PAPER_MEAN 23 (2026-10-18, rework round 1): carried a generator artifact, a
  request for evidence not yet issued at the team's expedite request still holding the decision back to its response,
  a forward-only floor no record shows; removed, and the rule run again on the whole range.
- v1 PAPER_MEAN 22, the rule's value nearest 5.50 on the process alone (2026-10-18): the constructions that read the
  quarter's category mix sat at 163 to 164 days, 0.11 from the 5.25 edge with one sigma; the rule's own gate, read over
  the range, chose 21 (`## Residual`).
- v1 reschedules of 7 to 21 days for every appointment (2026-10-18, retired at rework round 1): read as tuned to the
  common-exposure screen. Replaced by applicants' reschedules of about one queue length (several weeks to a couple of
  months) before the rule, rare after it (a reschedule past the card's expiry now costs leave, so conflicts go to
  walk-in biometrics), and USCIS's own moves of one to three weeks in both regimes; the subset at the forward exposure
  stays thin (3 since the rule) for that reason, not by a band.
- v1 one appointment share for both categories (retired at rework round 1): (c)(9) renewals reuse the adjustment's
  biometrics far more often; with three in ten sent to an appointment the quarter's category mix enters the forecast
  and widens the family by four days, inside the half month.
- v1 a flat four-week lead for 31 months (retired at rework round 1): the lead now drifts by month and season, differs
  by support centre (the filer's state) and rises about a day a month after the rule, to five weeks by the summer of
  2026, before the autumn's seventeen.
- v1 expedite decisions about a week after every request, 95 per cent accepted, every request on the card's expiry
  (retired at rework round 1): now about 85 per cent accepted, a response drawn around nine days, and a quarter of the
  requests a few days before or after the expiry; the record still reads a week (the response is read on renewals close
  to their own natural decision) and the same week in busy and quiet months.
- v1 option B for the expedite response, a response growing with USCIS's load and estimated forward (2026-10-18, on
  paper): the forward load is a quantity the pack would have to file or the solver choose, a construction fork on the
  main call, and the response growing toward three weeks takes the golden to the 5.75 edge; option A kept (the record
  shows the response held across months of very different volume).
- v1 ask A counting every card in hand (stage 4 round 1, judge NOT_DETERMINISTIC): no shipped text said which card
  counts, which category or which holders are current; GM-07 1.3 and 1.4 now pin each, and the golden is their literal
  execution. Under the pins the roster's category (A5) and the roster's gaps for renewals (counsel's approvals) are
  found by executing 1.4, so the identity device A6 was added beside A1; with every approval record taken and persons
  keyed by ID the cracker still misses five of the six cells.
- v1 the summer 2026 lead rise at 0.9 days a month (round 2, retired): medians of 37 to 41 days in June to August 2026
  raised the share of post-rule renewals expedited on the old lead; held to 0.4 a day (33 to 34 days), the re-centre
  rule run again chose the same value (21) and the margin held (0.128 and 0.214).
- v1 refile packets after Stop work (round 2, generator fault): the world simulated a renewal's packets before it knew
  the employee had left and voided only the receipt, so the mailroom log showed refiles of closed matters, three of
  them Receipted within 30 days of a Q3 2026 rejection (a judge's 17). The world now sends no refile after a stop, the
  first packet already with the mailroom still going out, and the mailroom marks a packet Receipted only where USCIS's
  receipt is on record.
- v1 children's benefits IDs drawn at random (round 2, generator fault): 11 children drew a spouse's dependant ID, one
  of them (D1329430) a card holder of household 925819, which gave a Benefits household that disagreed with Global
  Mobility's; Benefits now never repeats an ID.
- v1 the revision note naming sections 1.3, 1.4 and 2.4 as added in revision 4 (round 2 reader, a mild tell): the
  note keeps only the section 3 rewrite.
- v1 GM-07 1.3 reading "the person Global Mobility took into its care with the household, whether Benefits covers
  her as a spouse or as a domestic partner" (stage 4 round 3, judge SOLUTION_WRONG on September 2027 (c)(26), 769
  against 771): read as excluding the spouses known only by a Benefits ID, it let a judge drop the two spouses whose
  latest card the portal filed under that ID, and "whether Benefits covers her" could be read as taking in Benefits
  spouses never in Global Mobility's care; 1.3 now files the spouse as the one person Global Mobility took into its
  care with the household, however Benefits covers her, and no other dependant, and the golden stands at 771.
- v1 ask devices on the careful path (stage 4 round 4, scored reader 14 of 14 ask figures, `score_reader.py` exit 1):
  the roster's missing first (c)(9) cards sat in the register's approvals, a spouse's two IDs were joined by Benefits
  and GM-07 1.3's one spouse, the applicant-only rejections by the case log's forwarded notices and the applicants'
  own refilings by the register's receipts, every one on the path a careful reader takes once the pins are read;
  re-sited (the tracker's approvals, an employee's I-9 card under a spouse's, an employee's two HR IDs, the
  applicant's own case, the other filings' rejections), the asks, roundings and pins unchanged.
- v1 forwarded copies dated at a fixed offset (round 5 judge, Files/Hygiene, a regularity isolating device rows under
  law 7): every forwarded copy of a biometrics letter was dated receipt plus 12 days, counsel's copy of the same letter
  was not, and the other filing's rejection inherited the fixed date (16 of them exactly 12 days after receipt); now a
  copy carries counsel's date for the notice, or the date USCIS issues it, and the other filing's rejection its own trip.
- Architecture 1 (Sallowmere Software's work-permit renewal wait quote), retired 2026-10-31 by the batch audit before
  any portal result: it was designed before the survivor anatomy gate and its note carries no Actor, Link or Reflex
  line; the decisive cut (the team's expedite request filed at each card's expiry) was a deadline the case log shows
  rather than a quantity the record must be modelled to give, and its stump power was argued from the retired scored
  reader; re-rooted in a new domain so the portal sees one strong build.
