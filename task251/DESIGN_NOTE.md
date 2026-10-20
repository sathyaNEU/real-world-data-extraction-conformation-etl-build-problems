# task251 design note

## Draw

Card `cards/task251.json` (architecture 1, drawn 2026-10-20). Guard verdict WARN, no BLOCK. At the draw the card was
filed in Physical & Environmental Sciences (sensor calibration and measurement, shape 10, monitoring_export) with
WARNs only; when task250 shipped the same afternoon its delivered card brought ban.pairing, ban.subdomain and
ban.artifact into this card's window, and ban.shape stood against task471 v4. The axes were redrawn rather than
argued: the task is a measurement-error model's estimate, each analyzer's error read through a reference with its own
error (General Statistics & Data Science, missing data, censoring and measurement error, a task type the taxonomy tags
for Data Quality Monitoring & Alerting), the stakeholder's working file is the field operations log (the visit log and
the calibrators' log), and the criteria come from each analyzer's verdict and each station's three 2027 record figures,
a structure outside the eighteen shapes (shape 10 also wants one file). The WARNs left, answered: repeat.decision
(designation set after task471 v4: the decision is which analyzers go, a set by nature) and repeat.question_form
(which, after task471 v4: the question is a pick). driver.near 0.11 against task249 v2 (lineage), differentiated on the
card (there the units stood apart from references that shared the truth only in mixed hours; here the reference stands
with the unit and loses strength with its own age, at a rate its construction sets). `guard.py slots` for span,
cylinder, reference gas, decay, passivated and treatment: no slot note holds the mechanism. task249 v1 spent the
seed's own pitfall (the errors-in-variables slope, landed by the reader).

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error; drawn for Data Quality
  Monitoring & Alerting. The object is the health of the network's SO2 measurements, and the call is a monitoring
  decision: which analyzers go to the recalibration round.
- **The seed, re-found.** DQ24 gave the world (instruments read against references), the decision (which instruments'
  calibration breaches tolerance) and the quantity (each instrument's gain). Its pitfall, the attenuated slope between
  two noisy instruments, is spent (task249 v1); the decisive step is re-found in the data's own structure: the reference
  the routine checks read against loses strength as it ages, at a rate set by its construction rather than by who sold
  it.
- **Niche.** Fundición Caleta Lobos, a copper smelter on the Atacama coast, runs the SO2 network its decontamination
  plan requires (Red de Monitoreo Bahía Lobos): eleven stations with UV-fluorescence analyzers, a backup beside the
  principal at the two compliance stations, thirteen in all. Every night at 02:10 by its own standard-time clock each
  analyzer's calibrator spans it at 400 ppb from its own cylinder of SO2 in nitrogen; at the monthly visit the
  technician adjusts the analyzer when the span reads more than 3 per cent off, and at a cylinder change reads it on the
  outgoing and the incoming cylinder minutes apart. Cylinders come from two suppliers and wait in store for months;
  Cilgas Atacama sold untreated aluminium cylinders and, from March 2026, passivated ones too, Normagas Sur only
  passivated; the interior is written on the suppliers' certificates, not in the register. In January 2028 an
  accredited laboratory recalibrates, against fresh certified gas, the analyzers outside the network's 5 per cent
  tolerance against true SO2.
- **The call.** Which analyzers go to the January 2028 round: those whose gain against true SO2 on 31 December 2027
  lies more than 5 per cent either side of one.
- **Shape.** other: each of the 13 analyzers' verdict (13), the round list and the nine staying (2), the chart of the
  gains against the band with the four marked (4), each of the 11 stations' 2027 valid hours, mean and valid hours above
  350 (33), the two files (2): 54 criteria before the components.
- **Strategy.** `other` (reference ageing) with the reason in the card's notes. Gate G decomposition_attribution (the
  analyzer's apparent agreement split into its own gain and its gas's loss); generators G13 (the certified
  concentration holds at its certificate's date, not on the night of use), G6 (supplier A's cylinders changed interior
  in 2026, so a rate per supplier is a mixture), G3; gap objective, population; calibration parallel_run_overlap (two
  references read by one analyzer minutes apart); context artifact operations_log; Layer 2 estimation_fit, pattern
  own:span-gas-loss-by-cylinder-interior-written-into-the-analyzer.
- **Forum, event, organisation.** operations_desk (the network desk books the round), purchase_order_or_contract (the
  laboratory's January round is booked by list), manufacturer (a smelter). Role field_unit_lead (the head of the SO2
  monitoring network).
