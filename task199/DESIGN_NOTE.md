# task199 design note

Collective-action register, Catatumbo and middle Magdalena corridor. Anomaly Detection & Diagnostics.
Stage 1 (draw) complete; stage 2 held until the coordinator acknowledges the draw summary.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task199.json`, registered 2026-10-18, `guard.py check` WARN, 0 BLOCK |
| Domain / subdomain | political-science-public-policy / conflict-protest-event-data-analysis (client domain, task type serves anomaly-detection in the taxonomy) |
| Objective | anomaly-detection: a real event separated from an artifact |
| Shape | 01, ranked list under a cap. 11 cities x (window actions, rate per 100,000, items received, designation verdict) = 44, plus call, runner-up, gap, flip = 4, plus a chart's 5 named parts, plus 2 deliverables: 55 criteria |
| Decision | pick_one_of_n: the one city the half-yearly field verification goes to, named in the watch note with its recorded rate |
| Gap / pattern / generators | population (a row is a reported action, not an action) / none / G12 decisive (an absence of records is not a record of absence), G14 (the conditioned yield that repairs it), G16 (the choice among conditioners) |
| Gate G | decomposition_attribution: every city's recorded rise is correctly reported, and the call turns on assigning it to press presence or to activity |
| Strategy / Layer 2 | population_selection (which measured volume may stand in the exposure) / estimand_identification, client pattern political-science-public-policy/conflict-protest-event-data-analysis/1 |
| Calibration organ | none, by design (see `## Tried and rejected`) |
| World | Colombia; Observatorio Territorial del Nororiente keeps the Registro de Acciones Colectivas from material delivered by the Resena Andina clipping service; personas drawn with `guard.py names --locale es_CO --seed 199` |
| Spine | `envios_resena_andina.csv`, one row per outlet x city x delivery day, about 31,000 rows, 2024-01-01 to 2026-09-30 |
| Forum / forcing event / org | line_manager_or_team / audit_or_inspection (the half-yearly verification mission is allocated) / university_or_school |

**Data-native sentence.** In this register an action exists only where a monitored outlet filed an account of
it, and the clipping service's delivery log measures, for every city and every month, how much material
actually reached the monitor, so the record carries its own exposure; the two volumes a solver reaches for
first, the items retained for screening and the citations held per action, are produced by the recorded
actions themselves, so dividing by either cancels the rise being tested for. That is why the pitfall is here
and not in any record whose events arrive by their own channel.

**Why the call is retrospective.** The designation window closed on 30 September 2026 and the pack is cut
after it, so no period is open and no count is still developing (maturity censoring is deliberately absent:
it is banned against the last three builds and task194 holds it live). The decision the designation forces,
where the one funded verification mission goes next, is forward.

**A line per source read.**
- `guard.py mechanisms --objective anomaly-detection` (31 builds): the adjacent insights are task180 (a
  detection floor set by a known daily cycle), task182 (items entering a record in proportion to their own
  duration), task196 (how many events happened, from the overlap of two capture channels), task470 (rebuilding
  the activity a sensor never records for whole unit classes) and task448 (completing a register from a second
  incomplete list). All five estimate what is missing; none turns on which of the record's own measured
  volumes may stand in a denominator, which is this build's move.
- task192, the only other build on this subdomain: a classifier's hand-coded error rates transported past the
  window they were measured in. This build ships no classifier, no audit batch and no label correction.
- `stumping` Part 3 (the four pricing screens) and `references/client/layer2-rigor-patterns.md` pattern 1 for
  this task type, "reported events track media reach: condition on the reporting proxy": that pattern's own
  shortcut is raw counts, which is this build's rung 1, so the decisive step sits one level below the
  published pattern, in which proxy may be used.
- `guide-to-prompt` shapes 01, 17 and 08: 17 and 08 are native to the objective but take their criteria from
  the periods of one series, which would leave the eleven-city structure ungraded.

## Default path

The pipeline a competent analyst builds from the protocol's words and the files' grain.

1. Union the three yearly register exports `rac_acciones_2024.csv`, `_2025.csv`, `_2026.csv`, resolving the
   2025 column renames and the two date formats.
2. Drop the rows the preliminary and definitive monthly extracts hold twice, keyed on the action id.
3. Resolve the city key to the eleven study cities (names in some years, divipola codes in others, one code
   reassigned).
