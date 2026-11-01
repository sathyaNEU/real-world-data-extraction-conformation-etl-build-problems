# task133 design note: Matiri Forest Products, FY2028 log truck loads to Port Kowhai under the 50MAX limits

Private, never ships. Architecture 4, drawn 2026-11-01 after architecture 3's stage 4 SEND_BACK (the judge's Gate H line:
"decisive_step analytical only if the method is filed"; the ICAAP standard read word for word gave each borrower its
own division's change, the default path, so the payer route was an unfiled convention). The lesson this draw applies:
the easy route has to be wrong by the data, not by a convention the filed text never states. Here the easy route lets a
log truck carry what the raised mass limit allows, and the data say it cannot: the scaling volumes and the fleet
register's full-bunk volumes show the short grades fill their bunks a few tonnes above today's payloads. The
architecture 3 note is kept below as `## Architecture 3 record`, architecture 2's as `## Architecture 2 record`.

Stage 4 round 1 (2026-11-01, target.zip e53d1a72): DETERMINISTIC, FIX_NOW, Gates G and H PASS, the leak reader no leak.
Fixed in the generator in one pass: the cartage window filed as the loads' year; the payload conventions the WHAT
licenses (per-load or grade-mean density, mean payload or mean of inverse payloads, the 44 t units recomputed or at
their FY2026 net, every linking window) spread the total over about 145 loads, wider than a 100-load bin, so the loads
are graded at the precision the per-load data carry (total to 500, grades to 100) and the plan's grade yields are tuned
so every convention sits mid-bin; the fleet register and the planning basis rewritten for realism. Resume: the re-judge.

## Draw

- Pairing: Urban & Regional Science (`urban-regional-science`), task type `forecasting` (F), objective Forecasting &
  Predictive Modeling. The call faces forward: the export log loads the FY2028 harvest plan needs once the route to
  Port Kowhai opens to 50MAX vehicles on 1 July 2027.
- Shape 14 (cuts by segment): the total and the five export grades (6), three critical components, six carriers'
  cartage (ask A), three mills by four quarters (ask B, 12), the chart and the two files: 30 criteria.
- World: Matiri Forest Products Limited, five Hawke's Bay forests, 62 contracted units across six carriers (48 nine-axle
  units holding 50MAX permits), FY2026's 30,036 port loads carrying 764,072 tonnes; the FY2028 plan's export tonnes
  813,000; the port weighbridge tickets (30,036 rows), the port's log scaling records, the fleet register, the grade
  specification, the route approval and the cartage planning basis.
- Candidates written before choosing (fates in `## Tried and rejected`): (1) this draw; (2) a campus winter peak after
  heat-pump conversions, the warm-up surge beyond the units' output (energy load-forecasting: banned the moment task138's
  fresh card took the pairing); (3) a port's export tonnes after channel dredging, the berth pocket binding next; (4) a
  contact centre's offered calls once abandonment falls, retrials shrinking; (5) a bus fleet's winter range; (6) a
  bowel screening programme's first-round colonoscopy demand in a new district; (7) an airline's reactionary delay on
  tighter turns.
- Card: `.claude/skills/fingerprint/cards/task133.json`, registered 2026-11-01 (WARN only: repeat.gate_g and
  repeat.decision against task138 v3, first names on older builds); the structural NOTEs differentiated against task141,
  task142, task148 and task173; re-checked after registration.
- Personas from `guard.py names --geo "New Zealand" --seed 133` (the two used by architecture 3 left out): Belinda Carson,
  Stacey MacKay (fleet register), Nicole Clifford (harvest plan), John Morris (planning basis), Adam Fletcher, Christine
  Cumming.
- Data-native sentence: in this dataset a load's density lives only in the pairing of two systems that never share a
  key, the port weighbridge's net tonnes and the scaling station's JAS volume for the same truck minutes later, and each
  unit's full-bunk volume by log length lives only in the fleet register; the tickets carry no gross mass and no record
  says which limit a load hit.

## Survivor anatomy

- Actor: the deciding property, how much more each load could carry before its bunks are full, has no column: the
  tickets hold net tonnes, the scaling holds JAS volume, the register holds the unit's tare and full-bunk volumes by log
  length, and only their combination per load gives the headroom.
- Link: a ticket and its scaling record share no reference; they are paired by truck registration and the scaling
  station's time a few minutes after the weighbridge's, and the two units re-registered in February are read through
  the register's previous registrations.
- Reflex: the field's payload-gain reckoning for a higher mass limit (each permit unit's load rises to the new gross
  less its tare; the productivity case HPMV and 50MAX approvals are argued on) sits at rung 1 and files 27,000 loads.
- Back-test: the textbook route validates: under the 44-tonne limit it reproduces FY2026, since 86 per cent of FY2026
  loads sat at the mass limit and the rest are already full; nothing in the record says the bunks bind for the loads
  that were mass-limited.
- Second use: the weighbridge tickets are the cartage invoices' references (ask A), the fleet register names each unit's
  carrier (ask A) as well as its tare, the scaling records are the port's export documentation; the decisive step adds
  no file.
- Shock: nothing moves in the record; the FY2028 loads by grade read as ordinary growth on FY2026, and the short grades'
  shortfall shows only against the mass-only uplift.
