# task193 design note

Which of the quarter's disproportionate reporting signals the agency's assessment desk takes forward.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task193.json`, filed and committed with this note |
| Domain, task type | pharmacology-pharmacoepidemiology-safety, `safety-signal-detection` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 16, indicators into one score |
| Decision | designation_set, the pairs taken forward |
| Gate G | `signal_vs_noise_or_hold`; decisive generators G5, G8 |
| Strategy | `population_selection`, the comparison set the measure is taken against |
| Layer 2 | `estimand_identification`, own pattern `own:comparison-set-holding-the-measure-down` |
| World | Denmark, a national medicines agency, DKK |
| As-of date | 2026-10-08, the run closed and the extract pulled |
| Guard | registered at PASS with three WARNs, answered below |

**Guard WARNs answered.** `overuse.org_family`: a national medicines agency is the only body that holds a
spontaneous reporting database, and the decision is its own; nothing else in the pack is governmental.
`overuse.objective`: the lane is Anomaly Detection and the wave is drawn inside it. `repeat.gate_g`
against task195: task195 is drawn and not built, and its Gate G mechanism is varied there rather than
here, since the mechanism this build turns on, one dominant member of a comparison set holding every
other member's measure down, is not the uncertainty of a paired difference task195 rests on.

**Data-native sentence.** Forty per cent of this quarter's reports name one product, an autumn booster
whose reports carry its own reactogenicity, so for the handful of reactions that product reports often
the database's own background rate is mostly that one product's profile, and every other product's
measure against that background is held below the threshold however carefully it is computed.

**Sources read.**
- `analytical_tasks/02_anomaly_detection/` seed AD16: the decision shape only, which alarms a scarce
  paid reviewer is given under a cap, judged on the real faults the routing escalates. Its own
  architecture turns on a channel attribute that explains every alarm on it, a field read deciding the
  call, so the build is re-rooted on the field's own disproportionality measure.
- `guard.py mechanisms --objective anomaly-detection`: the spent drivers are a detection threshold that
  moves on a cycle (task180), a count read before its records arrive (task190, task457), a selected
  extreme against the record of extremes (task191), a shared driver with unit-specific lags (task182),
  composition against rate (task183, task125, task188) and capture measured on the overlap of two lists
  (task448). None of them is a comparison set holding its own members' measures down.
- `guard.py nearest` on the driver: 0.07 against task181 v1 (lineage), where victims of two independent
  sources are pooled so the dominant source's victims make the places they also passed through look
  like sources. That build's dominance acts on an attribution, not on the denominator of every other
  candidate's measure, and its answer is a count of cards to reissue; the differentiation line is in
  the card.

## Default path

1. Read `spontaneous_reports_extract.csv` (one row per reaction coded on one report) and
   `report_master.csv`, and keep the reports the agency received in the quarter, 1 July to 30 September
   2026, on receipt date as paragraph 2.1 of the standard defines the run's window.
2. Resolve the mess the agency's own pipeline produces: collapse the cases reported through both the
   clinician channel and the marketing authorisation holder channel on the case number, map the
   verbatim reaction terms to preferred terms through `reaction_dictionary.csv` at the dictionary
   version the report was coded at, and carry the product renamed on its licence transfer onto one
   product code through `product_register.csv`.
3. Build the two by two table for every product and reaction pair: reports for the product naming the
   reaction, reports for the product not naming it, and the same two counts for every other product in
   the database.
4. Compute the proportional reporting ratio and its chi-square for every pair with at least 15 reports.
5. Take the pairs that meet the standard's criteria in paragraph 3.2: a ratio of 2.0 or more, a
   chi-square of 4 or more, 15 or more reports.
6. Check the list against the desk's capacity in `assessment_capacity_report.pdf`, see that it fits,
   and file it.

**Ends on:** 11 signals taken forward, inside the desk's capacity of 16, with five assessment slots left
over.
**Golden:** 15 signals taken forward, filling 15 of the desk's 16 slots.

## Stump sentence

A competent solver cleans the extract, builds every pair's two by two table against the whole database,
applies the standard's three criteria and files **11 signals**, five slots inside the desk's capacity;
the step that lands it there is leaving the autumn booster inside the comparison set every other
product is measured against, when that one product is 40 per cent of the quarter's reports and its own
reactogenicity sets the database's background rate for the four reactions on which the four signals it
hides sit.

## Three rules

- **Task type:** `safety-signal-detection`, the task type in Pharmacology & Safety that serves Anomaly
  Detection: separating a real disproportion in spontaneous reporting from what the database's own
  composition produces.
- **Domain test:** the deciding quantity is a disproportionality measure, the proportional reporting
  ratio of a product and reaction pair against the reporting of that reaction for other products, and
  pharmacovigilance treats masking by one dominant product as part of computing it, re-running the
  measure with that product out of the comparison set. Swap the products for warehouses and the
  reactions for delivery delays and nothing is measured against a shared background, so there is no
  comparison set to be held down and nothing to unmask.
- **Swap:** "which of the carriers' delay patterns the control desk takes forward" is a sort of each
  carrier's own delay rate; what breaks is that a carrier's rate does not sit in the denominator of
  every other carrier's rate, so one dominant carrier cannot hide another's signal, and the measure
  stops being a disproportion against a shared background.
- **Layer 1:** the agency's own pipeline produces all of it. Cases arrive through two channels and the
  same case is reported by the clinician and by the licence holder, linked by case number; reporters
  write verbatim reaction terms that a dictionary maps to preferred terms, and the July revision merged
  two terms; the run's window is on receipt date while reports also carry an earlier report date; one
  product was renamed when its licence transferred mid-quarter and the register carries both names; the
  standard and the capacity report are tables inside PDFs. None of it is placed to be caught, and the
  four masked signals cross the threshold under every handling of it, asserted.
- **Layer 2:** `estimand_identification`. The methodological choice is what the measure's comparison set
  is, which the standard leaves to the coordinator.
- **Decisive step:** re-measure with the dominant product out of the comparison set, because a
  background 40 per cent of which is one product's reactogenicity is not a background for the other
  products on the reactions that product reports often.
- **Not semantics:** every field, code, term, date and version read correctly still leaves a correct
  extract, correct preferred terms, correct pair counts and a correctly computed ratio against the
  whole database. Reading all of it right is what produces the 11, which is the wrong answer's input.
- **Not rule application:** the standard files what a signal is, the measure's name, the three criteria
  and their numbers, the run's window, the quarter's basis and the desk's order of work. No shipped
  sentence says what the ratio is taken against, nor names masking, a dominant product, a comparison
  set, a background, a stratum or a second run, and a word sweep over every shipped file asserts it. A
  solver who executes every filed sentence exactly still has to construct the measure, and the
  construction the textbook supplies files 11.
- **Analyst test:** a strong analyst who collapses the duplicate cases, maps every verbatim term at the
  right dictionary version, carries the renamed product onto one code, reads the window on receipt date
  and applies the three criteria exactly computes every pair against the whole database and files 11
  signals, the default path's `Ends on:`, where 15 meet the criteria once the booster is out of the
  comparison set.
- **Estimand:** paragraphs 3.1 and 3.2 of the standard: "A signal of disproportionate reporting is a
  product and reaction pair whose reporting in the quarter is disproportionate, measured as a
  proportional reporting ratio with the chi-square of the same table. A pair is taken forward where the
  ratio is 2.0 or more, the chi-square 4 or more, and the pair is named on 15 or more of the reports the
  agency received in the quarter." Population, outcome, window, unit, measure and thresholds are there.
  The standard names the measure the field knows and says nothing about what the comparison is taken
  against, so no shipped sentence reads to the easy answer: the whole-database comparison is the
  textbook default a solver brings, not a reading of any filed word.
- **No decoy:** nothing is planted to be caught. No reports are copied, no memo argues a list, no
  stakeholder figure carries a count, and no file states a signal list for this quarter or any other.
  The booster's own pairs are its known reactogenicity and are the ordinary content of a campaign
  quarter.
- **No certified replay:** no signal list, confirmed-signal outcome or published count ships, so no
  method can be recovered by reproducing one. The closed assessments register holds only pairs closed
  before the run's window and ties under every rung, asserted.
- **Lesson:** a disproportionality measure is a ratio against a background, so when one member of the
  comparison set dominates it the measure answers a different question for every other member, and the
  members it hides are exactly those whose excess sits on the dominant member's own profile. No build
  on file teaches it.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the ratio against the whole database with the reporter's own words taken for the reaction | the standard files the criteria and the window | the extract carries the verbatim term and the dictionary version, so the join is one line | yes, the first run anyone writes | none | the battery finds the verbatim variants and the duplicate cases | one group-by and a ratio | readable |
| 1 the same on the cleaned extract | no | no | yes, the hygiene reflex | none | yes, that is the battery | one filter | readable |
| 2 the reporting odds ratio, or the ratio the standard names pooled over the report's own attributes | no | the master file carries channel, reporter type, age band, region and sex, which is what a stratifying reflex reaches for | yes, two opponent reflexes: pooling the ratio the standard names over any of the five attributes lands on the same 11, and the odds ratio lands on 13 | none | no | no | readable |
| 3 the dominant product out of the comparison set (decisive) | no sentence names masking, a dominant product, a comparison set, a stratum or a second run, asserted by a word sweep over every shipped file | no column holds a comparison set; the booster is one product code among 24 in the same extract | no reflex removes a member from its own denominator: the three corrections at rung 2 each leave the background as it is and file the same 11 | nothing scores a method; the closed register predates the window and ties under every rung | the battery cleans the extract and leaves the background as it is | no: it is the measure recomputed with one member out of the set it is measured against | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | the quarter | reports the agency received between 1 July and 30 September 2026 inclusive, on receipt date | on the report date, or on the coding date | the pair counts change | paragraph 2.1, quoted; asserted both ways |
| SF2 | a report | one case, however many channels reported it | one submission, so a case reported twice counts twice | the pair counts change | paragraph 2.2 and the case number in `report_master.csv`; asserted |
| SF3 | a reaction | the preferred term the verbatim term maps to at the dictionary version the report was coded at | the verbatim term as written, or the current version for every report | two merged terms split or collapse | paragraph 2.3 and the dictionary's version column; asserted |
| SF4 | a product | the product code, with the renamed product under one code | the product name as reported, so the transfer splits it | one product's reports split in two | `product_register.csv`'s former name and transfer date; asserted |
| SF5 | at least 15 reports | 15 or more reports of the pair, that is the cell count | 15 or more reports for the product, or for the reaction | the candidate set changes | paragraph 3.2, quoted; asserted |
| SF6 | the ratio and its chi-square | the proportional reporting ratio and the chi-square of the same two by two table, both uncorrected | the ratio with Yates' correction | `same call` under Yates, asserted. The reporting odds ratio is a different measure, ruled out by paragraph 3.1 naming the one the run takes; it is rung 2, and on this database it finds two of the four the booster hides and not the other two, asserted |
| SF7 | 2.0 or more | at or above 2.0 | strictly above | `same call`, asserted: no pair's ratio is 2.00 on either basis |
| SF8 | a signal already closed | a pair the agency closed before the window, which the register holds and the run does not re-raise | any pair the register names | `same call`, asserted: no pair the register names meets the criteria on either basis |
| SF9 | the desk's capacity | the 16 assessments the capacity report gives for the coming quarter | the assessor days, or the current quarter's capacity | `same call`: 15 fit under both readings, asserted |
| SF10 | serious | the reactions the dictionary marks as serious | the reporter's own seriousness flag | `same call` on the main call, which reads neither; the ask that reads it is pinned in its own sentence |
| SF11 | rounding | ratios to two decimals, chi-square to one, counts whole | ratios to one decimal | `same call`, asserted: no pair crosses 2.0 under either rounding |
| SF12 | ties in the order of work | none: the desk takes all 15 and the capacity is 16 | a tie-break would be needed if capacity bound | `same call`, asserted: the capacity does not bind |
| SF13 | "disproportionate", paragraph 3.1 | the pair's own ratio and chi-square against the thresholds in 3.2, which is what 3.2 states | disproportionate against the product's other reactions, or against the reaction's other products as a rank | the candidate set changes | paragraph 3.2, which gives the measure and all three numbers; asserted that no other reading of 3.1 leaves 3.2 satisfiable. What the comparison is taken against is nowhere stated and is the method, not a term: `## Literal reader` gives the forcing |
| SF14 | missing age or region | left as reported, which the main call never reads | imputed | `same call` on the main call; the ask that reads them is pinned |

