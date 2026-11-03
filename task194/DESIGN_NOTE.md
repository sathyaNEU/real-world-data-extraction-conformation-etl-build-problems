# task194 design note

Architecture 17, drawn 2026-11-03. The slot keeps its number and its objective (Anomaly Detection &
Diagnostics) and leaves the healthcare provider-quality world for good after sixteen dead architectures
(lineage on the card, every death in `## Tried and rejected`). New client domain, world, dataset and
generator; no seed mechanism used.

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task194.json`, architecture v17, registered 2026-11-03 at WARN |
| Client domain / task type | Energy Systems & Utilities (`energy-systems-utilities`), `grid-reliability-outage-analysis` (serves RC and AD): a water distribution network's burst detection is network reliability analysis on a utility grid |
| Objective | Anomaly Detection & Diagnostics: a real event (a new burst) separated from artifacts that raise the same measurement (supply passed through an open boundary valve, a new night user, a pressure set-point change) |
| Decision | where Harrowgate Vale Water's one leak detection crew works in week 46 (9 to 15 November 2026): the district metered area whose own leakage rose most between the September baseline nights and the October comparison nights; pick one of the areas (`pick_one_of_n`), forward facing (the crew's coming week) |
| Shape | 07, a grid of cells: every area by its own leakage change, plus the asks' per-area figures |
| Gap / pattern / generators | `objective` then `population`; pattern `none`; `G10` cross-dimensional duplication decisive (one area's water metered on another area's inlet), `G3`, `G2` |
| Gate G | `decomposition_attribution`: each area's metered night-flow change split into its own leakage, its night use, its pressure and what passes through it to a neighbour |
| Strategy | `decomposition_attribution`; Layer 2 family `field_method`; pattern `own:night-flow-change-netted-across-areas-sharing-an-open-boundary-valve` |
| Forum, forcing event, org family | `line_manager_or_team` (the network operations manager allocates the crew), `shift_or_daily_cycle` (the weekly crew allocation), `local_government` (a municipal water department) |
| Role | the department's leakage analyst (`other`) |
| Context artifact | `filed_standard`: Leakage Procedure LP04 rev 3 (night flow conventions, the allowances, the pressure exponent, the crew rule) |
| Calibration | none |
| Personas | Kirsty Lloyd, Colin Ward (`guard.py names --geo uk --seed 194`) |
| WARNs answered | `repeat.question_form` (where): the decision is a place, so `where` is the honest form and `which` is over its quota; `shell.repeat` read off the dead architecture's prompt at register time, re-read at heart off the new prompt |

**Data-native sentence.** A district metered area is defined by closed boundary valves, and the record of
which valves are closed is the GIS's, not the street's: a valve opened to keep supply on during a repair and
left open makes one inlet meter carry part of the next area's demand and leakage, so the area's night flow
rises exactly as its neighbour's falls, hour by hour, while every per-area method in the procedure reads the
rise as loss.

**Abstraction sentence (written to be refused).** "The decisive quantity is a unit's own change, and part of
its metered change is a neighbour's quantity carried through a connection the record shows closed, recovered
by netting against the neighbour's simultaneous opposite move." No approved or delivered build carries it:
task303 nets a feeder against its siblings' same-minute tickets (a common upstream cause, same sign), task162
rebuilds net night flow under pressure-reducing valves (a pressure model), task182 reads each bore's own
lagged response to a shared driver. Nearest driver on file 0.07 (task199, task250 v1).

**Sources.** Fully constructed operating layer for a fictional municipal water department in England: the
SCADA historian export, AZNP pressure loggers, the area register, the billing account event log, large-user
loggers, works orders, a GIS valve export, the PRV set-point log, the procedure, and three distractors (rain
gauge, customer contacts, last year's find-and-fix jobs). Provenance in `metadata.json`.

## Default path

1. Read LP04: minimum night flow is the mean inlet flow from 03:00 to 04:00 local time; baseline nights 7
   September to 4 October 2026, comparison nights 12 October to 1 November 2026.
2. Map each area's inlet tags from the area register, convert l/s to m3/h, take each night's 03:00 to 04:00
   mean and average over each period's nights.
3. Remove household night use (registered household properties at 1.7 l/h) and non-household night use (the
   logged large users' consumption over the same hour, plus unlogged non-household properties at 6.0 l/h).
4. Normalise each period's leakage to the area's baseline AZNP night pressure with N1 = 1.15, the field's
   FAVAD correction LP04 files.
5. Rank the areas on the change in pressure-normalised net night flow; the crew goes to the top.

Ends on: Kestle Hill
Golden: Thrushgate

## Stump sentence

The procedure's own night-flow method, run correctly with every allowance and the pressure correction, sends
the crew to Kestle Hill, whose rise is Moorend Low's night demand and leakage arriving through Kestle Hill's
inlet meter by a boundary valve opened for a repair on 6 October and left open, when only Thrushgate's rise is
matched by no neighbour's fall and is a new burst.

## Three rules

Task type: `grid-reliability-outage-analysis` in `energy-systems-utilities`, which serves anomaly detection; a water distribution network's burst detection is the utility's network reliability analysis.
Domain test: the deciding quantity is each district metered area's own leakage change, which water loss management reads from minimum night flow net of legitimate night use and normalised to pressure through the leakage-pressure exponent (FAVAD), and which only means anything inside an area bounded by closed valves; swap in another field's nouns and the task stops making sense.
Swap: "send the crew to the ward whose own infections rose most, read from night admissions" keeps none of it: there is no night flow, no allowance for legitimate night use, no pressure-dependent leakage and no boundary valve that moves one ward's supply onto another's meter.
Layer 1: inlet tags in l/s and m3/h (the historian keeps each instrument's native unit); UTC timestamps across the October clock change (the historian); a stuck-at-last-value stretch and gaps (telemetry); billing accounts as an event log with posted and effective dates (the billing system); large-user registers as cumulative readings with meter exchanges and rollovers (the AMR head-end); works orders as parent jobs with child tasks and two asset-id formats (the works management system); the GIS valve status rather than the field status (GIS); an area renamed at the 2025 boundary change (the register); none placed to be caught.
Layer 2: `field_method` / decomposition: the metered night-flow change is split into night use, pressure, transfer to a neighbour and own leakage; the methodological choice that flips the call is netting each area's change against the simultaneous opposite change of the areas it shares boundary valves with.
Decisive step: recognising that a district metered area's inlet measures its own consumption only while its boundary is tight, and testing the boundary by netting each area's change against its valve-sharing neighbours' simultaneous changes, hour by hour over the whole day, before reading any rise as leakage.
Not semantics: every field, unit, tag and status read correctly (including the GIS status, which says closed) still leaves the procedure's per-area net night flow on Kestle Hill; no code, unit or definition read differently moves the call, and the valve's true state is in no column.
Not rule application: LP04 files the night window, the allowances and the exponent and nothing about boundaries, so executing every filed rule names Kestle Hill; the enumerated family (raw night-flow change, net of night use, pressure-normalised, per-property or per-km rates, the largest percentage rise) spreads over four different areas, Pellow Bridge, Calver Rise, Kestle Hill and a small area on percentages, and the standing family once the boundary is tested is one member (Thrushgate), the ruling-out done by a whole-day profile match that only a cross-area comparison shows.
Analyst test: a strong analyst who cleans every logger, converts every clock and unit, removes night use exactly as LP04 states and normalises to pressure with N1 = 1.15 ranks the areas on pressure-normalised net night flow change and sends the crew to Kestle Hill, the default path's answer.
Estimand: LP04 section 6: the crew goes to the area whose own leakage, the water lost from the area's own mains and service pipes at night, rose most between the baseline and comparison nights, in cubic metres an hour; filed in `leakage_procedure_LP04_rev3.pdf`.
No decoy: nothing is planted to be caught: no memo, draft, briefing or stakeholder figure carries Kestle Hill, the works order for the Moorend Low valve job reads as every job sheet does, and the open valve is an ordinary operational slip whose only trace is the flows themselves.
No certified replay: the method is not recovered by reproducing certified or published figures; no shipped figure is a leakage estimate for either period.
Lesson: a district metered area's inlet meter measures what crosses the meter, not what the area loses, so a night-flow rise is read as leakage only after the boundary has been shown tight, which on a record is the absence of an equal simultaneous fall in a neighbour; no build on file teaches netting a unit against its neighbours' opposite moves.

## Survivor anatomy

Actor: the deciding property (water crossing a closed-in-GIS boundary valve) has no column in any file; it is a relation between two areas' inlet series at the same quarter-hours.
Link: the signal is read through a comparison the field's method never asks for, one area's 15-minute increment against its valve-sharing neighbour's decrement over the whole day; the GIS export lists the valve pair with status closed, so the key exists but invites nothing.
Reflex: the field's named method (minimum night flow net of night use, pressure-normalised by FAVAD) sits at rung 0 to 2 and files Kestle Hill.
Back-test: the textbook route validates: Kestle Hill's rise starts on a single night and holds at a steady level as a burst does, its pressure is unchanged and its night use unchanged, so every per-area check a solver writes passes.
Second use: the inlet export carries the asks' daily supply and the main call; the GIS valve export is the department's asset record; the works orders carry the repairs ask; deleting the decisive step removes no file.
Shock: Kestle Hill's rise reads as an ordinary burst and Moorend Low's fall as the ordinary effect of a repair job on the same day; Thrushgate's rise is fourth on the raw change and is no sort's extreme.
Pins: LP04 files the window, the allowances, the exponent and the estimand (own leakage); no filed sentence names boundaries, valves, transfers or neighbours.
## Tried and rejected

- **This pass, the judge's FIX_NOW and the reader's one finding, closed in one generator pass.** The judge
  returned DETERMINISTIC with SOLUTION_WRONG on five write-up defects, Gates A to H all passing and F
  rated STRONG; the reader landed the call at about 45.1 against 44.6 and its question 6 read the decisive
  step as an analytical choice and said so, which is Gate H holding from outside the design. No input file
  changed a graded figure: the twelve avoidable counts, the margin, the gap, the rung winners and all 44
  ask figures are identical before and after, asserted by comparing the emitted `figures.json` across the
  pass.
- **The serious defect was a filter that read the lag index backwards, and it was in the code, not the
  prose.** `lags[q]` is the index of the publication the record holds for a quarter, so every quarter in
  it is still filling and index 0 is the shortest of them, held at its own coding close and nothing after
  it. `figures.json`, `checks.py`, `verify.py`, `build.py`'s own print, the brief and the workbook's notes
  all filtered on a positive index and so named the four most settled of the five and dropped the one that
  carries most of the answer: of the golden's 311.55 of uplift, the dropped quarter carries 166.33 and one
  of the four named carries 0.00. The count, the set and the per-quarter uplift are now emitted, asserted
  in `checks.py`, recomputed independently in `verify.py`, and stated in the write-up. **The lesson: a
  derived index whose direction is a convention gets its direction asserted, not commented, because every
  consumer of it inherits the same mistake from the same line.**
- **Four of the five per-quarter uplifts were edge-fragile at one decimal, which is why one recomputation
  read 11.7 where the code gives 11.6.** 2025-26 Q3's uplift is 11.64968, three ten-thousandths from the
  11.65 boundary, and the golden's own developed count and uplift sit 3408.54965 and 311.54965, each four
  ten-thousandths from a one-decimal edge. The development arithmetic is now stated to two decimals, where
  all seven figures clear 0.3 of the unit, and `checks.py` and `verify.py` both assert the edge distance.
  The avoidable counts stay at the one decimal the asking sentence states. **Rejected: stating the
  per-quarter uplift to whole complications or as whole-per-cent shares**; both are worse, 11.65 sitting
  0.15 from a whole-complication edge and 3.74 per cent sitting 0.24 from a whole-per-cent edge. The
  quantity cannot be re-centred, because unlike the graded count it does not run through the planned
  volume `centre_plans` moves.
- **Step 7's numeric range is gone rather than corrected.** It claimed "between 1.528 and 1.608 times"
  over an unnamed variant set; the judge measured its own eight variants at 1.530 to 1.608 and the
  shipped five gave 1.5277. Both measurements are honest and the lower bound sits 0.0023 from a
  two-decimal edge, so any variant set prints a different digit. The convergence set is now the eight
  readings the register actually leaves open, and the claim is the count that name the same unit, which is
  exact. **The lesson: a range over a variant set the write-up does not enumerate is a claim nobody can
  reproduce, and the fix is to claim the count rather than the bound.**
- **Two inverted sentences, both the same inversion in two places.** The Final Recommendation said 41220
  "falls to 27.8" when developing raises it from 26.1 to 27.8 and it loses the lead on rank, not on value.
  Critical Component 2 and the brief both said a quarter "carries 1.763 of its eventual count at its own
  close" when 1.763 is the multiplier from the close to the ultimate and the share at the close is its
  reciprocal. Both now state the direction as a multiplier, and `verify.py` asserts the brief contains the
  word "multiplied" so the direction cannot drift back.
- **"Cycle IP-11" existed only in the write-up, and the fix went in the pack rather than the write-up.**
  No shipped file carried the string: the placement register ends at IP-10, the cycle in progress, and
  `placement_cycle_notes.txt` headed the April 2027 cycle "IP-10" while its own body made IP-10 the
  January cycle. The judge recommended repairing the write-up to avoid voiding prior runs; there are none,
  so the notes now head IP-11 and `checks.py` asserts that the register ends at IP-10, that the notes head
  IP-11, and that IP-11 is not in the register of closed and in-progress placements. The notes' two bare
  ordinals are dates now ("on 24 March", "20 March, four days before the committee"), which was the
  reader's independent finding on the same file.
- **The reader's one finding: the close-out register's presence was the hint.** It read the file as having
  no use but to show how incomplete the recent counts are, which `leak.py` cannot see because it sweeps
  vocabulary and figures and never purpose. The fix is the announcement, not the decisive step
  (`build-pipeline`: a rung executed as a work order is announced). The register now carries what a real
  coding close-out register carries beside the two vintages: the episodes still awaiting a code at that
  close, the episodes coded since the previous close, the coder establishment allocated, and the standing
  reason most open codes sit under. The queue scales with the cost centre's volume and with the season the
  cycle notes already mention and carries no signal about how far a cost centre's coding has settled,
  which is measured rather than intended: no cut on any of the four new columns reaches F1 0.75 against
  the four shortest records, asserted. **Rejected: keying the queue to the lag depth**, which is what a
  real queue would do and which would have handed over the mechanism in a column.
- **`cis_registered_date` was decorative to the reader and load-bearing to the judge, which is the
  problem.** The reader called it a planted clue; the judge used its near-monotone relation to the
  development factor as the evidence that pooling the factors is a demonstrable error rather than a
  licensed alternative. Both readings were available because nothing in the write-up used it. Step 4 now
  names it as that evidence, so the rubric owes it and it is load-bearing rather than decorative.
  **Rejected: giving it a second use inside the register**, which would have coupled the rollout to the
  queue columns and undone the orthogonality the mechanism rests on.
- **Left alone on the judge's reading, against the reader's.** The dashboard's cell A2 ("Quarter-end
  position; not a projection of any later quarter") reads to the reader as a warning aimed at the solver
  and to the judge as what a real quarter-end dashboard says, with its 41210 figure of 218 matching that
  quarter's first publication exactly. The `leak-check` test settles it: the sentence would exist without
  the trap. The three distractors stay for the same reason, the cycle notes giving them an in-world
  purpose.
- **Charter 4.3 still carried architecture 2's open phrase, and that would have killed architecture 3 the
  same way.** The clause read "less the complications that patients of the same risk band and age band
  ordinarily have", which architecture 2 wrote precisely so the comparison frequency stayed open. But the
  comparison is one of the five parts of the estimand, architecture 3's whole premise is that it is filed,
  and the note and the card both said it was filed when the shipped text did not file it: a literal reader
  could still have answered "ordinarily have" with the record's own frequencies. 4.3 now reads "less the
  expected complications of the unit's episodes in that period under the current indicator specification",
  which routes to specification 3.1's defined term and from there to Appendix A, so the comparison is
  beyond argument and the only thing left open is the observation process. `checks.py` asserts the new
  clause, asserts that "ordinarily have" appears in neither document, and asserts that 3.1's defined term
  resolves to the published table. **The lesson: a part of the estimand the note says is filed is filed in
  a shipped sentence or it is not filed, and the way to find out is to grep the built document rather than
  to read the design.**
- **H9, found by set equality rather than by spot check: the decisive input was not in the export
  manifest.** `coding_close_out_register.csv` is the file the whole call rests on and the manifest, whose
  own row says it covers "every file in the folder", never learned about it. That is the exact shape the
  register warns about, the newly load-bearing file shipping unregistered, and it was invisible because
  nothing compared the manifest's names with the folder's. The register now carries a flat row in the
  manifest's own voice, and `checks.py` asserts manifest names equal shipped files both ways, that the
  manifest's self-row says what it covers, and that the dictionary covers the register.
- **H16, answered by allow-list rather than by repair.** One file carries a date after the 5 March 2027
  pull, `improvement_placements.csv` at 2027-03-31, which is the in-progress placement's scheduled end.
  That is a forward-looking validity window and legitimate, as is the April quarter's activity plan, so
  the two are an allow-list that `checks.py` now asserts; no other shipped file carries a date past the
  pull.
- **The readability claim was two sweeps reported as one.** The note said it swept for backlog, delay,
  restatement and the rest and found "four hits", then listed four flat column definitions, which do not
  contain any of those words. Both facts were true and the sentence joined them wrongly. Measured
  separately on the final pack: the signposting sweep returns zero hits across all 21 files, and the
  migration and vintage facts surface in five places, every one a statement of what a column or a file
  holds.
- **This pass, stage 2 finished for architecture 3 and four items closed.** The 23-reflex sweep was re-run
  on a fresh cut of the current mechanism and **none reaches the golden**, so the mechanism is not spent
  and the slot does not re-root. The golden's rung-0 position was re-measured at **5th of 12**, inside
  section 6.2's 4th or 5th, which the patient-driven lag could not reach. The twelve sections `precut.py`
  reads were rewritten from architecture 2's to architecture 3's; every figure in them is measured on the
  cut pack rather than carried over.
- **The mid-bin bar was being measured against the wrong unit and at half its height.** `sim.EDGE_BAR` was
  0.15 where the filed bar is 0.3 of the rounding unit, and `centre_plans` centred the avoidable count at
  whole complications while the asking sentence's unit is one decimal. Measured under the filed bar, 10 of
  the 12 graded avoidable figures sat inside 0.3 of a tenth and 4 of 12 inside 0.3 of a whole complication,
  so the defect was wider than the one figure the pause recorded. The bar is now 0.30 and the count is
  centred at one decimal: all 24 graded figures of the call clear it, the tightest at 0.0302 against
  0.0300. One decimal is also the only unit that survives the adjacent-entity rule, because at whole
  complications 41310 and 41420 print as 5 and 4 while sitting 0.56 apart, which does not exceed the
  printed unit.
- **Rejected: `EDGE_BAR` at 0.35 for headroom.** It is infeasible rather than expensive: the smallest
  candidate's planned volume can only move a few per cent, and inside that window no volume centres both
  of 41330's graded figures at 0.35 of a tenth. Centring at the filed 0.30 is what the volumes can carry
  without inventing a plan, so the bar is the spec's and the headroom is the 0.0002 the tightest figure
  has.
- **`pipeline.json` named the golden's hospital wrong and the error is corrected.** Its `call` and `stump`
  both read "Marrowfield General Medicine (41210)". Cost centre 41210 reports under H1, Alderbrook
  Hospital, throughout the record, which the register and the facility map both say; Marrowfield is H3.
  The golden and the runner-up are both Alderbrook units, which is worth saying out loud in the write-up
  because it is the kind of coincidence a reader checks.
- **A2 was re-sited over every unit at the site, which is what finally cost the cracker its last two
  figures.** Under the earlier siting A2 counted only the acute units' excluded rows, and Carrowdean's
  only acute unit among the twelve is a candidate, so no device could reach that site without moving a
  candidate's separations and the cracker kept both Carrowdean figures. `precut.py` had been shipping at 1
  FAIL on exactly that row with the author's acceptance. Counting the whole of a site's excluded activity
  brings in the sub-acute rehabilitation unit at Carrowdean, which the indicator does not cover and the
  call never reads, and the statistical discharge is then the device there. All 44 ask figures are now
  missed, the pair ceiling fell from 36.4 to **34.4** and the mirror leakage from 3.6 to **0.0**.
- **Rejected: a day-procedure feed gap on a candidate's same-day records at Carrowdean.** It is the
  obvious way to reach the site and it would have put device rows inside the call's own declared
  population, because specification 3.4 carries the excess on all of a unit's separations and a same-day
  record is one of them. The call would not have moved (every figure is computed from the shipped record,
  so a row absent from the extract is absent for the golden too), but the property that no device row sits
  in the call's population is worth more than the convenience, and it is the property that lets the asks
  be measured independently of the call.
- **Rejected: the predecessor cost centres as Carrowdean's device.** 41511 and 41512 were amalgamated into
  41510 on 1 October 2025 and the register carries them with a closed date and an into-pointer, which is a
  genuine imperfect-key hazard; but they close before A2's window opens, so they carry no 2026 separations
  and cannot reach the figure.
- **Dropping the third feed gap, measured rather than assumed.** With A2 counting every unit, the feed gap
  at Marrowfield's placed unit and the statistical discharges at Marrowfield's mental health unit ran in
  opposite directions and nearly cancelled: the site's naive read landed 5 separations and 1 complication
  from the truth, which is technically outside a whole-number bin and in practice a coin flip. The gap at
  that unit was removed, leaving Marrowfield one clean device at 302 separations. A theatre system
  migration at two of the four sites is as ordinary as at three.
- **The out-of-scope complication risk now runs with the length of the stay.** It was a flat 5.2 per cent
  on every episode the indicator leaves out, which put the expected number of statistically discharged
  stays carrying a complication at about four a quarter and drew zero in 2025-26 Q1, handing the cracker
  that one figure. Making the risk run with the stay is both the fix and the more realistic model, because
  a sub-acute stay of several weeks acquires pressure injuries and falls at several times the rate of a
  same-day separation, and it touches no in-scope episode so the call is untouched (verified: every graded
  figure identical to four decimal places across the change).
- **Two stale architecture-2 references in the ask layer, found by running it rather than by reading it.**
  `cracker.py` read `g["groups"]` where architecture 3's golden returns `groups_by_year`, and scored the
  mirror on `d["published_excess"]`, which no longer exists because the mirror now stops at rung 0 rather
  than at the published excess. Both were dead on the first run. The lesson for the rest of stage 3 is
  that every architecture-2 module is presumed stale until it has been executed against architecture 3's
  golden, not until it has been read.

- `precut.py` ships at 1 FAIL and the author accepts it, with the reason here rather than in a thread.
  The failing row is Part 1.1's cracker check on two of A2's eight figures, Carrowdean's, which both
  responses get right because Carrowdean District Hospital's only acute units are two of the twelve
  candidates, so the feed gap cannot reach the site without changing a candidate's separations.
  Buying them would need either a ninth placed unit at Carrowdean, which removes a candidate from the
  twelve, or moving the amalgamation date so the predecessor wards still report in 2026, which leaves
  one unit a single closed quarter against charter 4.2's floor of four. Both cost more than two
  figures are worth. The reason this is an acceptance rather than an override of a ship gate: Part
  1.1's "every row misses" ends "or the ask is rebuilt", which is a design-iteration instruction, and
  the ship bars are Part 7's two numbers, the pair ceiling at or under 40 and the mirror leakage under
  35. Both pass, at 36.4 and 3.6, and they already price the figure keep, because the figures the
  cracker takes are what drive the pair. Reading the prose as an absolute per-figure zero would make
  the pair ceiling redundant.
- And the standing caveat on that 36.4, in the author's terms: it assumes a ladder that keeps the
  second-best real response off the call, nothing independent has tested that yet, and if the cold
  reader lands the call the finding is in the ladder and no ask measurement will matter. task190 was
  retired today at a measured 38.1 for exactly that premise failing.

- Ranking units by the fall in their adjusted rate rather than by complications avoided: the charter would
  have to file a rate, and then the whole decision is a one-column sort on each unit's own standing, with the
  planned activity and the register idle. Dropped at the draw; the charter files complications.
- Giving the closed placements a hot quarter the placement was decided on (a selection shock of 0.15), so the
  register's own falls were inflated by reversion as well: it put the share a placement removes 10 per cent
  apart depending on whether the decision quarter stayed in the unit's pre-placement record, which is a fork
  on a graded figure. Replaced by placements decided on units' standing, with the decision quarter at the
  unit's own level (asserted), so the register prices the programme the same way under every reading of its
  pre-placement window.
- Block-correcting each unit's quarterly deviations so the trailing four, eight and ten quarter windows all
  returned the unit's level exactly: it left the panel with a lag-1 autocorrelation of -0.28, which licenses
  an AR(1) counterfactual below the unit's level and forks every figure. Replaced by one uniform shift per
  unit (autocorrelation -0.107 over 156 pairs, what de-meaning a ten-quarter record implies).
- A monthly reconciliation ask whose gap was the activity summary's own vintage: it needed the summary to be
  short for the acute units too, which breaks the referee the call's own reconciliation leans on. Replaced by
  A3 on the non-acute units, where the summary stays exact and the replay is the device.

- **This pass, the reader's and the judge's findings in one generator pass.** The judge's recomputation
  confirmed the structure and asked for four things; the reader found a data defect and a realism list. The
  register's ten readings were brought from a 10.75 per cent spread to 2.9 per cent by levelling the network's
  own quarterly position and holding the comparison units still across each placement's two quarters, with
  the two operations writing disjoint unit-quarters so they no longer undo each other, and by choosing the
  embed-quarter counts once on the narrowest reading band rather than twice on different objectives. What
  "avoided" means is filed as a difference between two counts in charter 4.3, the standing's window in
  specification 3.3, and the in-progress placement in charter 4.2. The shared-admission path recomputed the
  length of stay, so no episode now separates before it was admitted. Ask 1's basis is pinned in the asking
  sentence and ask 3's missing units are declared in `unit_register.csv`.
- **Rejected: grading the twelve per-unit figures as the effect-free excess** to take the register's reading
  out of them. The prompt would then have to ask for the complications a unit's planned activity carries
  above its own standing, which files the decisive step. Kept the avoided counts and centred each unit's
  planned volume so all twelve round the same way under every reading instead.
- **Rejected: a cross-site patient index collision as texture.** Two episodes in different hospitals shared a
  patient number and an admission date, which reads as one duplicated episode and puts ask 1's episode count
  in play. Issued the index in blocks by site instead, which is what a master index does.

- **This pass, the judge's SEND_BACK closed on the register rather than by filing a method.** The judge
  found three pricings of the embed defensible on a register that carried no sampling noise: its own fit was
  chi-square 0.006 on six degrees of freedom and the likelihood ratio over the constant-drop shape was 1.8 to
  1. The repair widened the closed placements' standing from a unit at its expected number to one at nearly
  twice it, which is what makes a share of excess and a constant drop predict different falls, and let the
  quarters before each placement and the assessment quarters carry their own scatter instead of being forced.
  The three competing shapes now sit 1.4e7, 2.0e4 and 2.1e4 to one against the register's own fit, measured
  and asserted. The charter files the baseline's population and window and nothing about the shape of the
  fall.
- **Rejected: filing the effect model in the charter**, which the judge offered. It closes the fork and
  spends the stump in the same sentence: with the shape filed, every remaining step is arithmetic the
  specification already prescribes.
- **Rejected: more closed placements at the same spread of standing.** Volume moves a chi-square linearly
  and the gap needed was two orders of magnitude; what moved it was the second constraint inside the record,
  the spread of the placements themselves, which is the lesson task190 landed on from the other side.
- **Rejected: the unweighted and expected-weighted means of the per-placement shares as readings that have
  to converge.** One closed placement was made with a unit running at its expected number, so it has no
  standing excess to take a share of; those two estimators cannot be formed at all, and the register's own
  structure is what rules them out rather than a sentence.
- **Rejected: the two-constraint levelling** (holding both the unweighted and the pooled movement of the
  comparison units flat). With placed units an order of magnitude apart in size, the slope it needs pushes
  small units down and large units up by 0.1 of a ratio across the panel. One pooled constraint, and one
  difference-in-differences reading rather than two, leaves every unit's own record where it was.

- **This pass, the two routes the coordinator found.** A solver who meets an undefined per-placement share
  drops that placement and averages the rest, and that route is formable. Measured on the previous pack it
  gave 0.50719 against a pooled 0.52947 and the expected-weighted version gave 0.55306, both outside the
  window the twelve counts allow (0.51834 to 0.53955), moving six of the twelve. Rather than narrow the
  route set, the placement that was running at its expected number was raised to a tenth above it, so every
  share can be formed and all eight routes are asserted. The price was paid on the fit, as offered: the
  constant-percent shape went from 2.7e5 to one down and back up to 2.7e5 to one once the register was
  re-searched, and the headroom improved rather than fell, from 4.5 complications to 6.6.
- **Rejected: keeping a negative per-placement share alongside the two mean routes.** A placement that shows
  a rise is the right texture, but on a placement carrying 16 complications of standing excess it moves the
  unweighted mean of the shares by about 0.011, which is a third of a bin on the answer against the slack the
  eight routes leave. The register keeps the scatter in the form the window allows: one placement at 0.022
  that took off almost none of the excess it was carrying, one at 1.232 that took off more than all of it,
  and standardised residuals from -0.92 to +0.84.

- **Architecture 1 is spent: the fitted-counterfactual family is closed for this slot.** Its decisive
  quantity was the fall a scarce intervention causes, read off a closed register of past interventions. The
  judge sent it back NOT_DETERMINISTIC on `competing_defensible_answer` with margin fragility, and the
  reason is structural rather than a shortage of data. A power on the standardised ratio, where observed
  equals expected times the ratio raised to g, fits the register at chi-square 3.34 on seven degrees of
  freedom against 3.30 for a share of standing excess: **a likelihood ratio of 1.02 to 1**, and it gives 19
  against 21 for the recommended unit with a gap of 7 rather than 8. Near a standardised ratio of 1 the two
  forms agree to first order and they diverge only at high ratios, so separating them would need placements
  at ratios of three or four, which no hospital unit carries. The register's own assessment quarters were
  also **under-dispersed at 0.47 per degree of freedom against 1.65 for the rest of the record**, about
  three and a half times too clean, so every likelihood ratio the build reported was inflated and fixing
  the dispersion makes the separation worse rather than better. Three of the eight pooling routes also
  moved ten of twelve counts once enumerated properly (the mean excluding one placement 0.765, the
  geometric mean 0.480, the mean with the baseline lagged a quarter 0.537). Both forms named the same unit,
  so the call was robust and only the graded counts were not. **The rule this slot now carries: a graded
  quantity is either measured from the record or it is not graded.** A fitted quantity needs a forced
  functional form, a functional form can only be forced by the data when the plausible domain separates the
  candidates, and that has to be checked at the draw by listing the forms a competent analyst would try and
  asking whether any two agree to first order over the domain the world allows.
- **Rejected at the draw: making the window of a unit's position the decisive step.** It is the obvious
  replacement once the fitted fall is gone, and it is dead on the `stumping` 1.2 screen: the window is one
  of the estimand's five parts, so filing it makes the computation follow from the clause and leaving it
  unfiled makes the call indeterminate. The latest-quarter trap stays in the build as a rung, ruled out by
  charter 4.3, and is not the decisive step.
- **Rejected at the draw: judging each unit's excess against its own sampling error.** Measured and in the
  domain, but the ways of accounting for the error (a Poisson limit, a shrunk estimate, an
  over-dispersion-adjusted funnel) are again a family of forms with a free parameter, which is the disease
  that spent architecture 1 in another dress.

- **This pass, the design point measured rather than targeted.** Four rounds on the built record. The
  separation opened by deepening the published table's staleness in the orthopaedic bands and raising the
  golden's own standing together, holding their product fixed so its published excess stayed at fourth:
  the golden's lead went from 7.33 complications, 1.45x and 1.19 standard errors to 15.05, 1.60x and 2.41.
- **Rejected: scaling the golden unit up to buy standard errors.** A unit's excess against its own Poisson
  error improves with the square root of its record volume, so the cheapest way to clear two standard
  errors was to make Alderbrook Orthopaedics a 2,500-separation-a-quarter unit. Ten thousand orthopaedic
  separations a year is not a real unit at a principal referral hospital. The separation was bought from the
  drift and the standing instead, which cost nothing in realism because both are already in the story.
- **Rejected: a charter clause filing the mix-insensitivity criterion.** The clean way to satisfy
  `determinism-check` section 1 was a clause saying a unit is not placed with because the patients it
  treated changed, so that a measure which moves on a mix shift violates a quotable sentence. It was drafted
  and dropped: with only two rate sets in the pack, a clause ruling one out selects the other by
  elimination, which is the HOW filed in a fairness voice. The forcing sits on the data instead, where the
  record carries it by a factor of 8.5.
- **Rejected: the first backfill story.** The case-mix shift that forces the rate set was built by moving
  the demonstration unit into SURG-MAJ, which in this DRG set is major bowel resection and coronary bypass.
  Two hundred and thirty of those a quarter inside an orthopaedics cost centre is not a hospital. Replaced
  by the orthopaedic theatre closing for ventilation works, elective joint replacement stopping and the
  ward carrying the hospital's emergency general surgical admissions, which is SURG-MIN, keeps the unit's
  volume flat as the mechanism requires, needs no second unit to change because the elective work was
  deferred rather than transferred, and still moves the published avoidable count by a factor of 8.5.
- **Rejected: claiming the published-ratio route and the latest-quarter route as ladder rungs.** Both are
  routes a solver takes, and both were measured, but their own first-to-second margins are 1.04x and 1.12x,
  under the 1.15x floor. A rung whose own winner is ambiguous is not a rung. They are recorded under the
  ladder as measured routes, and the ladder claims three rungs whose margins are 2.11x, 1.32x and 1.60x.

- **This pass, the ask layer measured rather than described.** The sheet was written from a script run on
  the cut pack, as the skill requires, and the first measurement came back at a pair ceiling of 50.0 with
  the cracker keeping 32 of the 48 ask figures. Building A3's statistical-discharge primary took A3 from
  20 of 20 to 0 of 20 and the ceiling to 40.4; giving the renal and Carrowdean medical units a case mix
  the published table's drift reaches took the mirror's construction leakage from 2 of 12 to 0 and the
  ceiling to **39.5**, with mirror leakage at **0.0**. Both gated figures are the worst honest
  measurement, as `supplemental-stumping` Part 7 requires.
- **Rejected, and it is structural: a silent primary for A2 as the ask is worded.** A2 is each hospital's
  adjusted complication rate over in-scope acute episodes, and those are exactly the episodes the call's
  comparison frequency is computed over. Four devices were drafted and all four die on the separation
  line. A cross-source duplication on a candidate's episodes sits in the main population. The same
  duplication on an embedded unit still shifts the network's own stratum frequencies, so it moves the
  call, which is the gravest finding in the book. A partial extract for one site makes the site's expected
  count unrecoverable, which law 6 forbids. A site attribution the summary cannot resolve makes the truth
  unrecoverable the same way. The conclusion is not that A2 needs a cleverer device but that **an ask
  computed over the call's own population cannot carry one**, and the fix is a redraw: take A2 to a
  quantity over all care types, where the same-day, ungroupable and non-acute episodes of the acute units
  are rows the call never reads and a device can live. Held rather than rushed, with the ask sheet saying
  A2 keeps 12 of 12 so the defect is visible instead of dressed.
- **Rejected: softening the cracker assertion so `checks.py` would pass.** The gate that fails is Part
  1.1's, every cracker row misses, and A2 does not. The assertion stays strict and the build's own checks
  fail on it, which is the state of the ask layer; the two gated figures carry the measurement rather than
  the favourable of two numbers.
- **The chain rule had to be made exact before it could carry A3.** Recovering a stay from the feed by
  chaining an episode onto one that ended the same day first over-counted by three (another episode of the
  same patient sorted between the two segments, so the chain broke) and then under-counted by one (a
  genuine same-day readmission under the same group looked like a split stay). Matching segment ends
  rather than adjacency fixed the first; regrouping the one episode in the record that was readmitted
  under its own group fixed the second. The rule now reproduces the activity summary's separations exactly
  in all ten quarters, which is law 6, and that is what makes the device fair rather than merely hard.
- **This pass, two consistency defects in the fiction's own history, found by reading the register against
  the charter it is governed by.** The register placed the team with Alderbrook Aged Care twice, in
  2023-24 Q4 and again in 2026-27 Q1, and nine closed quarters apart is inside charter 4.2's twelve, so the
  partnership's own record breached its own rule. No unit in the register can legally be reused, because
  twelve closed quarters after the earliest row is the quarter being decided, so the earliest cycle was
  moved to a unit that appears nowhere else: the Stonecreek sub-acute unit, placed with under charter
  version 2.0 before clause 2.3 put sub-acute units outside the indicator and before 4.2 limited
  eligibility to acute units. It adds texture rather than losing it, because the register now carries a
  cycle the current rules would not allow, and it cannot move the eligible twelve because a non-acute unit
  is excluded by service type anyway. The second defect: the register's in-progress cycle is IP-10, and the
  deliverables called the cycle being decided IP-10 as well. The placement for the quarter from 1 April
  2027 is IP-11.
- **The theatre closure leaves a trace a hospital would actually have, checked rather than assumed.** The
  case mix shows it loudly: elective joint replacements at 41410 run about 300 a quarter and fall to 63 and
  60 in the two closed quarters. Bed-days do not show it, because length of stay is drawn per unit rather
  than per procedure, so the unit's mean stay holds at 6.8 and 7.2 nights across the closure against 6.7
  to 7.3 elsewhere. The operational trace is therefore in the rostering file, whose coverage was widened
  from four quarters to six so it reaches both closed quarters: nursing hours per patient day at 41410 run
  4.49 to 4.66 in the ordinary months and **5.13 to 5.30 in exactly the six months of the closure**, with
  the agency share up by nearly half, because unplanned general surgical admissions need more nursing per
  patient day than an elective list and the roster had been built for the list that stopped. The file is a
  declared distractor and no graded figure reads it, so the trace corroborates the argument without
  entering the computation. **Open realism item for the next pass:** length of stay should follow the
  episode's risk band, not only the unit's mix, which would put the closure in bed-days too and would fix
  a joint replacement and an appendicectomy currently averaging the same stay. It was held because the
  stay feeds the complication selection, so changing it moves the realised stratum frequencies and would
  need the design point and the hospital-rate centring re-measured.
- **This pass, A2 re-sited off the call's own population, which is the rule the pass produced.** Ask of
  each ask which rows its quantity reads, and where the call reads them too, re-site the ask before
  building anything. A2 read the in-scope acute episodes, which are exactly the rows the comparison
  frequency is built from, so no device could live there; it now reads the complement, the 10,377
  separations in the calendar year that specification 2.1 to 2.3 exclude. The primary is the day-procedure
  feed's two missing months at three units the team has already been placed with, all of them same-day
  records, so it can reach neither a candidate's separations nor an in-scope episode, asserted both ways by
  count. A2 went from keeping 12 of 12 against the cracker to 2 of 8, and the pair ceiling from 39.5 to
  **36.4** with mirror leakage at **3.6**.
- **Rejected: the first wording of the re-sited ask, which signposted its own answer.** It asked for the
  separations a hospital's acute units reported, how many the indicator excludes and how many of those
  recorded a complication. Naming the reported separations points straight at the activity summary, which
  is the system that counts them, so a careful response reconciles to it and the feed gap costs it nothing:
  measured, the cracker kept all 12 and the ceiling went to 40.9. The reported column came out, and with
  the summary unnamed the natural path is to count the extract's out-of-scope rows, which runs short at
  three of the four sites. A reconciliation ask that names both sides of the reconciliation has given its
  answer away.
- **Rejected: buying Carrowdean's last two figures.** It would take either a ninth placed unit at
  Carrowdean, which removes one of the twelve candidates, or moving the amalgamation date so the
  predecessor wards still report in 2026, which leaves 41510 one closed quarter against charter 4.2's
  floor of four. Both cost more than two figures are worth, and the sheet says so rather than hiding the
  residue.
- **Checked, not assumed: the mirror's leakage is attempted and missed.** `cracker.py` now carries what
  each response computed beside what the rubric owes for every one of the 44 ask figures and all 12
  construction figures, and `checks.py` asserts that every scored figure carries a computed value and that
  the mirror's twelve construction figures are all attempted and all wrong. A figure scored as a miss
  because the response reached for nothing would show as a blank rather than hide inside a count.

- **Architecture 2 is spent, and the cause is a WHAT filed in the HOW column.** The decisive step was which
  stratum rates answer charter 4.3's comparison, and whose rates supply the expectation **is** the
  comparison, which `determinism-check` section 1 lists as one of the five parts of the WHAT the estimand
  must file so that its literal execution is the golden. Treating it as HOW is what produced the whole
  design: 4.3 was worded to say nothing about the rate set, the forcing was pushed onto the data, and the
  judge executed the clause word for word against the only stratum rates the package carries, Appendix
  A's, and got 41220 at 59.2 or 64.0 against the golden's 41230 at 40. Filing the comparison does not
  rescue it either, because the next lever down is the comparison pool, and the pool is part of the
  comparison's definition: all in-scope network episodes give 41230 at 40.1 against 25.0 while the twelve
  eligible units give 41420 at 21.6 against 41230's 9.8. Every remaining lever was a part of the estimand.
  **The rule for this slot and any other: before a decisive step is accepted, name which of the five parts
  it could be mistaken for, and if the answer is any of them, it is a WHAT and must be filed.** Population,
  outcome, window, unit and comparison, and the comparison includes both whose rates and which pool.
- **Also fixed on the way through: the one figure the judge could not reproduce.** The note claimed the
  candidates' surgical share runs 0.075 to 0.851, and nothing in the shipped files defines "surgical", so
  the judge got 0.000 for two units with 0.075 belonging to a third. The measure is now named where it is
  used, a risk band of `drg_risk_bands.csv` whose name begins SURG, and stated as running from exactly
  0.000, with two units carrying none, to 0.851, and from 0.075 among the ten that carry any. A range whose
  foot silently excludes the zeros is not reproducible however correct its arithmetic.
- **Held, not rejected: the maturity direction, and the habit the hold teaches.** `maturity_censoring` is
  banned against the last three draws and task469 is the immediate neighbour, so the direction is
  unavailable rather than unsound and the slot waits for the window to lapse. **The habit: look a strategy
  label's ban window up before spending design time on the direction, in the same breath as `guard.py
  mechanisms` and `coverage`, because the ban is deliberately not escapable by argument and a direction's
  availability is a fact rather than a judgement.** The design time here was spent after the direction was
  named and before the label was checked, which is the wrong order whoever names it.
- **Rejected: relabelling the mechanism to get past the ban.** The guard bans the strategy label, so a
  different label would have passed it silently. The mechanism is maturity: a count for a fully observed
  population is still accumulating and the development is an observed ratio between two vintages. Any other
  label would be a false entry in the card, which is worse than a blocked draw, because the card is what
  guards every other build and what the clone screen reads.
- **Architecture 3 measured at stage 2 and stopped on a bound, before a ladder number was written.** The
  machinery works: the close-out register ships, the development factors are read back from its own bytes,
  the immature quarters are identified from the register alone, and all five readings of the development
  name the same unit. What fails is the ladder arithmetic, and it fails on a bound rather than on tuning.
  **The bound.** A development-flip ladder has to pay for two separations out of one budget, the uplift the
  immature quarters carry. Separation 1 is the flip: the golden must sit below rung 0's leader on the record
  as it stands, or the easy route names the golden and there is no stump. Separation 2 is the margin: the
  golden must lead once the quarters are developed. The uplift pays for both, and nothing else can, because
  on the record as it stands the golden is behind by construction. **Measured on the cut pack at the best
  point found:** the golden (41210 General Medicine) carries an uplift of 235.3 complications, which is
  **27.25** in the figure's own units. The flip comes out at **2.35 complications, 1.50x, and 0.32 standard
  errors**. The margin comes out at **16.03 complications, 2.008x, and 1.75 standard errors**. Together
  they spend 18.38 of the 27.25 available, and clearing two standard errors on each would take
  **33.14 against a 27.25 budget**. The architecture is short before any room is asked for, and the point
  that clears the margin does it by spending almost the whole budget there, leaving the flip inside the
  noise. That is architecture 1's fragility in another dress: there two functional forms fitted at 1.02 to
  1, here the thing that separates the easy route from the answer is a third of a standard error.
  **Why tuning cannot fix it.** The two separations trade off directly: pushing the golden further below
  the leader on the record means a smaller recorded ratio, which cuts the developed excess the margin is
  measured on. Both are measured in the same Poisson error of the same counts. **Why scale cannot fix it at
  unit scale.** The budget grows with the count and the error with its square root, so the budget closes at
  about twice the top units' volume for a bare two-and-two and four times for room: 30,000 to 60,000
  separations a year in one cost centre, which is a whole hospital rather than a unit. The relative-distance
  floor is not the one that fails, and that distinction matters: the flip clears a nearest-wrong-cell test
  easily at 1.50x and fails the sampling-noise test at 0.32 standard errors.
  **What is not wrong with it.** The estimand stays filed in all five parts with the published table as the
  comparison, the open step stays the observation process, and the WHAT screen passes. The design is sound
  and the ladder it can carry is not.
- **Correction to the line above, and it matters: the bound was measured against a bar this repo does not
  set.** There is no two-standard-error rule in the skills. What is filed is a rung margin of 1.15x, a final
  margin of 1.2x with a 1.5 to 2x target (`dataset-generation` 6.2) and a nearest-wrong-cell floor of 6 per
  cent (`determinism-check` C4), and architecture 1's lesson was not about sampling noise at all: there the
  graded counts were a fitted counterfactual and two functional forms the record admits were collinear, so
  the answer turned on a choice the data could not settle. Nothing is fitted here. The development factors
  are ratios read back from the register's own shipped bytes and all five readings of the development name
  the same unit, so the golden is determinate from the shipped files. **Against the floors that are filed,
  the measured point clears with room:** rung 0 separates at 1.50x, the intermediate rung at 1.23x, the
  decisive rung at 2.008x. One real deviation stands, that the golden sits 2nd of 12 on rung 0 where 6.2
  asks for 4th or 5th, and that is the bound's doing: the flip is paid for out of the uplift, so the
  further down the record the golden sits, the less of the uplift is left for the margin.
- **Architecture 3 is spent, and on the reflex rule rather than on any separation.** `stumping` is explicit
  that every reflex an opponent reaches for must file the default or another named wrong answer, and that a
  reflex reaching the golden spends the stump. Twenty-two reflexes were run on the record as it stands, on
  409,336 in-scope acute episodes: pool and aggregate scale, credibility weighting at four strengths and by
  empirical Bayes, stratification on each visible attribute, a site control, a volume control, trend and
  recency, ratio against difference and rate against count. **Six of the twenty-two reach the golden**, and
  the worst are not close: standardising on risk band, age band and length of stay band names it at
  **3.47x**, on length of stay alone, on risk band, age band and comorbidity band at 1.30x, on risk band,
  age band and site, the excess net of its own site's mean excess, and credibility weighting once the prior
  is strong enough. **The cause is a confound, not a tuning failure, and it is real rather than an
  artefact.** The lag's depth was made to follow the complication groups a unit's patients produce, and
  pressure injuries and delirium are produced by old, comorbid, long-staying patients. Those are exactly
  the patients the published table under-adjusts for, because it standardises on a risk band and an age
  band and nothing else. So the attribute that makes a unit's record late is the same attribute that makes
  its excess rise under any finer standardisation, and an opponent holding the pool to every visible
  attribute arrives at the golden without doing the maturity analysis at all. Within this mechanism the
  deep-lag units are all medical and aged and the shallow-lag ones all surgical, so no other choice of
  golden escapes it. More volume cannot help, and nor can a deeper lag: both make the confounded reflex
  stronger, not weaker.
- **Priced anyway, because it was asked for: the lag lever works arithmetically and is not needed.** The
  uplift budget is set by the completeness profile's depth and reach and the noise by the counts, so they
  are separable: deepening the profile over the four lags already modelled, from the golden's d of 0.079 to
  about 0.16, doubles the budget from 27.25 to about 55 while the counts and the standard errors stay
  exactly where they are. At the depth actually built, pressure injuries 43 per cent complete at a
  quarter's own close and 93 per cent four closes later, the backlog is one a network could document: a
  retrospective staging and audit programme running three quarters behind is ordinary. At the depth the
  doubling would need, 25 per cent complete at the close, it is at the outer edge and the realism sweep
  would be right to query it. Either way the lever is moot, because the bar it buys is not the bar that
  failed.
- **The mechanism that survives the reflex test, for the next pass.** Keep the strategy, the estimand and
  the open step exactly as they are, and move the lag's driver off the patients and onto the documentation
  path: a site or a ward whose complications reach the warehouse late because of where they are recorded,
  not because of who the patients are. That breaks the confound in both directions, since finer
  standardisation on patient attributes no longer touches the signal, and the site control, which an
  opponent reaches for, nulls it and lands elsewhere. The pack already carries the organ, one hospital's
  wards being off the clinical information system.
- **Superseded, and recorded because the earlier line overstated it.** The line above saying that within
  the patient-driven mechanism "no other choice of golden escapes it" was true of that driver and is not a
  statement about the strategy. With the driver moved onto the documentation path the same golden, 41210,
  is reached by none of the 23 reflexes, and the deep-lag units are no longer all medical: they are
  general medicine, general surgery, orthopaedics and renal medicine at three hospitals.
- **Rejected: making the registration date carry the depth.** The first cut of the approved mechanism gave
  the four deep-lag cost centres registration dates in 2027 and everyone else dates in 2022 to 2024, so
  each unit's recording mode was constant across the window and its development factors were cleanly
  identified. Grouping the register on the year of registration then isolated the four exactly, F1 1.00,
  which is the marker condition 2 forbids. Spreading the dates across the window instead would have put a
  mode change inside the graded window for several units, whose own finished quarters would then measure a
  factor that over-develops their short ones by up to 12 complications: a defensible pooling and a
  different number, which is a fork on the supplemental figures. Both were dropped in favour of
  `CIS_ADOPTION`, a ward-level property that is constant across the window, so the factors stay identified
  while the depth and the date come apart.
- **Rejected: arguing the two surviving reflexes rather than closing them.** The length-of-stay
  standardisation conditions on a consequence of the complication and the collapsed empirical Bayes
  estimator is not an estimator anybody would file, so both could have been written up as not real
  routes. A measurement that fires is not answered on paper; both were closed in the generator instead,
  by crowding the golden's peer group and by separating the two largest units' expected volumes.

### Architecture 4: two candidates, both killed by 1.6a's hard clause before design (2026-10-18)

Architecture 3 died because the completion method was not forced, so the decision was robust and the
graded figure was one of six values. `stumping` 1.6a now requires the construction to be **uniquely
determined by the data's structure**, and its test is one computation run before the six screens:
enumerate the variants a competent analyst would use and compute the graded figure under each.

**Candidate 1, each unit's own complication propensity identified from patients who pass through several
units.** The quantity is unobserved (a unit's propensity net of the patients it happens to get); the
construction combines the unit-stay segment grain with the separation outcome grain and absorbs a patient
effect, which is the closest thing on this ground to task197's forced least squares. Measured on the clean
truth, 13,403 segments over 9,000 patients with 45 per cent multi-unit:

| Variant | Names | Graded figure, per 100 separations | Prints |
|---|---|---|---|
| ordinary least squares, two-way | unit 3 | 18.32 | 18.3 |
| weighted least squares by stratum | unit 3 | 16.88 | **16.9** |
| ridge-shrunk unit effects | unit 3 | 18.28 | 18.3 |
| heavier shrinkage | unit 3 | 17.96 | **18.0** |
| multi-unit patients only | unit 3 | 18.32 | 18.3 |

**The name agrees and the figure does not: three printed values at one decimal.** That is architecture 3's
death exactly. And a second kill on top: the filed-strata excess route, which is the published method the
pack has to ship, **already names unit 3**, so the standard risk-adjustment route is the golden and only
the raw rate lands wrong.

**Candidate 2, the true complication count behind incomplete coding, recovered from a coding audit.** The
quantity is unobserved; the construction combines the audit's re-coded-separation grain with the register's
separation grain. Measured on 17,340 separations with a 6 per cent audit:

| Variant of the scale-up | Names | Figure | Prints |
|---|---|---|---|
| one detection ratio for the book | unit 7 | 8.79 | 8.8 |
| each unit's own audited ratio | unit 7 | 10.34 | 10.3 |
| detection by risk stratum | unit 7 | 8.81 | 8.8 |
| the audited rate direct | **unit 3** | 13.64 | 13.6 |
| mean of per-stratum ratios | unit 7 | 8.74 | 8.7 |

**Worse than candidate 1: the name forks too**, four variants naming unit 7 and one naming unit 3, with
four distinct printed figures.

**Why this ground cannot satisfy the clause, which is the finding rather than the build.** The dichotomy
and 1.6a close against each other here, and it is a property of the data type.

- Anything recovered by **arithmetic** on these records (interval containment of an onset in a unit stay,
  patient-days by unit, set arithmetic over a person key) is **observed** in the dichotomy's sense, because
  the records fix it. Filing it makes the computation executable, so the step is rule application.
- Anything genuinely **unobserved** here is a **rate**: a true rate behind incomplete coding, a unit's own
  propensity net of case mix, a counterfactual count. Every rate estimator on small counts across
  heterogeneous units carries a weighting choice (pooled or per-unit, which strata, ratio of totals or mean
  of ratios) and a shrinkage choice (fixed or random effects). All are standard practice and all move the
  graded figure, as both tables above measure.

**task197 escapes because of its data type, not its cleverness.** Its construction fits a dense physical
trace where the residual is measurement noise and no competent analyst would weight or shrink it, so least
squares returns one answer. Provider quality has no dense deterministic signal; it has sparse counts over
units, which is exactly the setting where weighting and shrinkage are both defensible. **So 1.6a's hard
clause is a constraint on the data type as much as on the mechanism: a uniquely determined construction
needs dense observations of one unit, not sparse counts across many.** That is the question to put to the
author rather than spend a ninth number on it.

### Architecture 5 candidate A, measured twice, and a refinement the test needs (2026-10-18)

**Candidate A, the unit that held the patient when the complication began.** The record charges a
complication to the separation that reported it, which is the discharging unit, while the only record of
which unit held the patient at onset sits in a movement file at a finer grain. The construction is interval
containment: records-fixed, an integer, no weighting and no shrinkage in it. Driver similarity **0.06**,
with task48, task103 and task184 not in the top five, so the driver is distinct from the three grain
builds on this objective even though the shape is shared.

**First parameterisation (short segments, an extreme golden unit).** The figure printed 24.0, 28.2 and
30.0 across the boundary conventions, with 8.5 per cent of onsets on a transition day, and **all four
rival routes named the golden**, because a unit with a propensity of 0.072 against a pack at 0.027 tops
every attribution rule. That second failure was mine, not the shape's.

**Corrected parameterisation: the golden unit sits mid-spell, so no positional rule charges it, with
longer segments cutting boundary onsets to 3.16 per cent.**

| Variant of the construction | Names | Count | Rate per 100 segments | Prints |
|---|---|---|---|---|
| containment, transfer day to the arriving unit | unit 3 | 532 | 10.545 | 10.5 |
| containment, transfer day to the departing unit | unit 3 | 517 | 10.248 | 10.2 |
| containment at midday | unit 3 | 532 | 10.545 | 10.5 |
| boundary onsets dropped | unit 3 | 510 | 10.109 | 10.1 |

| Rival route | Names | Verdict |
|---|---|---|
| the discharging unit (the easy route) | unit 7 | lands wrong |
| the admitting unit | unit 0 | lands wrong |
| the longest-stay unit | **unit 3** | **reaches the golden** |
| pro-rata by custody days | **unit 3** | **reaches the golden** |

**The real kill is the sixth screen, not the uniqueness clause.** Longest-stay and pro-rata reach the
golden because **a unit with a high propensity makes the spells it touches eventful**, so its signal is
published at the spell level and no onset containment is needed to find it. Breaking that means making the
golden's presence uninformative about a spell's event count, which is the quantity that makes it the
answer. Seventh instance of one number on both sides.

**The refinement the uniqueness test needs, and it matters beyond this build.** The figure forked at
10.1, 10.2 and 10.5 on the **boundary convention**, and a boundary convention is not a method family. It is
closure axis 9, inclusivity, which `precut.py` requires filed and which every shipped build files. So that
fork is legitimately closed by a sentence at authority, unlike architecture 3's chain-ladder variants,
which are a method family and may not be pinned without turning the step into rule application. **Run the
uniqueness test on the variants that are methods, not on the conventions the closure table already
requires closed, or it rejects every construction involving an interval, which is most of them.** Stated
as a test: if pinning the varying choice is something the closure table demands anyway, it is a convention;
if pinning it would make the decisive step executable, it is a method and the fork is fatal.

**So the objective question is premature on this evidence.** Candidate A died on the sixth screen with its
conventions legitimately closeable, not on 1.6a. Candidate C, a construction over orderings, scored the
cleanest driver of the three at **0.05** and has not been tested.

### Architecture 5 candidate C, killed by the sixth screen on volume proxies (2026-10-18)

**Candidate C**, the count of complications whose coded onset precedes the patient's arrival at the unit
charged with them: records-fixed, an integer, no rate and no denominator anywhere, driver 0.05. Built to
the author's caution with **every unit on the same daily propensity**, so no unit makes the spells it
touches eventful and the signal lives only in position within a spell. Sixth screen run first.

| Route | uniform hazard | front-loaded hazard |
|---|---|---|
| the construction (onset precedes arrival) | unit 0, count 1,703 | unit 0, count 1,556 |
| pre-arrival patient-days, movement file alone | **reaches it** | **reaches it** |
| spells discharged | **reaches it** | **reaches it** |
| total complications charged, the reported route | **reaches it** | **reaches it** |
| mean segment length | **reaches it** | **reaches it** |
| mean arrival day within the spell | unit 6, lands wrong | unit 6, lands wrong |
| own-onset containment (candidate A) | reaches it | unit 9, lands wrong |

Reflex sweep: discharging, longest stay and pro-rata all reach it; only the admitting unit lands wrong.
**Four routes reach the golden without building the ordering, under both hazard shapes, and the worst of
them is the reported route itself**, so there is no stump at all.

**Why, and it is the eighth instance of one number on both sides.** The quantity is a **count**, and a
count across units of different size ranks on **volume**. Unit 0 discharges the most spells, so it has the
most charged complications, the most inherited ones, the most pre-arrival patient-days and the longest
segments. Every volume proxy in the pack publishes the answer. This is the size tell that killed task57 at
a correlation of +0.98, arriving through the one property that made candidate C attractive: being an
integer with no denominator. **Normalising the count would fix it and would reintroduce a denominator,
which is the weighting freedom that killed candidate 1 and architecture 3.** A count is published by
volume; a rate needs a denominator and a denominator is a choice.

**What the corpus says to do instead, and it is a decision-type finding rather than a quantity one.** None
of the coarse ships on this objective answers a per-unit league table:

| Build | Decision type | Answer unit |
|---|---|---|
| task48 | `designation_set` | set of items |
| task103 | `go_hold_or_stop` | currency |
| task184 | `ranked_slate_under_cap` | set of items |
| task192 | `quantity_figure` | count |
| task188 | `pick_one_of_n` | named option, but its density's pooling is fixed by the group sizes |

`pick_one_of_n` is 13 of the 32 builds on this objective, the most common decision type, which is why the
objective keeps meeting this wall: **a pick-one-of-N over units of different size forces a per-unit
quantity, and a per-unit quantity is either a count that volume publishes or a rate whose denominator is a
weighting choice.** The coarse ships escape by answering a set, a slate, a hold or one population figure,
where no cross-unit comparison of heterogeneous sizes is made at all. task188 is the single exception and
it escapes the other way, through a pooling the design fixes.

**So architecture 6 should change the decision type, not the quantity.** This world supports a designation
set (which complications or which units enter the improvement programme), one population figure (how many
of the partnership's complications were avoidable) or a hold (whether the placement is funded at all), and
each escapes the volume leak by construction rather than by tuning.

### Architecture 6: a designation set against a filed tolerance, both cheap screens passed (2026-10-18)

**Shape**, taken from the three designation_set ships (task180, task181, task193) after reading them
rather than reasoning about them. Which clinical units the partnership designates for the 2027 Q4
improvement programme, each judged against the charter's filed tolerance of avoidable complications per
1,000 separations. Following task181's escape, the exposure the complications actually scale with is **not
filed**: they arise at care handovers, not per separation and not per bed-day, and the activity plan
reconfigures pathways so handovers and separations move differently.

**The structural advantage, measured rather than assumed.** Membership is decided per candidate against a
fixed tolerance, so there is no cross-unit comparison of heterogeneous sizes for a volume proxy to publish,
**and the tolerance fixes the denominator, so no weighting is free.** The measured contrast is the point:

| | Result |
|---|---|
| designated set across five estimator variants | **one set, [1, 3]**, identical under every variant |
| unit 1's printed rate across the same five variants | **28.4, 28.6, 28.7, three distinct figures** |

So the weighting freedom that killed candidate 1 (16.9 / 18.0 / 18.3), architecture 3 (36.6 to 49.0) and
candidate A (10.1 / 10.2 / 10.5) is still present and **does not cross the tolerance**. A designation set
discretises it away. That is why `designation_set` is 3 of the 9 coarse ships and 0 of the 5 pauses.

**Sixth screen, run first: passes.** The golden set is [1, 3], 2 of 14.

| Rival designation route | Set | Verdict |
|---|---|---|
| current count scaled by separations | empty | designates nobody |
| current count scaled by bed-days | empty | designates nobody |
| current observed rate, no projection | empty | designates nobody |
| current count carried forward | empty | designates nobody |

All four easy routes designate **nobody**, which is task180's own shape, where the analyst files that no
unit goes over. Of nine single sorted columns, eight differ (planned separations [0,2]; planned handovers
[1,2]; handovers per separation [1,9]; current rate per 1,000 [0,3]; current per-handover rate [0,8]; and
so on). The one that reproduces the set is **the construction itself**, the per-handover rate times
handovers per separation, which is the answer computed correctly rather than a leak.

**Uniqueness on methods, per the convention-versus-method clause: passes.** Each unit's own ratio of
totals, shrinkage halfway to the pooled rate, a James-Stein style shrinkage by counts, a Poisson maximum
likelihood with a continuity term and a rate pooled over the prior two quarters all designate [1, 3]. One
distinct set.

**Three test-design errors of mine, caught and corrected in the same pass, because the pattern matters
more than the instances.** First, the per-handover rate was uniform across units, which made the golden
rate exactly proportional to handovers per separation so that one column reproduced the set; the rate now
varies by unit. Second, the uniqueness table's first row passed the **true generating parameter** rather
than an estimate, so it was the oracle and not a variant, and I had reported a disagreement that did not
exist; the five genuine estimators agree. Third, the set test used a top-k sort with k of 10 out of 14,
which any correlated column satisfies, so the test could not discriminate; raising the tolerance to a
two-unit set made it bite. **Three times tonight I have built a test and read its artefact as a finding.**

**What has not been run.** Only the two cheap screens are done. The pincer and the dichotomy, the move
available against the move needed, the standard error of what the construction must estimate, and the
lever against both the ranked quantity's noise and the unit's own history are all outstanding, as are the
reflex sweep's filed-strata route and the readability screen. Two specific risks to settle there: the easy
route designating **nobody** means the prompt must not make an empty answer implausible on its face, and
Gate B requires the handover data shipped while nothing may name handovers as the exposure.

### Architecture 6: the three Gate B tests, all passed (2026-10-18)

Run before the remaining four screens, because Gate B is the test that could unmake the shape.

**Test 1, does anything shipped connect complications to handovers: PASSES.** Every csv, txt and pdf in
the pack grepped for handover, hand-over, transfer, transferred, moved between, ward move, pathway,
step-down, inter-unit and between units. **Two hits, both innocent:** `activity_plan_2027q4.csv` records
an "elective general surgery list transferred in from Marrowfield", which is a service reconfiguration
fact about workload, and `data_dictionary.csv` describes `amalgamated_into` as the "cost centre the unit's
activity transferred to on closure". Neither says anything about what explains a complication. **Both PDFs,
the charter and the specification, have no hits at all.** And `episode_outcomes_extract.csv`'s `unit_code`
is documented as "cost centre of the unit the episode separated from", so the shipped record attributes at
the separating unit, which is the easy route, with nothing pointing past it.

The rule the new file must follow, stated so it is not rediscovered: its column descriptions say what a
row **is**, never what it explains.

**Test 2, the sixth screen on the handover file itself: PASSES.** Nine columns the file affords, plus the
two rate columns the pack already **publishes**, which are zero-work routes and so the most dangerous.
Golden set [1, 3].

| Column | Top-2 | Verdict |
|---|---|---|
| handovers alone, planned | [1, 2] | differs |
| handovers alone, current | [2, 9] | differs |
| handovers per separation | [1, 9] | differs |
| handovers per bed-day | [1, 7] | differs |
| distinct receiving units | [3, 6] | differs |
| share of separations with a handover | [1, 9] | differs |
| growth in handovers | [1, 4] | differs |
| **published `standardised_ratio`** | [0, 3] | differs |
| **published `adjusted_rate_per_1000`** | [0, 3] | differs |

**None reproduces the set.** Better than expected on the empty-answer risk: the published
`adjusted_rate_per_1000`, used directly against the tolerance, designates **{0}**, a named wrong unit
rather than nobody. So the easy route gives one false positive and misses both true members, which is a
stronger rung than an empty set and lowers the prompt risk that worried me.

**Test 3, the single-use test on the movement log: PASSES, with evidence rather than reasoning.**
`episode_outcomes_extract.csv` holds **465,882 episodes** against `activity_summary_monthly.csv`'s
**463,691 separations**, a gap of **2,191**: the two files already differ in grain and in count, and a
movement log is the file that explains the gap. The existing architecture already asks about exactly that
reconciliation, so the log has an ask-side use in this world before the call touches it. Five further pack
files it would serve are present: `activity_summary_monthly.csv`, `nursing_hours_by_unit_monthly.csv`,
`hospital_sites.csv`, `unit_register.csv` and `quality_dashboard_2026q2.xlsx`. **The binding requirement
for architecture 6: at least one ask must actually consume the log, and the episode-versus-separation
reconciliation is the one to use.**

**The empty-answer device, read from task180's prompt rather than invented.** Its grammar licenses the
negative: "Will the new borehole networks put **any** of our five geothermal plants over the traffic-light
amber in 2027, **and if so which** and in which quarters?" A whether-first question with a conditional
which, so "none" is an ordinary outcome of the question's own form. Architecture 6's prompt takes the same
shape, and its easy route designating {0} rather than nobody means the device is a safeguard rather than a
load-bearing part.

**Still outstanding, and the sweep is not complete.** Four of the six screens (the pincer and the
dichotomy, move available against needed, the standard error of what the construction estimates, lever
against the ranked quantity's noise and against the unit's own history), the readability screen, and one
reflex I have not run: the **filed-strata excess** route, which `episode_outcomes_extract.csv` supports
directly through its `comorbidity_score` and `drg_code` columns. That route reached the golden in
candidate 1 and it has not been tested against a designation set.

### Architecture 6, killed by the filed-strata excess reflex through the pack's own published ratio (2026-10-18)

Run before the four remaining screens, on the instruction that one computation is cheaper than five. The
route: take `episode_outcomes_extract.csv`'s `comorbidity_score` and `drg_code`, build the stratum mix per
unit, apply a filed stratum rate to get an expected count, and designate on the excess. Two forms of it,
the one a solver constructs and the one the pack already prints.

Golden designated set `[1, 3]` against the charter tolerance of 22.0 avoidable complications per 1,000
separations. Tested at three confound strengths, where the confound is the realistic one: sicker patients
genuinely move between units more, so `comorbidity_score` correlates with handover exposure.

| Confound strength | excess projected on separations | published `standardised_ratio` |
|---|---|---|
| comorbidity independent of handovers | `[]`, 0 of 2 | `[1, 3, 9]`, 2 of 2 in common |
| **comorbidity correlated (realistic)** | `[]`, 0 of 2 | **`[1, 3]`, reproduces the golden** |
| comorbidity strongly correlated | `[]`, 0 of 2 | `[3]`, 1 of 2 |

**Why it dies.** The pack publishes `standardised_ratio`, observed over expected by stratum, and reading
that column against the tolerance hands back the golden set at the middle confound strength with no
construction at all. The handover exposure the design withholds is partly *proxied by case mix*, because
the units that take more handovers are the units that take sicker patients, so the standardisation the
pack already performs for a different purpose absorbs enough of the withheld driver to put the right two
units over the line.

**The honest reading, which is not that the kill is structural.** The route is clear at rho=0 and at
rho=0.9 and fires only at rho=0.6, so this is a confound-strength-dependent failure, and tuning rho away
from 0.6 would make it pass. That is exactly the move that is not available: the architecture would then
be resting on the claim that case mix and patient movement are *uncorrelated* in a hospital, or
correlated so strongly that standardisation overshoots, and neither is a world a reviewer would accept.
A designation set cannot be defended on a confound strength chosen to miss. Note also that `[1, 3, 9]` at
rho=0 contains both true members plus one false positive, so even where the published ratio does not
match it sits one unit away from the answer.

**The general rule this adds.** Where a design withholds the exposure a quantity scales with, check every
*adjustment the pack already publishes for another reason*: a standardisation performed on an observable
that correlates with the withheld exposure is a free partial recovery of it, and it costs the solver no
construction. The reflex sweep must therefore include the pack's published derived columns at every
confound strength the world makes plausible, not only at the one the generator happens to use.

Per the stop rule, the pass stops here: the four remaining screens (the dichotomy, the unit's own history,
move available against move needed in the tolerance's units, and the standard error of what the
construction estimates), the silent-row readability screen and the full enumerated sweep were not run.

- **Architecture 7 pass, 2026-10-18: five structurally distinct Layer 2 mechanisms screened on this
  cell, all five dead, nothing drawn and no card registered.** The pass was opened on the brief that an
  overdispersion-adjusted funnel was unspent. It is not: this note already carries it under
  `Rejected at the draw: judging each unit's excess against its own sampling error`, which names the
  over-dispersion-adjusted funnel by name. Screens were run as code on a 14-unit provider world
  (volumes 410 to 11,200 episodes, one real outlier of 1.62x at middling volume) and on a four-directorate
  28,000-episode hospital world. Scripts and output in the builder's scratch directory, `screen.py` and
  `screen2.py`.
