# task308: which 2027 capacity offer the cooperative should contract, and what it is worth

Architecture 3, drawn 2026-10-27 (wave 7, Opportunity Sizing & Decision Support, perssathya). Re-root after
architecture 2 (a catastrophe layer for one of four regional home books) was spent at stage 4. Moved to another client
domain and dataset under the rule that a stuck build is redrawn rather than parked (`CLAUDE.md`). Nothing of the
insurance world is carried.

## Draw

- **Pairing:** energy-systems-utilities x Opportunity Sizing & Decision Support, task type
  generation-capacity-planning (OS). Decision: pick one of four offers. Sized quantity: each offer's 2027 expected
  unserved energy removed (pool: the offered megawatts; realisable: the shortfall they would have covered in the
  recorded weather years), valued at the planning standard's value of lost load less the offer's annual capacity
  payment.
- **World:** Prairie Hollow Power Cooperative, a generation and transmission cooperative in a fictional US Upper Midwest
  territory serving eight member distribution cooperatives, winter peaking since its members' heat pump programmes. Its
  2027 fleet: a nuclear share, a hydro plant, one coal unit (its sister unit retires at the end of 2026), two combined
  cycles on firm pipeline transport, ten simple-cycle combustion turbines on Northgate Interstate Gas Transmission's
  interruptible service, six reciprocating engines, 800 MW of wind and 400 MW of solar under contract, 200 MW of firm
  imports from Red Willow Hydro Authority over the 345 kV tie. The resource planning committee awards one 2027 capacity
  contract from the request for offers: the Ketchum Ridge peaker (300 MW, interruptible transport on Northgate), a 300 MW
  firm import from Red Willow over the existing tie, Sandhill Draw Wind (450 MW), Coulee Flats Solar (500 MW).
- **Forum and forcing event:** the resource planning committee (committee_or_panel); the offers are firm to the award
  meeting and the contract is signed for delivery from 1 January 2027 (purchase_order_or_contract). Organisation:
  cooperative_or_member_body. Role: the resource planning engineer (capacity_planner).
- **Data-native sentence:** the outage event log records each unit's forced outages with a cause code, and the ten
  peakers on Northgate's interruptible service carry lack-of-fuel outages that begin and end together in the coldest
  hours, the same hours that carry nearly all of the 2027 fleet's replayed shortfall; a new peaker on that service has no
  record of its own, so what it would have done in those hours is read from its class's record in those hours, not from
  its rating.