## Ladder

| Rung | The analysis | The signals |
|---|---|---|
| 0 | the ratio against the whole database with the reporter's own words taken for the reaction, the rest done right | **19**, which overruns the desk's 16 slots |
| 1 | the same on the cleaned extract | **11** |
| 2 | the reporting odds ratio against the whole database, the measure a careful analyst reaches for when the reaction is common, or the same odds ratio pooled over the report's own attributes | **13**: it finds two of the four the booster hides, Keltaprin on headache and Serovane on fatigue, and neither Noralvex on pyrexia nor Ravistan on myalgia |
| 3 | **answer:** the measure recomputed with the booster out of the comparison set | **15** |

**Separation.** The sets differ in membership, which is how the shape grades: rung 1's 11 is a strict
subset of the answer's 15, so the easy route misses four named pairs and leaves five of the desk's 16
slots idle; rung 0's 19 goes the other way, splitting a reaction across the words reporters wrote for
it and taking forward eight pairs the dictionary does not support, which overruns the desk's capacity
and makes the coordinator carry three. The four pairs the answer adds sit at a crude ratio of 1.39 to 1.55, clearly short of
2.0, and at 2.70 to 3.09 once the booster is out, clearly past it; the lowest of the 11 is 2.44 crude
and 2.36 corrected, so every one of them stays past 2.0 on both bases, no pair is lost and the union
question does not arise. The nearest figure to the threshold on either basis is 0.36 away.

