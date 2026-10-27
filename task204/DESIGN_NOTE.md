# task204, Beldarrig ETB: the outdoor air the Tulrohan Block actually gets

Architecture v1, drawn 2026-10-27 (wave 5, oviya13ya). New number, no prior architecture. Every figure in
this note is a design-time measurement on the generator's clean truth, from
`<scratch>/task204/screen.py`, run twice to byte-identical output with `PYTHONHASHSEED=0`; the shipped
figures are owed from `generator/` at stage 3.

## Draw

| Axis | Value |
|---|---|
| Card | `<scratch>/task204/task204_card.json`, pending registration by the author (`guard.py check`: WARN, two WARNs, nearest driver 0.06) |
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
| Spine | `bms_co2_5min_autumn2026.csv`, about 302,400 rows, one row per monitored space per five-minute stamp |
| Deliverables | `tulrohan_ventilation_assessment.xlsx`, `tulrohan_session_balance.png` |

**Data-native sentence.** In a building whose ventilation plant is scheduled to occupancy, no interval in
the record has the plant in its occupied state with the rooms empty, so the field's own decay measurement
can never see the rate the standard is about; and the Tulrohan spaces are large and sparsely occupied, so
their response time (volume over flow, measured at 253 to 543 minutes here) runs 4.6 to 9.9 times a
55-minute timetabled session, which leaves no settled level anywhere in the record either.

**Criteria arithmetic (25 or more).** Ask A, 14 monitored spaces x 4 calendar months of the term = 56
graded cells; Ask B, 14 spaces = 14; Ask C, the block's 6 spaces = 6; Ask D, 4 rises x 2 fields = 8. That
is 84 ask criteria, plus 4 on the recommendation and its critical components (the block's rate, the verdict
against the 8 litres per second per person requirement, the remedy, and the evidence that no settled
reading exists in the block) and 2 on instruction-following: 90 criteria.

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

- **Ends on:** 11.0 litres per second per occupant present, 10.95 before rounding (three seeds 11.06,
  10.95, 10.56), which clears the 8 litres per second per person requirement by 1.37 times, so the block's flag is read as occupant
  density and January's allocation is spent on the timetable change.
- **Golden:** 5.0 litres per second per occupant present (three seeds 5.01, 5.07, 4.90, all printing 5.0),
  which fails the requirement by 1.58 times, so the allocation funds the block's air-handling replacement.

## Stump sentence