4. Keep actions whose action date falls in the protocol's window, 2026-04-01 to 2026-09-30, and in its
   baseline, 2024-01-01 to 2025-12-31, using the action date rather than the ingest timestamp.
5. Count actions per city per span and divide by 6 and 24 to get monthly levels.
6. Join the 2026 population projection (the units sheet, not the thousands sheet) and compute the window's
   actions per 100,000 residents.
7. Rank the eleven cities on the window's monthly level over the baseline's monthly level.
8. Designate the top city and print its window rate.

Ends on: Sardinata, 74.0 actions per 100,000 residents.
Golden: Tibu, 63.6 actions per 100,000 residents.

(Both figures are the pricing prototype's clean-truth values, provisional until the generator cuts the pack;
the golden is tuned mid-bin then.)

## Stump sentence

The default path files Sardinata at 74.0 actions per 100,000 residents because it ranks the eleven cities on
their own recorded rise with residents as the only denominator, and Sardinata's entire rise is the two
outlets that began filing from it in early 2026, while Tibu's 86 per cent rise happened with the material
reaching the monitor from it unchanged.

## Three rules

- `Task type:` conflict-protest-event-data-analysis, which the client taxonomy gives anomaly-detection and
  descriptive-distribution; this build takes the anomaly-detection reading, a real escalation separated from a
  reporting artifact.
- `Domain test:` the deciding quantity is protest incidence recovered from a media-sourced event record, which
  conflict-event analysis estimates by conditioning event counts on reporting intensity (the field's own
  pattern 1 for this task type, and the reason every published protest-event series carries a media-reach
  caveat). The estimator is a rate of recorded actions per unit of press material reaching the monitor,
  compared with the city's own earlier rate.
- `Swap:` "which city's protest activity rose, as against the volume of press material reaching the register
  from it" becomes, with another field's nouns, "which hospital's falls rose, as against the volume of
  incident forms reaching the registry from it", and it stops making sense: an internal incident system has
  no outside reporters whose filing volume the record separately measures, no citations per event, and no
  gap between an event happening and an account of it reaching a coder. The swap breaks on the fact that the
  register's rows are produced by third parties whose output the pack measures directly.
