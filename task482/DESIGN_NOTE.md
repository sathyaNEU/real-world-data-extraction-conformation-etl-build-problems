# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-21.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v1), registered 2026-10-21 after a pull.
  Guard WARN only, answered here: `overuse.org_family` (a state board is a government agency), `overuse.objective`
  (the lane), `repeat.question_form` (a capped slate is asked as "which"). Redrawn at the draw: calibration form,
  context artifact and strategy (bans against task479 and task272), then gap population with G2 (same driver as
  task486) to G5, Gate G `etl_conformance`, strategy `composition_mix`, artifact `published_series`. People from
  `guard.py names --geo us --seed 482`: Jeremy Cortez and John Huang.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: the federal finance and 12-month enrollment returns of a state's public four-year campuses conformed with
  the state's credit hour file, the consolidated returns of four parent campuses apportioned to the campuses inside
  them.
- **The decision and the quantity:** the coordinating board's 2027-28 instructional investment grant goes to the five
  reporting units with the lowest fiscal 2026 instruction expense per FTE student. Retrospective by statute: the grant
  formula reads the latest closed fiscal year, so the window is fiscal 2026 (July 2025 to June 2026), and nothing is
  forecast.
- **Data-native sentence:** six branch campuses report enrollment and credit hours of their own but have their
  finances inside their parents' returns, and they teach mostly freshman and sophomore credit hours, which the sixteen
  campuses that report alone show cost about a third of a graduate hour.
- **Strategy:** `composition_mix`; Gate G `etl_conformance`; gap `population`; generators G5, G2. Layer 2 family
  `estimation_fit`, pattern `own:a combined return split among the units inside it by a cost model fitted on the units
  that report alone, not by their head counts`.

## Default path

A strong analyst with every field read correctly:

1. Reads the guidelines: the five reporting units with the lowest fiscal 2026 instruction expense per 12-month FTE
   student; a branch whose finance sits in its parent's return is ranked on its own instruction expense, which the
   parent's return includes, and the parent on its own.
2. Joins the finance return (F1C011, PRCH_F, IDX_F) to the 12-month return (FTEUG plus FTEGD), sees the six branches
   at PRCH_F 2 and zero, and splits each parent's instruction among the parent and its branches by their FTE students
   (the credit hour split, or leaving the branches out, gives the same five).
3. Ranks the twenty-six campuses and takes the five lowest.

**Ends on:** 214506, 214682, 214858, 214946 and 215298 awarded

On that path the branches carry their systems' averages, $11,062 to $11,511 per FTE at Ferris Bend, Stoneleigh and
Dunmere, and the five are standalone campuses at $8,020 to $9,575.

**Golden:** 214682, 214946, 216190, 216278 and 216454 awarded; with each parent's instruction split by the fitted cost
of the credit hours each campus taught ($208.6, $429.9 and $749.6 a lower-division, upper-division and graduate hour,
fitted on the sixteen campuses that report alone), Ferris Bend, Stoneleigh and Dunmere stand at $7,558, $7,754 and
$7,829, under every standalone campus but Inglenook.

## Stump sentence

The default path splits each parent's instruction expense among the parent and its branches by FTE students and files 214506, 214682, 214858, 214946 and 215298 awarded, because it never asks whether a branch that teaches mostly lower-division credit hours costs what its system costs per student on average: the campuses that report alone show a lower-division credit hour costing under a third of a graduate hour, and three branches priced at the hours they teach have the lowest instruction expense per FTE in the state.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics): the federal directory, finance and 12-month enrollment returns conformed with the board's campus codes and credit hour file, and the four parents' consolidated finance returns apportioned to the campuses inside them, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each branch campus's own fiscal 2026 instruction expense, an item recorded only inside a consolidated return, worked the way an official-statistics register apportions a combined report to its units: by a model of the item on auxiliary variables recorded for every unit (credit hours by level), fitted on the units that report the item alone, the combined total kept.

Swap: "which five stores have the lowest payroll per customer, where a regional office reports its stores' payroll in one line" keeps a combined return and loses the step's ground: no recorded activity whose unit cost differs several-fold across kinds, measured on the units that report alone, and no administrative return whose consolidation a register must apportion.

Layer 1: the branches' finance reported within their parents' returns (PRCH_F 2, zero instruction), the board's campus codes against federal UNITIDs, the credit hour file by term and level against the 12-month return's annual hours, a fiscal year against an academic year of three terms, cross-listed courses carried under each course number and student ids reissued at the branches' August 2026 move to their parents' student systems (the asks); each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the call under them (SF5 to SF7).

Layer 2: estimation_fit, the model a consolidated return is apportioned by: the choice that flips the call is splitting each parent's instruction by the cost of the credit hours each campus teaches, the cost per hour by level fitted on the campuses that report alone, instead of by head count.

