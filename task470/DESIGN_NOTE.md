# task470 design note: Corrisan Valley's 2027 unleaded avgas grants

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task470.json` (architecture v1), registered 2026-10-18 after a pull, so
  every card filed before it was in the check. Guard check PASS. Two bans cleared at the draw by redrawing the axis:
  the context artifact (monitoring_export, against task190) is now operations_log, the receiver network's record of
  each field's operations; the organisation family (government_agency, against task190) is now local_government, a
  regional air district. The structural test's older matches (gap population, pattern E, Gate G
  decomposition_attribution) are differentiated on the card: task107 v1 (a check's reach set by each source's delivery
  kind), task129 v1 (two causes separated through a per-record state), task36 (a candidate excluded by a filed remedy)
  and task44 v2 (a pilot's pooled effect split by a behavioural moderator). Nearest driver task153 at 0.08.
- **Seed:** ET27 (a state aviation office funds first the airport with the highest 2019 share of departures flown by
  aircraft of 50 seats or fewer; analysts joined the flights' tail numbers to today's aircraft register, many tails did
  not match and some matched small private aircraft). Kept: the world (a public body funding airfields one by one, the
  FAA aircraft register read through identifiers that change hands, emissions inventories), the decision (which fields
  are funded first, on a quantity of activity by one class of aircraft at each field) and the quantity's kind (each
  field's activity by the class that matters, here piston-engine aircraft, priced in lead). Made forward facing: the
  2027 grant round, qualified on the 2026 inventory year. Dropped as the decisive step: the seed's move (reading old
  tail numbers through today's register), which is identity resolution and data semantics; it survives as Layer 1
  (a transponder's 24-bit address follows its N-number, and an N-number reissued or an aircraft re-registered since
  2026 reads differently in the register as it stands now).
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL. The district's evidence is a conformed
  inventory built from sources never designed to join: its receiver network's record of every operation it heard at
  each field (24-bit address, UTC time, event type), the FAA register's fixed-width files (master, deregistered,
  aircraft reference, engine reference), the state aviation office's based aircraft list keyed by N-number, six
  control towers' daily counts, four fields' count studies and the fields' master records. The deciding quantity is
  each field's 2026 lead from piston aircraft, which airport lead inventories build from piston operations by engine
  class and operation type times lead per operation; at a field without a count the operations come from the network,
  and what the network misses has to be completed.
- **Shape:** 01, a ranked list under a cap: each of the 24 non-towered fields' 2026 piston lead, qualified or not
  against 25 kg, the count of qualifying fields and the first field below the line.
- **Strategy:** composition_mix (the network's seen-to-counted rate pooled over the counted fields does not fit a field
  whose based fleet differs in the share that never broadcasts), pattern E, decisive generator G14 (the conditioned
  yield), with G12 (a field the network hears little at is not a field with little activity) and G6 (the pool shifted
  under the rate). Gate G decomposition_attribution: the decisive move books the missing operations to the aircraft
  that generate them.
- **World:** United States, an unnamed state. The Corrisan Valley Air Quality District, a regional air district run by
  a governing board of county and city representatives, inventories lead from piston-engine aircraft at the 30
  public-use general aviation fields in its valley: six with a control tower and 24 without. In 2025 it put an ADS-B
  receiver on every field. Its Unleaded Avgas Transition Grants pay for an unleaded fuel tank and dispenser at a field
  without a tower; the 2027 round funds every such field whose 2026 lead from piston aircraft is 25 kg or more, under
  the district's inventory method.
- **Forcing fact:** the governing board adopts the 2027 grant round with the district's budget at its 9 December 2026
  meeting; the air toxics planner's qualification memo and the field inventory go to it. As-of: 20 November 2026. The
  call faces forward (the 2027 grant round); its quantity is the closed 2026 inventory year, which the program's
  guidelines name as the basis (a retrospective quantity with its reason: the program qualifies on the latest complete
  year).
- **Forum and forcing event:** council_or_assembly (the governing board), budget_or_appropriation (the 2027 grant
  round adopted with the budget). Organisation local_government; role policy_adviser. Personas from `guard.py names
  --geo "United States" --seed 470`: Jeanette Steele (Air Toxics Planner, who writes the qualification memo), Yolanda
  Cortez (Air Quality Specialist, who runs the receiver network) and Tonya Krause (Grants Program Manager); Brian Rowe
  replaced (his first name in task445).
- **Data-native sentence:** the district's receivers sit on every field and record every operation of an aircraft
  that broadcasts ADS-B Out and none of one that does not; the aircraft that do not broadcast are not spread evenly but
  based where old, privately flown piston aircraft are kept, so the operations the network misses are concentrated at
  those fields and absent at the flight-school fields whose rental fleets all broadcast.
- **The WHAT screen.** Population: every piston-engine aircraft operation (a takeoff or a landing, a touch-and-go being
  one of each) at a field in 2026, by any aircraft, heard by the network or not (filed in the district's method).
  Outcome: lead emitted, at the method's per-operation factors by engine class and operation type. Window: calendar
  2026, local time. Unit: kilograms of lead per field. Comparison: 25 kg. The decisive step settles none of them: it
  is how the operations the network did not hear are estimated at a field without a count.
- **Deliverables:** `corrisan_2026_field_piston_lead.csv` (the conformed inventory, one row per field and engine class)
  and `cvaqd_2027_unleaded_grant_qualification.docx` (the qualifying fields, each field's lead against 25 kg, a chart).
  Names to be fixed at the prompt.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: Physical & Environmental Sciences has Layer 1 techniques
    and no Layer 2 patterns on file, so the pitfall comes from the five families: estimation_fit (survivorship,
    weighting and post-stratification), here the missed activity placed with the units that never register.
  - `dataset-generation/references/layer1-messiness.md`: detections in UTC against tower counts kept by local day and
    tower hours, 24-bit addresses against N-numbers, the register's fixed-width layouts, based aircraft lists in mixed
    N-number formats, consultants' count study layouts, master records carried for years; each to be asserted neutral
    on the call.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): task462 (aerial plume detection weighted by a
    probability that rises with rate and wind) is the nearest family, a sensor that misses some activity; here the
    miss is not a per-event probability but a property of the unit (it never broadcasts), and the missing activity is
    rebuilt from which units were never heard anywhere in the year. task448 (a register's capture depending on the
    filing route) and task456 (three imperfect records of one state) are capture problems on lists, not on a sensor.

## Default path

To be written at design.

## Stump sentence

To be written at design.

## Three rules

To be written at design.

## Readability screen

To be written at design.

## Semantic fork table

To be written at design.

## Ladder

To be written at design.

## Closure table

To be written at design.

## Literal reader

To be written at design.

## Oracles

To be written at design.

## Ask sheet

To be written at design.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own move, reading 2019 tail numbers through today's register, is identity
  resolution decided by reading the register right (data semantics); kept as Layer 1.
- 2026-10-18, at the draw: a 2027 projection of commercial aircraft NOx after the 50-seat jets retire, decided by a
  departure queue's relief at the hub's runway: the same lesson as task459 (a rate read at the decision's operating
  level, not the period average) in the same pairing, and a second hub ground-time task after task469.
- 2026-10-18, at the draw: the transition effect read against not-yet-transitioned airports (staggered adoption):
  already taught by task136 and task230.
- 2026-10-18, at the draw: operations at untowered fields from a rate per based aircraft learned at towered fields
  (selection on the outcome) as the decisive step alone: one live degree of freedom (every rung a different rate on
  the same based-aircraft list); kept as a lower rung beside the network route.
