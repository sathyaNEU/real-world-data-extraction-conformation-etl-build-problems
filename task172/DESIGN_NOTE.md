# task172 design note

Architecture 1, wave 7 (new), Forecasting lane (sathya8571), numbered from seed FC43. The seed (a technology
company's mobility team quoting, in its benefits portal, the wait within which four in five of next quarter's
work-permit renewals will have their decision) was read at its header and Situation only. Its world, decision and
quantity are kept. Its mechanism (whether USCIS still holds a filer's fingerprints, read off the record) is not used:
the share of renewals that need a new fingerprint appointment is stable across the record and decides nothing. The
pitfall is re-found from how a renewal's wait ends since the automatic extension stopped: a renewal still pending on
the day the filer's current card expires gets an expedite request from the team that day and is decided about three
weeks later, and USCIS now sets fingerprint appointments so far out that most of next quarter's renewals will reach
that day before the review that follows the appointment ends.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task172.json`, architecture v1, registered 2026-10-18T11:34:04Z; `guard.py check` WARN on the registered card (overuse.objective,
   the lane's objective; driver.near 0.13 against task127 v2, differentiated on the card). Nearest drivers: task127 v2
   0.13, task501 v3 0.10, task254 v3 0.07, task148 v2 0.07.
2. Pairing: General Statistics & Data Science (client domain) / `regression-classification-model-diagnostics` /
   Forecasting & Predictive Modeling. The setting is another field's (employer immigration operations), so the swap
   is of the method: the deciding object is a duration model's out-of-sample diagnostic, whether the stage model the
   record supports, with the appointment delay now being set added, still describes renewals that reach the card's
   expiry undecided. Free against the last three registrations (task246 general-statistics x data-quality-monitoring,
   task170 healthcare-delivery x forecasting, task244 survey-research x data-quality-monitoring).
3. Niche: a Bellevue software company's global mobility team quoting, in its benefits portal, the wait within which
   four in five of the work-permit renewals it files from January to March 2027 will have USCIS's decision, now that a
   pending renewal no longer extends the card and USCIS is setting fingerprint appointments about sixteen weeks after
   receipt.
4. Call and shape: the wait quoted from 15 December 2026 for the renewals filed 1 January to 31 March 2027, in months
   to the nearest half month (`quantity_figure`, `date_or_period`, question form what). Shape `other`: the call with
   its critical components, two ask tables on rows the call never reads, and a chart on an ask's quantity; criteria
   counted in `## Ask sheet`.
5. Mechanism keys: gap time (the decided record is about renewals whose appointments came about four weeks after
   receipt; the quote bets on a quarter whose appointments come about sixteen weeks out); decisive generator G3 (for
   most of next quarter's renewals the decision is ended by the team's expedite request at the card's expiry, not by
   the review the record's waits measure), then G16 (which model of the wait the record supports, chosen on the
   renewals rescheduled late since the rule change), G13 (the forward window's appointment delay, which no decided
   renewal met), G17 (censoring); Gate G `method_or_model_selection`; strategy `forecast_method_backtest` (the natural
   fit is wrong out of sample under the new appointment regime, and the honest history chooses the model). Time with
   G16 decisive is spent in four older builds and time with G13 is task162's inside the batch, so G3 leads; the
   choice is honest because the step that decides is who ends each forward wait.
6. Layer 2: `forecast_uncertainty` (model choice on out-of-sample error), pattern
   `own:stage-model-cut-at-each-filers-card-expiry-plus-the-expedite-response`.
7. Furniture: forum `other` (the mobility policy gives the quote to the analytics lead, who publishes it; no meeting
   decides it); forcing event `launch_or_rollout` (the portal's quarterly content release on 15 December); organisation
   family `software_or_platform`; role family `research_desk` (the global mobility analytics lead); context artifact
   `planning_thread` (the team's December thread on the quote); calibration `none`. Each is free against task246,
   task170 and task244, and none takes a value task165 (built, not yet registered) carries: its composition_mix,
   purchase_order_or_contract, register, local_government, operations_director, line_manager_or_team, G14 and
   single-figure are all avoided.
8. Spine: the case system's notice log for every work-permit renewal the team filed from January 2024 (case x notice),
   constructed in the layout of an immigration law firm's case-management export.
9. Deliverables: `q1_2027_renewal_quote.xlsx` (the quote, its components and the ask tables) and
   `q1_2027_expiring_permits.svg` (a chart on an ask's quantity, never on the quote).
10. World: Quillwater Software (invented; no company of that name found), Bellevue, Washington, about 21,000 staff; its
    Global Mobility team files renewals of work permits (Form I-765) for employees whose green-card applications are
    pending (category (c)(9)) and for the spouses of employees in H-1B status (category (c)(26)), about 900 a quarter,
    through its outside immigration counsel. The automatic extension of a pending renewal ended for renewals filed on
    or after 30 October 2025 (DHS interim final rule of that date; a real event, cited only as the company's policy
    states it). Personas from `guard.py names --geo "United States" --seed 172`: Melinda Yang (benefits portal content
    lead), Brandon Zamora (immigration case coordinator), Jasmin Sims (head of global mobility, the policy's owner).
    Barbara Davis and Sandra Weiss were passed over (first names on task460 and task130).
11. As-of: the case system's export pulled on Friday 4 December 2026; the quote goes live on Tuesday 15 December 2026.
12. Sources read for the domain (stumping 1.3): task127 (a delay fusing two concurrent waits, valued by the later of
    two dates; here the stages run in series and the wait is cut at a per-filer deadline, the earlier of two clocks),
    task148 (a queue drained by abandonment, patience estimated over every wait; here no unit leaves), task162 (a
    release-week reach set by a monthly restart burst; no calendar burst here), task153 (a site's draw built segment by
    segment between visits; no segments here), task142 (an upper percentile of a period's total built from arrivals
    and stays; here a percentile of each filer's own wait), task167 (two latent call schedules read from each fund's
    first year; here no latent class decides, the share needing new fingerprints is stable), task130 v2 (a queue rank
    against cumulative supply; no queue order here), task124 (an intervention holding down the analogs' measured
    values; here the forward units meet the intervention far more often than the record's did).
13. Data-native sentence: the deadline lives in a different record from the wait, each filer's current card in the
    HR roster and the team's expedite request in its own case-action log, while the notice log the quote is naturally
    built from carries only USCIS's notices, so the cut shows only where a renewal's decision is laid against the
    expiry of the card it renews, and in the record that happened only on the slowest tail.

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
