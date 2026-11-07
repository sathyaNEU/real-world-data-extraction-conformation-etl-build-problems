# task490 design note

Architecture 1, drawn 2026-11-07. Which summit the Coldmere Canals Trust's 2027/28 back-pumping scheme serves:
the summit whose two summit locks drew the most water from its summit pound by filling their chambers over the
2026 boating season (1 April to 31 October), rebuilt from the lock counters' camera records, the lock-keepers'
logs and the lock register into one ledger of chamber cycles. The number is fixed in Data Extraction &
Conformation (ETL) by `START_HERE.md`; its seed (ET47, Land Registry price-paid delta files) supplied the
objective only, for the reasons in `## Tried and rejected`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task490.json`, architecture v1, registered 2026-11-07 |
| Client domain / task type | General Statistics & Data Science (`general-statistics-data-science`), `data-integration-record-linkage-entity-resolution` (serves ETL): three record systems at six summit locks (two camera firmware layouts, a keepers' log in a scanned PDF, a lock register in two units) integrated into one ledger of chamber cycles, the grain that draws water |
| Objective | Data Extraction & Conformation: the season's boat movements at every summit lock conformed into the trust's lockage return (each chamber cycle with its lock, time, direction, boats and the water it drew), and lockage by summit and month read off it |
| Decision | which summit the 2027/28 back-pumping scheme serves, the one whose summit locks drew the most water from its summit pound over the 2026 season (`pick_one_of_n`). A retrospective quantity for a forward call: the pump is sited and sized on the last complete season's lockage because the 2027 season's boats are not yet on the water; nothing is forecast, so the tag stays ETL |
| Shape | 07: a grid of cells, lockage for every summit and month of the season, with each summit lock's season cycles, fillings and water; the arithmetic goes in `## Ask sheet` at stage 2 |
| Gap / pattern / generators | `objective` (the counters report boat movements correctly, and the decision is scored on water); pattern `none`; `G2` decisive (one unit of the decided thing is a chamber filling, and the record's unit is a boat movement, with no key between them), `G1` (a boat charged at a lockful, rung 0), `G19` (the lockage return's conformance, depth only) |
| Gate G | `etl_conformance`: the conformed lockage return is judged against the trust's lockage definition |
| Strategy | `grain_or_unit`; Layer 2 family `field_method`; pattern `own:lock-chamber-state-replayed-through-chamber-cycles` |
| Forum, forcing event, org family | `trustees_or_governors` (the trustees' capital meeting on 10 December 2026 approves the scheme), `budget_or_appropriation` (the 2027/28 capital programme), `nonprofit_or_charity` (a waterways charity that owns and runs a regional canal network) |
| Role | the trust's water resources planner, preparing the back-pumping siting paper (`capacity_planner`) |
| Context artifact | `operations_log`: the Tilsey lock-keepers' daily passage log |
| Calibration | none: the chamber's physics closes the reconstruction, and no sensor measures fillings |
| Personas | Katy Wilkinson (water resources planner, the golden's author), Elaine Freeman (head of water management, author of the programme paper), Keith Rahman (Tilsey lock-keeper team leader, the keepers' log), Kim Hussain (volunteer lock-keeper coordinator), Louis Carey (asset engineer, the 2025 lock survey), Gillian Walsh (counter programme officer, the camera site sheets), from `guard.py names --geo England --seed 490`; Nicole Holmes from the same draw was dropped on `people.first` |
| Fiction as-of date | 2026-11-06 (the planner's working date; the counter export is taken on 3 November 2026 and the keepers' log scanned on 4 November) |
| Guard | `guard.py check` on the first draft BLOCKed `test.same_puzzle_older` against task192 v4 and task311 (objective, G2, `pick_one_of_n`); both are differentiated on the card (192 groups fault events by a shared measured signature, 311 projects a standard error from variance components; here the grouping is physical and the quantity is a count rebuilt exactly). The register-time check is WARN only, answered below |

**The world.** The Coldmere Canals Trust (an invented waterways charity in the English West Midlands) owns and
runs a regional network of narrow and broad canals. Three of its canals cross a watershed at a summit pound fed
by reservoirs: Kelsby summit (narrow locks, the hire base at Kelsby Wharf and the Kelsby Ring holiday route),
Harnock summit (broad locks on the old barge route) and Tilsey summit (narrow locks at the head of the Tilsey
flight, staffed by volunteer lock-keepers in summer). Every summit pound loses water each time one of the two
locks that rise to it is filled. The 2027/28 capital programme carries one back-pumping scheme, and the
programme paper files the WHAT: the scheme serves the summit whose summit locks drew the most water from the
summit pound by filling their chambers over the 2026 season, 1 April to 31 October, in megalitres. The evidence
is the lock counter cameras' movement records at the six summit locks (one export, two firmware layouts across
the season), the Tilsey keepers' daily log for the weeks Tilsey Top Lock's camera was out, the camera site
sheets, the historic lock schedule and the 2025 asset survey of the chambers, the stoppage and restriction
notices, and the documents around them.

