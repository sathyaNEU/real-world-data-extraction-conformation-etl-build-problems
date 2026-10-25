# task199 design note

Collective-action register, Catatumbo and middle Magdalena corridor. Anomaly Detection & Diagnostics.
Stage 2. Every number below is printed by `generator/core.py` or `generator/ceiling.py`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task199.json`, registered 2026-10-18, `guard.py check` WARN, 0 BLOCK |
| Domain / subdomain | political-science-public-policy / conflict-protest-event-data-analysis (client domain, task type serves anomaly-detection in the taxonomy) |
| Objective | anomaly-detection: a real event separated from an artifact |
| Shape | 10, scorecard against thresholds. 11 cities x (window actions, baseline actions, rate per 100,000, eligible, designated) = 55, plus call, runner-up, gap, flip = 4, plus a chart's 5 named parts, plus 2 deliverables, plus 66 ask figures |
| Decision | pick_one_of_n: the one city the next verification mission goes to, named in the watch note with its recorded rate |
| Gap / pattern / generators | population (a row is a reported action, not an action) / none / G12 decisive, G14, G16 |
| Gate G | decomposition_attribution: every city's recorded rise is correctly reported, and the call turns on assigning it to press presence or to activity |
| Strategy / Layer 2 | causal_design (the exposure must not be caused by the outcome) / estimand_identification, client pattern political-science-public-policy/conflict-protest-event-data-analysis/1 |
| Decision-type WARN | pick_one_of_n repeats whichever build is filed immediately before this one (task198 v4 at filing, task166 earlier the same day): answered, because the call is a mission allocation among eleven recorded candidates, the records-fixed shape this wave's rules prefer over an estimator output, and task166 differs in domain, objective, gap, pattern, Gate G and driver at 0.05 similarity |
| Calibration organ | none, by design (see `## Tried and rejected`) |
| World | Colombia; Observatorio Territorial del Nororiente keeps the Registro de Acciones Colectivas from material delivered by the Resena Andina clipping service; personas drawn with `guard.py names --locale es_CO --seed 199` |
| Spine | `envios_resena_andina.csv`, one row per outlet x city x delivery day, about 31,000 rows, 2024-01-01 to 2026-09-30 |
| Forum / forcing event / org | line_manager_or_team / period_close (the half year closed on 30 September and the definitive extract on 5 November) / university_or_school |
| Answer | Tibu, 92.2 recorded collective actions per 100,000 residents over 1 April to 30 September 2026 (137 gathering-days over a published population of 148,590) |

**Data-native sentence.** In this register an action exists only where a monitored outlet filed an account of
it, and the clipping service's delivery log measures, for every city and every month, how much material
actually reached the monitor, so the record carries its own exposure; the two volumes a solver reaches for
first, the items retained for screening and the citations held per action, are produced by the recorded
actions themselves, so dividing by either cancels the rise being tested for. That is why the pitfall is here
and not in any record whose events arrive by their own channel.

**Why the call is retrospective.** The designation window closed on 30 September 2026 and the register's
definitive extract is dated 5 November 2026, after the 30-day definitive close of every window month, so no
period is open and no count is still developing. The decision the designation forces, where the one funded
verification mission goes next, is forward.

**A line per source read.**
- `guard.py mechanisms --objective anomaly-detection` (31 builds): the adjacent insights are task180 (a
  detection floor set by a known daily cycle), task182 (items entering a record in proportion to their own
  duration), task196 (how many events happened, from the overlap of two capture channels), task470
  (rebuilding the activity a sensor never records for whole unit classes) and task448 (completing a register
  from a second incomplete list). All five estimate what is missing; none turns on which of the record's own
  measured volumes may stand in a denominator.
- task192, the only other build on this subdomain: a classifier's hand-coded error rates transported past the
  window they were measured in. This build ships no classifier, no audit batch and no label correction.
- `stumping` Part 3: the four pricing screens and the variance screen, all run in `generator/core.py`.
- `references/client/layer2-rigor-patterns.md`, pattern 1 for this task type, "reported events track media
  reach: condition on the reporting proxy". That pattern's own shortcut is raw counts, which is this build's
  rung 1, so the decisive step sits one level below the published pattern, in which proxy may be used.
- `guide-to-prompt` shapes 10, 17 and 08: 17 and 08 are native to the objective but take their criteria from
  the periods of one series, which would leave the eleven-city structure ungraded; 10's own hard seam,
  different denominators and windows per metric, is this build's seam exactly.

## Default path

The pipeline a competent analyst builds from the protocol's words and the files' grain.

1. Union the three yearly register exports `rac_acciones_2024.csv`, `_2025.csv`, `_2026.csv`, resolving the
   2025 column renames and the two date formats.
2. Run the hygiene battery: drop the rows the preliminary and definitive extracts of 2026-05, 06 and 07 hold
   twice, keyed on the action id, and expand the 2026 template's day count so one row per gathering-day
   matches the manual's unit.
3. Resolve the city key to the eleven panel cities (names in some years, divipola codes in others).
4. Keep actions whose action date falls in the window, 1 April to 30 September 2026 inclusive, and in the
   baseline, the twenty-four months ended 31 December 2025, on the action date rather than the ingest stamp.
5. Count actions per city per span and divide by 6 and 24 for monthly levels.
6. Join the 2026 population projection (the units sheet, not the thousands sheet) and compute the window's
   actions per 100,000 residents.
7. Rank the eleven cities on the window's monthly level over the baseline's monthly level.
8. Designate the top city and print its window rate.

Ends on: Sardinata, 121.4 actions per 100,000 residents.
Golden: Tibu, 92.2 actions per 100,000 residents.

## Stump sentence

The default path files Sardinata at 121.4 actions per 100,000 residents because it ranks the eleven cities on
their own recorded rise with residents as the only denominator, and Sardinata's entire rise is the material
three outlets began filing from it, which took its delivered items from 12,670 to 22,211 while Tibu's rise
happened with the material reaching the monitor from it unchanged at 12,935 against 3,220 for a quarter of
the span.

## Three rules

**Written to the measured truth at the wave 7 triage, after three isolated reads landed the call and
the three screens were run twice byte-identical on the clean truth and on the shipped pack. Five of the
thirteen lines now fail. The architecture is refused and re-rooted at stage 1; the measurements are in
`## Tried and rejected`.**

- Task type: conflict-protest-event-data-analysis, taken in its anomaly-detection reading, a real
  escalation separated from a reporting artifact. Holds, and is not where the build fails.
- Domain test: holds on its own terms and is the reason the build fails. The deciding quantity is
  protest incidence recovered from a media-sourced event record, and the field's own method for it is to
  condition event counts on reporting intensity, which is the client's pattern 1 for this task type
  verbatim. The golden is therefore that published card applied as the card states it, which `stumping`
  1.3's library test says a blind reader lands: three did, at 45 to 50, 60 to 65 and about 75 per cent
  confidence, the last of them finding the coverage correction unaided and naming Sardinata as the trap.
- Swap: holds. "Which city's protest activity rose, as against the volume of press material reaching the
  register from it" does not survive hospitals and falls, because an internal incident system has no
  outside reporters whose filing volume the record separately measures.
- Layer 1: holds and is inert as designed. Renamed 2025 columns, day-first dates, the 2026 day-count
  template against one row per day, the preliminary and definitive overlap on three months, divipola
  reassignment, units against thousands, PDF tables, the RSA prefix, UTC ingest against local action
  date. None of it changes which city is designated.
- Layer 2: FAILS as drawn. estimand_identification is the right family, but the residue it leaves is
  empty. On the shipped pack the standing family (every construction that differs in what it does, with
  the knobs and the hats removed and the groupings counted: ratio of ratios, its count form, the window
  level, the square-root form, a pooled log-exposure fit, the same fit per stratum, and the two
  drop-the-risen-feeds routes) returns one designated city, 137 window action-days and 92.2 per 100,000,
  a spread of exactly zero on all three graded figures of the call. A standing spread of zero means the
  decisive step is a reflex whatever the documents say.