**The grid.** Two axes, the cleaning and the comparison set:

| | whole database | booster out of the comparison set |
|---|---|---|
| the reporter's own words taken for the reaction | 19 | 30 |
| cleaned extract | 11 | **15** |

Every cell is a named count. The decisive axis is the only one that adds the four masked pairs, and it
adds them in both rows, so a solver who finds the masking but not the duplicate cases still names them:
that is the fairness the ladder needs, and the cleaning is worth the ask criteria rather than the call.

**Dominance.** The pair the ladder turns on is the one on the reaction the booster reports most often:
its crude ratio is the lowest of the four and its corrected ratio the highest, so no partial correction
reaches it. Removing any other product from the comparison set moves no pair across the threshold,
asserted over all 24.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which reports are in the run | paragraph 2.1 files the window on receipt date; asserted |
| 2 | Unit of account | the report, the submission, the pair | paragraph 2.2 files the case as the report; asserted |
| 3 | Attribution window | which quarter a report falls in | receipt date, paragraph 2.1; no report received within a day of either boundary, asserted |
| 4 | As-of dating | the extract at 8 October | the manifest files the pull; the window closed eight days before, asserted |
| 5 | Version basis | the dictionary revision and the renamed product | the version column and the register's transfer date; C1, asserted |
| 6 | Denominator | what the ratio is taken against | **the decisive step. No shipped sentence states it, asserted by word sweep; forced by the data, and every masking-aware comparison set asserted to give the same 15; see `## Literal reader`** |
| 7 | Weighting | none: pairs are counted, not weighted | stated |
| 8 | Window length | one quarter | paragraph 2.1; asserted that every signal's pair count is reached inside it |
| 9 | Boundary inclusivity | 1 July and 30 September | paragraph 2.1 states both inclusive; no report on either day, asserted |
| 10 | Rounding path | ratios to two decimals, chi-square to one | the asking sentence; no pair within 0.08 of 2.0 on either basis, asserted |
| 11 | Tie-break | the order the desk works in | paragraph 4.2 files it; the capacity does not bind, asserted |
| 12 | Maturity and censoring | reports still arriving for the quarter | the manifest's own completion note; the window closed before the pull, asserted |
| 13 | Order of operations | clean then measure, or measure then clean | C1 is false here and that is the point: rung 0 and rung 1 differ, and both are below the answer on either comparison set, asserted in the grid |
| 14 | Row order | the extract's order | C1, asserted over three permutations |
| 15 | Duplicate resolution | the two channels' submissions of one case | C1: both submissions carry the case number and the same coded reactions, so any resolution keeps one case, asserted |
| 16 | Identity normalisation | product names, verbatim terms, licence holders | the register and the dictionary; asserted that every name resolves to one code |
| 17 | Netting against gross | nothing is netted | stated |
| 18 | Dimensional units | counts of reports, of submissions and of coded reactions | the dictionary names each; the call reads reports, asserted |
| 19 | Code and status semantics | the channel, reporter and seriousness codes | the data dictionary; never the decisive step |
| 20 | Integerisation | the count of signals is an integer by construction | stated |
| 21 | Clause scope | paragraph 3.2 per pair | the paragraph states it; asserted |
| 22 | Forward window contents | the assessments the desk will run next quarter | the call is the list the desk takes forward into the coming quarter, so it is forward facing: the pairs are designated now and worked after the run closes |