- Pins: the WHAT is filed in the cartage planning basis (a load, FY2028, the fleet with each unit's tare, 50MAX permit
  and full-bunk volume for each log length as the register records them, each grade's loads as the plan's tonnes over
  the average payload FY2026's loads would carry on the same units, the limits) and the council's approval; the default
  is an omission inside that WHAT (it leaves out the full-bunk volumes the fleet sentence lists), and no filed sentence
  says which limit binds, how a load's density is found or how mass and volume combine.

## Default path

1. Take FY2026's port loads from the weighbridge tickets and each unit's tare and 50MAX permit from the fleet register.
2. Give each permit unit's load the FY2028 route limit: 50 tonnes gross less its tare; the other units stay at 44 less
   their tare (planning basis, RDC-2026-114).
3. Average each grade's FY2028 payloads and divide the plan's export tonnes for the grade by it (planning basis).

Ends on: 27,000 loads (26,787 unrounded; A 4,900, Pruned 2,300, K 7,200, KI 6,900, KIS 5,500).
Golden: 29,000 loads (28,945 unrounded; A 4,900, Pruned 2,500, K 7,500, KI 8,000, KIS 6,100).

## Stump sentence

A strong analyst lets each 50MAX permit unit's load rise to 50 tonnes gross less its tare and files 27,000 loads; the
step that lands it there is ignoring the bunks: the scaling volumes and the register's full-bunk volumes show the
short-length grades fill their bunks a few tonnes above today's payloads, so they gain a fraction of the six tonnes the
new limit allows and FY2028 needs 29,000 loads.

## Three rules

- Task type: forecasting in Urban & Regional Science, which serves Forecasting & Predictive Modeling: the freight
  movements a regional harvest plan puts on a route in a coming year under a changed vehicle mass limit.
- Domain test: the deciding quantity is each log truck load's payload under the FY2028 route limits, which log
  transport planning gets from the unit's gross mass limit less its tare and the volume its bunks hold for the logs'
  length at the load's density; with another field's nouns the gross mass limit, the tare, the bunk volume by log
  length and the JAS volume per load have nothing to attach to.
- Swap: "how many log truck loads will the harvest need once the route opens to 50MAX" becomes "how many ward
  admissions will the season need once the beds open": the gross mass limit, the tare, the bunks' volume by log length
  and the scaled JAS volume of each load stop making sense.
- Layer 1: the weighbridge keeps net tonnes only and the fleet register the tare; the scaling station keeps its own
  clock and reference and keys loads to the truck's plates; two units changed plates mid-year; JAS volume beside green
  tonnes; grade codes on tickets and grade names in the plan; the register numbered by Matiri's induction across
  carriers; subcontracted units billed under their head contractor; credit notes reversing lines billed twice; mill
  dockets dated when posted. Each is produced by the system that holds it and none decides the call (asserted).
- Layer 2: estimand identification under a binding constraint: relaxing the limit that binds a load lifts it only
  until the next one binds, and for the short grades the next one, the bunks' volume, sits a few tonnes above today.
- Decisive step: recognising that a raised mass limit lifts a load only until its bunks are full, so each load's
  FY2028 payload is the lesser of its unit's new gross less tare and its full-bunk volume for the grade's length at the
  load's own density.
- Not semantics: every field can be read right (net tonnes, tare, permit, the limits, the grade lengths) and the
  analyst still lets each permit unit load to 50 tonnes gross, which is how a mass-limit change is reckoned, and files
  27,000; no field says a load's bunks were nearly full.
- Not rule application: the approval and the planning basis set the limits and the arithmetic, and no filed rule says
  a load stops at its bunks. The enumerated family spans 26,000 to 29,000 (fleet average plus six tonnes 25,860;
  permit units to the new limit 26,787; one bunk volume per unit 26,793; plus six tonnes on permit units 27,064; only the
  loads at the old limit lifted 27,175; the golden 28,945); the standing family (per-load or grade-mean density, mean
  payload or mean of each load's inverse payload, the 44 t units recomputed or kept at their FY2026 net, the tonne- and
  unit-weighted averages, the re-registered units' early loads kept or dropped, any linking window from 30 to 90
  minutes) spans 28,922 to 29,067, one 500-load bin; what rules the rest out is the data, the register's full-bunk
  volumes against the loads' JAS volumes.
- Analyst test: a strong analyst who reads the 50MAX approval, the fleet register and the harvest plan correctly, lets
  every 50MAX permit unit's load rise to 50 tonnes gross less its tare and divides the plan's tonnes by the new average
  payloads files 27,000 loads, because the short-length grades fill their bunks before they reach 50 tonnes.
- Estimand: the cartage planning basis (cartage_planning_basis_FY2028.docx, "What we are sizing" and "How we get to
  FY2028 loads") with RDC-2026-114: FY2028 loads for a grade are the plan's export tonnes for the grade over the average
  payload that grade's FY2026 port loads would carry on the same units in FY2028, each unit with the tare, 50MAX permit
  and full-bunk volume for each log length the register at 30 June 2026 records for it, permit units at 50 tonnes gross
  and others at 44.
- No decoy: nothing is planted: no file states a payload under the new limits, a load count for FY2028 or which loads
  are mass-limited; the approval states the legal limits truly; the fleet register's volumes are the units' own.
- No certified replay: the method is not recovered by reproducing any certified or published figure; no control total
  ties only under the golden and no document carries a graded figure.
- Lesson: a relaxed constraint helps only until the next one binds, and the next one has to be looked for in the
  record; a model learns to check what a load can physically carry before counting the gain a rule change allows. No
  build on file reads a freight forecast through a second physical limit (guard heart).

## Readability screen

| Rung | Answer | What a solver would need to see | Verdict |
|---|---|---|---|
| R0 fleet average payload plus six tonnes | 26,000 | the limit change alone | readable |
| R1 permit units to 50 t gross less tare (the field's reckoning) | 27,000 | the register's tare and permit | readable |
| R2 only the loads at the 44-tonne limit lifted, to the new limit | 27,000 | gross from net plus tare | readable |
| Golden: each load capped by its bunks at its own density (decisive) | 29,000 | the scaling volume paired to each ticket by truck and time against the register's full-bunk volume for the grade's length | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative and its call | Ruled out by |
|---|---|---|---|---|
| SF1 | load | one trip to Port Kowhai weighed over the port weighbridge | none | the basis (same call) |
| SF2 | FY2028 | 1 July 2027 to 30 June 2028 | none | the basis |
| SF3 | fleet | the register at 30 June 2026 | none | the basis; every plate maps (asserted) |
| SF4 | FY2028 payload | the lesser of new gross less tare and full bunks at the load's density | the mass limit alone: 27,000 | the register's full-bunk volumes against the loads' JAS volumes (physics; no FY2026 load exceeds its bunks) |
| SF5 | limits | 50 t gross with a permit, 44 t without | none | the basis, RDC-2026-114 |
| SF6 | loads by grade | plan tonnes over the grade's average FY2028 payload | none | the basis |
| SF7 | density | each load's net over its JAS volume | the grade's mean density: same call | same call (asserted) |
| SF8 | linking | the same truck's scaling record within the hour | any window 30 to 90 minutes: same links | asserted |
| SF9 | re-registered units | read through previous registrations | early loads dropped: same call | same call |
| SF10 | log length | the 2025 grade specification | none | the specification (asserted) |
| SF11 | rounding | total to 500, grades to 100 | none | the prompt; every convention inside the bins (SF11.1 to SF11.10, SF11.w asserted) |
| SF12 | plan tonnes | the Export sheet | the domestic sheet added | the basis (export loads to the port; its Export sheet) |
| SF13 | payload | the ticket's net tonnes | none | the ticket (asserted) |
| SF14 | the FY2026 base | tickets 1 July 2025 to 30 June 2026 | none | asserted |
| SF15 | route | every forest's road in the approval | none | RDC-2026-114 (asserted) |
| SF16 | cartage carrier | the carrier whose unit hauled the load | the billed code | the basis |
| SF17 | credit notes | netted | left out | the basis, "net of any credit note" |
| SF18 | delivery quarter | the date the load crossed the mill weighbridge | the docket's posting date | the basis, "by delivery date" |
| SF19 | tonnes delivered | gross less tare at the mill | none | equal to the docket (asserted) |
| SF20 | Matiri loads at the mills | the MFP docket series | none | asserted |
| SF21 | average payload | the mean of the loads' FY2028 payloads | the mean of each load's inverse payload, tonne- or unit-weighted: same call | same call (asserted) |
| SF22 | the 44 t units' FY2028 payload | recomputed from tare, bunks and density | kept at the FY2026 net: same call | same call (asserted) |
| SF23 | FY2026 cartage window | what was paid for FY2026's loads, July invoices, re-bills and credits included | invoices dated in FY2026 | the prompt and the basis ("paid for FY2026's loads"); asserted |

## Ladder

| Rung | Construction | FY2028 loads | Graded |
|---|---|---|---|
| R0 | fleet average payload plus six tonnes | 25,860 | 26,000 |
| R1 | permit units to the new limit (the field's reckoning) | 26,787 | 27,000 |
| R2 | only the loads at the 44-tonne limit lifted, to the new limit | 27,175 | 27,000 |
| Golden | each load capped by its bunks at its own density | 28,945 | 29,000 |

Every rung files another total bin and misses at least four of the five grades; the nearest wrong total is R2, 6.1 per
cent low.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | FY2026 port loads; the plan's export tonnes | the basis ("What we are sizing", the Export sheet) |
| 2 Unit of account | the load | the basis |
| 3 Attribution window | FY2028 for the plan, FY2026 for the base | the basis, the files' own windows |
| 4 As-of dating | the register at 30 June 2026 | the basis |
| 5 Version basis | the 2025 grade specification; RDC-2026-114; basis version 2 | document control |
| 6 Denominator | the grade's average FY2028 payload | the basis |
| 7 Weighting | each FY2026 load once | the basis (an average of loads); inverse, tonne- and unit-weighted averages file the same bins (asserted) |
| 8 Window length | the whole of FY2026 | the basis |
| 9 Boundary inclusivity | limits "up to" 50 and 44 t gross | no FY2026 load above 44 t gross (asserted) |
| 10 Rounding path | unrounded payloads and loads, rounded once | prompt; every convention inside the bins (asserted) |
| 11 Tie-break | none | not applicable |
| 12 Maturity and censoring | none: a year's loads | not applicable |
| 13 Order of operations | payload per load, then the grade average, then the plan's tonnes over it | the basis |
| 14 Row order | sums | C1 |
| 15 Duplicate resolution | one scaling record per ticket | asserted (each record used once) |
| 16 Identity normalisation | plates to units through current and previous registrations | asserted; dropping early loads same call |
| 17 Netting against gross | net tonnes per ticket | the ticket |
| 18 Dimensional units | tonnes, JAS m3, t per JAS m3 | the files' headers |
| 19 Code and status semantics | grade codes to lengths; permit Y or N | the specification and the register; never the stump |
| 20 Integerisation | loads unrounded until reported | prompt |
| 21 Clause scope | limits for every forest's route | RDC-2026-114 |
| 22 Forward window contents | the plan's FY2028 tonnes; the FY2026 loads re-run | the basis |

## Literal reader

A reader executing the planning basis word for word takes FY2026's port loads, re-runs each on the same unit in FY2028
at the limits the basis and the council's approval set, averages each grade's payloads and divides the plan's tonnes by
them. "The payload the loads would carry" is not filed as the legal maximum; it is what the load would weigh, and the
data say what that is: the register's full-bunk volume for the grade's length times the load's density caps it, and no
FY2026 load exceeds its bunks. Reading the payload as the mass limit less tare is the easy method on the same estimand,
which puts more logs on the short-grade loads than their bunks hold. Every licensed convention (SF7 to SF9, SF21, SF22)
files 29,000 and the same five grades, the tightest grade 29 loads inside its bin and the total 172; the ask readings
are closed in SF16 to SF20 and SF23.

## Oracles

- The export log prices, the vessel calls and the forest road closures (distractors): none states a payload or a load
  count, and none ties to a graded figure.
- The grade specification: lengths only.
- The approval: legal limits only, true as stated.
- None ties only under the golden; no document states a graded figure (asserted, R3c).

## Ask sheet

- Ask A, the cartage paid for FY2026's loads by the carrier whose unit hauled the load (six figures, NZD thousand):
  primary A1, subcontracted units billed under their head contractor's carrier code, the hauler found only by pairing
  each invoice line's ticket to the port weighbridge's plate and the plate to the register's carrier (D7, a key worked
  out across three files); hazard: lines billed twice and their credit notes. The window is the loads' year (SF23).
- Ask B, FY2026 domestic deliveries by mill and quarter (twelve figures, tonnes): primary B1, the docket extract dates
  each load when the docket was posted, days after delivery, while the delivery date sits only in the mills' weighbridge
  logs among every other supplier's trucks (D8, a reconstruction across two files); hazards: two dockets re-sent in the
  July batch, the docket extract missing the late-June deliveries posted in July.
- Separation: the call reads the port tickets, the scaling records, the register, the plan and the grade
  specification; the asks read the invoices (with the tickets and register) and the mills' dockets and logs; deleting
  every ask file leaves the call (asserted).
- Pair ceiling: 28.5 (cracker C 45.0 keeping 0 of 18 ask figures, mirror S 12.0; 46.8 if the cracker also finds one silent device)
- Mirror leakage: 0.0 per cent of ask weight (the mirror handles the asks as the cracker does)
- Measured by: generator/ceiling.py on the cut pack (target.zip 4a9ed312)

| Ask | Cracker's stop on the cut pack | Device it misses | Cracker keeps | Verdict |
|---|---|---|---|---|
| A cartage by hauling carrier (6) | invoice carrier codes, credit notes netted | A1 subcontract billing | 0 of 6 | miss |
| B mill deliveries by quarter (12) | docket dates, re-sent dockets dropped | B1 posting dates | 0 of 12 | miss |

## Leak review

`leak.py --asof 2026-10-20` on the final cut (target.zip 4a9ed312): REVIEW, no LEAK. Each REVIEW line ruled:

- Sweep 3, the planning basis carries the call's words and names Port Kowhai beside them: it is the governing document
  that defines a load, FY2028, the fleet and the limits for the port it plans for, and it states no figure of the call.
  Harmless.
- Sweep 4, the approval shares permit and limits: the council's legal limits, true as stated. Harmless.
- Sweep 4, the planning basis shares register, record, volume, permit, payload and credit: it files the WHAT (each
  unit's tare, 50MAX permit and full-bunk volume for each log length as the register records them, the payload FY2026's
  loads would carry on the same units, the limits, cartage net of credit notes), the listing the default omits; no
  sentence says which limit binds, how a load's density is found or how mass and volume combine (asserted, R3c).
  Harmless.
- Sweep 6, the fleet register names the carriers beside numbers: tares and bunk volumes, no cartage and no ranking.
  Harmless.
- Sweep 6, the harvest plan names the grades beside numbers: planned tonnes, not loads. Harmless.
- Sweep 5 (announcements) is clean on this cut: the note's first title, "Logistics planning note: ...", matched the
  "note:" pattern and was retitled.

## Architecture 3 record

The Orari Bank ICAAP business-book stress (stress-testing-capital), built 2026-11-01 (target.zip d613bac0) and spent the same day at stage 4 (SEND_BACK, Gate H). Its note as it stood, headings demoted one level.

### Orari Bank, the ICAAP 2026 severe-scenario loss on the business banking book

Private, never ships. Architecture 3, drawn 2026-11-01 at the Batch 3 queue reset. Architecture 2 (Bellbird personal
loans, the 30 September 2026 ECL allowance in expected-credit-loss-provisioning) landed on the portal: the survival-to-date
conditioning was the field's reflex. Its world is closed (one architecture per world) and its note is kept below as
`## Architecture 2 record`. This architecture moves to a never-drawn task type, stress-testing-capital, in a new world:
Orari Bank Limited, a South Island regional bank headquartered in Timaru, stressing its business lending book for the
2026 ICAAP under the severe scenario its Board approved on 24 September 2026.

### Draw

- Pairing: Banking, Credit & Financial Risk (`banking-credit-financial-risk`), task type `stress-testing-capital` (F),
  objective Forecasting & Predictive Modeling. The committed call faces forward: the stressed credit loss the scenario
  puts on the book in the stress year 1 October 2026 to 30 September 2027.
- Shape 14 (cuts of a distribution by segment): the call (1) and its six reporting segments (6), two critical
  components, twelve net credit loss cells (ask A), five bands' default counts and shares (ask B, 10), the chart and
  the two files: 34 criteria.
- World: 645 business customers on the 30 September 2026 book (632 performing, 13 in risk grade D), 1,346 facilities,
  EAD NZD 496.7 million; a year of operating-account credits (74,491 rows); the NZBN extract for Canterbury, Otago and
  Southland (26,300 entities); CR-ST-02 v3.1 (the business banking stress standard) and the board-approved scenario.
- Candidates written before choosing (fates in `## Tried and rejected`): (1) this draw, the sector scenario read through
  the industries that pay each borrower; (2) deposit-liquidity-behaviour, business deposit run-off by depositor type
  under the same scenario; (3) a term-deposit renewal ladder; (4) intraday payment netting after a merger;
  (5) lenders mortgage insurer capacity under the house-price path; (6) presale settlement risk on apartment
  development loans; (7) a head contractor's failure spreading to its subcontractor borrowers.
- Card: `.claude/skills/fingerprint/cards/task133.json`, registered 2026-11-01 (WARN repeat.gate_g only, the lane's
  objective); re-checked after the build, still WARN only. Strategy `other` (exposure transmission through the paying
  counterparties); forum board_of_directors, role finance_controller, context artifact register.
- Personas drawn with `guard.py names` for New Zealand and recorded on the card's world.people: Julie Dawick (the
  standard's author), Wendy Russell (the scenario), Keanu Boyd (the deposit listing), Tania Rees (collections receipts),
  Marilyn Kendall (overrides).
- Data-native sentence: in this dataset a business's sales are a year of named payments into its operating account, and
  the clearing system's payer names, matched to the NZBN register, are the only place the industries that pay each
  borrower appear; the lending book carries only the borrower's own industry code.

### Survivor anatomy

- Actor: the deciding property, the share of a borrower's sales each industry pays, has no column in any file: the
  lending book carries the borrower's own industry code, the credits carry a payer name the clearing system upper-cased
  and cut at 20 characters, and the register carries BIC codes keyed by legal and trading names.
- Link: the payer is read through a link no key offers: a credit's other-party string, normalised (upper case, LIMITED as
  LTD, & as AND, first 20 characters), against the register's legal or trading names; card settlements, branch cash and
  payments from individuals carry no industry and are the borrower's household sales.
- Reflex: the field's sector stress (each borrower at the scenario path of its own ANZSIC division, the industry PD
  multiplier every bank runs) sits at rung 0 and files NZD 10.0 million.
- Back-test: the textbook route validates: wherever the lending book carries a 2006 BIC code it agrees with the
  register's for every borrower, the blank and 1993-coded rows fill cleanly from the register, the own-division losses
  sum by segment to Table 4 with nothing left over, and every division the book holds has a scenario path.
- Second use: the credits extract is the bank's own record of each borrower's sales, the base CR-ST-02 2.1 measures the
  scenario's change against ("against the year to the book date"); the register fills the lending book's blank and
  1993-coded industry fields on every route; the decisive step adds no file.
- Shock: the movement the step recovers is ordinary: manufacturing, trade and logistics and business services rise,
  construction falls, hospitality holds; no borrower is the pack's largest anomaly and the golden's high-loss set is not
  an interval of any shipped statistic (grade, EAD, own division's path).
- Pins: the WHAT is filed in CR-ST-02 (stressed loss, the stress year, the 12-month PD, the fall in the borrower's own
  sales, Table 2, LGD, EAD, segments, net credit losses, the back-test) and the Board's scenario; no filed sentence names
  payers, receipts, a mix or a weighting.

### Default path

1. Take business_lending_book_2026-09-30.csv, drop the 13 customers in risk grade D (CR-ST-02 1.3) and set EAD per 3.4.
2. Fill each borrower's ANZSIC division from its BIC code on the NZBN extract where the book's industry field is blank
   or on the 1993 codes (4.1).
3. Stress each borrower at the severe scenario's sales change for its own division (the sector stress a bank runs).
4. Table 2 multiplier on that fall, Table 1 PD times the multiplier, Table 3 LGD per facility, sum by segment and book.

Ends on: NZD 10.0 million (9.804 unrounded; construction 2.9, manufacturing 0.6, trade and logistics 1.6, hospitality
3.4, business services 0.8, health 0.4).
Golden: NZD 11.5 million (11.4999 unrounded; 2.5, 1.3, 2.4, 3.4, 1.5, 0.4).

### Stump sentence

A strong analyst stresses each business borrower at the severe scenario's sales path for its own ANZSIC division and
files NZD 10.0 million; the step that lands it there is reading the fall in a borrower's own sales off its industry
label when its operating-account credits show who pays it: 56 per cent of the book's trading credits come from other
divisions, largely the builders, hotels and tour operators the scenario cuts by a quarter, so the transport, wholesale,
labour-hire and engineering firms they pay take far steeper Table 2 multipliers than their own divisions' paths give.

### Three rules

- Task type: stress-testing-capital in Banking, Credit & Financial Risk, which serves Forecasting & Predictive
  Modeling: a one-year stressed credit loss under a board-approved forward scenario.
- Domain test: the deciding quantity is each business borrower's stressed one-year probability of default under the
  ICAAP severe scenario, the bank's revenue-shock PD table applied to the fall in the borrower's own sales, with the
  stressed LGDs and EAD summed over the book; with another field's nouns the scenario's industry sales paths, the PD
  table and the stressed LGDs have nothing to attach to.
- Swap: "how much credit loss does the severe scenario put on our business banking book" becomes "how many bed-days does
  the flu season put on our hospital": the industry sales paths, the borrowers' paying industries, the revenue-shock PD
  table and the stressed LGDs stop making sense, because a hospital's demand does not arrive through who pays its
  suppliers.
- Layer 1: the clearing system upper-cases and cuts payer names at 20 characters; merchant-acquirer settlement batches
  and branch cash carry no cardholder; own-account transfers, GST refunds, insurance claims, loan advances and credit
  interest sit among the trading credits; the lending book's industry field is blank or on the 1993 code set for
  borrowers migrated from the earlier platform; names as Ltd or Limited; public bodies across divisions O, P and Q;
  each produced by the system that holds it and none placed to be caught (mess-neutral, asserted).
- Layer 2: estimand identification in credit stress transmission: a sector scenario reaches a lender's borrower through
  the industries that buy from it, weighted by what each pays, and Table 2's steep convex bands make an averaged mix
  understate the loss.
- Decisive step: recognising that a borrower's own sales fall under the scenario is the change for the industries that
  buy from it, weighted by what each paid it in the base year, and not the change for the industry it is classified in.
- Not semantics: every field, code and definition can be read right (the register's BIC, the 1993 codes mapped, card
  settlements as household spending, non-sales credits out) and the analyst still stresses each borrower at its own
  division, which is how sector stress is run, and files NZD 10.0 million; no field or code carries a payer's industry.
- Not rule application: CR-ST-02 keys the multiplier on the fall in the borrower's own sales and the scenario states
  division sales changes; no filed rule says how a division path becomes one borrower's own sales fall. The enumerated
  family spans 8.18 to 11.96 (own division 9.80, division-average mix 10.53, count-weighted mix 10.44, the acquirer as
  payer 9.08, households at the retail path 8.18, the harsher of the two 11.96, class-average mix 11.45); the standing
  family (value-weighted read-through under every licensed convention: legal or trading names, public bodies at their
  own division or O, the book's legacy letters, a six-month base, non-sales credits in or out) spans 11.458 to 11.574,
  one bin; what rules the rest out is the receipts themselves, quietly, since no sentence names payers.
- Analyst test: a strong analyst who fills the legacy industry codes from the register, reads the standard, the
  scenario and the PD table correctly and stresses each borrower at its own ANZSIC division's sales path files NZD 10.0
  million, about a seventh low, because the receipts show 56 per cent of the book's trading credits come from other
  divisions, largely the builders and hotels the scenario hits hardest.
- Estimand: CR-ST-02 3.1 to 3.4 with 2.1 and 2.2 (CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx): stressed
  PD times stressed LGD times EAD summed over the business book's facilities at 30 September 2026 not in default, for the
  twelve months to 30 September 2027, the stressed PD being the Table 1 PD times the Table 2 multiplier for the fall in
  the borrower's own sales under the scenario against the year to the book date.
- No decoy: nothing is planted: no shipped file states a business-book stressed loss, a borrower's payer mix or a sector
  multiplier per borrower; the rural summary is another book's stress (a declared distractor); the lending book's
  industry code is the borrower's own and correct as far as it goes; no memo argues the own-division answer.
- No certified replay: the method is not recovered by reproducing any certified or published figure; the scenario and
  Table 2 are inputs, no control total ties only under the golden, and no document carries a graded figure.
- Lesson: a sector shock reaches a lender's borrowers through who pays them, so a borrower's industry label is not its
  exposure; a model learns to read a counterparty's sources of revenue before mapping it to a sector path. No card on
  file reads a stress or forecast through the paying counterparties (guard heart).

### Readability screen

| Rung | Answer | What a solver would need to see | Verdict |
|---|---|---|---|
| R0 own division's path (the field's sector stress) | NZD 10.0 million | nothing: the standard, the scenario and the book's code suffice | readable |
| R1 the receipts' payer mix averaged over each division | NZD 10.5 million | that receipts matter, without carrying them to the borrower | readable |
| R2 card settlements read as payments by the acquirer (division K) | NZD 9.0 million | a field read wrongly (the settlement particulars) | readable |
| R3 the harsher of own division and payers for every borrower | NZD 12.0 million | an over-correction of the decisive step | readable |
| Golden: each borrower's own sales fall through its payers (decisive) | NZD 11.5 million | a relation between the credits' payer strings and the register no column holds, no sentence invites and the field's method does not ask for | silent |

### Semantic fork table

| Id | Term or convention | Golden reading | Alternative and its call | Ruled out by |
|---|---|---|---|---|
| SF1 | stressed loss | PD x LGD x EAD summed over facilities | none | CR-ST-02 3.1 (same call) |
| SF2 | stress year | the twelve months to 30 September 2027, 12-month PD | lifetime loss | 2.2 and Table 1's 12-month PD |
| SF3 | the borrower's own sales | what its payers pay it, each at its division's change, households at its own | its own division's change: NZD 10.0 million | 3.2's "the borrower's own sales" against 2.1's "the division's sales", with 56 per cent of credits from other divisions |
| SF4 | sales | trading credits only | every credit: 11.458, same call | same call |
| SF5 | base period | the year to the book date | six months: same call; the last quarter: business services 1.6 | 2.1 "against the year to the book date" |
| SF6 | card settlement batches | household spending at the borrower's own division | the acquirer as payer: NZD 9.0 million | the batches' own particulars (SETTLEMENT, a merchant ID) from two acquirers |
| SF7 | public bodies | each at its own BIC division | all at O: same call | same call |
| SF8 | the borrower's division | its BIC on the NZBN register | the book's 1993 letters: same call | 4.1 and same call |
| SF9 | payer names | legal or trading name | legal names only: same call | same call |
| SF10 | weight of a payer | the amount it paid | count of credits: NZD 10.5 million | the scenario states sales in NZD million |
| SF11 | payments from individuals | household sales at the borrower's division | left out: total same, manufacturing 1.4 | no unmatched payer carries a company word; 3.2's own sales include them |
| SF12 | households' spending path | the borrower's own division | the retail path for all: NZD 8.0 million | 2.1, each division's own sales |
| SF13 | EAD | drawn plus half the undrawn limit on revolving products | none | 3.4 (same call) |
| SF14 | customers in default | outside the stress | none | 1.3 (same call) |
| SF15 | Table 2 band edges | "or more" and "less than" | a fall on an edge | no fall within 0.02 points of an edge (asserted) |
| SF16 | the 100 per cent cap | never binds | none | asserted (same call) |
| SF17 | a sales rise | multiplier 1 | none | 3.2 "keeps its 12-month probability" |
| SF18 | segment | own division on the register, Table 4 | none | 4.1 (same call) |
| SF19 | rounding | total to NZD 0.5 million, segments 0.1 | none | the prompt; edges 0.25 and 0.05 (asserted) |
| SF20 | halves | October to March, April to September | none | 2.3 |
| SF21 | recovery timing | in the half received | the write-off's half | 4.2 "in the half" |
| SF22 | recovery amount | the agency's net remittance | its statement upload as well | 4.2 "the bank received" |
| SF23 | recoveries in scope | on loans already written off | receipts before write-off | 4.2 "already written off" |
| SF24 | portfolio | the business book | rural and commercial property rows | 1.2 |
| SF25 | segment of a written-off customer | its NZBN's division via the customer master | none | 4.1 (same call) |
| SF26 | risk grade at 30 September 2025 | the grade in force, override included | the model grade | Table 1 note on the grade in force |
| SF27 | default window | 1 October 2025 to 30 September 2026 | none | 4.3 "following twelve months" (asserted) |
| SF28 | grade D customers in 2025 | in no band | none | same call (asserted) |
| SF29 | share | the band's defaults over its borrowers | none | 4.3 (same call) |
| SF30 | which customer defaulted | the customer the lending book shows holding the facility | the register's customer number | the lending book's facility holder (the register's number is the group lead) |

### Ladder

| Rung | Construction | Book total (NZD m) | Graded |
|---|---|---|---|
| R0 | own division's path, the field's sector stress | 9.804 | 10.0, five of six segments off |
| R1 | the receipts' mix averaged by division | 10.528 | 10.5 |
| R2 | acquirer settlements as financial-services payers | 9.075 | 9.0 |
| R3 | harsher of own division and payers | 11.955 | 12.0 |
| Golden | each borrower's own payers, households at its division | 11.4999 | 11.5 |

Separation: every rung files another total bin and misses at least two segments; the nearest wrong total is R1 at
NZD 10.5 million (8.5 per cent low) or R3 at 12.0. Not a candidate ranking, so the which-of-N margins do not apply.

### Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | facilities at 30 September 2026 of customers not in risk grade D | 1.2, 1.3 filed; 13 customers out (asserted) |
| 2 Unit of account | the facility for the loss, the borrower for the sales fall | 3.1, 3.2 |
| 3 Attribution window | stress year to 30 September 2027; base year to 30 September 2026 | 2.1, 2.2; the credits cover exactly the base year |
| 4 As-of dating | book date 30 September 2026 | 2.2, the book extract's name |
| 5 Version basis | CR-ST-02 v3.1, the scenario approved 24 September 2026 | document control; one scenario ships |
| 6 Denominator | a borrower's trading credits in the base year | 2.1's base year; SF4 and SF5 same call |
| 7 Weighting | by amount paid | SF10; the scenario's sales in NZD |
| 8 Window length | the whole base year | 2.1; six months same call (SF5) |
| 9 Boundary inclusivity | Table 2 "or more" and "less than" | no fall within 0.02 of an edge (SF15, asserted) |
| 10 Rounding path | facility losses summed unrounded, rounded once when reported | prompt; edges asserted (SF19) |
| 11 Tie-break | none (one figure) | not applicable |
| 12 Maturity and censoring | none: a one-year stressed loss on the book at the date | 2.2 |
| 13 Order of operations | PD times multiplier, cap, then LGD and EAD | 3.1, 3.2; the cap never binds (SF16) |
| 14 Row order | sums | C1, order-free |
| 15 Duplicate resolution | one row per facility and per credit | asserted unique facility numbers; credits are distinct events |
| 16 Identity normalisation | payer strings to register names: upper case, LIMITED as LTD, & as AND, 20 characters | C1: legal-only and full matching land the same call (SF9); no ambiguous match (asserted) |
| 17 Netting against gross | none on the call; ask A nets recoveries against write-offs by filed rule | 4.2 |
| 18 Dimensional units | NZD; per cent changes; per cent PDs | the documents' headers |
| 19 Code and status semantics | BIC from the register, 1993 codes, MS and DEP as household sales | 4.1; SF6, SF8; never the stump |
| 20 Integerisation | none | not applicable |
| 21 Clause scope | Table 2 per borrower; LGD per facility | 3.2, 3.3 |
| 22 Forward window contents | the scenario's division changes for the stress year | 2.1 and the approved workbook |

### Literal reader

A reader executing CR-ST-02 word for word stresses every facility of a business customer at 30 September 2026 not in
risk grade D, at its Table 1 PD times the Table 2 multiplier for the fall in the borrower's own sales over the stress
year under the scenario, against the year to the book date. The scenario states each division's sales change; a literal
reader has to say what the borrower's own sales are and how the scenario reaches them, and the pack's only record of a
borrower's sales is its operating-account credits, where each payment names who paid. Reading the division's change as
the borrower's own is the easy method on the same estimand (it substitutes the division's sales for the borrower's own,
which 2.1 and 3.2 distinguish), never another reading of a filed term; every value-weighted read-through under the
licensed conventions (SF4 to SF11) files NZD 11.5 million and the same six segments (asserted). The ask readings are
closed in SF20 to SF30 by 2.3, 4.2, 4.3, the Table 1 note and the records.

### Oracles

- The rural book stress summary (distractor): the rural book's own-sector stress under the same scenario; another book,
  no business figure, and its total ties nothing in the business book.
- The industry sales series (distractor): each division's quarterly history; no stressed figure, no borrower.
- The deposit listing (distractor): balances only.
- The scenario's macroeconomic paths sheet: context for the division paths; nothing ties to a stressed loss.
- None ties only under the golden; no document states a graded figure (asserted, R3c).

### Ask sheet

- Ask A, net credit losses by segment and half (12 cells, NZD thousand): primary A1, guarantors' receipts posted to their
  own personal collection cases (customer master: Personal), linked to the written-off company only through the
  guarantees register (D7, a key worked out across two files); primary A2, the agency's statement upload (gross of
  commission, days earlier) beside the remittance it becomes (D1); hazards: receipts before the first write-off, later
  further write-offs, rural and commercial property rows, struck-off companies' segments through the customer master.
- Ask B, defaults by risk-grade band at 30 September 2025 (5 counts, 5 shares): primary B1, a connected group's
  cross-default recorded per facility under the group lead's customer number, the true holder found only in the lending
  book (D7, a cardinality the register shows); hazards: overrides in force at 30 September 2025, the March 2026 merge
  log, business borrowers moved to the rural book whose defaults sit in the rural register, grade D rows in the snapshot.
- Separation: the asks read the call's register only for a written-off customer's segment and the lending book only
  for a facility's holder; zero device rows in the call's population (asserted); deleting every ask file leaves the call
  (asserted).
- Pair ceiling: 28.5 (cracker C 45.0 keeping 0 of 22 ask figures, mirror S 12.0; 43.5 if the cracker also finds one
  silent device)
- Mirror leakage: 0.0 per cent of ask weight (the mirror handles the asks as the cracker does)
- Measured by: generator/ceiling.py on the cut pack (target.zip d613bac0)

| Ask | Cracker's stop on the cut pack | Device it misses | Cracker keeps | Verdict |
|---|---|---|---|---|
| A net credit losses (12 cells) | agency upload paired off, receipts after write-off, business rows | A1 guarantors' personal cases | 0 of 12 | miss |
| B default counts (5) | overrides in force, both registers, merge log | B1 the group lead's number | 0 of 5 | miss |
| B default shares (5) | the same | B1 | 0 of 5 | miss |

### Leak review

`leak.py --asof 2026-10-16` on the final cut: REVIEW, no LEAK. Each REVIEW line ruled:

- Sweep 3, CR-ST-02: 2.1, 1.3 and 3.4 are the standard's own section numbers and 2.4 a version in its history table;
  none is a figure of the call. Harmless.
- Sweep 3, CR-ST-02 carries the call's words: the standard defines the stressed loss the call reports and states no
  figure of it. Harmless.
- Sweep 3, the rural summary carries the call's words: the rural book's own stress under the same scenario, a declared
  distractor whose figures are the rural book's. Harmless.
- Sweep 4, CR-ST-02 shares seven terms of the note's vocabulary (borrower, register, division, system, carries,
  multiplier): its sentences file the WHAT (the fall in the borrower's own sales, a borrower's segment following its own
  division on the NZBN register); none names payers, receipts, a mix or a weighting. Harmless.

