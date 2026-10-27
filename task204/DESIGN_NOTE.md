# task204, Beldarrig ETB: the outdoor air the Tulrohan Block actually gets

Architecture v1, drawn 2026-10-27 (wave 5, oviya13ya). New number, no prior architecture. Every figure in
this note is now a measurement on the cut pack, printed by `generator/checks.py` (94 checks),
`generator/verify.py` (23 claims, bundle only) and `generator/ceiling.py`, from a generator that rebuilds
to byte-identical output twice over. Nothing here is owed.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task204.json`, registered 2026-10-27 (`guard.py check`: WARN, two WARNs, nearest driver 0.06) |
| Domain / task type | `physical-environmental-sciences` (client domain), task type `environmental-monitoring-exceedance`, which serves anomaly-detection |
| Objective | Anomaly Detection & Diagnostics: a monitoring campaign flagged a block, and the call is whether the flag is a genuine ventilation shortfall and how large it is |
| Prompt shape | `07`, grid-of-cells (space x month monitoring grid), criteria arithmetic below |
| Decision type / answer unit | `quantity_figure` / `rate_or_share`: the block's outdoor-air supply in litres per second per occupant present, to the nearest 0.5, and the remedy it points to |
| Gap / generators | `objective` then `population`; `G7` operating window (decisive), `G3` record versus operation |
| Gate G mechanism | `method_or_model_selection`, read against the vocab in the card's notes: two estimators of one filed quantity, the one that stands pinned by the data's own structure rather than by validation or a standard |
| Strategy / Layer 2 | `decomposition_attribution`; `estimation_fit`, pattern `own:unsteady-balance-across-a-filed-session-window` |
| Calibration organ | `none`. No corpus, no twin pair, no colleague voice carries the call |
| Context artifact | `filed_standard`: the campus monitoring procedure note (the 1,500 ppm screening indicator) and the TGD-M4 extract (8 litres per second per person) |
| World | Ireland, EUR, Beldarrig ETB's Kilmoneen Further Education Campus, Tulrohan Block; personas drawn with `guard.py names --geo ireland --seed 204` (Aileen Menton, Conall Murtagh), never typed |
| Forum / forcing event / org | `executive_team` (the ETB's senior management team settles the minor-works list) / `budget_or_appropriation` (January's minor-works allocation) / `university_or_school` |
| Spine | `bms_co2_5min_autumn2026.csv`, 293,559 rows, one row per monitored space per five-minute stamp |
| Deliverables | `tulrohan_ventilation_assessment.xlsx`, `tulrohan_session_balance.png` |

**Data-native sentence.** The two Tulrohan units run on a timetable-linked schedule, so the longest
interval in the record with the plant in its occupied state and the room empty is one logging step of five
minutes, and the field's own decay measurement can never see the rate the standard is about; and the
Tulrohan spaces are large, so their response time (volume over flow, measured at 189 to 355 minutes here)
runs 3.4 to 6.5 times a 55-minute timetabled session, which leaves no settled level anywhere in the record
either. The two decay windows the record does hold are the overnight off period and the midday setback,
and both measure a different plant state: they file 1.09 and 1.96 litres per second per occupant present.

**Criteria arithmetic (25 or more).** Ask A, 14 monitored spaces x 4 calendar months x 2 figures a cell =
112; Ask B, 14 spaces = 14; Ask C, the block's 6 spaces = 6; Ask D, 4 rises x 3 fields = 12. That is 144
ask criteria, plus 4 on the recommendation and its critical components (the block's rate, the verdict
against the 8 litres per second per person requirement, the remedy, and the evidence that no settled
reading exists in the block) and 2 on instruction-following: 150 criteria.

**Sources read, one line each.** `stumping` 1.1i (a recovered quantity, not a ranking: taken, and the floor
screen below is why); 1.6a (an unobserved quantity, two grains, a construction forced by arithmetic with no
free parameter: taken, with the forcing grain the attendance register's per-session counts); 1.1b (the
field's own method sits at rung 0, and the decisive step is that this dataset breaks its precondition:
taken); 1.1e (a watch or plant schedule recorded for its own sake: taken, the BMS plant-status file);
`determinism-check` section 1 (the data's structure forces the method, the first-ranked closure).

**Two WARNs from `guard.py check`, answered.** `repeat.decision`: `quantity_figure` repeats task157, and it
is kept because `stumping` 1.1i measures a recovered quantity as the only decision type this objective's
ships hold, while every ranking died; the answer differs in kind, a physical rate against a share.
`repeat.deliverables`: the `png` plus `xlsx` set repeats task157; kept because an estates officer sends a
workbook and one chart, and the chart is the only way the non-settling session reads at a glance.

**Abstraction test, run by hand because the text screen cannot see it.** `guard.py slots` on the mechanism
nouns returned task120, whose shipped driver is a mass balance with the stock change built from tank
heights. That is the nearest insight on file and the driver score does not show it (nearest driver 0.06,
task120 absent). It differs: task120 recovers a flow as the residue of a subtraction, a measured stock term
being added to it, while here the unknown is the balance's own transport coefficient and the error is that
the recorded level has not reached the state the easy estimator assumes, so both of the field's quick reads
fail in opposite directions (the settled-level read high by 2.16 times, the unoccupied decay low by 7.6
times). Differentiation lines for task193, task249 and task254 sit on the card.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, with every field read
correctly, every filed rule applied and the data clean.

1. Read `bms_co2_5min_autumn2026.csv`, drop the flagged sensor-swap gap, correct the local-time stamps
   across the October clock change, and keep the 28 September to 11 December window.
2. Join the autumn timetable to get each monitored space's session windows, and the attendance register to
   get the occupants present in each session.
3. Take the campus outdoor sensor as the baseline and compute each session's mean carbon dioxide excess
   over it.
4. Apply the field's standard steady-state relation, outdoor air per person equals the per-person
   generation rate in TGD-M4's table divided by the excess, to each session.
5. Occupant-weight the session rates over the term for the six Tulrohan spaces and report the block figure
   against the 8 litres per second per person requirement.

- **Ends on:** 11.0 litres per second per occupant present, 10.974 before rounding on the cut pack
  (10.953 on the generator's clean truth), which clears the 8 litres per second per person requirement by
  1.372 times, so the block's flag is read as occupant density and January's allocation is spent on the
  timetable change.
- **Golden:** 5.0 litres per second per occupant present, 5.074 before rounding (5.041 on the clean
  truth), sitting 0.176 from the nearer edge of its printed cell, which fails the requirement by 1.577
  times, so the allocation funds the block's air-handling replacement.

## Stump sentence

A competent solver reads each timetabled session's mean carbon dioxide excess as though the space had
settled at it, divides the filed per-person generation rate by it, occupant-weights the result across the
term and files 11.0 litres per second per occupant present for the Tulrohan Block, 10.974 before rounding,
clearing the standard
and sending January's allocation to the timetable; the step that lands them there is treating a
concentration that is still rising as a settled level, in spaces whose response time runs 3.4 to 6.5
times the length of the session the timetable files.

## Three rules

- **Task type:** `environmental-monitoring-exceedance` in physical-environmental-sciences, the cell whose
  own object is a monitored quantity judged against a standard's limit, which serves anomaly-detection.
- **Domain test:** the deciding quantity is the outdoor-air supply rate per occupant present, which
  building physics estimates from a space's own carbon dioxide record (source from occupancy, removal by
  air supply, storage from the room's volume); swap the nouns and there is no volume, no per-occupant
  generation rate and no response time, so the quantity stops existing.
- **Swap:** "Do the six wards in the Tulrohan Block get the eight nurses per patient that the standard
  requires" reads as a staffing count and loses the whole task, because nothing then has a volume, a
  generation rate per occupant or a response time of volume over flow, and there is no sense in which a
  measured level could be unsettled.
- **Layer 1:** the BMS export in Irish local time across the October clock change, 25 October carrying 300
  stamps (the plant's own system writes local time); room volumes in a table inside the as-built
  room-data-sheet PDF (the only place the design team recorded them); one analyser replaced mid-term with a
  40 ppm offset either side of its span check (the maintenance contract's own log); enrolment group sizes
  beside the statutory attendance register (two systems kept for two purposes); the campus outdoor analyser
  with a two-week gap filled from the Mace Head station's UTC publication; 441 session windows straddling
  the midday setback in the plant schedule, none of them in the block; 18 whole days and a counted number
  of scattered samples lost to a field bus fault, each whole day raised as a work order; room codes spelled
  three ways across the BMS, the timetable and the as-built set; one exported concentration column carrying
  thousands separators and a ppm suffix. Every item is asserted neutral in `checks.py`: the call prints 5.0
  with each of them corrected. None of it is placed to be caught and none of it carries the call.
- **Layer 2:** `estimation_fit`. The deciding rate is unobserved, and the estimator that stands has to
  integrate the space's unsteady carbon dioxide balance across the session the timetable files, because the
  record holds no settled level and no unoccupied interval with the plant in its occupied state.
- **Decisive step:** integrate each space's carbon dioxide balance over each timetabled session, so the
  stored term (the room's volume times the change between the session's own first and last reading) carries
  what a settled reading assumes away, and recover the supply rate from the session's generation and its
  integrated excess.
- **Not semantics:** every field is reported, correct and unambiguous; the concentrations are true
  readings, the attendance register states who was present, the plant status codes say what they mean, and
  a solver who reads every one of them correctly still files 11.0 because the error is in treating a mean
  of a rising series as an equilibrium, not in reading anything.
- **Not rule application:** no shipped sentence states the balance, the stored term or the session
  integration; the standard files the requirement (8 litres per second per person) and the generation rate,
  and the procedure note files only the 1,500 ppm screening indicator. What the filed rules leave open is
  the estimator family, and it was measured: the enumerated family of ten readings spreads the block
  figure 1.09 to 10.97 litres per second per person, while the standing family (the seven constructions
  that satisfy the balance the record supports, namely the session-integrated form under four quadratures,
  two decimations and the regression of the volume-weighted derivative on the excess) spreads 0.229
  of one printed bin, and files one call; the loudest thing that rules the rest out is the record itself,
  the plant-status file for the two decay routes and the non-zero end-of-session slope for the six settled
  readings, not any clause.
- **Analyst test:** with the data clean and every rule applied, the easy route is the field's own
  steady-state carbon dioxide estimate taken on each session's mean excess and occupant-weighted over the
  term, which files 11.0 litres per second per occupant present, 10.974 before rounding, and clears the
  standard, against a golden of 5.0. Asserted on the clean truth and again on the cut pack.
- **Estimand:** the outdoor air supplied to the six Tulrohan Block teaching spaces across the timetabled
  teaching sessions of 28 September to 11 December 2026, in litres per second per occupant present, as one
  rate over those sessions, compared with the 8 litres per second per person TGD-M4 requires; filed in
  `prompt.txt` and in the block's capital bid sheet, which lists the six room codes.
- **No decoy:** nothing is planted to be caught. There is no copied block, no withheld rule, no memo or
  briefing arguing a figure, no stakeholder number, and the one wrong-basis artifact (the commissioning
  record's design supply of 8.5 litres per second per person at design occupancy) is declared in
  `metadata.json`, is ruled out by its own deferred air-flow-proving note and is nowhere near either the
  default path's 11.0 or the golden's 5.0.
- **No certified replay:** no certified, published or closed figure in the pack is reproduced by the wrong
  method; the commissioning record states a design intent and never a measured supply, and no document
  carries a supply rate for any monitored space.
- **Lesson:** a measured level is evidence about a rate only once the system's own response time is set
  against the window the measurement spans; no build on file teaches it, the corpus's nearest insights
  being a stock term omitted from a subtraction (task120) and values censored at an instrument's limit
  (task189).

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 session-mean steady-state read | the procedure note names the screening indicator, not this | the excess column is one subtraction away | yes, the field's own screening practice | none | the battery reaches it | one divide | none | readable |
| R1 final-15-minute mean read | none | same columns | yes, the obvious "it has not settled" patch | none | plotting one session suggests it | one divide | none | readable |
| R2 peak-sample read | none | same columns | yes, guidance's peak carbon dioxide | none | the battery reaches it | one divide | none | readable |
| R3 session-integrated unsteady balance (decisive) | no sentence anywhere states the balance, the stored term or the integration | no column holds a rate, a storage term or a response time; the stored term is two rows of one series, not a field | the reflex for a carbon dioxide record is the settled read, which is R0 | no control scores it and none refutes the settled read | the battery stops at the exceedance indicators and the capture rate | no: an integral over 55 minutes of a series, a volume times a difference, and a divide | every file it needs (the series, the timetable, the attendance register, the room volumes) is needed by R0 to R2 as well, so nothing in the pack exists for it | silent |

Test 7 is answered by inspection: delete the decisive step and the pack is unchanged, because the series,
the timetable, the attendance register, the room volumes, the outdoor baseline and the plant schedule are
all needed by the default path and all exist for the campus's own reasons (comfort monitoring, teaching
administration, statutory attendance, the as-built record, air quality reporting, energy management).

Residual risk, stated rather than argued away: test 5 is the exposure. A solver who plots one session sees
the series still rising at the bell. The screen's answer is that seeing it and integrating the balance are
different steps, and the ladder prices the first one: R1 and R2 are exactly what a solver who notices does,
and both still clear the standard by 1.164 to 1.209 times.

## Semantic fork table

| id | Term or convention | Reading taken | Alternatives | Ruled out by |
|---|---|---|---|---|
| SF1 | per person | per occupant present, from the attendance marks, learners and staff alike | enrolled group size; design occupancy | `prompt.txt` ("per occupant present") and the standard's own reporting clause; measured, the enrolled reading files 6.575 and the design-occupancy reading 5.799 against 5.074, so the term is filed in the asking sentence rather than left to converge |
| SF2 | timetabled session | the autumn timetable's session rows for the space | the room-booking window; an occupancy-detected window | `prompt.txt` ("this term's timetabled sessions") and the bid sheet; the booking system is not in the pack as a session source |
| SF3 | outdoor baseline | the campus outdoor analyser, its two-week gap filled from the Mace Head station | a fixed 400 or 420 ppm; the station throughout | the campus analyser is the site's own record, and the two agree within 7.1 ppm over 1,464 overlapping hours; a baseline wrong by six ppm everywhere still files 5.121 and prints 5.0, asserted in `checks.py`, so same call |
| SF4 | per-person generation rate | the one value TGD-M4's design data table gives for a teaching or practical space, 0.0072 litres per second | a higher metabolic rate; a per-area rate | the extract's table carries exactly one per-person carbon dioxide figure and no activity band, asserted in `checks.py`, so there is nothing to choose between |
| SF5 | room volume | gross internal volume from the as-built room data sheet | floor area times a nominal 2.7 metres; the fire strategy's net volume | the as-built sheet is the only file in the pack carrying a room volume in cubic metres, asserted in `checks.py`, and the prompt names the room data sheets; measured, the area-times-2.7 reading files 8.054, a different call, which is why the volume is taken from the sheet and not inferred |
| SF6 | the monitored period | 28 September to 11 December 2026 | the whole sensor record, which starts at the pilot space in June | `prompt.txt` names the window |
| SF7 | timestamps | Irish local time as the export writes them, with the October clock change kept | UTC throughout; the repeat hour dropped | the export header states the offset per row; the block's sessions never fall in the repeat hour, which is a Sunday, so same call on the main figure (the asks grade it) |
| SF8 | rounding | once, at the end, to the nearest 0.5 litres per second per person | per space then averaged; per session then averaged | stated in the asking sentence; asserted in `checks.py` |
| SF9 | the block | the six room codes the capital bid sheet lists | every space in the building; every monitored space | the bid sheet files the six, and the prompt names the block; measured: the pooled-over-14 reading files 8.36, a different call, which is why the population is filed and not left open |
| SF10 | a session with nobody present | kept, contributing zero generation and its own excess | dropped | the estimand is over the timetabled sessions, so an empty session is one of them; measured on the cut pack, no block session carries nobody present, so the reading cannot arise and keeping or dropping files 5.074 either way |

## Ladder

Four rungs, each defensible, each reproducing from the raw files, each naming its own figure. Block figure
in litres per second per occupant present; the decision boundary is 8.0; the printed bin is 0.5.

| Rung | Analysis | Figure | Distance to the golden | Clears or fails 8.0 | Dies to |
|---|---|---|---|---|---|
| R0 | the field's steady-state read on each session's mean excess, occupant-weighted (the default path) | 10.974 | 5.900 | clears by 1.372x | nothing in the pack: it is the reflex, and only the balance moves it |
| R1 | the same read on the final fifteen minutes of each session | 9.675 | 4.602 | clears by 1.209x | the session's last reading is only about half the equilibrium excess, so the read still overstates by about two times |
| R2 | the same read on each session's peak sample | 9.313 | 4.239 | clears by 1.164x | the peak sits at the bell rather than at a plateau, the spaces' response time running 189 to 355 minutes against a 55-minute session |
| R3 | the session-integrated unsteady balance (decisive) | 5.074 | 0 | fails by 1.577x | nothing: it is the golden |

Rung worth in bins of 0.5: R0 to R1 2.60, R1 to R2 0.72, R2 to R3 8.48. The decisive move is the largest
gap and is not the smallest, every correction walks the same way, and only the decisive move crosses the
boundary. Rung clearances against the 1.15x floor: 1.372, 1.209, 1.164 on the clearing side and 1.577 on
the failing side, so no rung sits inside the floor. The floor is what fixed the block's supply rates: a
first world put the peak-sample rung at 1.140x, inside the floor, and lifting the six spaces' occupancy
and their supply together, which shortens the response time without moving a concentration anywhere,
carried it to 1.164x with the golden still printing 5.0.

Two routes that are not rungs because a shipped fact kills them on sight, kept in the reflex sweep: the
overnight decay files 1.09 (the plant-status file shows the air handling off outside the unit's occupied
band) and the midday setback decay files 1.96 (the same file shows the fan at setback between 12:00 and
12:55). They are the field's other standard method, and the data-native sentence is why neither can reach
the rate the standard is about.

**Bin test** (`determinism-check`, the Bins bullet), in units of the printed bin of 0.5:

| Reading | Measured | Bins |
|---|---|---|
| (a) the decisive step's worth, nearest rival reading less the golden | 4.239 | 8.48 |
| (b) the spread between the defensible populations the estimate could be read off (seven subsets, from all timetabled sessions to mornings only) | 0.155 | 0.31 |
| (c) the sampling interval of the construction the golden uses (four quadratures, 10 and 15 minute decimation, the regression member) | 0.115 | 0.23 |

(a) exceeds (b) plus (c) by 15.8 times, and (a) is the largest rung gap rather than the smallest. The three
filed readings: the test is necessary and not sufficient, which is why the floor, geometric-mean, deletion
and reflex screens were run beside it; (b) does not bind, so no population fork has to be closed to buy
the step; and (c) is 0.23 of a bin against a reflex precision of the same order, so the test is not bought
with volume, it is bought by the 8.48-bin lever.

**Convergence, measured against the rival family and not the golden's own.** The rival family is the
steady-state read, and it was enumerated at six licensed readings of the same record (session mean, final
fifteen minutes, last sample, peak sample, median occupied sample, 95th percentile of occupied samples).
All six file the same call, that the block clears the requirement, while spreading the figure 9.313 to
10.974 (1.661, or 3.32 bins) and printing 11.0 and 9.5, the lowest member clearing the boundary by 1.164x.
So the named wrong answer is
unanimous in the verdict and loose in the figure, which is why the main call grades the figure and the
remedy rather than the verdict alone. The golden's own family was measured separately and is not the
convergence claim: seven constructions, spread 0.229 of a bin, one printed call.

**Reflex sweep, run as code on the cut pack.** Ten routes: the six rival readings above, the overnight
decay (1.09), the midday setback decay (1.96), the balance pooled over all 14 monitored spaces instead of
the block (8.290), and the commissioning record's design supply (8.5). None lands within one bin of the
golden; the nearest miss is 6.23 bins away and is a population error that SF9 files.

**Floor and geometric-mean screens.** Measured across the 14 monitored spaces: sd(log correction factor)
0.2482 against sd(log base) 0.7038, so rho is 0.3526, under the 0.80 the multiplicative floor needs, and
the realised correlation between the naive figure and the truth is +0.9724. The reading that follows is the
one that fixed the decision type: a ranking of spaces on the naive figure is very nearly truth-equivalent,
so no ranking may be graded here, and none is. The designation is a different matter and is not reachable
at all: the naive family puts 0 of 14 spaces below the requirement where the truth puts 6. The
geometric-mean route does not apply, by arithmetic rather than by preference: the graded quantity is not an
observable divided by a per-case factor, the naive figure is not a transform of the golden, and there is no
candidate-level multiplier to estimate.

**Deletion tests.** 1, delete every wrong number and misleading claim: the pack carries none, and the
difficulty is unchanged because the default path is built from correct readings. 2, clean data: the easy
route on the generator's clean truth still files 10.953 and prints 11.0, which is the assertion
`checks.py` executes. 3, lens
swap: reading the call as "is the flag genuine" rather than "what is the rate" changes nothing, because
both answers come from the same figure. 4, identity: no governing arithmetic closes over shipped
quantities, since no file holds a supply rate. 5, control direction: the screening flags, the outdoor
station and the plant-status file tie on every basis (below). 6, first moves: the one-period group-by, each
clause's natural reading, the hygiene battery and the exceedance indicators all stop at the rival family.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 | Population: the six Tulrohan spaces' timetabled sessions, 28 September to 11 December 2026 | filed in `prompt.txt` and the bid sheet (SF2, SF6, SF9); C1, the seven-subset spread 0.31 of a bin, every subset printing 5.0 |
| 2 | Unit of account: litres per second per occupant present | named in the asking sentence (SF1) |
| 3 | Attribution window: each session's own start and end from the timetable | filed; every session boundary sits five minutes clear of the plant setback edges |
| 4 | As-of dating: the export and the register as pulled on 15 December 2026 | the export header states the pull; the register ships with it |
| 5 | Version basis: the attendance register's amended final state | one version per session with an amendment flag; C1, same call |
| 6 | Denominator: occupant-seconds present over the same sessions | filed in the asking sentence (SF1) |
| 7 | Weighting: total outdoor air supplied over total occupant-seconds, not a mean of session rates | C1, five aggregations (the ratio of totals, the occupant-weighted mean of session rates, the unweighted mean of space rates, the session-weighted mean and the occupant-weighted mean) spread 0.091 of a bin and all print 5.0 |
| 8 | Window length: the monitored period, no trailing window | filed (SF6) |
| 9 | Boundary inclusivity: a session's first and last recorded reading, both inclusive | C1, the five-minute grid places no sample on a session boundary |
| 10 | Rounding path: once at the end, to the nearest 0.5 | stated in the asking sentence (SF8); asserted in `checks.py` |
| 11 | Tie-break: none, the answer is one figure and no candidate list is ranked | not reachable by construction |
| 12 | Maturity and censoring: none, every timetabled session in the window has run; readings are missing where the field bus was down | C1, integrating what was recorded against keeping only the sessions whose whole grid was recorded files 5.0739 against 5.0784, 0.009 of a bin apart, and the analyser swap sits outside the block |
| 13 | Order of operations: integrate, then divide; the stored term carries its own sign | C1, the regression member agrees to 0.02 of a bin |
| 14 | Row order: the export is sorted by space then stamp | the construction is order-free; asserted over permutations |
| 15 | Duplicate resolution: the October clock change repeats one hour of stamps | the export's offset column separates them (SF7); the repeat hour is a Sunday, so no block session falls in it |
| 16 | Identity normalisation: room codes across the BMS, the timetable and the as-built sheet | the campus room register's crosswalk; C4, the three spellings map to one code |
| 17 | Netting against gross: the stored term may be negative and is kept with its sign | filed scope: the balance is over the session, not over positive changes |
| 18 | Dimensional units: ppm against volume fraction, litres against cubic metres, minutes against seconds | units stated in the data and in the room data sheet; asserted |
| 19 | Code and status semantics: the plant status codes occupied, setback and off | the plant schedule's own legend; never the stump, and only the two decay routes turn on it |
| 20 | Integerisation: none in the graded figure; attendance is a whole count | by construction |
| 21 | Clause scope: TGD-M4's requirement applies per teaching space; the bid is for the block | the bid sheet files the block as the decision's unit, and the workbook carries both |
| 22 | Forward window contents: January's allocation chooses between the two costed remedies, with the plant settings and the spring timetable unchanged | the bid sheet files both options and the academic calendar files the spring term; the call is a measurement of a plant property the spring term inherits, and this note records it as retrospective-measurement-driving-a-forward-commitment |

## Literal reader

A judge who executes the shipped text word for word takes the six room codes from the bid sheet, the
timetabled sessions of 28 September to 11 December 2026 from the autumn timetable, the occupants present
from the attendance register, the outdoor baseline from the campus sensor, the volumes from the as-built
room data sheet and the generation rate from the TGD-M4 extract, and asks for one rate in litres per second
per occupant present over those sessions to the nearest 0.5. That execution admits the seven constructions
of the balance the record supports and nothing else, and they print 5.0 together, spread 0.229 of a bin;
the steady-state readings are not admissible executions of the estimand because they assert a settled level
the same record refutes: the block's spaces have response times of 189 to 355 minutes against a 55-minute
session, so a session's last reading sits at about half its own equilibrium excess.

## Oracles

| Control | What it confirms on the wrong path | Ties on every basis |
|---|---|---|
| the procedure note's 1,500 ppm screening flags | the flag is computed from the record and never from a rate, so the same spaces are flagged under every reading of it; measured, the block carries 56.49 of the campus's 63.32 occupied hours over the indicator, which is why the block was brought forward | yes |
| the campus outdoor analyser against the Mace Head station | agree within 7.1 ppm over 1,464 overlapping hours under every reading | yes |
| the plant-status file | kills the two decay routes under every reading of the series | yes |
| the commissioning record's design supply, 8.5 litres per second per person at design occupancy | reads as "clears" on the wrong path; it is a design intent, not a measurement, its own outstanding-items section records that proving at the supply terminals was deferred, and TGD-M4 4.3 says volumes proved at a unit do not demonstrate compliance | declared wrong-basis distractor in `metadata.json`, never the stump, and equal to neither 10.974 nor 5.074 |

No control ties only under the golden, so there is no oracle to cut. The ask layer's referee never
arbitrates the call.

## Ask sheet

The asks are decoupled from the call: not one of them needs the balance, the stored term or a supply rate,
so a response that lands every ask has learned nothing about the main call, and a response that lands the
call gets no ask for free. Each carries its own silent device (`supplemental-stumping` Part 2.1), and each
device's strength is measured on the cut pack by `generator/ceiling.py`, which runs the careful solver's
path for the ask against the shipped files and counts what that path lands.

| Ask | Figures | Device the careful solver's path walks into |
|---|---|---|
| A, occupied hours recorded and occupied hours above 1,500 ppm, per monitored space per calendar month | 112 | "occupied" is the air handling unit's occupied state in `bms_plant_status_autumn2026.csv`, not the timetable's sessions, and the two differ by the midday setback, by the pre-heat on the two fixed-clock units and by the 441 sessions that straddle a setback band; the five-minutes-to-a-reading and month-of-the-local-stamp conventions are filed in the procedure note, once |
| B, the share of expected readings received per monitored space over the term | 14 | "expected" counts the term's 48 teaching days only, so the midterm break and the two closure days come out of the base; counting against all 75 calendar days puts four spaces above a hundred per cent, because 25 October carries 300 stamps |
| C, the mean occupants present per timetabled session for each of the block's six spaces | 6 | the enrolment group size and the attendance marks disagree in every session, and the year-one construction cohort is taught in two rooms in the same period, which the enrolment file cannot show |
| D, the four largest rises between a session's first and last reading in the block, with space, period and date | 12 | the largest rise on any day in the block spans the morning and the midday setback rather than one session, so a rise measured outside the timetabled window beats every within-session rise and names no period at all |

- **Pair ceiling, both responses off the main call:** 33.2 per cent (`generator/ceiling.py`, measured).
- **Sensitivity:** 49.7 per cent with one of the two on the call, 66.2 per cent with both on it. The ladder
  is what keeps at least one off: every licensed steady-state reading of the same record files that the
  block clears the requirement.
- **Mirror leakage:** 31.9 per cent of ask weight, under the 50 ceiling.
- **Each of the top two keeps** 32 and 22 per cent of the ask weight, both under the 40 ceiling.
- **Measured by:** `generator/ceiling.py` on the cut pack, with the per-ask miss counts from
  `generator/checks.py`. No reader, probe or scored read is run: stump power is argued here and measured by
  the portal alone.

| Ask | What the cracker does | Figures that path lands | Cracker verdict |
|---|---|---|---|
| A | counts hours over the timetabled sessions rather than over the unit's occupied state | 28 of 112, and every one of the 28 is a cell whose answer is zero under both readings | miss |
| B | divides every reading received by 288 times every calendar day in the window | 0 of 14 | miss |
| C | takes the enrolment group size as the occupancy | 0 of 6 | miss |
| D | ranks the largest rise anywhere in a day rather than inside a timetabled session | 4 of 12, and no period at all | miss |

## Leak review

`leak.py --asof 2026-12-15` reads CLEAN on eight of its eleven sweeps and REVIEW on three, with no LEAK.
One line per REVIEW, the fix being none in every case.

- Sweep 1, `minor_works_thread.txt`: the estates officer's own mail thread with the facilities manager,
  which sets the January decision and points at the record set and the maintenance log. It describes no
  column and names no file's role.
- Sweep 3, seventeen hits in the as-built sheets, the procedure note and the thread: every one is a room
  code fragment the write-up also carries (104, 107, 103, 016, 205, 012, 108, 211). No graded figure
  appears in any shipped document, which `checks.py` asserts separately over the write-up's own answer
  blocks.
- Sweep 4, five documents carrying stump-paragraph terms: the terms are the field's ordinary nouns
  (supply, record, volume, carbon, dioxide, design, measured). `checks.py` sweeps every csv, txt, xlsx and
  pdf for the vocabulary that would name the move (the balance, the stored term, the integration, a
  response time, a steady state) and finds none.
- Sweep 4, the prompt sentence carrying two stump terms: it is the deliverable sentence, naming the asks
  and their units. It states no method.
- Sweep 8, `air_temp_c` in the temperature export: a building management system point name carrying its
  own unit, which is what `dataset-generation` section 3 asks each file to do.
- Sweep 8, `flag` in the Mace Head file: the station's own data-quality column, published under that name.
- Sweep 9, four 2027 dates in the academic calendar: the spring term, published before it starts. It is
  the one forward-looking record in the pack and is on the allow-list `checks.py` keeps.

## Tried and rejected

- Curtailed or inverse sampling (a measurement programme that stops at a filed count of findings), killed
  at the slots screen before any code: task198's note measures the same mechanism (M1) with the naive route
  already naming the golden at 1.301x against the designed route's 1.083x, five of eight reflexes reaching
  it, and the correction reducing to one multiplication by a filed column.
- The non-equilibrium balance read as "the omitted stock term", killed at the abstraction test against
  task120's shipped driver; kept only in the re-rooted form above, where the unknown is the balance's
  transport coefficient and not a residue, with the differentiation line on the card.
- First-order sensor lag with a response-time deconvolution, killed by arithmetic before any code: a
  first-order lag preserves the integral, so a total is untouched, and recovering a peak needs a
  regularisation choice, which is a free parameter.
- Top-truncation of an over-range analyser channel recovered against a conserved register, killed on
  readability test 5: the recovery is the hygiene battery's own reconciliation of the series against the
  register, one group-by and one subtraction.
- Per-case multiplicative corrections on this ground (laboratory recovery factors, calibration drift,
  holding-time decay), killed on the dispersion ceiling: every candidate measured sd(log factor) well under
  1.4, where `stumping` prices the shape as closed.
- Interval placement of an onset against a shipped inspection schedule, killed twice over: the brief's
  closed family names the interval union, and `stumping` 1.1e has already measured the parameter-free
  correction at 0.95 to 0.96 of the golden, which is a lever of five per cent.
- Flow-weighted or diurnally weighted loads and inclusion-probability reweightings, killed on the swap test
  at the sentence, which is where the brief puts it: each reads identically with any field's nouns.
- Stage 3, the ask sheet's figure counts moved and the prompt was rewritten to carry every graded figure.
  At stage 2 the prompt asked for two of the four asks and the write-up would have graded the other two,
  which `determinism-check` section 5 calls an open fork by construction. Ask A now grades the recorded
  occupied hours beside the hours over the indicator, so no cell is empty for a well ventilated room and a
  cracker cannot bank a zero; ask D gained the period, which the day-window path cannot name. Prompt back
  through `voice-check.py` at 997 characters.
- Stage 3, the capital bid sheet's volume column was cut. It made the as-built room data sheets no longer
  the only record of a room's volume, which is the Layer 1 item the card files; the bid sheet now carries
  the as-built sheet reference instead and `checks.py` asserts the volume appears in one file only.
- Stage 3, the scattered sample losses were changed from a per-stamp rate to a counted number of
  teaching-day samples per space. At a rate, four of the fourteen capture shares collided at one decimal
  and the cracker's calendar-day base sat 0.05 of a point away from the golden in six cells; as counts the
  fourteen shares are distinct, each sits within 0.004 of a bin centre, and the cracker misses all
  fourteen by at least 0.79 of a point.
- Stage 3, ask A's hours moved from one decimal to two. An hour count that is a multiple of five minutes
  lands exactly on a one-decimal rounding boundary once every six values, and resting 112 graded figures on
  a filed rounding direction is a fragility the two-decimal report removes: the closest any figure now sits
  to an edge is 0.0017 hours against a half-bin of 0.005.
- Stage 3, the staff school column was derived from the group's own programme rather than drawn. Drawn, it
  produced tutors filed to one school whose every session taught another, which is the defect the measured
  task464 read names.
- Stage 3, the block's response times came out at 189 to 355 minutes rather than the 253 to 543 the stage 2
  prototype measured. Raising the six spaces' occupancy and their supply together leaves every
  concentration where it is and only shortens the response time, which is what lifted the peak-sample rung
  off the 1.15x floor; the ratio the stump turns on is unchanged and the note's figures are the cut pack's.
