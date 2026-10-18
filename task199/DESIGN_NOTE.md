# task199 design note

Collective-action register, Catatumbo and middle Magdalena corridor. Anomaly Detection & Diagnostics.
Stage 2. Every number below is printed by `generator/core.py` or `generator/ceiling.py`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task199.json`, registered 2026-10-18, `guard.py check` WARN, 0 BLOCK |
| Domain / subdomain | political-science-public-policy / conflict-protest-event-data-analysis (client domain, task type serves anomaly-detection in the taxonomy) |
| Objective | anomaly-detection: a real event separated from an artifact |
| Shape | 10, scorecard against thresholds. 11 cities x (window actions, baseline actions, rate per 100,000, eligible, designated) = 55, plus call, runner-up, gap, flip = 4, plus a chart's 5 named parts, plus 2 deliverables, plus 64 ask figures |
| Decision | pick_one_of_n: the one city the next verification mission goes to, named in the watch note with its recorded rate |
| Gap / pattern / generators | population (a row is a reported action, not an action) / none / G12 decisive, G14, G16 |
| Gate G | decomposition_attribution: every city's recorded rise is correctly reported, and the call turns on assigning it to press presence or to activity |
| Strategy / Layer 2 | causal_design (the exposure must not be caused by the outcome) / estimand_identification, client pattern political-science-public-policy/conflict-protest-event-data-analysis/1 |
| Decision-type WARN | pick_one_of_n repeats whichever build is filed immediately before this one (task198 v4 at filing, task166 earlier the same day): answered, because the call is a mission allocation among eleven recorded candidates, the records-fixed shape this wave's rules prefer over an estimator output, and task166 differs in domain, objective, gap, pattern, Gate G and driver at 0.05 similarity |
| Calibration organ | none, by design (see `## Stage 3 findings answered

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

| Finding | What was done |
|---|---|
| Ask 6's data contradicted the manual: all ranged entries held the range's low end in `participantes_est` while the manual promised a central estimate, and the committed figures reproduced only if each midpoint was floored before summing | The coder now leaves the numeric field empty where the source reported a range and no figure, which is what the manual and the dictionary state, and every range is drawn so its endpoints sum to an even number, so the midpoint is a whole participant and nothing has to be floored. The reconstruction and its grain are pinned in the asking sentence ("the participants per entry and in total for each actor sector, taking the midpoint where only a range is held") and the closing rounding clause now covers each class: actions, items and participant totals whole, participants per entry and every rate to one decimal |
| Ask 4's "with a line for each difference" equally carried the per-quarter arithmetic deltas | Reworded to "with a line for each item reconciling the gap" |
| The chart ask was internally inconsistent: bars of gathering-days per 1,000 items received cannot carry a line at 1.00, which belongs to the ratio | The bars carry the ratio of the half year's gathering-days per item received to the same figure over the comparison period, the axis says so, and the write-up's description matches |
| Step 5 said the retained-items and citations denominators both rank Teorama first | Measured on the cut pack: citations rank Teorama first with the golden fourth at 1.071, while retained items rank the golden first at 1.658. Step 5 now names the citations route alone, and the ladder and readability rows say the same |
| Seven graded figures sat inside the bin-edge floor, the worst being the designation ratio at 0.00013 and a sector mean on an exact tie at 330.85000 | No ratio is graded anywhere now: the chart prints no per-bar value, block 1 states the call on the four integer components instead, and the steps name the ordering rather than the ratios. The sector means are held clear by a deterministic pass in the generator that adjusts one plain entry per sector until the mean clears 0.3 of the printed unit and does not print round; the tightest is now 0.30 of the unit |
| The leak reader's three quotes | The bulletin's methodological note is cut to one sentence, its "no compara municipios entre si ni anticipa la designacion" is gone, and the dictionary's line telling the analyst which two files do not enter the register is replaced by a plain listing. Protocol 4.1 is untouched: deleting it would open the Gate C fork the judge certified closed, and it names no normaliser, no city and no file |

## Tried and rejected`) |
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

