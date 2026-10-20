# task471 design note: the 2027 preparation program reviews on the 2026 Elementary Literacy Instruction form

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task471.json` (architecture v2), registered 2026-10-20 after a pull.
  Architecture 1 (Kessick Valley's route pitch from a parking card survey) is in the card's lineage, spent at Gate F.
  Blocks cleared at the draw: G1 first (a 2026 rating point is not a 2025 rating point) repeated task472's decisive
  pattern inside three builds, so the decisive generator is G17 (the anchor has to measure both cohorts on one
  standard, a measurement-invariance point), with G6 (the cohort's real decline on the judged item) and G1 behind it;
  the older same-puzzle and same-driver signatures carry differentiation lines against task246, task266 v1, task202,
  task449 and task466, task246 being the nearest in mechanism (measurers' offsets read against a reference reader, for
  one survey's prevalence; here a link between two administrations, with the judged item kept). Stage 3 redraw: once
  task249's card was marked spent, task473 entered this card's window and `heart` blocked ban.calibration and
  ban.artifact (both builds calibrating on a verified audit set, with a register as context); the organ was redrawn rather than relabelled
  (WA2's validity papers are June 2025 responses carrying the score both of their 2025 reads gave, so the calibration is
  the overlap of the two scoring regimes on the same responses) and the context artifact is Pellmore's technical
  report, the vendor's equating model the Office now runs. WARNs answered: government_agency in 36 builds (the board is
  the state agency that licenses teachers and approves their programs); ETL in 4 of the last 12 (the lane's objective);
  Gate G method_or_model_selection in 8 of 12 (the decisive move is how the judged item enters the link, a method the
  data selects, and no other Gate G fits); png and xlsx repeat task250 (a program workbook and the chart the committee
  reads are an assessment office's own products); question form "which" repeats task250 (the decision picks
  programs). Nearest driver task450 v2 at 0.10. Personas from `guard.py names --geo us
  --seed 471`; Donald Lara (in v1) and Samuel Kim (first name in task120) not used.
- **Pairing:** Education & Learning Sciences / item-response-theory-test-equating / ETL. The board's Office of
  Assessment Research conforms two scoring contractors' score files, the 2026 written-assignment read file, the
  candidates' attempt history and sixteen programs' completer lists into one results file on the 2025 reporting scale,
  then the program pass rates; the deciding quantity, the 2026 raw score at the 2025 passing standard, is the equating
  that conformation needs.
- **World:** an unnamed U.S. state's Board of Educator Standards and Licensure and its Elementary Literacy Instruction
  test (60 multiple-choice items and three written assignments, each assignment read twice on a 1 to 4 scoring guide and
  counted twice, raw 0 to 108, reported on 100 to 300 with 240 passing). The previous contractor scored and equated the
  2025 form; from 2026 a new contractor scores and the board's office equates. The 2026 form shares 20 multiple-choice
  items and one written assignment with the 2025 form, an internal anchor built in proportion to the test's two
  formats. Sixteen preparation programs (universities and alternative routes) submit completer lists.
- **Decision:** which programs' 2025-26 completers have a first-attempt pass rate below 70 per cent, the board's line
  for a formal program review in 2027.
- **Shape 10:** the call; each program's first-attempt pass rate and review verdict (32); the 2026 raw passing score;
  the programs nearest the line on each side; the chart's parts; the files: 40 before the asks.
- **Strategy:** other (`own:rater-severity-drift-on-a-constructed-response-anchor`), Gate G
  method_or_model_selection, calibration form parallel_run_overlap (WA2's validity papers: June 2025 responses
  carrying the score both 2025 reads gave, read again by the 2026 raters), context artifact filed_model (Pellmore's
  technical report).
- **Data-native sentence:** the anchor's written assignment is its only item scored by people, and people's standard
  moves between scoring seasons: the 2026 contractor's raters, trained by new scoring leaders, read that assignment's
  validity papers, June 2025 responses, about a quarter point per read below the score both of their 2025 reads gave, while the 2026
  cohort really does write less well, and the link sees both at once unless the raters' part is taken out on those
  papers.
- **Sources:** Kolen and Brennan's common-item nonequivalent-groups design (Tucker, Levine, chained linear, chained
  equipercentile) teaches that the anchor is a miniature of the test scored the same way in both groups; the rungs
  here (as scored, dropped, re-expressed) come from that requirement. The constructed-response anchor literature
  (trend scoring and rater drift) teaches re-expressing the new raters' scores on the old standard measured on old
  responses scored again; the organ here is the contractor's validity papers, reported only as agreement. task450 v2
  screens keyed anchor items whose difficulty moved: that golden is this build's wrong rung, because here the judged
  item's change is partly real. task464 v2 links two instruments through a single-group sample: another design and
  another move. task246 reads measurers' offsets against a reference reader for a prevalence: the nearest mechanism,
  different purpose.
- **The re-root's lesson carried:** nothing in either score file shows the raters' shift; it sits in the read file's
  validity reads, which the contractor's QC summary reports only as agreement rates, and the default path never needs
  the read file because the score file carries every assignment's score.

## Default path

1. Conform Pellmore's June 2025 score file (position-order item string, two reads and a resolution read per
   assignment) and Arcwright's June 2026 files (score file, long item file), key each 2026 registration to its
   educator record through the Board's crosswalk, and date each educator's first attempt from the attempt history.
2. Build the equating samples the 2025 technical report names, each form's first-attempt candidates (3,035 on Form 25A,
   3,215 on Form 26A), and score the anchor on both: the 20 items the forms share (matched by item ID in the item maps)
   plus twice the WA2 score.
3. Equate Form 26A to Form 25A through that anchor (Tucker, Levine, chained linear or chained equipercentile, which
   agree), round each equated score and convert it with Form 25A's table: the Form 26A raw passing score is 52.
4. Take each program's 2025-26 elementary completers from its Title II list (Rule 8.4.2), give each its first attempt
   at or before June 13, 2026 (a June 2026 attempt passes at raw 52, an earlier one keeps its result) and send the
   programs under 70 per cent to review.

Ends on: raw passing score 52 and eight programs on review (Delacourt, Eastridge, Harrowgate, Linden Valley, Marisford,
Riverbend, Statewide Teacher Residency and Tarrance).

Golden: raw passing score 49 and five programs on review (Eastridge, Harrowgate, Linden Valley, Statewide Teacher
Residency and Tarrance).

## Stump sentence

The default path equates Form 26A through the anchor as Arcwright's raters scored it, puts the raw passing score at 52
and sends eight programs to review, because WA2, the anchor's written assignment, was read in 2026 by a new scoring
team whose raters read its validity papers, June 2025 responses, 0.25 points per read below the scores their two 2025
reads agreed on, so the anchor reads the 2026 cohort as weaker than it is and the cut too high; with WA2's 2026 reads
put back on the 2025 standard (0.98 anchor
points) the cut is 49 and five programs go to review, while dropping WA2 from the anchor instead puts the cut at 46 or
47 and frees Eastridge, because the cohort really does write less well.

## Three rules

- **Task type:** education-learning-sciences / item-response-theory-test-equating, which serves Data Extraction &
  Conformation: conforming two contractors' results onto the 2025 reporting scale requires equating Form 26A to Form 25A.
- **Domain test:** the quantity that decides the call is the Form 26A raw score at the 2025 passing standard, estimated
  by common-item nonequivalent-groups equating through a mixed-format anchor; test equating requires the anchor scored to
  one standard in both administrations, and for a rater-scored anchor item the field measures the raters' shift on
  responses already scored under the earlier standard and takes it out before the link (the trend-scoring problem of constructed-response
  anchors).
- **Swap:** "which hospitals fall below the readmission line on the new claims form": with a hospital for a program and
  a claims system for a test there is no anchor, no rating standard and no equating, so the quantity that decides has
  no counterpart and the call stops making sense.
- **Layer 1:** Pellmore's and Arcwright's own layouts (a position-order item string and read columns against a long item
  file and assignment scores), registrations keyed to educator records through the licensing system's crosswalk
  (typed IDs blank, unprefixed or transposed), first attempts read from a history spanning both contractors, sixteen
  Title II lists in three layouts carrying other pathways, the previous year's late-spring completers, summer 2026
  completers and pasted duplicates, and the register's 2024-25 completers under second educator records; each comes
  from the system that writes it and none is placed to be caught.
- **Layer 2:** field_method: the anchor's rater-scored assignment is put back on the 2025 rating standard by the shift
  measured on the validity papers, June 2025 responses the 2026 raters read again, rather than used as scored or
  dropped from the anchor.
- **Decisive step:** taking the raters' shift out of the anchor's written assignment before it carries the link (each
  2026 WA2 score moved up by twice the mean validity-paper shortfall), keeping WA2 in the anchor so the link still sees
  the cohort's real change on what only the assignment measures.
- **Not semantics:** both routes read every field the same way (the validity reads and each paper's score on file, the
  assignment scores, the item maps, the history); the flip comes from recognising that the anchor's judged part is not on
  the 2025 standard, which no field, code or definition states, so a reader who reads all of them correctly still equates
  through the anchor as scored.
- **Not rule application:** no filed rule, procedure or method says to adjust the anchor for the raters: the technical
  report files the design, the samples and the rounding, the memo the anchor's composition, Rule 8.4 the population and
  the line; executing every one of them with the anchor as scored files the eight-program set at raw 52.
- **Analyst test:** a strong analyst who conforms both contractors' files, builds the first-attempt samples and equates
  through the anchor as Arcwright scored it files raw 52 and eight programs on review (the five plus Delacourt, Marisford
  and Riverbend); dropping WA2 from the anchor files raw 46 or 47 and frees Eastridge.
- **Estimand:** Rule 8.4 files the population, outcome, window and unit (each program's 2025-26 elementary completers'
  first attempts at or before June 13, 2026, passing at a reported scale score of 240, below 70 per cent to review); the
  technical report files the reporting scale through the previous form, the first-attempt equating samples and the
  rounding of equated scores; the memo files that 2026 scores are reported through Form 25A's conversion.
- **No decoy:** nothing is planted: Arcwright's QC summary reports agreement rates as scoring contractors do, the
  validity papers are routine monitoring, no document argues for using the anchor as scored or dropping WA2, and no file
  ranks the programs.
- **No certified replay:** no certified or published figure is reproduced to recover the method; the one published
  conversion is Form 25A's own table, which every route uses the same way.
- **Lesson:** when a rater-scored item anchors an equating across scoring seasons, the raters' standard is part of what
  the anchor measures, so it is measured on responses already scored under the earlier standard and taken out, and neither the item as scored nor the item
  dropped gets the cohort difference right; task450 teaches screening keyed anchor items whose difficulty moved, and no
  build on file teaches rater drift on a judged anchor.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the 2025 raw passing score on Form 26A | the technical report's equating section names the design | the item maps show shared items | equating a new form is the reflex | none | none | one subtraction | readable |
| R1 the anchor as Arcwright scored it (decisive) | none names the raters' standard or ties the validity papers to the anchor | the validity reads are a monitoring read type among 29,520 reads; nothing joins them to the anchor | the reflexes (equate through the anchor, screen anchor items for drift) land on R1 or R2 | no control scores the routes | no sweep sees a mean shift on one assignment | a shift carried through an equating, not one subtraction | silent |
| R1p every assignment's validity papers pooled | the QC notes say WA1 and WA3 papers come from 2026 | the validity papers sheet's source column | none | none | none | one mean | readable |
| R2 WA2 dropped from the anchor | the memo and the report say the anchor carries both formats in proportion | none | screening a moving anchor item is a reflex | none | none | none | readable |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | first attempt | the educator's first attempt ever, including before completion | the first attempt after completion or within the program year | differs for programs with early testers | Rule 8.4.3 ("whenever it was taken, including an attempt before the program was completed") |
| SF2 | 2025-26 completers | completion date July 1, 2025 to June 30, 2026 on the program's list | every row of the 2025-26 list | the out-of-year rows enter | Rule 8.4.2 ("on a date in the program year") |
| SF3 | elementary pathway | Elementary, or Elementary and Special Education | Elementary only | the dual completers leave | Rule 8.4.2 names both |
| SF4 | below 70 per cent | the exact fraction under 0.70 | the rate rounded to one decimal under 70.0 | same call (the nearest are 69.0 and 72.0, asserted) | same call |
| SF5 | an attempt | a scored, not voided attempt | voided attempts counted | same call (no voided attempt in 2025 or 2026, asserted) | Rule 8.4.3 and same call |
| SF6 | the raw passing score | the lowest Form 26A raw score whose equated score, rounded to a whole number, converts to 240 | the unrounded equated score at 56 or more | raw 49 or 50 by method: the same five programs, but the passing score and the rates move under most methods | technical report section 4 ("each equated raw score is rounded to a whole number and converted") |
| SF7 | equating samples | each form's first-attempt candidates | every candidate who sat | same call (raw 49 under every method, asserted) | technical report section 4 ("the equating samples are each form's first-attempt candidates") |
| SF8 | the Form 26A raw score | the raw total as Arcwright scored it (RAW_TOTAL) | a raw score with the 2026 assignments adjusted | same call (the cut on the adjusted scale less the shift is 49, asserted) | same call |
| SF9 | completers counted | completers with a first attempt at or before June 13, 2026 | every completer on the list | the untested enter the denominator | Rule 8.4.4 |
| SF10 | a first attempt passes | reported scale score 240 or more; for June 2025 and earlier, the reported result | recomputing earlier results | same call (the history's results tie to Form 25A raw 56, asserted) | Rule 8.4.5 and same call |
| SF11 | the program's completer | each educator once in a program's list | duplicated rows counted twice | moves two programs' counts (Ostrander and Hollis Creek each carry one pasted row) | Rule 8.4.2 ("a candidate the program reports") with each educator once |
| SF12 | the 2024-25 completers (the ask) | the register's program year 2024-25, elementary pathways, first attempt at or before June 14, 2025 | the completers listed, the untested read as not passing; or June 2025 first attempts only | moves the ask figures (142 untested completers; 180 who first tested before June 2025) | the asking sentence ("who had made a first attempt by the June 2025 administration") and Rule 8.4.3 |

## Ladder

| Rung | What it does | Form 26A raw cut | Programs on review |
|---|---|---|---|
| R0 | the 2025 raw passing score on Form 26A, no equating | 56 | 11 |
| R0p | the 2026 assignments moved by the WA2 shift, no equating | 53 | 9 |
| R1 (default path) | the anchor as Arcwright scored it, every method | 52 | 8: the five plus Delacourt, Marisford and Riverbend |
| R1p | the anchor moved by every assignment's validity papers pooled (shift 0.28 anchor points) | 51 | 6: the five plus Delacourt |
| G | WA2's 2026 reads put back on the 2025 standard (0.98 anchor points), every method | 49 | 5: Eastridge, Harrowgate, Linden Valley, Statewide Teacher Residency, Tarrance |
| R2 | WA2 dropped, the 20 shared items alone | 46 (chained, Levine) or 47 (Tucker) | 3 or 4: Eastridge off, Tarrance off at 46 |

- **Margins:** at raw 49 every method's equated Form 25A score is 55.88 to 56.02 (0.38 to 0.52 above 55.5); at raw 48,
  54.90 to 55.13 (0.37 to 0.60 below). The nearest programs are Eastridge, 160 of 232 (69.0, 2.4 completers under 70 per
  cent), and Delacourt, 149 of 207 (72.0, 4.1 completers over).
- **Position and dominance:** the golden set is bracketed: every route that ignores the raters (R0, R0p, R1, R1p) sends
  more programs, the route that drops WA2 (R2) fewer; only the decisive move lands between them. Every rung names its
  own set (asserted).
- **The generating truth:** the 2025 first-attempt cohort sitting Form 26A under the 2026 scoring, equated single-group,
  puts the cut at 49 (asserted within one point; the link's population and the reference population differ on the
  writing dimension).
- **C1, the adjustment's form:** the per-read mean, the per-paper mean, an equipercentile map of the 2026 reads onto
  the papers' 2025 scores, every 2026 assignment moved before equating, and the 2025 anchor moved to the 2026 standard
  all give 49 (asserted). A regression map (the expected 2025 score given a 2026 read) gives 46 to 48 by method: it
  shrinks the 2026 reads toward the papers' mean while the 2025 anchor scores keep their spread, so the two sides of the
  anchor would sit on different metrics; the shift keeps both on the 2025 raters' metric (asserted, C4).
- **Worth:** the decisive move is three raw points and three programs against R1, two raw points and one program
  against R2; nothing else on the ladder moves the set the other way.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | Rule 8.4.2 and 8.4.4: each program's 2025-26 elementary completers with a first attempt at or before June 13, 2026; untested completers are stated as not counted |
| 2 | Unit of account | the completer (each educator once per list); the program is the unit of the call |
| 3 | Attribution window | the program year July 1 to June 30 (8.4.2); no completion date on a boundary day (asserted) |
| 4 | As-of dating | the June 13, 2026 administration (8.4.4); the history is the licensing system's August 18 export |
| 5 | Version basis | the scores as Arcwright released them; no verification has run before release (no revised release) |
| 6 | Denominator | completers counted (8.4.4, 8.4.6) |
| 7 | Weighting | each completer counts once; the equating's synthetic weights converge (C1, three weights asserted) |
| 8 | Window length | one program year; the ask's window is in its asking sentence |
| 9 | Boundary inclusivity | "below 70 per cent" strict; no program within a completer of the line (C1) |
| 10 | Rounding path | equated scores rounded to whole raw scores, then converted (report section 4); rates to one decimal for display only |
| 11 | Tie-break | none needed: no program at 70.0 |
| 12 | Maturity and censoring | completers not yet tested are not counted (8.4.4), stated in the rule |
| 13 | Order of operations | the anchor adjusted before equating; equivalent orders (adjusting the 2025 side, adjusting every assignment) converge (C1) |
| 14 | Row order | no result depends on file order (sorted reads; asserted over a reversed read file) |
| 15 | Duplicate resolution | pasted list rows are exact duplicates (each educator once); no duplicate attempt in the history |
| 16 | Identity normalisation | list IDs in three formats normalised to the licensing system's (C1: every list ID resolves, asserted); registrations through the crosswalk |
| 17 | Netting against gross | none |
| 18 | Dimensional units | each assignment score counts twice in the raw score and the anchor (report section 2) |
| 19 | Code and status semantics | read types, pathways and results read from the files' own words; never the stump |
| 20 | Integerisation | the cut is an integer raw score; counts are whole completers |
| 21 | Clause scope | Rule 8.4 governs the 2025-26 review; the ask's window is its own sentence |
| 22 | Forward window contents | none: the June 2026 administration is closed and scored; the reviews begin in 2027 on it |

## Literal reader

Executed word for word, Rule 8.4 with the technical report's equating section and the memo files the golden's estimand:
the method of putting Form 26A on Form 25A's scale is open, every NEAT method agrees once the anchor is on one rating
standard, and the anchor as scored and the anchor without WA2 differ from the golden by an analytical choice (the
validity papers measure the 2026 raters against the 2025 standard), never by a reading of a filed sentence.

## Oracles

None. No control scores the routes: Arcwright's agreement rates, the administration summary's counts and Form 25A's
table tie under every route; no published 2026 figure, conversion or pass rate exists before the September release.

## Ask sheet

- **Ask A, each program's 2024-25 completers who had made a first attempt by the June 2025 administration, and the
  share of them who passed it (32 figures: 16 whole completers, 16 per cent to one decimal).** H18 home: a measure every
  program carries that the call does not turn on, the prior year's rate the committee's letters quote beside this year's.
  Path: the completer register (program year, pathway, educator ID, name, birth date), the attempt history (educator ID,
  name, birth date, test date, result), Rule 8.4.2 and 8.4.3 for the definitions, and the program directory: four files,
  eleven columns. Primary device: D7, the true key elsewhere: in 2024-25 a program could open a new educator record when
  its lookup missed a candidate, so 98 of the 2024-25 completers who tested sit in the register under a record that
  holds none of their attempts, which sit under the record they registered for the test with; the same name and birth
  date join them, and every program has at least two. No sweep sees it: every register ID is well formed and unique,
  completers who had not tested are expected and Rule 8.4.4 drops them, so the unmatched rows read as untested.
  Hazards: the pathway filter (dual completers count), the window (first attempts in June 2024 and earlier count),
  names written with apostrophes and spaces. Stops (asserted, generator/ceiling.py and checks.py): the register's
  educator ID (the cracker) misses all 32; ID, then name and birth date where the ID has no attempts, is the golden and
  equals the generator's truth. Realism: a provider portal that lets a program open a record when its lookup misses is
  how licensing systems collect duplicate educator records.
- **The construction layer:** the call, the raw passing score, each program's completers counted, passers and rate, the
  nearest programs, the chart and the files; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no register row; the duplicate records' June 2025 attempts
  are first attempts on Form 25A under either record, so the 2025 equating sample and every 2026 figure are the same with
  the register deleted.
- **Hazard table (asserted):** the duplicate records move all 32 ask figures; the pathway filter moves every program with
  a dual completer; the window moves the programs with first attempts before June 2025.
- **Referee:** none; no total in the ask's files ties under one handling only.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each program's 2024-25 completers tested by June 2025 and their first-attempt rate | joins the register to the history on educator ID; completers whose record holds no attempt read as untested and are dropped under Rule 8.4.4 | miss |

- Mirror leakage: 0.0 per cent of ask weight (a response on R1 builds the ask the same way and misses all 32).
- Pair ceiling: 28.8 (weights 38 / 7 / 55: the call 8, the raw passing score 2, each program's rate 1, passers 0.5 and
  completers counted 0.25; the cracker keeps 38 + 7 + 0 = 45.0; the best mirror, every assignment's papers at raw 51,
  keeps 5.5 + 7 + 0 = 12.5; average 28.8), rerun from the generated rubric at ship.
- Measured by: generator/ceiling.py

## Pre-ship check

- **Three rules, re-read against the built pack.**
  - Domain: the deciding quantity is the Form 26A raw score at the 2025 passing standard, estimated by
    common-item nonequivalent-groups equating through the mixed-format anchor.
  - Decisive step: the anchor's rater-scored assignment is put on the 2025 raters' metric. The measure is WA2's validity
    papers, June 2025 responses carrying the score both of their 2025 reads gave, read again by the 2026 raters.
  - Asserted on the clean truth and on the pack: the easy route files raw 52 and its eight programs (T2); changing only
    WA2's treatment files raw 49 (T3); the generating truth is 49 (T4).
  - Two layers: the Layer 1 inventory in `## Three rules`, each item from the system that writes it. The ask's device
    sits in the register, which the call never reads (S1 to S5).
  - Not a plant: no document names the raters' shift, an adjusted anchor or a verdict. Arcwright's QC summary reports
    agreement rates only.
  - Not semantics: in the fork table, every term read right still leaves the as-scored route on raw 52.
  - Not rule application: no filed rule adjusts the anchor. Executing every filed rule with the anchor as scored files
    the eight-program set.
