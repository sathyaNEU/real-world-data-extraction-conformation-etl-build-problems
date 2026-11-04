# task399 design note

Architecture 1, drawn 2026-11-04. Root-Cause Analysis, Human Factors & Ergonomics, safety-incident-error-analysis.
A rail infrastructure manager's regional operating centre (Fenmoor Rail Operating Centre, the Wyvern route,
England), whose 2027 improvement plan funds one programme against the cause that produced the most of the
operating centre's own delay minutes in the twelve months to 30 September 2026.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task399.json`, registered 2026-11-04 and re-checked as filed: WARN
  only (`driver.near` 0.13 against two task307 lineage entries that were never drawn, `repeat.question_form`), the
  older same-puzzle and same-driver notes differentiated against task107 v2 and task121 v4. Nearest drawn driver
  0.06 (task137 v3).
- **Seed:** RC05 (an electricity distributor's one reliability programme, when the costliest cause leaves no fault
  record), read through `status.py task399` only. Kept: the decision (one programme from a catalogue of five) and
  the quantity (the outcome units the funded programme's cause accounted for over the last twelve months). Its world
  was set aside at the draw: `grid-reliability-outage-analysis` holds seven cards, and its slot notes spend every
  distribution-reliability mechanism this pass could find (Tried and rejected), so the number moved to another
  client domain under the same objective.
- **Pairing:** Human Factors & Ergonomics / `safety-incident-error-analysis` / Root-Cause Analysis. The call names
  the cause behind the operating centre's signaller-error delay minutes, so that the programme placed against it
  removes them.
- **Shape:** 12 (drill-down to one leaf): the operating centre's delay minutes taken apart by the cause that
  produced each incident, the funded cause's minutes taken down by workstation to the stage delivery begins on,
  and two decoupled ask tables (signaller hours by workstation and competence band; ARS sub-area hours off by
  workstation and quarter) supplying the rest of the criteria.
- **Decision:** root_cause_named: which of the five catalogue programmes the 2027 plan funds (A signaller competence
  training, B workstation display renewal, C eight-hour shifts, D ARS timetable data rebuild, E a seventh
  workstation splitting Hatherby), and the delay minutes its cause produced in the window. The plan is forward
  facing (the 2027 programme); the quantity is retrospective by the decision's nature (a cause is read off the
  incidents it produced), the reason recorded here.
- **Strategy:** classification_error: each incident's cause is observed only through the local investigation's
  finding, which is right for decisions, omissions and late route setting and wrong for slips (booked to the
  signaller), so the observed composition of causes is a biased image the analysis rebuilds from evidence. Gate G
  decomposition_attribution. Calibration organ none.
- **Data-native sentence:** Fenmoor's screens had later lines squeezed in eight to eleven pixels from an existing
  line, so at the entrances whose exits include both lines (nine on Hatherby, five or six on every other
  workstation) the exit a signaller wants sits beside another exit of the same entrance, and every signaller who
  sets those routes sometimes lands on the neighbour; the control system logs each slip that is caught as a route
  cancelled within seconds and reset from the same entrance, and each one that is not becomes a wrong route the
  local investigation books to the signaller.