## Architecture 2 record

The Bellbird personal-loan ECL allowance (expected-credit-loss-provisioning), shipped 2026-10-14 (target.zip 1fb3303f), landed on the portal and re-rooted 2026-11-01. Its note as it stood, headings demoted one level.

### Bellbird personal loans, the 30 September 2026 ECL allowance

Private, never ships. Round 2 (2026-10-14), the slot's second architecture under the same draw. The 10/10 audit found
the loop 1 build compliant but weak: its decisive step (conditioning a crude cohort curve on survival of both exits) sat
one rung above the step the v1 portal winner solved, and the development sample's prepaid outcomes beside a "share of
every loan drawn" header signposted it. Round 2 moves the decisive step inside the same world. There is no filed curve
any more: CRM-ECL-04 3.2 files the PD estimand and points at the loan system's record of every loan it has held, and the
record holds the earlier platform's loans only from the 1 October 2019 go-live, when the loan system took over those
still open. A competent PD build (monthly default and repayment rates by month on book, repayment as a competing exit,
the textbook survival product) counts those loans from their drawdown and fills every early month's loans at risk with
months the record never observed. The allowance is now reported in AUD million to one decimal. Ask A gains a second
silent device (reissued agency references); ask B keeps its June arrears clock, now with the record's default month as
in-world evidence. At stage 4 the judge reproduced the main call (13.179) and found both asks open: every Collections cure
taken at its word, the remittances taken where the receipts file posts them and the June column read as close of
business gave its own loss shares and counts. The asks repair (2026-10-14, main call frozen) files each in the text the
lender would write: 3.3 measures a loan the record shows written off on what it recovered, pools the share by balance
and keeps 70 and 76 per cent in force; the dictionary says what the receipts file's loan number and Wirraway's
reference hold, that a closed loan is in no stage, and records the job's move to the end-of-day snapshot at
CHG-26-0418; 2.2 says when a cancelled arrangement stops. No graded figure moved. The re-judge (round 2b) reproduced the main call,
the stage amounts and all eight loss shares and found one gap, slide 2's June clock: no file said the June extract counts
days past due to its run date. The dictionary's two loan book lines now record each extract's run clock (the judge's
prescribed fix), CRM-ECL-04 2.4, 3.3, 3.6 and the 4.2 history line read plainer. Round 2c gives ask B a new silent
device (B4: the June month end's scoring run carried one partition's last scores forward on 1 July and rescored it on 2
July), with no ask B figure moving, redraws the forum to the Audit and Risk Committee (deck arc_ecl_q3_2026.pptx) and the
hardship register's job-account persona, both against heart BLOCKs.

### Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task133.json`, edited in place for round 2 (the slot's 2026-10-11 draw kept: world, forum, forcing event, organisation), v1 and loop 1 in `lineage`; heart WARN, no BLOCK (GUARD lines in Ask sheet's tail and below) |
| Domain / task type | banking-credit-financial-risk / expected-credit-loss-provisioning (client domain itself) |
| Objective | Forecasting & Predictive Modeling: the allowance is the expected loss over each performing loan's next 12 months or remaining life, its PD estimated from the record's default and repayment experience |
| Shape | 02: one committed figure with its stage split, plus two grids (realised loss by product and quarter, 8 cells; the June book's stages by where they stand at 30 September, 16 cells) |
| Gate G mechanism | forecasting |
| Gap, pattern | population (who is at risk in each month on book: a taken-over loan only from the take-over), then time; pattern none, the generators leading with G12 |
| Generators | G12 absence of record against record of absence, G9 downstream survival against upstream acquisition, G13 horizon mismatch |
| Stump strategy | maturity_censoring (relabelled from stated_rule_hard_construction): left truncation, the record watching the taken-over loans only from the go-live; population_selection names the same risk-set error from the denominator side and is banned against task132 at this draw |
| Layer 2 family / pattern | estimation_fit / `own:delayed-entry-for-a-taken-over-book` |
| Decisive rule filed | no: 3.2 files the estimand (PD(k) for a loan in month on book a is the probability that a loan of the product open and not in default at the end of a first defaults at a + k, from every loan of the product in the record) and no method; nothing filed names entry, truncation, the risk set or the take-over's effect (asserted) |
| Official decoy, validated decoy | no, no |
| Decision | quantity_figure, currency |
| Stakeholder | Head of Credit Risk Reporting (finance_controller), to the Audit and Risk Committee (committee_or_panel, redrawn from board_of_directors in round 2c), at the quarter close (period_close) |
| Context artifact | register: the loan record, the loan system's list of every loan it has held |
| Calibration form | none |
| World | New South Wales, AUD; Bellbird Personal Finance (fictional non-bank lender); PL36, PL60; Wirraway Mercantile Agents (collections agency) and Tarwin Receivables Pty Ltd (debt buyer), both invented |
| People | Matthew Gardner, Stephanie Manning, Joseph Mitchell, Tamara Farrell, Adam Gordon, Renee Foster, Troy Olson, Natalie Hanna, Declan Wallace (round 2c, seed 133, for Vanessa King), Christine Fletcher (guard.py names, en_AU, seed 133; Vanessa King replaces Kayla Stokes, whose first name the guard now blocks against task118) |

**Data-native sentence.** Bellbird's loan system went live on 1 October 2019 and took over only the loans still open and
under 90 days past due on the earlier platform, so the record's 2014 to 2019 vintages are survivors (163 loans from 2014
against 5,271 from 2018, mostly PL60s from before 2017): 16,479 loans the record holds only from their month on book at
30 September 2019, whose earlier months could not end in a recorded default or closing, sit in every early month on
book's loans at risk if each loan is counted from its drawdown, and the young book (median month on book 14 for PL36,
21 for PL60) reads its PD from exactly those months.