- **Rejected, measured: overdispersion-adjusted funnel limits as the decisive step.** The flagged set is
  not invariant to the overdispersion estimator. Across five standard variants (exact Poisson, multiplicative
  by sqrt of raw phi, multiplicative by sqrt of winsorised phi, additive random effects on a
  DerSimonian-Laird tau2, empirical Bayes shrunk ratio) the measurements are phi raw 1.373, phi winsorised
  0.484, Q 15.66 on 13 df, tau2 0.00271, and the five variants return **three distinct flagged sets**,
  with the real outlier flagged by **four of five** and empirical Bayes flagging **nobody**. Pinning phi
  files the method; leaving it open forks the decisive object. Architecture 1's disease in another dress,
  exactly as the earlier draw-stage rejection predicted.
- **Rejected, measured: the expectation fitted on the same data the outlier is judged in (leave-one-out
  standardisation).** Move available against move needed, which is the skill's first pricing step. The
  national pooled ratio is 1.0260 over 1,126 expected harms. Taking a unit out of its own reference moves
  its ratio by 0.0391 on the largest unit (11,200 episodes), 0.0028 on an average one and 0.0021 on the
  smallest, against **0.1219 needed** to cross the tolerance: available over needed is **0.320**, so the
  step cannot decide a threshold crossing at any volume a hospital carries. It also settles whose rates
  each episode is compared to, which is the comparison, so the WHAT screen kills it independently.