- **Gates.**
  - Inputs: 17 files in 3 formats (csv, pdf, xlsx); the item response file has 250,260 rows; two distractors (the test
    framework and the administration summary) are named in metadata.json.
  - Generator checks: checks.py 47 of 47. verify.py works from the bundle alone (its own readers, and its own Tucker,
    chained linear and chained equipercentile) and matches the golden.
  - Two builds byte-identical (target.zip 14b337c337f9190b).
  - figures_check.py: 142 figures. precut.py: 51 checks, 0 FAIL, 0 WARN. voice-check.py: exit 0.
  - leak.py: REVIEW, no LEAK.
  - Guard: check WARN and heart WARN after the stage-3 redraw of the calibration organ.
  - Containers normalised (PDF stamps, OOXML properties) in build.py; producer metadata audit clean.
- **Pair ceiling.** 28.8, measured by generator/ceiling.py.
  - The cracker lands the call and keeps 45.0, with 0 of 32 ask figures.
  - The best mirror is every assignment's papers at raw 51, at 12.5.
  - Mirror leakage is 0.

## Leak check

`leak.py --asof 2026-08-21`: REVIEW, no LEAK. Each REVIEW line answered:
- Sweep 3: the thirteen figures sit in the technical report's 2025 agreement table and Form 25A's raw-to-scale table.
  They are coincidences of value, not rankings.