**Sources.** `layer2-rigor-patterns.md`, banking (PD term structures from loan-level performance with prepayment as a
competing risk): teaches the default path's own construction; here the competing exit is the reflex and the step past it
is where exposure starts. `exemplars.md` (the client's ECL and survival tasks): the depth of a staged ECL build; none
turns on entry to observation. task134 v1 (an estimator under censoring with competing exits, landed): the reason the
audit's suggestion (Aalen-Johansen on right-censored vintages) was not taken; censoring and competing exits are the
default path here. task255 (deductibles carried as truncation on a size distribution): truncation of sizes by a floor;
here it is truncation in time, by the date a record began. task132 (module-age band rates over a go-live window with
renewal): a renewal process; here a loan defaults once and the issue is which months the record watched.

**Layer 1 (the mess, and the systems that make it).** A loan system extract that gives drawdown and first-repayment
dates rather than months on book, repayment dates moved to the next NSW business day; a loan record carrying the earlier
platform's loans under their own lower numbering block, defaults at month ends and closures by reason; a hardship
register of approved, active, completed and cancelled arrangements whose status is set by a Tuesday-night batch and read
as at 30 September, with the 2020 and 2021 COVID-19 deferrals loaded in bulk and never moved on; origination scores on
two scorecard versions with a published conversion; scenario weights in a committee workbook beside the prior quarter's;
the June quarter-end extract from the same job without the behaviour score column (added by a change in July) and, from
before the same change, counting days past due to its 07:30 run, beside month-end scoring runs stamped with the day each
run was made; a Collections MI file whose case resolution is set when the case closes, so a cure recorded on an approved
arrangement stands after the arrangement is withdrawn; a receipts ledger across every cohort with dishonoured direct
debits reversed by negative rows, one debt-sale receipt carried without a loan number and agency remittances posted by
the reference they quote; the agency's placement report with its own column names and day-first dates, whose references
the agency reissues after a placement closes; the sale schedule priced in cents per dollar of face value; a write-off
file and a roll-rate workbook that set nothing.

**Layer 2 (the shortcut, and why an expert refuses it).** The textbook PD build from a loan-level record: for each
product and month on book, the share of the loans open and not in default at its start that default in it and the share
that close, then PD(k) as the default rate at a + k times the survival through a + 1 to a + k - 1. Every step of that is
right except who is at risk: the record holds a loan drawn in 2016 only because it was still open in October 2019, so its
months on book before then are months nobody watched it could have defaulted in. Counting it from drawdown puts it among
the loans at risk in months where only survivors appear, which drives every early month's default rate down; an expert
counts each taken-over loan only from its first month on book after the take-over (delayed entry), or reads the rates off
the loans the record watched from drawdown, and either way lands the same figure.

### Default path

1. Stage `personal_loan_book_2026-09-30.csv` under CRM-ECL-04 sections 1 and 2: 3,266 loans in stage 2, 343 in stage 3.
2. Read `loan_record_2026-09-30.parquet`: each loan's month on book of first default (default_month), of closing without
   a default (closed_date), or the month it has reached if still open, counted in calendar months from its drawdown month
   (3.2).
3. For each product and month on book m, take the loans open and not in default at the start of m, every loan counted
   from month on book 1, and the shares of them that first default in m and that close in m.
4. PD(k) for a loan at month on book a: the default share at a + k times the shares neither defaulting nor closing in
   each month a + 1 to a + k - 1; the 2.4 scalar on stage 2 (3.2).
5. Apply LGD, the re-amortised balance and monthly discounting at the contract rate over 12 months or the remaining term
   (3.1, 3.3 to 3.5), and the probability-weighted multiplier 1.0555 from the Q1 FY27 sheet (section 4).
6. Sum: AUD 11,551,554.

Ends on: AUD 11.6 million
Golden: AUD 13.2 million

### Stump sentence

A strong solver builds each product's monthly default and repayment rates by month on book from the loan record,
counting every loan from its drawdown, rolls each performing loan forward from its own month on book, and books AUD 11.6
million against AUD 13.2 million (12.3 per cent low); the step that lands it there is counting the 16,479 loans the
record took over at the October 2019 go-live as at risk from their drawdown, when the record holds them only because
they were still open that day, so their earlier months fill every early month's loans at risk with exposure that could
not end in a recorded default.

### Three rules

Task type: expected-credit-loss-provisioning, the banking domain's task type that serves Forecasting & Predictive Modeling: each performing loan's expected loss over its next 12 months or remaining life at 30 September 2026.
Domain test: The deciding quantity is each loan's AASB 9 12-month or lifetime ECL, whose PD term is the product's default probability by month on book estimated from a loan-level performance record with repayment as a competing exit, then staged, scenario-weighted, re-amortised and discounted at the contract rate.
Swap: Written as a maintenance reserve on pump leases from a lease register, the survival estimate survives, but staging on a significant increase in credit risk, the 2.4 scalar, LGD from recoveries, re-amortised EAD and probability-weighted scenarios have nothing to attach to, so the call stops reading the same.
Layer 1: Dates rather than months on book (loan system), the earlier platform's numbering block (take-over), as-at hardship statuses moved by a Tuesday batch and stale COVID-19 rows (hardship workflow), v3 and v4 scores (scorecard migration), a June extract without the score column and counting arrears to its run, runs stamped the next day (batch scheduler), a blank-key sale receipt and reissued agency references (collections ledger); none carries the call.
Layer 2: Estimation that fits the data (estimation_fit): left truncation; a record that took over the earlier platform's open loans watched them only from the go-live, so each taken-over loan enters the loans at risk at its month on book after 30 September 2019, not at drawdown.
Decisive step: Delayed entry in the PD's life table: each loan taken over at the 1 October 2019 go-live counts among the loans at risk only from its first month on book after September 2019, because the earlier platform's loans that defaulted or closed before then never reached the record.
Not semantics: Every field, the record's population sentence and 3.2's estimand read correctly still leave the textbook build counting each loan from drawdown, AUD 11.6 million; the miss is in which months a loan was observed at risk, an estimation choice, not the meaning of any field or code.
Not rule application: CRM-ECL-04 3.2 files what PD(k) is and that it comes from every loan of the product in the record; no filed sentence says how to estimate it, when a loan enters the loans at risk, or anything about the take-over's effect (asserted), so executing every stated rule still files AUD 11.6 million.
Analyst test: A strong analyst who stages the book cleanly, reads CRM-ECL-04 and the record's dictionary entry correctly and builds the textbook PD from monthly default and repayment rates by month on book over every loan in the record, each counted from its drawdown, books AUD 11.6 million against AUD 13.2 million, 12.3 per cent low.
Estimand: CRM-ECL-04 1.1, 3.1 and 3.2 fix the population (loans open at close of business on 30 September 2026 in stages 1 and 2), the outcome (first default in month on book a + k for a loan open and not in default at the end of a, from every loan of the product in the loan record), the window (12 months or the remaining term), the unit (loan, 3.7) and the AUD allowance.
No decoy: Nothing is planted to carry the wrong answer: no memo, draft, briefing, prior allowance, fitted curve or stakeholder figure ships; the record, the book, the register, the scenarios and the policy are all correct, and the distractors are the roll-rate workbook and the write-off file.
No certified replay: No certified, published or prior-quarter allowance or PD ships, so the method cannot be recovered by reproducing a figure; the estimators that respect what the record watched (delayed entry, the taken-over loans left out, landmark shares) agree with each other, not with a filed number.
Lesson: A loan-level record that took over a predecessor's open loans watched them only from the take-over, so a life table built from it must enter each taken-over loan at its age then; no build on file teaches left truncation of a taken-over cohort (nearest drivers 0.10 and below, task255's size truncation and task134's right censoring differentiated).

### Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 risk grade added to the rates, from drawdown | 7.1 says PD is by product and month on book only | risk_grade is a column | the covariate reflex itself | none | no | no | readable |
| R2 repayment censored (default-only survival), from drawdown | 3.2's "open and not in default ... first defaults" | closure_reason column | the textbook Kaplan-Meier reflex | none | no | no | readable |
| R3 each taken-over loan held from its month on book at the go-live (decisive) | no: 3.2 and the dictionary state the record's population, never entry, exposure or the take-over's effect (asserted) | no: no flag, entry or month-on-book column; the taken-over loans are known only by drawdown before the go-live | no: the reflexes (pool, stratify, censor, compete, smooth) all land wrong (R0 to R2b, the audit's crude routes) | no: no control, corpus or published PD scores the risk set | no: keys unique, no duplicates, every join lands; thin early vintages read as a smaller old book | no: rebuilding every month's loans at risk, not one ratio | silent |

### Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "collective expected credit loss allowance" | stages 1 and 2 | stage 3 included | off (and no PD for stage 3) | 1.1: stage 3 is assessed under CRM-ECL-06, outside this method |
| SF2 | "our PL36 and PL60 loans at 30 September 2026" | the September extract, loans open at close of business | the record's Open loans | same call (the same 40,897 loans, asserted) | same call |
| SF3 | "every loan of its product in the loan record" | every loan, the taken-over ones included, each where the record held it | the taken-over loans left out | same call, 13.2 (AUD 13,226,802) | same call |
| SF4 | "open and not in default at the end of month on book a ... first defaults in month on book a + k" | default with repayment as a competing exit | repayment treated as censoring (default-only survival) | 14.1 | 3.2: a loan repaid before a + k never first defaults at a + k |
| SF5 | months on book | calendar months from the drawdown month | counted from the first repayment month | same call, 13.2 | 3.2 pins the drawdown month; same call |
| SF6 | the significant-increase scalar | on PD(k) | on the monthly default rate | 13.1 | 3.2: "Stage 2 loans carry the significant-increase scalar of 2.4 on PD(k)" |
| SF7 | PD's dimensions | product and month on book | grade added | 13.3 | 7.1: "PD is set by product and month on book only" |
| SF8 | "the record's experience is used as it stands" | rates read off the record, no fit | landmark shares read off the loans followed that far | same call, 13.2 | same call |
| SF9 | a loan past contractual maturity | one month remaining | nothing remaining | same call, 13.2 | 3.2; same call |
| SF10 | pause dates | count as repayments fallen due | left out | same call (AUD 13,192,848) | 3.2; same call |
| SF11 | hardship in force at 30 September | 2.2's dates | the status label; the register ignored | label same call; ignored 12.9 | 2.2; 2.1 names the condition |
| SF12 | v3 origination scores | converted to v4 | read as v4 | 13.1 | 2.3 |
| SF13 | scenario weighting | probability-weighted multiplier 1.0555 | base only; the prior quarter's sheet | 12.5; 13.0 | section 4: the quarter's approved workbook, probability-weighted |
| SF14 | EAD(k) | re-amortised current balance | balance held flat | 15.3 | 3.4 |
| SF15 | DF(k) | monthly at the contract rate | none | 14.4 | 3.5 |
| SF16 | rounding path | loan totals, rounded when reported | stage amounts rounded first | same call (10.6 + 2.6 = 13.2) | 3.7; same call |
| SF17 | the record's default | first month end at 90 or more days past due | the day 90 was reached | not computable from the record | the record's field definition (1.2) |
| SF18 | the record's window | events to 30 September 2026 | events to an earlier cut | not offered by the files | the record's population note |
| SF19 | "the loans that defaulted in 2023-24" | the Collections MI file, July 2023 to June 2024 | calendar 2023 and 2024 | not offered by the files | the file's own population and name |
| SF20 | "by product and quarter" | quarter of the default month within 2023-24 | quarter of resolution | off on all 8 | the MI file's default month; the prompt ties the ask to the defaults |
| SF21 | "actually lost as a share of their balance at default" | 3.3's measure: receipts and the sale share, monthly discounting to the default month end | undiscounted; by days; from the month start; at the annual rate | off on 6 to 8 | 3.3 and 3.5 |
| SF22 | a case Collections closed as cured that the loan record shows written off or settled | measured on what it recovered: the 59 cured on arrangements withdrawn before they started, every one written off | every cure at its word (the judge's round 2 build); every withdrawn cure doubted | off on all 8; off on 7 of 8 | 3.3: "a loan the loan record shows written off or settled for less did not return to performing, whatever resolution Collections recorded, and is measured on what it recovered"; the record and the register select the same 59 (C1) and every other cure is repaid in full or open (asserted) |
| SF23 | "every amount received" on a loan | each remittance on the account placed under the reference it quotes that day | the receipts file's posted loan (the judge's round 2 build); the reference's latest placement; reissued references dropped | off on all 8 each | the dictionary: the loan number is the one "the receipt was posted to; an agency remittance is posted on the Wirraway reference its narrative quotes", and the Agency Ref is "Wirraway's reference for the account while it is placed"; each of the 20,902 remittances falls inside exactly one placement of its reference, none on a first or last day, and each of the 2,034 posted elsewhere arrives outside the posted account's own placement (asserted) |
| SF24 | the sale proceeds | each sold account's face value at the cut-off times 3.85 cents | the receipt spread over the written-off cases | off on all 8 | 3.3 counts the proceeds of the debt's sale; the schedule prices each account |
| SF25 | stage at 30 June | section 2 with days past due at close of business on 30 June | the June extract's days past due as they stand (the judge's round 2 build) | 14 of 16 counts move | 1.3 and the dictionary's loan book lines: the June extract's days_past_due "counted to the run date, 1 July 2026", the September extract's "counted to the reporting date, 30 September 2026"; executed literally (each June value put back by the day between) all 16 counts are the golden, read unadjusted 14 move (both asserted, the clock parsed from the dictionary by the verifier); the record dates the default of the 6 loans at 90 days to July and the 15 at 180 had not been written off by 1.4's June batch |
| SF26 | the June behaviour score | the month-end run on the 30 June position, made 1 July | the run made before 30 June | 16 of 16 move | 2.1 at the reporting date; the runs file names the month ends it scores and dates each run by the day it was made |
| SF27 | "the number closed" | June loans absent from the September extract | the record's Closed status in the quarter | same call (3,317, asserted) | the dictionary: a loan leaves the extract once it closes |
| SF28 | hardship in force at 30 June | 2.2's dates | the September status label | 16 of 16 move | 2.2 |
| SF29 | "as a share of their balance at default" by product and quarter | the quarter's balance not recovered, summed over its defaults, over their total balance at default | the mean of each loan's own share | off on all 8 (nearest 0.58 points) | 3.3: "summed over the quarter's defaults, as a share of their total balance at default" |
| SF30 | the LGD the allowance uses | 70 and 76 per cent | the 2023-24 losses the review is setting them against (PL36 68.9, PL60 75.1 per cent) | 13.0 | 3.3: "the rates in force until the Audit and Risk Committee approves a change"; the prompt's "will be set" |
| SF31 | a cancelled arrangement, and the end date, at 30 June | in force to its end date, both days included, until the day it is cancelled (57 cancelled after 30 June were in force) | every cancelled arrangement out whenever cancelled; the cancellation ignored; the end date excluded | 14, 8 and 6 of 16 move | 2.2: "one that is cancelled stops being in force on the day it is cancelled"; the dictionary: the end date is "the last day of the varied repayments"; no cancellation falls on 30 June (C1) |
| SF32 | "60 or more points below" on the June scores | 60 or more on whole points: every score whole, every v3 score converted and rounded to the nearest point, none within 0.02 of a half (82 June loans fall exactly 60) | more than 60 | 12 of 16 move | 2.1's "60 or more"; the migration note: "rounded to the nearest whole point" |
| SF33 | stage 3 and written-off loans at 30 September | stage 3: in the September extract at 90 or more days past due; written off: closed | written off counted as stage 3 (6 loans of the four groups) | 4 of 16 move | the dictionary: "a closed loan is in no stage"; 1.4: a loan written off is closed |
| SF34 | the June behaviour score (slide 2) | the June month end's Scored row: the run dated 1 July, or the 2 July rerun for the partition carried forward on 1 July | the run dated 1 July as it stands (carried-forward scores in), or its Scored rows only | 16 of 16 counts move either way | the scoring file's own fields: score_status says a Carried forward score repeats the last score held, and runs and run_date make the 2 July rows the June month end's; each loan's latest June month-end row gives the golden (C1); asserted |
| SF35 | when a defaulted loan leaves the loans at risk | at its first default | the 1,223 defaulted loans not written off or settled kept at risk from the default month (an instant cure; the round 2c judge's residual fork) | AUD 13.1 million (10.5, 2.6) | 3.2: the probability that a loan open and not in default at a "first defaults in month on book a + k"; the record carries no cure date and 343 of the 761 still open are 90 or more days past due at 30 September, so the data do not support an instant cure; asserted |

### Ladder

Measured by `checks.py` and `verify.py` on the shipped pack (allowance, AUD; reported to AUD 0.1 million):

| Rung | Construction | Allowance | Reported | vs answer |
|---|---|---|---|---|
| R0 (default path) | life table by product and month on book, every loan from its drawdown, repayment competing | 11,551,554 | 11.6 | -12.35% |
| R1 | the covariate reflex: rates by product, grade and month on book, from drawdown | 11,653,209 | 11.7 | -11.58% |
| R2 | the textbook survival curve: repayment censored, from drawdown | 12,243,098 | 12.2 | -7.10% |
| R3 (decisive) | each taken-over loan held from its month on book at the go-live | 13,178,713 | 13.2 | answer |
| R2b | repayment censored, held from the take-over (over-correction) | 14,073,342 | 14.1 | +6.79% |

- Every correction walks up and only the over-correction overshoots; the decisive move is the largest (+14.1 per cent
  over the default path). R0 misses the allowance and both stage amounts; R1 and R2 miss the allowance and stage 1 and
  land stage 2's bin (2.64 and 2.57 against 2.59) by offsetting errors, priced in the pair simulation.
- The audit's routes on the record (a crude cumulative default share and its conditional readings) all land off:
  resolved loans over 1 - C(a) 14.8, over the share still open 17.1, plain increments 14.3; every loan over 1 - C(a)
  8.6, over the share still open 9.2; read from month on book 0 24.8; repayment counted again on EAD, on top of the
  competing exit, 12.4 (-5.92 per cent).
- C4 cells, each off the bin and ruled out by a quoted sentence: grade held from the take-over 13.3 (7.1), the scalar on
  the default rate 13.1 (3.2), v3 read as v4 13.1 (2.3), hardship ignored 12.9 (2.1, 2.2), base scenario only 12.5
  (section 4), EAD flat 15.3 (3.4), no discounting 14.4 (3.5).
- C3 corridor: the answer and every convergent estimator sit inside AUD 13.15 to 13.25 million (13,174,979 to
  13,226,802: taken-over loans left out, landmark shares, the first-repayment clock, past-maturity nil, the status label).
  The answer sits 0.29 of a bin from its lower edge, stage 1 0.34, stage 2 0.45 (asserted at 0.2 or more).
- R3a and R3b (three-rules block): the easy route with every filed rule executed files AUD 11.6 million on the answer's
  stages and multiplier; changing only the entry of the taken-over loans files the answer to the cent.

### Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | allowance: loans open at close of business 30 September 2026 in stages 1 and 2; PD: every loan of the product in the record | 1.1, 3.2 filed; C1: taken-over loans in or out land the same bin (SF3) |
| 2 Unit of account | the loan | 3.7: ECL per loan, the allowance their total |
| 3 Attribution window | forward months k from October 2026 | 3.1, 3.2; the record's events dated at month ends and closing dates |
| 4 As-of dating | close of business 30 September 2026 | 1.3 and the extract and record headers |
| 5 Version basis | CRM-ECL-04 v4.2, the Q1 FY27 scenario sheet | the document control; the sheet name; the prior quarter's sheet lands 13.0 (SF13) |
| 6 Denominator | PD: loans open and not in default at the start of each month on book, each where the record held it | 3.2 files the estimand; the method is forced by the record's structure and every valid estimator converges (C3); the stump lives here as HOW |
| 7 Weighting | 55 / 30 / 15 per cent on the scenario multipliers | section 4 and the approved sheet |
| 8 Window length | the record's whole history | 3.2 "every loan of its product in the record"; C1 across own-only and landmark |
| 9 Boundary inclusivity | 30, 90 and 60-point thresholds inclusive; arrangement dates inclusive | 2.1, 1.2, 2.2; C1: no arrangement ends or is cancelled on 30 September (asserted) |
| 10 Rounding path | loan level, rounded when reported, AUD million one decimal | 3.7 and the prompt; stage amounts add (asserted) |
| 11 Tie-break | none (one figure) | not applicable, asserted single answer |
| 12 Maturity and censoring | open loans followed to September 2026; taken-over loans entered at the go-live; past-maturity loans one month | 3.2; the record's population; C3 |
| 13 Order of operations | scalar on PD(k), then the multiplier (both multiply PD) | 3.2, section 4; the scalar on the rate is SF6 (13.1) |
| 14 Row order | sums | C1, order-free |
| 15 Duplicate resolution | one row per loan in every extract | asserted unique keys |
| 16 Identity normalisation | loan numbers join book, record and register | asserted; the earlier platform's lower block joins as it stands |
| 17 Netting against gross | per-loan ECL, no netting | 3.7 |
| 18 Dimensional units | AUD; annual rates divided by 12 | 3.4, 3.5 |
| 19 Code and status semantics | hardship status against dates; v3 against v4; closure reasons | 2.2, 2.3, the record's field definitions; never the stump |
| 20 Integerisation | repayments fallen due counted on the business-day schedule | 3.2 and the dictionary's repayment day rule |
| 21 Clause scope | 7.1 applies to PD; 3.2's estimand per product | 7.1, 3.2 |
| 22 Forward window contents | PD from the record's experience, multipliers on PD, EAD on schedule | 3.2, section 4, 7.4 |

### Literal reader

A reader executing CRM-ECL-04 3.2 word for word estimates, per product and month on book, the probability that a loan
open and not in default at the end of a first defaults at a + k, from every loan of the product in the loan record; the
record files its own population as every loan the loan system has held since it went live on 1 October 2019, when it took
over the earlier platform's book, so the earlier platform's loans in it are there because they were open at the go-live,
and a literal estimate cannot treat their months before the go-live as months watched; every literal method that keeps to
what the record holds (delayed entry, the taken-over loans left out, landmark shares) files AUD 13.2 million (C3,
asserted), and the default path is an easy method on the same estimand, never another reading of it. The ask readings
are closed in SF19 to SF33, each by a quoted sentence the lender files (3.3's measure, its cure and its rates in force;
2.1 to 2.3; the dictionary's field descriptions, its change log and its closed loans) or by records that converge. The
judge's round 2 builds are reproduced to the figure in `checks.py` (60.5 to 74.7; 14,450 to 113) and part from the
golden only at the cure, the remittance attribution and the June clock, each now ruled on by one filed sentence; the
literal execution of the repaired text gives all eight loss shares and all sixteen counts on the verifier's own code.

### Oracles

- The write-offs extract (distractor): monthly write-offs and recoveries, totals invariant under either attribution of
  agency remittances (D9, asserted); it states no PD, loss rate or allowance.
- The roll-rate workbook (distractor): FY26 arrears roll rates by count; no PD by month on book, no allowance.
- The scenario workbook's prior-quarter sheet: last quarter's multipliers (1.04 weighted), off the bin (13.0) and ruled
  out by section 4's "the quarter's approved scenario workbook".
- The sale schedule's header: face value times 3.85 cents equals the consideration and the blank-key receipt to the
  cent under every reading of ask A.
- The receipts total: the same under either attribution.
- None ties only under the golden; no document states a graded figure (asserted).

### Ask sheet

Both asks are decoupled from the call: neither reads the PD (asserted by running both with the PD code disabled), and
the main call reads none of the June extract, the scoring runs, the Collections files, the sale schedule or the
placement report (deleting them leaves the allowance identical, asserted). Zero device and hazard rows sit in the main
call's population: none of the 72 withdrawn collections arrangements and none of the 1,334 bulk COVID-19 rows is in force
at 30 September or 30 June or sits on a loan in either book; the 1,827 June loans whose arrears the extract counts to its
run sit in a file the call never reads; the reissued references sit in the receipts ledger and the placement report,
which the call never reads.

**Ask A, realised loss of the 2023-24 defaults by product and quarter (8 figures, per cent to one decimal, workbook)**

- Answer: PL36 67.9, 65.8, 70.7, 70.9; PL60 70.2, 77.4, 73.2, 79.3 (July to September 2023 through April to June 2024).
- Named use and H18 home: the LGDs in 3.3 (70 and 76 per cent) are reviewed against what the defaults have lost; the
  audit trail of the LGD input the call consumes.
- Primary device A2, silent (D7, codes reissued to other entities): Wirraway reissues the reference of a placement it
  closed at least 90 days earlier to some new placements from its November 2024 platform move, the most recently freed
  first, and Bellbird's receipts loader posts a remittance to the first placement on file with the reference it quotes:
  639 references carried twice or more, 2,034 remittances posted to another account, 719 of them on accounts sold to
  Tarwin in March 2026, after the sale. The posted read credits 2023-24 loans with later accounts' remittances. The
  dictionary says what the two fields hold, the way the ledger and the agency document them: the receipts file's loan
  number is the one the receipt was posted to, an agency remittance posted on the reference it quotes; the Agency Ref is
  Wirraway's reference for the account while it is placed. Nothing says a reference is reissued or how the posting picks
  a placement; the reuse shows only in the placement report's rows.
- Hazard A1, filed (round 2 repair; D2, a stored label taken before a silent switch): Collections closes a default case
  as cured when it approves a collections arrangement, dated from its start, and does not reopen it when the arrangement
  is withdrawn: 72 withdrawn, 59 on loans the record shows written off (some sold in March 2026), 13 that caught up. 3.3
  now files that a loan the record shows written off or settled is measured on what it recovered, whatever Collections
  recorded, so every careful path executes it; taking every label at its word, as the judge's round 2 build did, zeroes
  the 59 and misses all eight.
- Why A2 survives the battery: keys unique, no duplicate rows, every receipt joins the record and the defaults, the
  receipts and write-off totals tie under every attribution. The inconsistency exists only across files, at a cut nothing
  in the battery makes: a remittance whose posted account's placement had closed, or been recalled for the sale, while
  the placement report shows its reference on another account that day.
- Resolution, unique: 3.3's cure sentence on the record (the 59, the same set the register gives, C1); each remittance to
  the account placed under its reference on the day it was received (exactly one per remittance, none on a first or last
  day, asserted).
- Hazards crossed: A1 (filed), the sale receipt with no loan number (shared by face value), the dishonour reversals
  (texture), the discount clock (3.3, 3.5), the pooled share (3.3, SF29).
- File path (7 files on the golden's path, the register an eighth that reaches the same cure set):
  collections_defaults_2023-24.csv, collections_receipts_2023-07_2026-09.csv, debt_sale_2026-03_schedule.xlsx,
  wirraway_placements_2026-09-30.csv, loan_record_2026-09-30.parquet (closure reasons), CRM-ECL-04 (3.3, 3.5),
  ecl_extract_dictionary.txt (loan_no, Agency Ref); hardship_register_2026-09-30.xlsx (the withdrawn arrangements, C1).
- Columns (17 on the golden's path): loan_no, product, contract_rate, default_month, balance_at_default, resolution;
  received_date, amount_aud, source, narrative; face_value_aud and the Price line; Agency Ref, Client Ref, Placed, Closed;
  closure_reason.
- Stops (nearest figure to the answer, every figure off at one decimal, asserted): the judge's round 2 build (cures at
  their word, remittances as posted) 2.50; A1 executed, as posted 0.55 (the cracker's and the mirror's path); A2
  cracked, cures at their word 1.96; over-cleaner (every withdrawn cure doubted), as posted 0.36; the reference's
  latest placement 0.87; reissued references dropped 0.87; latest placement with cures at their word 0.61; the sale
  left out 1.10; the sale spread 4.39; not discounted 2.77; every cure on its receipts 8.00; the mean of loan shares
  0.58. Composed (cure rule by sale by discounting by attribution, 319 paths): at most 1 of 8
  with one, two or three mishandlings: the over-cleaner that also cracks A2 hits PL60 April to June (no caught-up case
  there was withdrawn), with the annual rate as well PL60 July to September, and the sale left out with no discounting
  and the latest placement PL60 January to March.
- Realism: an approved arrangement closing a case is how collections MI records a cure; agencies reissue account
  references and a lookup on the first match is an ordinary loader's behaviour; the placement report is the agency's
  standard client export; a run folder's dictionary says what each field holds and where a ledger's postings come from.

**Ask B, where the loans in stage 1 and stage 2 at 30 June stand at 30 September (16 counts, deck slide 2)**

- Answer (stage 1, stage 2, stage 3, closed at 30 September): PL36 stage 1 at June 14,470, 680, 42, 1,586; PL36 stage 2
  468, 658, 115, 123; PL60 stage 1 17,724, 831, 46, 1,180; PL60 stage 2 560, 942, 140, 112.
- Named use and H18 home: the Audit and Risk Committee sees the quarter's deterioration and cures behind the stage 2 amount it signs; the
  audit trail of the staging the call consumes.
- Primary device B4 (round 2c, a scoring-run partition carried forward): Behaviour Scoring's run for the June month end,
  made 1 July, could not score one partition of the engine's book (loan numbers whose last digit before the check digit
  is 3 or 4) and wrote each of those loans its last score, marked Carried forward: the May month-end score, or the
  application score on v4 for a loan first due in June. The partition was run again on 2 July, so the file holds a
  Scored row for every loan of the June month end and, for the partition, a carried-forward row dated 1 July beside it.
  The careful path takes the run dated 1 July for the June month end (B2's own logic), every join lands and every
  score is a plausible number: read as it stands, 16 of the 16 counts move; its Scored rows alone (the partition left
  unscored, as the loans before their first repayment are), 16 of 16. Resolved from the scoring file alone: its
  `score_status` description says what a Carried forward score is, and its `runs` and `run_date` say the file holds
  month-end runs dated by the day they were made, so the 2 July rows can only be the June month end's. Each loan's
  latest June month-end row gives the golden too (C1). No filed rule on the path: neither the dictionary nor the
  policy mentions the rerun (asserted).
- B3, filed since round 2b (D8 spent): the dictionary records the June extract's days_past_due as counted to its run
  date, 1 July, and the September extract's as counted to the reporting date; staging at 30 June under 1.3 puts each
  June value in arrears back a day. Read unadjusted, 14 of the 16 counts move; now a hazard the careful path crosses.
- In-world evidence, consistent with the filed source: 0 of the 1,827 June values sit on a due date counted back from
  30 June and every one from 1 July; the 15 loans at 180 days were at 179 when the June batch ran (1.4); the loan record
  dates the default of each of the 6 loans the extract shows at 90 days to the July month end (at close of business on
  30 June they were at 89, in stage 2, inside the four groups), and of every loan above 90 to June or before.
- Hazards crossed: B1 the status label and the cancellations (2.2, restated: a cancelled arrangement stops on the day it
  is cancelled), B2 the run dated 1 July for the June month end, 2.2's end date, the 60-point fall on whole points
  (SF32), written-off loans closed rather than in stage 3 (SF33), the September status lag (2 counts).
- File path (8 files): personal_loan_book_2026-06-30.csv, personal_loan_book_2026-09-30.csv,
  behaviour_score_runs_2026-03_2026-08.parquet, hardship_register_2026-09-30.xlsx, scorecard_v4_migration_note.pdf,
  loan_record_2026-09-30.parquet (default months), CRM-ECL-04 (1.3, 1.4, 2.1 to 2.3), ecl_extract_dictionary.txt.
- Columns (15): loan_no, product, days_past_due, first_repayment_date, origination_score, origination_scorecard at both
  dates; run_date, score_v4, score_status; arrangement_start, arrangement_end, cancelled_date, arrangement_status; current_score_v4;
  default_month.
- Stops (counts moved of 16, every pair distinct, asserted): the judge's round 2 build (as extracted, the 1 July run,
  2.2's dates) 14; labels and the May run 16; dates without any cancelled and the May run 16; dates and the May run 16;
  dates without any cancelled and the June run 11; cancellation ignored 14; September scores for June 16; the July run
  16; the end date excluded 14. Every composed path moves at least 6. With the June clock read from the change log:
  every cancelled arrangement out 14, the cancellation ignored 8, the end date excluded 6, more than 60 points 12,
  written off as stage 3 4. Round 2c, the clock executed: the run dated 1 July as it stands 16, its Scored rows only 16,
  as it stands with the June column unadjusted 16; every composed path, the B4 readings included, moves at least 6.

**Necessity matrix** (one device mishandled, everything else right): A2 8 of 8, A1 (filed) 8 of 8, the sale left out 8,
not discounted 8, every cure on its receipts 8, the sale spread 8, the mean of loan shares 8; B4 the run dated 1 July as it stands 16 of 16, its Scored rows only 16; B3 (filed since round 2b) 14 of 16, B1 the label
16, B1 every cancelled out 14, B2 the May run 16, more than 60 points 12, the end date excluded 6, written off as stage
3 4.

**Hazard table.** Sale receipt (A, 8 figures, 1.1 to 1.6 points); discounting (A, 8, 2.8 to 5.5); dishonours (A, none:
texture); B1 label (B, 16); B2 run date (B, 16); the September status lag (B, 2 counts).

**Referee.** The sale schedule's consideration, AUD 1,800,666.58: face value times 3.85 cents and the blank receipt to the
cent, under every handling of A1 and A2.

| Ask | The cracker's path (lands the call, runs the battery, executes every filed rule it points at) | Figures kept | Verdict |
|---|---|---|---|
| A, 8 realised losses | 3.3 as filed (pooled, the cure sentence on the record, the sale by face value, monthly discounting); remittances as the receipts file posts them, every join landing | 0 of 8 (nearest 0.55 points) | miss |
| B, 16 migration counts | the run dated 1 July for the June month end as it stands (B4), 2.2's dates, 60 or more on whole points, closed loans in no stage; June days past due put back to 30 June by the dictionary's run clock | 0 of 16 | miss |

Mirror leakage: 0.0 per cent of the ask weight (the mirror takes the same ask paths and keeps none of the 24).

Pair ceiling: 28.5 (planning weights 38 / 7 / 55, r = 5; cracker 45.0, 0 of 24, mirror 12.0, 0 of 24; asserted in
`checks.py`). With the mirror on R1 or R2 also keeping stage 2's component, 31.0; both top responses on the call, each
executing the June clock, 45.0. The most obvious device is A2 (the dictionary's loan_no entry names the posting rule),
and the cracker cracking it puts the pair at 37.7 (asserted at or under 40). Residuals: the cracker cracking B4 instead
46.8, both A2 and B4 56.0; both top responses cracking A2 63.3, B4 81.7. B4 is the quieter of the two: every join of the
battery lands on the run dated 1 July and its scores are ordinary numbers, and only the file's own status column and its
seventh run date show the partition. The habitual sheet 28.5.

**Span floor.** Ask B 8 files; ask A 7 on the golden's path since the cure is read off the record (3.3), the register an
eighth route to the same 59.

**Guard lines.** Round 2c clears the two BLOCKs heart read at round 2b: ban.forum board_of_directors against task119
(forum redrawn to committee_or_panel, which guard.py check passes now that task129 is outside the three builds drawn
before this one) and people.first Vanessa against task108 (Declan Wallace drawn with guard.py names, seed 133). Heart is
WARN, no BLOCK. Earlier (heart WARN, no BLOCK): people.last Olson (task181) and people.first Vanessa (task108), Christine
(task104): older builds only, names drawn by guard.py. repeat.gate_g forecasting against task132: both in the
Forecasting block, mechanisms differ (renewal against left truncation). repeat.deliverables pptx and xlsx against
task129: the deliverables are the slot's since v1. Driver nearest 0.10 (this slot's loop 1), 0.06 task501 v3 and task23;
same_driver_older against task180 differentiated on the card.

### Leak review and stage 3 gates

- Round 2c (2026-10-14): `checks.py` PASS 600 (SF34 and B4's readings, the pair sheet asserted), `verify.py` PASS,
  two rebuilds byte-identical to `target/`, `target.zip` and `golden/`, `figures_check.py` exit 0 (65 figures), `precut.py`
  49 PASS, voice-check PASS (874 characters), `leak.py --asof 2026-10-12` REVIEW no LEAK, guard validate 169 valid,
  surface 1 promoted (task180, unchanged), heart WARN no BLOCK, freeze check --mode rubric PASS (--mode determinism names only the deck's renamed
  heading, board_ecl to arc_ecl, every figure unchanged).
  Documents changed under `target/`: the scoring runs parquet, the CRM-ECL-04 docx and the hardship register (metadata).

- Round 2b (2026-10-14, after the re-judge's fix): `checks.py` PASS 581, `verify.py` PASS (the June clock parsed from
  the dictionary), two rebuilds byte-identical to `target/`, `target.zip` and `golden/`, `figures_check.py` exit 0,
  `precut.py` 49 PASS, voice-check PASS, `leak.py --asof 2026-10-12` REVIEW no LEAK (the same lines as below), freeze
  check --mode determinism PASS, guard validate 169 valid, surface as below, heart BLOCK pre-existing (Guard lines).
  Documents changed under `target/`: `ecl_extract_dictionary.txt` and the CRM-ECL-04 docx.

- `leak.py task133 --asof 2026-10-12` (rerun after the round 2 asks repair): REVIEW, no LEAK. Each line:
  - 7.1 in CRM-ECL-04: the limitations clause number, which the write-up cites, not a figure.
  - 560 and 680 in the migration note: v3 scores in its conversion table, not the counts they coincide with.
  - CRM-ECL-04 carries 9 of 10 words of the call: its scope sentence (1.1) names the allowance it governs, with no figure.
  - stump-term overlap, CRM-ECL-04 6 of 25 (record, repayment, status, months, points, arrangement) and the dictionary 10
    of 25 (record, drawdown, repayment, status, months, earlier, agency, among them): the subject's own words. The
    repair's new dictionary lines say what two fields hold and where the extract is read from; none names the reissue,
    the posting rule or a recount (asserted in `residue_and_pins`). The dictionary's
    "earlier platform" and "took over" are the loan record's population sentence, the filed WHAT the literal reader
    needs; neither document says anything about entry, exposure, truncation, the loans at risk or how to count a
    taken-over loan (asserted in `forks`).
  - dates after the setting: arrangement end dates and approved starts in the register; first repayment dates of loans
    drawn in September in the book and the record.
- `guard.py surface task133`: 1 pair promoted, task180 (surface 0.078, corpus percentile 52), on the card-level
  same-driver signature (gap population, pattern G12, Gate G forecasting), not on wording, file names, schema or
  personas; differentiated on the card (task180 restores events a detector masked, so its record misses events that
  happened; here every default after the take-over is recorded and what the record lacks is the taken-over loans'
  earlier months). Left for the author's `/clone-check`. The only persona the cut pack names is Stephanie Manning.
- `guard.py validate`: 169 cards valid. `guard.py heart task133`: WARN, no BLOCK (lines in the Ask sheet's tail).
- `golden-realism`: the round 2 repair rewrote two notes on the workbook's Method sheet to the filed wording (the June
  clock, closed loans in no stage, the pooled share, the cure and the attribution); no figure moved, the container
  audit is clean. Named sheets, findings as titles, precision by quantity (AUD million, whole loans, the
  multiplier to two decimals, balances to the cent, losses to one decimal), source lines from the fiction, the rounding
  convention and the method on a notes sheet; the deck's titles are findings with a source strip and slide numbers.
- `reduce-house-fixes`: H1 container audit clean on `target/` and `golden/`; H4 the zip holds the 15 files flat; H6 the
  golden's attribution rule holds for every remittance (one placement each) and its cure rule for every case (asserted);
  H7 two rebuilds byte-identical to the shipped `target/`, `target.zip` and `golden/`; H8 every clause cited resolves;
  H9 every shipped file named in the run folder's dictionary and in `metadata.json` (asserted); H11 one write-up and one
  prompt; H16 no record dated after its extract; H24 the constructed-pack statement sits only in `metadata.json`.

## Tried and rejected

- Healthcare same-day access with demand censored at sell-out time (the slot's first draw): too mild a censoring to separate the rungs and two rigorous uncensoring methods disagreed by one session in several cells.
- Building the PD curve from the outcome history inside the task: the naive denominator (every loan originated) and the unconditional reading cancel to within 2.3 per cent of the answer, so the curve is filed as model output instead.
- Months-on-book bands as the breakdown ask: it names the decisive dimension in the prompt; drawdown year carries the same information the way a credit committee reads it.
- No stage 2 scalar: stage 2 coverage came out barely above stage 1 (7.6 against 6.3 per cent), which no credit reviewer would accept; CRM-ECL-04 now files a 2.4 scalar.
- Realistic default levels (lifetime default 10 per cent PL36, 14 per cent PL60, no 90-day default before the fourth repayment) put the half-step rung (curve shifted, no survival division) at 3.3 per cent low against its 6 per cent floor; reaching 6 per cent needs PL60 lifetime default near 20 per cent, a loss-making lender, so the floor is 2.5 per cent and the rung stays a distinct wrong answer at the nearest thousand.
- Post-default resolution near one default in five with recoveries near 26 per cent of the written-off balance: the implied gross LGD fell to about 60 per cent, ten points under the filed 70 and 76, so resolution is set near one in six and recoveries near a quarter (about 24 per cent at three years: PL36 30, PL60 20).
- Tuning the rounding margins on the one-month reading of past-maturity loans alone: the allowance and the PL60 2023-and-earlier figure straddled their edges between that reading and the zero one (the loans carry about AUD 220), so the tuner now centres both readings at once.
- Pinning the past-maturity PD by curve position ("the curve's final month") in CRM-ECL-04: rejected, the sentence would tell a solver that a loan reads the curve from its own month on book, which is the decisive step; 3.2 pins only the one-month remaining term and the corridor assertion covers the PD reading.
- Stale arrangement_status labels from a weekly status refresh: not built. The labels sit on the main call's staging path, so a solver staging on status instead of dates would move a handful of loans and the allowance bin; the statuses stay current to the reporting date and CRM-ECL-04 2.2's date rule decides.
- Weekly status batch on Sunday or Monday night (round 3, B4): 12 or 6 arrangements end after the run, 9 or 5 book loans otherwise in stage 1, and staging on the label alone moves the allowance to AUD 13,778,000 or 13,775,000 (set STATUS_RUN_WEEKDAY to 6 or 0 to reproduce). The Tuesday run leaves two and moves one loan, and the allowance keeps its bin, so the main call stays mess-neutral.
- Blank state or channel for loans migrated at the October 2019 go-live (round 3, B4): no such loan is on the book, where the earliest drawdown is May 2021, so the blank states are overseas addresses.
- Stale arrangement_status labels, revisited in repair 3: built after all with a Tuesday-night status batch (two arrangements that ended 29 September still show Active), because a Sunday or Monday batch moved a status-only staging's allowance out of its bin (AUD 13,778,000 or 13,775,000) while the Tuesday batch moves one PL36 loan and keeps the bin (asserted); the line above records the earlier refusal.
- v1's conditioning on survival to date was landed on the portal: one model filed AUD 13,773,000 by dividing the curve's increments by 1 - C(a) and scored 100 per cent, the other was stumped; loop 1 files the curve as the crude default share of every loan drawn, so that division is now rung R4 (10.8 per cent low).
- The inheriting asks (stage by product, drawdown year, the stage 3 count) were banked by the response that landed the call, because each was an output of the same construction; loop 1 retires them for two asks that read neither the curve nor the sample.
- A debt-sale price of 10.35 cents: leaving out the discounting and leaving out the sale move each figure by similar amounts in opposite directions anywhere from about 7 to 22 cents, so stop s2 landed 0.11 points from a figure; at 5 cents or below the two effects stay at least 0.8 points apart, and a few cents is what aged written-off unsecured debt sells for, so the price is 3.85 cents.
- Agency remittances capped at a fixed monthly amount: 62 per cent of the remittances sat exactly on the cap, a pattern no collections ledger shows; replaced by a log-normal affordability draw per arrangement, its median raised to AUD 320 when the first draw left recoveries under the level the 70 and 76 per cent LGDs imply.
- Dating each default on the day it reached 90 days past due: 39 of the 2023-24 defaults resolved inside that same month, so the population turned on a day-or-month reading; 1.2 now records the default at the first month end at 90 or more days past due, and the defaults file carries only those (no default resolves in its default month, and no receipt falls in it).
- Hardship windows that reached the instalments of a default run (18 loans, 4 of them 2023-24 defaults) cleared those instalments in the simulation; the windows now stop before the run's first missed instalment.
- The release-package filing note in the development sample's own metadata (pre-round repair): not built. It was written at extraction on 2 June 2026, before the 24 June approval and months before the September run, so a note about this run cannot sit there without moving the file's date; the note is in the run folder's list of other files, which Credit Risk Reporting keeps for the run.
- A calendar-first prompt with the workbook commissioned before the chair's slides (loop 1): the same build order as task130, task132, task134 and task135, read by the clone check as one skeleton across the lane (Idiom); it now opens on the slides and puts the workbook behind them.
- The blank-key sale receipt as ask A's primary device (loop 1 round): the careful solver found the blank loan number with the hygiene battery and shared the receipt out at the schedule's price, as 3.3 told it to; it stays as a hazard under the silent cure-label device.
- The status label and the run date as ask B's primaries (loop 1 round): the solver took hardship in force by 2.2's dates and the 1 July run from the file's own run_date note; both stay as hazards under the silent arrears clock.
- Smoothing PLPD-2026.06 freely (6b): a three- or five-month moving average, a log-linear tail, block-preserving fits and an unconstrained log spline moved the allowance by 12k to 235k and split the divisor's default share between the curve and the sample by 0.5k to 6.4k, several bins either way; the released spline is fitted under the six constraints that keep both readings, and the unsmoothed rebuild, in every bin.
- Smoothing only the last month's step (6b): left the noise the reader flagged and moved the allowance by 20k on its own.
- A cure that re-defaults as ask A's device (6b): the cure clause either blesses the wrong answer (a loan that returned to performing and later defaulted again "lost nothing") or announces the check ("and does not default again"); a cure recorded on an arrangement withdrawn before it started has no such fork, because the loan never returned to performing.
- Paused loans left out of the June extract as a second silent device for ask B (6b): 7 of the 181 pauses in force at 30 June sit on loans closed by 30 September, whose product nothing else in the pack gives, so the June population could not be rebuilt; not built.
- Agency remittances carried gross of Wirraway's commission as a span-adding ask A device (6b): needs a filed "net of commission" rule the careful solver would execute and a commission source; not built.
- The caught-up half of the cure-label device sized at 0.3 points (6b): doubting every cure on a withdrawn arrangement and leaving the sale share undiscounted then cancelled to the answer in one cell; the caught-up cases are drawn to 0.8 points.
- The 8-file span floor for both asks (6b): not met (6 and 7 files). The asks may not read the curve or the sample, and every other file left (the scenarios, the two distractors) could enter only through a dependency written for the purpose.
- Round 1 shipped design: weak per the 10/10 audit, because its decisive step (dividing a crude cohort curve's increments by the share of the cohort neither defaulted nor repaid, read from the development sample) sat one rung above the step the v1 portal winner had already solved, and the sample's prepaid outcome column beside a curve header saying "share of every loan drawn" pointed straight at it; round 2 ships no curve and no sample and moves the decisive step to where a taken-over loan's exposure starts.
- The audit's suggestion, a crude curve rebuilt by Aalen-Johansen from right-censored recent vintages: an estimator under censoring with competing exits is task134 v1's driver, whose default construction landed; censoring and the competing repayment exit are this build's default path instead, and the decisive move is left truncation.
- EAD at default (re-amortised against the balance at default) as the decisive step: 3.4 files EAD, so the step would be rule application.
- A cure followed by a re-default as the PD's decisive step: the cure clause either blesses the wrong answer or announces the check (already rejected for ask A at 6b).
- Hazard against landmark estimation as the stump: both are valid on the record and land the same bin, so the choice between them is no stump; both sit in the corridor.
- LGD development (recoveries not yet complete) as the main call's step: 3.3 files the LGDs, so the call estimates none.
- Scenario weighting as the step (the weighted multiplier against weighting scenario ECLs): linear in PD, identical; no stump.
- The allowance at the nearest AUD thousand: the estimators that respect what the record watched (taken-over loans left out, landmark shares, the first-repayment clock) sit 0.1 to 0.4 per cent apart and split the thousand-dollar bins; reported in AUD million to one decimal they all file 13.2 (C3).
- Stage amounts at two decimals of a million: leaving the taken-over loans out moves stage 2 from 2.59 to 2.62; one decimal keeps the corridor, and R1 and R2 then land stage 2's bin by offsetting errors (accepted and priced: the call and stage 1 miss on both).
- The earlier platform's loans numbered as a separate go-live block: a marker column in all but name; they keep their own BPL numbers, below the loan system's range.
- The first-repayment clock at -2.9 per cent: an artefact of reading rates on one clock and positions on the other; on one clock throughout it lands the answer's bin (13.2), so SF5 converges.
- Withdrawn-arrangement cures drawn at one rate for every 2023-24 case (6 or 12 per cent): the over-cleaner hit 6 or 7 cells; drawn by how each case ended (55 per cent of the caught-up, 9 per cent of the written off and settled) it misses every cell unless it also cracks A2, then 1 (PL60 April to June, where no caught-up case was withdrawn).
- A2 with references reissued from the go-live, at random or oldest first: new 2023-24 placements took references first held by 2019 to 2022 write-offs, so the posted read raised losses 1 to 4 points while A1 lowered them, the two composed to within 0.1 point of the answer in two cells, and the reference's latest holder reproduced the answer in seven cells; reissued from the agency's November 2024 platform move, the most recently freed first, the posted read sits below the answer in every cell and the latest holder above it.
- A second silent device for ask B (a superseded re-run of the June scoring run; an origination scorecard label corrected between the June and September extracts; paused loans left out of the June extract): the first two need a filed rule to adjudicate them, the third loses the truth; B3 stays the one silent primary, with the loan record's default month added as its in-world evidence, and the pair is priced with A1 as the most obvious device and B3 as the residual risk (49.1).
- The change log naming the June arrears clock (the audit's suggested WHAT for B3): a filed sentence on the ask's path is executed by the cracker; 1.3 files the WHAT (close of business) and three records show the June column counts to the run, so the device stays unnarrated.
- A1 as a silent device (round 2 judge): the judge took every Collections cure at its word (with the posted remittances, 60.5 to 74.7) and found the cure's treatment unfiled; 3.3 now files that a loan the loan record shows written off or settled is measured on what it recovered, so A1 is a filed rule every careful path executes. No replacement drawn: the cracker sheet already had the cracker resolving it, so the pair sheet does not move.
- The receipts file's loan number described only as a loan number (round 2 judge): the judge read the posting as the attribution and the placement report as a distractor; the dictionary now says what both fields hold (the loan number the receipt was posted to, an agency remittance posted on the reference it quotes; Wirraway's reference for the account while it is placed). Describing the reissue or the first-match posting as well was not built: it would announce the device.
- The June clock left out of the change log (round 2 judge): the judge read the June column as close of business and the 6 loans at 90 days with July defaults as a defect; CHG-26-0418 now records the move from the live system at the run to the quarter-end day's end-of-day snapshot, the job's source and nothing about days past due (the line above still holds against a sentence naming the clock; the judge showed the clock needs its source filed to be literal). Not taken: dropping the clock (ask B would carry no device), removing the loans at 89 and 179 days at the June close (the clock would stay with nothing filed to resolve it), a run log or a position-date column (a new file, or a load stamp marking the June file).
- Moving the 82 June loans that fall exactly 60 points off the threshold (round 2 judge): a gap at exactly 60 on whole-point scores would itself be a tell; 2.1 says 60 or more and the migration note rounds the converted score to a whole point, so the boundary is literal (SF32).
- A second device on ask B that a literal reader could resolve (round 2 repair): ask B classifies filed fields and every condition is pinned (1.3, 2.1 to 2.3, the runs file's dates, the register's dates); a backdated hardship approval, a superseded scoring run and a silently partial June extract each need a filed rule or lose the truth. Not built; the risk is priced on the pair line.
- The June clock left silent behind the change log's source (round 2 re-judge, FIX_NOW on slide 2 only): the judge's literal build read the June column unadjusted (PL36 stage 1 14,450 / 680 / 39 / 1,582) and no file said the June days past due count to the run date. Applied as prescribed: the dictionary's loan book lines record each extract's run clock, and B3 dies as a device (pair 65.2 with both careful, 49.1 cracker only). Not taken: restating the June column at close of business (the re-judge's alternative), which leaves ask B a plain read; re-keying slide 2 to the literal counts, which the re-judge ruled out and freeze.py holds.
- Ask B left device-less after the June clock was filed (round 2b, not shipped): the pair sat at 65.2 with both careful responses executing the clock. Round 2c draws B4 from the scoring engine's own failure mode (a partition carried forward on 1 July, rescored on 2 July), one digit of the loan number at first: single digits moved 10 to 16 counts on the run as it stands and 4 to 16 on its Scored rows alone, no digit both at 16; digits 3 and 4 together move all 16 both ways. Not taken: a status column alone without the rerun rows (loses the June-position score), a split run with no carried-forward rows (the battery's coverage check finds the missing loans), a Sept-side closed-or-stage-3 device (contradicts the dictionary's population sentences).
- The judge's optional pin on exit at first default (round 2c re-judge, APPROVE): not taken. 3.2's estimand already says "first defaults", and the one variant that moves a figure (an instant cure, AUD 13.1 million) needs a cure the record never dates and that 343 still-defaulted open loans contradict; closed as SF35 and asserted.
- Architecture 2 (Bellbird personal-loan ECL allowance) re-rooted 2026-11-01 at the Batch 3 queue reset: landed on the portal, the survival-to-date conditioning being the field's reflex; its world is closed and the slot moves to stress-testing-capital in a new world.
- Candidate: business deposit run-off by depositor type under the scenario (deposit-liquidity-behaviour): the deciding step was a depositor-type run-off rate applied to balances, a lookup, and the deposit cell sits beside task170's driver; dropped.
- Candidate: a term-deposit renewal ladder: the renewal rate by maturity bucket reads straight off the history, rule application; dropped.
- Candidate: intraday payment netting after a merger: the decisive step was matching two systems' payment keys, identity semantics under rule 3; dropped.
- Candidate: lenders mortgage insurer capacity under the house-price path: the stress lands in the insurer's capital, outside the bank's ICAAP book, and the call drifted toward opportunity sizing; dropped.
- Candidate: presale settlement risk on apartment development loans: the decisive step settled which presales settle, a population that is WHAT (the WHAT screen); dropped.
- Candidate: a head contractor's failure spreading to its subcontractor borrowers: reduces to a grouping (the contractor and its subcontractors at one PD), which stumping 1.1c rules out; dropped.
- A payment-limit run under stress: task168's mechanism; not drawn.
- First prototype of this architecture, with commercial-property investors and pass-through payers in the book: the payer and own-division readings cancelled (golden over the own-division rung 0.97 to 1.04), so the book was redrawn on business types whose buyers sit in other divisions.
- Strategy composition_mix on the card: banned by the guard against the window, and the driver carries no rate across mixes; tagged other.
- Forum committee_or_panel, role compliance_or_audit and context artifact filed_standard: banned against task273 and task130; redrawn as board_of_directors, finance_controller and register.
- Ask B at twice the grade PD with 16 forced group defaults: realised default shares of 6 to 24 per cent in grades whose PDs run 0.25 to 16 per cent, and 51 customers in default at the book date; redrawn at a realised rate equal to the grade PD, five group defaults, and the later-written-off companies carried into the 2025 snapshot (graded, or grade D when already in default).
- Write-offs at a NZD 150,000 median: the year's net credit losses near NZD 8 million against an 11.5 million stressed loss, a stress no ICAAP reviewer would accept; now a NZD 40,660 median with construction and hospitality failures heavier and later in the year (net credit losses NZD 3.9 million, the stress 2.9 times them).
- Agency remittances as one receipt type among three: the double record touched 7 of 12 cells; placement with the agency now follows a write-off by three to six months with remittances every one to three months, touching every cell.
- Folding buyers worth under NZD 1,200 a year into the borrower's largest buyer in the division: legal-name-only matching and the six-month base left their segment bins (business services 1.427, trade and logistics 2.348) through one engineering firm near a Table 2 edge; reverted, and a buyer's month under NZD 40 is simply not paid.
- The rural register with no mass: no business borrower moved to the rural book defaulted at the realised rate, so the register moved nothing; three of the moved borrowers now default on their own stream (the dairy downturn reaching agricultural contractors), moving two bands.
- The trigger Cross-default only on group rows: a marker isolating the device rows; ordinary events now carry it too (a borrower in default with another lender).
- Card payments at the trade counter at 30 per cent for non-retail types: payments from individuals carried enough of manufacturing and trade sales that leaving them out moved the book total to 12.0; the trade-counter card share is 55 per cent, and leaving them out now keeps the total (manufacturing still moves, SF11).
- Grading the book total to NZD 0.1 million: the six-month base would file 11.6 and the non-sales reading sit 0.008 from an edge; the 0.5-million bin keeps every licensed convention (11.458 to 11.574) inside with 0.18 to spare.
- The prompt's second sentence opening on "The workbook": its shell (how-much, the, docx+xlsx) repeated task305 v3 (guard heart WARN shell.repeat); the sentence now opens "Set out".
- Architecture 3 (Orari Bank's ICAAP business-book stress) spent 2026-11-01 at stage 4: the judge returned NOT_DETERMINISTIC with SOLUTION_WRONG and SEND_BACK, its Gate H line "decisive_step analytical only if the method is filed": CR-ST-02 2.1 and 3.2 read word for word give each borrower its own NZBN division's change (NZD 10.03 million, the default path), the payer route is unfiled (Gates B, C, E) and filing it would make it rule application; the leak reader's question 6 read the call as a stated rule plus fields read correctly; the asks rested on unfiled choices (guarantor receipts to the company, the agency's remittance against its collection, the rural-book customers and register, a lead's cross-default moved to the holder), Trade and logistics did not reproduce on the judge's payer method (2.56 to 2.61) and unmatched-payer weightings put the total from 11.72 to 11.91. The world is closed.
- Candidate (architecture 4): a campus's winter peak after six boiler houses go to air-source heat pumps, the morning warm-up asking for more than the units' output at the outdoor temperature and the electric flow boilers carrying the rest one for one: a physics-forced step with the field's COP route at rung 1, but energy-systems-utilities forecasting was taken by task138's fresh card (ban.pairing, ban.subdomain, ban.shape and ban.forum BLOCK), so redrawn.
- Candidate: a port's export tonnes after channel dredging, the berth pocket binding next: the berth's under-keel clearance is a harbour rule, so the step a literal reader executes is rule application; dropped.
- Candidate: a contact centre's offered calls once abandonment falls, retrials shrinking: the retrial window is a convention and "demand" invites the easy reading; dropped.
- Candidate: an electric bus fleet's winter range: cold-weather range loss is the field's reflex; dropped.
- Candidate: a bowel screening programme's first-round colonoscopy demand in a new district: a screening world beside task281's, and positivity at new ages needs an extrapolation; dropped.
- Candidate: an airline's reactionary delay on tighter turns: the swap test fails (any rotation of resources reads the same); dropped.
- Candidate: log trucks with only the loads at the old mass limit gaining: readable from net plus tare alone; kept as rung R2 under the bunk-volume step.
- The ask devices first drafted with the invoice's own registration and a docket file named for the weighbridge date: each was executed by the filed WHAT that pins it, so the invoice now carries only the port ticket and the dockets their posting date.
- The planning basis's fleet sentence without the units' recorded volumes: a later judge lesson (a decisive fact the WHAT does not name reads as a hidden rule) made 2.3 name each unit's tare, permit and full-bunk volumes, so the default is an omission inside a filed WHAT; how the limits combine stays unfiled.
- Arch 4, the loads graded to the nearest 100 for the total and 50 for each grade (stage 4 round 1, FIX_NOW): the payload
  conventions the WHAT licenses (per-load or grade-mean density, the mean payload or the mean of each load's inverse
  payload, the 44 t units recomputed or kept at their FY2026 net) spread the total over about 145 loads, wider than a
  100-load bin, and the judge's variants filed 29,200 against the golden's 29,100; no tuning of the plan can hold a
  spread wider than its bin. Filing the payload convention was not taken (it files the HOW); the loads are graded at
  the precision the per-load data carry, the total to 500 and each grade to 100, and the plan's grade yields are tuned
  so every convention, the tonne- and unit-weighted averages and every linking window sit inside the bins (tightest
  grade 29 loads, total 172).
- Arch 4, tightening the FY2026 loading margins to narrow that spread (0.06 t under the limit, bunks 0.4 per cent short
  of full): it halved the 44 t units' variant but left the inverse-payload variant, which follows the fleet's real
  payload spread, at about 80 loads; reverted to the original tightness once the bins carried the spread.
- Arch 4, "the FY2026 cartage paid against each carrier" (stage 4 round 1): open between invoices dated in FY2026 and
  what was paid for FY2026's loads (2,607 lines sit on the July invoices, the re-bills and the credits); the prompt and
  the basis now file the loads' year.
- Arch 4, the planning basis's numbered definitions with the fleet sentence naming each unit's tare, permit and
  full-bunk volumes (stage 4 round 1, realism): a planning note does not list the register's columns, and the sentence
  pointed at the volume cap; the note is rewritten in Logistics' planning voice, files the fleet as the register records
  it and the payload as what FY2026's loads would carry on the same units, and names no bunk or volume.
- Arch 4, fleet units coded by carrier (RLC-01 to PLH-08) with tares drawn per configuration and one bunk volume table
  (stage 4 round 1, realism): read as generated; Matiri's truck numbers now run with induction across the carriers,
  tares follow configuration, bunk count, age and fit-out, and full-bunk volumes the bunk count with unit-to-unit spread.
- Arch 4 round 1 repair, the fleet basis cut to "the units as the register records them" (coordinator, before the
  re-judge): it left the full-bunk volume out of the filed WHAT, so the mass-limit-only default stayed compliant on a
  literal reading and the re-judge could fail Gate H on it; the Logistics planning note now lists each unit's tare,
  50MAX permit and full-bunk volume for each log length as the register records them, in its own voice, and still no
  sentence says how mass and volume combine or that a load stops at its bunks (asserted, R3c). No graded figure moved.