## Literal reader

Executing the prompt, the standard's paragraphs 2.1 to 2.3, 3.1, 3.2 and 4.2, the dictionary and the
register word for word selects the cases the agency received between 1 July and 30 September 2026, one
case per report, each reaction at the preferred term of its coding version, each product at one code,
and asks for the pairs named on 15 or more of those reports whose proportional reporting ratio is 2.0
or more with a chi-square of 4 or more. Every term and convention in that sentence has an SF row ruled
out by a quoted sentence or asserted to give the same list. What the text does not fix, and nowhere
mentions, is what the ratio is taken against: that is the measure's own construction. No shipped
sentence says "other products", "the database as a whole", "the comparison set" or anything a literal
reader could execute into the crude run, asserted by a word sweep over every shipped file, so the easy
answer is the textbook default a solver brings rather than a reading of a filed word.

The data forces it. One product holds 40.2 per cent of the quarter's reports, and on the four reactions
whose signals it hides it holds between 61.6 and 68.6 per cent of every report naming them, rising to
86.8 per cent on injection site pain, so the expectation those reactions carry is that one product's
reactogenicity rather than the database's background.
Every comparison set that answers the standard's question gives the same 15: the booster out, the two
largest products out, the three largest out, and every product holding more than a tenth of the
quarter's reports out, all four asserted on the figure and on the membership. Removing any single other
product moves no pair across, asserted over all 24. The crude run's 11 is a strict subset of the 15, so
no licensed reading drops a pair, and the easy answer is an easy method on the same literal estimand
rather than another reading of it.