- **Rejected, measured: the exposure window and the competing exit (per-episode against per-patient-day,
  with discharge as a competing risk).** On simulated stays the same hazard prints, per 1,000, a
  per-episode 21.042 against a per-bed-day 4.931 on the short-stay unit and 27.297 against 3.195 on the
  long-stay unit, and the two bases **reverse the ordering of the two units**. The three bases are three
  different filed units of analysis, which closure axis 9 and the WHAT screen require pinned anyway, and
  once pinned the computation follows from the clause. task192's architecture 2 also already holds the
  competing-exit insight, so the driver is on file.
- **Rejected, and this is the finding of the pass: `uncertainty_hold` is closed on provider-quality ground
  in both directions, because the domain's two documented reflexes are monotone.** If the golden is a hold,
  the reflexes that reach it are shrinkage toward the pooled value and overdispersion-inflated limits, which
  are rigor patterns 3 and 4 of the client's own library for this subdomain: measured, empirical Bayes
  declines to flag the loudest raw ratio (O/E 1.356) with no analysis at all, so a hold is reflex-reachable.
  If the golden is an act, the easy route has to overstate the expectation, so **every** under-adjustment
  reaches the golden: measured on the four-directorate world, the golden ratio is 1.661 and the
  no-comorbidity-adjustment route gives 2.273, both over the 1.20 tolerance, so the laziest route on the
  pack files the golden verdict. There is no third direction, so no uncertainty object on this ground can
  be silent.