- **Four candidates, each with a default path and a screen** (the author file's rule):
  1. *Correlated fuel outages (chosen).* Default: replay the fleet, credit the new peaker its rated or class-average
     forced outage rate in every hour, award the peaker. Screen: the decisive step is a dependence between a unit with
     no record and its class, read only by setting the class's outages against the shortfall hours; no filed sentence
     names fuel, curtailment, cold or the class's hours.
  2. *Risk hours moved by the solar already contracted.* Default: credit solar its output in last decade's top gross
     load hours. Screen: on a winter-peaking system every competent replay already removes it; a lower rung, not the stump.
  3. *Energy-limited demand response against long cold spells.* Default: credit a capped number of four-hour calls at
     nameplate. Screen: the call schedule is a dispatch rule (a method fork on the main call); dropped.
  4. *Imports curtailed when the neighbour is short.* Default: firm import at full availability. Screen: the neighbour's
     shortage would have to be planted in a document; a hydro exporter with its own record carries no such hidden
     condition. Dropped; the import is the honest winner instead.
- **Guard (filed card, 2026-10-27):** WARN only. The gap, generator and Gate G axes were redrawn from the first draft
  (gap population with G14 repeated nine older builds' signature; objective with G14 and method_or_model_selection
  carries one differentiation line against this slot's architecture 2). `repeat.question_form` (which, against task271)
  is answered by the decision: a pick of one offer asks which. Deliverables moved to xlsx and docx after the pdf and xlsx
  set repeated task271.

## Default path

The route a capable analyst takes with every file read and every filed rule executed:

1. Puts the planning load table on UTC (hour ending in local prevailing time, the starred autumn hour the standard-time
   01:00), reads 2019's load column in MW, and replays the 2027 fleet through the forced events and derates of the
   outage event log at their latest revision, part hours for their part, with the 200 MW import whenever the tie is in
   service: 9,500 MWh a year of expected unserved energy.
2. Adds the Red Willow import (tie in service), Sandhill Draw and Coulee Flats (modelled profiles) hour by hour:
   7,100, 2,000 and 400 MWh removed.
3. Counts the Ketchum Ridge peaker, which has no record of its own, at its expected available capacity: 300 MW less its
   4.5 per cent EFORd (or less the Northgate IT peakers' 5.2 per cent forced outage rate over the ten years) in every
   hour, and finds it removes 6,900 MWh.
4. Values each reduction at USD 20,000 per MWh less the 2027 payment and awards the highest.

Ends on: Ketchum Ridge, net USD 115 million (the import second at USD 106 million).
Golden: Red Willow import, net USD 106 million (Ketchum Ridge removes 0 MWh, net USD -23 million).

## Stump sentence

A capable analyst replays the 2027 fleet through the ten weather years, credits the new Ketchum Ridge peaker with its
rated (or its class's average) availability in every hour, and awards Ketchum Ridge at a net USD 115 million, because
the peaker is the cheapest capacity per available megawatt; but the ten existing peakers on Northgate's interruptible
transportation were out together, on lack of fuel, in every hour that carried a shortfall, so a peaker taking gas on
the same service would have been out in exactly those hours, removes no unserved energy and loses its whole payment,
and the 300 MW firm import over the Red Willow tie (net USD 106 million) is the award.

Data-native sentence: the event log's lack-of-fuel outages (cause 9130) take all ten Northgate IT peakers out together
in the coldest hours, which are the only hours with replayed shortfall; a new unit on that service has no record, so its
availability in those hours can be read only from its class's record in those hours.

## Three rules

Task type: energy-systems-utilities / generation-capacity-planning (OS): a capacity procurement sized by the
reliability each offer buys.
Domain test: the deciding quantity is each offer's reduction in expected unserved energy, which resource adequacy
planning estimates by running the planning-year fleet through recorded weather years; whether a resource's availability
moves with the conditions that cause shortfalls (correlated, common-mode forced outages, the reason accreditation moved
to effective load carrying capability after the winter storms) decides its capacity value.
Swap: "award the hospital's new theatre to the supplier whose staff would be absent in the weeks the waiting list
peaks" keeps the words and loses the replay of a fleet through weather years, the forced outage record and the value
of lost load: no field outside power system planning prices an addition on the shortfall it removes hour by hour.
Layer 1: the planning table by hour ending in local prevailing time with its starred autumn hour against an event log
in UTC, profiles by hour beginning in UTC and a tie log in CST and CDT; 2019's load delivered in kW by the old
forecasting tool; event records revised after first report; derates beside full outages, overlapping on one unit;
planned and maintenance work in the same log; a retiring unit still in the log; four prices in four units. Every item is
what a GADS-style outage system, a forecasting tool and an RFO produce; none moves the call (SF1 to SF11 asserted).
Layer 2: estimand identification: what a unit with no record of its own would have contributed in the hours that carry
the shortfall, given that its class's outages share one cause with those hours.
Decisive step: treating the new peaker's availability as dependent on its class's: in each replayed hour it is available
only as far as the Northgate IT peakers were, because it would take gas on the same interruptible service; its rated or
average availability is independent of the hours that matter.
Not semantics: every field, code and unit can be read right (cause 9130 included) and the peaker still be credited at
4.5 per cent EFORd in every hour, filing Ketchum Ridge; the step is a dependence between a new unit and its class, which
no field states.
Not rule application: RA-3 section 7 files only that an addition counts at its expected available capacity in each hour
from the evidence the record holds; the enumerated family of availability models for the new peaker (rated EFORd, the
class's ten-year rate with or without lack of fuel, nameplate, the class's hourly share, out in lack-of-fuel hours and
rated otherwise, two units at the class share) spans 0 to 7,100 MWh removed (71 printed units of 100 MWh) and files two
different awards; the standing family that reads the class's record in the hour (four constructions) spans 0 MWh,
every one filing the import; the ruling out is quiet, done by the event log's co-timed outages rather than any clause.
Analyst test: a strong analyst who resolves the clocks, units, revisions and derates and reads RA-3 literally credits
the peaker with its 4.5 per cent rated EFORd (or its class's average) in every hour and awards Ketchum Ridge at a net
USD 115 million; the golden reads the peaker's availability from its class's record in each hour and awards the Red
Willow import at USD 106 million.
Estimand: RA-3 Rev. 4 (sections 2 to 7) files the population (the 2027 fleet, Sandoval 1 out, each offer alone), the
outcome (unserved energy: load less wind, solar, available units and imports, where positive), the window (the ten
weather years 2016 to 2025, equally weighted, averaged to a year), the unit (MWh a year, valued at USD 20,000) and the
comparison (EUE without the offer less EUE with it); the RFO files the 2027 payment and the award rule.
No decoy: nothing is planted: the manufacturer's 4.5 per cent EFORd is a true annual figure for a new peaker and close
to the class's own record; no memo, draft or stakeholder figure points at the peaker.
No certified replay: no certified or published figure is reproduced to recover a hidden method; the standard states
the estimand and the record carries the evidence.
Lesson: a unit's capacity value lives in the hours of shortfall, and where the units of its kind fail together for one
shared reason in exactly those hours, a new unit of that kind adds nothing however good its average; no build on file
values an addition by its dependence on its class's outages.

## Readability screen

| Rung | Test 1 (a filed sentence names it) | Test 2 (a file or column names it) | Test 3 (the field's reflex reaches it) | Verdict |
|---|---|---|---|---|
| R1 the clocks and units of the planning table | the table's own headers | yes | yes | readable |
| R2 the replay of forced events at their latest revision | RA-3 section 4 | yes | yes | readable |
| R3 hour-by-hour profiles for wind and solar | RA-3 section 7, the RFO | yes | yes | readable |
| R4 the peaker's availability read from its class in each hour (decisive) | no: section 7 says only expected available capacity from the record | no: no column, file or document names fuel, curtailment, cold or a dependence | no: the field's reflex for a new unit is its EFORd | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the 2027 fleet | Sandoval 1 out | Sandoval 1 replayed | same call | the RFO (retires 31 December 2026); asserted |
| SF2 | forced outages | forced events and derates only | planned and maintenance replayed too | same call | RA-3 section 4; asserted |
| SF3 | the record of an event | latest revision | first report | same call | RA-3 section 4; asserted |
| SF4 | part hours | counted for the part | whole hour counted out | same call | RA-3 section 4; asserted |
| SF5 | overlapping events | least capability governs | losses added | same call | RA-3 section 4; asserted |
| SF6 | profile clock | hours beginning UTC | read as local | same call | the RFO; asserted |
| SF7 | hour ending | hour ending, the starred hour standard time | read as hour beginning | same call | RA-3 section 3, the table; asserted |
| SF8 | tie outages | forced and planned | forced only | same call | RA-3 section 5; asserted |
| SF9 | the new import's availability | contract quantity while the tie is in service | every hour | same call | RA-3 section 5, the RFO; asserted |
| SF10 | 2019's load | kW read as MW | left in kW | ruled out: a load a thousand times the fleet | the data; asserted |
| SF11 | payment | quotes converted to 2027 dollars | a 366-day year | same call | the calendar; asserted |
| SF12 | expected available capacity | expected megawatts in the hour | a two-state draw for each 150 MW unit | same call | RA-3 section 7; asserted |
| SF13 | each offer | alone against the fleet | offers combined | same call | RA-3 section 7 |
| SF14 | the award | the highest value if positive | none | same call | the RFO; asserted |
| SF15 | weather years | equal weight | recent years weighted | same call | RA-3 section 2; asserted |
| SF16 | imports in the fleet | the 200 MW contract counted | omitted | same call | the RFO, the fleet list; asserted |
| SF17 | wind and solar | the contracted output in the table | none | same call | RA-3 section 3 |
| SF18 | what is compared | capacity payment only | energy costs added | same call | the RFO evaluation basis |

## Ladder

- R0 nameplate (300 MW every hour): Ketchum Ridge, USD 118 million.
- R1 UCAP at the 100 highest net-load hours (rated EFORd for the peaker, the profiles for wind and solar): Ketchum Ridge.
- R2 an independent-outage convolution of the fleet at each unit's ten-year forced outage rate: not the import (asserted).
- R3 the replay with the peaker at its rated 4.5 per cent EFORd: Ketchum Ridge, USD 115 million (the default path).
- R4 the replay with the peaker at the Northgate IT class's ten-year rate (5.2 per cent, or 4.4 without lack of fuel):
  Ketchum Ridge, USD 114 or 115 million.
- Golden: the replay with the peaker at the class's available share in each hour: Red Willow import, USD 106 million,
  Ketchum Ridge 0 MWh. Every rung's margin over the import is at least USD 8 million (asserted over USD 5 million).
- Cheap routes on the clean truth that land the call: one, the class's availability read in the peak hours, which is the
  decisive insight itself.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 2027 fleet (fleet list less Sandoval 1), the 200 MW import, the contracted wind and solar; each offer alone | filed (RA-3 sections 4, 5, 7; the RFO); SF1, SF13, SF16 asserted |
| 2 | Unit of account | MWh of unserved energy a year; USD million of net value | filed (RA-3 sections 6, 8; the RFO) |
| 3 | Attribution window | the ten weather years 2016 to 2025 | filed (RA-3 section 2) |
| 4 | As-of dating | the planning year 2027; the record to the end of 2025 | filed |
| 5 | Version basis | each event's latest revision | filed (RA-3 section 4); SF3 asserted |
| 6 | Denominator | the ten years, equally weighted | filed (RA-3 section 2); SF15 asserted |
| 7 | Weighting | each hour once | filed (RA-3 section 6) |
| 8 | Window length | the ten years | filed |
| 9 | Boundary inclusivity | part hours for their part | filed (RA-3 section 4); SF4 asserted |
| 10 | Rounding path | figures from unrounded hours, rounded once at the stated unit | filed (the prompt) |
| 11 | Tie-break | none: the award leads by USD 94 million | asserted |
| 12 | Maturity and censoring | none in the call; the meters' late records in the asks | filed (MS-12 section 2) |
| 13 | Order of operations | replay, then each offer, then value | filed (RA-3 sections 6, 7; the RFO) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | revisions: the latest; meter versions: the highest | filed (RA-3 section 4, MS-12 section 2) |
| 16 | Identity normalisation | GADS unit codes in the log and the fleet list | the shared key |
| 17 | Netting against gross | unserved energy only where positive; member energy delivered less received | filed (RA-3 section 6, MS-12 section 3) |
| 18 | Dimensional units | MW, kW in 2019, four price units | the data and the quotes; SF10, SF11 asserted |
| 19 | Code and status semantics | event types U1, U2, U3, SF, D1 to D3 forced; PO, MO planned | filed (RA-3 section 4); never the stump |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | section 7 for every offer | filed |
| 22 | Forward window contents | 2027 is the weather years replayed with the 2027 fleet and load | filed (RA-3 sections 2 to 4) |

## Literal reader

Executed word for word, RA-3 replays the 2027 fleet through each weather year with the forced outages it had and counts
each offer "at its expected available capacity in that hour, judged from the evidence the record holds". For the import,
wind and solar the record holds their hour directly. For the peaker the only evidence about a peaker on Northgate IT in
a given hour is what the ten such peakers did in that hour; in every shortfall hour all ten were out, so the literal
execution gives 0 MWh. A reading that credits the rated EFORd in every hour does not use the evidence of that hour, and
a reading by temperature band or day uses other hours; neither is the sentence. The call is the import under every
member of the standing family (asserted).

## Oracles

The generator's clean truth (world.py, records.py) reproduces the pack's replay to 1e-6 MW per unit-hour; verify.py
recomputes every graded figure on its own code path (minute grids, hand-rolled clocks, a pivot) with 0 failures; the
standing family and every rung are asserted in checks.py (202 checks).

## Ask sheet

**Ask A: each member's 2025 net energy delivered (8 figures, whole MWh).** Use: the contract's cost allocation (MS-12).
Primary device, silent: the current transformers at one or more delivery points of every member were replaced in 2025
and the MDM went on applying the old multiplier for 30 to 100 days, so those intervals carry half their energy; only the
meter service orders (ratio and multiplier at the replacement) show it. Interior: four replacements the MDM picked up on
the day (a blanket correction over-repairs them). Hazards (filed, executed by the cracker): highest version, delivered
less received, the Lone Elm point moving to Marais on 1 July. Paths: the natural read 0 of 8; year-end members 0 of 8;
delivered only 0 of 8.

**Ask B: each member's 2025 12-CP average (8 figures, MW to one decimal).** Use: the allocation key itself. Primary
device, silent: one meter in every member stayed on standard time after the spring change until a technician reset it
(June to October), so its intervals sit an hour early and its load at each monthly peak is the wrong hour's; the
service orders record the reset. Second device: ask A's multipliers. Paths: the natural read 0 of 8; delivered only 0 of
8; after one of the two devices, 0 and 1 of 8.

| Ask | Cracker (lands the call, executes every filed rule, runs the battery) | Verdict |
|---|---|---|
| A net energy | 0 of 8 on every path that does not meet the multiplier lag | miss |
| B 12-CP average | 0 of 8 on every path that meets neither device; 1 of 8 at most after one | miss |

Pair ceiling: 39.3 ((45.0 + 33.6) / 2), the cracker keeping 0 of the 16 ask figures and the mirror (the rated peaker)
7 of the 10 call figures.
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

## Pre-ship check

- 2026-10-27, stage 4 on the cut pack. Leak reader (isolated, sonnet, medium): no decisive-step sentence, no ranking
  or helper file, no answer-like figure; question 5 lists RA-3 sections 4 to 7 and MS-12 sections 1 to 4, whose
  literal execution is the golden's construction with the evidence-to-capacity method left open by section 7;
  question 6 analytical. Every REVIEW line harmless (the offers' MW and prices are inputs; the offer and member lists
  rank nothing; the fleet list's later dates are a retirement and contract ends).
- Judge pass 1 (/tmp/determinism-check-task308-r1): DETERMINISTIC, APPROVE; Gate G method_or_model_selection,
  analytical_non_defect, no surface read; Gate H domain pass, layers pass, decisive step analytical. Every graded
  figure reproduced. Two optional notes: Sandhill Draw's payment sat on an exact half-up tie (450 MW at USD 5.25 per
  kW-month, 28.35), moved off it by pricing the offer at 5.30 (28.6; net still USD 12 million, the award unchanged);
  Ketchum Ridge's 0 MWh rests on section 7's "in that hour", and a temperature-conditional estimator files about
  770 MWh and a net near USD -8 million with the award unchanged, left as filed because a clause naming the
  estimator would file the how.
- After the price move: rebuild with checks, verifier and byte-identical builds, figures_check 61 of 61, precut 53
  checks 0 FAIL, leak.py REVIEW (the same lines), guard heart WARN (question form which against task271). The price
  change touched one figure in the offers paper, so the reader was not re-run.
- The 10/10 rules re-read against the built pack: the decisive step is judging a new peaker's availability in the
  hours that carry a shortfall from its sister units' record, an analytical choice; the mess (mixed time stamps,
  revised MDM intervals, a delivery point moved between members) stays Layer 1.

## Tried and rejected

- 2026-10-25, before the pack: the seed's own step (cannibalisation measured on flat streets carried to a hilly
  district) is a visible-state stratification on elevation, which the probes on this lane land by reflex; a
  station-level pilot comparison missing members who switched stations is a contaminated comparison, found by both
  probes on task304; battery swaps capping a hilly district's rides are handed over by battery columns. Set aside on paper.
- 2026-10-25, stage 2: twenty small University stations; per-station cells by day of week within month overshot the
  turned-away requests by 13 per cent (a station's stocked seconds and empty seconds move together when a few bikes
  drain), so the family forked; five large hubs (two residence halls, three class hubs) cut it to 3 per cent.
- 2026-10-25, stage 2: the graded figure to the nearest USD 10,000; the standing family on University spans about USD
  8,000 (induced riders on the rides served, day-of-week cells, the simulated e-bike world), so no seed holds it in one
  10,000 bin; 25,000 holds every network with USD 5,000 to spare.
- 2026-10-25, stage 2: per-station 2024 trips as a distractor; it licenses a difference-in-differences reading of the
  pilot that moves the uplift by a point and University's figure by USD 6,000. Dropped for the vendor's quotation.
- 2026-10-25, stage 2: the operations director's line that the e-bikes should go where the riders are, in the board
  paper; a stakeholder view pointing at the wrong answer reads as a planted decoy. Cut.
- 2026-10-25, stage 2: billing ZIP codes with a lookup for ask A; any real ZIP ties the invented city to a real one. The
  register carries the rider's home area from sign-up instead.
- 2026-10-26, stage 2: road-test retests reopened within 90 minutes only; a one-day window repair then lands the golden.
  Retests now reopen up to 39 hours later and intermittent faults come back within a ride or two, so no window separates
  them from genuine repeats.
- 2026-10-26, stage 3: the e-bike crew's moves on a 15-second grid, every charging session taking the lowest free point and
  192 sessions plugged in at local midnight on 1 January read as generated; the crew's pace, the point a rider picks and
  the New Year's Eve plug-ins now come from their own stream, and no call figure moved.
- 2026-10-26, stage 3: the 03:00 audit showed each station at its par on 92 per cent of mornings, a constant stream; the
  night crew now leaves a station a bike or two off par when the van runs short, and the call's figures moved by under
  USD 200 (University USD 127,946 to 127,804).
- 2026-10-26, stage 3: the first controller replacement in April; with the points re-drawn, a register-must-rise filter
  landed two of the three months before it. Moved to January, the filter misses every month.
- 2026-10-26, stage 4: architecture 1 spent. Both isolated scored readers (sonnet and opus at medium, prompt and pack
  only) rebuilt each station's classic stock from the 03:00 audit, the trips and the van moves, imputed the requests the
  empty seconds turned away and named University (USD 100,000 on station x day x hour-by-weekend cells; USD 125,000, the
  golden, on station x hour x day type x term cells): demand censored at empty stations is the field's textbook estimate,
  and a pack holding the audit and the dispatch log makes it executable. Both landed ask B (the re-sent sessions by their
  repeated registers) and neither ask A (one person a card) nor ask C (every job card). The judge thread returned
  NOT_DETERMINISTIC, SEND_BACK on Gate C (the estimation grain and the e-bikes' new riders unfiled in the measure; the
  person and job definitions in asks A and C), Gate G analytical_non_defect and Gate H pass. Realism tells the readers
  named: the inventory closing to zero on every station-day, one par per network at the 03:00 audit, Harbour's flat
  per-station rides, trip durations and the e-bike share flat across networks, hours and distances, the pilot note issued
  in January in the past tense, the pilot stations' capacities against the 5 per cent match. Re-root at stage 1.
- 2026-10-26, re-root screen (scratch t308v2): the pilot's comparison stations ran dry too, so the ride-based uplift
  double counts the relief; call-only probe B (opus) found the comparison stations' empty hours and measured the uplift
  on demand (University at USD 125,000). Any stump that runs through censoring or stock in this world is spent.
- 2026-10-26, re-root concept readers (opus, medium, scenario text only): household interference in an
  account-randomised retention trial, appraisal-smoothed private-fund returns, first-round against repeat screening
  yield. Each reader took the named textbook move at once (household-level contrasts, Geltner desmoothing, first kits
  split from repeats). Dropped before a pack.
- 2026-10-26, re-root, the journey unit (scratch t308v3): members re-dock at 45 minutes and day-pass holders at 30 to
  restart their included minutes, and the pilot's riders choose an e-bike once per journey, so take-up read per ride
  undervalues Central's day-pass tours. Both concept readers and both call-only probes on the first pack missed it
  (Riverside at USD 125,000 against the golden Central at USD 200,000). On the second pack (tourists riding two or
  three journeys a pass-day), probe D (opus) read the pile-up of classic rides just under the included minutes and
  the cliff after them as riders re-docking, chained same-station restarts within five minutes and filed the golden
  exactly (Central USD 225,000), and probe C (sonnet) reached Central through the day-pass e-bike rides' uncapped
  lengths. The allowance's cliff in the ride-length distribution announces the re-dock. Dead.
- 2026-10-26, re-root screen (plan-only Opus readers, text only, no figures): county procurement savings that budget-bound
  departments re-spend, a growth grant's induced jobs where the workforce commutes in, a Medicaid plan's savings past its
  members' churn, bus journeys from housing sites that build out slower than the developers' survey says, and contingent
  business interruption carried by suppliers' locations. Each reader named the step itself as the decisive one, unprompted.
  An economic mechanism that the filed estimand's own wording invites ("the fall in expenditure", "regional jobs", "the
  plan's spending") is a reflex, whatever the world.
- 2026-10-26, re-root probe pack (job-search app, a cancellation-flow save offer tested in two markets, carried to five):
  subscribers who cancel because an employer on the platform has just hired them cannot be saved by a price, and one
  market's employer side hires half its cancellers. The plan-only reader missed it; on the pack the Sonnet probe filed
  Mexico (USD 510,000) and the Opus probe linked the employer placement invoices to the cancellers and filed Colombia
  (USD 420,000, the golden). A hire record in its own file is read as churn by the first reader who opens it. Dead.
- 2026-10-26, plan-only screen of six general mechanisms (Opus readers, text only): a list-price rise judged on promotion-week elasticities (stockpiling), an adherence programme sized on the adherent against non-adherent admission gap (healthy adherer), a heat programme sized on same-day excess deaths (harvesting), threshold clinics sized on the last reading (regression to the mean), fare-free days sized on the trial days' lift (trips moved between days), and a ward sized on average occupancy (queueing at the peaks). Every reader named its mechanism unprompted, five of them as a numbered step. A general statistical mechanism is a reflex whatever world it is dressed in; only a world-specific structure is worth a pack.
- 2026-10-26, plan-only screen of four world-specific candidates (Opus readers, text only): a road reconstruction sized on patching avoided (the reader weighted traffic by standard axles unprompted), a station car park sized on new rail journeys (the reader named railheading and the full car park's hidden demand), and a cancellation-screen save offer carried to five markets (the reader named app-store billing as the first thing that could move the winner). All three dead on paper. The fourth, a bus priority corridor whose late running carries into the vehicles' next journeys, passed: the reader worked the corridor's own journeys only.
- 2026-10-26, probe pack (bus priority on one of four corridors, sized by the passenger lateness removed in 2027; Mill Lane's buses go straight on to the busy cross-town 22 and 30 on a short layover, so the lateness the scheme removes there stops passing into those journeys; the corridor-journeys replay files Harbour Road at 62,000 against the golden Mill Lane at 96,000): the plan-only reader missed it, but on the pack the Opus probe rebuilt the 2025 operation from the AVL, found that holding at timing points and a two-minute stand on each running board reproduced every recorded arrival to the second, replayed every board-day with the scheme and filed Mill Lane at 96,000 in eight tool calls; the Sonnet probe read the same two-minute stand off the running boards and filed Mill Lane at 96,000 too. A record that a replay of its own rules reproduces exactly invites the replay, and a replay of the whole operation carries every knock-on with it. Dead.
- 2026-10-26, plan-only screen of eight more (Opus readers, text only): an express lane whose toll would pass the statutory cap (the reader solved the toll under the cap and the speed standard), a security programme on a layered defence (marginal effect after the controls in place), a card limit increase whose defaulters draw the new limit (the pilot's own charge-off gap carried by score and utilisation band), a lender's product line whose losses sit with brokers since removed from the panel, an unlit artificial pitch (floodlight conditions applied slot by slot), courier-delayed potassium samples, a price rise that rivals follow, and a GP surgery sited by floating catchments. Each mechanism was a numbered step in the reader's plan. Dead on paper.
- 2026-10-26, plan-only screen of two more (Opus readers, text only): a motor rate cut sized by underwriting profit with one segment's case reserves strengthened by a claims-handling change (step 1 of the reader's plan checked case-reserve adequacy against the reserve history and fell back to paid), and a recycling service sized by tonnes diverted with contaminated loads rejected at the sorting plant (step 2 netted each area's reject rate). Both mechanisms were numbered steps. Dead on paper.
- 2026-10-26, plan-only screen of four more (Opus readers, text only): an extra ambulance crew sized by category 2 calls reached in time (step 4 split each late call into an availability miss and a geography miss, step 5 replayed the dispatch with the extra vehicle), e-bikes sized by ride revenue with flat batteries waiting for the swap van (step 6 capped usable e-bike-days by the 2027 swap rota), a home renewal increase sized by the underwriting result with multi-line households cancelling their car policy (step 6 priced the car-line spillover), and four nurse posts sized by agency spending avoided with the bank nurses the posts free covering agency shifts on other wards (missed: the reader netted bank-filled gaps as no saving, but the freed pool is a workforce mechanism any staffing field shares, so the swap test fails). Dead.
- 2026-10-26, plan-only screen of four more (Opus readers, text only): a survey boost sized by the cut in the regional standard error (step 4 rebuilt the design effect of the added sample by PSU take and interviewer workload), a regional catastrophe cover sized by expected recoveries less premium (step 4 rebuilt events from uncoded claims under the hours clause), a bus priority scheme sized by passenger time riding and waiting (step 5 priced waiting from each stop's headway spread, E[H squared] over 2E[H]), and a seven-day discharge team sized by bed-days released (steps 2 and 3 kept only the delay the team can remove and counted midnights, weekends first). All named. Dead on paper. The bus reader used the smartcard taps only to sense-check the counters and never followed a passenger from one bus to the next.
- 2026-10-26, the bus corridors with an hourly country connection at Grove Road (passengers set down late by the corridor bus wait for the next hour's country bus): two plan-only readers passed it on paper (one priced the country buses' waits against the timetable and used the smartcard taps only to reconcile loads; the other chained taps only to find alighting stops), but the estimand cannot carry it. Counting the connection wait needs either a sentence naming the change of bus (which hands the step over) or an arrival convention for passengers who walk to a stop, whose scope is then the decisive step (a definition reading under rule 3). Dropped before any data was cut.
- 2026-10-26, stage 2: the first ask layer (the unit's figures over the platform's, cases that left the report open;
  the scheme rebuilt by effective dates). On pack t5 the opus probe kept 16 of 16, finding the open cases and the
  effective dates, and the sonnet probe 4 of 16 by the effective dates: every device sat on a path a careful reader
  takes. Re-sited onto the unit's re-dated losses and reopened cases and the scheme's reinstatements and rewrites; on
  t7 both fresh probes kept 0 of 16.
- 2026-10-26, stage 2: taking the usual day's claims off each period moves Severn Vale to the bin edge (-0.150 against
  -0.084); the event definitions now say every claim of the peril dated in the period belongs to the occurrence.
- 2026-10-26, stage 2: the unit's re-dating capped at 120 days for a leak and 210 for subsidence reached 9 or 10 of 12
  cells on every stream, Fenland having no leak or subsidence case near a year start; widened to 200 and 300 days it
  reaches 11 (Fenland 2025 stays out of reach).
- 2026-10-26, stage 4 round 1: event claims notified late without the code at 8 per cent across every peril let the
  codes-only route at the index alone name Pennine (-0.771 against Severn Vale -0.992): the dropped claims pull Severn
  Vale's floods under the retention while Pennine's large freezes stay over it, a cheap route onto the golden region.
  Freeze claims now come in late more often (16 per cent, frozen pipes found after the thaw) and storm and flood claims
  less (3 per cent); the codes-only route names Fenland with Pennine third (asserted).
- 2026-10-26, stage 4 round 1: ask B's devices B0 to B3 fell whole to reader J (opus), who read a cancellation followed by
  later In force rows as a reinstatement. Re-sited with B4 and B5 (notice given ahead of the day cover ends, so a term
  is listed for the month its cancellation takes effect); the golden figures did not move, the heuristic now misses by
  GBP 0.89 million or more in every region.
- 2026-10-26, stage 4 round 2: four catastrophes that reach the layer (Severn Vale's floods of April 2012, June and
  November 2019; Coastal North's windstorm of January 2015) carried no event code, so the coded storms read as the
  occurrences named Pennine at its default -0.428 (reader K, sonnet). Coded on their own stream as declared late; every
  graded figure unchanged; the coded-storms route now names Severn Vale (asserted in checks.py).
- 2026-10-26, stage 4 re-judge (pass 3): NOT_DETERMINISTIC, SEND_BACK on ask B, the main call forced (Pennine +0.087
  on every route the judge built, Gate H analytical). Ask B's population was open: 17 terms given notice in September for
  a day in October or November were listed for October and never again, their Cancelled rows before the window, and
  nothing filed said what a listing means (GBP 0.5 to 1.8 million a region). Read as an ask-layer and fork repair, not a
  re-root, because both findings sit outside the decisive step and the judge found the call forced. A notice for a day
  inside the bordereaux is now keyed inside them (no term leaves the bordereaux without its end or a Cancelled row,
  asserted), the claims operations report files what a bordereau lists (SF21) and step 7 states the golden's rule.
  Filing the rule made B2 and B4 readable, and a December-listing snapshot then filed the golden in every region (gaps
  0.00 to 0.07), so the old B5 (the terms listed once) went and ask B's primary became the listing's sum insured moving
  when an endorsement is keyed, carried by the society's further advances. The judge's Fenland fork (the 2025 panel
  counted on weather claims only, 131 firms against 137, Fenland -0.727 against -0.775) was closed in the data (SF20),
  and the claims parquet lost its pandas schema block.
- 2026-10-26, stage 4 pass 4 (8851863d): NOT_DETERMINISTIC, SEND_BACK on the main-call estimand. RC-07's "at what
  repairing them would cost in the cover year", beside the plan's 2027 index, executed literally to the recorded cost
  carried by the index alone (Severn Vale -0.1), and nothing filed said the 2027 cost of repairing a catastrophe's
  claims is anything else; both round-3 readers took that reading for question 5. Ask A's step 6 did not reproduce the
  twelve figures (the judge's reconstruction differed by 0.05 to 1.5 pounds a policy). Repaired rather than re-rooted,
  because the judge found the effect in the data and the decisive step analytical (Gate H), and its own fix is a
  filing of what is valued, not of how: RC-07 s.3 now says the plan's index follows the price of rebuilding a standard
  home in ordinary times and does not carry what else made a catastrophe's repairs cost what they did, naming no
  driver, panel or method. Filing it makes a surge readable, so the surge the field reads on a catastrophe's size
  became a rung: on the old quote 3 of its 16 forms filed Pennine (the catastrophe's loss, pooled: linear, quadratic
  and hinge), a cheap route onto the golden. Severn Vale's quote was re-priced from GBP 4.42 to 4.34 million (rate on
  line 29.47 to 28.93 per cent), which moves no other region and puts all 16 size readings on Severn Vale (SF22, with
  the claims-per-firm fit far ahead of every size reading); the default now ends on Severn Vale at GBP 0.0 million.
  Step 6 states the unit's case handling word for word and the rival clause in block 1 was rewritten for a runner-up
  at nil. Round 3's realism tells were fixed in the same pass (repair lags by peril, one claim a policy for a peril on
  a day, each catastrophe's own span); no graded figure but Severn Vale's value moved.
- 2026-10-26, stage 4 round 4 and judge pass 5 (eb9d2db9): architecture 2 spent. Reader O (sonnet) landed the call: it
  read RC-07 s.3's new sentence (the index does not carry what else made a catastrophe's repairs cost what they did)
  as demand surge, fitted the cost of a claim on claims per panel contractor (flat to about 17.5, then 3.9 per cent a
  claim a firm), re-priced each event at its 2027 load and filed Pennine at GBP 0.9 million, quoting the s.3 sentence
  and the contractor column as what decided it. Reader P (opus) read the same sentence as leaving the recorded surge
  in the costs and filed Severn Vale at the index alone (0 of 1 call, 4 of 20). The pass-5 judge returned
  DETERMINISTIC, FIX_NOW: the main call forced by the s.3 sentence and the claims, with the 2027 panel unfiled (a
  panel grown with the book, or a fit not carried past the 35 claims a firm on record, gives no uplift) and ask B's
  term identity read by policy number (10 to 30 million high, the rewrites' old terms kept). The dial is the
  architecture's own: filing that the index leaves out what a catastrophe's own repair load adds (Gate C, the pass-4
  SEND_BACK) hands a reader holding the panel-firm column the step (Gate F), and without the sentence the pass-4 judge
  read the index alone as the literal estimand. A call any reader lands is spent; re-root at stage 1, architecture 3
  (the last before the number is retired, which needs the author).
- 2026-10-27, re-root: architecture 3 moved to energy-systems-utilities (generation-capacity-planning) under the
  no-idle-pause rule; the insurance world and its panel-firm surge are not carried.