## Oracles

- `closed_assessments_register.csv` records the pairs the desk assessed and closed in the twelve months
  before the window, with the date each closed. It names no pair that meets the criteria on either
  basis and states no outcome for any pair in this quarter, so it ties under every rung, asserted.
- `assessment_capacity_report.pdf` gives the desk's 16 assessments and its assessor days. The capacity
  does not bind on either basis, so it confirms nothing about the method, asserted.
- `campaign_vaccination_log.csv` gives doses by week and region. It confirms the campaign's size, which
  the extract already shows, and ties under every rung.
- `extract_manifest.csv` states each file's rows and range and settles the ask layer's one designed
  disagreement without naming a level.
- No file states a signal list, a confirmed-signal outcome, a ratio or a count of signals for any
  quarter. There is no calibration organ.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per channel and month, the cases received, those the agency could not code and the median days from receipt to coding | 3 per channel-month | the audit trail from an input the call consumes, through rows it never reads, to the channel's own control total | the pipeline review the agency runs each quarter | D4 absence as the signal: the cases that failed coding sit in `coding_exceptions.csv`, which no habitual join reaches, and never enter the extract | D6 the exceptions file is per submission, the channel totals per day; D8 the submission clock is the holder's, not the agency's | exceptions file, channel totals, report master, submissions, dictionary, standard, manifest, register; 12 columns | 4 stops, lazy delta 5 of 6 channel-months | an ingest pipeline's own quarterly review |
