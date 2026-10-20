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
  one survey's prevalence; here a link between two administrations, with the judged item kept). WARNs answered:
  government_agency in 36 builds (the board is the state agency that licenses teachers and approves their programs);
  ETL in 5 of the last 12 (the lane's objective); Gate G method_or_model_selection repeats task476 and runs in 9 of 12
  (the decisive move is how the judged item enters the link, a method the data selects, and no other Gate G fits);
  designation_set repeats task476 (the board designates programs for review); png and xlsx repeat task250 (a program
  workbook and the chart the committee reads are an assessment office's own products); question form "which" repeats
  task250 (the decision picks programs). Nearest driver task450 v2 at 0.11. Personas from `guard.py names --geo us
  --seed 471`; Donald Lara (in v1) and Samuel Kim (first name in task120) not used.
- **Pairing:** Education & Learning Sciences / item-response-theory-test-equating / ETL. The board's Office of
  Assessment Research conforms two scoring contractors' score files, the 2026 written-assignment read file, the
  candidates' attempt history and sixteen programs' completer lists into one results file on the 2025 reporting scale,
  then the program pass rates; the deciding quantity, the 2026 raw score at the 2025 passing standard, is the equating
  that conformation needs.
- **World:** an unnamed U.S. state's Board of Educator Standards and Licensure and its Elementary Literacy Instruction
  test (60 multiple-choice items and three written assignments, each assignment read twice on a 1 to 4 rubric and
  counted twice, raw 0 to 108, reported on 100 to 300 with 240 passing). The previous contractor scored and equated the
  2025 form; from 2026 a new contractor scores and the board's office equates. The 2026 form shares 20 multiple-choice
  items and one written assignment with the 2025 form, an internal anchor built in proportion to the test's two
  formats. Sixteen preparation programs (universities and alternative routes) submit completer lists.
- **Decision:** which programs' 2025-26 completers have a first-attempt pass rate below 70 per cent, the board's line
  for a formal program review in 2027.
- **Shape 10:** the call; each program's first-attempt pass rate and review verdict (32); the 2026 raw passing score;
  the programs nearest the line on each side; the chart's parts; the files: 40 before the asks.
- **Strategy:** other (`own:rater-severity-drift-on-a-constructed-response-anchor`), Gate G
  method_or_model_selection, calibration form gold_standard_subsample (the validity papers).
- **Data-native sentence:** the anchor's written assignment is its only item scored by people, and people's standard
  moves between scoring seasons: the 2026 contractor's raters, trained by new scoring leaders, score the 2025 validity
  papers for that assignment about a quarter point per read below the consensus the 2025 leaders set, while the 2026
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

Provisional until the generator is calibrated (figures from the prototype `proto2.py`, seed 482).

1. Conform the 2025 score file (previous contractor's layout) and the 2026 score file (new contractor's layout), key
   every attempt to the board's educator identifier and read each candidate's first attempt from the attempt history.
2. Build the equating samples the 2025 technical report names, each year's first-attempt candidates: the 2025 total
   and anchor score on the 2025 form, the 2026 total and anchor score on the 2026 form, the anchor being the 20 shared
   items plus twice the carried-over assignment's score.
3. Equate the 2026 form to the 2025 form through the anchor (Tucker, Levine, chained linear or chained equipercentile)
   with the assignment as the 2026 raters scored it; the 2026 raw passing score is the smallest raw score whose
   equated score rounds to the 2025 passing raw score.
4. Each program's 2025-26 completers with a first attempt by the as-of date: a first attempt on the 2026 form passes
   at the 2026 cut, one on the 2025 form keeps its 2025 result.
5. The programs under 70 per cent go to review.

Ends on: the cut with the assignment as scored, two or three raw points above the golden's, and its larger review set.

Golden: the cut with the carried-over assignment's 2026 reads moved up by the mean amount the 2026 raters scored its
2025 validity papers below their consensus, and its smaller review set.

## Stump sentence

The default path equates the 2026 form to the 2025 form through the 21-item anchor as the 2026 raters scored it and sets the 2026 raw passing score two to three points too high, sending more programs to formal review than the golden; the 2026 raters scored the carried-over written assignment's 2025 validity papers about a quarter point per read below their consensus scores, so the anchor reads the 2026 cohort as weaker than it is, and screening that item out of the anchor instead overshoots, because the cohort really did write worse; with the written assignment put back on the 2025 rating standard the anchor sets the cut the golden takes.

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