- Sweep 4: the memo, the technical report, the rule, the framework and Arcwright's summary share the field's own words
  (anchor, assignment, validity papers, scoring, standard). None names a raters' shift, an adjusted anchor or a verdict.
- Sweep 6: the completer lists name the programs beside completer rows and rank nothing on pass rates.
Harmless.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own moves, a round-trip itinerary fare read as a one-way fare and the New York
  airports left as three markets: data semantics and a market definition (the estimand's unit), so neither may decide;
  kept as Layer 1 and as ask devices.
- 2026-10-18, at the draw: a windshield census (cards put on every car parked in the lots at sweep times), whose cards
  over-represent long stays in proportion to their length: population_selection, banned against task245 at the draw,
  and the label is not moved to pass the guard; replaced by the entry-plaza handout, a different mechanism (replies
  censored by the collection close, which thins the long stays instead of inflating them).
- 2026-10-18, at the draw: the fare premium over a log-log fare-distance benchmark, decided by retransformation bias:
  generic econometrics, and a clinic's charges against a severity curve read the same (swap test fails).
- 2026-10-18, at the draw: the three markets with the highest premium in thin ticket-sample cells, decided by
  shrinkage (the winner's curse): the shrinkage method is not forced by anything filed, a coin flip for determinism.
- 2026-10-18, at the draw: leakage read from an agency ticket dataset whose capture depends on the sales channel,
  measured where the ticket sample sees everything: the same lesson as task448 and task470 (capture by unit measured
  on the overlap).
- 2026-10-18, at the draw: a departure-lounge survey with a fixed quota of interviews per flight (unequal inclusion):
  a ratio within each destination sidesteps it, and by house precedent (task452) a design-weight stump is
  population_selection, banned at the draw.
- 2026-10-18, at the draw: capacity-censored (spilled) demand on full flights to the hubs: the demand turned away is
  model-dependent and every demand model is a fork.
- 2026-10-18, at the draw: the share of one-way tickets that are residents' trips (a one-way ticket's origin is not
  its traveller's home): turns on reading what the ticket origin field means, data semantics.
- 2026-10-18, at the draw: business travel by market from the fare-class proxy corrected for its false positives
  (Rogan-Gladen): the lesson task456 teaches (an imperfect record's false positives subtracted, not only its misses).
- 2026-10-18, at the build: the party verbatim beside the coded party in the cards file, with a filed rule sending the
  analyst to the verbatim for parties of nine or more: the rule pointed every careful solver at the verbatim column,
  where the sums sit in plain view; the verbatims moved to their own file and the cap dropped.
- 2026-10-18, at the build: home ZIPs keyed with a plus-four on 16 per cent of cards: matched as keyed they moved every
  trips figure out of its hundred, so a Layer 1 item carried figure difficulty; cut to a realistic 0.3 per cent and
  asserted neutral, with the two-county ZIP made a small rural office and the repeated batch chosen so its second copy
  moves no figure out of its hundred.
- 2026-10-18, at the build: passengers on the default path's weights ranked Washington, Phoenix and Tampa, the golden's
  three, so ranking on passengers was a shortcut to the call; the winter markets' parties cut to couples and singles
  (1.65 to 1.75) and Myrtle Beach's summer family trips raised to 3,000, so passengers on any weighting carry Myrtle
  Beach.
- 2026-10-18, at the build: the first realisation (seed 471) put New York within 1.12 of the third market once the party
  draw moved onto each card; New York and Dallas set lower in the world and a seed search run over 60 worlds; seed 504.
- 2026-10-18, at stage 4: seed 504's world, where New York led Dallas for the first market left out by 2 per cent and
  a reweighting or a dropped batch could swap them (reader round 1); the handout coverage reworked plaza by plaza and
  day by day with lot choice independent of the stay, and a 120-world search run with the fourth against the fifth at
  1.07 or more; one world passed, seed 512.
- 2026-10-18, at stage 4: the passengers device cut one way (a sum written on the card coded as its first number):
  reader round 2 read Q4 in the verbatims against `party` and recoded every party, the sums added.
- 2026-10-18, at stage 4: the same device cut both ways (the parties written with who they cover coded right, so adding
  every number written counts them twice): reader round 3 recoded every party right. Both cuts are mirror devices: the
  verbatims are documented beside the coded column (methods report 4.2), so reconciling them is the cracker's reflex,
  and no reading of Q4 the frozen documents leave open is both determinate and missed by a careful parser.
- 2026-10-19, re-root tried on paper: the same parking survey with the third pick held unless its lead over the first
  market left out clears twice its design-based standard error (cards clustered by handout day, weighted by the return
  window). Measured on the v1 pack it cannot bind: 73,909 returned cards put Phoenix, Tampa and Washington each 3.5
  standard errors clear of New York on the weighted card-level variance and 2.3 to 3.4 clustered by day; binding it
  would need a tenfold smaller sample and same-day group travel, a planted structure, and the clustering unit itself
  is arguable when the waves are consecutive days. Dropped before any data was cut.
- 2026-10-20, re-root: architecture 1 (the parking card survey, replies censored by the collection close) spent at
  Gate F, every reader landing the call, with its ask device a mirror device; by the author's rule (no retirement)
  architecture 2 is a fresh world in the least-drawn ETL task type, its decisive step one the record does not display.
- 2026-10-20, at the draw: repeat candidates who saw the anchor items on an earlier attempt, left in the equating
  sample: an anchor-contamination screen beside task450's, and the sample definition has to be filed anyway (a
  convention), which files the step; kept only as the filed sample (first attempts), with no exposure in the data.
- 2026-10-20, at the draw: Tucker against Levine under a large cohort difference (the anchor's reliability): the two
  differ by less than their sampling error at the cut and nothing a pack can carry forces one, a fork.
- 2026-10-20, at the draw: 2025 responses re-scored as a labelled trend sample: the label names the drift check, so
  the organ announces the step; replaced by the contractor's validity papers, which its QC summary reports only as
  agreement rates.
- 2026-10-20, at the draw (prototype 1): an anchor of 15 multiple-choice items and two of the three written
  assignments, heavier in written work than the test: the golden's methods split (Tucker 56 against chained
  equipercentile 57) and missed the generating truth; the anchor made proportional (20 items and one assignment, 44
  per cent written by points, as the test is).
- 2026-10-20, at the draw: filing the program's equating method (Tucker) in the 2025 technical report to close the
  equipercentile spread: its literal execution on the anchor as scored is the default path's cut, an official decoy;
  the method stays unfiled and the world is tuned so that Tucker, Levine and chained linear (each at three synthetic
  weights) and chained equipercentile agree on one cut with margin.
- 2026-10-20, stage 3: WA2's validity papers scored by the 2025 leaders' consensus (an audit set): `heart` blocked
  ban.calibration and ban.artifact against task473 once task249 was marked spent; redrawn as June 2025 responses
  carrying the score both of their 2025 reads gave, the two scoring regimes' overlap on the same responses and the
  operational metric the 2025 anchor scores are on (validity sample drawn on its own stream so the shift sits mid-bin:
  0.98 anchor points, raw 49 with 0.38 and 0.37 of margin, every rung and set unchanged).