Decisive step: apportioning each parent's reported instruction expense among the parent and its branches in proportion to their credit hours by level priced at the fitted cost per credit hour (lower-division $208.6, upper-division $429.9, graduate $749.6), which puts Ferris Bend, Stoneleigh and Dunmere under every standalone campus but Inglenook.

Not semantics: every field, code and definition read correctly (PRCH_F and IDX_F, the zero returns, FTEUG and FTEGD, the campus codes, the terms) still leaves the easy route splitting each parent's instruction by FTE, because no field gives a branch's own instruction expense or says how to split a parent's; the step is the inference that instruction cost follows the level of the hours taught, which the campuses that report alone show and no sentence says.

Not rule application: the guidelines fix the population, the outcome (each campus's own instruction expense, inside its parent's return for a branch), the window, the unit and the comparison, and no rule says how a parent's return is split; executing every filed rule with an FTE split files 214506, 214682, 214858, 214946 and 215298 awarded.

Analyst test: a strong analyst who conforms every file and reads every rule, splitting each parent's instruction by FTE students, files 214506, 214682, 214858, 214946 and 215298 awarded (the default path's Ends on); one who splits by total credit hours or leaves the branches out files the same; one who prices undergraduate and graduate hours only files 214506, 214682, 214946, 216190 and 216278; only pricing each campus's lower-division, upper-division and graduate hours files the golden five; checks.py runs them on the clean truth (R3a, R3b).

