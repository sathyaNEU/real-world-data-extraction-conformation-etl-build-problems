# task251 design note

## Draw

Card `cards/task251.json` (architecture 3, re-rooted 2026-10-20 from architecture 2, spent at stage 4; see Tried and
rejected and the card's lineage). Guard verdict WARN, no BLOCK. The WARNs, answered: repeat.decision (designation_set
after task478: the decision is the set of meters the visit takes, and a set is what the manufacturer's engineer needs; a
count or a gate would hide which meters, and the scoring unit is the meter, not task478's road segment);
repeat.deliverables (png and xlsx after task481: the list goes to the manufacturer as a workbook and the quality office
reads the chart; no other format family fits the decision); repeat.question_form (which, after task480 and task478: a
pick asks which, and the question is a pick of meters). The structural notes are differentiated on the card against
task229, task231, task236, task245, task265 and the slot's two earlier architectures. `guard.py slots` on the candidate
driver: the four slot notes it returns (task202, task253, task190, task260) share words, not the move. The draw waited
for the window: task471 and then task271 held population_selection and task271 the hospital family until later
registrations pushed them out, and the analyzer parallel run was folded into the laboratory's note when task481 took
parallel_run_overlap (Tried and rejected). At filing task478 held operations_desk, purchase_order_or_contract and
monitoring_export, and the three were redrawn to the honester labels below; its re-filing took field_unit_lead, and the
role was redrawn with it.

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error, drawn for Data Quality
  Monitoring & Alerting. The object is the health of the trust's bedside glucose results, which reach the clinical record
  from 52 meters, and the call is a monitoring decision: which meters the point-of-care office withdraws for the
  manufacturer's recalibration.
- **The seed, re-found.** DQ24 gave the world (instruments checked against a reference, both noisy), the decision (which
  instruments go for recalibration) and the quantity (each instrument's factor against a tolerance). Its pitfall, the
  attenuated slope between two noisy instruments, is spent (task249 v1); this number's first two architectures spent a
  reference chain and a wear clock. The decisive step is re-found in the data's own structure: most of a neonatal
  meter's pairings with the laboratory exist because the meter's own reading was critical.
- **Niche.** The ASST Pianura Orientale (fictional, the Po valley) runs 52 Glyvera GX2 meters on thirteen wards of the
  Castelmarne, Rivobello and Valdarena hospitals. The meters' data manager, GlyLink, pairs a meter result with the central
  laboratory's result whenever the nurse reads a tube's barcode on the meter: on the morning round on the days the
  point-of-care office's plan gives each meter, and whenever a reading under 50 or over 400 mg/dL is confirmed in the
  laboratory. The manufacturer recalibrated every meter in January 2027 and returns from 17 to 21 January 2028 under the
  service contract; the procedure withdraws a meter whose systematic error against the laboratory is beyond 5 per cent.
- **The call.** Which meters go on the list for the January 2028 visit, or none.
- **Shape.** other: the list (each of the eight meters and no other: 9), each listed meter's ward, hospital and error
  (8), the chart of every meter's error against the band with the list marked (4), the share of 2027 results reaching the
  record late per hospital and quarter (12), the 2027 patient tests per ward (13), the two files (2): 48 criteria.
- **Strategy.** `population_selection` (strategies F7: checks that see a unit because it was wrong). Gate G
  signal_vs_noise_or_hold (a confirmation pairing's apparent bias is the meter's selected random error); generators G9,
  G5, G11; gap population; calibration none (the analyzer change rides on the note's filed factor); context artifact
  register (the meter register with its location history); Layer 2 field_method, pattern own:confirmation-pairs-selected-on-the-meter-reading.
- **Forum, event, organisation.** customer_or_counterparty (the manufacturer receives the list: its service manager's
  mail asks for it by Monday 10 January, and the visit, not the office, acts on it), other for the event (the
  manufacturer's scheduled recalibration visit of 17 to 21 January 2028, a service visit with no order, renewal or tender
  at stake, which purchase_order_or_contract overstated), hospital_or_health_provider. Role compliance_or_audit (the
  coordinator answers for the meters' analytical quality under POCT-GLU-02; field_unit_lead, drawn first, went to task478
  at its re-filing and named a site unit the office is not). Context artifact register: anagrafica_glucometri.xlsx answers where each meter stands, where it stood
  and when it was last calibrated, correctly, and ranks nothing; the data manager's export is the spine.
- **People** (`guard.py names --geo Italy --seed 251`, locale it_IT): Lorenzo Carfagna, the point-of-care office's
  coordinator, who asks; Silvestro Fittipaldi, the laboratory's director, who signs the analyzer note; Adelmo Gori, the
  manufacturer's service manager. None appears in the prompt.
- **Data-native sentence.** A pairing sits in GlyLink's report either because the plan drew the meter on the morning
  round, whatever it read, or because the meter's own reading was under 50 or over 400 mg/dL and the nurse sent a
  confirmation; the second kind sees the meter when its random error ran outward, and on the nursery and the neonatal
  intensive care it is about two pairings in three (62 and 67 in a hundred).
- **As-of.** Tuesday 4 January 2028 (the manufacturer's mail); the list is due Monday 10 January, the visit runs 17 to 21
  January. The call faces forward: which meters' error the 2028 recalibration has to correct.
- **Sources.** The client's two-layer standard; meter-laboratory comparison practice for bedside glucose (CLSI POCT12,
  ISO 15197); laboratory confirmation of critical bedside readings and neonatal hypoglycaemia screening; regression to
  the mean of a sample selected on a noisy measurement.

## Default path

1. Read POCT-GLU-02: a meter beyond 5 per cent is withdrawn; its systematic error is the factor e of section 7, on the
   current calibration, against the laboratory's method in use.
2. Read GlyLink's pairing report (13,938 pairings from July 2026), keep those after each meter's ultima_taratura in the
   register, numeric meter values only.
3. Divide the C600's values drawn before 13 September 2027 by 1.035 (the laboratory's note).
4. Take each meter's mean of meter over laboratory ratios less one and withdraw the meters beyond 5 per cent.

Ends on: GX2-A564E, GX2-J921X, GX2-M707F, GX2-P722J, GX2-R842P, GX2-S959P, GX2-W228Y and GX2-W234L (GX2-M707F in, GX2-K532W out)
Golden: GX2-A564E, GX2-J921X, GX2-K532W, GX2-P722J, GX2-R842P, GX2-S959P, GX2-W228Y and GX2-W234L

## Stump sentence

A competent solver puts every pairing since each meter's January 2027 calibration on the C900 scale and withdraws
GX2-A564E, GX2-J921X, GX2-M707F, GX2-P722J, GX2-R842P, GX2-S959P, GX2-W228Y and GX2-W234L (GX2-M707F in, GX2-K532W out):
on the nursery and the neonatal intensive care two pairings in three are confirmations, drawn because the meter's own
reading was under 50 mg/dL, so they catch the meter when its random error ran low, pull GX2-M707F from -1.6 to -5.8 per
cent and GX2-K532W from +8.4 to +4.8; on the pairings the plan drew, GX2-K532W goes and GX2-M707F stays.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), tagged in the taxonomy for Data Quality Monitoring: a measurement-error model's bias term estimated from paired measurements, judged by how the pairs were drawn.
Domain test: The deciding quantity is each meter's systematic error against the laboratory, the bias of a measurement-error model estimated from meter and laboratory pairings as bedside glucose practice does it; whether a pairing measures it depends on why it was drawn, which only the field's workflow (scheduled verification against critical-value confirmation) tells.
Swap: "the meters whose error is beyond 5 per cent, read on the pairings the plan drew, because the confirmations were drawn by the meter's own critical reading" put into a warehouse's scales and its audit weighings loses its mechanism, since no weighing sends a second sample to a reference because the scale's own reading crossed a clinical limit; replacing the selection-aware estimate with the mean over every pairing changes the list.
Layer 1: the data manager's export in reception order with the copies an unacknowledged docking re-sends; the meters' clocks on solar time against the laboratory's civil time and the server's UTC; the export's ward and hospital as each meter's current assignment; LO and HI as text; the laboratory's analyzer change of 13 September 2027 never recalculated; the per-meter pairing plan with holidays moved; seven meters moved between wards.
Layer 2: field_method under population_selection: a sample selected on the measured value regresses toward the reference, so a bias is read on the pairs drawn independently of the meter's reading.
Decisive step: estimating each meter's systematic error on the pairings the plan drew on the morning round and leaving out the confirmations of critical readings, which exist because the meter's own result was extreme and so carry its random error outward.
Not semantics: every field of the pairing report reads as what it is (a meter result and the laboratory's result on the tube its barcode linked), the procedure describes the plan's pairings and the confirmations side by side without ranking them, and nothing in any field, code, unit or definition says a confirmation misstates a meter's bias.
Not rule application: no filed sentence says which pairings estimate the systematic error; section 7 defines the factor and its estimate as a mean of ratios without naming the pairings, so executing every filed rule over every pairing files the default list.
Analyst test: A strong analyst who reads the procedure, the note and the register, keeps every pairing since each meter's calibration on the C900 scale and takes each meter's mean ratio withdraws GX2-A564E, GX2-J921X, GX2-M707F, GX2-P722J, GX2-R842P, GX2-S959P, GX2-W228Y and GX2-W234L (GX2-M707F in, GX2-K532W out), dropping the nursery meter reading 8 per cent high and adding one reading 2 per cent low.
Estimand: each of the 52 meters' factor e by which it reads the laboratory's method in use (the C900) times 1 + e, the same at every concentration, on its current calibration (results after the manufacturer's last calibration), estimated as the mean of meter over laboratory ratios less one, a meter withdrawn when e is beyond 5 per cent either way (POCT-GLU-02 section 7 and the prompt).
No decoy: nothing is planted: the confirmations are the procedure's own critical-value practice, every pairing holds a true meter result and a true laboratory result, no memo, draft or figure argues for the pooled list, and no file ranks the meters.
No certified replay: no certified or published figure reproduces only under one method; the pairing report carries no per-meter summary, the procedure no worked example and the service report no measured error.
Lesson: a paired comparison is only as sound as the reason each pair was drawn, and pairs a meter's own extreme reading triggered show its error at its most outward, so a bias is read on pairs a schedule drew; no build on file estimates a measurement's bias from pairs selected on that same measurement.

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. Every pairing, the laboratory as reported (eleven meters) | the pairing report | readable |
| 2. Each meter's current calibration: pairings after ultima_taratura | the register, section 7 | readable |
| 3. The C600's values divided by 1.035 | the laboratory's note, section 7 | readable |
| 4. (decisive) The pairings the plan drew, the confirmations left out (the eight) | nothing names it: section 5 describes the plan's pairings and section 6 the confirmations, the report carries both without a type, and only the reasoning that a pair drawn because the meter read critical carries that reading's own error sends a reader to the plan | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the meters | the 52 in the register | only those with pairings | same call | every meter carries 98 or more plan pairings (asserted) |
| SF2 | systematic error | section 7's mean of ratios less one | ratio of totals, slope through the origin, geometric mean, median ratio | same call | section 7; the list asserted over five estimators, closest margin 1.3 points |
| SF3 | against the laboratory | the C900, the C600 divided by 1.035 | each pairing's own analyzer | another list | section 7 (metodo in uso alla data della valutazione) and the note |
| SF4 | the current calibration | pairings after ultima_taratura | every pairing since July 2026 | another list | section 7 (risultati successivi all'ultima taratura) |
| SF5 | the calibration day | after it | on or after it | same call | no plan pairing falls on its meter's calibration day (asserted) |
| SF6 | beyond 5 per cent | strictly | at or beyond | same call | the closest meter is 1.3 points from the line (asserted) |
| SF7 | LO and HI | out of the estimate | at 20 and 600 | same list | section 7 files them out (asserted) |
| SF8 | the plan's holidays | moved to the next working day | not moved | same call | the plan's rule; asserted |
| SF9 | the morning round | the laboratory's draw from 6:00 to 7:30 | other edges | same call | no other pairing within ten minutes of either edge on a planned day (asserted) |
| SF10 | the note's factor | divide by 1.035 | multiply by 0.965 | same call | the note; asserted |
| SF11 | a pairing's date | the laboratory's draw | the meter's clock | same call | asserted |
| SF12 | a patient result (asks) | once per meter and memory number, first reception | every row | the asks only | section 3: a result is in the record from the moment the data manager receives it |
| SF13 | a test's instant (asks) | the meter's clock less one hour | the clock as civil time or as UTC | the asks only | the plan pairings show the meter an hour before the draw in summer and on time in winter (asserted) |
| SF14 | the ward and hospital (asks) | where the meter stood on the day | the export's presidio and reparto | the asks only | section 8 (eseguiti nel reparto), the dictionary (assegnato), the register's history |
| SF15 | a test's date (asks) | Italian civil date | UTC or the meter's date | same figures | asserted |
| SF16 | more than two hours (asks) | over 7,200 seconds | 7,200 or more | same figures | asserted |
| SF17 | a listed meter's ward and hospital | the register's current assignment | where it stood when paired | same figures | none of the eight moved (asserted) |

## Ladder

| Route | Withdraws | Count | Golden |
|---|---|---|---|
| Every pairing, the laboratory as reported | the golden eight without GX2-K532W, with GX2-M707F, GX2-U982T, GX2-Y416X and GX2-Y986N | 11 | no |
| Every pairing since the calibration on the C900 (the default path) | the eight with GX2-M707F for GX2-K532W | 8 | no |
| The same, ratio of totals | the same eight | 8 | no |
| The same, median ratio | the golden eight with GX2-M707F and GX2-Y416X | 10 | no |
| Every pairing within 15 per cent of the laboratory | the golden eight without GX2-K532W | 7 | no |
| Every pairing whose meter value is not critical | the golden eight with GX2-J313P | 9 | no |
| The plan's pairings, the laboratory as reported | the golden eight with GX2-U982T | 9 | no |
| The plan's pairings since July 2026 | the golden eight without GX2-J921X and GX2-R842P | 6 | no |
| Golden: the plan's pairings since the calibration on the C900 | GX2-A564E, GX2-J921X, GX2-K532W, GX2-P722J, GX2-R842P, GX2-S959P, GX2-W228Y, GX2-W234L | 8 | yes |

The golden family agrees on the eight under every estimator of a single factor (mean of ratios, ratio of totals, slope
through the origin, geometric mean, median ratio), the note's factor as a division or as 0.965, the plan with or without
its holidays and LO and HI out or at the range's ends (asserted, closest margin 1.3 points). On the clean truth, every
pairing files the wrong list and the plan's pairings alone the truth (checks.py, dataset-generation 7.1).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 52 meters in the register | filed (register) |
| 2 | Unit of account | a meter, withdrawn or not | filed (section 7) |
| 3 | Attribution window | each meter's results after its last calibration | filed (section 7, register) |
| 4 | As-of dating | 4 January 2028, the record to 31 December 2027 | filed (mail, export) |
| 5 | Version basis | POCT-GLU-02 revision 3 | filed |
| 6 | Denominator | the laboratory's value in each ratio | filed (section 7) |
| 7 | Weighting | each pairing once | filed (section 7's mean) |
| 8 | Window length | to 31 December 2027 | filed (export) |
| 9 | Boundary inclusivity | beyond 5 per cent | C1 (1.3 points clear, asserted) |
| 10 | Rounding path | the error to one decimal from the unrounded mean | filed (the prompt) |
| 11 | Tie-break | none open | asserted |
| 12 | Maturity and censoring | every pairing resulted | C1 |
| 13 | Order of operations | the factor, then the ratios, then the mean | C1 |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per tube in the pairing report | asserted |
| 16 | Identity normalisation | the matricola across every file | filed |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | mg/dL and per cent | filed (section 3, the prompt) |
| 19 | Code and status semantics | LO, HI, PAZIENTE, CONTROLLO | filed (dictionary, section 7); never the stump |
| 20 | Integerisation | whole counts on the asks | filed (the prompt) |
| 21 | Clause scope | section 7 for every meter | filed |
| 22 | Forward window contents | the January 2028 visit corrects the current calibration's error | filed (section 7, the mail) |

## Literal reader

Executing the prompt and every filed sentence word for word (sections 3 to 8, the note, the register, the plan) leaves
one open move, which pairings estimate each meter's factor; the data's structure forces it (the confirmations exist
because the meter's reading was critical, and on the neonatal wards they are two pairings in three and run outward),
and every estimator of a single factor on the plan's pairings files the same eight (asserted, closest margin 1.5
points).

## Oracles

- No file ranks the meters or carries a per-meter error, a list or a projected figure.
- The 2027 service report lists every meter as calibrated; every route passes it.
- The laboratory's note states its 3.5 per cent; every route that reads it applies it.
- The external quality scheme shows the laboratory's own accuracy; every route sees it and none needs it.

## Ask sheet

Ask 1: per hospital and quarter of 2027, the share of patient results reaching the clinical record more than two hours
after the test (12 figures, per cent to one decimal). Ask 2: per ward, the patient tests of 2027 (13 counts). Both read
the data manager's export (GlyLink_risultati_2026-2027.csv), which the call never reads; the call reads the pairing
report, the plan, the register and the note (separation asserted).

Devices, silent (no filed sentence points at any of them):
- The meters' clocks keep solar time all year: read as Italian civil time, every summer result looks an hour later than
  it reached the record, read as UTC every result an hour earlier. Moves every figure of ask 1. Found only in the plan
  pairings, which show the meter an hour before the laboratory's draw from April to October and on time in winter.
- The export's presidio and reparto are each meter's current assignment; seven meters moved in 2027, three of them
  between hospitals (the register's Storico ubicazioni). Moves every figure of ask 2 and nine of ask 1.
Hazards: the copies a docking the meter never saw acknowledged re-sends whole at the next docking under new
id_risultato (moves every figure of both asks unless removed by matricola and n_memoria keeping the first reception);
control runs among the results; LO and HI as text.

| Path | Ask 1 late share | Ask 2 tests per ward | Keeps |
| --- | --- | --- | --- |
| the export as delivered, every row a result | 0 of 12 | 0 of 13 | 0 of 25 |
| the copies removed by memory number, the export's ward, the clock as civil time | 0 | 0 | 0 |
| the same, the clock read as UTC | 0 | 0 | 0 |
| the copies removed keeping the last reception | 0 | 0 | 0 |
| the solar clock found | 3 | 0 | 3 |
| the location history found | 0 | 13 | 13 |
| both found, the copies kept | 0 | 0 | 0 |

| Ask | Cracker (the call landed, the export's ward, the clock as civil time) | Verdict |
| --- | --- | --- |
| 1 late share per hospital and quarter | 0 of 12 | miss |
| 2 tests per ward | 0 of 13 | miss |

Pair ceiling: 28.5 ((45.0 + 12.0) / 2), the cracker keeping none of the 25 ask figures on the call and the mirror the same.
Mirror leakage: 0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack. A reader who finds the location history keeps 13 of 25 (73.6 with the
call); the stage 4 readers are the measurement.

## Pre-ship check

- Free gates (stage 3): generator checks 56 passed (the golden is the world's truth, five single-factor estimators
  agree on the list at least 1 point clear of the line, every named wrong route files another list, the easy route
  fails on the clean truth and the scheduled pairings alone recover it, SF1 to SF17, the asks against the world, the
  devices present, the pack gates, the documents read back); verify.py 0 failures on its own csv and openpyxl path;
  two builds byte-identical (target.zip dfd2d32a); figures_check 62 of 62; precut 51 of 51; voice-check PASS.
- leak.py REVIEW, no LEAK, both lines harmless: 400 mg/dL is section 6's critical value, which the procedure files
  because the ward needs it, and the write-up names it to say why the confirmations are drawn; the prompt's ask
  sentence carries the deliverable's own column words (ward, hospital, systematic error), which the decision needs.
- guard heart WARN (repeat.decision, repeat.deliverables, repeat.question_form, answered under Draw); surface: the
  pack's personas are the card's three; six pairs promoted for the author's optional adjudication, none on a hard tell
  (task243, task244, task246, task247 on the lane's shared xlsx and png deliverables and formats; task245 and task265
  on gap, pattern and decision family, differentiated on the card).
- Containers clean (no producer signature, no out-of-band timestamp) in target/ and golden/.
- Golden realism: the workbook opens on the finding (8 of 52) with the procedure and the office's date under it, the
  list by hospital and ward with the plan pairings each error rests on, every meter's sheet with its last calibration
  and outcome, the section 8 indicators by hospital and quarter and by ward, and a notes sheet citing the procedure,
  the note and the data's cut-off; the chart is a lollipop of every meter by hospital and ward against the band, the
  listed eight marked and labelled, a source line under it.
- The 10/10 rules re-read against the built pack: the decisive step is still which pairings estimate a meter's
  bias, and no filed sentence makes it (section 7 defines the factor and its estimator, not the pairings); the solar
  clocks, re-sent copies, current ward fields, LO and HI, the analyzer change and the plan's holidays are each the
  systems' own and none moves the list.
- Open risk, stated: a reader who asks why a nursery meter has three times the pairings of a ward meter, and reads
  section 6 as a selection on the meter's own value, lands the call. The stage 4 readers are the measurement.

## Tried and rejected

- The seed's own pitfall (the errors-in-variables slope between two noisy instruments): spent by task249 v1, landed
  by its reader.
- One key, the loss per supplier (the draw as filed, prototype 4): a single insight readers enumerate once they see the
  changes' jumps, the coin-flip shape of the measured drivers (task249's five architectures each landed on one reflex);
  prototype 5 sets the loss by the cylinder's interior, which one supplier changed in 2026, so the per-supplier rate is
  a mixture and is a rung.
- The ask layer with the check hour named invalid in the manual (valid hours and hours above 350): the counts do not
  move when a dropped hour shifts by one, so a reader executing section 5 on the stamps as written kept the valid hours
  whatever the clock; measured pair 76.0. The check hour is now left to the 45-minute rule and the check's times, the
  old firmware stored ppb, and the mean joins the asks.
- Physical & Environmental Sciences, sensor calibration and measurement, shape 10, monitoring_export: BLOCKed by
  task250's shipment (pairing, subdomain, artifact) and task471 (shape); redrawn as above.
- Architecture 1 (the SO2 analyzers' gain against true SO2 read through span gas that loses SO2 with its age since
  certification at a rate the cylinder's interior sets, fitted on the 31 cylinder changes): spent 10-20 at stage 4.
  Both scored readers landed the four analyzers, each by fitting the change readings' jumps to an exponential loss from
  the certificate date and splitting on the certificates' passivation once the per-supplier fit left a 4.5 per cent
  residual; reader B also kept 32 of 33 ask figures, finding the firmware update's 2.62 level jump, the standard-time
  stamps and the unmarked check hour. The estimand's own words (gain against true SO2) sent both straight to the
  reference's truth, and the change readings measured it in one division: a chain a careful reader models, with a
  misfit that points to its second link. Judge pass 1 DETERMINISTIC, FIX_NOW (the visit edge, pinned before the
  readers came back).
- The ask devices as first drafted (stage 2): section 5 named the hours of verification and maintenance not valid and
  the spare's hours as the station's, so a literal executor of the rule found both devices; the rule now files only the
  45 minutes of station air, visits are shaped so every hour they touch holds 16 minutes of them or more, and the spare's
  hours sit under the store's code.
- A 25 degrees C logger setting on integer micrograms (stage 2): too weak to move a mean at one decimal, and rescaling
  the database against reading the archive's ppb split two 19th values at whole micrograms; now 0 degrees C, the
  database at one decimal and the archive at two, both routes agreeing at the asked rounding.
- Architecture 2 (the NOx converters' efficiency clocked in the NO2 they reduce, a pooled curve steepening past about
  90 ppm-hours carried on each station's seasonal load to the 2028 service): spent 10-20 at stage 4. Both scored
  readers landed the seven (BP01, BP02, BP03, BP04, BP05, BP08, BP13), each going straight to the converter's
  accumulated NO2 as the wear clock (reader A: "modelling converter decay from the exposure it accumulates"); the
  field's own wear model is inside a strong reader's hypothesis space, and the stations' different loads, which the
  stump needs, make it visible in the first plot. The ask layer held for both (4 of 48 each): the new contractor's
  titration hours coded valid were missed by both, MAG and the 0 degrees C loggers found by both. Judge pass 1: the
  isolated thread's Bash calls were refused by the auto-mode classifier and no verdict was issued.
- Architecture 2's judge pass 1b (the same pack, the isolated thread re-run once from the scratchpad): DETERMINISTIC
  APPROVE; the architecture stays spent on Gate F.
- Architecture 3's first world (each meter's random error proportional only, pairings twice a week): the confirmations
  moved a neonatal meter's pooled mean by about 1.5 points against a 0.8-point standard error, so no seed held a clear
  golden and a pooled list two meters off; the meters' constant error at low glucose (5 mg/dL beside the proportional
  5 per cent) and three plan days a week on the neonatal wards give the confirmations about 4 points there.
- The route that keeps every pairing whose meter value is not critical landed the golden list while the nursery's median
  sat at 70 mg/dL; at 60 the plan's own low pairings leave with the confirmations and the route files a ninth meter.
- Regression with an intercept (Passing-Bablok, least squares) in the golden family: the slope spread several points on
  the narrow-range wards and broke the margin; section 7 defines a single factor, which the intercept forms do not
  estimate, and files the mean of ratios because the printed error still spread half a point among the single-factor
  estimators.
- The analyzer parallel run as a pack file (calibration parallel_run_overlap): BLOCKed by ban.calibration against task481
  at registration; the run's relation is a lower rung, so the laboratory's note files the factor and no corpus ships.
- Architecture 3 (52 bedside glucose meters, each meter's systematic error read on the plan's pairings, the critical-value
  confirmations being selected on the meter's own reading): spent 2026-10-20 at stage 4 on target.zip dfd2d32a. Scored
  reader A landed the call by keeping only the planned morning-round pairings (it quoted section 5's "almeno nei giorni
  del piano" and read every confirmation's meter value beyond 50 or 400 as selection on the meter result); reader B filed
  the default path (every pairing since the calibration: GX2-M707F in, GX2-K532W out). Both kept 25 of 25 ask figures:
  the re-sent copies (a duplicate check on matricola and n_memoria), the solar clocks (the planned pairings' summer gap)
  and the register's location history are battery work, the measured-as-executed list. Judge DETERMINISTIC APPROVE, Gate H
  analytical. Selection on the measured value is a textbook reflex once the data shows it in one column; a fourth
  architecture is the author's call.
