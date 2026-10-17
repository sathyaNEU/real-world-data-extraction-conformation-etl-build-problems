# task239 design note

Architecture 1, wave 3, seed DQ12 (which items leave a dashboard index after the structure check): the seed's world,
decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Psychology & Behavioral Science,
psychometric measurement and scale validation, Data Quality Monitoring & Alerting. Mid Coast Health Board, a regional
health board in Scotland, runs the Staff Voice survey every autumn. Its Team Climate Index (twelve agree-disagree
items on how safe, open and supportive a team is to work in) is reported to every team with five or more returns on
the team leaders' dashboard, and team leaders' development plans are set against it. The index describes teams, not
their members, so the board's survey measurement standard runs an annual structure check on it: each item is kept
for the next survey only when its loading on the factor the twelve items share at team level clears the standard's
line. The 2027 survey closed in October; the head of workforce insight takes the check's item list to the executive
team, which signs off the 2028 questionnaire before it goes to print.

## Draw

Card `cards/task239.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, each answered here:
repeat.gate_g and overuse.gate_g (method_or_model_selection against task192 and task182, an event-coding and an
exceedance build: the shared key is the generic method family, the mechanisms share nothing); repeat.question_form
(which, against task182, retired: the decision is a designation of items, so the form follows it). The older
same-puzzle and same-driver signatures on G2 carry differentiation lines against task264 v1, task48 and task120 v1.

- **Pairing.** Psychology & Behavioral Science / psychometric-measurement-scale-validation, serving Data Quality
  Monitoring & Alerting. Not banned against the last three builds (task467, task192, task182). The object is the
  health of a reported index's measurement (whether each item still measures the team property the index reports),
  the call a monitoring decision on what the index carries into the next survey.
- **Niche.** Multilevel construct validation of a unit-level index: an index reported per team is valid at team level
  only, and an item's team-level structure (how teams' own levels on it go with the climate the other items share)
  can part company with its member-level structure (how one member's answer goes with the same member's other
  answers).
- **The call.** Which of the twelve items stay in the Team Climate Index for the 2028 survey (the others withdrawn).
- **Shape.** 10, scorecard against a threshold: each item's team-level loading checked against the standard's 0.75
  line, a verdict per item. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** decomposition_attribution (the covariance of team means split into the teams' own covariance and the
  members' covariance it carries), G2 decisive (team means sit at the team grain but carry the member grain's
  covariance), G16 (the estimator of the between-team covariance the standard's team level entitles), G17; Gate G
  method_or_model_selection; calibration none; context artifact filed_standard (the survey measurement standard);
  layer 2 family estimation_fit, pattern own:between-team-structure-net-of-the-members-covariance.
- **Forum, event, organisation.** executive_team (the board's executive team signs off the 2028 questionnaire),
  launch_or_rollout (the 2028 survey's questionnaire goes to print), hospital_or_health_provider.
- **People** (`guard.py names --geo Scotland --seed 239`, locale en_GB): Carolyn Burrows, head of workforce insight,
  who owns the survey and takes the item list to the executive; George Haynes, survey methods analyst, who keeps the
  exports and the codebook; Laura Miles, Staff Voice programme manager, who ran the 2027 fieldwork.
- **Deliverables.** `mhb_tci_structure_check_2027.xlsx` (each item's team-level loading and verdict, and the asks'
  figures) and `mhb_tci_items_2028.pptx` (the slide for the executive: the items that stay, with a native chart of
  each item's team-level loading against the 0.75 line).
- **As-of.** 2027-11-19: online fieldwork ran 6 September to 4 October 2027, paper forms were accepted to 8 October,
  the dashboard was published on 1 November, and the executive signs off the 2028 questionnaire in January 2028.
- **Data-native sentence.** Each return is one member's answers to all twelve items, and a member who rates the team
  well on one item tends to rate it well on the others (a disposition that is the member's, not the team's), while a
  team is seen only through the eight or so members who returned a form; so every team mean carries an eighth of the
  members' own covariance across the items, which here is as large as the teams' own, and the items whose answers
  follow that member disposition most (two whose team levels follow workload) look most like the climate in team
  means, while the two items on team practice, where whole teams differ and members barely differ in the same
  direction, look least like it.

Sources, one line each (what it teaches; how this build differs):
- Multilevel factor analysis (Muthén's decomposition of a two-level covariance into a pooled within-group and a
  between-group part; the scaled between-group matrix estimating the within matrix plus a multiple of the between
  matrix; full-information two-level estimation): the field's method for a team-level structure; here it is never
  named in the pack, and the factor analysis of team means, with or without a reliability correction, is the reflex
  it has to beat.
- Composition models for team climate (referent shift, aggregation justified by agreement and ICC): the frame in
  which a team-level index is valid; here the aggregation is justified and the question is the structure of what is
  aggregated.
- The client's psychometric patterns (alpha against omega, polychorics, parallel analysis): the kind of pitfall the
  field holds; none of the three is this build's step.
- Seed DQ12: the world (a dashboard index), the decision (the items that stay) and the quantity (each item's loading
  in the structure check) only; its pitfall (factor retention by eigenvalue over one) is not used.
- Spent on this objective (`guard.py mechanisms`): task229 (a convex conversion of a daily mean), task231 (a rate over
  active units with late exits), task232 (transmission from delayed mixed outcomes), task230 (a late channel's net
  classification bias), task228 (variance at the randomised unit), task233 (a missing-not-at-random departure), task234
  (a source's output from a share a loss cannot move), task235 (a missing event censored until its device's next
  contact), task236 (a capture share against an independent sample), task237 (the trait's share of a score with a
  wording factor), task238 (a mode effect read through a randomized contact strategy). Psychometric drivers elsewhere:
  task450 (anchor items screened for drift before a link), task257 (Pearson correlations on lopsided categories),
  task464 (a concordance by distribution matching). None separates a team-level structure from the members'.

## Default path

1. Read the survey measurement standard: the index is reported for teams with five or more returns; the structure
   check keeps an item when its loading on the single factor the twelve items share at team level is 0.75 or more.
2. Build the 2027 returns from the online export and the paper scan file under the standard's rules (submitted
   returns, one per invitation, the paper scale and the negatively worded items scored as the codebook sets out, team
   codes resolved through the HR crosswalk), keep the teams with five or more returns and the returns answering all
   twelve items.
3. Average each item over each team's returns (the team means the dashboard reports) and fit one factor to the
   correlation matrix of the team means.
4. Keep the items loading 0.75 or more.

Ends on: eight items stay; the two team-practice items (TC09 regular reviews 0.59, TC10 time for new starters 0.62)
and the two workload-tracking items (TC11 0.53, TC12 0.47) are withdrawn (prototype figures; the cut pack's are
asserted in `checks.py` and carried here at stage 3).

Golden: ten items stay; only TC11 and TC12 are withdrawn (team-level loadings about 0.25 and 0.20), the practice items
loading about 0.90, from one factor fitted to the between-team covariance net of the pooled within-team covariance.

## Stump sentence

A competent analyst fits one factor to the 2027 team means of the teams with five or more returns and withdraws four
items for 2028, keeping eight (Ends on: eight items stay, TC09, TC10, TC11 and TC12 withdrawn); the step that lands it
there is reading the covariance of team means, which carries the members' own covariance across the items divided by
team size, as the covariance of the teams' own levels, when the between-team covariance net of the pooled within-team
covariance keeps both practice items far above 0.75 and withdraws only TC11 and TC12.

## Three rules

- **Task type:** psychology-behavioral-science / psychometric-measurement-scale-validation, which serves Data Quality
  Monitoring & Alerting; the object is whether each item of an index reported per team still measures the team
  property the index reports, and the call is which items the index carries into the next survey.
- **Domain test:** the quantity that decides is each item's standardised loading on the team-level factor of a
  two-level factor model of the index's Likert items, the multilevel scale validation a psychometrician runs before an
  index is reported per team; the field separates the between-team covariance from the pooled within-team covariance
  rather than factor-analysing team means.
- **Swap:** "which items stay in the Team Climate Index" rewritten as "which meters stay in the substation load index"
  with megawatt-hours for the staff's answers loses the respondent whose answers to every item share one disposition,
  the team level distinct from the member's, and the climate the items share at team level; there is nothing for the
  structure check to separate and the call stops making sense.
- **Layer 1:** an online survey platform export in long format (one row per answer, UTC submission stamps, item codes)
  beside a paper-form scan file in wide format (one row per form, questionnaire numbers, the answer scale printed in
  the opposite order); paper forms carrying the respondent's pre-reorganisation team code, resolved through the HR
  team crosswalk; online sessions submitted twice from one invitation and sessions abandoned before submission, kept
  in the export; don't-know and not-answered codes that differ between the channels; negatively worded items stored
  as answered and scored reversed per the codebook; teams below the dashboard's five-return floor. Each is how the
  system that writes it behaves; none is placed to be caught, and none moves the call.
- **Layer 2:** estimation_fit: the team-level covariance of the items estimated net of the members' own covariance,
  which the team means carry in proportion to one over the team's size.
- **Decisive step:** estimating the covariance of the teams' own levels as the scaled between-team covariance less the
  pooled within-team covariance (or by a two-level model) before fitting the one factor, rather than fitting it to the
  team means as they stand or to team means corrected for their unreliability.
- **Not semantics:** reading every field, code, scale and definition right (the returns built under the standard, the
  paper scale and the negatively worded items reversed, the team codes resolved, the standard's team level read as
  the team's own level) still leaves the analyst estimating that level by the team mean, and one factor fitted to the
  team means, computed correctly, withdraws four items.
- **Not rule application:** the standard files what the team level is, the single factor, the standardisation and the
  0.75 line; no rule says how to estimate the covariance of the teams' own levels from members' returns, and
  executing every stated rule with team means still files eight items.
- **Analyst test:** a strong analyst who builds the 2027 returns under the standard's rules from both channels, scores
  the negatively worded items reversed, keeps the teams with five or more returns and fits one factor to the team
  means withdraws four items and keeps eight (Ends on: eight items stay, TC09, TC10, TC11 and TC12 withdrawn); one who
  first corrects the team means for their unreliability keeps TC11 and TC12 and still withdraws the two practice
  items.
- **Estimand:** the survey measurement standard (`mhb_survey_measurement_standard_2027.pdf`, section 4) fixes the
  population (teams with five or more returns in the 2027 survey and their returns answering all twelve items), the
  outcome (each item's standardised loading on the single factor the twelve items share at team level, a team's level
  on an item being its members' expected answer), the window (the 2027 survey), the unit (one item; loadings
  standardised on the teams' levels) and the comparison (the 0.75 line).
- **No decoy:** nothing is planted: no earlier check, memo or draft gives a loading or an item list; the dashboard's
  own team scores are the board's release; the fieldwork close-out reports returns and response, never structure.
- **No certified replay:** no certified or published loading or check result exists for a method to reproduce.
- **Lesson:** a unit-level index's structure lives in the covariance of the units' own levels, which the unit means
  carry together with the members' covariance divided by the unit's size, so the structure check subtracts the pooled
  within-unit covariance before it fits the factor; no build on file separates a between-unit structure from the
  within-unit structure it is mixed with (task450 screens drifted anchors, task257 corrects correlations on lopsided
  categories, task237 separates a wording factor).

## Tried and rejected

- Item drift between 2026 and 2027 judged by differential item functioning with a purified matching score (total-score
  matching contaminated by several items drifting the same way): the insight (screen the shared items that moved and
  link through those that held) is task450's, so the lesson repeats; dropped at the draw.
- The seed's pitfall (factor retention by eigenvalue over one against parallel analysis): the retention method is the
  decisive step and several retention rules stand with no data-native reason to prefer one, so the call is either rule
  application (the rule filed) or not determinate; dropped at the draw.
- Ceiling effects lowering Pearson item-rest correlations (polychoric against Pearson): task257 holds the correlation
  correction on lopsided categories; dropped at the draw.