Estimand: the grant guidelines (lhecb_instructional_investment_grant_guidelines_2027-28.pdf, sections 1 and 2): the population (the twenty-six public four-year reporting units), the outcome (each campus's own fiscal 2026 instruction expense, a branch's the part of its parent's return its own instruction incurred), the window (fiscal 2026, July 2025 to June 2026), the unit (per 2025-26 12-month FTE student, undergraduate plus graduate) and the comparison (the five lowest).

No decoy: nothing is planted: the federal returns, codes, credit hours and census rows are the producing systems' records, the guidelines state the basis without a method, and no earlier award, cost study or published figure ranks the campuses on fiscal 2026; the appropriations, tuition and graduation rates are distractors that rank nothing on instruction expense.

No certified replay: no certified or published cost per credit hour, allocation factor or branch expense ships; the method is not recovered by reproducing any figure.

Lesson: a total reported for several units together is apportioned by what drives it, measured where it is reported alone, and instruction expense follows the level of the credit hours taught; no build on file splits a consolidated return by a cost model fitted on the units that report alone.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 the branches at their returns' zero | the finance return | readable |
| Layer 1: PRCH_F and IDX_F, campus codes, terms | the dictionary and the code list | readable |
| R1 (default path) each parent's return split by FTE | the guidelines' "which its parent's return includes" and the 12-month return | readable |
| R2 split by undergraduate and graduate hours priced on the standalone campuses | the 12-month return's two credit hour columns | readable |
| R3 (decisive) split by lower-division, upper-division and graduate hours priced on the standalone campuses | nothing: no sentence names a cost per credit hour, a level weight or an allocation by cost; the credit hour file is listed in the manifest as credit hours by level | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a branch's instruction expense | its own, inside its parent's return | the zero on its own return | not filed alternatives | guidelines section 2 |
| SF2 | the parent's instruction expense | its own, without its branches' | the whole return | not filed alternatives | guidelines section 2 |
| SF3 | FTE | the 12-month return's FTEUG plus FTEGD | fall FTE | not filed alternatives | guidelines section 2 |
| SF4 | the fiscal year | July 2025 to June 2026 | the academic year | same call (one return) | guidelines section 2 |
| SF5 | credit hours | the board's file by level | the 12-month return's two columns | the file ties to the return (asserted) | SF5 in checks.py |
| SF6 | the zero returns | PRCH_F 2 rows carry no instruction of their own | a missing return | same call | the dictionary's PRCH_F |
| SF7 | campus codes | one code per UNITID | another mapping | same call (asserted) | the code list |
| SF8 | the split | the parent's reported total kept | fitted costs used directly | not filed alternatives (direct files another five) | guidelines section 2, "No campus's fiscal 2026 return is restated for the grant" |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L3, C2 to C4), instruction expense per FTE, dollars.

| Rung | Route | Awarded | 216190, 216278, 216454 / 214506, 214858, 215298 |
|---|---|---|---|
| R0 | the branches at zero | the five branches 216190, 216278, 216454, 216630, 216718 | 0, 0, 0 / 8,838, 9,575, 9,042 |
| R1 (default path) | split by FTE | 214506, 214682, 214858, 214946, 215298 | 11,511, 11,511, 11,062 / 8,838, 9,575, 9,042 |
| R2 | split by undergraduate and graduate hours priced | 214506, 214682, 214946, 216190, 216278 | 8,796, 8,797, 9,052 / 8,838, 9,575, 9,042 |
| Golden | split by hours by level priced | 214682, 214946, 216190, 216278, 216454 | 7,558, 7,754, 7,829 / 8,838, 9,575, 9,042 |

- Dominance: under the golden and its least-squares forms (FTE weights, three terms) the sixth stands 3 per cent or
  more over the fifth, with an intercept 2 per cent (C2, C2b); the fitted costs sit within 4 per cent of the truth (C3)
  and every campus's estimate within 4 per cent of its own expense (C4).
- The data separates the readings: across the sixteen standalone campuses instruction expense is fitted by the three
  levels' credit hours at $208.6, $429.9 and $749.6, so a lower-division hour costs under half an upper-division hour
  and the two-level model, which prices every undergraduate hour alike at $294.3, overcharges the branches.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the twenty-six reporting units | filed (guidelines 1) |
| 2 | Unit of account | per 12-month FTE student | filed (SF3) |
| 3 | Attribution window | fiscal 2026 | filed (SF4) |
| 4 | As-of dating | the board's collection of 1 October 2026 | manifest |
| 5 | Version basis | one return per campus | SF6 |
| 6 | Denominator | FTEUG plus FTEGD | filed (SF3) |
| 7 | Weighting | none | L1 forms |
| 8 | Window length | one fiscal year | filed |
| 9 | Boundary inclusivity | the five lowest | C2 |
| 10 | Rounding path | unrounded ranks | prompt |
| 11 | Tie-break | none (3 per cent gap) | C2 |
| 12 | Maturity and censoring | closed fiscal year | filed |
| 13 | Order of operations | conform, fit, split, divide, rank | commutes |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | none on the call's files | SF7 |
| 16 | Identity normalisation | campus codes to UNITID | SF7 |
| 17 | Netting against gross | instruction total expense | filed |
| 18 | Dimensional units | dollars and credit hours | the dictionary |
| 19 | Code and status semantics | PRCH_F 1, 2, blank | the dictionary; never the stump |
| 20 | Integerisation | none | commutes |
| 21 | Clause scope | every reporting unit | filed |
| 22 | Forward window contents | none (retrospective by statute) | filed |

## Literal reader

The guidelines executed word for word rank each campus on its own fiscal 2026 instruction expense, a branch's being the
part of its parent's return that the branch itself incurred; the literal question is how much of each parent's
instruction each of its campuses' teaching cost, which the campuses reporting alone answer through the cost of an hour
at each level. A literal reader who splits by FTE has assumed every campus in a system costs its average per student,
which the standalone campuses' costs by level contradict; every other reading converges or violates a quoted sentence
(fork table). Re-run on the finished pack.

## Oracles

- No shipped file carries a branch's instruction expense, an allocation factor, a cost per credit hour or a ranking of
  the campuses on fiscal 2026 instruction per FTE.
- The appropriations, tuition and graduation rates are distractors (metadata.json); none ranks the campuses on
  instruction expense.
- No control ties only under the golden on the asks.

## Ask sheet

- **Ask A, each branch campus's fall 2026 FTE students (six figures, one decimal).** H18 home: the base of the branches'
  first own returns (guidelines section 3). Path: the fall 2026 census file (student, course, CRN, level, credit hours,
  meeting, instructor), the code list. Primary device: D1, the same records under two keys: a cross-listed course
  carries each of its students under both course numbers and CRNs at one meeting with one instructor, so summing rows
  counts those hours twice. Hazards: graduate hours over 12.
- **Ask B, each branch campus's unduplicated fall 2026 headcount (six figures, whole numbers).** H18 home: as ask A.
  Path: the same file. Primary device: D7, codes reissued: each branch moved to its parent's student system in August
  2026; a student's courses registered in the spring stayed under the old id and the courses added after the move sit
  under the new one, with the same six-digit form and no arithmetic tie; the new systems also carry four majors under
  their 2020 programme codes. Only birth date, sex, home ZIP code and first term within the campus tie the two ids:
  birth date, sex and ZIP alone are shared by different students, and the major differs on the movers' new rows.
- **The construction layer:** the call, the twenty-six decisions and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the finance, the 12-month return, the codes and the credit
  hour file; the fall census file is read by the asks only (X1).
- **Hazard table (asserted):** A1, A2, B1, B2 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, branches' fall FTE | one row per course number, no exact duplicate to drop; keeps 0 of 6 | miss |
| B, branches' headcount | one person per student id; keeps 0 of 6 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 12).
- Pair ceiling: 36.8 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the five and keeps 20 of 26 decisions, 28.5). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

READERS_LINE

JUDGE_LINE

## Tried and rejected
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