| A2 per licence holder, the submissions it filed, those filed after the quarter closed and the fee due under its data agreement | 3 per holder | an input reconciled to another system's total, the gap made of devices | the finance office settles the holders' agreements | D2 version: one holder's agreement was amended inside the quarter and the fee is at the amended rate, which the superseded schedule does not carry | D3 a fee per submission against a fee per month; D7 one holder files under two codes after a merger | submissions, agreement schedule, the amendment, channel totals, register, manifest; 13 columns | 5 stops, lazy delta 3 of 8 holders | the finance office's quarterly settlement |
| A3 per region and age group, the cases received and the share naming a reaction the dictionary marks serious | 2 per cell | the construction's own output on the segment the desk wants anyway | the bulletin's standing table | the construction layer: a wrong case unit, an unmapped verbatim term or the wrong dictionary version fails every cell | D4 blanks that mean the reporter did not state an age; D8 the dictionary revision inside the quarter | report master, extract, dictionary, standard, manifest; 11 columns | 4 stops, lazy delta 7 of 12 cells | the agency's own quarterly table |

**The main population's zero counts.** Zero device rows and zero hazard rows in the reports and pairs
the call rests on: the devices sit in the exceptions file, the submission register, the agreement
schedule and its amendment, none of which carries a coded reaction. Deleting every device leaves the
15 and the 11 exactly as they are, asserted.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D6 grain | A1, A2 | A1 one channel-month, A2 two holders |
| D8 clocks | A1, A3 | A1 one channel's median, A3 one cell's share |
| D4 absence | A1, A3 | A1 the uncodeable count in every month, A3 two cells |

**The referee.** `extract_manifest.csv` states each file's rows and date range and settles the one
designed disagreement, the exceptions file's extent, without naming a level.

**The cracker sheet.** The cracker filed the 15, ran the hygiene battery, executed every filed
paragraph and matched every control.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 cases the agency could not code, holder channel | the extract and the master, which hold only coded cases | 0 | to be measured at build | miss |
| A1 median days to coding, clinician channel | the submission stamp | too low | to be measured at build | miss |
| A2 fee due, the amended holder | the superseded schedule's rate | too low | to be measured at build | miss |
| A2 submissions filed, the merged holder | one holder code | too low | to be measured at build | miss |
| A3 share naming a serious reaction, the two merged terms' cells | the current dictionary version for every report | too high | to be measured at build | miss |

**Pair ceiling:** 39.0
**Mirror leakage:** 19.5

## Tried and rejected

- The seed's own architecture, a channel attribute that explains every alarm on the channel: the answer
  flips on reading one field, which the client's rules ban as the decisive step. Re-rooted at the draw.