- `Layer 1:` the register ships as yearly exports whose columns were renamed in 2025 and whose dates change
  format (the office's own export tool, revised between calendar years); a preliminary and a definitive
  monthly extract overlap for three months (the register's publication cycle); city keys arrive as names and
  as divipola codes with one code reassigned (the national coding standard's own revision); population
  projections ship in thousands on one sheet and units on another in two vintages (the statistics office's
  release practice); the quarterly bulletin's figures sit inside PDF tables (it is a published bulletin);
  outlet codes carry a service prefix in the 2026 delivery file only (the clipping service renumbered its
  desks); the ingest timestamp is UTC while the action date is local. Nothing here is placed to be caught and
  none of it changes which city is designated.
- `Layer 2:` estimand_identification. The recorded count is the product of how often actions happen and how
  reliably an account of one reaches the monitor, and the decisive choice is which of the record's own
  measured volumes may stand for the second factor.
- `Decisive step:` condition each city's rise on the press material the monitor received from that city, the
  one volume in the record that is not produced by the actions themselves, rather than on residents (which
  cancels out of a within-city rise), on the items retained for screening, or on the citations the register
  holds per action.
- `Not semantics:` every field, code, unit and date can be read correctly and the easy route still files
  Sardinata. The data dictionary defines all three volumes accurately; nothing in any definition says which
  one belongs in a denominator, and the two wrong ones are wrong for a structural reason (they contain the
  action count by construction) that no reading of a field reveals.
- `Not rule application:` the protocol files the designation's population, outcome, window, unit and
  comparison, and no filed rule, formula or procedure performs the conditioning or names a volume. Executing
  every stated rule gives the eleven cities' recorded rises against their own baselines, which is the default
  path's wrong answer.
- `Analyst test:` with every field read, every date and code resolved and the protocol's window and unit
  applied, the easy route compares each city's half-year actions with its own baseline and files Sardinata,
  74.0 actions per 100,000 residents; the obvious correction, dividing actions by the register's own protest
  material (retained items, citations or citing outlets), files Teorama, whose citations halved when one
  outlet stopped republishing. `checks.py` will execute both on the generator's clean truth.
- `Estimand:` the protocol's designation clause fixes the population (every action in the register for the
  eleven study cities, all sources, including actions known from a single outlet), the outcome (a rise in the
  actions occurring in the city, for which the register's entries are the evidence and not themselves the
  measure: an entry exists where an action occurred and the monitor received an account of it), the window
  (2026-04-01 to 2026-09-30 against 2024-01-01 to 2025-12-31), the unit (one gathering, on one day, at one
  place; the printed figure per 100,000 residents) and the comparison (the city against its own record over
  the baseline). It sits once, in the register's designation protocol, never in the prompt.
- `No decoy:` nothing is planted to be caught. No memo, draft or stakeholder figure argues for any city, no
  block of records is copied, no rule is withheld. The quarterly bulletin reports completed quarters as it
  always has and designates nobody. The three cities whose press presence rose have unrelated causes and no
  shipped sentence states that any of them changed.
- `No certified replay:` no certified, published or closed figure in the pack is reproduced by the wrong
  method, and no bench blesses a method. The pack ships no completeness audit at all.
- `Lesson:` an exposure measure has to be independent of the outcome being measured; a denominator that the
  outcome itself produces subtracts the signal. No build on file teaches it: the five nearest builds all
  estimate what a record is missing, and none of them turns on which measured volume may normalise a rise.

## Pricing (clean truth, before any file; `scratchpad/task199/price4.py`)

| Screen | Result |
|---|---|
| 1 residue of the filed WHAT | a method, not a knob: which of three measured volumes stands in the denominator. Not a tolerance, cut-off, rounding or nearest-k |
| 2 move needed vs available | 0.400 ranking units needed, 1.260 available if every capture-added record of the leader flipped: 3.15x |
| 3 standard error of the estimate | decisive margin 0.690 ranking units = 5.2 standard errors of the golden's own rise; thinnest city 0.206 |
| 4 lever vs ranked-quantity noise | two variances: the lever moves the denominator's level by 126 per cent while its own sampling noise is 0.016 against the ranked quantity's 0.124 |
| seed sweep, 60 seeds | decisive route names the golden 60/60; default path misses it 56/60; golden's default-path position mean 3.4 |
| position and margins | golden 4th of 11 on the default path at 1.22x behind the leader; 1.59x ahead of the runner-up on the decisive route |
| every right-family form | per received item 1.86 (1.59x), per sqrt 1.86 (1.24x), saturating 1.86 (1.31x), fitted log-presence covariate beta 1.00 1.86: all name the golden |
| every wrong family | raw and per-capita rise, window level and absolute increase name a presence riser; retained items, citations and citing outlets name Teorama; the redundancy family's winner moves with its free parameter and never names the golden |

## Tried and rejected

- Multi-source deduplication against the coding manual: the decisive step would be executing the manual,
  which is rule application and banned as the decisive step. Rejected before the draw.
- One-sided reporting of ongoing against ended episodes: maturity censoring, banned against the last three
  builds and live on task194. Rejected before the draw.
- A capture estimate from the overlap of two sources: task196's family. Rejected before the draw, and the
  pack deliberately carries no second channel.
- A completeness audit as the calibration organ (past verification missions reconstructing a city-month from
  local archives, against which the candidate volumes could be validated): dropped. It would hand over the
  insight that the register's completeness differs by city and period, which makes the decisive rung readable
  on the readability screen's control-bench test, and `stumping` Part 7 bars a corpus that refutes the naive
  read. The method is forced by the data's structure instead: the retained-item and citation volumes contain
  the action count by construction, the redundancy family needs a free parameter the pack does not fix, and
  every parameter-free presence form agrees.
- Pattern E (conditioned yield) on the card: BLOCKed by `ban.pattern` against task166 and by both older
  structural tests. The pattern axis was redrawn to G12 with Gate G decomposition_attribution rather than
  argued, which also moved the signature off task192's.
- Small municipalities (10,000 to 40,000 residents) as the candidate set: the ranked quantity's standard
  error reached 0.39 and the seed sweep fell to 34 of 40, so the ranking would have been a tuned seed rather
  than a designed mechanism. Replaced by eleven intermediate cities and a six-month window, which cut the
  thinnest standard error to 0.21.
- The golden as the largest and highest-rate city in the candidate pool: a one-period group-by on the
  window's rate, and a rank on population, both reached it for free. Its population and activity were moved
  so that it sits fourth on the window rate and fourth by size, and inside the wrong candidates' range on
  every static attribute (baseline capture, presence per 100,000, baseline citations).