- Decisive step: FAILS, by algebra. `log(score) = log(raw rise) - log(delivered-item rise)` to a maximum
  absolute difference of 2.22e-16 on the clean truth and again on the cut pack, so the decisive
  construction is two group-bys and one subtraction, and it recovers the generator's own activity
  multiplier exactly (correlation +1.0000, error zero). Worse, on the eight cities whose feed did not
  move the designed score equals the raw rise to a mean of 2.87 per cent with the order identical
  (correlation +0.993114), so the construction does no work on them at all: its only effect is to push
  the three risen feeds from 2.78, 3.17 and 2.78 down to 0.48, 0.45 and 0.44. Dropping those three and
  ranking the remaining eight on the raw rise therefore names the golden at 1.637x against the designed
  route's 1.815x, with the same 137 action-days and the same printed 92.2, and it does so at 576 of 576
  cells of a four-axis dial sweep.
- Not semantics: FAILS. The two wrong volumes are not ruled out by anything structural a solver has to
  work out; they are ruled out by reading the data dictionary's own column descriptions correctly (a
  `cita` is "un item que el registro vinculo a una entrada", so it moves with the numerator; `items_retenidos`
  is what the register's own filter kept). Reading a column definition correctly is the second banned
  class, and here it is what eliminates every candidate but one.
- Not rule application: FAILS, with the three numbers the line owes. ENUMERATED family on the shipped
  pack: 20 constructions, 3 distinct designations, printed-rate spread 71.7 per 100,000, which is 717
  times the printed unit of 0.1, on window action-days of 81, 137 and 177. STANDING family: 8
  constructions, 1 designation, spread exactly zero on the designated city, on 137 and on 92.2.
  LOUDNESS of the ruling-out: the elimination is performed by one filed sentence at authority, protocol
  clause 4.1 ("Los registros del Observatorio son la evidencia de esa actividad y no su medida"), plus
  the dictionary's column definitions, and by nothing in the record. A Poisson-offset profile of the
  rival exposure bases against the 5,711 events the register actually carries ranks the golden's own
  base third of four: retained items best, citations 23.77 behind in `2 dlogL`, delivered items 184.36
  behind, residents 300.75 behind. So the data not only fails to force the delivered-item exposure, it
  positively disprefers it, and axis 6's closure ("forced by the data's structure") is not what closes it.
- Analyst test: holds as written and is insufficient as a gate. The easy route does file Sardinata at
  121.4 per 100,000 and the citation correction does file Teorama, and `checks.py` executes both. What
  the test never executed is the step between them: once clause 4.1 pushes a reader off the raw count,
  every remaining non-circular construction files the golden, which is the half of the test that decides
  Gate F.
- Estimand: the five parts are filed (population, outcome, window, unit, comparison in protocol clauses
  2.1, 3.2, 4.1, 4.2 and 4.5) and the MEASURE OF THE RISE is not, which the wave 6 audit recorded as a
  separate finding and which SF12 states outright ("not closed by any sentence"). A literal raw-count
  reading of 4.2 gives Sardinata, so the ranking measure is open on the shipped text. Filing it makes the
  step rule application; leaving it open forks the main call. Same dial, both ends.
- No decoy: holds. Nothing is planted, no memo or stakeholder figure argues for a city, no block of
  records is copied, the bulletin designates nobody. The note's own single-use test, however, records
  that deleting the sentence which forces the call leaves the designation unforced, which is the
  announcement and the forcing being one sentence rather than two.
- No certified replay: holds. No completeness audit, gold standard or certified rate ships, and no bench
  blesses a method.
- Lesson: as drawn there is none a model can take, because the standing family has nothing to choose. The
  lesson the triage banks instead is a screen: where the decisive step is which of a record's own measured
  volumes may stand in a denominator, price the standing family and the one-exclusion subset route before
  the world is drawn, because a correction that leaves most of the record alone is published by the part
  it leaves alone.

## Readability screen

Six tests per rung (filed sentence, schema, reflex, control bench, hygiene battery, linear arithmetic),
verdict last. The decisive rung is silent on all six.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 rows as the exports hold them, ranked on the rise (Convencion 3.013) | the window and unit clauses send a reader to the action date and the gathering-day | two date columns and a day count column | yes, the first group-by | none ships | yes, the duplicate check finds the extract overlap | yes | readable |
| 1 battery run, actions on the filed unit, per 100,000, ranked on the rise (Sardinata 3.175) | the protocol's comparison clause gives the baseline | counts and a population join | yes, the opponent default | none ships | yes | yes | readable |
| 2 conditioned on the citations the register holds per action (Teorama 1.748, the golden fourth at 1.071) | no sentence names a denominator; the field's published caveat is general | the retained-item and citation columns sit in the files the call already reads | yes, the media-reach reflex reaches exactly here | none ships | no, no sweep divides a count by its own coverage | one ratio | readable |
| 3 (decisive) conditioned on the material the service delivered, every parameter-free form (Tibu 2.435) | no sentence names the delivered-item column, a denominator or an exposure; the protocol says only what an entry is | the delivered-item column sits in the same table as the retained-item column, named after the service's own delivery, with nothing marking it as the exposure and nothing excluding the other | no, measured: 10 of 10 reflexes name a wrong city, worst at 1.346 against the golden's 1.980 | none ships, and no audit, gold standard or certified figure measures the register's completeness | no, the battery does not reconcile a count against a volume at another grain | no, two ratios and a comparison across eleven cities | silent |

**The eligibility condition is not a rung.** A response that ignores it still files Sardinata, because
Sardinata is eligible, and the only city it removes is Hacari, whose rise is 0.95 and which no route names.
It supplies the scorecard's threshold column and is asserted inert against every rung.

## Semantic fork table

| id | Term or convention | Golden reading | Alternatives and their call | Ruled out by |
|---|---|---|---|---|
| SF1 | recorded collective action | one gathering, on one day, at one place | the register's row (the 2026 template collapses multi-day actions, Convencion 3.112); an episode however long (El Tarra leads) | the coding manual's definition of an entry and its day-count field description, quoted in the dictionary |
| SF2 | the half year to 30 September 2026 | 1 April to 30 September 2026 inclusive, on the action date | by registration date (Convencion); exclusive of an endpoint (same city, rate moves 0.3) | the protocol's designation clause states the span and the word inclusive, and names the action's own date |
| SF3 | per 100,000 residents | the 2026 projection, units sheet | the thousands sheet (a factor of 1,000); the 2024 vintage | the protocol names the statistics office's 2026 projection; the ranking is a within-city rise, so every vintage gives the same designation, asserted on figure and counts |
| SF4 | the two years before it | the twenty-four months ended 31 December 2025 | a rolling twenty-four months to 31 March 2026 | same call, measured: the decisive route names Tibu at the same 1.69x margin and the default path names Sardinata under both readings |
| SF5 | the eleven panel cities | the protocol's panel list | every municipality the register covers (23) | the protocol's panel list, and the asks ask for the other twelve separately |
| SF6 | designated | exactly one city each half year | a set of cities above a threshold | the protocol: one city is designated each half year and receives the mission |
| SF13 | meets the register's condition for a mission | at least thirty actions in the half year and panel membership through the baseline | the condition read against the baseline count, or against the rate | the protocol's clause names the half year and the count; same call either way, and no city sits within 9 actions of the floor |
| SF7 | the actions the register holds | the definitive extract | the preliminary extract; the union of both (Convencion) | the publication clause: the definitive extract supersedes the preliminary |
| SF8 | items the clipping service delivered | every item the service delivered from the municipality | items retained for screening | the ask's own words and the delivery log's two column descriptions, which separate what the service delivered from what the register's filter kept |
| SF9 | municipality outside the panel | the register's city table, on the action's date | the published monthly summary's municipality column (desk grain) | ask B's primary: the summary stands above its own parts for every desk seat, measured |
| SF10 | participants per action | the total participants over the actions holding a participant figure | counting unreported participants as zero; the numeric column's lower bound | the manual's sentence that the column carries a central estimate, and the note field holding the range |
| SF11 | rate | actions over residents, rounded once at the end | rounded per month then summed | the prompt's closing rounding sentence governs the printed figures only |
| SF12 | the material reaching the monitor | the delivered-item count for the city and month | the retained-item count; the citation count | not closed by any sentence: this is the open HOW, forced by the data's structure (see `## Literal reader`) |
| SF14 | a line per item group closing each quarter's gap (ask 4) | the five groups that close the four quarterly gaps between delivered and billed: 82, 138, 70, 126 and 7 | the annual gap, which two groups close (82 and 7); the publication basis against the billing, which two others close (125 and 7) | the asking sentence names each quarter's gap, and only the five-group set closes all four quarters: the two-line annual set closes none of them, and the 125 items published in 2025 and delivered in 2026 sit on neither side of 2025. Asserted as SF14 in `checks.py` and again in `verify.py` from the shipped bytes. The grain of the lines is forced the same way: the invoice bills by desk and month and carries no outlet-type dimension, so a gap between delivered and billed exists only per quarter, and what closes it is the four timing groups and the credited lote |