- Masking confined to one reaction, with one dominant product flooding a single preferred term: the
  decisive step would move one pair, which no ladder can carry, and a solver who missed it would be
  wrong by one. Replaced by a campaign quarter, where the dominant product's whole profile sets the
  background for four reactions at once.
- Forcing the comparison set with a filed criterion in general terms, that the measure must not move
  when reporting for unrelated products moves: it makes the solver ask the decisive question, which the
  readability screen fails on test 1. Replaced by forcing through the data, with every masking-aware
  comparison set asserted to give the same 15.
- A register of the previous quarters' confirmed signals, to force the comparison set by showing which
  run caught them: a corpus that refutes the naive read makes the decisive rung readable, and it is a
  calibration organ the card does not carry. Dropped; the closed register ships with pairs that predate
  the window and ties under every rung.
- Letting the desk's capacity bind, so the call is the top 15 of 16 qualifying pairs by report count:
  the cap adds a filed ordering rule on top of the decisive step and puts two pairs on a boundary the
  judge would have to adjudicate. The capacity is left at 16 against 15 taken, which is what makes the
  easy answer's five idle slots a visible consequence.


## Leak sweep answered

`leak.py --asof 2026-10-08` is REVIEW with thirteen lines and no LEAK. Each one, and why it is
harmless:

- **Sweep 3, the figure 119 in `assessment_capacity_report.pdf`.** The desk's assessor days for the
  quarter now closing. It coincides with no graded figure: the answer's figures are counts of pairs,
  ratios and chi-squares, and 119 is days of staff time.
- **Sweep 3, the strings 3.2 and 4.1 in `signal_standard.pdf`.** Its own paragraph numbers, which the
  write-up cites. A standard without numbered paragraphs could not be cited at all.
- **Sweep 3, seven of ten words of the committed call in the capacity report.** The call is stated in
  the desk's own vocabulary (assessment desk, capacity, slots, quarter), which is the vocabulary the
  capacity report is written in. The report states no count of pairs and no measure of any pair's
  reporting, and says so in its own note.
- **Sweep 4, stump-paragraph terms in the standard and the capacity report** (measure, extract,
  report, reporting, register, criteria). They are the words a signal detection standard is made of.
  Neither document says what the measure is taken against, which is the decisive step, and a word
  sweep over every shipped file asserts that nothing does.
- **Sweep 6, `coding_exceptions.csv` and `data_agreement_schedule.xlsx` naming ten of eleven
  candidates beside numbers.** The names the sweep matched are licence holders, not product and
  reaction pairs. The schedule ranks holders by a fee per submission and the exceptions file counts
  submissions that failed coding; neither carries a coded reaction, asserted by column name, and
  neither ranks a pair on the question.
- **Sweep 10, the container line.** Every PDF and workbook is normalised to an in-fiction author and
  stamp, and the two rebuilds are byte-identical.

## Pre-ship check

The pack as built, read against the gates one last time.

- **Free gates.** 628 generator assertions, 182 independent checks in `verify.py` (it reads only
  `target/` and `figures.json`), `precut.py` 49 checks 0 FAIL 0 WARN, `figures_check.py` 214 of 214,
  `voice-check.py` exit 0 at 986 characters, `leak.py` REVIEW with thirteen answered lines and no
  LEAK, `guard.py heart` WARN with every line answered above, `guard.py surface` promoting three
  pairs on card signature alone, each answered in the card's `differentiation`. Two rebuilds
  byte-identical (pack md5 512455a3ec9082d171b33960dc64868b), `target.zip` cut from the final
  rebuild, 16 entries, md5 74068ce195de8b46234157d9d380ea48.
- **Input gates.** 16 files, 4 formats (csv, pdf, xlsx, json), one file of 25,660 rows
  (`spontaneous_reports_extract.csv`, with `report_master.csv` at 10,082 and
  `holder_submissions.csv` at 4,445), three distractors named in `metadata.json`, none named in a
  file name.