- **People** (`guard.py names --geo Chile --seed 251`, locale es_CL): Daniela Ferrada, head of the monitoring network,
  who asks; Vicente Toloza, the field technicians' lead; Néstor Fuentes, the laboratory's account manager. None appears
  in the prompt.
- **Data-native sentence.** A low-concentration SO2 span gas loses SO2 to its cylinder's walls as it ages, fast in
  untreated aluminium and slowly in a passivated cylinder, so every adjustment of an analyzer to an aged untreated
  cylinder writes the gas's loss into the analyzer and the nightly spans against that cylinder cannot see it; the
  cylinder changes, each read on both cylinders minutes apart, measure the loss, and fitted by the cylinder's interior,
  which only the certificates record, they give each analyzer's gain as its span over the fraction its cylinder holds.
- **As-of.** Monday 3 January 2028 (the laboratory's mail); the list is due Friday 7 January, the round runs 17 to 21
  January. The estimand is the gain at the close of 2027 because the manual's section 7 sets the round on it; the call
  faces forward to a round not yet held.
- **Sources.** The client's two-layer standard; the stability of low-concentration reactive gas standards (wall loss in
  untreated aluminium against passivated cylinders, ISO 6142 and ISO 6143 practice, EPA Protocol gas certification);
  EN 14212 quality assurance for UV-fluorescence SO2 analyzers (span checks, as-found and as-left, adjustment criteria,
  the 45-minute hour).

## Default path

The path a competent analyst takes after reading every file and filed rule correctly, the pack cleaned (the cylinder
numbers keyed into the calibrators resolved to the register, the visit log read, the certificates and the register
matched).

1. Read the manual: the round takes the analyzers more than 5 per cent off true SO2 at the close of the year (section
   7), the visits adjust past 3 per cent off the cylinder's 400 ppb (section 4).
2. Read each analyzer's span on the night of 31 December over 400 ppb: every one within 3.4 per cent, so on the span
   route none goes.
3. (the careful step) Read the cylinder changes, where the incoming cylinder reads the analyzer up to 24 per cent higher
   than the outgoing one, as the gas the outgoing cylinder lost; fit the loss rate per supplier on the 31 changes with
   each cylinder's age since its certificate (Cilgas Atacama 9.6 per cent a year, Normagas Sur 1.3), and divide each
   analyzer's span by the fraction its cylinder holds on 31 December.

Ends on: six analyzers
Golden: four analyzers

## Stump sentence

A competent solver who reads the cylinder changes' jumps as the old gas's loss fits the loss rate per supplier and sends
six analyzers to the round (none on the December spans alone), adding UVF-2051 and UVF-1932, which run on Cilgas
Atacama's passivated cylinders; the loss is set by the cylinder's interior, which only the certificates record, and a
passivated cylinder loses SO2 as slowly from either supplier, so four go: UVF-2207, UVF-1964, UVF-1987 and UVF-2075.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), a task type the taxonomy tags
for Data Quality Monitoring & Alerting; the call is which analyzers go to the recalibration round, a monitoring decision
on the health of the network's SO2 record.

Domain test: the deciding quantity is each analyzer's systematic measurement error, estimated from a measurement-error
model in which the reference itself carries an error that grows with its age at a rate its construction sets,
identified only by paired readings of two references minutes apart; that a reactive gas standard loses SO2 to its
cylinder's walls, faster in untreated aluminium than in a passivated cylinder, is the setting's (gas metrology), and the
model, its identification and its stratification are the task type's own.

Swap: General Statistics is swapped on the method: replace the measurement-error model with the routine checks' own
agreement with their reference (a generic summary) and none of the 13 goes; fit the reference's error by vendor rather
than by construction and six go; the call turns on the model itself, so the domain carries it.

Layer 1: the calibrators' log keyed by cylinder numbers in three forms; the register and the two suppliers'
certificates in their own formats and Spanish, decimal commas; the visit log's readings and notes in Spanish; the
loggers' 2027 export semicolon separated with decimal commas and a re-sent block; until each station's firmware
upgrade the old firmware's hours on standard time and in ppb, its check and visit hours unmarked; Chile's April and
September clock changes in the new firmware's hours; a meteorological tower and the stack's emissions beside them.

Layer 2: estimation_fit: the reference's error (span gas lost to the cylinder walls since its certificate) estimated
from the transfer comparisons at the cylinder changes and stratified by what drives it, the cylinder's interior, not by
the vendor that sold it, then divided out of each analyzer's check.