## Ladder

| Rung | Analysis | Names | Score | Dies to |
|---|---|---|---|---|
| 0 | the exports read as they come | Convencion | 3.013 | the publication clause (the definitive supersedes) and the manual's unit |
| 1 | battery run, filed unit, per 100,000, rise against the city's own baseline (the default path) | Sardinata | 3.175 | the protocol's outcome: a rise in the actions occurring, not in the entries held |
| 2 | conditioned on the citations the register holds per action (the golden fourth at 1.071), or capture estimated from citation redundancy | Teorama | 1.748 | the volumes are produced by the recorded actions, so the ratio cancels the rise; the redundancy family needs a free parameter the pack does not fix, and its winner moves from Teorama to Sardinata as that parameter moves |
| 3 | conditioned on the material the service delivered, the only volume not produced by the actions | **Tibu** | 2.435 | nothing |

**Arithmetic, on the cut pack.** Golden 4th of 11 on rung 1 (the default path), 1st on rung 3. Default-path
margin leader over golden 1.309x; decisive margin golden over runner-up San Calixto 1.815x. On the clean
truth the same margins are 1.26x and 1.85x, the decisive margin is 0.910 ranking units, 3.8 standard errors
of the ranked quantity (0.2398 in the same units) and 22.7 units of the lever's own noise (0.0401), the
number Part 3's refinement asks for in place of a preference for a decision shape. Every parameter-free form of rung 3 names the golden: per delivered item 1.69x, per square root 1.25x,
saturating 1.28x, a fitted log-presence covariate at beta 1.002 1.69x. The exposure elasticity corridor is
[0.255, 1.600] and the fitted value sits at 1.002 inside it. Move needed 0.520 ranking units against 1.500
available, 2.88x. Each rung names its own city, every correction walks one way and only rung 3 reverses, and
the two separations are financed by independent parameters (the risers' presence multipliers and the golden's
activity multiplier).

**Mechanisms, from different gaps.** Rung 0 time and identity (an extract vintage and a template's unit),
rung 2 objective (the metric is right and the denominator is not), rung 3 population (the file is not the
thing). The decisive gap is not rung 1's.

**The two volumes the record offers do not behave alike on the cut pack, and the measured fact is what
ships.** The citations held per action rank Teorama first at 1.748 with the golden fourth at 1.071, so that
is rung 2. The items retained for screening rank the golden first at 1.658, so the retained-item route is a
second exposure measure that reaches the same city rather than a rung, and the choice between the two is
forced by the dictionary's own split between what the service delivered and what the filter kept. The
write-up's step 5 names the citations route alone for that reason.

**The agreement across rung 3's forms is structural, not insensitivity.** The golden's delivered volume does
not move between the two spans, so no transformation of it can absorb its rise, while the rivals' scores
spread 0.55 across the same four forms (Sardinata 1.000 per item, 1.581 per square root, 1.530 saturating,
0.998 fitted). The family therefore separates the candidates and agrees only on the answer.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every action the register holds for the eleven panel cities, all sources | filed in the designation clause; unobserved members stated (the definitive close has passed for every window month) |
| 1b | Candidate set | the cities the protocol's eligibility condition admits | filed in the same clause; asserted inert, it removes Hacari at 25 actions against a floor of 30 and no city within 9 of the floor, and no route names a removed city |
| 2 | Unit of account | one gathering, one day, one place | the manual's entry definition; C4, the row reading is a factor of 1.21 on the window count and names another city |
| 3 | Attribution window | the action's own date | filed; the clause's word inclusive licenses one reading |
| 4 | As-of dating | the definitive extract of 5 November 2026 | filed in the publication clause; the population projection vintage filed |
| 5 | Version basis | the definitive extract supersedes the preliminary | filed; C1 asserted on row counts for the three overlapping months |
| 6 | Denominator | the printed figure's denominator is residents | filed in the protocol. The exposure that estimates incidence is the open HOW, not a convention: forced by the data's structure, with the corridor measured |
| 7 | Weighting | pooled counts, no weighting | the comparison is within city, so no weighting exists to choose |
| 8 | Window length | 6 months against 24 | filed; C1 across the rolling reading, measured, same designation and margin |
| 9 | Boundary inclusivity | inclusive of both endpoints | the clause states it |
| 10 | Rounding path | once, at the end, from the unrounded count | the prompt's closing sentence; asserted |
| 11 | Tie-break | the larger absolute rise | filed in the protocol; the first level resolves it at 1.69x |
| 12 | Maturity and censoring | no period open | the 30-day definitive close plus an extract dated after it; asserted |
| 13 | Order of operations | dedup then expand the day count | C1: both orders give the same action-day count, because duplicate rows carry the same day counts, asserted |
| 14 | Row order | counts are order-invariant | asserted over permutations |
| 15 | Duplicate resolution | the definitive extract's rows | the publication clause; asserted by count |
| 16 | Identity normalisation | the register's city table maps each code on the action's date | C4; the raw-code join drops three municipalities, all outside the panel, which is ask B's hazard |
| 17 | Netting against gross | no netting | actions are not offset against anything |
| 18 | Dimensional units | items in units, invoice amounts in thousands of pesos, population in units | the dictionary; C4 at a factor of 1,000 on the amount figures |
| 19 | Code and status semantics | action type and actor sector codes | the dictionary; never the stump |
| 20 | Integerisation | counts are integers; only the rate is not | rounded once, mid-bin |
| 21 | Clause scope | the designation clause covers the panel, its eligibility condition the half year alone, and the summary table's scope is the desk | filed; the summary's scope sentence is ask B's primary |
| 22 | Forward window contents | nothing is forecast; the mission is the forward act | the designation's window is closed, so no span is uncovered |

## Literal reader

Executed word for word, the protocol's designation clause and the manual's entry definition name a rise in
the actions occurring in a panel city over 1 April to 30 September 2026 inclusive against the twenty-four
months ended 31 December 2025, on the definitive extract of 5 November 2026, printed per 100,000 residents of
the 2026 projection; the entries are evidence of those actions and not the measure of them, so a reader has
to divide each city's recorded rise by something that stands for how much material reached the monitor, and
of the three volumes the record measures about itself two are produced by the recorded actions themselves
(the retained items are the items that report them and the citations are counted per action, so each ratio
returns the inverse of citations per action and contains no activity term at all) while the third, the items
the service delivered, is not; every parameter-free form of that third volume names Tibu, the elasticity
corridor runs [0.255, 1.600] with the data's own fitted value at 1.002, and the redundancy family that needs
an unfixed parameter names Teorama or Sardinata and never Tibu at any value of it, so the literal reading
lands on the golden and every differing reading either violates a quoted sentence or returns the same city.

## Oracles

| Control in the pack | What it says on the wrong path | Disposition |
|---|---|---|
| the quarterly bulletin's per-city counts for completed quarters to 2026 Q1 | ties to the definitive extract on every basis, designates nobody, and stops before the window | not an oracle; asserted to tie under the row reading and the gathering-day reading alike |
| the service's invoices (ask A's control total) | cover 2025 only, so they bear on no window figure | not an oracle for the call; they arbitrate ask A alone |
| the register's published monthly summary | agrees with the detail for every panel city on every basis, and stands above its own parts only for the non-panel desk seats | not an oracle; that disagreement is ask B's primary and sits outside the panel |
| the delivery log's own monthly totals | tie to the sum of their rows under every handling | not an oracle |
| the panel register's entry dates (`panel_fuentes.xlsx`, Municipios del panel) | names every panel municipality beside a date and says nothing about activity, volume or the designation | not an oracle; it exists so the protocol's clause 4.3 can be executed in full. Every municipality is seated before the comparison period opens, so the membership half admits all eleven and the count floor alone removes Hacari, asserted in `checks.py` and again in `verify.py`; the seating is asserted uninformative |
| a completeness audit, gold standard or certified rate | none ships | by design |