**Why the world moved.** ET47 asks which local market drove a regional mean-price fall, read from monthly
price-paid delta files appended to a yearly base. Every decisive step it offers is a field reading (the delta
files' add, change and delete records, the Category B transfer flag), a field method a strong solver takes as
written (a mix-adjusted or repeat-sales index), or a family banned or spent (mix against price is composition,
splitting the fall by market is decomposition, banned against task211). The number keeps its objective and
moves to a physical record system, where the ETL pincer does not close: what the counters record is a boat,
what drains the summit is a chamber filling, and the arithmetic between them is the lock's own.

**The 10/10 rules at the draw.** `stump_class` analytical. The deciding quantity, lockage, is what canal water
managers estimate for a summit's water budget, and the field works it by replaying each lock's chamber through
its boat movements: a boat going up always fills the chamber from the summit, a boat going down fills it only
when the cycle before left it empty, and boats that share a broad chamber fill it once. Layer 1 is the mess the
trust's systems make (a firmware change mid-season from the counter's clock time to UTC and from UP and DOWN to
the camera's A-to-B axis, a three-week camera outage covered only by a scanned keepers' log in local time,
duplicate detections when a boat holds under the camera, canoes logged though they portage round the lock,
unreadable index plates and visitor passes, chamber dimensions in feet and inches against cubic metres with one
lock re-measured); none of it moves the call. Layer 2 decides: on the generator's clean truth, with every record
and unit right, charging a lockful a boat and replaying each chamber one boat at a time both file Harnock,
because two boats that share a broad chamber are two records and one filling.

**Priced on a clean-truth prototype before registering (five seeds).** A lockful a boat files Harnock (about
2,830 ML against Tilsey's 2,480), the boat-by-boat replay files Harnock (about 2,170 against Kelsby's 1,730),
cycles charged a lockful each (pairing without the chamber's state) file Tilsey, and the replay through chamber
cycles files Kelsby (about 1,720 against Tilsey's 1,500 and Harnock's 1,290) on every seed. Kelsby's holiday
ring sends most boats up one summit lock and down the other, so its chambers are left set against the next boat
and it draws about 0.79 of a lockful a boat; Tilsey's queues are worked in turn (about 0.60); Harnock's broad
chambers carry two boats a cycle two times in three (about 0.45 a boat at twice a narrow lockful).

**Window and WARN answers.** `three_rules.strategy_risk`: the analyst test is executed on the clean truth, where
every field is read and no rule is filed; the easy routes fail on the chamber's grain and state, not on a
reading. `overuse.objective`: the objective is fixed by the number. `repeat.decision`: the scheme serves one
summit, so the call is one of a set; the asks carry the quantities. `people.first`: Nicole replaced from the
same draw.

## Tried and rejected

- Seed ET47's world (which local market drove the regional mean-price fall, read from price-paid delta files): every decisive step is a field reading (the delta records' add, change and delete status, the Category B flag), a field method taken as written (mix-adjusted or repeat-sales index; repeat sales screened dead in task479 screen 13), or a family banned or spent (composition_mix, decomposition_attribution against task211); world moved, objective kept.
- Bounding suppressed cells of published tables from overlapping cross-tabulations: spent by task475, task465 and task201 at the draw.
- Administrative-world candidates in the remaining ETL cells (identity resolution, grain, time semantics in a register or claims world): the ETL pincer closes them, a correction input on file makes the step rule application and one absent fails Gate B; screened at the draw against task464 architecture 5's cell map and task476's screens.
- Bridge weigh-in-motion with coincident lorries on the span (each event's strain is the sum of every vehicle on it, and the routine reads it as one): the honest stump strategy is decomposition_attribution (one measured response split across coincident components), banned against task211, and labelling it other to pass the ban is a relabel; the probe card also hit test.same_driver against task461 and the older same puzzle against task194. Dropped at the draw.