Decisive step: fitting the loss rate by the cylinder's interior from the 31 cylinder changes (the log of the incoming
over the outgoing reading as the outgoing cylinder's rate times its age less the incoming one's) and dividing each
analyzer's span on 31 December by its cylinder's remaining fraction; by supplier, three passivated Cilgas Atacama
cylinders' small jumps are averaged with the untreated cylinders' large ones and two analyzers on passivated Cilgas
Atacama cylinders go with the four.

Not semantics: every field reads plainly (the spans, the readings at a change, the certificate's interior line, the
register's supplier and dates); read correctly they give each analyzer's agreement with its own cylinder's label and
each cylinder's interior, and nothing in any field says the label has aged or that the interior sets how fast.

Not rule application: no filed rule corrects a certificate or fits a loss; the manual sets the tolerance against true
SO2 and the adjustment against the cylinder's 400 ppb, and executing every rule on the record files the span route
(none); the loss model, its stratification and the division are the analyst's.

Analyst test: a strong analyst who cleans the pack and reads every rule takes each analyzer's span on the year's last
night as its gain and sends none; one who reads the cylinder changes' jumps as the gas's loss and fits it per supplier
sends six analyzers, two of them on passivated cylinders that have lost almost nothing; the rate set by the interior
sends four.

Estimand: each of the 13 analyzers in service on 31 December 2027, its gain against true SO2 that day (its reading of
a known true concentration over that concentration), flagged when it lies more than 5 per cent either side of one; the
gain and the tolerance in the manual's section 7, the date and the population in the prompt.

No decoy: no document argues for the spans or certifies the gas's stability (the certificates state a concentration at
a date and carry no stability or validity claim); no memo, summary or briefing carries a round list; the register
carries the supplier because a register would.

No certified replay: no certified figure exists to reproduce; the spans every route reproduces are the record the
decision reads through, not an answer (validated_decoy false).

Lesson: a monitor whose every routine check passes can be wrong when the reference the checks read has its own error,
and that error must be modelled by its physical cause, not by the label that happens to sort it; no build on file reads
a reference's own decay out of a check (`guard.py slots`).

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. The December spans read as the gains (none) | the calibrators' log, the manual's 400 ppb | readable |
| 2. The loss per supplier from the changes (six) | the visit log's two readings at each change, the register's supplier and certificate date | readable |
| 3. (decisive) The loss by the cylinder's interior (four) | nothing names it: the register sorts the cylinders by supplier, the interior sits on the certificates, and only the changes' readings against the cylinders' ages show three Cilgas Atacama cylinders losing as slowly as Normagas Sur's | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | gain | the reading of a known true concentration over it: the span over 400 over the fraction the cylinder holds | the span ratio | none | section 7, true SO2; the analyst test asserted |
| SF2 | more than 5 per cent either side | the gain's distance from one above 0.05 | at or beyond | same list | every gain 1.2 points or more from the line under every form (asserted) |
| SF3 | on 31 December 2027 | that night's span | the last visit's as-left span | none | no adjustment on 31 December (asserted) |
| SF4 | our analyzers | the 13 in service, the two backups included | the 11 principals | same four, both backups stay | the register's cylinders in service on 31 December (asserted) |
| SF5 | the gas's age | since the certificate's date | since installation | three | the certificate dates the concentration; installation ages file three (asserted) |
| SF6 | the loss's form | a constant fraction a year | a straight line | same list | asserted |
| SF7 | the outgoing reading at a change | the visit's span as found | that night's span | same list | the two agree within 0.5 per cent (asserted) |
| SF8 | the incoming cylinder | its own loss since its certificate in the fit | read as fresh | same list | asserted |
| SF9 | a certificate bias | none | an intercept in the fit | same list | asserted |
| SF10 | the stratum | the interior | supplier and interior | same list | asserted |
| SF11 | the span read | that night's | the last week's mean | same list | asserted |
| SF12 | the zero | the span as read | the night's zero subtracted | same list | asserted (every zero within 2 ppb) |
| SF13 | the interior | the certificate's line (interior pasivado, tratamiento interior de pasivación) | supplier A's cylinders filled from 2026 | another list | the certificates name it; supplier A filled both after March 2026 (asserted) |
| SF20 | valid hour | at least 45 minutes of air; no hour a visit touches | the flags alone | not the call | section 5 (asserted against the truth) |
| SF21 | the check's hour | 02:00 by the calibrators' standard-time clock, 30 minutes of air, on each night the calibrators' log shows a check | 02:00 on every stamp | not the call | sections 2, 3 and 5; the new firmware's C flags fall on it (asserted) |
| SF22 | a visit's hours | every hour from arrival to departure | the hours with check gas only | not the call | section 5 (filed) |
| SF23 | the old stamps' clock | local standard time | official time | not the call | no clock change in the old firmware's rows, the C hours' place (asserted) |
| SF24 | the old values' unit | ppb | µg/m³ | not the call | the range reported at 1,000.0 before the upgrade and 2,620.0 after (asserted) |
| SF25 | each hour once | identical rows once, both rows of the hour lived twice | one row per stamp | not the call | asserted |
| SF26 | above the limit | greater than 350.0 µg/m³ | at or above | same figures | section 6; no valid hour at 350.0 (asserted) |
| SF27 | the mean | over the valid hours, in µg/m³ at 2.62 to the ppb | 2.6187 | same figures | section 5's 2.62; every mean 0.0096 or more from its rounding edge (asserted) |
| SF28 | 2027 | the hours the database holds for 2027 by each logger's clock | official 2027 | same figures | the official first hour of the year sits in 2026's file; no station ends the year on the old firmware (asserted) |
| SF29 | an hour at the range | valid, at the range | left out | another count | section 5 (asserted) |