A competent solver reads each timetabled session's mean carbon dioxide excess as though the space had
settled at it, divides the filed per-person generation rate by it, occupant-weights the result across the
term and files 11.0 litres per second per occupant present for the Tulrohan Block, 10.95 before rounding,
clearing the standard
and sending January's allocation to the timetable; the step that lands them there is treating a
concentration that is still rising as a settled level, in spaces whose response time runs 4.6 to 9.9
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
- **Layer 1:** the BMS export in Irish local time across the October clock change (the plant's own system
  writes local time); room volumes in a table inside the as-built room-data-sheet PDF (the only place the
  design team recorded them); one sensor replaced mid-term with a 40 ppm offset either side of its span
  check (the maintenance contract's own log); enrolment group sizes beside the statutory attendance
  register (two systems kept for two purposes); the campus outdoor sensor with a two-week gap filled from
  the national station; session windows straddling the lunch unoccupied setback in the plant schedule; one
  exported concentration column carrying thousands separators and a ppm suffix. None of it is placed to be
  caught and none of it carries the call.
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
  the estimator family, and it was measured: the enumerated family of eleven readings spreads the block
  figure 0.67 to 10.97 litres per second per person, while the standing family (the three constructions
  that satisfy the balance the record supports, namely the session-integrated form, its quadrature
  variants and the regression of the volume-weighted derivative on the excess) spreads 0.24, which is 0.49
  of one printed bin, and files one call; the loudest thing that rules the rest out is the record itself,
  the plant-status file for the two decay routes and the non-zero end-of-session slope for the six settled
  readings, not any clause.
- **Analyst test:** with the data clean and every rule applied, the easy route is the field's own
  steady-state carbon dioxide estimate taken on each session's mean excess and occupant-weighted over the
  term, which files 11.0 litres per second per occupant present, 10.95 before rounding, and clears the standard,
  against a golden of 5.0.
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
and both still clear the standard by 1.20 to 1.27 times.

## Semantic fork table

| id | Term or convention | Reading taken | Alternatives | Ruled out by |
|---|---|---|---|---|
| SF1 | per person | per occupant present, from the attendance register | enrolled group size; design occupancy | `prompt.txt` ("per occupant present") and the standard's own wording; the two rivals are a different denominator over the same numerator, and their spread is owed a measurement at stage 3 because the term is filed rather than left to converge |
| SF2 | timetabled session | the autumn timetable's session rows for the space | the room-booking window; an occupancy-detected window | `prompt.txt` ("this term's timetabled sessions") and the bid sheet; the booking system is not in the pack as a session source |
| SF3 | outdoor baseline | the campus outdoor sensor, its two-week gap filled from the national station | a fixed 400 or 420 ppm; the national station throughout | the campus sensor is the site's own record and the generator builds the overlap to agree within 6 ppm and asserts it (owed at stage 3), so same call |
| SF4 | per-person generation rate | the TGD-M4 table value for seated classroom activity | a higher metabolic rate; a per-area rate | the standard's extract table, and every block session carries a sedentary subject code in the timetable |
| SF5 | room volume | gross internal volume from the as-built room data sheet | floor area times a nominal 2.7 metres; the fire strategy's net volume | the as-built sheet is the only record of volume and the prompt names the room data sheets |
| SF6 | the monitored period | 28 September to 11 December 2026 | the whole sensor record, which starts at the pilot space in June | `prompt.txt` names the window |
| SF7 | timestamps | Irish local time as the export writes them, with the October clock change kept | UTC throughout; the repeat hour dropped | the export header states the offset per row; the block's sessions never fall in the repeat hour, which is a Sunday, so same call on the main figure (the asks grade it) |
| SF8 | rounding | once, at the end, to the nearest 0.5 litres per second per person | per space then averaged; per session then averaged | stated in the asking sentence; asserted in `checks.py` |
| SF9 | the block | the six room codes the capital bid sheet lists | every space in the building; every monitored space | the bid sheet files the six, and the prompt names the block; measured: the pooled-over-14 reading files 8.36, a different call, which is why the population is filed and not left open |
| SF10 | a session with nobody present | kept, contributing zero generation and its own excess | dropped | the estimand is over the timetabled sessions, so an empty session is one of them; the spread is owed a measurement at stage 3, the generator asserting same call |

## Ladder

Four rungs, each defensible, each reproducing from the raw files, each naming its own figure. Block figure
in litres per second per occupant present; the decision boundary is 8.0; the printed bin is 0.5.

| Rung | Analysis | Figure | Distance to the golden | Clears or fails 8.0 | Dies to |
|---|---|---|---|---|---|
| R0 | the field's steady-state read on each session's mean excess, occupant-weighted (the default path) | 10.95 | 5.88 | clears by 1.37x | nothing in the pack: it is the reflex, and only the balance moves it |
| R1 | the same read on the final fifteen minutes of each session | 10.19 | 5.12 | clears by 1.27x | the session's last reading is only about half the equilibrium excess, so the read still overstates by 2.0 times; the last-ten-minute slope is positive in 60.7 per cent of block sessions on a three-sample slope, the rest noise rather than settling |
| R2 | the same read on each session's peak sample | 9.56 | 4.49 | clears by 1.20x | the peak sits at the bell rather than at a plateau, the spaces' response time running 253 to 543 minutes against a 55-minute session |
| R3 | the session-integrated unsteady balance (decisive) | 5.07 | 0 | fails by 1.58x | nothing: it is the golden |

Rung worth, measured on the graded figure: R0 to R1 0.76, R1 to R2 0.63, R2 to R3 4.49. The decisive move
is the largest gap and is not the smallest, every correction walks the same way, and only the decisive move
crosses the boundary. Rung clearances against the 1.15x floor: 1.37, 1.27, 1.20 on the clearing side and
1.58 on the failing side, so no rung sits inside the floor. The floor is what fixed the block's volumes: at
the first world the worst of the three seeds put the peak-sample rung at 1.144x, inside the floor, and
raising the six spaces' volumes eight per cent (2,400 to 4,650 cubic metres) lifted it to 1.154x with the
golden still printing 5.0 in all three seeds.

Two routes that are not rungs because a shipped fact kills them on sight, kept in the reflex sweep: the
overnight tracer decay files 0.67 (the plant-status file shows the air handling off outside 07:30 to 15:30)
and the lunch-setback decay files 1.40 (the same file shows the fan at setback between 12:05 and 12:50).
They are the field's other standard method, and the data-native sentence is why neither can reach the rate
the standard is about.

**Bin test** (`determinism-check`, the Bins bullet), in units of the printed bin of 0.5:

| Reading | Measured | Bins |
|---|---|---|
| (a) the decisive step's worth, nearest rival reading less the golden | 4.486 | 8.97 |
| (b) the spread between the defensible populations the estimate could be read off (seven subsets, from all timetabled sessions to mornings only) | 0.132 | 0.26 |
| (c) the sampling interval of the construction the golden uses (four quadratures, 10 and 15 minute decimation, the regression member) | 0.261 | 0.52 |

(a) exceeds (b) plus (c) by 11.4 times, and (a) is the largest rung gap rather than the smallest. The three
filed readings: the test is necessary and not sufficient, which is why the floor, geometric-mean, deletion
and reflex screens were run beside it; (b) does not bind, so no population fork has to be closed to buy
the step; and (c) is 0.52 of a bin against a reflex precision of the same order, so the test is not bought
with volume, it is bought by the 8.83-bin lever.

**Convergence, measured against the rival family and not the golden's own.** The rival family is the
steady-state read, and it was enumerated at six licensed readings of the same record (session mean, final
fifteen minutes, last sample, peak sample, median occupied sample, 95th percentile of occupied samples).
All six file the same call, that the block clears the requirement, while spreading the figure 9.56 to 10.95
(1.39, or 2.78 bins), the lowest member clearing the boundary by 1.195x and by 1.154x in the worst of the
three seeds. So the named wrong answer is
unanimous in the verdict and loose in the figure, which is why the main call grades the figure and the
remedy rather than the verdict alone. The golden's own family was measured separately and is not the
convergence claim: three constructions, spread 0.52 of a bin, one printed call.

**Reflex sweep, run as code on the clean truth before any figure was tuned.** Ten routes: the six rival
readings above, the overnight decay (0.67), the lunch-setback decay (1.40), the balance pooled over all 14
monitored spaces instead of the block (8.36), and the volume-weighted session-mean read (11.02). None lands
within one bin of the golden; the nearest miss is 6.6 bins away and is a population error that SF9 files.

**Floor and geometric-mean screens.** Measured across the 14 monitored spaces: sd(log correction factor)
0.3018 against sd(log base) 0.4163, so rho is 0.7249, under the 0.80 the multiplicative floor needs, and
the realised correlation between the naive figure and the truth is +0.8988. The reading that follows is the
one that fixed the decision type: a ranking of spaces on the naive figure is very nearly truth-equivalent,
so no ranking may be graded here, and none is. The designation is a different matter and is not reachable
at all: the naive family puts 0 of 14 spaces below the requirement where the truth puts 6. The
geometric-mean route does not apply, by arithmetic rather than by preference: the graded quantity is not an
observable divided by a per-case factor, the naive figure is not a transform of the golden, and there is no
candidate-level multiplier to estimate.

**Deletion tests.** 1, delete every wrong number and misleading claim: the pack carries none, and the
difficulty is unchanged because the default path is built from correct readings. 2, clean data: the easy
route on the generator's clean truth still files 10.9, which is the assertion `checks.py` executes. 3, lens
swap: reading the call as "is the flag genuine" rather than "what is the rate" changes nothing, because
both answers come from the same figure. 4, identity: no governing arithmetic closes over shipped
quantities, since no file holds a supply rate. 5, control direction: the screening flags, the outdoor
station and the plant-status file tie on every basis (below). 6, first moves: the one-period group-by, each
clause's natural reading, the hygiene battery and the exceedance indicators all stop at the rival family.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 | Population: the six Tulrohan spaces' timetabled sessions, 28 September to 11 December 2026 | filed in `prompt.txt` and the bid sheet (SF2, SF6, SF9); C1, the seven-subset spread 0.23 of a bin |
| 2 | Unit of account: litres per second per occupant present | named in the asking sentence (SF1) |
| 3 | Attribution window: each session's own start and end from the timetable | filed; every session boundary sits five minutes clear of the plant setback edges |
| 4 | As-of dating: the export and the register as pulled on 15 December 2026 | the export header states the pull; the register ships with it |
| 5 | Version basis: the attendance register's amended final state | one version per session with an amendment flag; C1, same call |
| 6 | Denominator: occupant-seconds present over the same sessions | filed in the asking sentence (SF1) |
| 7 | Weighting: total outdoor air supplied over total occupant-seconds, not a mean of session rates | C1, four aggregations agree within 0.49 of a bin |
| 8 | Window length: the monitored period, no trailing window | filed (SF6) |
| 9 | Boundary inclusivity: a session's first and last recorded reading, both inclusive | C1, the five-minute grid places no sample on a session boundary |
| 10 | Rounding path: once at the end, to the nearest 0.5 | stated in the asking sentence (SF8); asserted in `checks.py` |
| 11 | Tie-break: none, the answer is one figure and no candidate list is ranked | not reachable by construction |
| 12 | Maturity and censoring: none, every session in the window is complete and every reading is reported | stated; the only gap is the sensor swap, which is flagged and sits outside the block |
| 13 | Order of operations: integrate, then divide; the stored term carries its own sign | C1, the regression member agrees to 0.02 of a bin |
| 14 | Row order: the export is sorted by space then stamp | the construction is order-free; asserted over permutations |
| 15 | Duplicate resolution: the October clock change repeats one hour of stamps | the export's offset column separates them (SF7); the repeat hour is a Sunday, so no block session falls in it |
| 16 | Identity normalisation: room codes across the BMS, the timetable and the as-built sheet | the campus room register's crosswalk; C4, the three spellings map to one code |
| 17 | Netting against gross: the stored term may be negative and is kept with its sign | filed scope: the balance is over the session, not over positive changes |
| 18 | Dimensional units: ppm against volume fraction, litres against cubic metres, minutes against seconds | units stated in the data and in the room data sheet; asserted |
| 19 | Code and status semantics: the plant status codes occupied, setback and off | the plant schedule's own legend; never the stump, and only the two decay routes turn on it |
| 20 | Integerisation: none in the graded figure; attendance is a whole count | by construction |
| 21 | Clause scope: TGD-M4's requirement applies per teaching space; the bid is for the block | the bid sheet files the block as the decision's unit, and the workbook carries both |
| 22 | Forward window contents: January's allocation chooses between the two costed remedies, with the plant settings and the spring timetable unchanged | the bid sheet and the spring timetable ship it; the call is a measurement of a plant property that the spring term inherits, and the design note records it as retrospective-measurement-driving-a-forward-commitment |

## Literal reader

A judge who executes the shipped text word for word takes the six room codes from the bid sheet, the
timetabled sessions of 28 September to 11 December 2026 from the autumn timetable, the occupants present
from the attendance register, the outdoor baseline from the campus sensor, the volumes from the as-built
room data sheet and the generation rate from the TGD-M4 extract, and asks for one rate in litres per second
per occupant present over those sessions to the nearest 0.5. That execution admits the three constructions
of the balance the record supports and nothing else, and they print 5.0 together; the steady-state readings
are not admissible executions of the estimand because they assert a settled level the same record refutes:
the block's spaces have response times of 253 to 543 minutes against a 55-minute session, so a session's
last reading sits at about half its own equilibrium excess.

## Oracles

| Control | What it confirms on the wrong path | Ties on every basis |
|---|---|---|
| the procedure note's 1,500 ppm screening flags | the same six spaces are flagged under both routes, so it confirms the flag and never the rate | yes |
| the campus outdoor sensor against the national station | agree within 6 ppm over the overlap under every reading | yes |
| the plant-status file | kills the two decay routes under every reading of the series | yes |
| the commissioning record's design supply, 8.5 litres per second per person at design occupancy | reads as "clears" on the wrong path; it is a design intent, not a measurement, and its own note records that air-flow proving was deferred | declared wrong-basis distractor in `metadata.json`, never the stump, and equal to neither 11.0 nor 5.0 |

No control ties only under the golden, so there is no oracle to cut. The ask layer's referee never
arbitrates the call.

## Ask sheet

The asks are decoupled from the call: not one of them needs the balance, the stored term or a supply rate,
so a response that lands every ask has learned nothing about the main call, and a response that lands the
call gets no ask for free. Each carries its own silent device (`supplemental-stumping` Part 2.1).

| Ask | Figures | Device the careful solver's path walks into |
|---|---|---|
| A, occupied hours above 1,500 ppm per monitored space per calendar month of the term | 56 | "occupied" is the plant schedule's occupied state, not the timetable's sessions, and the two differ by the lunch setback and the 07:30 to 09:00 pre-heat; the October clock change gives 25 October 25 local hours |
| B, the share of expected readings received per monitored space over the term | 14 | "expected" counts the term's teaching days only, so the midterm break and the two closure days come out of the base, and the sensor-swap gap is one space's only loss |
| C, the mean occupants present per timetabled session for each of the block's six spaces | 6 | the enrolment group size and the attendance register disagree on every session, and one group is taught in two rooms in the same period |
| D, the four largest single-session rises in the block, with space and date | 8 | the largest raw rises straddle the lunch setback, so a rise measured across a session boundary beats every within-session rise |

- **Pair ceiling:** 37.2 per cent (design-time model; the measurement on the cut pack is owed at stage 3).
- **Mirror leakage:** 37.0 per cent of ask weight, under the 50 ceiling (same model, same owing).
- **Measured by:** `generator/ceiling.py` (design-time model at stage 2; re-run on the cut pack at stage 3).

| Ask | What the cracker does | Cracker verdict |
|---|---|---|
| A | counts hours above 1,500 ppm over the timetable's sessions and keeps the local-time stamps as given | miss |
| B | divides received readings by 288 times every calendar day in the window | miss |
| C | takes the enrolment group size as the occupancy | miss |
| D | ranks raw consecutive-reading rises over the whole series | miss |

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