- **Abstraction sentence** (what a reviewer holding this build and its nearest approved build would say is the
  same): none can be written. The approved Root-Cause build (111) asks which cause still operates in the forward
  window; the approved physical attributions (303's sibling feeders opening in the same minute, 275's unobserved
  trips, 193's piezometer gradient) re-attribute through a shared upstream supply, an observer's coverage or a flow
  direction. None re-attributes an operator's errors to a fixed geometry of two controls, read through the
  operators' own corrected reversals.
- **Clean-truth prototype** (scratchpad `t399/proto2.py`, 20 seeds) and the shipped pack (`generator/checks.py` on
  the cut pack): the display renewal's but-for minutes beat every rival's widest honest reach by 2.35 times in the
  pack (1.80 to 5.29 on the prototype seeds); the investigations' findings file A on 20 of 20 prototype seeds and in
  the pack under every booking of the distraction findings.
- **Simulation seed:** the drawn-close routes' request mix (peak-heavy December 2025 services), the first-two-years
  mistake rate and Hatherby's extra drawn-close entrances were set so every ladder statistic holds in expectation;
  the shipped seed (15) was chosen among 24 swept (`t399/sweep.py`) as one whose realisation keeps all of them and
  both "counted in full" bounds at once. Nothing is placed by hand.
- **WARN answers:** `driver.near` (0.13, task307 "seed OS09" and "resource adequacy draft"): both entries are
  draws dropped before any driver was written, so the similarity is lexical. `repeat.question_form` (which, against
  task489 and task314): the decision is a pick among five filed programmes; the shell is redrawn at the role level
  and the deliverable set (pptx and xlsx) is new to the last twelve builds.
- **Furniture:** forum committee_or_panel (the route's safety review panel commits the plan), forcing event
  statutory_or_regulatory_filing (the plan goes to the safety regulator by 15 December 2026, answering its July
  2026 letter), org family utility_or_infrastructure, stakeholder the operating centre's safety and assurance
  manager, context artifact register (the operating incident register). None banned against the last three builds.
- **People** (drawn with `guard.py names --geo England --seed 399`, kept in `generator/names_drawn.txt`): Helen
  Douglas (safety and assurance manager, Panel secretary), Alan Pope (operating centre manager), Zoe Hayward (route
  performance analyst), Jake Bray (head of operations, Wyvern, who approves the catalogue), Joanna Bryan and
  Julian Thomson (the consultants who wrote and checked the 2025 workload assessment). Invented names: Fenmoor Rail
  Operating Centre, the Wyvern route, Linwell Ergonomics Ltd, Corvane.
- **Sources** (all synthetic, generated by `generator/`, CC0 1.0, dated within the fiction; provenance in
  `metadata.json`): the control system's signaller action log (357,103 rows, the spine), both operating incident
  registers (the 2025-26 workbook and the 2026-27 tool export with its category crosswalk), the OCF delay records
  and the attribution review log, the workstation layout export r8.2.1 (screen objects, routes, ARS sub-area
  crosswalk), the 2025-26 and 2026-27 rosters, the roster changes list, the competence register, the ARS status log
  of both servers, the terms of reference (PDF), the improvement catalogue (DOCX), and two distractors named in
  `metadata.json` only: the 2025 workload assessment (PDF) and the autumn 2025 railhead adhesion reports (CSV).

## Three rules

- **Task type:** safety-incident-error-analysis: attributing a control room's operating incidents to the causes
  that produced them, which serves Root-Cause Analysis in the taxonomy.
- **Domain test:** the deciding quantity is each wrong route's error mode, a slip of selection onto the control
  drawn beside the intended one against a mistake of intention, which human-factors incident analysis tells apart
  from the task and interface conditions of the error and checks against error probability per opportunity by
  performance shaping factor; the call is the cause whose removal, but for it, takes the most delay minutes.
- **Swap:** with an electricity network's nouns (feeders for routes, crews for signallers, megawatt-hours for
  minutes) the call "fund the display renewal because the wrong selections booked to competence are slips onto a
  control drawn eight pixels from the intended one" stops making sense: there is no operator choosing between two
  drawn controls and no record of the operator's own corrected selections.
- **Layer 1:** the 2025-26 register (desk names, local date and time, route text in three forms) against the
  2026-27 tool (W numbers, category codes, one datetime), crosswalked by the tool's own sheet; delay records with a
  review log moving minutes between incidents under three statuses; the control log in UTC with both servers'
  copies around each server change and desk names until release 8.2; the ARS log of both servers, renamed codes on
  each server's own release date, workstation-wide rows and server B stamping Central European time; two roster
  layouts (a periodic grid with a code key, a long tool export); a changes list missing changes made on the day;
  the competence register. Each is what the producing system writes; none is placed to be caught.
- **Layer 2:** classification error: the recorded cause is the investigator's attribution, not the mechanism, and
  the choice that flips the call is to classify each wrong route by the interface condition it occurred at (how far
  apart its set and required exits are drawn) and attribute by but-for, instead of trusting the recorded finding
  and the error rates by performance shaping factor that agree with it.
- **Decisive step:** separating design-induced slips from mistakes: recognising that the wrong routes at entrances
  whose two exits are drawn 8.0 to 11.5 pixels apart are capture slips of selection, made at the same rate by any
  signaller at any hour, so the cause that would have prevented them is the screen drawing, not the signaller.
- **Not semantics:** every field read correctly (finding codes, category crosswalk, desk names, route text forms,
  review statuses, the OCF code) still books the 76 slips to competence, distraction or workload, because the
  findings are correct records of what the investigators concluded and no field, code or unit carries the error
  mode.
- **Not rule application:** no filed rule says how to tell a slip from a mistake, and the terms of reference's
  but-for clause (2.3) is general; executing every filed rule with the recorded findings files A at 8,240 minutes.
  The enumerated family (booking by finding, with distraction to A, E, C or unbooked; rates by experience and peak
  hour; the display's own claim; classification by drawn separation) spans three calls and B from 812 to 8,985
  minutes; the standing family, once the geometry is computed, is one call at one figure (8,985 at every distance
  threshold from 12 to 50 pixels, and the same 76 incidents from the log's quick resets); the ruling-out is silent,
  a computation across the register, the layout export and the log that no sentence or column invites.
- **Analyst test:** a strong analyst who cleans the data and reads every rule books each incident's minutes by the
  investigation's finding, confirms it with wrong routes per request by experience (6.67 against 4.40 per 10,000)
  and funds A, signaller competence training, at 8,240 minutes; the golden is B at 8,985.
- **Estimand:** terms of reference WR-SRP-TOR-26-04, sections 2.1 to 2.5: the programme whose cause produced the
  most of the operating centre's delay minutes from 1 October 2025 to 30 September 2026; the register's incidents
  with OCF delay, by the date and time they occurred, UK time; an incident counts for a programme when it would not
  have happened had that programme been in place; minutes are primary and reactionary after the agreed review moves;
  delivery begins with the stage that would have removed the most.
- **No decoy:** no document argues for a programme, ranks the programmes or prices their benefit; the findings are
  honest records of what an investigator sees (experience, hour, time into shift); the workload assessment is a
  consultant's 2025 workload index, a declared distractor; nothing is copied, hidden or written to carry A or E.
- **No certified replay:** no certified or published figure reproduces under the golden's method and none is
  matched to recover it; the method is found from the evidence, not from a filed total.
- **Lesson:** a model learns that an error taxonomy's recorded cause can be the investigator's attribution rather
  than the mechanism, and that design-induced slips are found from the interface geometry and the operators' own
  corrected selections, not from error rates by performance shaping factor; no build on file attributes operator
  errors to the drawn geometry of two controls.

## Survivor anatomy

- **Actor:** the wrong route is the actor (a register row with its set and required route); the deciding property,
  how far apart the two exits are drawn on the screen, has no column in any file: it is a relation between two
  signal objects in the layout export, reached from the register's route text through the export's route table.
- **Link:** register route text to layout route (entrance, exit), exit to signal object, object to screen and
  position, the two positions to a distance; and, apart, the log's route set, cancelled within twenty seconds and
  reset from the same entrance to another exit; no key joins the register to either and no sentence invites it.
- **Reflex:** error probability per manual request by performance shaping factor sits at rung 1 and files A (first
  two years 6.67 against 4.40 per 10,000) or E (peaks 6.33 against 4.20); the investigation's own taxonomy is rung 0.
- **Back-test:** the textbook route validates: the first-two-years rate runs 1.52 times the experienced rate, the
  investigations' competence findings agree with it, and the 2025 workload assessment rates Hatherby the highest.
- **Second use:** the layout export also carries the ARS sub-area crosswalk and the desk numbering (ask 2 and the
  register's desks); the control log also carries who signed on to each desk (ask 1, relief placement and the
  changes made on the day); neither drops out of the pack if the decisive step is deleted.
- **Shock:** the slips run through every workstation and every month; Hatherby leads on them but also on late
  route setting (134 of 211), regulating and communication errors and on traffic (198 of the window's 470
  incidents); no unit, month or signaller is an outlier on any shipped statistic, and the 76 slips are not an
  interval of any one-column sort.
- **Pins:** the terms of reference file the WHAT in the organisation's genre (programme, window by UK time, OCF,
  but-for, minutes after agreed moves, first stage) and no filed sentence names a slip, the screen drawing, a
  distance, the layout export's coordinates or the log's cancellations.

## Default path

1. Read the terms of reference (the programme whose cause produced the most of the operating centre's delay
   minutes in the twelve months to 30 September 2026, an incident counting for a programme when it would not have
   happened had the programme been in place) and the improvement catalogue (programmes A to E).
2. Keep both registers' incidents occurring in the window, join them to the OCF delay records on the TRUST
   incident, total primary and reactionary minutes and apply the agreed review moves.
3. Book each incident to the programme its local investigation's underlying-cause finding names: competence to A,
   fatigue to C, ARS data to D, workload to E, equipment to B (distraction to A, to E, to C or left unbooked).
4. Check the finding with the field's own measure, error probability per opportunity: wrong routes per manual
   route request by the performance shaping factors the records carry. First-two-years signallers run at 6.67 per
   10,000 requests against 4.40, which confirms competence; the peaks run at 6.33 against 4.20, which a reader who
   weighs workload takes as the seventh workstation's case.
5. Fund the largest.

Ends on: A, signaller competence training, at 8,240 minutes.

Golden: B, the workstation display renewal, at 8,985 minutes, delivery beginning on W03 Hatherby.

## Stump sentence

A competent solver books the operating centre's delay minutes by each local investigation's underlying cause and
funds signaller competence training (A) at 8,240 minutes, confirmed by the higher wrong-route rate per request among
first-two-years signallers, because no column marks a slip and the investigations book every wrong route to the
signaller; the 76 wrong routes whose two exits are drawn 8.0 to 11.5 pixels apart are slips every signaller makes at
the same rate in quiet and busy hours, and the display renewal (B) accounts for 8,985 minutes.

## Readability screen

Tests: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second use.

| Rung | What fires | Verdict |
|---|---|---|
| Rung 0, findings booked to the catalogue (A 8,240) | 2 schema: the finding column is the booking | readable |
| Rung 0b, distraction booked to A, E or C (A in every booking) | 2 schema, 3 reflex | readable |
| Rung 1, wrong routes per request by experience and by hour (A, or E) | 3 reflex: the field's error probability by performance shaping factor | readable |
| Rung 2, the display's own claim, equipment findings and display faults (B 812, fourth) | 2 schema: the EQ1 code and the equipment finding | readable |
| Rung 3 (decisive), wrong routes whose set and required exits are drawn within 12 px, corroborated by the log's quick resets (B 8,985) | none: 1 no sentence names a slip, a distance or the drawing; 2 no column holds the separation, two joins and a geometry away; 3 the field's reflex measures rates, not the controls' geometry; 4 no control scores causes; 5 the battery computes no distance between screen objects; 6 a per-incident geometric classification and a but-for re-attribution, not one subtraction; 7 the layout export and the log ship for the asks | silent |

## Ladder

| Rung | Construction | Files | Leads | Figure | Golden's place |
|---|---|---|---|---|---|
| 0 | minutes by the investigations' findings | registers, delay records, reviews, catalogue | A | 8,240 (E 2,608, D 1,264, B 812, C 783) | B fourth |
| 0b | distraction (4,157) booked to A, E or C, or unbooked | the same | A | A 8,240 to 12,397 | B fourth or fifth |
| 1 | wrong routes per request by experience and by peak hour | registers, control log, competence register, rosters | A or E | 6.67 against 4.40, 6.33 against 4.20 per 10,000 | absent |
| 2 | the display's own claim (equipment finding, display faults) | registers | B | 812 | loses to A by 10.1 times |
| 3 | slips by drawn separation, but-for | registers, layout export, control log | B | 8,985 (slips 76 at 8,173, faults 10 at 812) | first |

Final margin: B 8,985 against the widest honest reach of any rival (C 3,825, A 3,195, E 1,784, D 1,264), 2.35
times; against every incident each rival touches (A 6,517, C 7,487, E 6,642) it still leads by 1.20 times. With
only the slips re-attributed in rung 0, B leads A 8,985 to 2,940. Starting workstation: W03 Hatherby 3,544 against
W05 Kestrow 1,487, 2.38 times. Inside the drawn-close routes the slip rate per request runs alike for both
experience bands (1.07), in and out of the peaks (0.86) and after eight hours on shift and before (0.93). Of the
360 routes cancelled within twenty seconds of being set, all but three were followed from the same entrance by a
request for the exit drawn beside the one cancelled; the three others cancel a route seconds after the same route
was set a second time and are followed by another exit or by none. Every one of those quick resets falls on one of
the 37 drawn-close pairs that carry the 76 slips, and those pairs select the same 76 incidents as the geometry.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | delay minutes | primary and reactionary | primary only (4,392) | same call | ToR 2.4 "primary and reactionary minutes" |
| SF2 | review moves | agreed moves only | every move, or none | same call, figure moves at most by the non-agreed rows | ToR 2.4 "as agreed"; asserted that every reading keeps B 1.4 times clear |
| SF3 | twelve months | UK date and time of occurrence | UTC | same call, same figure | ToR 2.2 "UK time"; no incident within two hours of either end (asserted) |
| SF4 | the register | both financial-year registers | the 2026-27 tool alone | A, a half year | ToR 2.2 "its operating incident register" over the window; both registers carry it |
| SF5 | the display's cause | the slips and the display faults | the equipment findings alone | B fourth at 812 | ToR 2.3 but-for; no investigation names the display for a wrong route (asserted) |
| SF6 | drawn close | within 12 px on one screen | any threshold to 50 px, or the log's quick-reset pairs | same call, same 76 | records converge: no exit pair drawn between 12 and 36 px, and no ARS wrong route at a drawn-close pair (asserted) |
| SF7 | a rival's minutes | but-for reach | every incident the rival touches | same call | asserted: B leads every rival counted in full |
| SF8 | by workstation | the register's workstation | the signaller's home desk | same call | the register records the workstation; the split adds to the figure (asserted) |
| SF9 | stage delivery begins on | the workstation removing the most | the busiest workstation | same (W03 both) | ToR 2.5; W03 leads by 2.38 times (asserted) |
| SF10 | route set and required | any of the register's three text forms mapped to the layout route | route identifiers only | same call | every wrong route's text maps to one layout route (asserted) |
| SF11 | the operating centre's incidents | register rows with OCF delay | every register row | same call | ToR 2.2; every window incident carries OCF delay (asserted) |
| SF12 | an incident with nil minutes | counted at nil | dropped | same call | no window incident ends at nil (asserted) |
| SF13 | an incident's minutes | the attribution records | the register's initial delay (4,190 for B) | same call | ToR 2.4 names the attribution records |
| SF14 | then in their first two years | the band on the date worked | the band on the shift's start | same figures | records converge: both window-edge nights worked outside the first two years (asserted) |
| SF15 | the second anniversary | split at that midnight | the band at the shift start | same figures | no worked span crosses a qualification date or second anniversary (asserted) |
| SF16 | hours worked | on the clock | twelve per shift | the clock-change nights move the bands | the prompt's "hours"; the 13 and 11 hour nights are on the clock (asserted) |
| SF17 | calendar quarter | UK quarters | UTC quarters | same figures | records converge: no ARS interval within two hours of a quarter boundary or clock change (asserted) |
| SF18 | a workstation-wide switch-off | applies to every sub-area of the workstation | one row, one sub-area | every cell moves | the row names the workstation, not a sub-area; each sub-area comes back on separately (asserted) |
| SF19 | the display renewal's cause | slips and the VDS-3 display faults | slips alone (8,173) | same call, but the figure moves (8,985 against 8,173) and so do five of the six workstation bars | the catalogue's B scope, "The VDS-3 equipment removed from every workstation.", with ToR 2.3: the faults of equipment the programme removes would not have happened; asserted that the sentence ships, that the figure moves without the faults and that the call holds |
| SF20 | switched off | every OFF row, the workstation-wide FAIL rows included | FAIL rows left out as failures, not switch-offs | every ARS cell moves (24 of 24) | the rows' own state column reads OFF; asserted that leaving them out moves the cells |
| SF21 | each workstation's sub-area hours | one total per workstation and quarter (6 by 4) | one row per sub-area (15 by 4) | the asks' table changes shape | "in total" in the asking sentence; every per-sub-area cell also sits at least 0.02 h from a rounding line (asserted, 60 cells, nearest 1.50 minutes) |

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | register incidents with OCF delay in the window | filed, ToR 2.2; C1 on OCF (every window incident carries it) |
| 2 Unit of account | the incident | the question and ToR 2.3 name it |
| 3 Attribution window | by occurrence, UK time | filed, ToR 2.2; C1, nothing within two hours of either end |
| 4 As-of dating | the review log as exported 6 October 2026 | filed, ToR 2.4 "as agreed"; Under review rows unapplied |
| 5 Version basis | the agreed review state | C1: every review reading keeps the call |
| 6 Denominator | rung 1 rates per manual request | not graded; the call does not divide |
| 7 Weighting | none: minutes add | the estimand is a sum |
| 8 Window length | twelve months | filed, ToR 2.1 |
| 9 Boundary inclusivity | 1 October to 30 September inclusive | C1, no incident near either edge |
| 10 Rounding path | whole minutes, integers throughout; hours and ARS to one decimal once | filed in the prompt; every graded cell at least 2.05 minutes from its edge (asserted) |
| 11 Tie-break | none needed | margins 2.35 and 2.38 times; no tied cells (asserted) |
| 12 Maturity and censoring | incidents in the window, minutes as attributed | ToR 2.4; under-review moves stay unapplied |
| 13 Order of operations | moves applied before the sum | C1: the sum is linear |
| 14 Row order | none | C1: no step reads file order |
| 15 Duplicate resolution | the log's server-change copies and the ARS copies are one event | C1 for the call (the log is not summed); the ARS merge is ask 2's device |
| 16 Identity normalisation | desk names to W numbers, old codes to new, route text forms to route identifiers | the systems' own crosswalks (layout export, category sheet) |
| 17 Netting against gross | moves out and in both applied | ToR 2.4 |
| 18 Dimensional units | minutes; hours | units in the headers |
| 19 Code and status semantics | category codes, finding codes, review statuses | the 2026-27 tool's category sheet; ToR 2.4 for statuses; never the stump |
| 20 Integerisation | whole minutes by construction | C1 |
| 21 Clause scope | ToR section 2 governs the choice, 2.5 the stage | filed |
| 22 Forward window contents | the 2027 programme removes the cause; no forecast is graded | retrospective quantity, reason in Draw |

## Literal reader

Executing the prompt and the terms of reference word for word: the programme whose cause produced the most of the
operating centre's delay minutes in the twelve months (ToR 2.1), over the register's OCF incidents by UK occurrence
time (2.2), counting an incident for a programme when it would not have happened had the programme been in place
(2.3), minutes from the attribution records after agreed moves (2.4), delivery from the stage removing the most
(2.5). Every reading of every term is a row of the fork table and lands on B at 8,985 or is ruled out by a quoted
clause; the easy answer (A at 8,240) comes from an easy method on the same literal estimand (trusting the recorded
finding as the but-for cause), never from another reading. The asks read literally: "hours each workstation was
worked by signallers then in their first two years since qualifying" is the as-worked hours by the date qualified
in the competence register; "each workstation's sub-area hours with automatic route setting switched off, in
total, in each calendar quarter" is the sum over each workstation's sub-areas of hours off inside each UK quarter.

## Oracles

None hands over the answer. The log's quick resets corroborate the slip set and are reached only by a sequence
analysis across a third file; no total, control or identity in the pack ties only under the golden; the catalogue
carries cost and delivery, never benefit; the workload assessment reports workload indexes and names no programme.
On the asks: the hours add to 8,760 a workstation under the golden and under every wrong route (staffing is
continuous), so the total is no referee; server B's copies reconcile to A's in count under every handling.

## Ask sheet

**Ask 1, hours worked by workstation and competence band (12 figures).** H18 home: the staffing record the Panel
may ask the case to extend to (ToR 3.2). Use: the operating centre manager's read of who works each desk. Primary
device D7 (the true key elsewhere): a whole-shift change made on the day reached the control system's sign-on and
never the changes list (two a workstation, each between bands, 24 hours median miss). Second device D7: relief
duties carry no desk in either roster; the log places them. Hazards: the clock-change nights of 13 and 11 hours
(D8), anniversaries inside the year, sickness covers cut on the half hour, two roster layouts. Files: both roster
workbooks, the changes list, the control log, the competence register (5 files, 14 columns). Stops: roster and
changes only (every cell off by about 24 hours); twelve-hour shifts (the clock nights); relief dropped. Realism:
the changes list is kept by the roster clerk from forms, and telephone swaps never reach it. Pin test: the asking
sentence pins the window, the band and "worked"; the device sits in which person worked, which no pin names.

**Ask 2, ARS sub-area hours off by workstation and UK quarter (24 figures).** H18 home: the ARS record ToR 3.2
names. Use: the timetable manager's read of where ARS is taken out. Primary device D8 (a clock): server B's
ARS process stamps Central European time into the `logged_utc` column, so its copies of A's events sit one hour
behind in winter and two in summer; merging the servers within seconds leaves every short interval counted twice.
Second device D1/D4: on A's monthly maintenance nights only B logged (32 rows, with users), so the master-server
read loses them. Hazards: old sub-area codes on each server until its own release date (D2), workstation-wide
switch-off rows (D6), quarters in UK time against a UTC log. Files: the ARS log, the layout export's crosswalk (2
files, 9 columns). Stops: merged at face value (every cell, 53 to 94 hours median miss); master server only (15 of
24 cells off); rows with a user only (every cell off by 3 to 5 hours). Realism: a supplier-installed server left
on its home time zone is a common control-room finding. Pin test: "calendar quarter" and "switched off" are pinned;
the devices sit in which rows are one event and what B's stamp means, which no pin names.

Main population zero-counts: no ask device row is in the call's population (the call reads the registers, the
delay records, the reviews and the layout's routes and signals; asserted by deleting every ask file).

| Hazard | Asks moved | Delta |
|---|---|---|
| clock-change nights | ask 1 | up to 1 hour per band where the two nights fall in different bands |
| old sub-area codes | ask 2 | every Q4 and Q1 cell, dozens of hours |
| workstation-wide rows | ask 2 | 34 drops, one to four hours a cell |

Referee: none; each handling is checked by its own recomputation in `generator/verify.py`.

| Ask block | The cracker (on the call; the battery, every filed rule, relief from the log, both servers merged, codes mapped, workstation rows expanded) | Kept | Verdict |
|---|---|---|---|
| Hours, first two years (6) | roster and changes for who worked | 0 of 6 | miss |
| Hours, everyone else (6) | roster and changes for who worked | 0 of 6 | miss |
| ARS off, October to December 2025 (6) | B's stamps read as UTC | 0 of 6 | miss |
| ARS off, January to March 2026 (6) | B's stamps read as UTC | 0 of 6 | miss |
| ARS off, April to June 2026 (6) | B's stamps read as UTC | 0 of 6 | miss |
| ARS off, July to September 2026 (6) | B's stamps read as UTC | 0 of 6 | miss |
| Full includer of every device the battery or a blank field shows | the same route | 0 of 36 | miss |

Partial includers (measured, not on the cracker sheet): both clocks handled but the day's changes missed keeps 24
of 36; the day's changes handled but B's clock missed keeps 12 of 36; the rows-with-a-user over-cleaner keeps 12.

Mirror leakage: 25.0 per cent of ask weight (the mirror off the call, on twelve-hour shifts and the master server,
keeps 9 of 36).

Pair ceiling: 35.4 (cracker 45.0 on the call, mirror 25.8 off it); 51.9 if both land the call with the mirror's
ask routes.

Measured by: generator/ceiling.py, run on the cut pack by `generator/checks.py` on every build.

## Gate answers at the stage 4 hand-off

`leak.py --asof 2026-10-09`: REVIEW, no LEAK. Each line, answered:
- Sweep 3, the terms of reference carry ten of the call sentence's words: they are the filed estimand's own words
  (2.1, "the programme whose cause produced the most of the operating centre's delay minutes"); no programme, no
  figure and neither "display" nor "renewal" appear in it. Harmless.
- Sweep 4, the terms of reference (register, incident, review, performance): the WHAT in the Panel's own genre;
  nothing names a slip, a distance, the drawing or the log's cancellations. Harmless.
- Sweep 4, the catalogue (signaller, competence, layout, Hatherby, screen, display): programme scopes in the
  operating centre's words; B's scope says the renewal redraws every screen's track layout on the new product,
  which is what a display renewal does and what makes the but-for clause true of the slips; it names no fault
  in the present drawing. Open for the reader and the judge: whether that clause points at the screens.
- Sweep 4, the workload assessment (signaller, routes, Hatherby, recorded, request, workload): a declared distractor whose
  genre is workload; it says nothing of wrong routes, slips or the display. Harmless.
- Sweep 9, the 2026-27 roster runs to 10 October 2026: a roster is a plan published before its period (file dated
  9 September 2026), so its last period ends after the as-of date. Harmless, on the forward-records allow-list.
- Sweep 12, the workload assessment names five header-like strings (Signaller, W01 Fenmoor, W03 Hatherby,
  Workload, Workstation): the consultant's own tables of workstations and time bands, not a note for the
  analyst. Harmless. The column names that had made three documents LEAK were generic export headers and keys
  (route, minutes, period, date, change, code, screen, workstation); they now carry the producing systems' own
  forms (route_id, pfpi_minutes, fin_period, duty_date, change_type, subarea_code, screen_no, wkstn).

`guard.py heart`: WARN, unchanged from the draw (driver.near 0.13 against two undrawn task307 entries;
repeat.question_form; the older same-puzzle and same-driver notes differentiated), plus one WARN read after the
final pull: repeat.deliverables, pptx and xlsx against task489, whose card took that set at its stage 4 hand-off
(16:25 UTC on 4 November), after this draw was registered (16:20 UTC); recorded, not a redraw (the question form,
the opener and the deck's role differ). `guard.py surface`: one
promoted pair, task398 against task399, back to back on two mechanism axes (decisive gap objective, decision type
root_cause_named), surface 0.017. The decisive rungs share nothing: task398 routes a pollutant through a
stratified lake to one intake depth; task399 re-classifies operators' recorded errors as slips by the drawn
geometry of two controls and the operators' own corrected selections. Both labels are the objective's ordinary
ones and neither is relabelled; the differentiation line is on the card, and the adjudicated read is the author's
call.

## Stage 4, pass 1: the judge's FIX_NOW and the reader's realism notes

The judge returned DETERMINISTIC with FIX_NOW: its derivation reproduced every committed answer before it read
the submission; the leak read was clean. The fixes, all in the generator, with no graded figure moved (every key
of `figures.json` the write-up grades is unchanged; the ARS raw cells moved by less than 1e-13 h):
- Step 4 claimed every route cancelled within twenty seconds and reset falls on a drawn-close pair; it is 357 of
  360. Reworded to "of the 360 routes cancelled within twenty seconds of being set, all but three were followed
  from the same entrance by a request for the exit drawn beside the one cancelled", the counts computed by
  `golden.quick_cancels` and asserted in `checks.py` and `verify.py`; the ladder paragraph above corrected.
- SF19 moved the graded figure, not only the call: the catalogue's B scope now carries "The VDS-3 equipment
  removed from every workstation." (a scope fact in the catalogue's own voice, naming no exit, distance or slip).
- SF20 and SF21 added; "in total" added to the ARS asking sentence; a clearing pass in `ops.py` keeps every
  per-sub-area cell at least 1.5 minutes from a line while every workstation total stays the same to the
  millisecond.
- Clock hours left literal, as the coordinator ruled.
- Realism: the catalogue now carries Word's own statistics, one company, a revision count, a reference block, page
  numbers and an approval block (Alan Pope, Helen Douglas, Jake Bray), and none of the writing template's
  extras (its thumbnail, the 2010 styles part, the bibliography stub); its 1980-01-01 part dates stay, which is
  what Word itself writes. The consultant's report is typeset in LaTeX (pdfTeX 1.40.25, PDF 1.5) with its own
  author and checker; the route's terms of reference stay on its office suite (LibreOffice 24.2, PDF 1.7).

## Tried and rejected

- 2026-11-04, draw, seed RC05's own pitfall (planned interruptions done de-energised, which leave no fault
  record): the costliest cause appears once the reliability standard's definition of an interruption is read
  correctly, so the decisive step is a definition (data semantics), banned.
- 2026-11-04, draw, electricity distribution: recloser lockouts turning transient faults into sustained ones
  (task198 H4 spent the completion route, and fast-trip conversion died as semantics in task188's fourth pass);
  lateral fuses switched from fuse saving to fuse blowing (task129, a dated cause an event study finds); shared
  substation supply losses (task303, approved); same-phase repeats at one point (task192); crew queueing on storm
  days (task198's queue screens); abnormal back-feeds during planned work extending outages (task194's tie flows
  are the same structure on water). The cell's drivers are spent and the world was moved.
- 2026-11-04, draw, Human Factors candidates set aside before this one: the interval since a worker last did a
  rare task, acclimatisation from the previous fortnight's shifts, and a handover splitting a task across two
  technicians (each is an exposure built from the worker's own consecutive records, task121's driver); interception
  by a later check (task275's approved driver); forklift impacts under tall loads and heat strain by the weather
  (a time join to a shipped key, readable); maintenance-induced failures after intrusive exams (a dated regime
  change an event study finds, and the post-exam window is one as-of join).
- 2026-11-04, draw, other Root-Cause cells: an airline's satisfaction against journeys broken by missed
  connections (the linkage is the step, task121 v4's death); a custody-rate rise read through the conviction
  offence (set aside in task121's architecture 4 screen); dispensing-cabinet selections onto look-alike drug names
  (tall-man lettering is the field's reflex for wrong-drug errors); coastal recirculation of a stack plume and a
  lake's internal phosphorus load (the receptor-routing abstraction task398 holds); the multilevel classroom cell
  (closed by task397's record).
- 2026-11-04, build, a third slide charting each month's minutes split between the cause and everything else: a
  split of the committed figure, banned as an ask (it measures the call twice), cut from the prompt.
- 2026-11-04, build, the first ask layer (relief desks from the log, the clock-change nights, anniversaries, old
  ARS codes, workstation-wide rows, the master-server reflex): every device is shown by a blank field or the hygiene
  battery, so the cracker on the call kept all 36 figures on paper; the day's changes missing from the changes list
  and server B's Central European stamps were added, each a judgment about which person or which rows are one event.
- 2026-11-04, build, the first simulation settings: the drawn-close routes evenly busy through the day and five or
  six on every workstation left the peak-hour rate, the starting workstation's lead and the eight-hour bound on
  noise (W04 led one seed, C's touched incidents passed B on eleven of 24); the peak-heavy December services and
  Hatherby's extra entrances made them hold in expectation.
- 2026-11-04, build, the competence register's "Qualified" header beside per-workstation competence dates read as
  a second meaning of "since qualifying": renamed "Date qualified" and "Competent" by workstation, a WHAT closed in
  the record's own form.