## Ladder

| Route | Loss a year | Analyzers sent | Files |
|---|---|---|---|
| The December spans as the gains | none | none | none |
| The last week's spans, the last visit's as-left | none | none | none |
| The loss per supplier from the changes | A 9.6, B 1.3 | UVF-2207, UVF-1964, UVF-1987, UVF-2075, UVF-2051, UVF-1932 | six |
| The loss per supplier, the outliers set aside | A 10.2, B 1.4 | the same six | six |
| One loss for every cylinder | 7.2 | eight (five on passivated cylinders) | eight |
| The loss by interior from installation | untreated 11.6 | UVF-2207, UVF-1987, UVF-2075 | three |
| The loss read from the spans' decline between adjustments | untreated 13.6, passivated 3.9 | six (UVF-2051, UVF-2148 added) | six |
| The certificates older than a year | none | six | six |
| Every untreated cylinder | none | six (UVF-2318, UVF-2263 added) | six |
| Golden: the loss by interior from the changes | untreated 10.2, passivated 1.3 | UVF-2207, UVF-1964, UVF-1987, UVF-2075 | four |

The golden list is the world's truth (every analyzer's true gain against the tolerance, asserted), and the same four
come out with the loss linear, with an intercept, by supplier and interior, with the incoming cylinder read as fresh,
on the last week's spans and with the zero subtracted (asserted).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 13 analyzers in service on 31 December 2027 | filed (prompt, register); SF4 |
| 2 | Unit of account | an analyzer; a valid hour | filed (sections 5 and 7) |
| 3 | Attribution window | the 2025 to 2027 changes; 2027 for the record figures | data; filed (prompt) |
| 4 | As-of dating | 3 January 2028 | filed (the laboratory's mail) |
| 5 | Version basis | MC-SO2-03 version 3 | filed |
| 6 | Denominator | the gain over one; the mean over the valid hours | filed (section 7, prompt) |
| 7 | Weighting | each change once in the least squares | C1 over the forms (SF6 to SF10) |
| 8 | Window length | the night of 31 December | filed; SF3, SF11 |
| 9 | Boundary inclusivity | more than 5 per cent; greater than 350.0 | filed; SF2, SF26 |
| 10 | Rounding path | whole hours; means to one decimal from unrounded values | filed (prompt); SF27 |
| 11 | Tie-break | none open | asserted (no gain within 1.2 points of the line; no mean at an edge) |
| 12 | Maturity and censoring | none | not applicable |
| 13 | Order of operations | the loss fitted, then each span divided | C1 |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | identical rows once; the hour lived twice twice | SF25 |
| 16 | Identity normalisation | cylinder numbers keyed in three forms resolve to the register's | asserted |
| 17 | Netting against gross | either side of one | filed (section 7) |
| 18 | Dimensional units | ppb for the spans; µg/m³ for the hours, the old firmware's ppb converted | filed (section 5); SF24 |
| 19 | Code and status semantics | flags C, M, F, R; ajuste; the interior lines | dictionary, certificates; never the stump |
| 20 | Integerisation | whole hours | C1 |
| 21 | Clause scope | section 5's visit rule over every hour a visit touches | filed |
| 22 | Forward window contents | the January 2028 round on the gain at the close of 2027 | filed (section 7) |

## Literal reader

Executing the prompt and every filed sentence word for word (sections 2 to 7, the register, the certificates, the logs)
gives the golden: section 7's gain is a reading of a known true concentration over that concentration, which a span
over 400 ppb is only when the cylinder still holds what its certificate says, and the cylinder changes, read on both
cylinders minutes apart, show it does not; the one open move, the loss's model, converges over every form a competent
analyst would use (SF5 to SF13) once its rate is set by the cylinder's interior, and the golden list is the world's
truth (C1, asserted).

## Oracles

- No figure in the pack certifies a gain, a loss rate or a round list; the certificates state a concentration at a
  date.
- The spans every route reproduces (the calibrators' log) read every analyzer within 3.4 per cent of 400 ppb on 31
  December; they pass every route alike.
- The new firmware's C and M flags fall exactly on the check hours and the visits' hours (asserted); they document the
  rule the old firmware's hours are read by and control nothing on the call.

## Ask sheet

Ask A: each station's valid hours in 2027 (11 figures). Ask B: each station's mean SO2 over its valid hours, µg/m³ to
one decimal (11). Ask C: each station's valid hours above 350 µg/m³ (11). None reads the call's rows: the call reads
the calibrators' log, the visit log's readings, the register and the certificates; the asks read the loggers' 2027
export with the visit log's times and the calibrators' nights, none of which moves the call (deleting the export leaves
the list, asserted). The three devices share one real cause, each station's 2027 logger firmware upgrade (the visit
log's note): until it, the old firmware left the nightly check's hour unmarked with the zero's minutes averaged in
(ask A's primary, and ask B's through the zero), stored the analyzer's ppb (ask B's and C's primary) and kept standard
time, so a visit's official times sit an hour late on its stamps from September to April (ask B's and C's secondary).

| Path | Valid | Mean | Above | Kept |
|---|---|---|---|---|
| the flags as the record, the values as written | 0 | 0 | 2 | 2 of 33 |
| the flags, one row per station and stamp | 0 | 0 | 2 | 2 of 33 |
| the manual's visit rule on the stamps as written | 0 | 0 | 2 | 2 of 33 |
| the visit rule on the stamps, the manual's 02:00 hour too | 0 | 0 | 1 | 1 of 33 |
| one device found: the old values in ppb | 0 | 5 | 0 | 5 of 33 |
| one device found: standard time under the visits | 0 | 0 | 2 | 2 of 33 |
| one device found: the unmarked check hours | 6 | 0 | 2 | 8 of 33 |
| two found: ppb and standard time | 0 | 3 | 8 | 11 of 33 |
| two found: the check hours and standard time | 11 | 0 | 2 | 13 of 33 |
| golden | 11 | 11 | 11 | 33 of 33 |

| Ask | Cracker (the flags and units as the dictionary gives them, the battery, the manual's visit rule on the stamps as written) | Verdict |
| --- | --- | --- |
| A valid hours | 0 of 11 | miss |
| B mean | 0 of 11 | miss |
| C above 350 | 2 of 11 (two stations whose old hours never crossed 350) | miss |

Pair ceiling: 31.8 ((48.3 + 15.3) / 2), the cracker keeping 2 of 33 ask figures on the call and the mirror the same.
Mirror leakage: 6 per cent of ask weight.
Measured by: generator/pair.py on the cut pack. A reader who finds one silent device keeps at most 8 of 33 (58.3 with
the call); two, 13 of 33 (66.7 with the call); the stage 4 readers are the measurement.

## Pre-ship check

- Free gates (stage 3): generator checks 182 passed (the call against the world's truth, the ladder and the closure
  over seven forms, the analyst test on the clean truth, SF1 to SF29, the separation line and the deletion test, the
  asks against the loggers' truth with every device's move asserted, the documents read back, the realism sweep);
  verify.py 0 failures; two builds byte-identical (target.zip 9c884ce8); figures_check 66 of 66; precut 51 of 51;
  voice-check PASS.
- leak.py REVIEW, no LEAK, each line harmless: the manual carries three of the call's words (analyzers, January,
  round) as its own subject; the stump-paragraph terms in the manual and the dictionary are the network's ordinary
  nouns; the certificates carry their interior lines, the evidence the decisive step reads, naming no loss and no move.
- guard heart WARN (repeat.decision and repeat.question_form, answered under Draw); surface: the card's three people
  only.
- Containers scrubbed at every save, audit clean, in target/ and golden/.
- Golden realism: the note leads with the finding as its title under a header block, carries the chart (the band, the
  four marked, the span ticks), the thirteen analyzers' table and a footnote on the gain and the certificates; the
  workbook's Round sheet is titled with the finding, frozen, formatted per column, beside the cylinder changes, the
  stations' 2027 record with a total row and a note on the old firmware, and a notes sheet.

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
