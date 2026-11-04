# task488 design note

Architecture 2, drawn 2026-11-04: a re-root of the number into a new world, dataset, generator and prompt shell.
Architecture 1 (commissioning new items below the Approaching cut from a consortium's adaptive item bank) was found
spent at the 2026-11-02 re-check; its line is in `## Tried and rejected`, its build files are cleared from the folder
and kept in history, and its shipped pack (target.zip bfca5a21) stays at the portal, pending. This build replaces it
at ship. No seed: the world, the decision and the quantity are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task488.json`, architecture v2, registered 2026-11-04T07:59:59Z, v1 in
  its lineage with its fate and its prompt shell (how-many, put, csv+docx+xlsx) in `lineage_shells`. `guard.py check`
  on the filed card: WARN only. `repeat.gate_g` (etl_conformance repeats task476 v3 and task461 v3) is answered here:
  the label is the honest one, the stump sitting in a conformed recall list and section drain plan judged against the
  operator's quality procedure, on another driver in another world. `test.same_puzzle_older` against task270's ninth
  architecture (objective, G13, designation set) is a NOTE, differentiated on the card: that build read a variability
  standard at one interval from readings at others; nothing here is an interval or a variability. Nearest drivers on
  file 0.07 (task307's lineage) and 0.05 (task201 v2, task98 v1); none is a displacement front in a pipe network.
- **Window at the draw:** task192 v4, task476 v3 and task461 v3, so the strategies grain_or_unit,
  decomposition_attribution and other, the forums operations_desk, executive_team and customer_or_counterparty, the
  forcing events shift_or_daily_cycle, statutory_or_regulatory_filing and audit_or_inspection, the organisation
  families local_government, agriculture_or_food_producer and other, the roles other, compliance_or_audit and
  portfolio_manager, the artifacts filed_standard, register and operations_log, and the shapes 15 and other are off
  the table; record linkage and emissions-inventory BLOCK on pairing and subdomain.
- **Pairing:** Supply Chain & Logistics (house domain) / transportation-network / Data Extraction & Conformation (ETL),
  in its client domain General Statistics & Data Science, task type data-integration-record-linkage-entity-resolution,
  which serves ETL. The call is read from a conformed set: the fuel farm's tank line-ups, the hydrant network register,
  two into-plane agents' fuel tickets in two layouts, the truck rack's loading log and the refuellers' records
  integrated into the recall's notification list and the operator's drain plan.
- **Why this cell:** the 2026-11-04 map of the six ETL task types (task476's `## Tried and rejected`, S3.1 to S3.60)
  closes payment claims, census and register quality, official time series and test equating on mechanism, and its one
  survivor was a physical mechanism in a data-integration world; record linkage and emissions-inventory sit in the
  window, so the number moves to a house world that inherits data integration, as task472 did. Twenty-five screens of
  this draw, each one line below, died before this one was priced.
- **Shape:** 07, a grid of cells: the register's eight sections, each holding the batch or clear, with the litres
  standing in each that holds it (8 and 3); the refuellers, each holding it or clear, with the litres in each (4 and
  4); the airlines the refuellers served, each with the batch litres those uplifts delivered (6); the uplifts to
  notify, hydrant and refueller (2); the return's conformed fields (UTC starts, litres at 15 C) and the schematic's
  marked sections (3): about 30 criteria from the answer's structure, none from stacked asks.
- **Strategy:** population_selection (exposure): which sections and uplifts the recalled batch reached is set by the
  volume each segment of the hydrant passed downstream after the batch entered it, not by the window the tank line-up
  records. Decisive generator G13 (each pit's own exposure window against the tank's line-up window), with G3 (the
  line-up record against the physical delivery) and G19 (the conformed list against the procedure). Gate G
  etl_conformance.
- **World:** Canada, Pacific time. Windrell International Airport's fuel farm, truck loading rack and hydrant system
  belong to the Windrell Fuel Facilities Corporation, which its member airlines own, and are run under contract by
  Pellacre Aviation Services, the Operator; two into-plane agents fuel aircraft from hydrant dispensers at the pits and
  from refuellers loaded at the rack. Jet A-1 arrives by products pipeline in batches; each batch is received into one
  tank, settled, recertified and released. Names are provisional until the near-name check at stage 3.
- **Forum, forcing event, organisation, role:** committee_or_panel (the corporation's fuel quality committee approves
  resumption after a quality incident), incident_or_complaint (the supplier's recall of a released batch),
  cooperative_or_member_body (an airline-owned fuel facility corporation), field_unit_lead (the Operator's fuel quality
  manager at the site, Natalie Daugherty; William Hopkins chairs the committee). Personas from `guard.py names --geo
  Canada --seed 488`; the other names it drew warn on first names held by older builds, so the logs carry initials.
- **Forcing fact:** batch J-26-1187 was released from Tank 3 and lined up to the hydrant and the truck rack at 06:00 on
  Tuesday 13 October 2026; the rack moved to Tank 1 at 12:20 and the hydrant at 15:40. At 05:12 on Wednesday 14
  October the supplier recalled the batch (FAME far above the specification), and the duty supervisor suspended
  hydrant and refueller fuelling at 05:30. The committee meets at 08:00 to approve what is drained before fuelling
  resumes and which aircraft operators are told. The call faces forward (the drain and the notices are still to do);
  its quantity is the state at the 05:30 suspension. As of 14 October 2026, 07:30 (the `--asof` for `leak.py`).
- **Data-native sentence:** the hydrant is always full and its branches end at their last pit, so fuel moves in a
  segment only while a pit downstream of it draws; the busy piers took the batch soon after the main turned over and
  were flushed by evening, while the cargo apron and the remote stands drew a few uplifts a day, took the batch hours
  after it reached their junctions and still held it past their first pits when fuelling stopped, Pier B's far stands
  closed for resurfacing with the batch in the pipe under them, and the maintenance base, which drew nothing on
  Tuesday, never took it at all.
- **Abstraction sentence:** "a substance entering an always-full branched network reaches and leaves each outlet as the
  draws downstream of each conduit displace it, so the outlets that drew little received it late and still hold it."
  No build on file carries a displacement front through a network; the nearest drivers sit at 0.07.
- **The WHAT screen.** Population: every uplift that delivered fuel from the batch, in any quantity, and every hydrant
  section and refueller holding fuel from it at the suspension. Outcome: the batch litres standing in each and taken in
  each uplift. Window: from the batch's release to the 05:30 suspension. Unit: litres. Comparison: none beyond any
  against none. The decisive step settles none of them: it is how the records show where the batch went.
- **Deliverables:** `j26-1187_recall_uplifts.csv` (the airlines' notification list and the supplier's recall return,
  one row per uplift that delivered batch fuel) and `hydrant_resumption_plan.pdf` (the committee's plan: each section
  and refueller to drain with the batch litres in it, a schematic of the hydrant marking where the batch stands, the
  refuellers' batch litres by airline).
- **Shell:** question form `where` (the decision is a set of places), second sentence opening on the hold ("Nothing
  reopens"), the rounding sentence opening on "Round", deliverables csv and pdf; `voice-check.py task488` PASS with
  every shell class under its corpus cap. Architecture 1's shell (how-many, put, give, csv+docx+xlsx) is in the card's
  `lineage_shells`; the card's `question_form` moves from `which` to `where` with the stage 3 card update.
- **Sources, one line each:**
  - Airport hydrant practice: an always-full pressurised network from the fuel farm's pump station to pits on the
    apron, its line fill held by section in the operator's register, fuel delivered by into-plane agents through
    hydrant dispensers whose tickets name the pit; product changes are reckoned in line fills.
  - The quality-control practice of the jet fuel industry: a released batch later found off specification is traced
    to every aircraft that may have received it and removed from every part of the system holding it before that
    part is used again.
  - `dataset-generation/references/layer1-messiness.md`: two agents' exports in two layouts (gross litres at fuel
    temperature and local time against net litres at 15 C and UTC), pit identifiers in two schemes, a re-issued
    ticket, a meter register reset at a proving, tank line-ups in the farm's own shift log.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`, read in full at the draw) and the slot notes
    (`guard.py slots` on hydrant, line fill, plug flow, displaced, dead leg, branch): no build moves a substance
    through a network by volume displaced.

## Default path

Measured on the generator's clean truth (seed 4882, refueller fork 14; `generator/model.py`), every figure re-derived
from the cut pack by `generator/solve.py` at stage 3.

1. Read the recall notice and QM-09: every hydrant section and refueller holding product from J-26-1187 when fuelling
   stopped is drained before use, and every uplift that delivered product from it, in any quantity, is notified.
2. From the farm shift log and the SCADA valve states: Tank 3 was on the hydrant pumps from 06:00 to 15:40 on Tuesday
   and on the rack pump from 06:00 to 12:20.
3. Conform the two agents' ticket exports (Corbel's in local time with gross and 15 C litres and pit tags, Northgarth's
   in UTC with 15 C litres and stand numbers) to one list of hydrant uplifts keyed to the register's pits, dropping
   the voided ticket.
4. Apply the field's product change reckoning: a hydrant's fuel has changed over once one line fill of the whole
   network (398,781 L, the register's total) has passed the pump station's meter after a line-up change. The SCADA
   meter passes it at 09:27 after the 06:00 change and at 18:19 after the 15:40 change, and the Operator's product
   change checks at P-A01 (09:40 on Tank 3's density, 18:36 on Tank 1's) confirm both.
5. So every pit dispensed the batch from 09:27 to 18:19 and the hydrant held none of it by Tuesday night; the
   hydrant uplifts drawing in that window are the ones to notify.

Ends on: no hydrant section holds batch fuel at 05:30 and 64 hydrant uplifts took it.
Golden: Pier B (6,600 L), the cargo apron (11,000 L) and the remote stands (3,600 L) hold batch fuel at 05:30, and 73 hydrant uplifts took it.

## Stump sentence

The product change reckoning the Operator's own checks confirm files the hydrant clear by 18:19 and 64 uplifts to
notify, because one line fill through the pump station's meter turns over only the main and the busy piers: fuel in
each segment moves only while a pit downstream of it draws, so the cargo apron's far segments, the remote stands and
Pier B's closed tail still hold 11,000, 3,600 and 6,600 L of the batch at 05:30 and 73 hydrant uplifts took it.

## Three rules

- **Task type:** general-statistics-data-science's data-integration-record-linkage-entity-resolution, which serves
  Data Extraction & Conformation: the call is read off one conformed set integrated from the farm's line-ups, the
  network register, two agents' ticket exports in two layouts and clocks, the SCADA historian and the check records.
- **Domain test:** the deciding quantity is the position of the recalled batch in each segment of the network at the
  suspension, and the field's own estimate of it is the product change reckoning in line fills against the pump
  station's meter; the call changes when that reckoning replaces the per-segment front, which is what the pits'
  sampled densities measure.
- **Swap:** "which wards of the hospital and which drug trolleys still held doses from recalled lot 1187 at 05:30" has
  no always-full pipe, no segment that moves only when its own outlets draw, no line fill and no front left standing
  in a branch that drew little; the reckoning and the fronts stop making sense.
- **Layer 1:** Corbel's export in local time with gross and 15 C litres and pit tags, Northgarth's in UTC with 15 C
  litres and stand numbers (the agents' own ticketing systems); a ticket voided for a mistyped registration and
  re-issued (Corbel's back office); the SCADA totaliser reset at a meter proving (the farm's historian); segment
  lengths and bores in the register with volumes derived (the Operator's register); tank line-ups in the shift log
  and as valve states (the farm's own two systems); nothing placed to be caught.
- **Layer 2:** estimand identification by exposure (population_selection): which sections and uplifts the batch
  reached is set by the volume each segment passed downstream after the batch entered it, so the methodological
  choice is the unit the front is tracked at (the network, the pit's path, the section, or the segment).
- **Decisive step:** tracking the batch segment by segment, each segment's fuel moved only by the draws of the pits
  downstream of it, rather than reckoning the change by the line fills the pump station's meter has passed.
- **Not semantics:** every field read correctly (the UTC clock converted, the 15 C litres used, the void dropped, the
  stands mapped to pits, the line-up times taken from the log) still leaves the reckoning at 64 uplifts and a clear
  hydrant, because nothing in any field says which segments moved and the batch's position is not a column.
- **Not rule application:** no filed rule or procedure says where the batch went: QM-09 files what is drained and who
  is told, never how the batch's position is found; the enumerated family (the line-up window, one line fill, each
  pit's own path volume, a branch's turnover against its line fill, each section as one pipe, the per-segment front)
  files six answers from none to three sections and 64 to 73 uplifts; the standing family the shipped samples leave
  (72 densities, none of them mispredicted) is the per-segment front alone, at a spread of zero on the sections, the
  litres' 100 L cells and the 73; the ruling-out is quiet, 9 to 22 mispredicted samples per rival in two check sheets
  and a maintenance record.
- **Analyst test:** a strong analyst who conforms every file and applies QM-09 reckons the change in line fills,
  confirmed by the Operator's own checks, and files no section to drain and 64 hydrant uplifts to notify, against
  three sections and 73.
- **Estimand:** QM-09 3.2 and 4.1 (and the supplier's notice RN-2026-031): every hydrant section and refueller holding
  product from the batch when fuelling is suspended, and every uplift into which product from it was delivered in any
  quantity from its release to the suspension, in litres at 15 C, one record per uplift.
- **No decoy:** nothing is planted: no copied block, no memo or briefing arguing the clear hydrant, no hidden rule;
  the product change checks are the Operator's routine record, true where they were taken, and say nothing of where
  else the batch stands.
- **No certified replay:** no certified or published figure is reproduced to recover the method; the samples are
  routine quality checks whose densities the golden explains, not a corpus whose outcomes were set by the method.
- **Lesson:** an always-full branched network is displaced by its outlets, not turned over by its throughput, so a
  product's front is tracked per segment by the draws downstream; no build on file moves a substance through a network
  by volume displaced, and the nearest drivers sit at 0.07.

## Survivor anatomy

- **Actor:** the deciding property (which segments still hold the batch, and when each pit's fuel changed) has no
  column in any file: the register holds segments, the tickets hold draws at pits, the samples hold densities; the
  front is a relation across all three that nothing stores.
- **Link:** the signal is read through the register's from-node and to-node chain, joining every draw to every
  segment upstream of its pit; no key offers it, and no sentence invites a comparison of a branch's draws against the
  segments behind each pit.
- **Reflex:** the field's product change reckoning in line fills sits at rung 0 and files the hydrant clear and 64
  uplifts against three sections and 73.
- **Back-test:** the Operator's product change checks at P-A01, taken after one line fill on each change, show Tank 3's
  density at 09:40 and Tank 1's at 18:36, exactly as the reckoning predicts; the meter's line fills reconcile to the
  tickets' litres on every path.
- **Second use:** every file the decisive step reads is in the pack for its own reason: the register for product
  changes and maintenance, the tickets for billing, the SCADA for the pump station, the agents' check sheets for daily
  quality control, the low point drain record for weekly maintenance; deleting the step removes none of them.
- **Shock:** the batch standing where it does reads as ordinary operation: busy piers flushed, quiet branches drawing
  a few uplifts a day, two stands closed for resurfacing; the golden set (B, E, F) is no interval of any one section
  statistic (sorted by draws after 06:00 or after 15:40, or by draws per line fill after 15:40, it is the 2nd, 3rd
  and 5th of six branches; by line fill the 2nd, 4th and 6th; asserted in `checks.py`).
- **Pins:** QM-09 (the corporation's quality manual) and the supplier's recall notice file the WHAT (what is drained,
  who is told, in any quantity, litres at 15 C, the window from release to suspension, and in 2.3 that a refueller
  holds product from every batch it has received since it was last drained to empty, its contents mixed, which is the
  refuellers' population and says nothing of the hydrant); no filed sentence names a line fill, a turnover, a front or
  a window for the batch's position.

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7
dedicated organ); the reflex row comes from the field's vocabulary for a product change in a hydrant (line fill,
turnover, product change check, flushing).

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the line-up window at every pit (none, 67) | the shift log's line-up times | the SCADA valve states | yes | no | no | yes | no | readable |
| R1 one network line fill through the meter, the field's reckoning (none, 64) | the register's total line fill | the SCADA totaliser | yes | the product change checks agree | no | yes | no | readable |
| R2 each pit's own path volume through the meter (none, 64) | no | the register's lengths and bores | yes, once the path is summed | no | no | yes | no | readable |
| R3 a branch turned over once it drew its line fill after 15:40 (G, 64) | the register's section line fills | the tickets' pit and section | yes | no | no | yes | no | readable |
| R5 each section as one pipe, fed by its own draws (F, 66) | no | no | no | no | no | no: a FIFO per section | no | readable |
| G (decisive) each segment's fuel moved only by the pits downstream of it (B, E, F, 73) | no sentence names a front, a segment's flow or a displacement | no column holds a segment's contents or a pit's change time | no: the reflex reckons in line fills | quiet: the agents' and the drain round's densities refute every rival, but only once each is matched to a certificate at its pit and time; no sheet names a batch, and the product change checks agree with every rung | no | no: a FIFO per segment through the node chain | every file it reads has its own use | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "still standing", "held fuel from the batch" | any quantity of the batch in the section or tank | a material share only | a share floor would drop F's and RF-24's small holdings | QM-09 3.2 and the recall notice: product from the batch in any quantity |
| SF2 | "took any of it" | any uplift whose litres included batch fuel | uplifts mostly of the batch | fewer rows | QM-09 4.1: delivered in any quantity |
| SF3 | the as-of instant | 05:30, the suspension | 05:12, the recall notice | same call: no draw between them reaches B's tail, E or F (asserted) | QM-09 3.2: when fuelling is suspended |
| SF4 | "section" | the register's sections (farm header, main, six branches) | segments or pits | same call at the section grain; the plan lists the segments too | the register's Sections sheet |
| SF5 | the dead legs past each branch's last pit | part of their section, holding the August batch | holding whatever the branch holds | same call (no dead leg holds the batch, asserted) | the low point drain record's densities |
| SF6 | an uplift's draw between its start and end | a steady rate, as the SCADA minute flows show | all at its start, middle or end minute | same sections and litres; the 73 moves by 1, 1 and 1 (asserted) | the SCADA flow steps by each uplift's rate for its minutes (fit within 0.3 per cent, asserted); the judge's pass 1 read this closure as the data's own |
| SF7 | the litres a pipe moves | litres at fuel temperature | litres at 15 C as Northgarth prints them | same call, same 100 L cells (asserted) | convergence |
| SF8 | the idle-pit flushes and the low point drains | draws on the hydrant | ignored | same call (asserted) | convergence |
| SF9 | the line-up instants | the shift log's 06:00, 12:20 and 15:40 | the SCADA valve minute, 90 s either side | same call (asserted) | convergence |
| SF10 | the voided ticket | dropped, its re-issue kept | both kept | one uplift counted twice | Corbel's status and reissue columns |
| SF11 | Northgarth's clock | UTC, converted to local | read as local | fronts and windows shifted 7 h | the export's own header (Start (UTC)) |
| SF12 | one row per uplift | each fuelling of an aircraft | each aircraft | fewer rows | the prompt's asking sentence |
| SF13 | litres at 15 C in the return | each ticket's 15 C litres, the batch's share of them | gross litres | other litres per row | QM-09 3.3 and the recall return's columns |
| SF14 | the hydrant's standing litres | litres of pipe at line temperature | the same at 15 C | same 100 L cells (asserted) | convergence |
| SF15 | "refueller" | the tank vehicle holding the fuel: a rigid refueller or an articulated refueller's trailer | the tractor a ticket names | other refueller names | the equipment register's type and compartment columns |
| SF16 | a refueller tank's contents | one mixed body of fuel: a refueller holds product from every batch it has received since it was last drained to empty | first in, first out (each delivery drawn from the oldest fuel aboard), or each delivery from the latest load | FIFO drops RF-24 and T-35 from the drain list (RF-23 and T-31 only, 6 refueller uplifts against 13) and moves every refueller litre; the latest-load reading moves every litre | QM-09 2.3: "A refueller holds product from every batch it has received since it was last drained to empty, its contents mixed"; both readings computed and the sentence's literal population asserted in `checks.py` |
| SF17 | the batch litres on a hydrant row the batch's head or tail crossed during the uplift | the steady-rate trace on 15 C litres | litres at fuel temperature (Corbel's printed or Northgarth's recovered by Corbel's own correction), the flushes left out, the line-up minute 90 s either side | the 22 partial rows move: the two rows the batch's tail crossed (NG2690219, NG2690240) by up to 2,185 and 2,423 L, CB418385 and CB418386 by 645 and 617 L, the rest by 144 L or less; the sections, their 100 L cells and the 73 do not move | the deliverable answers grade each partial row within its own band (the widest departure plus 250 L, rounded up to 100 L: 300 or 400 L, 900 L for CB418385 and CB418386, 2,500 and 2,700 L for the tail rows) and every whole row within 10 L; the clean truth's readings asserted inside every band, the least room 146 L |
| SF18 | the rack line between the farm valves and the loading arms | it holds 4,222 L (RK-01, the register's rack sheet) of the tank before, which leaves first in the first load after each rack change | every load read as the tank the rack was lined up to at its start | T-35 drops from the drain list, RF-23 and RF-24 move (4,270 and 426 L against 3,070 and 310) and 10 refueller uplifts against 13 | the register's line-fill volume and the shift log's rack change times, no load in progress at either change (both asserted in `checks.py`); the same displacement the hydrant needs |

## Ladder

Every reading priced on the clean truth (`model.py`, asserted in `checks.py` R3 and the route block):
- **Rung 0, the field's reckoning (none, 64 uplifts):** one network line fill (398,781 L) through the meter after each
  change: every pit on the batch 09:27 to 18:19, 5 uplifts notified that took none, 14 that took it missed; 17 of the
  72 shipped samples mispredicted (7 idle-pit, 6 low point drain, 4 shift start).
- **Below it, the line-up window (none, 67):** every pit on the batch 06:00 to 15:40; 14 extra, 20 missed; 22 samples
  mispredicted.
- **Rung 1, each pit's own path volume (none, 64):** 4 extra, 13 missed; 15 samples mispredicted.
- **Rung 2, the section reckonings:** a branch turned over once it drew its own line fill after 15:40 files the
  maintenance base (7,711 L), which drew nothing and never took the batch, and clears E and F (105,447 and 29,306 L
  drawn against 66,227 and 21,815); each section as one pipe files the remote stands alone (711 L) and 66 uplifts (2
  extra, 9 missed), 9 samples mispredicted.
- **Rung 3, decisive (B, E, F; 71):** each segment's fuel moved only by the pits downstream of it: Pier B's closed
  tail (6,587 L, two whole segments), the cargo apron past its first pit (10,996 L, three whole segments) and the
  remote stands (3,625 L); 73 uplifts; every one of the 72 samples reproduced.
- **Heuristics, each a bucket:** the branches the agents flush as idle (E, F, G: G in, B out); the stands closed
  during the batch's time (B alone); a branch whose last uplift took the batch on rung 1's windows (none).
- **Separation:** every rung and heuristic files another section set; the golden's notified set differs from each
  rung's by 11 to 34 uplifts; each rival is refuted by at least 9 samples at 2.0 kg/m3 or more of density at 15 C.
- **Robustness:** the 73 and every sample's reading hold under 15 C litres, the flushes ignored and line-up instants
  90 s either side; the standing cells hold with margins 37, 46 and 25 L; the smallest exposure is 1,268 L.

## Closure table

| Axis | Reading here | Closure |
|---|---|---|
| 1 Population | every section, refueller and uplift holding or taking batch fuel in any quantity | QM-09 3.2 and 4.1, the recall notice; C1 on the 73 |
| 2 Unit of account | sections (register), refueller tanks, uplifts | the prompt names them; SF4, SF12, SF15 |
| 3 Attribution window | release (06:00 Tue) to suspension (05:30 Wed) | QM-09 4.1; nothing draws on the edges that moves the call (SF3) |
| 4 As-of dating | the state at 05:30 | QM-09 3.2; SF3 asserted |
| 5 Version basis | the voided ticket dropped | Corbel's status column; SF10 |
| 6 Denominator | none in the call; the batch share of an uplift's 15 C litres in the return | QM-09 4.1; SF13 |
| 7 Weighting | none | not applicable to a set and litres; asserted none |
| 8 Window length | none beyond axis 3 | not applicable |
| 9 Boundary inclusivity | uplifts straddling a front take a part | C1: the smallest exposure 1,268 L, no uplift at a boundary |
| 10 Rounding path | hydrant litres to 100 L, refueller and row litres to 10 L, each from exact litres; airline sums equal on both paths | the prompt's rounding sentence; asserted mid-bin |
| 11 Tie-break | none | no ranking |
| 12 Maturity and censoring | none | not applicable |
| 13 Order of operations | the rack header before each tank's mix | C1: the golden order is the physical one, asserted |
| 14 Row order | the export orders | C1: the simulation sorts by time, asserted over a shuffled read |
| 15 Duplicate resolution | the voided and re-issued ticket | SF10 |
| 16 Identity normalisation | stands to pits, tractors to trailers | the register's pits sheet; the vehicle log's couplings (SF15) |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | gross against 15 C litres, L/min against m3 | SF7, SF13, SF14; units in every header |
| 19 Code and status semantics | VOID, check types, valve states | the files' own columns; never the stump |
| 20 Integerisation | litres per row whole, sums from exact values | C1: both paths in the same 10 L cells, asserted |
| 21 Clause scope | QM-09 3.2 covers tanks, sections and refuellers | filed scope |
| 22 Forward window contents | none: the call is the state at the suspension, the drain still to do | not applicable |

## Literal reader

Executed word for word on paper and on the clean truth: QM-09 3.2 and 4.1 and the recall notice file the population
(sections, refuellers and uplifts holding or taking batch product in any quantity), the window (release to
suspension), the unit (litres at 15 C) and the record (one per uplift); nothing filed says how the batch's position is
found, so the literal reader must find it, and the only reading every shipped sample confirms is the per-segment front;
every other reading (SF1 to SF16) is either refuted by a quoted sentence or converges on the same sections, litres and
73 (asserted in `checks.py`).

## Oracles

- The Operator's product change checks at P-A01: they agree with every rung, the golden included (the first pit off
  the main changes within minutes), so they confirm the reckoning and arbitrate nothing.
- The SCADA meter against the tickets: the minute flows reconcile with the tickets' litres on every reading; they fix
  the draw profile (SF6) and say nothing about where the batch went.
- The agents' check sheets and the low point drain record: they refute the rivals only through the densities at the
  pits where the front's timing differs, a cross-file reading nothing invites (each sheet's own use is daily quality
  control); no column states a batch number.
- The rack loading log: litres at 15 C per load against each refueller's tickets; it ties under every reading of the
  refuellers and arbitrates nothing.

## Ask sheet

Planning weights 38 / 7 / 55. The call's own construction (the sections, their litres, the 73 hydrant uplifts, and
the refuellers to drain, each named with the rest clear) is scored with it: the prompt asks where the batch stands
refueller by refueller. The asks are the refueller figures QM-09 3.2 and 4.1 require beside the drain list: A, the
batch litres each refueller holds at 05:30 (four litres); B, the refueller uplifts that delivered batch fuel (the
return's refueller rows, 13); C, the batch litres the refuellers delivered to each airline (6 figures).

- **Ask A, the refuellers holding the batch:** H18 home: what is drained before reuse (QM-09 3.2). Path, the columns
  the golden reads: the rack loading log (tank_unit, load_date, start_local, loaded_l_15c), the equipment register
  (Fleet no, Equipment type, Compartments, Usual trailer), Corbel's tickets (ticket_no, tkt_status, tkt_date,
  start_local, loc_code, unit_no, customer_name, litres_15c), Northgarth's tickets (Ticket No, Unit ID, Operator Name,
  Start (UTC), Vol @15C (L)), Northgarth's vehicle log and Corbel's equipment log (event_code, unit, remarks, qty_l
  and the time each), the shift log's rack line-ups and the register's rack line. Primaries: Northgarth's tickets
  name the tractor and the equipment register pairs N-7 with T-31 as of 5 October, while N-7 left T-31 at the
  workshop at 11:52 and coupled the spare T-35 at 11:58 (the vehicle log), so the fuel N-7 delivered after that came
  out of T-35 (a label stored before a silent switch, D7); Corbel pumped 3,843 L from RF-23 into RF-24 at 12:50 before
  RF-23's hose reel repair, recorded only in its equipment log (a channel no join reaches, D4). Hazards: the rack line
  (4,222 L) carries the fuel of the tank before into the first load after each line-up; the tanks start from the
  weekly Monday dip, two days of loads and tickets before the batch. Pin test: the asking sentence pins the instant,
  the unit and the rounding; no pin names a coupling, a transfer or a rack line.
- **Ask B, the refueller rows:** H18 home: the notification list (QM-09 4.1). Same path and primaries: the uplifts
  RF-24 made after the transfer carried the batch, N-7's afternoon uplifts carried T-35's share and not T-31's.
- **Ask C, the airlines' refueller litres:** H18 home: the quantities each operator is told (QM-09 4.1). Same path;
  the two primaries move disjoint blocks: the transfer moves Orvelle, Brightwing and Tallowmere, the pairing moves
  Northcove, Sablewood and Vireo (`checks.py` and `ceiling.py`).
- **Main population zero-counts:** no refueller row is a hydrant draw (asserted in `checks.py`); the hydrant call reads
  the register, whose rack sheet the asks also read, and nothing else of the refuellers'.
- **Silence:** under the cracker's keying no tank runs below empty or over its capacity at any instant, and no file
  dips a refueller after the weekly Monday dip, so nothing inconsistent shows on the careful route (asserted).
- **The full includer:** a response that rebuilds every trailer's state across the couplings, books the transfer and
  carries the rack line keeps all three asks; each primary's remedy is a state rebuilt across two systems' keys, and
  the layer carries no third device from another family, a known limit recorded here.
- **Realism:** articulated refuellers whose tractor carries the pump and meter, a trailer left at the workshop, a
  defuel into a sister vehicle before a repair, and a spare trailer on the line are ordinary into-plane operations.
- **Referee:** none; every ask figure is recomputed on `generator/solve.py`'s own path.

| Ask figure | Cracker (the equipment register's pairing, the transfer unbooked, the rack line carried) | Golden | Cracker |
|---|---|---|---|
| A: RF-23 batch litres | 5,030 | 3,070 | miss |
| A: RF-24 batch litres | 0 | 310 | miss |
| A: T-31 batch litres | 1,140 | 14,680 | miss |
| A: T-35 batch litres | 4,220 | 2,340 | miss |
| B: refueller uplifts that delivered batch fuel | 7 | 13 | miss |
| C: Brightwing Airlines | 3,220 | 4,130 | miss |
| C: Northcove Air | 15,890 | 10,740 | miss |
| C: Orvelle Airways | 0 | 240 | miss |
| C: Sablewood Air | 12,010 | 7,550 | miss |
| C: Tallowmere Air | 2,510 | 3,020 | miss |
| C: Vireo Airlines | 2,380 | 330 | miss |

Pair ceiling: 30.4 (the cracker 42.1: the hydrant call landed, the refuellers to drain named but for RF-24, 12 of
13 call criteria and no ask figure; the mirror 18.7 at rung 0, which clears the hydrant at 18:19, notifies 64 uplifts
and drains RF-23 and T-31 only, 4 of 13 call criteria and no ask figure).
Mirror leakage: 0.0 per cent of ask weight (the mirror reads the refuellers the cracker's way and the rack by its
line-up times, and keeps nothing).
Measured by: generator/ceiling.py, on the cut pack (target.zip of this build).

## Leak review

`leak.py task488 --asof 2026-10-14`: REVIEW, no LEAK. Each REVIEW line, ruled here:
- Sweep 4, `QM-09_product_quarantine_and_recall.pdf`, `farm_shift_log_2026-10-12_14.pdf` and
  `recall_notice_RN-2026-031.pdf`: the terms they share with the stump paragraphs (register, network, product,
  change, quality, record, samples) are the organisation's ordinary words for its own procedure, log and notice;
  none names a segment's draws, a front, a displacement or the batch's position. Harmless; ruled here and never
  handed to the reader.
- Sweep 6, `corbel_fuel_tickets_2026-10-12_14.csv` and `northgarth_tickets_20261012-20261014.xlsx`: the tickets name
  airlines beside each uplift's litres; they are the raw records the call is built from and rank nothing on the
  decision question. Harmless.
- Cleared at stage 3: sweep 12 (QM-09 and the notice repeated generic column names: the data files now carry their
  systems' coded field names), sweep 13 (the batch number read as a graded figure in metadata: blocks 1 and 4 of the
  write-up say "the recalled batch"), sweep 8 (temperature columns renamed from `temp` to `degc`).
- The stage-4 reader (on target.zip c7c2288a): nothing quoted for question 1, no ranking file, no helper file, no
  answer-reading figure; question 5 names QM-09 3.2 and 4.1 and the prompt as fixing the population, the instant, the
  unit and the rounding, executing to the golden's population; question 6 an analytical choice, nothing planted.
- Ruling: the shift log's product change checks ("one hydrant line fill on the meter") are the Operator's own check at
  P-A01, true where they were taken, and never a declaration that the hydrant is clear.
- Ruling: the stands 27 and 28 closure entry is ordinary airport operations traffic in a farm shift log.
- Ruling: the reader's realism notes (drain and filter values in narrow bands, Northgarth's log in UTC against
  Corbel's local time) are plausible differences between two agents' systems and an operator's routine readings.
- After the reader: QM-09 2.3 gained one sentence (the commingling sentence of SF16), the only document that changed;
  `leak.py` re-run on the new cut. The second reader read 2.3 as the manual's own definition, saying nothing of the
  hydrant (its answers under "Second read" in `leak_check_report.md`).
- The judge's second pass (dde9588d, DETERMINISTIC, APPROVE, `determinism_check_report_pass2.md`), ruled one line each:
- Ruling: the rack line's carry-over (RK-01's 4,222 L) is the refuellers' softest point and is forced: the register
  files the line fill and the shift log the rack changes, it is the hydrant's own displacement physics, and SF18
  asserts both readings.
- Ruling: the golden CSV's into-plane agent column is not in the prompt's field list and is ungraded; it stays as the
  recall notice's own field, ordinary context that moves nothing.
- Ruling: the 10 L tolerance in the deliverable answers covers every refueller figure 1 to 2 L from a boundary, the
  plan's holdings and airline totals as well as the return's rows (RF-24 306, CB418424 124, CB418399 274, CB418369 276).

## Tried and rejected

- Precision of an attribute matcher carried from a small-block pilot to the full build, rebuilt from the
  per-comparison false-acceptance rate times the comparisons each block makes: the lesson is task192's
  (an instrument's error rates carry, its predictive values do not when the base rate moves) and task446
  v2's, in record-linkage nouns, so it is a repeated driver whatever the guard's lexical score (0.07).
- Resolving pairwise links into entities under a one-record-per-source constraint, chains cut at the
  weakest link: task486 architecture 2's driver, landed by its scored reader A.
- Correcting a noisy disagreement flag for its own error rates measured on known true and false links to
  estimate a barcode join's false-match share: task468's heart (linker misses and false links measured on
  control groups) and close to task456's latent class.
- Self-null coincidence rate (how often FDC's own distinct products agree on brand, serving and panel)
  applied to label-snap stubs: a paper simulation on seeds 488, 7 and 11 showed pair-level precision
  dominated by visible ties, so the tie rung lands the golden, and the per-link form needs the
  counterpart share, which no file pins.
- Clustered audit errors read with a design effect at the company prefix: task228's and task261's lesson
  (variance built at the unit the errors cluster within).
- The ET45 world's two live record-linkage candidates (value-specific agreement weights; a matcher's overconfidence carried to the auto-link band) were left unbuilt at the 2026-10-28 redraw into education at the user's request; the first had no determinate form inside the seed's world and the second's miscalibration shows to anyone who bins the review band.
- Ask layer, first form: the import's population left to the export's operational status with nothing filed on a
  revised item's keys, and enemy groups read from every version's row; the judge's pass 1 loaded both keys of the 98
  re-keyed revisions and called the one-per-item golden wrong, a fork sold as a device. Replaced by the section 1 pin
  and a version-history catalog whose 2025 accessibility versions carry the silent primary.
- Architecture 1, at the 2026-11-02 re-check: the golden is the field's own fixed-anchor calibration by marginal maximum likelihood with the launch items held at their 2021 values, applied as the textbook states it, with nothing in the data violating its precondition and a standing spread of 0. The field's method is therefore the top rung, not rung 0 or 1 (stumping 1.1b), and the honest anatomy fails Link, Reflex and Back-test. The easy routes do file wrong commissions on the clean truth (138, 116, 93), but the portal's models run this method by reflex. Spent, not re-rooted; the next step is the orchestrator's.
- 2026-11-04, architecture 2 draw, screens before the hydrant (each dead on paper, read against task476's S3.1 to
  S3.60, task274's and task486's lists and the cards):
  - Test equating, another world: anchors drifting together (the drift screen's masking) needs an outside link the
    records do not hold, and a drifted anchor dropped is cleaning (task479 v4's Gate G); testlet dependence is a model
    fork; anchors seen again by repeaters is the first-time-taker rule; mode and accommodation effects are DIF, the
    field's reflex; items calibrated in another position is task482 architecture 6; the item-family mean for new
    clones adds a term to a fitted specification (determinism-check, the identity).
  - Census and register quality: oldest-old and emigrant over-coverage by signs of life (task471 architecture 4,
    task173, task274); stock against flow sampling (task182); usual residence by duration (task485); households from a
    shared address (grain, banned in the window); an enterprise group from ownership chains (a filed SME rule);
    unrecorded cattle deaths against fallen-stock collections (task476 S3.41, an inner join); a care home capped at its
    licensed beds (S3.38).
  - Official time series: closed seasonal establishments imputed as open (S3.44, dead twice); degree-day adjustment
    (task486's screen, the textbook route); ISO week 53 in a weekly series (time semantics); the error of closure
    spread over an intercensal decade (an estimator family); first-release revision bias with a HAC test (the field's
    method, a variance step); journey factors for season tickets (S3.48, and the yield conversion task476 v3 spent).
  - Payment claims: the facility fee beside a hospital clinic's professional claim (the health economist's reflex);
    therapy units under the 8-minute rule, anaesthesia concurrency, a benefit period across facilities (filed rules);
    GLP-1 fills by the member's diagnoses (the population, the WHAT screen).
  - House worlds: a weighbridge's stored tare drifting with fuel (a model of the measurement); wood chips by moisture,
    fuel by temperature, cylinders by pressure (task476 v3's conversion at a state); a raw milk silo's dilution of a
    contaminated tanker (the field's mass balance is the golden); FIFO and FEFO lots in drive-in racking (task56 v12's
    batch running balance, and a record against an operation alone); a whisky warehouse's evaporation by cask size (a
    rate by condition); a network's device outages implying its topology (task461 v3's hierarchy from series); a
    pipeline's batch tracked by volume (the field's own method, the golden); a weight-or-cube freight driver (an
    allocation basis fork).
- 2026-11-04, the hydrant's first prototype (proto.py, session scratchpad, three seeds) put each pit on a 160-litre
  riser: every pit used during the batch then held batch fuel in its riser, so its next uplift after the trailing front
  took a sub-one-per-cent dose and the notified set grew by twenty for a reason no reader would weigh; the register's
  pits sit on the branch pipe (proto2.py, six seeds), where the routes' notified sets differ by 6 to 24 and the time
  window, one line fill and the path volume against the pump station's meter all file the hydrant clear while the
  per-segment front leaves batch fuel in the low-use branches on five seeds of six.
- 2026-11-04, stage 3 of architecture 2, dead ends while cutting the pack (each replaced before the hand-off):
  - Pier stands working to one shared slot table: every stand's turns fell in the same minutes, the pump station ran
    in bursts (420 m3 in one hour, nothing in another), one line fill passed in 77 minutes and the Operator's product
    change check at P-A05 read Tank 2's fuel after the reckoning said Tank 3's; each stand now runs on its own offset
    and the check is taken at P-A01, the first pit off the main.
  - A 6,500 L transfer from RF-23 into RF-24: without it booked RF-24 ran 5,400 L below empty within the afternoon,
    an inconsistency any careful rebuild sees, because each top-up fills to a fraction of capacity and carries the
    deficit forward; the transfer is 3,843 L and RF-24 now never runs below the transferred litres.
  - Daily refueller dips at each handover, and a quarantine dip after the suspension: each is a control that ties
    only under the right keying of trailers and the transfer (an oracle for both primaries); only the weekly Monday
    dip ships, and the tanks are rebuilt through Monday's loads and tickets.
  - Operator against billed customer (a wet-leased fleet billed to another airline's account) as a third primary:
    the lessor flies widebodies on the hydrant, so the device would sit in the main population; dropped.
  - Names one or two letters from real ones (an airline a letter off a Baltic carrier, a cargo line and a terminal
    named for real places, an airline sharing a Californian town's name): renamed before the near-name review.
  - Generic column names (agent, batch, equipment, litres, operator, registration, tank): QM-09 and the recall notice
    used them as ordinary words and `leak.py` read both documents as describing the data; the systems' coded field
    names replaced them.
- 2026-11-04, stage 4 residuals on architecture 2 (after the reader and the judge, both clean):
  - Converging the 73 across atomic draw orderings by moving the marginal uplifts: the SCADA minute flows already fix
    the steady-rate reading (checks.py asserts the fit and the count's shift), and moving uplifts would move graded
    figures and the samples; not pursued, on the coordinator's word.
  - Grading the partial hydrant rows' batch litres at 10 L: on the records' own readings (the litres basis, the
    flushes, the line-up minute) the two tail rows move by up to 2,423 L, two Pier A rows by about 630 L and the rest
    by up to 144 L, so each partial row now carries its own band in the deliverable answers.
  - The refueller tank closed only by the compartment count: one compartment rules out a per-compartment reading and
    not a first-in first-out tank, which drops RF-24 and T-35 from the drain list; QM-09 2.3 now files the
    commingling sentence.
