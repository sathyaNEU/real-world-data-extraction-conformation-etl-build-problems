# task172 design note

Architecture 1, wave 7 (new), Forecasting lane (sathya8571), numbered from seed FC43. The seed (a technology
company's mobility team quoting, in its benefits portal, the wait within which four in five of next quarter's
work-permit renewals will have their decision) was read at its header and Situation only. Its world, decision and
quantity are kept. Its mechanism (whether USCIS still holds a filer's fingerprints, read off the record) is not used:
the share of renewals that need a new fingerprint appointment is stable within each category across the record (most
(c)(9) renewals reuse the adjustment's fingerprints, most (c)(26) renewals go to an appointment) and moves the quote
only inside its half month. The pitfall is re-found from how a renewal's wait ends since the automatic extension
stopped: a renewal still pending around the day the filer's current card expires gets an expedite request from the
team and is decided about a week later, and USCIS now sets fingerprint appointments so far out that about nine in ten
of next quarter's renewals that need one will reach that day before the review that follows the appointment ends.

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
   pending renewal no longer extends the card and USCIS is setting fingerprint appointments about seventeen weeks
   after receipt.
4. Call and shape: the wait quoted from 15 December 2026 for the renewals filed 1 January to 31 March 2027, in months
   to the nearest half month (`quantity_figure`, `date_or_period`, question form what). Shape `other`: the call with
   its critical components, two ask tables on rows the call never reads, and a chart on an ask's quantity; criteria
   counted in `## Ask sheet`.
5. Mechanism keys: gap time (the decided record is about renewals whose appointments came four to five weeks after
   receipt; the quote bets on a quarter whose appointments come about seventeen weeks out); decisive generator G3 (for
   most of next quarter's renewals that need an appointment the decision is ended by the team's expedite request at the
   card's expiry, not by the review the record's waits measure), then G16 (which model of the wait the record supports, chosen on the
   renewals filed since the rule change that were still pending at their card's expiry), G13 (the forward window's
   appointment delay, which no decided renewal met), G17 (censoring); Gate G `method_or_model_selection`; strategy
   `forecast_method_backtest` (the natural fit is wrong out of sample under the new appointment regime, and the honest
   history chooses the model). Time with G16 decisive is spent in four older builds and time with G13 is task162's
   inside the batch, so G3 leads; the choice is honest because the step that decides is who ends each forward wait.
6. Layer 2: `forecast_uncertainty` (model choice on out-of-sample error), pattern
   `own:stage-model-cut-at-each-filers-card-expiry-plus-the-expedite-response`.
7. Furniture: forum `other` (the mobility standard gives the quote to the analytics lead, who publishes it; no meeting
   decides it); forcing event `launch_or_rollout` (the portal's quarterly content release on 15 December); organisation
   family `software_or_platform`; role family `research_desk` (the global mobility analytics lead); context artifact
   `planning_thread` (the team's December thread on the release); calibration `none`. Each is free against task246,
   task170 and task244, and none takes a value task165 (built, not yet registered) carries: its composition_mix,
   purchase_order_or_contract, register, local_government, operations_director, line_manager_or_team, G14 and
   single-figure are all avoided.
8. Spine: counsel's case-management export of every USCIS notice and case-status event on the renewal matters
   (case x notice), 72,572 rows, constructed in the layout of an immigration law firm's export.
9. Deliverables: `q1_2027_renewal_quote.xlsx` (the quote, its components and the ask tables) and
   `q1_2027_expiring_permits.svg` (a chart on an ask's quantity, never on the quote).
10. World: Sallowmere Software (invented; no company of that name found), Bellevue, Washington; its Global Mobility team
    files renewals of work permits (Form I-765) through outside counsel (Marrowby Teale LLP, invented; no firm of
    that name found) for employees whose green-card applications are pending (category (c)(9)) and for the spouses of
    employees in H-1B status ((c)(26)), about 800 a quarter in the record and about 1,150 in the coming quarter, about
    half of them (c)(9), when the 18-month (c)(9) cards issued from 5 December 2025 first come due. Post-rule (c)(9)
    renewal history does not exist under the real validity rules: a (c)(9) card approved before 27 September 2023 ran
    out by September 2025, so its renewal reached USCIS by spring 2025, and later cards ran five years or, from 5
    December 2025, 18 months, first due in June 2027; the record's (c)(9) renewals are the 2024 and 2025 ones. Two real events are used as the standard and
    the thread state them, never as USCIS's own words: the end of automatic extension for renewals filed on or after
    30 October 2025 (DHS interim final rule of that date), and the 18-month cap on (c)(9) cards approved from 5 December
    2025. Card validities follow the real rules: (c)(9) cards approved before 27 September 2023 run two years, those to
    4 December 2025 five years, later ones 18 months; (c)(26) cards run to the H-4 end date. Personas from `guard.py
    names --geo "United States" --seed 172`: Melinda Yang (benefits portal content lead), Brandon Zamora (immigration
    case coordinator), Jasmin Sims (head of global mobility, the standard's owner); Raymond Navarro appears only as the
    H-1B calendar's author, and the case log carries the coordinators' initials. Barbara Davis and Sandra Weiss were
    passed over (first names on task460 and task130).
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
13. Data-native sentence: the deadline lives in a different record from the wait, each renewed card's expiry in the
    team's register and the team's expedite request in its own case-action log, while counsel's notice export the quote
    is naturally built from carries only USCIS's notices, so the cut shows only where a renewal's decision is laid
    against the expiry of the card it renews, and in the record that happened only on the slowest tail (181 of the
    2,665 renewals filed since the rule change on the old appointment lead, 6.8 per cent).

## Screens (stumping 1.2, as code)

Measured by `generator/ladder.py` and the screens script on the clean world; `generator/checks.py` re-asserts each.

- `guard.py slots --driver` (the card's driver): hits on task127 (concurrent waits, the later of two clocks; already
  differentiated on the card) and task130 (claims-made windows priced by report lag, a different mechanism); the other
  ten slots share vocabulary only (charging, mortality review, trimming, irrigation, garage queues, lead lines,
  collections). No slot records this mechanism dying.
- Dispersion: the decisive quantity is a level (the forward 80th percentile), not a spread; the estimator family is
  closed on the pack, seventeen constructions from 5.39 to 5.53 months, all in the 5.5 bin (the margin rule in
  `## Residual`).
- Variance-only: the decisive step moves the point estimate (7.0 on the default path, 5.5 with the cut), it does not
  widen an interval; of 18 conservative reflexes on the record (buffers, multiples, high percentiles, mean plus sd)
  one lands by coincidence (the record plus 1.5 months) and one more by quoting a 97.5th percentile against the
  standard's four in five.
- Common-exposure subset: one decided renewal filed since the rule attains the forward exposure (appointment leads
  at or past the forward tenth percentile of 96 days), too few to read a percentile from; the honest reason is the
  rule itself, since once a pending renewal no longer extends the card a reschedule past the card's expiry costs the
  employee leave, so applicants' reschedules fall from about one appointment in twenty-two to one in a hundred and
  seventy and coordinators send conflicts to walk-in biometrics. The whole record's nine (filed before the rule,
  their cards extended, so never cut) give 6.8 months. Below the exposure the long-lead subsets since the rule give
  4.7 (42 days or more out, 176 renewals) and 5.1 (56 days, 25); at 70 days or more there are 6. The whole record's
  give 5.0, 5.8, 6.1 and 6.2 at 42 to 84 days. The subset of renewals expedited at expiry lands (5.4), but choosing it
  is the decisive step itself.
- Truncation direction: the record's censoring and the cut both hide the top (open renewals are the recent and the
  long ones; a cut renewal's natural wait runs past its decision), so the forward percentile needs the latent upper
  part, which is the case the screen keeps alive.

## Default path

1. Join counsel's notices to the register, keep each renewal's receipt date, its latest appointment notice and its
   decision, leave out withdrawn renewals, censor open renewals at the export and stopped ones at the stop.
2. The record's own 80th percentile, Kaplan-Meier: 4.0 months (3.98 to 4.11 over every window).
3. Read the appointment notices on the newest receipts: about seventeen weeks out against four to five before, 89
   days more than the post-rule record's median.
4. Add the extra 89 days to the appointment-route waits of the renewals filed since the rule change and take the 80th
   percentile: 6.9 months, quoted 7.0 (the same path reweighted to the quarter's categories gives 6.5).

Ends on: 7.0 months
Golden: 5.5 months

## Stump sentence

A competent solver who sees the fingerprint appointments now being set about seventeen weeks out adds the thirteen
extra weeks to the record's appointment-route waits and quotes 7.0 months (the record's own waits, open cases
censored, give 4.0); about nine in ten of the quarter's renewals that need an appointment will reach the filer's card
expiry undecided, and since the automatic extension ended the renewals pending at expiry have been decided about a
week after the expedite request the team files around the day the card expires, so the quarter's 80th percentile is
5.5 months.

## Three rules

- Task type: regression-classification-model-diagnostics (General Statistics & Data Science), serving Forecasting: the
  call is a forecast whose decisive step is a model's out-of-sample diagnostic.
- Domain test: the forward 80th percentile of a censored duration under the stage model the record supports, chosen by
  how the rival models predict the renewals filed since the rule change that were still pending at their card's
  expiry; the field's estimator is a Kaplan-Meier stage model with the cut at each filer's own expiry.
- Swap: "the wait within which four in five renewals will have a decision" reads with hospital nouns ("the wait within
  which four in five referrals will be seen"), but no referral is cut short at its own card's expiry by a request the
  team files that day, so the swapped task has no deadline to decide it and the call becomes the record's percentile.
- Layer 1: counsel's matter numbers against the register's case references across its April 2025 system change (RN and
  GM, a crosswalk column), dates as text in the earlier sheet, rescheduled appointment notices (the latest stands),
  notices logged days after their date, receipt notices issued days after the received date, renewals stopped when an
  employee leaves, withdrawn renewals, transfers, requests for evidence, card mailing events with carrier re-scans,
  rejection notices with no receipt number in the same export, and the register lagging counsel's notices.
- Layer 2: forecast_uncertainty; the methodological choice is the forward model of the wait, a stage model cut at each
  filer's card expiry plus the expedite response, against the record's pooled percentile and the uncapped stage model.
- Decisive step: recognising that the appointment delay now being set pushes about nine in ten of the renewals that
  need an appointment past their card's expiry, so each of those forward waits ends at the team's request around that
  expiry plus the expedite response, a cut the record shows only on its slowest tail.
- Not semantics: every field, code and date in the pack read correctly (the receipt date, the latest appointment, the
  decision notice, the card's expiry, the case log's expedite requests) still leaves the default path on 7.0, because
  no field says that the forward renewals will be cut; that is a forecast about who ends each wait.
- Not rule application: the standard files what the quote is (filed on the receipt date, the wait to the decision
  notice, four in five, months of 30.4 days, the nearest half month, withdrawn renewals out) and that an employee whose
  card lapses goes on leave; no filed sentence says the team expedites at expiry or how USCIS answers, so executing
  every stated rule gives 7.0 or 4.0, never 5.5.
- Analyst test: a strong analyst who joins the notices to the cases, keeps the latest appointment notice, censors open
  cases, reads the standard correctly and sees the appointment delay now being set adds that delay to the record's
  appointment-route waits and quotes 7.0 months, where the card expiries those renewals will reach first, each
  followed about a week later by a decision on the team's expedite request, put the quarter at 5.5 (5.4 to 5.5 over
  every construction, the quarter's category mix moving it by four days inside the half month).
- Estimand: mobility_renewal_standard.pdf 2.3 and 4.1 to 4.3 (the renewals Global Mobility files in the coming
  quarter, filed on the receipt date, the wait to USCIS's decision notice, four in five, months of 30.4 days, nearest
  half month, withdrawn renewals left out), with the prompt naming January to March 2027.
- No decoy: nothing is planted to be caught; the thread states only that appointment letters run to late January into
  March and that the 18-month (c)(9) cards come due; no memo, draft, briefing or stakeholder figure carries a quote,
  and the team's own posted-time capture is a declared wrong-basis distractor ruled out by its own header.
- No certified replay: the method is not recovered by reproducing a certified or published figure; no prior quote
  ships, and the posted times are USCIS's national figures for another population that no construction reproduces.
- Lesson: when a regime change makes a deadline-triggered intervention binding for most future units, the forward
  percentile is set by the deadline plus the intervention's response, so the stage times laid on the record overstate
  it and the record's own waits understate it; no build on file teaches a per-unit deadline cut, task127's later of
  two concurrent clocks being the nearest.

## Readability screen

| Rung | What the move needs | Pointer in the pack | Verdict |
|---|---|---|---|
| 0 to 1, the posted time to the team's own record | the quote is the team's renewals (standard 4.1) | standard 4.1 | readable |
| 1 to 2, open renewals censored | Kaplan-Meier on the record | none; the field's method | silent |
| 2 to 3, the appointment delay now being set | the newest appointment notices | the thread's appointment letters | readable |
| 3 to 4 (decisive), the cut at each card's expiry plus the expedite response | the register's card expiry, the case log's requests, the decisions a week later | none; the cut is visible only by laying decisions against expiries | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "we file" | received by USCIS (receipt date) | the date the packet left the mailroom | 5.5 (same call) | standard 2.3 |
| SF2 | "January to March 2027" | receipts 1 January to 31 March 2027 | dispatches in the quarter | 5.5 (same call) | standard 2.3, same call |
| SF3 | "four in five" | the 80th percentile of the wait | the median | not a reading | prompt and standard 4.1 |
| SF4 | "USCIS's decision" | approval or denial notice | approval only | 5.5 (same call) | standard 4.2 |
| SF5 | the wait | receipt to the decision notice's date | receipt to the card's delivery | 6.0 | standard 4.2 |
| SF6 | the month | 30.4 days | 365.25/12 days | 5.5 (same call) | standard 4.3 |
| SF7 | rounding | nearest half month, once | nearest month | not a reading | prompt and standard 4.3 |
| SF8 | withdrawn renewals | left out | kept as censored | 5.5 (same call) | standard 4.2 |
| SF9 | renewals stopped on an employee's departure | in the quarter, wait unobserved | left out | 5.5 (same call) | same call |
| SF10 | the two categories | one quote over both | one per category | not a reading | standard 4.1 (the renewals) |
| SF11 | members not yet observed | every renewal received in the quarter, none observed at the export | the renewals already opened | 5.5 (same call) | standard 4.1 (the coming quarter) |
| SF12 | percentile convention | empirical 80th percentile of the simulated wait | interpolated | 5.5 (same call) | same call, mid-bin |
| SF13 | the as-of | the export of 4 December 2026 | the release date of 15 December | 5.5 (same call) | same call, no record after the export |
| SF14 | the latest appointment notice | the latest notice stands | the first notice | 5.5 (same call) | dictionary Codes, same call |
| SF15 | the decision date | counsel's decision notice | the register's decided_on | 5.5 (same call) | the two agree on all 9,245 cases both hold (asserted) |
| SF16 | the quarter's categories | the quarter's own mix (about half (c)(9)) | the record's mix, or the post-rule (c)(26) share | 5.5 (same call) | a construction, not a reading; every construction in the family lands (`## Residual`) |
| SF17 | ask A, "work permits held by" | each person's card approved most recently, held to its last day | every card in hand; the latest-ending card | pinned | GM-07 1.4 |
| SF18 | ask A, the card's category | the category on its approval | the roster's entry | pinned | GM-07 1.4 |
| SF19 | ask A, "current employees" and their spouses | Active on HR's program roster at the export; a spouse while her household's employee is | Benefits coverage; any record of employment | pinned | GM-07 1.3 |
| SF20 | ask B, "within 30 days" | received no later than the 30th day after the notice date | day 30 excluded | pinned, and moot: no refiling lands on day 30 or 31 (asserted) | GM-07 2.4 |
| SF21 | ask B, "filed again" | USCIS's receipt of the renewal | the packet's dispatch | pinned | GM-07 2.3 and 2.4 |
| SF22 | the appointment lead a (c)(9) renewal sent to an appointment meets in the quarter | the support centre's queue now set, about seventeen weeks | the record's (c)(9) lead, about five weeks (5.0) | misconstruction | an appointment is a support centre's slot, not a category's: the October and November lead stands at four to five times the 2025 lead in every state the receipts reached (asserted); no record has a queue by category |
| SF23 | ask A, a domestic partner Benefits covers | the household's spouse | not a spouse (180 / 184 / 755) | pinned | GM-07 1.3 (the one person Global Mobility took into its care with the employee's household, however Benefits covers her; no other dependant is tracked) |
| SF24 | ask A, the household a spouse belongs to where records disagree | Global Mobility's records | Benefits | pinned, and no record disagrees: a child's ID that matched a spouse's was a generator fault, now repaired (asserted) | GM-07 1.3 |
| SF25 | ask A, a card the benefits portal files under a spouse's Benefits ID where Global Mobility's records carry her under another | her card: the household has one spouse, so the two IDs are one person, counted once by her latest card (September (c)(26) 771) | a Benefits-only spouse never taken into care, left out (769, the round 3 judge), or a second person (202 / 200 / 803) | pinned | GM-07 1.3 (the one person Global Mobility took into its care with the employee's household, however Benefits covers her); each of the 897 households with a Benefits spouse ID no Global Mobility record carries has exactly one Global Mobility spouse ID, and the 97 spouses Benefits covers in households Global Mobility never took in hold no card on any record (asserted) |

## Ladder

| Rung | Route | Quote (months) | Rounds to |
|---|---|---|---|
| 0 | USCIS's posted time, latest capture (Potomac, Vermont, Nebraska, the NBC line) | 4.0, 5.0, 3.0, 4.5 | miss |
| 1 | the record's own waits, Kaplan-Meier, all receipts / since the rule / last 12 months | 4.05 / 4.08 / 4.11 | 4.0 |
| 1 | decided renewals only / decided in September to November / mean plus one sd | 4.01 / 4.57 / 4.26 | 4.0, 4.5, 4.5 |
| 2 | default: the new delay laid on the post-rule appointment-route waits / reweighted to the quarter's categories | 6.91 / 6.55 | 7.0, 6.5 |
| 2 | the record since the rule plus the new delay, flat / times the record's appointment share | 6.97 / 5.96 | 7.0, 6.0 |
| 3 | the stage model with the new delay, uncapped / at the quarter's categories | 6.94 / 6.58 | 7.0, 6.5 |
| 3 | renewals with appointments 42 / 56 / 70 / 84 days or more out (whole record) | 5.04 / 5.84 / 6.11 / 6.15 | 5.0, 6.0, 6.0, 6.0 |
| 3 | the same since the rule, 42 / 56 days (176, 25 renewals; 6 at 70 days or more) | 4.74 / 5.11 | 4.5, 5.0 |
| 4 | golden: stage model cut at each filer's request plus the expedite response, the quarter's category mix | 5.39 | 5.5 |
| 4 | the record's own route share / the post-rule share, no category mix | 5.53 / 5.53 | 5.5 (same call) |
| 4 | cut at expiry with no response time / every renewal cut / renewals expedited at expiry | 5.23 / 5.56 / 5.43 | 5.0, 5.5, 5.5 (contain the cut) |
| flag | the record plus 1.5 months / the post-rule 97.5th percentile | 5.55 / 5.33 | 5.5 (no analysis; not four in five) |
| flag | the record (since the rule, or all receipts) plus the new delay times the quarter's appointment share (0.475) | 5.44 / 5.44 | 5.5 (a mean added to a percentile; coincidence) |
| flag | an expedite response assumed at 14 / 21 days | 5.59 / 5.76 | 5.5, 6.0 (the log says a week) |
| misread | the response read from USCIS's reply date / every expedite accepted / the quarter's mix keeping approved adjustments | 5.33 / 5.33 / 5.39 | 5.5 (asserted; none in the family) |

Back-test at depth (the 154 renewals filed since the rule change that were pending at their card's expiry and had an
accepted expedite): decided a median of 7 days after the request, 97 per cent within 14; the uncapped stage model
fitted on the renewals filed before the change predicts a median remaining wait of 20.0 days for them, a mean absolute
error of 14.1 days against 2.8 for the cut model.

## Closure table

| Axis | Name | Reading on this build | Move |
|---|---|---|---|
| 1 | Population | the renewals received 1 January to 31 March 2027, none observed at the export | filed, standard 4.1 and 2.3; the prompt's quarter |
| 2 | Unit of account | one renewal (one receipt) | the standard's renewals; C1 (one receipt per renewal) |
| 3 | Attribution window | the receipt date places a renewal in the quarter | standard 2.3; C1 |
| 4 | As-of dating | the export of 4 December 2026 | the manifest's extract dates; same call to 15 December |
| 5 | Version basis | the latest appointment notice stands | dictionary Codes; C1 (the first notice gives the same call) |
| 6 | Denominator | every renewal received in the quarter, withdrawn ones out | standard 4.2 |
| 7 | Weighting | each renewal once | the standard's percentile over renewals; C1 |
| 8 | Window length | the record's components from every window give one bin | C3 over the lead and card-gap windows (5.39 to 5.40) |
| 9 | Boundary inclusivity | receipts on 1 January and 31 March are in | C1; no forward receipt record ships |
| 10 | Rounding path | once, the quote to the nearest half month | prompt and standard 4.3 |
| 11 | Tie-break | none; one figure | not applicable, asserted single value |
| 12 | Maturity and censoring | open renewals censored at the export, stopped ones at the stop | the field's method (Layer 2), C3 (decided-only gives the same bin) |
| 13 | Order of operations | the cut applies after the natural wait is drawn | the model's structure; C1 |
| 14 | Row order | none | C1, asserted over the export's order |
| 15 | Duplicate resolution | one receipt per renewal; carrier re-scans and repeated appointment notices collapse | C1, asserted |
| 16 | Identity normalisation | counsel's client reference to the register through RN and GM references | the register's legacy_case_id; C1 |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | days throughout, months of 30.4 days at the end | standard 4.3; C3 (365.25/12 gives the same bin) |
| 19 | Code and status semantics | approval and denial notices are decisions; a withdrawal acknowledgement is not | dictionary Codes, standard 4.2 |
| 20 | Integerisation | none in the quote | not applicable |
| 21 | Clause scope | standard 2.3 defines filing for every renewal | the clause's own words |
| 22 | Forward window contents | the coming quarter's appointment delay, from the newest notices, and its categories, from the permits whose renewals reach USCIS in it | the export's appointment notices for receipts from October 2026; the current permits by last day; C3 (the record's mix gives the same call) |

## Literal reader

Executed word for word, the standard defines the quantity (the 80th percentile of the receipt-to-decision wait of the
renewals filed in the coming quarter, in months of 30.4 days, to the nearest half month) and leaves the forecast to
the analyst; no clause names a method, so no literal reading files a number. Every licensed reading of the estimand
(SF1 to SF16; SF17 to SF21 are the asks' pins) gives 5.5 under the cut model, the readings that differ (SF5, the
card's delivery) violate standard 4.2, and the easy answers (4.0 and 7.0) come from easy methods on the same estimand,
never from another reading.

## Oracles

No control ties only under the golden. The manifest's row counts tie under every handling; the register's statuses
and counsel's notices agree whatever model is fitted; no prior quote, scorecard or published figure ships; the posted
processing times are USCIS's figures for all filers, a declared wrong-basis distractor that no construction reproduces;
the thread carries no figure about the wait.

## Ask sheet

Criteria: the quote (1), three critical components (the appointment lead now set, 17 weeks against 4 through 2024 and
2025; about nine in ten of the quarter's appointment-route renewals reaching the card's expiry undecided; the expedite
response, about a week), ask A's six cells (three months by two categories), the chart's six labelled bars, ask B's
eight cells (four quarters by rejected and refiled within 30 days) and the two files: 26.

- Ask A, permits expiring July to September 2027 by category, each current person's permit as GM-07 1.3 and 1.4 pin it
  (the card USCIS approved for the person most recently, in its approval's category, held to its last day; current
  while HR's program roster shows the employee, or the spouse's household employee, as Active). Rows: HR's roster,
  counsel's approval notices, the register's approved filings, the tracker's (c)(9) cards, HR's program roster,
  Benefits' dependants. The call reads the same card records only for the quarter's category mix, and with every ask A
  device left uncracked it moves one day inside its half month (5.43 against 5.39, asserted). Silent devices: A1 (D5, a
  silently partial extract: a fifth of the spouses' renewed cards and a quarter of the derivatives' first (c)(9) cards
  never reach the roster; the renewals are in counsel's approvals, but the first (c)(9) cards, filed with the
  adjustment, are held only by the register's initial filings and the tracker), A6 (a grain of identity: a spouse who
  joined Sallowmere benefits after the household came into Global Mobility's care keeps her MP- person ID on the
  register, the tracker, counsel's matters and her onboarding entry, and the benefits portal files her later uploads
  under the dependant ID Benefits gave her, so one card sits under two IDs; 897 households carry two spouse IDs and
  560 of them share a card to the day, and an employee has one spouse; it moves every (c)(26) cell and July's
  (c)(9)). Documented and pinned: A2 (the household link, Benefits covering only spouses on the plan today, the
  roster's onboarding entry, the register and the tracker carrying the rest; GM-07 1.3 files the spouse as the
  one person Global Mobility took into its care with the household, however Benefits covers her (238 Benefits rows name a domestic partner), and no other dependant), A5 (GM-07 1.4
  names the roster's category as not always the approval's; a spouse who moved from (c)(26) to (c)(9) uploads her new
  card under the category of her first entry), A3 (GM-07 1.4 keeps a permanent resident's last card to its last
  day). Benefits gives every dependant an ID of her own (a child's ID once repeated a spouse's, a generator fault, now
  repaired and asserted).
- Ask B, lockbox rejections October 2025 to September 2026, filed again as GM-07 2.3 and 2.4 pin it (USCIS's receipt
  no later than the 30th day after the notice's date). Rows: counsel's rejection notices, the case log's forwarded
  notices, counsel's receipt notices, the register's receipts, the mailroom's dispatch log; the call reads no rejection
  notice and no dispatch row. Devices: B4 (D4, absence: a fifth of the rejection notices went to the applicant alone,
  since the lockbox did not accept the G-28 on those packets, and reach the team only as a forwarded notice in the case
  log), B6 (D5: about a third of those applicants refiled online themselves, a filing only the register holds), B1 (D2,
  a field overwritten later: from 2 March 2026 the new dispatch system writes a resend over the packet's row), B3 (D5:
  the earlier dispatch system's Returned holds courier returns beside lockbox rejections), B7 (hazard: applicants'
  copies of rejections counsel also holds, under the case reference in use that day). A matter the team closed on an
  employee's departure is never filed again: a packet already with the mailroom when the employee left still went
  out (its rejection stands), but the team sends nothing after Stop work, and the mailroom marks a packet Receipted
  only where USCIS's receipt is on record (both asserted), so the mailroom log adds no refiling to any quarter.

How each ask enters the call (H18): ask A is the population behind the quote's quarter, the permits whose renewals
Global Mobility opens from January to March 2027 under GM-07 2.1 (cards expiring July to September 2027), the
page's recurring chart; ask B is the audit trail of the filing date the quote counts from, the renewal packets the
lockbox returned before USCIS received them (GM-07 2.3) and how fast they were filed again.

Pair ceiling: 33.1 (the strongest response on the call, executing GM-07 1.3, 1.4 and 2.4, joining the roster to
counsel's approvals, linking every spouse and credited with any one more device, keeps at most 4 of 20 ask cells, 20.0
per cent, with the forwarded rejection notices or with the register's filings and the tracker; with a spouse's two
IDs merged 0; the best response off the call keeps none; with both top responses on the call and no device cracked,
44.0)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/cracker.py

| Ask | Cracker sheet (executes every pin, runs the battery, links every spouse) | Hits | Verdict |
|---|---|---|---|
| Ask A, six cells | the roster's cards with counsel's approvals and their categories, current persons by ID through every link | 0 of 6 | miss |
| Chart, six labelled bars | the same counts | 0 of 6 | miss |
| Ask B, rejected, four quarters | counsel's rejection notices by notice date | 0 of 4 | miss |
| Ask B, refiled within 30 days, four quarters | counsel's receipt notices within 30 days of each notice date | 0 of 4 | miss |

## Residual

Re-centre rule, fixed on 2026-10-18 before any outcome of the stage 4 rework was measured: after the realism changes
(the appointment lead's drift, the reschedules, the expedite handling, the (c)(9) fingerprint reuse share, the
paperwork tail), the mean of the main paperwork component (opening to dispatch, in whole days from 12 to 30, its sd a
third of the mean) is set to the value at which the generator's process 80th percentile for the quarter (every
renewal received in the quarter, its own category, state and card gap, the process re-run 200 times) is nearest 5.50
months. No other parameter moves to place the bin. If no value in that range leaves every construction a quarter-bin
from both edges with one sigma, the rework is reported, not loosened.

Applied, in two passes, both on the full range 12 to 30. The first pass picked 23 days (process 167 days, 5.49) with an
artifact in the generator: a request for evidence not yet issued at the team's expedite request still held the decision
back to its response. With the artifact removed, the value nearest 5.50 is 22 (process 5.49), and there the family
fails the margin: the constructions that read the quarter's category mix sit at 163 to 164 days, 0.11 from the 5.25
edge with one sigma. The rule's gate reads over the range, so the family (fixed in `ladder.py` before the scan:
seventeen constructions, the margin taken with the golden's largest one-sigma move) was run at every value: 18, 19 and
21 clear it, and 21 is the one whose process is nearest 5.50 (168 days, 5.53). Adopted: PAPER_MEAN 21. The scan is
`generator/recentre.py` (about forty minutes; exit 0 when the chosen value is the world's). Run again after round 2
held the summer 2026 lead rise to about a week: 18, 19 and 21 clear again, 21 is chosen again (process 5.53), exit 0.

What stays open after the rework, and why each is accepted:

- The record-based constructions sit one to four days under the generator's process (golden 164 days, process 168,
  the realised quarter 167). The record reads USCIS's expedite response on renewals close to their own natural
  decision, so a share of the record's responses are the earlier of the two and the response reads short (median 7
  days against a drawn median of about 9). Every construction carries the same bias, so it does not open a fork, and
  the bias keeps the truth inside the golden's half month.
- The family spans 5.39 to 5.53 (164 to 168 days). Its width is the quarter's category mix: about half the quarter is
  (c)(9), whose renewals mostly reuse fingerprints, against a record nine in ten (c)(26); a solver who ignores the mix
  quotes 5.53, one who reads it 5.39 to 5.46. With one sigma the family runs 5.38 to 5.54, 0.128 and 0.214 from the
  edges; the golden is 4.4 days above the 5.25 line (159.6 days) and 10.8 under the 5.75 line. The margin is
  integer-day: one day is 0.033 months.
- The (c)(9) appointment lead in the quarter (SF22): a judge's one exit (the backlog skipping (c)(9) renewals that
  need fingerprints, 157 days, 5.0) is a misconstruction. An appointment is a support centre's slot: the October and
  November lead stands at four to five times the 2025 lead in every state the receipts reached, and no record keeps a
  queue by category.
- An expedite response assumed rather than measured: 14 days gives 5.59 (lands), 21 days 5.76 (6.0). The case log's
  189 requests say a week, and say it in the busiest request month (September 2026, 60 decided requests, median 6
  days, against 7 in the rest) and after the appointment queue tripled; the forward quarter needs about two and a half
  times the record's busiest month, under the same appointment regime the autumn's ran.
- Coincidental landings, flagged and asserted, none a construction of the family: the record's 80th percentile plus
  the new delay times the quarter's appointment share (0.475), 5.44 since the rule or over every receipt (a mean
  added to a percentile; the record's own share gives 6.0); the record plus 1.5 months (5.55); the post-rule 97.5th
  percentile (5.33). Misreads that land, asserted: the response read from USCIS's reply to the service request
  rather than the decision notice (5.33, standard 4.2 rules it out), every expedite accepted (5.33), the quarter's mix
  keeping the (c)(9) cards of approved adjustments (5.39).
- The long-lead analogs since the rule are thin: 6 decided renewals with appointments 70 days or more out, 1 at the
  forward exposure (96 days or more). Reschedules after the rule are rare because a reschedule past the card's expiry
  now costs the employee leave.
- Ask A's identity device (A6) is a grain the pin forces: GM-07 1.4 counts a person's permit, and an employee has one
  spouse; the 897 households the pack shows with two spouse IDs each carry them for one spouse (asserted against the
  world), and 560 of them share a card to the day across the two IDs, which is the figure that makes per-ID counting
  wrong. A same-day pair of approvals exists for one current person; neither card ends from June to September 2027.
  GM-07 1.3 files the spouse as the one person Global Mobility took into its care with the household, however
  Benefits covers her, and no other dependant (SF23, SF24, SF25).
- Ask A's September 2027 (c)(26) cell is 771 (round 3 judge 769, settled). The two are the spouses of employees
  723523 (MP-75243 on Global Mobility's records, D8711081 in Benefits) and 425305 (MP-28124, D7713094). Each joined
  Benefits after her household came into Global Mobility's care, and the benefits portal filed her latest card
  (approved 26 February and 4 January 2024, both ending 30 September 2027) under the Benefits ID only; her
  Global Mobility ID's latest card ended 25 May and 6 April 2024. The judge counted persons by ID and left out the
  Benefits IDs no Global Mobility record carries as spouses never taken into care, which drops exactly these two
  (asserted, SF25). GM-07 1.3 forces 771: the spouse is the one person Global Mobility took into its care with
  the household, however Benefits covers her, and every household with such a Benefits ID has one Global Mobility
  spouse; the spouses Benefits covers in households never taken in exist (97) but hold no card. Submission step
  5 names the people counted and left out and the two cards.
- Ask B's Q3 2026 refiled count is 14: the three matters a judge read as refiled (SLW-2026-03819, -03932, -04941)
  were closed on the employee's departure before any refile; the generator had shipped refile packets after Stop work
  and marked them Receipted though USCIS's receipt was never on record. The world now sends nothing after a stop and
  the mailroom marks Receipted only with a receipt on record (asserted); every other figure of both tables is unchanged.
- No post-rule (c)(9) renewal history exists (the real validity rules, `## Draw` 10); the (c)(9) route share is read on
  the 2024 and 2025 renewals, and the route share is a property of the category, stable across the rule for (c)(26)
  (0.70 before the rule, 0.72 after).

## Strength

P(one strong solver lands 5.5): about 0.29 (0.21 to 0.39). P(both): about 0.105 (0.07 to 0.15), above the independent
0.085 because the same signals drive both. The round 2 recheck put them at 0.30 and 0.11 on the earlier pack, the
insight about 0.24 and the bypasses about 0.06 (the coincidental mix route about 0.03, the flagged reflexes about
0.02, the thin analog about 0.01). Round 2's lever, the summer 2026 lead rise held to about a week (medians 33 to 34
days in June to August, against 37 to 41), takes the share of renewals filed since the rule that carry an expedite
request from 7.5 to 6.8 per cent (181 of 2,665), keeps the September cluster (73 requests) and 154 measured
responses, and leaves the thin analog with 6 renewals, so it is no longer a route; most of the visibility comes from
the paperwork tail and the request timing, which the round 1 audit asked for, so the lever moves P(both) by about
0.005, not to 0.09. The coincidental mix route cannot be closed cheaply (moving the (c)(9) appointment share far
enough breaks the domain or the low-edge margin), so it is flagged and asserted. P(both) stays at the 0.1 line, not
clearly under it, and the asks carry the bar (pair ceiling 33.1, both on the call with no device cracked 44.0).

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