- Task type: conflict-protest-event-data-analysis, which the client taxonomy gives anomaly-detection and
  descriptive-distribution; this build takes the anomaly-detection reading, a real escalation separated from
  a reporting artifact.
- Domain test: the deciding quantity is protest incidence recovered from a media-sourced event record, which
  conflict-event analysis estimates by conditioning event counts on reporting intensity, the field's own
  pattern 1 for this task type and the reason every published protest-event series carries a media-reach
  caveat; the estimator is a rate of recorded actions per unit of press material reaching the monitor,
  compared with the city's own earlier rate.
- Swap: "which city's protest activity rose, as against the volume of press material reaching the register
  from it" becomes, with another field's nouns, "which hospital's falls rose, as against the volume of
  incident forms reaching the registry from it", and it stops making sense, because an internal incident
  system has no outside reporters whose filing volume the record separately measures, no citations per event,
  and no gap between an event happening and an account of it reaching a coder.
- Layer 1: the register ships as yearly exports whose columns were renamed in 2025 and whose dates change
  format (the office's own export tool, revised between calendar years); the preliminary and definitive
  extracts of three 2026 months overlap (the publication cycle); the 2026 template records a day count where
  earlier templates wrote one row per day (a template revision); city keys arrive as names and as divipola
  codes with one code reassigned after a merger (the national coding standard); population projections ship
  in thousands on one sheet and units on another in two vintages (the statistics office's release practice);
  the quarterly bulletin's figures sit inside PDF tables; outlet codes carry a service prefix in the 2026
  delivery file only; the ingest stamp is UTC while the action date is local. Nothing is placed to be caught
  and none of it changes which city is designated.
- Layer 2: estimand_identification. The recorded count is the product of how often actions happen and how
  reliably an account of one reaches the monitor, and the decisive choice is which of the record's own
  measured volumes may stand for the second factor.
- Decisive step: condition each city's rise on the press material the monitor received from that city, the
  one volume in the record that is not produced by the actions themselves, rather than on residents (which
  cancels out of a within-city rise), on the items retained for screening, or on the citations the register
  holds per action.
- Not semantics: every field, code, unit and date can be read correctly and the easy route still files
  Sardinata; the data dictionary defines all three volumes accurately, nothing in any definition says which
  one belongs in a denominator, and the two wrong ones are wrong for a structural reason, that they contain
  the action count by construction, which no reading of a field reveals.
- Not rule application: the protocol files the designation's population, outcome, window, unit and
  comparison, and no filed rule, formula or procedure performs the conditioning or names a volume; executing
  every stated rule gives the eleven cities' recorded rises against their own baselines, which is the default
  path's wrong answer.
- Analyst test: with every field read, every date and code resolved and the protocol's window and unit
  applied, the easy route compares each city's half-year actions with its own baseline and files Sardinata,
  121.4 actions per 100,000 residents; the obvious correction, dividing actions by the register's own protest
  material, files Teorama, whose citations fell by two thirds when one outlet stopped republishing. `checks.py` executes
  both on the clean truth and asserts the named wrong answers, then changes the denominator alone and asserts
  the golden.
- Estimand: the protocol's designation clause fixes the population (every action the register holds for the
  eleven panel cities, all sources, single-source actions included, on the definitive extract of 5 November
  2026, with actions not yet registered at that date outside it because every window month has passed its
  30-day definitive close), the outcome (a rise in the actions occurring in the city, for which the
  register's entries are the evidence and not themselves the measure), the window (1 April to 30 September
  2026 inclusive against the twenty-four months ended 31 December 2025), the unit (one gathering, on one day,
  at one place, with the printed figure per 100,000 residents of the 2026 projection) and the comparison (the
  city against its own record over the baseline), and the candidate set (a city is eligible where the
  register holds at least thirty actions for it in the half year and the city has been in the panel for the
  whole of the baseline, which removes Hacari at 25 actions and no other city, and removes nobody any route
  names).
- No decoy: nothing is planted to be caught; no memo, draft or stakeholder figure argues for any city, no
  block of records is copied, no rule is withheld, the quarterly bulletin reports completed quarters as it
  always has and designates nobody, and the three cities whose press presence rose have unrelated causes
  which no shipped sentence states.
- No certified replay: no certified, published or closed figure in the pack is reproduced by the wrong
  method, and no bench blesses a method; the pack ships no completeness audit at all.
- Lesson: an exposure measure has to be independent of the outcome being measured, because a denominator the
  outcome itself produces subtracts the signal; no build on file teaches it, since the five nearest builds
  all estimate what a record is missing and none turns on which measured volume may normalise a rise.

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
| SF8 | items the clipping service delivered | items delivered, all topics | items retained for screening | the ask's own words and the delivery log's two column descriptions |
| SF9 | municipality outside the panel | the register's city table, on the action's date | the published monthly summary's municipality column (desk grain) | ask B's primary: the summary stands above its own parts for every desk seat, measured |
| SF10 | participants per action | the total participants over the actions holding a participant figure | counting unreported participants as zero; the numeric column's lower bound | the manual's sentence that the column carries a central estimate, and the note field holding the range |
| SF11 | rate | actions over residents, rounded once at the end | rounded per month then summed | the prompt's closing rounding sentence governs the printed figures only |
| SF12 | the material reaching the monitor | the delivered-item count for the city and month | the retained-item count; the citation count | not closed by any sentence: this is the open HOW, forced by the data's structure (see `## Literal reader`) |

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
| a completeness audit, gold standard or certified rate | none ships | by design |

**The leak sweeps' REVIEW lines, answered.** Sweep 4 reads three design-note terms in the protocol: two are
the words protocol and extract, and the third is Sardinata, which appears there only in clause 2.1's list of
the eleven panel cities. Sweep 6 reads the three register exports, the delivery log, the city table, the road
incidents and the published summary as naming every candidate beside numbers, which is what a register and a
delivery log are: none of them ranks the cities on whether activity rose, the only aggregate among them
covers 2025 at desk grain, and the one published artifact that does aggregate by city, the bulletin, stops at
2026 Q1 and designates nobody.

## Ask sheet

Three asks, 64 graded figures, every device outside the call's declared population.

**Ask A. The service's deliveries for 2025 beside what its invoices bill, by quarter and outlet type, with a
line for each difference.** 23 figures (16 quarter x outlet-type cells, 4 quarterly amounts, 3 difference
lines). H18 home: an audit trail of an input the call consumes, through rows the call never reads, to another
system's control total. Use: the coordinator signs the service's invoices. Primary: the contract's monthly
completeness re-push, so items that failed checksum arrive in the next month's batch under fresh item ids
with their publication dates kept, while the invoice bills each item once; found only by reconciling the
log's own monthly count against the invoice line and resolved only by the transmission batch, since dropping
by publication date also drops genuine same-day items. Hazards: H2 (invoice amounts in thousands of pesos),
H1 (outlet codes gain a service prefix in 2026). Files and columns: the delivery log plus the invoice PDFs,
11 columns on the path. Stops: log as exported 41,860; invoice total read as the log's 40,980; dropped by
publication date 41,402; golden 41,508. Realism: a clipping service bills per desk-month and re-pushes failed
items; the log keeps every push.

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
| H5 three municipalities re-coded after a merger | B | 6 figures |

**Referee.** Ask A's disagreement is arbitrated by the delivery log's transmission batch column, ask B's by
the city table's effective dates, ask C's by the manual's sentence on the participants column. Each says
which rows, never which value, so none hands over a level.

**Forcing, measured on the cut pack** (`generator/ceiling.py --forcing`): 35 of 35 sampled figures move
beyond the rounding their asking sentence states. Ask A's four billed quarters move by 49 to 126 items and
its three difference lines from zero to 82, 125 and 7; ask B's twelve municipal figures move by 17 to 131
gathering-days, three of them from zero; ask C's sixteen move by 18 to 56 participants per action and by 197
to 3,721 in total.

| Ask figure group | The cracker's path | Cracker verdict |
|---|---|---|
| A items delivered, 16 quarter x outlet-type cells | reconciles the log to the invoice, finds the gap, drops by publication date | miss |
| A quarterly amounts billed, 4 | reads the dictionary's unit correctly, but the item set is still the dropped-by-date set | miss |
| A difference lines, 3 | attributes the whole gap to one cause | miss |
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
cracker may keep 26 of 64 figures before the pair breaches 40, and it keeps 0. Re-run on the cut pack at
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
| graded figure | every candidate city's rate sits at least 0.29 of the printed unit from its bin edge on the clean truth, and the populations are re-tuned against the realised counts at stage 3 to hold every graded rate at 0.3 or better |

## Single-use test

Of every file and every sentence added to force a convention: what else does the organisation use it for?

| Organ | Its other uses in the pack | Verdict |
|---|---|---|
| the delivery log (the decisive organ) | ask A reconciles it to the service's invoices; the bulletin's methodology page quotes the panel's monthly intake from it; the register's coverage appendix lists which outlets filed from which municipality; the coding desk's workload page counts items screened per coder | four other uses, one of them a graded ask, so the file is not a single-use organ |
| the manual's entry definition ("an entry exists where an action occurred and a monitored source filed an account of it") | it is the instruction coders follow when deciding whether to open an entry, and the dictionary's description of the entry table points at it; it also governs the register's own duplicate rule | not a lone sentence: deleting it leaves the designation unforced (the recorded-count reading names Sardinata and the activity reading names Tibu), so it is load-bearing for determinacy rather than announcement, and the fork is measured in SF12 |
| the protocol's designation clause | it also sets the panel, the publication cycle, the tie-break and the mission's funding, and the coordinator's own role is defined in it | not single-use |
| the invoice PDFs | the coordinator signs them; ask A's control total | not single-use, and they cover 2025 only, so they bear on no window figure |
| the published monthly summary | the bulletin is built from it and the register's own returns process produces it | not single-use; it is ask B's primary and agrees with the detail for every panel city |

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

| Finding | What was done |
|---|---|
| Ask 6's data contradicted the manual: all ranged entries held the range's low end in `participantes_est` while the manual promised a central estimate, and the committed figures reproduced only if each midpoint was floored before summing | The coder now leaves the numeric field empty where the source reported a range and no figure, which is what the manual and the dictionary state, and every range is drawn so its endpoints sum to an even number, so the midpoint is a whole participant and nothing has to be floored. The reconstruction and its grain are pinned in the asking sentence ("the participants per entry and in total for each actor sector, taking the midpoint where only a range is held") and the closing rounding clause now covers each class: actions, items and participant totals whole, participants per entry and every rate to one decimal |
| Ask 4's "with a line for each difference" equally carried the per-quarter arithmetic deltas | Reworded to "with a line for each item reconciling the gap" |
| The chart ask was internally inconsistent: bars of gathering-days per 1,000 items received cannot carry a line at 1.00, which belongs to the ratio | The bars carry the ratio of the half year's gathering-days per item received to the same figure over the comparison period, the axis says so, and the write-up's description matches |
| Step 5 said the retained-items and citations denominators both rank Teorama first | Measured on the cut pack: citations rank Teorama first with the golden fourth at 1.071, while retained items rank the golden first at 1.658. Step 5 now names the citations route alone, and the ladder and readability rows say the same |
| Seven graded figures sat inside the bin-edge floor, the worst being the designation ratio at 0.00013 and a sector mean on an exact tie at 330.85000 | No ratio is graded anywhere now: the chart prints no per-bar value, block 1 states the call on the four integer components instead, and the steps name the ordering rather than the ratios. The sector means are held clear by a deterministic pass in the generator that adjusts one plain entry per sector until the mean clears 0.3 of the printed unit and does not print round; the tightest is now 0.30 of the unit |
| The leak reader's three quotes | The bulletin's methodological note is cut to one sentence, its "no compara municipios entre si ni anticipa la designacion" is gone, and the dictionary's line telling the analyst which two files do not enter the register is replaced by a plain listing. Protocol 4.1 is untouched: deleting it would open the Gate C fork the judge certified closed, and it names no normaliser, no city and no file |

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
