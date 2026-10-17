# task239 design note

Architecture 1, wave 3, seed DQ12 (which items leave a dashboard index after the structure check): the seed's world,
decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Psychology & Behavioral Science,
psychometric measurement and scale validation, Data Quality Monitoring & Alerting. Lowfirth Parcels, a national
parcels carrier with two sortation hubs, a ring of delivery depots and a head office, runs the Staff Voice survey
every autumn. Its Team Climate Index (twelve agree-disagree items on how safe, open and supportive a team is to work
in) is reported to every team with five or more returns on the team leaders' dashboard, and team leaders'
development plans are set against it. The index describes teams, not their members, so the company's survey
measurement standard runs an annual structure check on it: each item is kept for the next survey only when its
loading on the factor the twelve items share at team level clears the standard's line. The 2027 survey closed in
October; the head of workforce insight takes the check's item list to the executive team, which signs off the 2028
questionnaire.

## Draw

Card `cards/task239.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, each answered here:
repeat.gate_g and overuse.gate_g (method_or_model_selection against task182 and task267, an exceedance build and a
screening-rule build: the shared key is the generic method family, the mechanisms share nothing); repeat.question_form
(which, against task182 and task267: the decision is a designation of items, so the form follows it). At stage 3 the
guard's heart check found task267 (filed before this card, pulled after it) on the same shape, forcing event and
organisation family; those three axes were redrawn (below), the world relabelled with every figure unchanged. The older
same-puzzle and same-driver signatures on G2 carry differentiation lines against task264 v1, task48 and task120 v1.

- **Pairing.** Psychology & Behavioral Science / psychometric-measurement-scale-validation, serving Data Quality
  Monitoring & Alerting. Not banned against the last three builds (task192, task182, task267). The object is the
  health of a reported index's measurement (whether each item still measures the team property the index reports),
  the call a monitoring decision on what the index carries into the next survey.
- **Niche.** Multilevel construct validation of a unit-level index: an index reported per team is valid at team level
  only, and an item's team-level structure (how teams' own levels on it go with the climate the other items share)
  can part company with its member-level structure (how one member's answer goes with the same member's other
  answers).
- **The call.** Which of the twelve items stay in the Team Climate Index for the 2028 survey (the others withdrawn).
- **Shape.** 16, indicators into one score: the criteria come from each of the twelve indicators as it enters the
  index for 2028 (its team-level loading against the standard's 0.75 line and its verdict, then its company-wide
  answers and favourable answers), with the returns by channel and by division as the check's audit trail.
  Arithmetic: 12 item lines + 24 item counts + 12 channel figures + 12 division figures + 3 slide parts = 63 ask
  criteria, beside the call and its two components. Decision designation_set, answer set_of_items, question form
  which.
- **Strategy.** decomposition_attribution (the covariance of team means split into the teams' own covariance and the
  members' covariance it carries), G2 decisive (team means sit at the team grain but carry the member grain's
  covariance), G16 (the estimator of the between-team covariance the standard's team level entitles), G17; Gate G
  method_or_model_selection; calibration none; context artifact filed_standard (the survey measurement standard);
  layer 2 family estimation_fit, pattern own:between-team-structure-net-of-the-members-covariance.
- **Forum, event, organisation.** executive_team (the company's executive team signs off the 2028 questionnaire),
  period_close (the structure check closes each survey year once the dashboard is out, before the next
  questionnaire), logistics_or_3pl. All three clear the last three builds and the three filed after this card whose
  ban windows hold it (task158, task468, task190).
- **People** (`guard.py names --geo Scotland --seed 239`, locale en_GB): Carolyn Burrows, head of workforce insight,
  who owns the survey and takes the item list to the executive; George Haynes, survey methods analyst, who keeps the
  exports and the codebook; Laura Miles, Staff Voice programme manager, who ran the 2027 fieldwork.
- **Deliverables.** `lfp_tci_structure_check_2027.xlsx` (each item's team-level loading and verdict, and the asks'
  figures) and `lfp_tci_items_2028.pptx` (the slide for the executive: the items that stay, with a native chart of
  each item's team-level loading against the 0.75 line).
- **As-of.** 2027-11-19: online fieldwork ran 6 September to 4 October 2027, paper forms were accepted to 8 October,
  the dashboard was published on 1 November, and the executive signs off the 2028 questionnaire in January 2028.
- **Data-native sentence.** Each return is one member's answers to all twelve items, and a member who rates the team
  well on one item tends to rate it well on the others (a disposition that is the member's, not the team's), while a
  team is seen only through the eight or so members who returned a form; so every team mean carries an eighth of the
  members' own covariance across the items, enough here to reorder them, and the items whose answers
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

1. Read the survey measurement standard: the index is reported for teams with five or more returns that count; the
   structure check keeps an item when its loading on the single factor the twelve items' team levels share is 0.75 or
   more.
2. Build the 2027 returns that count from the platform's session and response exports and the paper scans under the
   standard's section 3, resolve each return's team under section 3.4, keep the 1,016 teams with five or more returns
   and their 8,323 returns answering all twelve items, scored per section 2.
3. Average each item over each team's returns (the team's level as its returns show it) and fit one factor to the
   correlation matrix of the 1,016 team means.
4. Keep the items loading 0.75 or more.

Ends on: eight items stay (TC09 0.58, TC10 0.58, TC11 0.34 and TC12 0.33 withdrawn; the climate items 0.79 to 0.82).

Golden: ten items stay (TC01 to TC10 at 0.89 to 0.94; TC11 and TC12 at -0.02), from one factor fitted to the
between-team covariance net of the pooled within-team covariance.

## Stump sentence

A competent analyst fits one factor to the 2027 team means of the 1,016 teams with five or more returns and withdraws
four items for 2028, keeping eight (Ends on: eight items stay, TC09 0.58 and TC10 0.58 withdrawn beside TC11 and TC12);
the step that lands it there is reading the covariance of team means, which carries the members' own covariance across
the items divided by the team's 8.2 or so returns, as the covariance of the teams' own levels, when the between-team
covariance net of the pooled within-team covariance puts both practice items at 0.94 and 0.91 and withdraws only TC11
and TC12.

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
- **Layer 1:** the survey platform's session export and its long response export (one row per question shown, UTC
  stamps, online question codes) beside the scanning bureau's wide file of paper forms (one row per form, paper
  columns, codes 8 and 9 for a double mark and no mark) and the pack list the forms' serials join to; paper packs and
  the site tablets' first team list carrying codes of the July structure, read through HR's reorganisation map, with
  five July codes of split teams reissued on 1 September to new teams; a member returning on two channels, a personal
  link submitted twice, a tablet re-sending a session when its connection came back; sessions abandoned or open at the
  close; forms scanned after the deadline and forms returned blank; don't know beside the scale; TC04 and TC07 stored
  as answered; HR's register at its November state, with a team's previous division. Each is how the system that
  writes it behaves; none is placed to be caught, and none moves the call (R2, asserted slip by slip).
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
- **Analyst test:** a strong analyst who builds the 2027 returns under the standard's rules from every channel, scores
  the negatively worded items reversed, keeps the teams with five or more returns and fits one factor to the team
  means withdraws four items and keeps eight (Ends on: eight items stay, TC09 0.58 and TC10 0.58 withdrawn beside TC11
  and TC12); one who first divides each team-mean correlation by the square root of the two items' team-mean
  reliabilities keeps TC11 and TC12 (0.91, 0.84) and still withdraws the two practice items (0.68, 0.65). Subtracting
  the pooled within-team matrix over the team sizes from the means' covariance is the decomposition itself and files
  the ten.
- **Estimand:** the survey measurement standard (`lfp_wi_sv03_measurement_standard_2027.pdf`, sections 3 to 5) fixes
  the population (the teams reported under 5.1 and their returns that count answering all twelve items on the scale),
  the outcome (each item's loading on the single common factor of the twelve items' team levels, a team's level being
  the score a member of the team is expected to give, which stays the same as staff come and go), the window (the 2027
  survey), the unit (one item; each item's team level standardised across the teams) and the comparison (the 0.75
  line, inclusive).
- **No decoy:** nothing is planted: no earlier check, memo or draft gives a loading or an item list; the dashboard's
  own team scores are the company's release; the fieldwork close-out reports returns and response, never structure.
- **No certified replay:** no certified or published loading or check result exists for a method to reproduce.
- **Lesson:** a unit-level index's structure lives in the covariance of the units' own levels, which the unit means
  carry together with the members' covariance divided by the unit's size, so the structure check subtracts the pooled
  within-unit covariance before it fits the factor; no build on file separates a between-unit structure from the
  within-unit structure it is mixed with (task450 screens drifted anchors, task257 corrects correlations on lopsided
  categories, task237 separates a wording factor).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0a one factor on every member's answers: no item reaches 0.75 (climate items 0.68 to 0.72) | 4.2's single factor, read on the returns | every return is a row of twelve answers | yes, the textbook scale check | none | no | one fit | readable |
| 0 (default) one factor on the team means: eight stay, TC09 0.58, TC10 0.58, TC11 0.34, TC12 0.33 withdrawn | 4.1 and 4.2 send the check to team level, and a team mean is the obvious estimate of a team's level | the team code on every return makes the means a group-by | yes: aggregate to the unit the index reports | none | no | one group-by, one fit | readable |
| 1 the same means weighted by returns, from teams with ten or more returns, shrunk towards the company mean, or as a first principal component: eight stay in each | the floor in 5.1 invites a stricter floor; nothing else | returns per team are counted anyway | yes: weight, trim, shrink | none | no | one group-by, one fit | readable |
| 2 team means corrected for their unreliability (each correlation over the root of the two ICC(2) reliabilities): TC09 0.68 and TC10 0.65 withdrawn, TC11 0.91 and TC12 0.84 kept | none; 4.1's level is a property of the team, which invites correcting for noise | none | yes, for an analyst who knows team means are noisy | none | no | a ratio per pair | readable |
| 3 (decisive) the between-team covariance as the scaled between-team matrix less the pooled within-team matrix, then one factor: ten stay, TC11 and TC12 at -0.02 | no sentence names a decomposition, a within-team matrix or an estimator; the standard files only what a team's level is | no column holds a within-team or between-team part; the returns hold members' answers | no: the reflexes aggregate, weight, trim, shrink or correct for reliability, and none takes the members' own covariance back out of the means | no control scores an estimator; no earlier check ships | no | not linear: two matrices from member rows, a team-size constant, a difference, then a factor fit | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a team's level on an item | the score a member of the team is expected to give, the same as staff come and go | the mean over the team's current staff (finite team) | eight stay (TC09 at 0.74 and TC10 at 0.73) | standard 4.1 ("a property of the team itself ... which stays the same as staff come and go") |
| SF2 | team-level loading's standardisation | each item's team level standardised across the teams | the loading standardised on the whole answer | every item withdrawn | standard 4.2 ("when each item's team level is standardised across those teams") |
| SF3 | a single common factor | one factor | two team-level factors, the climate one taken | same call (TC11 and TC12 under 0.4 on the climate factor) | standard 4.2; same call (asserted) |
| SF4 | 0.75 or more | inclusive | exclusive | same call (no item within 0.05 of 0.75) | standard 4.3; same call (asserted) |
| SF5 | the teams in the check | teams reported under 5.1 (five or more returns that count) | teams with five or more complete returns | same call | standard 4.4; same call (asserted) |
| SF6 | the returns in the check | returns answering all twelve items on the scale | every pair of answers (pairwise) | same call | standard 4.4; same call (asserted) |
| SF7 | an item's score | 1 to 5, TC04 and TC07 reversed | favourable or not (0 or 1) | same call | standard section 2; same call (asserted) |
| SF8 | paper codes 8 and 9 | not answers on the scale | read as values | same call | codebook, sheet Answer codes; same call (asserted) |
| SF9 | a member's returns on two channels | the one received last | both | same call | standard 3.3; same call (asserted) |
| SF10 | a tablet session reaching the platform twice | once | twice | same call | standard 3.3 ("each return counts once"); same call (asserted) |
| SF11 | July team codes, the five reissued among them | through the reorganisation map for paper packs and for tablet sessions started before the second list load | joined as they stand, or every tablet code through the map | same call | standard 3.4; same call (asserted) |
| SF12 | the one-factor estimator | principal axis | maximum likelihood, first principal component | same call | same call (asserted) |
| SF13 | the between-team covariance estimator | the returns-weighted scaled between-team matrix less the pooled within-team matrix | the unweighted version; the cross-half covariance of team half-means | same call | same call (asserted) |
| SF14 | 23:59 on 4 October | UK time (the dictionary: times not ending `_utc` are UK time) | 23:59 UTC on the `_utc` stamps | same call (no submission within two hours of either) | standard 3.1; same call (asserted) |
| SF15 | late forms | after 8 October | kept | same call | standard 3.2; same call (asserted) |
| SF16 | the sign of a loading | its size, TC04 and TC07 scored reversed | the signed loading on unreversed codes | same call | standard section 2; same call (asserted) |

## Ladder

Four rungs and a floor, each a defensible way to read an item's team-level structure, each dying to one fact of the
data (figures on the cut pack, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0a | one factor on every member's answers | no item stays (climate items 0.68 to 0.72; within-team fit 0.63 to 0.68) | the index reports teams (4.1): a member-level fit mixes the members' structure with the teams' |
| 0 (default) | one factor on the 1,016 team means | eight stay; TC09 0.58, TC10 0.58, TC11 0.34, TC12 0.33 withdrawn | each team mean carries the pooled within-team covariance divided by the team's returns (8.2 on average); within teams the members' answers carry the climate and workload items together (within-team loadings 0.63 to 0.68 for the climate items, 0.77 and 0.76 for TC11 and TC12) and the practice items hardly at all (0.08 and 0.07), so the means' factor lifts TC11 and TC12 and leaves TC09 and TC10 short, although the practice items' team levels vary as much as the climate items' (ICC 0.14 and 0.17 against 0.15 to 0.18) |
| 1 | the means weighted by returns, from teams with ten or more returns, shrunk, or as a first component | eight stay in each (practice items 0.62 to 0.73) | the same: weighting, trimming and shrinking keep the members' covariance in the means |
| 2 | team means corrected for their unreliability | TC09 0.68 and TC10 0.65 withdrawn, TC11 0.91 and TC12 0.84 kept: ten stay, the wrong ten | the correction assumes a team mean's noise is unrelated across items, while one member's answers move together: correlations above one show it |
| 3 (golden) | between-team covariance net of the pooled within-team covariance | ten stay: TC01 to TC10 at 0.89 to 0.94, TC11 and TC12 at -0.02 | |

- **Margins.** On the default path the practice items sit 0.17 under the line and the climate items 0.04 to 0.07 over
  it; on the golden every kept item sits 0.14 or more over the line and the withdrawn pair 0.77 under it. Across the
  five golden estimators (principal axis, maximum likelihood, first component, unweighted, cross-half) the kept items
  stay at 0.88 or more and the withdrawn pair between -0.12 and 0.05; across every Layer 1 slip (R2) at 0.80 or more
  and under 0.25, the bands the write-up grades.
- **Position.** The golden's ten is reached by no other rung: the default path and its variants give eight, the
  reliability correction ten with the practice items out, the member-level fits none or two.
- **Dominance.** The decisive move lifts both practice items by 0.33 or more and drops the workload pair by 0.35 or
  more. Rung 1's variants leave the practice items at 0.62 to 0.73 and the workload pair at 0.29 to 0.39, on the
  default's side of the line; the reliability correction lifts the practice items by under 0.10 and the workload pair
  over the line (0.91 and 0.84), the opposite way to the decisive move.
- **Grid.** The cells the checks run, each a named wrong answer except the decomposition: member level pooled (none
  stay) and within teams (two, TC11 and TC12); team means as they stand, weighted, from teams with ten or more returns,
  shrunk, or as a first component (eight each); the means corrected for unreliability, on ICC(2) or on split halves
  (ten with the practice items out); the decomposition under five estimators (the golden ten). On the simulator's
  clean truth the same rungs file one, two, eight, ten with the practice items out, and the golden (R3).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the teams reported under 5.1 and their returns answering all twelve items (4.4); C1 with complete-return floors (SF5) |
| 2 | Unit of account | one item's loading; the team level defined in 4.1 (SF1) |
| 3 | Attribution window | the 2027 survey: online by 23:59 on 4 October, paper scanned by 8 October; no online submission within two hours of the close |
| 4 | As-of dating | teams as resolved under 3.4 on the census date; divisions (asks) as on 1 September per the dashboard note |
| 5 | Version basis | the September structure; July codes through the map (3.4), the tablets' list by its load time |
| 6 | Denominator | for the call, none; for the counts ask, answers on the scale (dashboard note) |
| 7 | Weighting | the returns-weighted between-team matrix; unweighted gives the same call (SF13) |
| 8 | Window length | one survey; nothing longer is read |
| 9 | Boundary inclusivity | 0.75 or more (4.3); no item within 0.05 (SF4) |
| 10 | Rounding path | loadings to two decimals at the close; bands graded (0.80 or more; under 0.25) |
| 11 | Tie-break | none needed: no tied loadings near the line |
| 12 | Maturity and censoring | the survey is closed; nothing arrives after the as-of date |
| 13 | Order of operations | returns that count (section 3), then teams (3.4), the floor (5.1), then complete returns (4.4); the floor on complete returns gives the same call (SF5) |
| 14 | Row order | no step depends on file order; the last received return is by time, ties absent (pairs two days apart) |
| 15 | Duplicate resolution | the last received per member (3.3), one copy of a re-sent tablet session; same call either way (SF9, SF10) |
| 16 | Identity normalisation | typed codes compared without case or spacing (dictionary: kept as typed); paper members through the pack list |
| 17 | Netting against gross | not applicable: no amounts net |
| 18 | Dimensional units | every item on the same five-point scale |
| 19 | Code and status semantics | don't know, 8 and 9 are not answers on the scale (4.4, codebook); same call if read as values (SF8) |
| 20 | Integerisation | counts are whole; loadings continuous |
| 21 | Clause scope | the standard's sections apply to the 2027 survey and its dashboard |
| 22 | Forward window contents | the call is the 2028 item list; nothing about 2028 is estimated |

## Literal reader

Executing the prompt and the standard word for word: the returns that count (section 3), each placed in its team (3.4),
the teams reported (5.1), the returns answering all twelve items (4.4), each item's team level the score a member of
the team is expected to give, the same as staff come and go (4.1), one common factor across the teams with each team
level standardised (4.2), the 0.75 line (4.3). The quantity is the covariance of the teams' own levels; every
estimator of it the checks run (five) files the ten. The easy answer, eight, comes from an easy method on that same
literal estimand (the team means' covariance taken for the levels' covariance), never from another reading: the one
reading that would also file eight, the current staff's mean (SF1), is ruled out by 4.1's sentence.

## Oracles

None. No earlier structure check, published loading or certified figure ships; the 2026 dashboard's item results
(a distractor) give percent favourable, not loadings, and tie to nothing in the check; the close-out's returns are
given only to the nearest hundred.

## Ask sheet

**Ask 1, returns by channel** (personal link, site tablet, paper form: returns that count, outside the teams the
dashboard reports, in a reported team but missing an item, used by the check; 12 figures). H18: the audit trail of the
check's input, from the returns that count down to the returns it reads. Use: the executive team's question of which
staff the check speaks for. Primary device S2 (five July codes of split teams were reissued on 1 September; paper
packs and the tablets' first team list carry July codes, so a return whose July code was reissued reads as the new
team when joined as it stands: site outside 314 against 298, paper outside 290 against 262); hazards S1, S7 and the
personal-link resubmissions. Path: sessions, answers, scans, packs, register, reorganisation map, tablet log (7 files,
12 columns). Stops: the natural read (no member link across channels, re-sent sessions kept, codes as they stand)
personal 7,918 / 1,068 / 945 / 5,905, site 2,352 / 274 / 267 / 1,811, paper 1,866 / 264 / 282 / 1,320; S1 alone
missed personal 7,918 / 1,119 / 937 / 5,862; S2's over-correction (every tablet code through the map) site outside
317. Realism: every device is a system's own behaviour (reissued cost-centre codes, a team list loaded before a
reorganisation, a member answering twice, a tablet re-sending on reconnection).

**Ask 2, each item's company-wide answers on the scale and favourable answers** (24 figures). H18: a measure every item
carries that the call does not turn on. Use: the dashboard's item results behind the 2028 list. Primary device S1 (a
member who returned twice counts once, at the last received: 335 earlier returns, linked only through the personal
link's code, the code typed on a tablet and the pack a form was posted in); hazard S7 (319 re-sent tablet sessions:
every base 308 to 318 higher when kept). Path: sessions, answers, scans, packs, dashboard note (5 files). Stops: both
devices missed, every base 640 to 651 higher; S1 alone missed, 330 to 335 higher; S7 alone missed, 308 to 318 higher;
the check's own returns (8,323 per item); don't know in the base, 32 to 279 higher. Realism: a member answering online
after posting a paper form, and a tablet's sync retry, are what the systems record.

**Ask 3, by division: teams the dashboard reports and returns the check used** (12 figures). H18: the audit trail of
the check's teams. Use: where the check's evidence sits. Primary device S3 (the register's November state: 11
depot conveyor maintenance teams moved from Engineering to Delivery Operations on 1 November, after the census date,
and 8 depot administration teams moved from Corporate Services to Delivery Operations on 1 September keeping their CS
codes; the current division moves 11 teams and 67 returns, the code prefix or the previous division 8 teams and 55
returns); hazards S1, S7, S2. Path: register, the dashboard note, and Ask 1's path (9 files). Stops: the natural read
Hub Operations +3 / +100, Linehaul and Fleet +3 / +64, Customer Service +3 / +44, Engineering 0 / +108, Delivery
Operations +28 / +355, Corporate Services +4 / +42. Realism: HR keeps a team's current
division with the one it left and the date.

Main population zero-counts: the golden's check population holds none of the 335 earlier returns, none of the 319
re-sent copies and none of the returns whose July code was reissued (they resolve to no team); every device mishandled
leaves the ten (separation, asserted), and the main path is mess-neutral (R2).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| S1 a member's returns on two channels | 1, 2, 3 | ledger paper count +152; bases +335; Engineering used +73 |
| S7 a tablet's re-sent session | 1, 2, 3 | site count +319; bases +318; Delivery Operations used +184 |
| S2 reissued July codes | 1, 3 | paper outside -28; Hub Operations used +16 |
| S3 division at the census date | 3 | Engineering -11 teams |
| resubmitted personal links (seen) | 1, 2, 3 | personal count +68 |

Referee: none needed; no control ties under any handling.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask 1, personal link | dedups the link by code; misses members across channels and the re-sent copies' effect on the floor | miss |
| Ask 1, site tablet | keeps the re-sent sessions (session ids unique) and joins July codes as they stand | miss |
| Ask 1, paper form | maps the codes that fail to join, not the reissued ones that join | miss |
| Ask 2, every item's base | counts each member's returns on two channels and the re-sent sessions | miss |
| Ask 2, every item's favourable answers | the same returns | miss |
| Ask 3, Hub Operations | the reissued HO codes join as they stand | miss |
| Ask 3, Linehaul and Fleet | members across channels | miss |
| Ask 3, Customer Service | re-sent sessions at the depots | miss |
| Ask 3, Engineering | the current division, re-sent sessions | miss |
| Ask 3, Delivery Operations | the current division, re-sent sessions, reissued DO codes | miss |
| Ask 3, Corporate Services | members across channels, the CS-coded teams in Delivery Operations since 1 September | miss |

The cracker keeps the item table (12 lines, construction-keyed) and the slide (3): 15 of 63 ask criteria, Lc 0.24.
The mirror (stopped at the team means) keeps the item lines whose team-mean loading clears 0.80 (TC01, TC02, TC04,
TC06, TC07: 5 of 63), Ls 0.08.

Pair ceiling: 37.3 ((38 + 7 + 55 x 0.24) and (5 + 7 + 55 x 0.08), averaged)

Mirror leakage: 7.9 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each item's loading on the team-level factor of a two-level factor model, the
   between-team covariance net of the pooled within-team covariance, the multilevel construct validation a
   psychometrician runs before an index is reported per team; one factor on the team means files eight (TC09 and TC10
   withdrawn with the workload pair), the reliability-corrected means the wrong ten. With depot volumes or
   megawatt-hours in place of the members' answers there is no respondent whose answers share one disposition, no
   team level distinct from a member's and nothing for the check to separate.
2. Two layers: Layer 1 (the platform's session and long response exports in UTC beside the bureau's wide scan file
   with its own codes; paper packs and the tablets' first team list carrying July codes, five of them reissued; a
   member on two channels linked through three keys; tablet sessions re-sent after the sync fault; abandoned and open
   sessions, resubmitted personal links, late and blank forms; teams under the five-return floor; the register's
   current division) is neutral on the call: every slip in R2 keeps the ten inside the graded bands and leaves the
   default path on eight. Layer 2 is the decomposition, asserted alone to move the default path to the golden on the
   simulator's clean truth (R3b).
3. No banned stump decides: nothing is planted (no earlier check, memo or draft gives a loading or an item list; the
   2026 item results give percent favourable only); not semantics (the default path reads every field and code right
   and files eight on the clean truth, R3a); not rule application (WI-SV-03 files the team level, the single factor,
   the standardisation across teams and the 0.75 line, and names no estimator, asserted on its text).
4. Gate G: no shipped artifact ranks the items on a loading or on the decision; the two distractors (HR's staff in
   post and the 2026 dashboard's item results) carry no loading and no team-level figure.
5. Determinism: the item lines grade bands (0.80 or more kept, under 0.25 withdrawn) that hold under five estimators
   of the between-team covariance and every Layer 1 slip; the 48 ask figures are integers, each moved by at least one
   silent device; the fork table's 16 rows are asserted in `checks.py` and the verifier recomputes every figure from
   the bundle alone.
6. Fingerprint: heart WARN (repeat.gate_g, overuse.gate_g, repeat.question_form, answered under Draw); the shape,
   forcing event and organisation family were redrawn after task267's clash, with every figure unchanged.
7. Judge (one isolated thread, Sonnet, medium, the bundle and the graded blocks only): DETERMINISTIC, APPROVE. Every
   graded figure reproduced from the files (11,482 returns, 1,016 teams, 8,323 used, the 12 channel figures, the 24
   item counts, the 12 division figures; TC01 to TC10 at 0.885 to 0.936, TC11 and TC12 at -0.02); the team means'
   factor keeps eight and the member-level fit none. Gate G statistical_rigor, analytical_non_defect, no surface read,
   not a sole data defect; Gate H domain pass, layers pass, decisive step analytical. Its four low findings, none moving
   a committed answer: the write-up's "correcting the team means for their unreliability" read as the covariance
   correction (which files the ten), now named exactly as the division of each correlation by the root of the two
   reliabilities; which team list each channel's codes follow and where a team that moved on 1 September sits, now
   field descriptions in the dictionary (a personal link's code as HR held it when the links were issued on 6
   September, a tablet's list as HR held it the day it was loaded, a team's `division_since` the date it joined its
   division now); and the bands graded for loadings asked to two decimals, kept because the unbiased estimators part at
   the second decimal (TC01 0.88 to 0.91) while every one clears the band. No re-judge: the disposition was APPROVE.

## Leak check

`leak.py --asof 2027-11-19`: REVIEW, no LEAK (the response export first shipped as `..._platform_answers.csv`, the author
word "answer" in its name and column, renamed `..._platform_responses.csv` with `response`; the tablets' `device_ref`
became `tablet_ref`). The REVIEW lines:

- WI-SV-03 carries 0.75: the filed line in 4.3 that every route applies, not a result.
- WI-SV-03 and the dictionary carry the call's words: the items, the index and the 2028 survey are the fiction's own
  nouns; neither states which items stay.
- WI-SV-03, the README, the dashboard note and the close-out carry stump-paragraph words (factor, member, levels,
  method, analyst, reported): the standard's own estimand and a job title; none names the decomposition, a within-team
  matrix or an estimator (asserted on the standard's text).

Isolated reads (Sonnet, medium, prompt and pack only): pass 1 found no decisive-step sentence, ranking file or answer
figure, judged the call an analytical choice and read 4.1 as defining the target, not the method; its realism
findings (corporate team names like "Legal Coastal 7", a stray "bureau" in the close-out, session numbers stepping in
threes) were fixed by naming teams by queue, function or area, rewording the close-out and numbering sessions with the
gaps a platform shared with other surveys leaves (no figure moved). Pass 2, after the judge's dictionary sentences,
again found question 1 none and the call analytical; its findings (renamed and merged teams carrying unrelated July
names, the close-out's tablets set up "in the week before launch" against installs on 19 and 20 August, a personal
link's structure left to inference) were fixed by renumbering a renamed or merged team's July name, giving both halves
of a split team its function, dating the tablets to the second half of August and filing a personal link's code as HR
held it on 6 September (no figure moved). Pass 3 found question 1 none and the call analytical again, read each
channel's team structure off the dictionary and the log, and placed a team that joined a division on 1 September in it
on the census date; its data-only tells (most renamed teams keeping their names, every tablet going offline in the same
minute, `invited` too regular) were fixed from generators kept apart from the records' own (no figure moved).
`guard.py surface` promotes task237 (the same pairing two builds apart in this lane; a wording method factor there, the
members' covariance in team means here): the adjudicated clone check is the author's call.

## Tried and rejected

- Item drift between 2026 and 2027 judged by differential item functioning with a purified matching score (total-score
  matching contaminated by several items drifting the same way): the insight (screen the shared items that moved and
  link through those that held) is task450's, so the lesson repeats; dropped at the draw.
- The seed's pitfall (factor retention by eigenvalue over one against parallel analysis): the retention method is the
  decisive step and several retention rules stand with no data-native reason to prefer one, so the call is either rule
  application (the rule filed) or not determinate; dropped at the draw.
- Ceiling effects lowering Pearson item-rest correlations (polychoric against Pearson): task257 holds the correlation
  correction on lopsided categories; dropped at the draw.
- The paper form printing its scale the other way round (5 strongly disagree): a reading that, mishandled, moved the
  climate items' band under the slip check, so the call would have turned on reading a code; the paper scale was made
  the same as online and the paper team code moved to the pack list, which keeps the member link as Layer 1 mess.
- An ask for each item's percent favourable to one decimal: two items sat within a hundredth of a rounding edge under
  the defensible bases; replaced by the whole counts behind it (answers on the scale and favourable answers).
- The first world, a Scottish health board (shape 10, forcing event launch_or_rollout, hospital_or_health_provider):
  task267, filed before this card and pulled after it, held the same three axes, so the guard's heart check blocked;
  the world was relabelled as a parcels company (every list length and random draw kept, every figure unchanged) and
  the axes redrawn to shape 16, period_close and logistics_or_3pl. The council first considered was dropped because
  task468, filed after this card, is local government; shape and event `other` because task158 holds both; and the
  event audit_or_inspection because task190, once task194's re-registration moved it, holds this card in its window.