- **The three rules against the built pack.** The decisive step is still the analytical one: no
  shipped sentence says what the ratio is taken against, and a word sweep over all sixteen files
  asserts that none of nineteen phrasings of it appears. The forcing is the data's: one product holds
  40.2 per cent of the quarter's reports and 61.6 to 86.8 per cent of every report naming the six
  reactions its own reactogenicity produces, and every masking-aware comparison set (the largest
  product out, the two largest, the three largest, every product over a tenth or a twentieth of the
  quarter) gives the same 15, while leaving out any single other product moves no pair across. The
  mess stays in Layer 1: the four masked pairs cross the threshold under every mishandling of the
  duplicate cases, the window basis and the renamed product, asserted. Nothing is planted: the
  booster's own six pairs are its known reactogenicity and paragraph 3.3 keeps every pair the product
  information describes out of the run on both bases alike.
- **Gate G.** No shipped artifact ranks the pairs on the decision question, and `metadata.json`
  declares no wrong-basis distractor. The capacity report says in its own note that capacity "carries
  no measure of how strong a pair's reporting is"; the closed assessments register names no pair that
  meets the criteria on either basis and every row in it closed before the window. Delete every wrong
  number in the pack and the call still turns on what the ratio is taken against.

## Architecture 1, spent at stage 4 on the judge's SEND_BACK

**The verdict.** NOT_DETERMINISTIC, `underspecified_objective`, disposition SEND_BACK. Gate G passes
(`method_or_model_selection`, `analytical_non_defect`, no surface-read dependency, no sole data
defect) and Gate H passes on all three rules, with the decisive step read as analytical: the choice
of comparison group under masking. Every golden figure reproduced from the shipped files, the 15
pairs with their ratios and chi-squares among them. The call is what failed: paragraph 3.1 names the
measure and no shipped text says what it is taken against, so the proportional reporting ratio
against all other reports, which is the textbook default, gives 11 and the golden's 15 appears only
when the booster is out of the comparison. The leak reader, reading the same pack cold, landed the
same 11 at moderate to high confidence and named the comparator as the one choice the documents left
to it.

**Why this is structural and not a missing sentence.** The judge's own fix is to file the comparison
population in the standard, and that is right: `determinism-check` section 1 counts the comparison
inside the estimand, the WHAT, which must be filed so that its literal execution is the golden. This
build put the decisive step in the comparison population, so it put the stump in the WHAT. File it
either way and the computation follows from the clause, which is rule application; leave it unfiled
and the call is not determinate. There is no third position, and no hardening reaches one: a general
criterion on the measure ("the expectation must not turn on the volume of any one product") makes the
exclusion an executed rule, and a record of past runs that shows which comparator caught the
confirmed signals is a corpus that refutes the naive read, which the readability screen fails on
test 4.

**The lesson, which is wider than this build.** Three architectures in this wave have now died the
same death: task190's population had to say whether members not yet observed are in it, task192's
decisive count had no parameter-free definition, and this one's comparison population is part of the
estimand. In each the decisive step sat in the WHAT. The next draw puts the estimand wholly beyond
argument, every term and population filed, and leaves two or more methods standing on it, with the
data's own structure ruling out the easy one. `method_or_model_selection` on a filed estimand, not
`estimand_identification`.

**Worth keeping from the build.** The world and the ask layer are sound and the pack is realistic
enough to reuse under another decisive step. Three defects the judge and the reader found in it are
recorded so a re-root does not repeat them:
- `dictionary_version` in the extract was set from the receipt date while paragraph 2.3 reads the
  version in force when the case was coded, so 1,388 rows disagree and the serious share forks.
- 501 licence-holder submissions carry a coded date one to four days before the receipt date, so the
  mean days to coding forks three ways (raw, clipped at zero, negatives dropped).
- The agreement schedule does not say whether the quarter's fee covers submissions received after
  the quarter closed, so the holder fees fork by about 7,300 kroner.