**The leak sweeps' REVIEW lines, answered** (`leak.py --asof 2026-11-05`: REVIEW, 0 LEAK, six REVIEW lines
on the final rebuild, two in sweep 4 and four in sweep 6). Sweep 4 draws its vocabulary from this note, so
which documents it names shifts whenever the note is edited; all three it has named are answered here. In the
protocol it reads the words protocol and extract, and the city name that appears there only in clause 2.1's
list of the eleven panel cities. In the data dictionary it reads the column name `action_id`, the word
extracto in the edition line and the word material in the delivery log's own row description: all three are
the vocabulary a dictionary of these files has to use, and none of them names a denominator, an exposure or a
city. In the prompt it reads the words action and record inside "recorded collective actions", which is the
quantity the question asks for and cannot be named without them. Sweep 6 reads the three register exports,
the delivery log, the city table, the road incidents and the published summary as naming every candidate
beside numbers, which is what a register and a delivery log are: none of them ranks the cities on whether
activity rose, the only aggregate among them covers 2025 at desk grain, and the one published artifact that
does aggregate by city, the bulletin, stops at 2026 Q1 and designates nobody.

## Ask sheet

Three asks, 66 graded figures, every device outside the call's declared population.

**Ask A. The service's deliveries for 2025 beside what its invoices bill, by quarter and outlet type, with a
line per item group closing each quarter's gap.** 25 figures (16 quarter x outlet-type cells, 4 quarterly
amounts, 5 reconciling groups). H18 home: an audit trail of an input the call consumes, through rows the call
never reads, to another system's control total. Use: the coordinator signs the service's invoices. Primary:
the service hands over the first days of a month's batch once the month has turned, so a delivery row can
carry the month before as its publication period, and the invoice bills the publication period while the log
is keyed by the delivery day; the register also rejected one lote wholesale in August, which the credit note
covers and the invoice does not bill. Found only by reconciling the log's own quarterly count against the
invoice's quarterly lines, and resolved only by the publication-period column and the credit note, since
re-dating the rows to their publication month also moves the delivered cells the ask asks for. Hazards: H2
(invoice amounts in thousands of pesos), H1 (outlet codes gain a service prefix in 2026). Files and columns:
the delivery log plus the invoice PDFs, 11 columns on the path. Stops, measured on the cut pack: the
delivered grid read as the billing gives 7,351, 7,599, 7,549 and 7,360 against the invoice's 7,407, 7,531,
7,598 and 7,234; every reconciling group reads zero against 82, 138, 70, 126 and 7; the amounts read in
pesos rather than thousands are out by a factor of 1,000; golden 29,859 delivered against 29,770 billed, the
gap closing in every quarter. Realism: a clipping service bills the period it published and delivers a
month's tail after the month turns; the log keeps every delivery day.

**Ask B. What the register holds for the twelve municipalities outside the panel in 2025, and in how many
months of that year it holds none.** 27 figures (12 x 2, plus 3 corridor totals). H18 home: a component the
coordinator wants before committing a mission, on rows the designation never reads. Primary: the register's
published monthly summary is built at desk grain and named by municipality, so for every two-municipality
desk the seat's count stands above its own parts and the partner's below, and the empty-month figures move
with it. Hazards: H5 (three municipalities re-coded after a merger, so a raw-code join drops them), H3 (the
2024 export's day-first dates). Files and columns: the register's detail, the summary table, the city table
with its effective dates, 12 columns. Stops: the summary as published 1,352; raw-code join 1,184; join plus
an unmatched-row drop 1,131; golden 1,268. Realism: a register publishes a monthly summary from its desk
returns, and the desks are seated in one municipality.

**Ask C. Participants per entry and in total, by actor sector, 2025, the municipalities outside the
panel.** 16 figures (8 sectors x 2). H18 home: the scale behind the register's counts, a measure every city carries that
the designation does not turn on, in a column the call never reads. Primary: where the source reported a range and no figure, the
coder leaves the numeric field empty and transcribes the range in the note, which is what the manual and the
dictionary both state; the entries are reconstructed at the range's midpoint, which every range makes a
whole participant. Radio transcripts reach every sector, so the primary reaches all sixteen figures. Hazards:
H4 (the sector code list gained two codes in 2025), H3. Files and columns: the register's participants and
note columns, the sector code list, the manual, 9 columns. Stops, measured on the cut pack: reading the numeric
column alone gives 221.7 participants per entry for the largest sector against the golden's 275.2, and
53,219 in total against 61,921. Realism: a coder
transcribing a radio report writes what was said and fills the numeric field with the lower figure.

**The separation line.** Zero device and zero hazard rows inside the call's declared population (the eleven
panel cities, action dates 2024-01-01 to 2026-09-30, the columns the call reads). Ask A's devices sit in 2025
delivery rows and the invoice; ask B's sit in the twelve municipalities the protocol does not cover; ask C's
sit in the participants and note columns, which the call never reads. `checks.py` asserts each by count, and
asserts that every main-call figure is unchanged when the participants and note columns are dropped
altogether.

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| H1 outlet code prefix from 2026 | A | 0 figures in 2025, 4 if the ask is extended into 2026 |
| H2 invoice amounts in thousands | A | 4 amount figures, a factor of 1,000 |
| H3 day-first dates in the 2024 export | B, C | 3 municipality figures, 2 sector figures |
| H4 two sector codes added in 2025 | C | 2 sector figures |
| H5 three municipalities re-coded in the national list | B | 6 figures |

**Referee.** Ask A's disagreement is arbitrated by the delivery log's publication-period column and the
invoice's own credit note, ask B's by
the city table's effective dates, ask C's by the manual's sentence on the participants column. Each says
which rows, never which value, so none hands over a level.

**Forcing, measured on the cut pack** (`generator/ceiling.py --forcing`): 37 of 37 sampled figures move
beyond the rounding their asking sentence states. Ask A's four billed quarters move by 49 to 126 items and
its five reconciling groups from zero to 82, 138, 70, 126 and 7; ask B's twelve municipal figures move by 17
to 131 gathering-days, three of them from zero; ask C's sixteen move by 18 to 56 participants per action and
by 197 to 3,721 in total.

| Ask figure group | The cracker's path | Cracker verdict |
|---|---|---|
| A items delivered, 16 quarter x outlet-type cells | reconciles the log to the invoice, finds the gap, drops by publication date | miss |
| A quarterly amounts billed, 4 | reads the dictionary's unit correctly, but the item set is still the dropped-by-date set | miss |
| A reconciling groups, 5 | reads the gap off the year rather than the quarter, so the groups that cross a quarter boundary never appear | miss |
| B actions held, 12 municipalities | takes the published monthly summary, which is the natural municipal source | miss |
| B months holding no action, 12 | same source, so the empty months follow it | miss |
| B corridor totals, 3 | sums the summary | miss |
| C participants per action, 8 sectors | reads the numeric column, which the dictionary describes accurately | miss |
| C participants in total, 8 sectors | same column | miss |