- **Rejected: over-adjustment of the risk model by conditions acquired during the stay (the client's own
  rigor pattern 1 for this subdomain), the strongest candidate of the pass and dead on the WHAT screen.**
  Built and measured: a directorate of low pre-existing risk that harms its patients accumulates coded
  conditions during the stay, so its index-coded expectation is inflated and hides a real breach. On the
  28,000-episode world the ratio is **1.248 on the index-coded band against 1.661 on the pre-existing band**
  with a 1.20 tolerance, the two separations are financed by different quantities (the acquired-code
  inflation and the true harm multiplier, so they do not trade off, which is what architecture 3 lacked),
  the crude rate passes at 16.1 per 1,000 against a 32 tolerance, and every conservative reflex lands wrong.
  It still dies: the decisive step settles which reference rate each episode is compared to, which is the
  comparison, and the pipeline's own lesson from architecture 2 records that the comparison includes both
  whose rates and which pool. The three devices that could close the fork each fail a different screen, and
  that pincer is the reason to re-root rather than tune: filing the band's source in the framework names the
  decisive quantity (readability test 1), closing it with the reference table's provenance note makes the
  stump a reading of that sentence (rule 3, data semantics), and closing it with the reference table's
  published band distribution, which only the pre-existing construction reproduces, refutes the naive read
  (readability test 4). Announce it, make it a reading, or leave it open: there is no fourth device.