Pair ceiling: 28.5 (bar 40, build to 40), cracker 45.0 and mirror 12.0 on Part 0's weights of 38, 7 and 55;
33.0 to 34.0 at the ends of CLAUDE.md's legal bands, so the figure is not an artifact of a favourable point
inside them.
Mirror leakage: 0.0 per cent of ask weight (bar under 35). The two rows agree on the asks because every
device sits outside the call's population, which the separation assertions prove by count; what differs
between them is the call, worth 33 points.
Measured by: `generator/ceiling.py`, which sweeps the cracker's keep count and prints the pair at each: the
cracker may keep 27 of 66 figures before the pair breaches 40, and it keeps 0. Re-run on the cut pack at
stage 3, where each keep flag becomes a measured per-figure assertion that the response's own path lands
outside that figure's bin, and the gated field takes the worse measurement.

## Pricing (clean truth, `generator/core.py`)

| Screen | Result |
|---|---|
| 1 residue of the filed WHAT | a method, not a knob: which of three measured volumes stands in the denominator |
| 2 move needed vs available | 0.520 ranking units needed, 1.500 available, 2.88x |
| 3 standard error of the estimate | decisive margin 0.810 ranking units = 3.4 standard errors of the ranked quantity and 20.2 units of the lever's own noise; SE of the log rise, thinnest city 0.221, golden 0.121 |
| 4 lever vs ranked-quantity noise | two variances: the lever moves the denominator's level 2.500x while its own sampling noise is 0.0148 against the ranked quantity's 0.1188, a ratio of 102 to 1; the distance to the nearest decision boundary is 20.2 units of that lever noise |
| seed sweep, 60 seeds | decisive route names the golden 60 of 60; default path misses it 60 of 60; golden's default-path position min 2, max 4, mean 3.6 |
| knob sweep | the redundancy family's winner moves from Teorama to Sardinata as its free parameter moves, and the golden leads it at no value from 0.05 to 0.95 |
| reflex sweep | 10 of 10 reflexes name a wrong city: raw rise, per-capita rise, window level, absolute increase, per retained item, per citation, per citing outlet, redundancy capture, the export read, the summary read |
| orthogonality | inside the seven-city pool the activity multiplier correlates at most 0.43 with any static attribute; the golden sits inside the three presence risers' range on baseline capture, presence per 100,000 and citations per action, so no stratification separates it from them |
| graded figure | every candidate city's rate sits at least 0.29 of the printed unit from its bin edge on the clean truth, and the populations are re-tuned against the realised counts at stage 3 to hold every graded rate between 0.30 and 0.45 of the printed unit from its bin edge, so no rate lands on the tenth it prints |

## Single-use test

Of every file and every sentence added to force a convention: what else does the organisation use it for?

| Organ | Its other uses in the pack | Verdict |
|---|---|---|
| the delivery log (the decisive organ) | ask A reconciles it to the service's invoices; the bulletin's methodology page quotes the panel's monthly intake from it; the register's coverage appendix lists which outlets filed from which municipality; the coding desk's workload page counts items screened per coder | four other uses, one of them a graded ask, so the file is not a single-use organ |
| the manual's entry definition ("an entry exists where an action occurred and a monitored source filed an account of it") | it is the instruction coders follow when deciding whether to open an entry, and the dictionary's description of the entry table points at it; it also governs the register's own duplicate rule | not a lone sentence: deleting it leaves the designation unforced (the recorded-count reading names Sardinata and the activity reading names Tibu), so it is load-bearing for determinacy rather than announcement, and the fork is measured in SF12 |
| the protocol's designation clause | it also sets the panel, the publication cycle, the tie-break and the mission's funding, and the coordinator's own role is defined in it | not single-use |
| the invoice PDFs | the coordinator signs them; ask A's control total | not single-use, and they cover 2025 only, so they bear on no window figure |
| the published monthly summary | the bulletin is built from it and the register's own returns process produces it | not single-use; it is ask B's primary and agrees with the detail for every panel city |
| the panel register's municipalities sheet, with each one's panel entry date and semester | the register the panel is administered from: clause 2.2 of the protocol creates the fact (a municipality enters at the start of a semester and stays while monitoring is continuous), the workbook already holds the other half of the same register in its source sheets, the semestral ficha review at the close of each semester runs off it, and the semester label is how the coordinator knows which municipalities a given semester's note covers. Clause 4.3 is one consumer among those | not single-use, and it points at no part of the decisive step: it names no volume, no denominator, no exposure and no city's activity. The deletion test was run and is the measurement below: with the sheet gone the answer is forced exactly as before, because the clause it serves is the eligibility threshold, which is asserted inert and which no route's answer turns on. The contrast with the cut Notas sentence is the point: that sentence's only work was to stop a reader inferring coverage from declared scope, which is the decisive denominator, while a date register serves a membership clause |
| the panel workbook's note that the declared scope is self-reported and does not describe the volume a medium sends | none: a ficha sheet documents its own columns, and warning a reader off a volume it does not carry is work no panel sheet does | single-use, and cut. The deletion test settles it: the sentence is read by nothing, so with it gone the designation, the printed rate, all four call components, every rung and all eleven city rates are identical (target tree unchanged but for the four documents this pass edited), which means it was handing over the insight rather than forcing anything. What is left is the ficha's own column descriptions, including the delivery channel the sheet already distinguishes |

## Stage 3 findings answered

| Finding | Where it came from | What was done |
|---|---|---|
| The generator attributed a multi-day action's days to its start date while the shipped rows carry each gathering-day on its own date | `verify.py`, on its own code path | The generator was changed to the shipped rows' convention, which is the manual's unit; the designation and every rung held, and the populations were re-tuned against the corrected counts |
| The published monthly summary and one assertion still used the old convention | the same verifier run | Both were moved to gathering-days on their own dates |
| The export manifest declared every file "sintetico", a statement inside the bundle that the world was built | `reduce-house-fixes` H24 | Rewritten as the area of the Observatorio that delivers each file; `verify.py` now asserts the manifest stays inside the fiction and covers the shipped set |
| `leak.py` returned LEAK on two documents | sweep 2, author vocabulary | Both were the sweep's English TODO marker matching the Spanish word "todo" in ordinary prose. The four sentences were reworded without it; the clauses' force is unchanged and the verifier's controls were re-pointed. The sweep cannot tell the two apart, which is worth knowing for any Spanish-language pack |
| `guard.py surface` found a persona "Campo Plantilla" | the surface screen | The manual's table header read as a name; the column was renamed and the screen now finds only the two carded personas, who sign the protocol and the manual |
| The eligibility condition excluded nobody once the thin cities were thickened, leaving a graded column with eleven identical values | the golden's own figures | The protocol's floor was raised to seventy actions, which removes Hacari at 56 and nobody else, with the nearest other city 16 actions clear of it; the condition stays inert for the call, asserted |
| Nine ask-A cells and six ask-B rows in the write-up were typed rather than read | `figures_check.py` | Every line in block 4 is now emitted from `figures.json`, and the units and clause numbers the write-up names are emitted with them |
| Six of ask C's eight "largest single action" figures did not move: the biggest action in a sector is usually not one the coder recorded as a range | the forcing measurement on the cut pack | The figure was replaced by the sector's total participants, which the device moves in all eight sectors by 197 to 3,721, and the ask's unit was tied to the register's own entry (the 2025 export holds one per gathering-day, as the dictionary states) so the term carries no second reading |

## The judge's FIX_NOW, answered

The first six rows are pass 1, from the judge's first NOT_DETERMINISTIC. The rows under them are pass 2,
which the judge returned on ask 4 alone with everything else forced, and the leak reader's own findings from
the same round.