- **The structural rule this cell now carries, and it explains all six earlier architectures as well as
  these five.** On `provider-quality-risk-adjustment` a decisive step has to be one of three things and each
  is closed. A per-unit rate carries a free weighting or shrinkage choice, which forked the graded figure in
  architecture 3 (36.6 to 49.0), architecture 4 candidate 1 (16.9, 18.0, 18.3) and architecture 5 candidate A
  (10.1, 10.2, 10.5). An uncertainty object is reflex-monotone in both directions, measured above. Anything
  else available here settles a part of the estimand: the window (rejected at the draw), the unit
  (architecture 5, candidate C, and the exposure screen above), the population or the comparison
  (architecture 2, architecture 6 and the over-adjustment candidate). Risk adjustment is what this domain
  publishes most, so its decisive quantities are nearly all comparisons, and a comparison is a WHAT. **The
  next pass on this number should change the cell rather than the mechanism**, because what is spent is not
  one driver family but the WHAT-screen residue of this one, and the skill's own note that a cell is
  redrawable does not reach a cell whose every decisive step is a filed part of the estimand.

- **The funnel candidate re-screened properly, on the coordinator's test, and dead across 60 seeds.** The
  first screen of the architecture 7 pass built a world with phi raw 1.373, too little between-provider
  dispersion for rigor pattern 4's trap to exist at all, so it measured determinism and not stump power.
  Rebuilt to the candidate's own specification (16 providers, 300 to 15,000 episodes, between-provider
  sigma 0.18, one real 1.65x outlier at 4,300 episodes, phi raw mean **5.726** over 60 seeds, range 2.662
  to 10.444, tau2 mean 0.04601), it dies on three measurements at once.
  **One, there is no stump on a named outlier.** The plain exact Poisson limits the pattern names as the
  shortcut flag the real outlier in **60 of 60 seeds**, and so does the worst-decile shortcut in 40 of 60.
  A genuine 1.65x effect at 4,300 episodes sits far outside plain limits whatever the dispersion is, so
  the overdispersion correction changes which OTHER units are flagged, never whether the real one is. The
  decisive object therefore has to be the flagged set, not a name.
  **Two, the flagged set is not determinate.** Four defensible members of the golden's own family
  (multiplicative on winsorised phi, multiplicative on raw phi, additive on a DerSimonian-Laird tau2,
  additive centred on the pooled ratio) return **a mean of 1.83 distinct sets and disagree in 40 of 60
  seeds**. This is Gate C in the same words that sent architectures 1 and 3 back, and the coordinator's own
  constraint closes the only exit: pinning the dispersion treatment anywhere in the pack files the decisive
  step and removes it.
  **Three, the reflex reaches it.** The empirical Bayes posterior flags the real outlier in **60 of 60**
  seeds and reproduces the golden set exactly in **33 of 60**; the hierarchical predicted-over-expected
  reflex also flags it 60 of 60 and matches the set 33 of 60; James-Stein flags it 48 of 60. Shrinkage is
  rigor pattern 3 of the same block, which is to say the opponent's first reflex on this ground, and it
  reaches the answer while taking no overdispersion step at all. That is the repo's own measured precedent
  (empirical Bayes beating a designed step better than three to one) reproduced on this cell.
- **Conceded, and worth recording precisely because it is not the reason the candidate dies: the funnel
  candidate PASSES the estimand test.** Its decisive quantity is the between-provider dispersion, phi or
  tau2, which is estimated rather than defined, and it is none of the five parts: not the population (every
  provider in the framework), not the outcome (the coded harm), not the window (the review period), not the
  unit (the provider), not the comparison (the published reference rates). So filing the estimand does not
  file the method here, which is exactly why the candidate is tempting and why it survived six architectures
  of screening. **Passing that test is necessary and not sufficient.** It dies on the three measurements
  above, and the general form is worth carrying: a decisive step whose quantity is a dispersion can pass
  the estimand test and still fail, because the estimator family for a dispersion is open (horn two) and
  shrinkage reaches the same ranking without estimating it (horn three). Its `layer2_pattern` is
  `healthcare-delivery-health-economics/provider-quality-risk-adjustment/4`, the client's own pattern, not
  an own-named one.

- **Architecture 8 pass, 2026-10-18: the number moved off `provider-quality-risk-adjustment` to
  `business-operations-analytics` / `service-operations-sla` x anomaly-detection (client task type
  `human-factors-ergonomics/safety-incident-error-analysis`), three structurally distinct Layer 2
  mechanisms screened to death with measurements, nothing drawn and no card registered.** The axis window
  on the new ground is wide: `guard.py check` on the probe card returns **PASS, exit 0, with no WARN**
  (shape 09, gap `rule`, pattern A, `signal_vs_noise_or_hold`, `structural_verdict`, `binding_constraint`,
  `physical_verification`, `operations_log`, `operations_director`, `line_manager_or_team`,
  `incident_or_complaint`, `professional_services`, question form `whether`, Portugal, personas drawn at
  `names --geo Portugal --seed 194`), nearest driver 0.05. **What shut the pass was the mechanism, not the
  window.** Scripts in the builder's scratch directory: `screen_c1.py`, `screen_c2.py`, `screen_c3.py`,
  `probe.py`.
- **Rejected, measured: the latent concentration of event propensity across a unit's own members (the
  field's accident-proneness deconvolution).** Decision shape was a designation against a filed tolerance
  of 0.40, which is architecture 6's device and the one escape from a weighting fork. It does not reach:
  over 20 world redraws of 12 depots (40 to 260 operatives each, gamma shapes 0.45 to 6.0), the golden's
  **own** estimator family (latent truth, empirical Bayes, negative-binomial MLE, moment-matched mixture)
  returns a mean of **3.0 distinct designated sets out of 4 variants**, maximum 4, and on one seed the
  four sets were `()`, `(1,5)`, `(5)` and `(5)`. Stump power was present and irrelevant: empirical Bayes
  reproduced the golden designation in **1 of 20** and the naive observed share in **0 of 20**. This is
  the dispersion screen's horn two measured on new ground: discretising against a tolerance only helps
  when the family's spread does not cross the line, and a concentration's spread crosses it.
- **Rejected, measured: separating a verifier's discriminability from where it sets its acceptance line,
  with a filed change to a common line making the historical miss rate uninformative (signal detection
  theory, the field's own method for an inspection judgement).** The strongest candidate of the pass and
  the only one whose stump power and domain fit both held: over 25 redraws of 12 teams (9,000 to 60,000
  items each, discriminability 1.0 to 3.0, own lines -0.6 to 1.3), carrying each team's own historical
  miss rate forward reproduced the true designation in **2 of 25**. It dies on the estimator family. The
  four standard members (equal-variance d-prime, unequal-variance d_a at a signal spread of 1.25, a logit
  ROC, non-parametric A' mapped back through an equal-variance ROC) return a mean of **1.64 distinct
  designated sets**, maximum 3, and reproduce the true designation in 24, 14, 20 and 14 of 25
  respectively; the worst absolute error on the graded figure across the family averages **9.67 escapes
  per 1,000 against a 6.0 tolerance**, about a hundred times the printed unit. The ROC form is a method
  and not a convention the closure table demands, so pinning it files the decisive step, and the dial
  fails at both ends: a smaller move of the line shrinks the family's spread and makes the naive
  carry-forward right. **It dies a second time, independently, on the abstraction test**, and this is the
  fourth measured instance of the lexical blind spot: at 0.05 nearest it is lexically clean, and three
  incumbents hold the same insight told in other nouns, each being "a measured classification statistic
  does not transport, so find the invariant that does" (task192, class-conditional instrument behaviour
  across a composition shift, live in the last twelve; **task446 v2**, a screen's yield carried onto a
  population whose base rate moved; task229 v2, the share in a correct state seen through checks that
  reset it).
- **Rejected, measured: a unit's own defect rate where the record holds only what got past a shared
  downstream check whose catch probability moves with its own instantaneous load.** Three independent
  kills over 25 redraws of 12 depots across 52 weeks (volumes 60 to 420 jobs a week, own rates 5.0 to 14.0
  per 1,000, a tolerance of 9.0, catch probability 0.05 to 0.95). **One, the corrected estimator cannot
  rank:** the escape-weighted route reproduced the true designation in **1 of 25**, because thinning
  leaves the escape counts too small to carry the comparison, which is the standard-error pricing step.
  **Two, the quantity is not latent at all:** the desk logs what it caught, so caught plus escaped over
  jobs is exact arithmetic on shipped records, and that route was the best of every non-truth route at
  **7 of 25** while the naive escapes-per-job route scored 0 of 25 and the weekly-standardised reflex 0 of
  25. Architecture 4's finding reproduced on new ground: anything recovered by arithmetic on these records
  is observed, so filing it is rule application. **Three, the correction's own family forks:** a weekly, a
  pooled and a monthly catch probability return a mean of **2.32 distinct designated sets out of 3**.
- **Not re-screened, and recorded so it is not paid for twice: adjusting the comparison for a quantity the
  unit's own conduct produces (over-adjustment, and its collider-bias form).** It probes clean at 0.10
  nearest and it is this number's own architecture 7 screen 5, dead on the WHAT screen because the step
  settles which reference rate each unit is compared to. The lexical score does not see it; the slot note
  does.
- **The structural rule the two passes together now carry for a unit-comparison anomaly call on human-error
  ground, and it is measured from both sides.** task182's architecture 5 measured the records-fixed side of
  the pincer on this same client task type: with every printed figure an exact integer or ratio the
  determinacy half passes everywhere (the slate identical under all six licensed bandings 20/20, all eight
  licensed forms of the conditioning naming one slate 20/20), and the stump is gone, the crude route
  reaching the golden slate 20 of 20 in two of its three models. This pass measured the estimator side:
  stump power is easy (naive routes at 0 of 20, 2 of 25 and 0 of 25) and determinacy is gone (1.64 to 3.0
  distinct designated sets inside the golden's own family). **The dial that closes the family is the dial
  that makes the quantity observed or the naive route right**, measured three times here: pin the ROC form
  and the step is filed, shrink the move of the line and the carry-forward is correct; make the catch
  probability exact per item and the total is arithmetic; close the mixture family with a standard and the
  concentration is a definition. So a draw on this ground needs a graded figure that is records-exact while
  the construction that produces it is not reachable by any group-by, which is the one shape neither pass
  has screened.
- **The one route left unscreened, with its forcing device named and its predicted death, so the next pass
  starts past it.** An exactly-determined attribution system: each incident is recorded against work whose
  touch pattern across units the pack gives at another grain, the per-unit quantities are the unique
  solution of a square full-rank system (so every member of the estimator family, ordinary least squares,
  weighted least squares and Poisson maximum likelihood, returns the identical numbers and the family
  freedom that killed architecture 4's candidate 1 and candidate C2 above is absent by construction), and
  the graded figures are records-exact. Predicted deaths, in the order to test them: the solve is an
  attribution, so the WHAT screen asks whether it settles the unit; task48, task103 and task119's
  never-registered draft hold the path-attribution insight; and a square incidence structure has to be
  argued realistic against an operation that would produce an over-determined one. Not screened in this
  pass and not claimed to survive.

- **Architecture 9 pass, 2026-10-18: the number stayed on `business-operations-analytics` x
  anomaly-detection, the route architecture 8 left unscreened was screened to death on all three of its
  predicted deaths, two further structurally distinct mechanisms were screened to death beside it, nothing
  was drawn and no card was registered.** Scripts in the builder's scratch directory
  `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/wave5/task194c/`:
  `screen_a.py`, `screen_a2.py`, `screen_a3.py`, `screen_b.py`, `screen_c.py`, and the probe card
  `task194_card_probe.json`.
- **The window is confirmed open and now tested on a second subdomain and a second client domain, so no
  later pass pays for this read again.** `guard.py check` on the probe card returns **PASS, exit 0, with no
  WARN**, nearest driver 0.06, on `business-operations-analytics` / `workforce-labour-planning` x
  anomaly-detection with `client_domain` `general-statistics-data-science`, shape 09, gap `rule`, pattern
  `A`, `signal_vs_noise_or_hold`, `structural_verdict`, `binding_constraint`, `physical_verification`,
  `operations_log`, `operations_director`, `line_manager_or_team`, `incident_or_complaint`,
  `professional_services`, question form `whether`, Portugal. This holds after task172 registered and
  pushed task246 out of the ban window, so the live three are task172, task244 and task170. **Three facts
  the same probe bought, each of which would otherwise cost a redraw at stage 2.** A house-domain draw here
  must carry `client_domain` or `domain.house` WARNs. Decision `designation_set` with gap `population` and
  decisive pattern `G2` is a `test.same_puzzle` **BLOCK** against task239 inside the live batch, and
  `test.same_puzzle_older` against task264 and task48 v2 and `test.same_driver_older` against task228 v5
  besides, so the verdict shape is the cheap one here and the slate shape is not. Question form `which`
  WARNs on `repeat.question_form` against task190; `whether` is clean.
- **Rejected, measured, and this closes the one route architecture 8 left open: the exactly-determined
  attribution system** (per-unit rates as the unique solution of a square full-rank system over observed
  aggregates, so ordinary least squares, weighted least squares and Poisson maximum likelihood coincide by
  construction). World: 12 crews, jobs touched by 3 crews each with Dirichlet shares, callbacks Poisson on
  the crew-share mixture, true rates 3.0 to 16.0 per 100 touches. **Death one, the forcing device is the
  kill, and it fires before the WHAT screen is even reached.** A realistic touch matrix aggregated to
  exactly 12 buckets has condition number **median 437, max 3,256**, so the solve multiplies the
  aggregates' Poisson noise by that factor: mean absolute error on the graded figure **546.56 per 100
  touches against the job-grain regression's 1.16 on the same records at 25,000 jobs, 471 times worse**,
  and the exact solution returned a **negative rate in 25 of 25 redraws at every size tested (worst
  -3002.1 against a true range of 3.0 to 16.0)**. The non-negativity the rate actually carries then binds,
  the constrained Poisson maximum likelihood cannot return the unconstrained solve, and **the family
  reopens at exactly the point exact identification was supposed to close it: 2.00 distinct designated
  sets of 4 inside the golden's own family**, against the determinacy screen's bar of one. The solve named
  the true designated set **0 of 25 at 900, 6,000 and 25,000 jobs**. **Death two, the dichotomy, confirms
  it from the other end** (`stumping` 1.2a): if the per-unit quantities are the unique solution of a square
  system over observed aggregates then they are an exact function of the records, so the filed quantity is
  observed, nothing is left to estimate, and the route that apportions computes a different quantity, which
  makes filing it rule application and leaving it unfiled a fork. The route cannot be exactly determined
  and estimating something at the same time, which is the pincer in one line. **Death three, realism, is
  the same dial from the third side:** the system is square only because the job rows were discarded, and
  any field-service system holds them because an incident is logged against a job, so the real system is
  over-determined and the family spreads **8.209 per 100 touches on average, 27.702 at worst, with mean
  1.80 distinct designated sets and a maximum of 3**. That is architecture 4 candidate 1's weighting fork
  returned in the new nouns. **Death four, the abstraction test, is independent of all three and is the
  fifth measured instance of the lexical blind spot.** At 0.05 to 0.06 nearest the driver is lexically
  clean, and `guard.py slots` returns **task244, live in the last three**, carrying
  `own:true-flows-by-inverting-misclassification-at-both-ends`: "only inverting the misreading at both ends
  against the full table of stocks gives the real moves." Stripped of nouns that is this candidate exactly,
  the per-unit truths recovered by inverting a known matrix against observed aggregates while the route
  that works on the marginals leaves the error in. task246, also live, deconvolves a measurer's offset and
  error out of a spread. The attribution half is held three times over: task48's two-sided pair grain,
  task103's handed-over quantity decomposing into per-unit standard amounts, task119's whole paths credited
  to the unit where the path began.
- **Rejected, measured: the binding constraint on a coupled operation** (every station's throughput equals
  the line's, so the unobserved quantity is each station's standalone capability, and the constraint starves
  and blocks its neighbours so every idle-time route names the neighbour). Serial line, 6 stations, finite
  buffers of 1 to 3, blocking after service, lognormal service at a coefficient of variation of 0.35, true
  cycle times 0.80 to 1.00 with one constraint at 1.25, 6,000 parts, 20 redraws. The nameable wrong answer
  is real and it is not enough: **the most-idle route lands on a station adjacent to the constraint in 13 of
  20**. The candidate dies on one number in the other column. **Utilisation, the single most standard output
  this field produces, names the true constraint 20 of 20, and "filter to busy time and divide by parts"
  names it 20 of 20.** That is the common-exposure subset screen firing in its own words, a filter and a
  divide estimating the same quantity with no model, and it is the opponent's first group-by rather than a
  reflex it has to think of. The field's published refinement is worse than useless here besides: the
  average uninterrupted active period named the constraint **0 of 20**, so the ladder inverts as well.
- **Rejected, measured: the block-maximum inversion**, drawn on
  `general-statistics-data-science/exploratory-data-analysis-distribution-assessment`, **the one task type
  this house domain inherits that no pass had screened** (the other four all serve anomaly-detection and
  are each closed: `provider-quality-risk-adjustment` by architectures 1 to 7,
  `payment-claims-health-plan-analytics` by task198's four mechanisms, `safety-incident-error-analysis` by
  architecture 8 and task181, `multiple-testing-selective-inference` by task195). The quantity is the 95th
  percentile of interval-level concurrent demand, which no record holds because a workforce system stores
  only each day's peak, and because units trade different hours a stored peak is a maximum over a different
  number of draws, so the parent percentile is the daily-max distribution's own `0.95 ** n` quantile:
  records-exact, no parametric fit, and not reachable by any group-by. 12 units, 500 days, 18 to 44
  intervals a day, lognormal interval demand, 20 redraws. **At zero serial dependence it is everything the
  designation determinacy screen asks for: 1.00 distinct designated sets of 4 inside the golden's own
  family, and all five reflexes (the peaks' 95th percentile, their mean, their maximum, peak per interval,
  a log-corrected peak) reach the true set 0 of 20.** It dies on the single dial, and the dial is serial
  dependence, which no staffing world can set to zero because demand carries a within-day profile by
  construction. At **rho 0.45** the effective block size becomes a fitted quantity and the golden's own
  four-member family (nominal count, integral timescale, extremal index, matched) returns **2.85 distinct
  designated sets of 4, maximum 4**, the nominal inversion reaches the truth **0 of 20**, and the worst
  absolute error on the graded percentile across the family is **5.77 demand units against a printed unit of
  0.1, about 58 times it**; at **rho 0.75** it is **3.00 sets and 11.71 units**. Pinning the effective block
  size is pinning a method, not a convention the closure table demands, so it files the decisive step. **It
  dies a second time, independently, on the abstraction test against task191, live in the last twelve**,
  whose insight is "the largest a quiet set of the same size and length produces": stripped of nouns both
  are "a maximum over more draws is larger at the same parent distribution, so maxima across units of
  different draw counts are not comparable", with the same default path of comparing the raw maxima and
  differing only in the direction of the correction. `guard.py check` also puts task461 at 0.05 nearest, "a
  low quantile of a distribution seen directly only over one short and unrepresentative" window.
- **The structural law the three passes together now carry for this ground, stated so a fourth pass does not
  rediscover it, and it is exhaustive rather than a list of incidents.** For a quantity estimated per unit
  from that unit's own records, a construction is forced in exactly three ways and all three are dead. It is
  **exact arithmetic on the records**, which makes the quantity observed and the step rule application
  (screen A here, architecture 4's escape total, task198's B4 split lines). It is **non-parametric**, which
  makes it a stratification and therefore the opponent's own first group-by (screen B here at 20 of 20, and
  the crew-size version of the work-content candidate, which is a group-by on job type and crew size). Or it
  is **parametric**, which reopens the estimator family (screen C here at 2.85 sets, architecture 1's two
  functional forms, architecture 3's chain-ladder variants). There is no fourth case, which is why the dial
  that closes the family has been the dial that makes the quantity observed or the naive route right in
  every one of the eleven mechanisms the last three passes have measured. **The escape is the one all three
  of this sitting's ships took and it is not a cleverer statistic: the construction's forcing input comes
  from a different file at a different grain whose variety no stratification of the decision file
  reproduces** (task197's high-resolution archive against a programme schedule, task196's second capture
  channel, task199's record of observation effort). So a fourth pass here does not look for a better
  quantity on the unit's own records; it looks for the second file, and the question to ask of a candidate
  before anything else is which file does the forcing and why no group-by on the decision file reaches it.
- **Named and not screened, so it is not claimed either way: the verdict direction the window itself points
  at.** The axis set that passes clean is `structural_verdict` with question form `whether`, and
  `stumping` Part 3 holds that a judge-against-noise mechanism survives on a verdict about one named unit
  (one boundary, placeable far from it) where it cannot decide which of N is largest. No quantity was found
  for it in this pass, so there is no candidate yet by the skill's own test: the file that does the forcing
  cannot be named. The two shapes of the fresh task type left unmeasured are a mixture's component share and
  a tail index, and both are expected to die parametric by the law above unless a second file pins them.

- **Cell 3 opened and closed in one pass: pharmacology-pharmacoepidemiology-safety /
  `safety-signal-detection`, three candidates screened to death with measurements, nothing drawn, no card
  registered, no file in `target/` or `golden/` touched.** The cell was chosen because the client taxonomy
  gives `safety-signal-detection` anomaly-detection as its only objective, so the task-type block that
  governed architecture 3 cannot fire here and a forward-facing count cannot be retagged as forecasting.
  The one spent AD driver on the cell is task193's (how many units would show one of two orderings by
  chance, each unit's room for an ordering set by where its own first exposure falls), and all three
  candidates were drawn away from it. **The axis window is open and what is missing is a mechanism**, the
  same finding as architecture 8 on its ground: `guard.py check` on the probe card returns no axis ban at
  all, no overuse WARN, and nearest driver 0.08, with only `test.same_driver_older` against task229 v1
  (gap `population` plus pattern `D` plus Gate G `signal_vs_noise_or_hold`, a differentiable older match
  that owes one line) and two persona WARNs. The reserved axis set itself is therefore not what shut the
  pass.
- **Candidate 1, the exposure denominator of a reporting rate, dead on measurement in three modes.** The
  brief's own pointer (exposure denominators come from a different system at a different grain) and the
  only live field tool the cell's four leave open, task193 holding the sequence screen and task180 v3 the
  self-controlled comparison. Decision shape: an additional risk minimisation measure renewed, replaced or
  lapsed at the periodic safety filing, on a reporting rate per 1,000 patient-years against the charter's
  bar, patient-years being unobserved and built from aggregate supply through a consumption factor the
  dispensing panel holds at patient grain. Measured over market growth 0.000 to 0.140 a month and a
  non-panel maintenance dose of 14 to 28 mg: (a) **the denominator is observed**, because a supply file
  publishes packs and a pack is a known number of days of therapy, so packs times days of therapy returns
  the truth at +0.000 per cent at every one of the ten settings, which makes filing the quantity rule
  application and the panel unnecessary; (b) **where the supply is published as mass only, the decisive
  construction forks across its own family**, four defensible readings of realised mg per patient-day
  (person-time weighted 17.911, mean of per-patient rates 14.468, median patient 16.719, maintenance
  patients only 18.169) putting the graded rate at 2.4812, 2.0043, 2.3161 and 2.5169 per 1,000
  patient-years, a spread of 0.5127 against a printed precision of 0.01, about fifty times over, which is
  architecture 3's death repeated; (c) **the only mode that separates is panel-to-market transport**, the
  error running from -21.02 to +27.92 per cent as the non-panel markets' dose moves over a range nothing
  in the pack records, which is selection and is `population_selection`, task182's reserved strategy this
  wave. The cohort-maturity mode is the smaller half of the family besides: across the whole plausible
  growth range the nominal-factor error moves only from +23.78 to +12.48 per cent, so about eleven of the
  twenty-four points are composition and the rest is a published constant, and `composition_mix` is
  blocked on the last three builds anyway.
- **Candidate 2, the share of the event's risk inside the measure's monitored window, the largest
  separation measured on this cell and dead on the estimand.** The decision renews a fixed early
  monitoring schedule, replaces it with continuing monitoring, or lapses it, on the share of the risk
  arising in the first twelve weeks of treatment; the easy route reads that share off the cases' own
  time-to-onset distribution, which is pharmacovigilance's standard instrument. Measured on a cohort of
  thirty monthly initiation cohorts at 5 per cent growth with 20 per cent abandoning during titration:
  person-time is front-loaded at 0.3890 in weeks 0 to 12, so under a **flat** true hazard the
  time-to-onset instrument files 0.3986 of the risk inside the monitored window against a truth of
  0.1154, a 3.5 times overstatement, and the hazard-resolved route recovers 0.1211; under an early hazard
  0.7035 against 0.5051, under a late one 0.2447 against 0.0455. The separation is the best this slot has
  measured and the candidate still dies, three ways. The decisive construction is cases per band over
  person-time per band, and **person-time per band is exact arithmetic on the panel's fills once the
  charter files the bands**, so the quantity is observed and the step is rule application. Removing the
  panel sends the construction into a deconvolution of the maintenance-supply series against the
  initiation series implied by starter packs, which is architecture 8's exactly-determined attribution
  route and architecture 9 killed it by condition number (median 437, negative in 25 of 25 redraws).
  Leaving the long durations unobserved at the lock point is whether the not-yet-observed members are in
  the population, the WHAT screen's first failure mode, and **task193's own note already dropped this
  exact candidate at the draw for that reason** (its architecture 2, third draw), with task184 and task189
  holding interval-censored event times and left-censored measurements in this lane.
- **Candidate 3, the informative person-time a surveillance arrangement will deliver, dead on separation
  before the estimand.** The decision renews the current claims source, replaces it with a smaller and
  more stable one, or lapses to spontaneous reporting only, on the exposed person-time each source can
  deliver with the charter's twelve months of continuous follow-up, which is unobserved and forward
  facing. Measured on three sources (14.2 million lives at 19 months median enrolment, 3.4 million at 58,
  8.9 million at 11): the decisive construction ranks the large commercial source first at 3,850
  informative patient-years against 3,050 and 1,502, and **covered lives alone ranks them the same way**,
  so the construction does not change the answer at any realistic setting. The dial that would separate
  them, lengthening the required follow-up against median enrolment, is the dial that makes every source
  unusable. Independently dead on the WHAT screen: which enrollees contribute is the population part of
  the estimand, filed it is a procedure over the spans file and unfiled the figure is not determinate.
- **What the three measurements leave for a fourth pass on this cell, stated so it is not paid for twice.**
  Every candidate died at the same joint: a pharmacovigilance rate's denominator is either exact on a
  shipped aggregate, which makes the step rule application, or estimated per patient from a panel, which
  reopens the weighting family, and that is architecture 4's dichotomy and architecture 9's law restated
  in a third set of nouns. Candidate 2 is the one worth returning to, because its separation is measured
  at 3.5 times and only its denominator is the problem: a live draw here needs a risk set by duration that
  is neither exact arithmetic on a shipped file nor a question about which members the population holds,
  and no file a safety desk keeps (case versions, follow-up questionnaires, dispensing panel, aggregate
  supply, prescriber certification register, signal management log) supplies one. The three escapes
  `stumping` 1.2b licenses are each spent or banned on this objective besides: a second independent
  observation of the same events is task196, a verified subsample is task192 and task244, and a filed
  external rate is rule application. So the cell is not drawable on a rate, and the next pass on it should
  start from a non-rate quantity or the number should move to a fourth ground.

- **Cell 4 opened and closed in one pass: banking-credit-financial-risk / `fraud-aml-detection`
  (architecture 13), three candidates screened to death with measurements, nothing drawn, no card
  registered, no file in `target/` or `golden/` touched.** The cell was chosen because the client taxonomy
  gives `fraud-aml-detection` anomaly-detection as its only objective, and `org_family` was moved from
  `financial_institution` to `software_or_platform` so the world is a payments platform rather than a bank.
  The one spent anomaly-detection driver on the cell is task196's, which shipped on this subdomain the same
  day and is pending review, so the driver search was held clear of capture, undercount, two-channel
  estimation and completing a partial record throughout. **The axis window is not what closed this pass,
  and this is now the fifth cell to report that:** `guard.py check` on the probe card returns PASS with no
  axis ban, no overuse WARN, no `three_rules.strategy_risk` WARN, no persona WARN and nearest driver 0.06,
  under both the honest strategy label and the one free label. Two mechanical corrections to the brief fell
  out of it: `other` does **not** trip `ban.strategy` against task248, and with `pattern: none` the guard
  prints `generators[0]` as the decisive pattern (here `pattern G3`), so varying off `D` cleared task229
  v1's triple without a differentiation line being needed.
- **Candidate 1, the first-party share of a control's credited coverage, the strongest of the three and
  dead on its own sampling noise in one horn and on the estimator family in the other.** The decision renews,
  replaces or lapses a card-not-present control at the annual return, on the share of the fraud-coded
  dispute set the control could actually have prevented: a dispute raised under a scheme fraud reason code
  is either a third party's fraud or the cardholder's own purchase disputed as fraud, the second type is
  unreachable by any control because the party the control screens for is the party that authorised the
  payment, and the reason code does not separate them. The forcing file was the authentication message log,
  which pins the liability shift, because the scheme rule forbids an issuer to charge back a liability-shifted
  transaction as third-party fraud, so that population carries first-party disputes alone. Measured on
  120,000 transactions with 509 third-party and 1,702 first-party disputes, first-party being 76.98 per cent
  of the dispute set: the easy route credits the incumbent with 51.274 per cent of fraud-coded dispute value
  against the challenger's 6.630 and files **renew**, while on third-party value the incumbent covers 1.464
  against the challenger's 11.672 and the answer is **replace**, a clean flip with 1 of 7 reflexes reaching
  the golden verdict. It still dies three ways. **(a) The call only flips where the two dispute types are
  anti-correlated across the visible attributes**, and in the correlated configuration first measured there
  is no flip at all (naive renew by 35.966, golden renew by 9.055) with 6 of 7 reflexes landing the golden;
  but anti-correlation is exactly what puts the discriminator in a shipped column, and the liability-shifted
  dispute rate per merchant category prints 4.224, 3.882 and 2.955 for the intangible categories against
  0.148 to 0.447 for the rest, a tenfold separation visible in one two-column group-by, which is readability
  test 2. **(b) The graded figure is seed-hostage.** Over 20 redraws the truth itself ranges 0.000 to 10.457
  points against a golden margin of 10.209 on the single seed above, and the filter-and-divide recovery off
  the liability-shifted population carries a mean absolute error of 9.1152 points and a maximum of 26.1502
  against a printed precision of 0.01, so the correction injects more noise than the bias it removes and the
  ladder's roles would be hostage to the seed (task198 architecture 2's death, in new nouns). **(c) Remove
  the revealing subset and the family opens**: with no authentication state in the pack the first-party share
  is a two-component mixture, seven defensible routes put the graded figure between 0.000 and 51.274, a
  spread of 51.274 points or about 5,127 times the printed precision, and the verdict itself forks between
  renew and replace. The quantity is a share of a share of a rare event inside a 7 per cent control slice,
  and that is the general form: **on this ground a decisive quantity built on the confirmed-fraud events
  cannot rank, because third-party fraud is 0.42 per cent of traffic and the lever and the noise are the
  same scarce events.** Draw on the abundant side instead.
- **Candidate 2, the control's forward cost in genuine sales, drawn deliberately on the abundant
  false-positive side after candidate 1's lesson, and dead on identification.** The decision is the same
  three-way renewal; the quantity is the value of genuine business the control turns away, which is tens of
  thousands of rows rather than hundreds, and the unobserved part is whether a declined genuine customer
  recovered or was lost. The forcing attempt was the card-on-file population, where the merchant passes a
  customer account identifier so a later successful purchase is linkable, against guest checkout where it is
  not. Measured: the naive transport of the card-on-file recovery rate onto the whole decline set is fixed at
  45.098 per cent lost while the truth moves from 45.192 to 70.285 as the guest-to-card-on-file recovery
  ratio moves over its plausible range, an error running 0.094 to 25.187 points, with a family spread of
  35.255 points across four transports. **Nothing in any file a payments platform keeps pins that ratio**, so
  the figure is not determinate; pinning it in a shipped sentence makes the step rule application, and
  recovering it from the card-on-file subset is transport off a selected subpopulation, which is
  `population_selection` and reserved to task182 this wave.
- **Candidate 3, the adversary's response to the control, dead before any ladder on 1.2b case three.** The
  quantity is net forward fraud prevented, where a blocked attempt is deterred, relocated to another merchant
  on the platform, or relocated to a processor the platform cannot see. This was the one direction with no
  slot-note hit at all (`guard.py slots displacement deterrence blocked attempts re-routed` returns nothing).
  Measured: the graded figure moves from 69.905 to 20.121 per cent of gross blocked value as the
  out-of-platform relocation share moves from 0.00 to 0.50, a range of 49.784 points or 4,978 times the
  printed precision, **while the one observable the platform does hold, inside-platform relocation, stays at
  29.6 to 30.1 per cent throughout and so carries no information about the parameter at all.** That is 1.2b's
  profile test failed by construction rather than by width: a platform sees only its own traffic, so
  out-of-platform relocation has no observable that moves with it.
- **Killed free, with no screen spent, on the brief's own clause:** the control's standalone contribution net
  of the rest of the control portfolio, unobserved because the engine short-circuits on the first terminal
  rule and the case manager suppresses duplicate alerts. Estimating the overlap between two detection
  channels is two-channel estimation whatever the quantity on top of it, which is task196's ground and
  pending review on this very subdomain.
- **What the three measurements leave for a later pass on this cell, stated so it is not paid for twice.**
  The pharmacology law restates itself here in a fourth set of nouns, with the horn relabelled: a fraud or
  AML quantity's latent split is either **exact or near-exact on a revealing subpopulation some rule makes
  immune** (liability shift, authentication state, a scheme exemption), which puts the discriminator in a
  shipped column and makes the step a filter and a divide, or it is **a mixture with no revealing subset**,
  which reopens the family by thousands of times the printed precision. Candidate 1 adds a horn the
  pharmacology pass did not have and it is the more general one: **the confirmed-fraud events are too few to
  rank on**, so the quantity must be drawn on the abundant population (alerts, dispositions, declines, the
  queue) and not on the outcomes. Candidate 2 shows that moving to the abundant side is necessary and not
  sufficient, because the abundant side's latent part is pinned only by a linkable subpopulation, which is
  selection again. **The one direction this pass did not spend a screen on, and the one a later pass should
  start from, is the task202-shaped escape in this cell:** an estimand filed at a grain the fraud and AML
  decision file does not carry, with a second abundant file supplying the structure, the candidate forcing
  files being the alert and disposition log and the queue's own worked-and-unworked record, which pins the
  capacity actually applied and which no other file holds. A candidate there must name which file does the
  forcing before anything else, and why no group-by on the decision file reaches it.
- **Drawn and clean, for whoever takes the cell next:** personas `Sander Denissov`, `Tatjana Liivak`,
  `Jaanus Niit`, from `guard.py names --locale et_EE --seed 194`, all three clear of `people.first`,
  `people.last` and `people.full` on `guard.py check`. The locale is Estonian rather than Irish because
  `en_IE --seed 194` returns `Lauren Connachton` and `Paul Murnane` first, which are the two names the
  previous pass had to drop, and because Estonian surnames are not gender-inflected, so a drawn pair cannot
  produce the mismatch a Lithuanian draw does. Probe card at
  `<scratch>/w6_194b/task194_card.json`, marked PROBE ONLY and not registered.

- **Cell 5 opened and closed in one pass: epidemiology-public-health /
  `disease-surveillance-outbreak-anomaly-detection` (architecture 14), three candidates screened to death
  with measurements, nothing drawn, no card registered, no file in `target/` or `golden/` touched.** The
  cell was chosen because the taxonomy gives this task type anomaly-detection and data-quality-monitoring
  only, so a forward-facing count here cannot be retagged as forecasting, and because the brief named one
  spent anomaly-detection driver on it (task188's pooled-test density). **`guard.py slots` found three more
  builds on the cell that `recent`, `mechanisms` and `nearest` cannot see as neighbours, and they matter
  more than the card screen did:** task232 (a transmission rate per unit of exposure from closed episodes
  whose outcomes surface on a delay, attributed inside the delay's range), task242 (a share read through a
  detector whose chance of registering fades with time since the event) and task501 on the adjacent
  `infectious-disease-transmission-modeling` (a who-passes-to-whom matrix measured by pooling two regimes).
  With task188 those four close the cell's rate-and-share family from four sides, which is why this pass
  drew only non-rate quantities. **Screen 6 was run first, as the brief requires, and all three candidates
  were drawn to escape it rather than to argue with it:** C2's deciding quantity is a span in days, C1's is a
  date, and C3's is a dimensionless reproduction number, so none of the three has a denominator to choose and
  the pharmacology-and-AML law was not re-found. Harness in the builder's scratch directory
  `<scratch>/w7_194/`: `screen_c2.py`, `screen_c2b_c1_c3.py`, both rerunning byte-identically
  (`e3228f8a7e0c6555ae3a48fc18fe1cd7`, `fc2c9a99f4d95bff9c0b52ea22fc444e`), probe card
  `task194_card_probe.json`.
- **The axis window is open and what is missing is a mechanism, and this is the sixth cell in this lane to
  report it.** `guard.py check` on the probe card returns **PASS, exit 0, with no WARN at all**, nearest
  driver 0.06 (task201 v2), on `epidemiology-public-health` / `disease-surveillance-outbreak-anomaly-detection`
  x anomaly-detection with shape `17`, gap `time`, pattern `none` so `G7` reads as decisive, gate
  `signal_vs_noise_or_hold`, decision `structural_verdict`, strategy `other`, role `field_unit_lead`, forum
  `operations_desk`, forcing event `incident_or_complaint`, context artifact `operations_log`, question form
  `whether`, New Zealand. **One axis BLOCKed and was redrawn rather than argued:** `org_family`
  `government_agency` is `ban.org_family` against task471 (and `overuse.org_family` at 37 builds besides), so
  it moved to `hospital_or_health_provider`, which is the honester label anyway because a New Zealand public
  health unit sits inside the district health service rather than in a central agency. **Two corrections to
  the brief's own axis list, which had gone stale inside a day:** the last three builds are now task471,
  task474 and task475, not task269 to task271, so `composition_mix` and shape `01` are free again while
  `population_selection`, `time_semantics` and `decomposition_attribution` are blocked and the blocked shapes
  are `05` and `07`; and the drawn personas `Warwick Dalziel`, `Joanna Ham` and `Gabriel Monk`, from
  `guard.py names --geo "New Zealand" --seed 194`, raise no `people.first`, `people.last` or `people.full`
  flag.
- **Candidate C2, the strongest of the three and the one the pass was built around: a point-source against a
  persistent-source verdict benchmarked on the implicated run's own dispensing profile. Dead twice, and the
  second death is the one worth carrying.** The world is a genomically defined listeriosis cluster among the
  clients of a chilled ready-meals supplier; the call is the structural verdict, one contaminated production
  run (recall it and reopen the line) against a persistently contaminated plant environment (withdraw the
  range and close the line). The deciding quantity is the span of the exposure process behind the cluster,
  unobserved because no record holds an exposure date. The forcing file is the warehouse's own stock movement
  record, which pins what no other file pins: that one run's cartons are dispensed over five weeks when they
  sit in a slow retail-chilled channel and over four days when they sit in an aged-care channel. The textbook
  route compares the onset span against the pathogen's own incubation range. **The separation is real and
  large: with one contaminated run the onsets carry a standard deviation of 20.27 to 23.12 days against an
  incubation standard deviation of 12.45 days, so the naive verdict files persistent contamination in 19 or
  20 of 20 worlds across a slow-channel share of 0.45 to 0.95, and the moment-subtraction route
  (`Var(onset) - Var(incubation)`, the only additive dispersion measure and so a genuinely forced
  construction) reports a phantom exposure window of 15.67 to 19.35 days.** **Death one, screen 2, fired on
  the first measurement and was repairable:** with the contaminated run placed at the extreme of the forcing
  file's plainest per-run column, "the run with the largest slow-channel share" names it **20 of 20** and
  "the longest dispensing tail" **13 of 20**; moving it to the second, third, fifth or seventh place in that
  column drops both to **0 of 20** while the naive verdict still fails 17 to 19 of 20. So the forcing column
  is not the wall here, which is worth recording because it is the wall on most grounds. **Death two is the
  wall and it is in the other column: there is a one-group-by route to the verdict itself, and it beats the
  designed construction.** Take the longest-dispensing run in the warehouse file, convolve its profile with
  the incubation density once, and ask whether the cluster's onset spread fits inside it: that route files
  the golden verdict **20 of 20** in the single-run world with no likelihood, no per-run fit and no
  deconvolution. **And the same measurement convicts the designed route from the other side: in the
  persistent world the one-line route is right 1 of 20, the naive route 19 of 20 and the designed likelihood
  0 of 20.** The likelihood files "single" in both worlds; its 20 of 20 in the single-run arm was a constant
  and not discrimination, exactly as the naive route's 20 of 20 in the persistent arm is a constant. A
  construction that cannot tell the two worlds apart cannot carry a verdict about which of them obtains, so
  the 20 of 20 the first screen reported was an artifact of comparing two constants. **Dead a third way on
  the graded object even if the verdict had held:** the run's name is not determinate, the likelihood naming
  the true run **13 to 15 of 20** with a mean absolute offset of 0.25 to 0.40 runs and a maximum of 2, so the
  call could only have graded the bare verdict; and the attaining subset is live besides, short-stay clients
  with one delivery in the window pinning the exposure dates directly and reaching "single" **14 of 20** at a
  realistic 6 per cent short-stay share.
- **Candidate C1, the recall's earliest contaminated production run, dead on the lever-against-identification
  pincer, which the measurement states more sharply than the prediction did.** The decision is how far back a
  recall must reach; the deciding quantity is the earliest production run whose output carried the organism,
  unobserved and forward facing because long-shelf-life stock of the early runs is still in the market. The
  predicted pincer was that the naive route (the earliest onset minus the incubation maximum) is wrong only
  where the early runs produced no observed case, and that is exactly where nothing in the case data
  identifies the start. **Both halves measured, and the second half is worse than predicted: the start run
  produced an expected case count under one in 20 of 20 worlds at an early-volume fraction of 0.02, 0.05 and
  0.12 and in 0 of 20 at 0.30 and 0.60, while the one-parameter maximum likelihood over the start run names
  it 1, 1, 0, 2 and 4 of 20 across those same five settings.** So the quantity is not identified at any
  setting, including the settings where the early runs certainly produced cases: an onset curve smeared by a
  12.45-day incubation standard deviation carries almost nothing about a release date three days from its
  neighbour's. **And the naive route's error is a constant rather than a lever**, missing the true start by
  exactly -6.00 runs at every one of the five settings and missing it on the conservative side, so it
  over-recalls; a route that is wrong in the safe direction and a decisive route that cannot beat it is an
  inverted ladder, not a stump.
- **Candidate C3, a facility's transmission verdict from the final-size inversion, dead on the parametric
  horn and on the easy route at once.** The decision is whether a named aged-care facility's outbreak is
  still transmitting above the response threshold; the deciding quantity is the facility's reproduction
  number, unobserved, recovered by inverting the final-size relation on the attack rate and the resident
  count, which is the field's own method and the one place a nonlinearity makes the attack rate itself
  misleading (the relation is convex, so a facility that has nearly exhausted its susceptibles shows a
  compressed attack rate). **Measured over 20 worlds at 42 to 120 residents and a true reproduction number of
  1.05 to 1.75, the four defensible inversions (the SIR final-size equation, a Reed-Frost chain binomial, a
  Greenwood chain binomial and the linearised form) spread the graded figure by a mean of 0.4733 and a
  maximum of 0.6055 against a printed precision of 0.01, about 47 to 60 times over, and they straddle a 1.30
  verdict boundary in 10 of 20 worlds, so the verdict itself forks in half the worlds.** That is architecture
  9's parametric horn in surveillance nouns. **And the inversion changes almost nothing anyway: the
  attack-rate-only sort, which is a filter and a divide with no model, agrees with the true ordering in 19 of
  20 adjacent pairs.** The other horn is the familiar one: with the susceptible pool taken as the resident
  count the inversion is exact arithmetic on two shipped columns, so filing the estimand makes the step rule
  application.
- **What the three measurements leave for a later pass on this cell, stated so it is not paid for twice.**
  The cell's rate family is closed four ways (task188 pooled tests, task232 exposure-delayed attribution,
  task242 a fading detector, task501 a regime-pooled contact matrix), and this pass shows that escaping
  screen 6 by drawing a span, a date or a dimensionless number does not buy anything on its own: each of the
  three died on a different one of the lane's standing laws, and the new one is C2's. **The law this pass
  earns, and it is not the forcing file's column: where the decisive construction is a benchmark for a
  statistic, the one-group-by route competes on the benchmark rather than on the statistic, and it wins
  because a benchmark is a single number however elaborately it was built.** C2's likelihood over 24 runs and
  a one-line maximum over the same file reach the same verdict 20 of 20, because both end in one comparison
  of one spread against one spread. So on surveillance ground the question to ask of a verdict candidate
  before anything else is not which file forces the benchmark but **whether the benchmark is a single number
  once the second file is read**, and if it is, the construction's elaboration is decoration. The direction
  left unscreened, where a later pass starts: a candidate whose second file supplies **one benchmark per
  case** rather than one benchmark for the cluster, so that no single comparison can stand in for it, the
  candidate forcing files being the client-level delivery register and the per-case enhanced-surveillance
  questionnaire, which pin each case's own exposure opportunity and which no group-by on the line list
  reaches. Any candidate there states, before any world is drawn, what the one-group-by route to its call
  would be and why it does not reach it, because this pass shows that the route exists and is found by the
  second measurement rather than the tenth.
- **`## Three rules` for C2, the only candidate that reached the point of being worth writing them for, with
  the lines that do not pass said plainly rather than written to pass.** `Task type:`
  `disease-surveillance-outbreak-anomaly-detection`, which the taxonomy serves with anomaly-detection and
  data-quality-monitoring, so the pairing is legal and the call cannot be retagged as forecasting. PASSES.
  `Domain test:` the deciding quantity is the span of the exposure process behind an epidemic curve, and the
  field's own instrument for it is the comparison of the curve against the incubation distribution, which
  only an infectious exposure makes meaningful because only there does a weeks-long random lag sit between
  the exposure and the record. PASSES. `Swap:` "whether one production run or the plant carried it, read off
  the seven-week span of the cluster's onsets" does not survive putting megawatt-hours or school enrolments
  in, because nothing there interposes a lognormal lag between cause and record. PASSES. `Layer 1:` onset
  dates missing on a share of notification forms, two laboratories' sequence-type nomenclature for one
  cluster, warehouse movements in cartons against deliveries in meals, mid-window client address and
  programme changes; each produced by a system the organisation runs and none placed to be caught. PASSES.
  `Layer 2:` `field_method`, the benchmark span for a single contamination event being that event's own
  dispensing profile convolved with the incubation density rather than the incubation density alone. PASSES
  as a description and is the line the build dies on, because the benchmark collapses to one number.
  `Decisive step:` benchmark the cluster's onset spread on the implicated run's dispensing profile rather
  than on the incubation range. **DOES NOT PASS: measured, a one-group-by maximum over the same file reaches
  the same verdict 20 of 20, so the step is not decisive, and the designed likelihood files "single" in both
  worlds (0 of 20 in the persistent arm), so it does not decide anything either.** `Not semantics:` holds,
  every field, code and unit read correctly still leaves the textbook comparison on "persistent" in 19 of 20
  worlds. PASSES. `Not rule application:` holds for the span itself, since no filed rule names the dispensing
  profile as the benchmark. PASSES. `Analyst test:` the analyst reads the onset span against the incubation
  range and files persistent contamination and a whole-range withdrawal, wrong in 19 of 20 worlds. PASSES as
  written and is worthless given the `Decisive step:` failure, because the wrong easy route is no protection
  when a one-line route is right. `Estimand:` "the number of production runs of the implicated product that
  carried the outbreak sequence type, as at the trace-back report" sits in the investigation's terms of
  reference. PASSES on paper. `No decoy:` nothing is planted; the warehouse record is the organisation's own
  and reads the same on every path. PASSES. `No certified replay:` no certified or published figure is
  reproduced to recover the method. PASSES. `Lesson:` **DOES NOT PASS, and this is the honest verdict on the
  pass: the lesson a model would learn is one a one-line route already teaches, so there is nothing here no
  build on file teaches.** Eleven of the thirteen lines pass and the two that fail are `Decisive step:` and
  `Lesson:`, which are the two that have to pass, so the candidate is re-rooted rather than resumed.
- **C2 dies a fourth time, on the abstraction test, and this kill was the cheapest available and was found
  last rather than first: it is the lane's sixth measured instance of the lexical blind spot.** Running
  `guard.py slots` on the **physical setting's** nouns rather than on the mechanism's (the pathogen, the
  notification route, the laboratory, the epidemic curve) returns **task242, on this very cell**, whose
  driver is "each unit's detection rate is the detector's curve averaged over that unit's own spread of
  event times up to its reading date", and its note at line 114 states it as "the curve by days since onset
  (the laboratory's panel) averaged over the zone's own epidemic curve". Stripped of nouns that is C2
  exactly: a filed kernel averaged over the unit's own spread of event times, in place of the kernel alone,
  with the default path using the kernel alone. The same run returns **task232, also on this cell**, whose
  literal reader counts a case when "onset within the condition's incubation range after a day the index
  attended while infectious", which is C2's incubation-range-against-a-dispensing-schedule comparison with
  the schedule being an attendance register instead of a warehouse record. `guard.py check` scored C2's
  driver at **0.06 nearest, against task201 and with task242 nowhere in the five returns**, so the text
  screen saw none of this. **The procedural lesson, which is the one to carry rather than the incident:
  `slots` on the setting's own vocabulary is a different screen from `slots` on the mechanism's, it is free,
  and on a cell this lane has already drawn four builds on it should be run before the first harness is
  written, not after the third.** Had it been run first this pass would have cost one measurement rather
  than three.
- **Axes re-checked immediately before hand-back, as the mid-wave window update requires, and the window had
  not moved again:** `guard.py check` on the probe card still returns PASS, exit 0, no WARN, nearest driver
  0.06. Every axis is clear of the live window's blocked values: shape `17` against the blocked `05` and
  `07`, strategy `other` against `population_selection`, `time_semantics` and `decomposition_attribution`,
  role `field_unit_lead` against `research_desk`, `compliance_or_audit` and `programme_officer`, org family
  `hospital_or_health_provider` against `government_agency`, `utility_or_infrastructure` and
  `local_government`, forum `operations_desk` against `committee_or_panel`, `board_of_directors` and
  `council_or_assembly`, forcing event `incident_or_complaint` against `other`,
  `budget_or_appropriation` and `statutory_or_regulatory_filing`, and context artifact `operations_log`
  against `register`, `filed_standard` and `close_out_summary`. Gate `signal_vs_noise_or_hold` rather than
  `method_or_model_selection` also keeps the draw clear of the `repeat.gate_g` and `overuse.gate_g` WARNs the
  update predicts, 8 of the last 12 carrying that gate. **`org_family` is the one axis that was redrawn and
  the honest label is the one that passes, not the other way round:** `government_agency` BLOCKed against
  task471 and a New Zealand public health unit genuinely sits inside the district health service.

- **Architecture 15, the one-benchmark-per-case shape itself, screened to a measured refusal
  (2026-10-23). Nothing drawn, no card registered, no file in `target/` or `golden/` touched.** The
  resume line this pass was handed ("a second file supplying one benchmark per case, not one for the
  cluster") was tested as algebra rather than as three arbitrary candidates, and the shape has a real
  window that the per-case quantity cannot reach. Harness in the builder's scratch directory
  `<scratch>/a15_194/`: `verify_floor.py`, `screen_c1.py`, `screen_pincer.py`, `screen_heavy.py`,
  `screen_joint.py`, `screen_perworld.py`, `screen_last.py`, `screen2.py`, every one rerunning
  byte-identically.
- **The floor law verified and one clause of it corrected.** For `log designed = log reflex - log factor`
  the minimum of `corr(log reflex, log designed)` over the coupling is exactly `sqrt(1 - rho^2)`, attained
  at a coupling of plus or minus rho and not at the reciprocal (that stationary point returns zero and is
  unreachable below rho of 1). Reproduced at 0.9798, 0.8773 and 0.6000 for rho of 0.20, 0.48 and 0.80,
  with the reflex taking the top candidate 79.0, 51.5 and 21.2 per cent of the time over 600 redraws of 40
  candidates. **The practical correction: a factor coupled NEGATIVELY to the base, which is the intuitive
  "the under-counted cases are the big ones" direction, returns a correlation of exactly 1, so that
  direction makes the reflex more rank-equivalent rather than less.**
- **The aggregation finding, which is this pass's own and closes the shape from the arithmetic side.** The
  decision is at candidate grain and the correction is at case grain, so the decision's own aggregation
  averages n per-case factors and cuts their log dispersion by about the square root of n: measured
  `sd(log f)` at case grain 0.285 against `sd(log F)` at candidate grain 0.0676 at n of 2, and 0.289
  against 0.0265 at n of 120. **So the shape that passes screen 1 by construction (a factor of about 1 on
  no candidate, measured share 0.00) fails the floor by construction**, and the two are different screens.
- **Candidate C1, the clause's own licensed form, dead four separate ways.** Each case's own observed span
  as the correcting duration, `Q = D sum(y_i/d_i)` against the pooled exposure offset `D n sum(y)/sum(d)`,
  which is the Poisson maximum likelihood with a log-span offset and is the one-group-by route. The
  algebra is exact: `Q - B1 = n cov(y, D/d)` within the candidate, so the construction is the group-by
  plus a within-candidate covariance and is not affine in it. It does not reorder anything. Over nine
  cells of events-per-case 0.9 to 21.4 by coupling 0.8 to 3.0, rho never exceeded 0.120, the floor never
  fell below 0.9926, `corr(log B1, log Q)` ran plus 0.9944 to plus 0.9993 and the count form plus 0.9902
  to plus 0.9956, every reflex named the golden as often as the designed route did (0.75 to 1.00), and **0
  of 9 cells passed, then 0 of 45 over a wider sweep.** Independently dead on Gate C: the enumerated
  family spreads the graded figure 679.46 on a level of 1,203.15, 56.5 per cent of the figure, and the
  **standing family alone (per-case sum, precision-shrunk per-case, trimmed per-case, strata of the span)
  still spreads it 46.32, 3.8 per cent of the figure and 463 times a printed precision of 0.1**, which is
  architecture 3's death in new nouns. Independently dead on readability: the only thing that rules the
  pooled route out is a within-candidate regression of the per-case rate on the per-case span, which is
  the hygiene battery.
- **The window, measured, and it is real.** Requiring rho at or above 0.80 means
  `sd(log f) >= 0.80 sqrt(n) sd(log Q)`: at `sd(log Q)` of 0.35 that is 0.48 at n of 3, 1.40 at n of 25
  and 1.98 at n of 50. Counting the share of worlds in which all seven requirements hold at once (realised
  correlation at or under 0.80, the designed route naming the golden in at least 38 of 40 record redraws,
  the golden 4th to 8th of 12 under the raw reflex, no reflex ever naming it, each reflex's own top
  clearing its runner-up by 1.15x, designed margin over the designed figure's coefficient of variation at
  or above 1.15, and the standing family unanimous), the sweep gives **0 of 40 worlds at `sd(log f)` of
  1.3, 2 to 5 at 2.0, 4 to 10 at 2.5 and 8 to 12 at 3.0, best 12 of 40 at n of 25.** A passing world reads
  rho 3.61, realised correlation plus 0.151, designed 40 of 40, every reflex 0 of 40, golden 5th of 12,
  rung clearances 1.38 and 2.02, margin over coefficient of variation 3.5, standing family 40 of 40. **So
  the dial is not one-ended here, which is new on this number: what closes the window is the realisability
  of the per-case quantity, not the ladder.**
- **The pincer that closes it, and the two jaws meet.** The only per-case quantities carrying
  `sd(log f)` at or above 1.4 are unbounded magnitudes, measured at 2.00 and 2.80 for a loss severity and
  2.07 for a network reach; **every quantity the surviving clause licenses is bounded by the window, the
  roster or the contract and sits under the requirement: a window share 0.38, a coverage share 0.71, an
  inclusion probability from a daily capacity 0.57, an opportunity count of 1 to 20 at 0.79, a duration in
  days 0.89, a currency amount capped by a contract 0.80.** And an unbounded magnitude is exactly what
  task198's filed intensity law refuses, because converting intensity into the decision's own quantity
  needs an exponent the record does not carry (2.55 distinct designated classes of 5 there, the graded
  figure spread 107.9 per cent of its level). The third jaw is the retraction of the identity clause: a
  per-case quantity that is a shipped column makes the target shipped-determined, so the designed
  construction is the cheapest group-by route. **So the floor law and the intensity law are two jaws of
  one pincer on step three's shape, and the dispersion the first demands is available only from the
  inputs the second refuses.**
- **Two candidates refused before a harness, on the two screens that are cheaper than one.** An exact
  per-case inclusion probability from a capacity or queue identity is refused on algebra: an exact design
  weight is a property of a sampling cell that both files carry (the day, the unit, the stratum), so the
  one-group-by on that cell reproduces it exactly, and the one form that is genuinely per case is a filed
  design weight, which is rule application and is task190's architecture 3 with its Gate B death. An
  unobserved heavy-tailed per-case COUNT recovered with no free parameter, which is the one corner the
  arithmetic leaves open at `sd(log f)` of 1.43 to 2.07, is refused on the corpus: `guard.py slots` on the
  setting's nouns returns **task201 line 133, where "each interruption's interrupted customer-hours as the
  customers behind the device times the hours without supply" is the DEFAULT PATH and the `SF1` row, and
  task183's ask 2 on the same construction.** Run on the mechanism's nouns the same screen returns
  nothing, which is the lexical blind spot for the seventh measured time; the setting run was made before
  the first harness this pass, as the skill now requires, and it cost one command.
- **What a later pass needs, stated so it is not paid for twice.** The window is `sd(log f)` of 2.5 to 3.0
  at about 25 cases per candidate, and a candidate must satisfy four clauses at once that nothing on file
  yet does: the per-case quantity is UNOBSERVED (else choosing it over the plain count is the estimand's
  outcome and the WHAT screen takes it), it is recovered with NO FREE PARAMETER (no exponent, lag, decay or
  distribution family), it is UNBOUNDED enough to carry a log dispersion of 2.5, and it is not a reach
  through a network (spent as task201's default path). The first measurement such a candidate makes is not
  a separation: it is `sd(log f)` on its own clean truth and then the realised `corr(log reflex, log
  designed)` at its world's own coupling, because the coupling's sign is world-specific and a prototype
  that draws the factor independently of the base flatters every candidate of this shape.

- **Architecture 16 opened (2026-10-23), on the shape task125 shipped this morning rather than on any
  per-case correction. Record written as the pass runs.** The brief hands this slot the generalisation of
  task125: a change acts on a unit that is NOT the unit the data is reported at, its effect propagates
  through a structure the organisation's own process imposes (a rotating panel, an enrolment cohort, a
  queue, a replacement or maintenance cycle, a vintage, a contract term), so each reported period is a
  mixture of affected and unaffected units whose proportions move, and the graded object is the PATH of the
  distortion over periods rather than a ranking. Harness in the builder's scratch directory
  `<scratch>/a16_194/`.
- **The per-case-correction test, written out first because this slot's whole history is in that family
  and the brief requires it explicitly. The shape is NOT in it, and here is the algebra.** Write the graded
  quantity for reported period `t` as `P(t) = R_pub(t) - R_cf(t)`, where `R_cf` is the same published
  estimator on the units the change would have left. Decomposing over the cohorts `c` the structure holds
  at `t`, `P(t) = sum_c w(c,t) * delta(t - c) * 1[c >= T]`: `w(c,t)` is cohort `c`'s observed share of
  period `t`'s reporting population, `delta(a)` is the per-cohort contrast at position `a` in the
  structure, and `T` is the first affected cohort. **Three properties decide the test.** (a) The
  correction is ADDITIVE in cohort-position cells, not an observable divided by a per-case factor: there
  is no `observed = base * factor` per case anywhere in it, so the floor `sqrt(1 - rho^2)`, the
  one-over-root-n averaging law, the floor-versus-precision pincer, the geometric-mean route and the
  dispersion ceiling have no term to bind. (b) The latent object is a PROFILE over positions, a vector of
  length L shared by every cohort, not one factor per case, so there is no per-case dispersion to measure
  `sd(log f)` on. (c) There is no candidate ranking at all, which is what every one of the six laws is
  stated about: they bound `corr(log reflex, log designed)` across CANDIDATES, and this object has one
  reporting series. **The one way back into the closed family, named so it can be checked on any
  candidate: if the graded figure were a per-unit level recovered as an observable over a per-unit
  factor and the call ranked units on it, all six laws apply.** A path of period-level distortions, each
  a weighted sum of additive contrasts, is not that. Verified against the generating process below rather
  than left as an argument: the harness prints `sd(log f)` as undefined because no per-case factor exists
  in the model, and the decision has no candidate set to correlate over.
- **The PATH object is real and this pass confirms the brief's point 2 before it kills the shape.** Candidate
  V, the strongest instance the shape allows, was prototyped on one generating process (a distribution
  network's four-year vegetation clearance cycle, 1,200 feeders, 44 quarters, a narrowed clearance envelope
  issued for four quarters from quarter 20, a narrow clearance behaving like a wide one three quarters older,
  faults Poisson on the resulting intensity; the clearance regime, the position in the cycle, the intensity and
  the counts all come from that one process rather than from independent draws). The published indicator's
  distortion path on the clean truth runs 0.0261, 0.0389, 0.0675, 0.1527, 0.2337, 0.1632, 0.1746, 0.2862,
  0.3864, 0.2490, 0.2516, 0.3947, **0.5152**, 0.3231, 0.3192, 0.4915, 0.4786, 0.2025, 0.0935, 0.0000 faults per
  100 circuit-km from quarter 20 to quarter 39, so it **peaks nine quarters after the last narrowed clearance**
  and reaches zero only five years after the change. **Every reflex lands wrong in a different direction, as
  predicted:** attributing to the reporting unit files 0.0713 for the four quarters the spec was issued and
  **0.0000 at the peak** (root mean square error 0.1922 against a live level of 0.2552); carrying the first
  period's difference forward files 0.0261 for ever, understated from quarter 22 on and never decaying (0.1790);
  share times a mean effect files a flat 0.1092, overstating quarter 20 and understating the peak **4.7 times**
  (0.1379); holding the weights fixed files 0.1092 past the point the cycle has cleared it (0.1360).
- **And the shape dies on the cheapest licensed route, measured, which is the kill and it is structural rather
  than particular to this world.** One join of the fault record to the clearance register, one two-way group-by
  on (regime of last clearance, quarters since clearance), one reweight by the register's own composition
  reproduces the golden path at **root mean square error 0.0072 and maximum absolute error 0.0170 on the clean
  truth** (2.8 and 3.3 per cent of the path's own level), and at **0.0393 and 0.1053 on the realised counts**.
  That route is not a clever construction: it is the opponent's first group-by, and on this ground it is also
  the field's own standard output, the vegetation-fault rate by time since clearance. So the designed route and
  the cheapest licensed route are **one route**, and the decisive step is not silent.
- **The linkage trichotomy, which is why that result generalises and is not a property of a shipped register.**
  For the path to be computable at all the mixture weights `w(c,t)` must be recoverable, so each reported row's
  cohort must be derivable, and there are exactly three ways it can be. **(i) The reported row carries the
  cohort or the regime directly** (a vintage column): one group-by, dead as above. **(ii) The reported row
  carries a unit key and a register maps unit to cohort and regime:** one join plus one group-by, and a join is
  one line, so the cost is identical to (i) and the measurement above is of exactly this case. **(iii) The
  reported rows carry nothing that identifies the unit** (aggregate-only reporting), so there is no
  within-period contrast between affected and unaffected units and the position profile can be identified only
  from the published series itself, which is the quantity the call is about. Measured: a cubic trend with
  seasonal terms reproduces **90.5 per cent** of the distortion path's variance over the live window (a cubic
  alone 74.9 per cent), so the distortion is indistinguishable from a smooth real deterioration using the
  series alone, and identifying it from the series assumes the answer. **There is no fourth case.** task125
  sits in case (ii) and shipped because a true operational sentence in its own field instruction (telephone
  interviews at waves 2 to 5 unchanged) made the one-line join look pointless. **That is a device, a true
  sentence pointing the wrong way, and `stumping` Part 6 licenses re-skinning a device and never a driver.**
- **The forward-facing form is the one configuration that escapes the group-by, and it dies on the hygiene
  battery and on this slot's own architecture-1 closure.** Set the as-of so the affected cohorts have reached
  only positions 0 to 7 while the forward path needs positions 8 to 15: the group-by cannot supply the late
  positions, so the contrast must be **transported**, and that is a real residue. The enumerated transports
  (an age shift, a constant multiple, a constant additive offset, linear in position, proportional to position)
  spread the forward graded figures by a mean of **1.9345 and a maximum of 2.2991 over 20 worlds, 193 printed
  units of 0.01 and 3.6 times the true forward peak of 0.5351**, and they disagree on which quarter the
  distortion peaks (28, 32, 35, 35 and 36 against a true 32). **But the record selects one of them in 20 of 20
  worlds:** excess Poisson deviance over the best fit is 723 to 1,417 for the constant multiple, 663 to 1,376
  for linear in position and 7.6 to 30.4 for the constant additive, against a bar of 4.0, with exactly one
  transport inside 2 log-likelihood units in **20 of 20** worlds. The designed route then recovers the offset
  at **2.993 plus or minus 0.177 against a true 3.0** with a forward-path maximum error of 0.0253. So the
  standing family is unanimous and Gate C would hold, and the decisive step has **moved off the brief's own
  step**: it is no longer which unit the change acts on, which the register gives away in a column, but which
  functional form carries the contrast to positions nobody has observed. **Fitting two forms and comparing
  their deviance is the hygiene battery**, readability test 5, and it reaches the golden in 20 of 20 worlds.
  Independently, a fitted counterfactual whose form is selected by the record is architecture 1's family, which
  this slot's note closes outright; architecture 1's own rule is satisfied here (the forms ARE separated, at
  663 to 1,417 against architecture 1's likelihood ratio of 1.02 to 1), so reopening it is an author decision
  and not a builder's, and it is recorded as an escape rather than taken.
- **The abstraction test and the guard both refuse the shape, and the guard's refusal is mechanical.**
  `guard.py check` on the probe card (`<scratch>/a16_194/probe.json`, PROBE ONLY, not registered) returns
  **BLOCK `test.same_puzzle_older` against task125 (v2)** (decisive gap, decisive pattern and decision type all
  repeat) and **BLOCK `test.same_driver_older` against task125 (v2)** (decisive gap, decisive pattern and Gate G
  mechanism all repeat), with `driver.near` at **0.19 against task125, the nearest driver on file by three
  times over** (next 0.06, task129). Four further BLOCKs sit beside them and two are not clearable by
  relabelling: `ban.strategy` composition_mix and `ban.pattern` G6 both against task179, plus
  `overuse.strategy` at 3 of the last 12. The structural tests take a one-line differentiation, and **the line
  cannot be written honestly**: stripped of nouns task125's own card driver already reads "the unit the change
  acts on is the intake and not the period, so each period's distortion is a re-estimate on that period's own
  mix of filtered and unfiltered intakes ... while the first-period gap repeated while the change lasts files
  no change at all and the same gap applied at every position overstates every period", which is the candidate
  including its reflex table. **And task125's `Lesson:` line states the brief's generalisation verbatim**, so
  any faithful instance fails its own `Lesson:` test, which asks what a model learns that no build on file
  already teaches. Redrawing gap, pattern, Gate G or decision type to clear the mechanical tests would be
  writing a card to pass, which `fingerprint` Part 4 names as the failure mode.
- **ARCHITECTURE 16 IS A MEASURED REFUSAL. Nothing drawn, no card registered, no file in `target/` or
  `golden/` touched.** Harness in the builder's scratch directory `<scratch>/a16_194/`: `screen_v.py`,
  `screen_fwd.py`, `screen_sep.py`, `screen_agg.py`, each rerunning byte-identically (md5
  `e10628e0541245d3dfb5812ba2cb0e3b`, `289dd7ca1c674ff8caa865edf781fbba`, `cb12a0c7fe08eb72ac7154485da55188`
  for the three that print a digest).
- **What a later pass needs, stated so it is not paid for twice, and the general law first.** **For a change
  acting on a unit coarser than the reporting unit, the decisive construction is one join plus one two-way
  group-by on (regime, position) plus one reweight, because the mixture weights have to be shipped for the path
  to be computable and the position variable is shipped with them.** The shape therefore carries a stump only
  where a device hides that join, which is task125's and is spent, or where the positions the answer needs have
  not been observed, which moves the decisive step onto a transport and into architecture 1's family. **Two
  directions this pass did not spend a screen on.** The first is the path's **turning point** rather than its
  levels, graded as the period in which the distortion peaks: the transports disagree on it (28, 32, 35, 35,
  36 against 32), it is a discrete level-dependent object rather than a monotone summary, and the standing
  family here is one member so it would be determinate; it is still the same driver, so it needs a ground
  where the propagation is not task125's. The second is a structure whose **position is not registered at all**
  and has to be reconstructed from each unit's own history, which makes the position an estimated quantity; it
  is expected to die on the parametric horn by this lane's standing law, and nothing on file measures it.
- **2026-11-03, the healthcare provider-quality risk-adjustment world abandoned for good (architectures 1 to 16).** Sixteen architectures in one world, the last refused because the propagation shape is task125's driver; under one architecture per world the slot moves to another client domain, dataset and generator, keeping the objective and the number.
- **2026-11-03, architecture 17 candidate A, a closed landfill's groundwater with three co-located sources (physical-environmental-sciences / environmental-monitoring-exceedance), dead before a card.** Each compliance borehole's chloride, sodium and boron rise split across the landfill leachate, a composting tenant's lagoon and a highways salt soakaway by their own compositions. `guard.py check` BLOCKs on test.same_driver_older against task121 v5 (gap objective, G6, decomposition_attribution); task263 already ships mass-balance unmixing of co-located sources in the same client domain (nearest 0.07, the same insight in other nouns); and task121's own nitrate-source-share screen is on file as dead ("any column that measures the process announces it"). A strong analyst also reasons the split from the indicator pattern without the mixing solve.
- **2026-11-03, architecture 17 candidate B, dyadic coverage weighting of genomic TB transmission links (epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection), dead on the pricing sequence before a card.** A link shows in the close-pairs list only when both cases were sequenced, coverage being a district property. Observed links for a district are its own coverage times the partner-coverage-weighted true links, so dividing by own coverage (the obvious correction) cancels that factor exactly; on the intended world the raw rate names another district but the clustering proportion, the own-coverage and the squared-coverage corrections all name the golden first, the own-coverage rung at 1.04x against the 1.15x floor. The flip and the margin are financed by one quantity, the coverage spread, the bound architecture 3 died on. **General screen: a decisive step that is a product of two independent detection or sampling chances cannot carry a ranking when the record identifies each unit's own chance, because the obvious correction factors one chance out exactly and the residue is bounded by the spread of the other.** The axis cell it measured clear (gap objective first, G17 decisive, pick_one_of_n, shape 07, WARN only) stays usable for another mechanism.