| Finding | What was done |
|---|---|
| Ask 6's data contradicted the manual: all ranged entries held the range's low end in `participantes_est` while the manual promised a central estimate, and the committed figures reproduced only if each midpoint was floored before summing | The coder now leaves the numeric field empty where the source reported a range and no figure, which is what the manual and the dictionary state, and every range is drawn so its endpoints sum to an even number, so the midpoint is a whole participant and nothing has to be floored. The reconstruction and its grain are pinned in the asking sentence ("the participants per entry and in total for each actor sector, taking the midpoint where only a range is held") and the closing rounding clause now covers each class: actions, items and participant totals whole, participants per entry and every rate to one decimal |
| Ask 4's "with a line for each difference" equally carried the per-quarter arithmetic deltas | Reworded to "with a line for each item reconciling the gap" |
| The chart ask was internally inconsistent: bars of gathering-days per 1,000 items received cannot carry a line at 1.00, which belongs to the ratio | The bars carry the ratio of the half year's gathering-days per item received to the same figure over the comparison period, the axis says so, and the write-up's description matches |
| Step 5 said the retained-items and citations denominators both rank Teorama first | Measured on the cut pack: citations rank Teorama first with the golden fourth at 1.071, while retained items rank the golden first at 1.658. Step 5 now names the citations route alone, and the ladder and readability rows say the same |
| Seven graded figures sat inside the bin-edge floor, the worst being the designation ratio at 0.00013 and a sector mean on an exact tie at 330.85000 | No ratio is graded anywhere now: the chart prints no per-bar value, block 1 states the call on the four integer components instead, and the steps name the ordering rather than the ratios. The sector means are held clear by a deterministic pass in the generator that adjusts one plain entry per sector until the mean clears 0.3 of the printed unit and does not print round; the tightest is now 0.30 of the unit |
| The leak reader's three quotes | The bulletin's methodological note is cut to one sentence, its "no compara municipios entre si ni anticipa la designacion" is gone, and the dictionary's line telling the analyst which two files do not enter the register is replaced by a plain listing. Protocol 4.1 is untouched: deleting it would open the Gate C fork the judge certified closed, and it names no normaliser, no city and no file |
| Pass 2, ask 4, Gate C and E: "a line per reconciling item" had three defensible readings on this pack, and each gives a different line set. Measured on the cut pack: the annual delivered-against-billed gap of 89 is closed by two lines, 82 and 7; the shipped golden's three lines, 82 / 125 / 7, close a publication basis of 29,902 against 29,770 and not the delivered one, because the 125 items published in December 2025 reach the service in January 2026 and so are neither delivered nor billed in 2025; and the quarterly gaps, which is the grain the prompt's own table is asked at, are closed by five, 82, 138, 70, 126 and 7 | The asking sentence now pins the basis and the grain: "with a line per item group closing each quarter's gap". The quarterly bridge was verified first, since a reconciliation at a coarser grain than its own table does not reconcile it: it closes exactly, T1 7,351 less 7,407 = 82 less 138, T2 7,599 less 7,531 = 138 less 70, T3 7,549 less 7,598 = 70 less 126 plus 7, T4 7,360 less 7,234 = 126, so the annual fallback was not needed. Exactly one line set survives: the two-line annual set closes none of the four quarters and the 125 forms no group at all. The golden workbook now carries a Diferencia column and one line per group with the quarter it was delivered in and the quarter the invoice bills it in; `checks.py` asserts the closure per quarter as SF14 and `verify.py` recomputes it from the shipped bytes, deriving the credited mesa's pair from the published summary. Nothing else in ask A moved: the 16 cells, the four delivered totals, the four billed counts and the four amounts are byte-identical |
| The leak reader's single-use finding: the panel workbook's Notas sheet warned that the declared scope "no describe el volumen que remite", which is work no ficha sheet does and which points at the decisive denominator | Cut, with the deletion test run first and recorded in `## Single-use test`: the sentence is read by no computation, so with it gone every call figure, every rung and all eleven rates are identical, which is what makes it an announcement rather than a closure. The sheet keeps its own column descriptions and gains the one it was missing, that the delivery channel distinguishes the primary mesas from the ones the team consults. The dictionary's `items_entregados` line also loses "sea cual sea el tema", which the rest of the line already says: the two column descriptions still separate what the service delivered from what the register's filter kept, which is what closes SF8 |
| Three dictionary statements were not true of the shipped data: a citation table where 13 `id_item` values cite two entries each was described as one entry per item; a header claiming to describe the definitive extract while the 2026 export ships 320 preliminary rows; and three re-coded municipalities described as a merger of two entities that nothing in the data shows | All three were fixed in the sentence rather than the data, because each piece of data is load-bearing Layer 1 mess: the citation line now reads "un item puede citar mas de una entrada", the header describes "los archivos del extracto de esa fecha" and leaves the `extracto` column to say which rows are preliminary, and the city table's line now says the national list reassigned three codes. The register's rows, the citation table and the city table are byte-identical |
| Two realism tells: all eleven city rates sat within 0.00004 of an exact tenth, and the Mujeres organizadas per-entry mean was exactly 356.500 | `tune_population` now runs two deterministic passes: the first fixes the printed rate exactly as before, the second keeps that printed rate and moves the projection off the bin's centre to a per-city offset, so the ten tunable rates sit 0.007 to 0.017 from the tenth they print and 0.30 to 0.43 of the printed unit inside their bins. Every printed rate is unchanged. The designated city is the exception by scope: its projection of 148,590 is a Critical Components figure and its printed 92.2 is the call, so the denominator is pinned in `PINNED_POP` and its rate still sits on the printed value, which `checks.py` asserts as the pinned case. The sector-mean pass gained the same off-centre condition and now adjusts a one-day entry, because a prolonged entry carries its figure on every day it ran and the mean then steps in multiples that skip the band: Mujeres organizadas is 356.2 on a total of 5,699 and Transportadores 61,922, and no other sector figure moved |
| The reader's two smaller observations, judged, and the author's ruling on the first | Protocol 4.3's panel-membership half and the 4.4 tie rule could not be executed because no file gave a panel entry date. Both are measurably inert: the count floor alone removes Hacari at 56 actions, the nearest other city sits 10 actions clear of it, the tie rule never fires at a decisive margin of 1.8150x, and every one of the eleven panel cities holds at least one action in every one of the 24 baseline months. Inert is not enough, because a clause in a governing document that cannot be executed from anything in the pack is the shape of a Gate B missing-input finding, so on the author's ruling `panel_fuentes.xlsx` gained a Municipios del panel sheet carrying each municipality's entry date and semester, and the dictionary's line for the workbook names it. The three conditions on it are met and measured: it moves nothing (every one of the 199 `figures.json` values identical, and every city's window and baseline counts, delivered volumes, population, rate and all four rung scores identical to six decimals, winners, position, margin and lead with them); it passes the single-use test, recorded above with its deletion test; and the seating is varied and uninformative, eight distinct semester starts from 2017-II to 2022-I, the golden on 2020-II shared with Hacari and neither the earliest nor the latest, the three presence risers on three different dates, and the newest and oldest members both cities that no route's answer names. The manual's misplaced layout table was cheap and is fixed: the field-by-year table now sits under section 2 as clause 2.4, where the template fields are described, and section 3 keeps its own sentence about the monthly sample review |

**Pass 2's gates, measured on the final rebuild.** `checks.py` exit 0, 127 checks, 127 PASS, 0 FAIL (100
before; the 27 new ones are the SF14 closure, the two off-centre bands, the pinned projection and the panel
register's six invariants). `verify.py` exit 0, 91 checks, 91 PASS, 0 FAIL (76 before), reading only the
shipped bundle, deriving the credited mesa's pair from the published summary and executing clause 4.3 on both
halves from the panel register. `figures_check.py` exit 0, 124 figures in blocks 1 to 4, 0 absent
from `figures.json`. `precut.py` exit 0, 51 checks, 0 FAIL, 0 WARN, the new no-repeated-H2 check among them: this note carried a second copy of two sections inside the Draw table's last row, which left the earlier copy unread, and the duplicates are removed and the row restored. `voice-check.py` exit 0, 13 checks PASS,
`prompt.txt` 995 characters, unchanged in length, with the call sentence byte-identical. `ceiling.py` pair
ceiling 28.5 on 66 graded ask figures (bar 40), mirror leakage 0.0 per cent, the cracker keeping 0 of 66 and
able to keep 27 before the pair breaches 40; `--forcing` 37 of 37 sampled figures move beyond their stated
rounding. `leak.py --asof 2026-11-05` REVIEW, 0 LEAK, six REVIEW lines answered in `## Oracles`. `guard.py
surface` clean, 0 pairs promoted, the personas found are the two on the card; `guard.py heart` WARN, 0 BLOCK,
nearest driver 0.06. Two consecutive full rebuilds byte identical: target tree
`16ee337366733892eba5aa3a64fa2b68`, golden `e93d935ac77539eee0cf0ac608a63a50`, `target.zip`
`97dd76fb2a5658bfa2746afc7f23baa1` with 17 members, re-cut from the final rebuild. Before the panel register
sheet was added the same three digests were `cbb36f20c8baff69042eb85e72810d25`,
`e93d935ac77539eee0cf0ac608a63a50` and `365b1d62dd2d6206f39bb9a4178eec30`: the golden is unchanged by it,
which is the first of the three conditions the sheet had to meet.

**What moved in the pack.** Four documents and one data file: `diccionario_datos.md` (four sentences plus
the line naming the panel register sheet), `panel_fuentes.xlsx` (the Notas sheet and the new Municipios del
panel sheet),
`manual_codificacion.pdf` (the layout table moved to clause 2.4),
`proyecciones_poblacion.xlsx` (ten projections, every printed rate unchanged) and `rac_acciones_2025.csv`
(nine rows' `participantes` values, in Rio de Oro, San Martin, Chimichagua and Pelaya, all outside the
panel). Byte-identical: the delivery log, the invoices, the protocol, the 2024 and 2026 register exports, the
citation table, the published monthly summary, the city table, the bulletin, both distractors and the export
manifest. In `figures.json` 191 of 202 keys are unchanged, the three `ask_a_differences` keys are replaced by
the five `ask_a_lines` keys, and the only values that moved are ask C's Mujeres organizadas pair and
Transportadores total.

**`freeze.py check --mode rubric`, run after the rebuild against the snapshot pass 1 took** (not retaken,
because a snapshot retaken at the end of a repair proves nothing about the repair): exit 1, the same two
frozen items as before this pass and no others, both of them pass 1's and both recorded above. The Final
Recommendation numbers moved when pass 1 replaced the two ratios with the four integer components on the
judge's own FIX_NOW, and the ladder section moved when pass 1 corrected its row to the measured fact that
only the citations route names Teorama. The allow list reaches `figures.json` keys only, so neither can be
expressed in it and neither was suppressed. On the ask side it reports both deliverable files and 24 ask
figures moved, 8 more than before this pass, which are exactly the three retired and five added reconciling
keys. Everything the mode freezes and this pass could have touched is unchanged: the Critical Components
numbers, every main-call `figures.json` key, the stump sentence, the card's stump and driver, the default
path and the prompt's call sentence.

## Tried and rejected

- Multi-source deduplication against the coding manual: the decisive step would be executing the manual,
  which is rule application and banned as the decisive step. Rejected before the draw.
- One-sided reporting of ongoing against ended episodes: maturity censoring, banned against the last three
  builds and live on task194. Rejected before the draw.
- A capture estimate from the overlap of two sources: task196's family. Rejected before the draw, and the
  pack deliberately carries no second channel.
- A completeness audit as the calibration organ (past verification missions reconstructing a city-month from
  local archives, against which the candidate volumes could be validated): dropped, on its own reasoning
  rather than despite it. It would have forced the method cleanly and handed over the insight that
  completeness differs by city, which is the readability screen's control-bench test firing, and
  `stumping` Part 7 bars a corpus that refutes the naive read. Forcing the method by the data's structure
  instead is the stronger closure and the one `determinism-check` ranks first: the retained-item and citation
  volumes contain the action count by construction, the redundancy family needs a free parameter the pack
  does not fix, and every parameter-free presence form agrees, with the elasticity corridor measured at
  [0.255, 1.600] against a fitted 1.002.
- Pattern E (conditioned yield) on the card: BLOCKed by `ban.pattern` against task166 and by both older
  structural tests. The pattern axis was redrawn to G12 with Gate G decomposition_attribution rather than
  argued, which also moved the signature off task192's.
- Small municipalities (10,000 to 40,000 residents) as the candidate set: the ranked quantity's standard
  error reached 0.39 and the seed sweep fell to 34 of 40, so the ranking would have been a tuned seed rather
  than a designed mechanism. Replaced by eleven intermediate cities and a six-month window.
- The golden as the largest and highest-rate city in the candidate pool: a one-period group-by on the
  window's rate, and a rank on population, both reached it for free. Its population and activity were moved
  so that it sits fourth on the window rate and fourth by size, and inside the wrong candidates' range on
  every static attribute.
- An activity multiplier of 1.86 on the golden: the weakest licensed form of the decisive route (exposure at
  the square root of delivered items) gave a margin of 1.18x, close to the 1.15x floor. Raised to 1.98, which
  lifts that form to 1.25x and the per-item form to 1.69x without moving the golden off fourth place on the
  default path.
- A delivery-log device for an ask (a desk whose log rows carry the desk seat rather than the item's own
  dateline): drafted and held, because as drafted it changes the delivered-item count for panel cities, which
  moves the call. The safe construction, confining it to desks that serve only non-panel municipalities, is
  recorded here and is to be measured before cutting rather than after.
- The stump strategy label population_selection and the forcing event audit_or_inspection: both BLOCKed at
  stage 2 when a later registration moved task245 into the last three (task190 is paused with its ground
  banked, not retired, and a retirement would not reorder the window in any case: the window is ordered by
  filing time). Redrawn to
  causal_design and period_close, which are the honester labels: conditioning on the retained-item or
  citation volume is conditioning on a descendant of the count being tested, which is a control choice, and
  the designation falls due because the half year closed on 30 September and the definitive extract on 5
  November.
- Shape 01: BLOCKed by `ban.shape` at stage 2, after task198 re-rooted and re-registered later the same
  day, which moved task471 (shape 01) into the last two builds. The axis was redrawn to 10 rather than
  argued, and 10 is the honester label anyway: the criteria come from five checks on each of eleven cities,
  the mission is a maximum rather than a cap that runs out mid-list, and 10's hard seam is different
  denominators per metric. The protocol's eligibility condition supplies the threshold column and is
  asserted to remove no city any route names, so no stated check decides the call.
- Grading any ratio: the decisive ratio printed to two decimals sat 0.00013 from its bin edge and five
  per-city ratios were inside the floor, and the only lever that could move them is the delivery log, which
  is the main-call surface and had to stay byte-identical. Cutting the ratios from the graded surface was
  the available fix and it costs nothing: the call is stated on the four integer components, the chart
  keeps its ordering, its line at 1.00 and its annotation, and `freeze.py check --mode rubric` is run with
  the ratio keys allowed for this reason.
- The sixth pricing screen, run on this pack before a row was cut: a short pre-window baseline isolates the
  golden with no denominator at all, but only where press presence has already moved and activity has not.
  Measured in `core.screen6`: with presence stepping first the raw comparison against the quarter before the
  window names Tibu at position 1, with both stepping together it names Sardinata and puts the golden fourth.
  Every presence shift and the activity rise therefore step on 2026-04-01, every pre-window and sub-window
  month carries the baseline's own levels, and the invariant is asserted. The screen's other two subsets do
  not fire: the highest retained-over-delivered ratio anywhere is 0.059, so the wrong denominator never meets
  the right one, and the thinnest panel city-month holds hundreds of delivered items, so presence is never
  readable off an absence.
- The generator seed: 40 seeds were scanned against the stage-3 floors (the golden fourth or fifth on the
  default path, a decisive margin of at least 1.30x, a default-path leader at least 1.20x ahead, four
  distinct rung winners, the citation route on Teorama). Three cleared them and the first, 230875, was taken.
  The decisive route named the golden in 80 of 80 seeds before the search, so the search chose among seeds
  that all carry the same answer rather than searching for one that produces it.
- A per-sector action count in ask C and an agency column free of ask A's primary: both were figures free to
  every response by construction, diluting the criteria beside them. The action count is not asked for at all
  and the re-push was re-sited as the contract's monthly completeness run, which reaches every batch.
- Closing ask 4 by pinning the basis alone, leaving the grain to the table: rejected, because that is the
  reading the judge returned. The sentence has to name the grain, since the annual bridge and the quarterly
  bridge are both defensible on a table asked by quarter and they give two different line sets.
- The annual two-line bridge (82 and 7) as the pinned reading: rejected on the measurement rather than on
  taste. The quarterly bridge closes exactly, and a reconciliation coarser than the table it reconciles
  leaves three of the four quarterly gaps unexplained, so the richest grain that closes is the one the ask
  takes. The annual fallback was written into the repair's order and was not needed.
- Keeping the shipped 125 line by pinning the publication basis instead: rejected. It would have moved the
  billed side off the invoice's own quarterly lines, which this repair holds byte-identical, and the prompt
  asks for what the invoices bill rather than what the service published.
- Moving the designated city's projection off the printed tenth with the other ten: rejected. The projection
  148,590 is a Critical Components figure and the printed 92.2 is the call, both frozen by the repair's
  scope, so one rate of eleven still equals the tenth it prints and the generator pins it rather than
  leaving the tuner to re-derive it.
- Nudging a sector mean through a prolonged entry, as the pass did before this round: it adds the entry's
  figure once per day it ran, so the mean moves in multiples of the day count and can step over the whole
  band between the bin's centre and its edge. Mujeres organizadas alternated between the centre and the edge
  for 400 iterations and the pass raised rather than converged. One-day entries only.
- Leaving protocol 4.3 inert and shipping no panel entry date, which is what this pass first proposed on
  the measurement that the clause removes nobody: overruled by the author, and rightly, because an inert
  clause and an unexecutable one are different findings. The portal's judge reads a governing clause it
  cannot execute from the pack as a missing input, so the register now carries the date and the clause can
  be executed on both halves. The three conditions the sheet had to meet are measured in the row above.
- Seating every panel municipality on one date, or on dates drawn from anything the call reads: rejected.
  The seating is drawn from the municipality's name alone and asserted uninformative, because a register
  whose dates line up with the answer is a decoy in a file the solver has every reason to open.
- Putting the entry date on the panel workbook's source sheets as a column: rejected on the data's own
  structure. Those sheets are the panel of monitored outlets, one row per medium, and clause 4.3 is about a
  municipality's membership, so the fact belongs in its own sheet of the same register rather than bolted to
  a row about a newspaper.
- Correcting ask A's primary sentence to the mechanism the generator actually builds: the sheet described a
  monthly completeness re-push under fresh item ids resolved by the transmission batch, and what the pack
  carries is the publication period against the delivery day plus the credited lote. No data changed; the
  sheet now describes what the cut pack contains, which is what the forcing measurement reads.
- Architecture 1 as a whole, the delivered-item exposure as the decisive step: refused at the wave 7
  triage on measurement, not on taste. Three screens, each run twice byte-identical on the clean truth
  and on the shipped pack. (1) The standing family, knobs and hats removed and groupings counted, is 8
  constructions and returns one designation, 137 action-days and 92.2 per 100,000: spread exactly zero
  on every graded figure of the call, against an enumerated family of 20 constructions, 3 designations
  and 717 printed units of spread. (2) The construction is an identity, log(score) = log(raw rise) minus
  log(delivered-item rise) to 2.22e-16, so it is two group-bys and one subtraction. (3) A four-axis dial
  sweep over 576 cells passes 0 cells jointly, with the one-exclusion route landing the call in 576 of
  576. The step is a reflex that one filed sentence and one dictionary page select; it is not an analysis.
- A magnitude fix on the risers' feed multiplier, in either direction: measured dead before it was
  drafted. On the eight cities whose feed did not move the designed score equals the raw rise (mean 2.87
  per cent apart, identical order, correlation +0.993114), so dropping the three risen feeds and ranking
  the remaining eight on the raw rise names the golden at 1.637x with the same 137 and the same 92.2. The
  risers' multiplier appears in neither ranking's top element, so it cannot separate the two routes:
  turning the lever down hides the trap and leaves the route that lands the call untouched, and turning it
  up only makes the three risen feeds louder (they already sit at 5.8x to 7.0x per semester against 0.97x
  to 1.10x everywhere else, which the group-by ask A already requires separates at a glance).
- A clause removal on protocol 4.1, leaving the measure of the rise to the data: rejected on the note's
  own deletion test, which records that without the forcing sentence the designation is unforced
  (Sardinata on the recorded-count reading, Tibu on the activity reading). The sentence that announces the
  decisive step is the sentence that forces the call, so removing it trades a Gate F failure for a Gate C
  failure. The same pincer measured from the data side: a Poisson-offset profile of the rival exposure
  bases against the record's 5,711 events puts the golden's own base third of four, 184.36 in `2 dlogL`
  behind retained items, so the data cannot take the clause's place.
- The saturating presence form counted as a parameter-free member of the decisive family (the `## Ladder`
  row's "saturating 1.28x"): wrong, and it hid a fork. Its scale is a free knob, and swept over four
  orders of magnitude on the shipped pack it names Sardinata at every scale up to about 1,500 (where it
  is the raw rise, fully saturated) and the golden only from 3,000 up (where it is the per-delivered-item
  route). At the shipped volumes with the note's own scale of 700 it names Sardinata at 1.142x. The
  member was one of the other two wearing a hat, and neither the judge nor the leak reader tested it.
- The clean truth's own retained-item route as evidence that a second exposure measure agrees: it does not
  agree. `core.routes` builds retained items as citations times 1.18, so on the clean truth the
  retained-item route is algebraically the citation route and names Teorama at 2.778, while the pack
  builder gives retained items an additive near-miss term that scales with delivery rows, so on the cut
  pack it names the golden at 1.140x. The `## Ladder` paragraph's "the retained-item route ranks the
  golden first at 1.658" is a cut-pack artifact of that unmodelled term, not a designed property, and
  1.140x is under the 1.15x floor besides.
- The rung floor as shipped: three of the five wrong rungs sit inside it on the cut pack, so the default
  path is not a stopping point. Raw rise 1.142x, raw rise in its count form 1.142x, absolute increase
  1.083x, retained items 1.140x; only the window level (1.182x) and the citation route (1.587x) clear. A
  solver who computes the raw rise sees Sardinata barely clear of Convencion and El Tarra and is sent on,
  which is where the one remaining step is the answer. On the clean truth the same clearances are 1.052x,
  1.052x, 1.029x and 1.008x. The dial sweep clears the floor in 2 of 576 cells and 116 cells fail on it
  alone, so it is spendable only by widening the risers' spread tenfold, which makes the trap louder still.
- Resuming this architecture at all: blocked by the free gate independently of the measurements. `guard.py
  heart task199` now reads HEART VERDICT: BLOCK with three BLOCKs the corpus grew after this build shipped,
  `ban.shape` on shape 10 against task245, `ban.strategy` on causal_design against task163, and
  `test.same_puzzle_older` on gap, pattern and decision type against task268 v2 with no differentiation on
  the card. A re-root has to redraw the shape and the strategy whatever it does with the ground.
- **(2026-10-25, measured) Re-measured with the scorer: call landed and ask layer whole.** `score_reader.py` on the stored reader answers: **2 of 2 call figures hit** (Tibu, 92.2 per 100k) and **4 of 4 ask figures (100.0 per cent)**, with the call's window input also hit. The construction being an identity is the diagnosis this note already carries; the reader is the independent confirmation, and it rules out an ask-only repair.
