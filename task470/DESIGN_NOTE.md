# task470 design note

Architecture 2 (re-rooted 2026-10-31). Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task470.json`, architecture v2, registered 2026-10-31T17:41:05Z after a pull,
  so every card filed before it was in the check (the re-roots of task118, task181 and task306 included). `guard.py check`
  on the registered card: PASS. One older-build match on gap, pattern and Gate G (task477) is answered by a
  differentiation line on the card. Axes drawn clear of the window at registration: organisation family
  research_or_statistics_office (local_government is banned against task181, government_agency against task306,
  utility_or_infrastructure against task118), forum minister_or_cabinet, forcing event statutory_or_regulatory_filing,
  role statistical_office_head, strategy classification_error, calibration none, context artifact register, shape 01.
  Architecture 1's identity and fate are the card's lineage, its shell (how-many, "Put", csv and docx) in
  `lineage_shells`.
- **Pairing.** Survey Research & Official Statistics / `census-register-administrative-data-quality` / Data Extraction &
  Conformation. The task type serves ETL in the taxonomy. The work is the field's own: a register-based dwelling statistic
  built by conforming the cadastre, the population register, the electricity hub's meter point register and its hourly
  reads into one dwelling-level occupancy file under the scheme's data contract, and the call is the grant designation
  that file decides.
- **Niche.** A ministry's 2027 vacant dwelling activation grant, piloted in one fictional Norwegian county of ten
  municipalities, goes to every municipality where at least 5.0 per cent of the dwellings the regulation counts stood
  vacant in the reference fortnight of 9 to 22 November 2026. The regulation defines vacant by whether anyone lived in the
  dwelling, whatever the population register shows, and has the national statistics office certify each municipality's
  share by 15 January 2027 from the hub's hourly meter data, which the regulation makes the office's source.
- **The call.** Which municipalities qualify (a designation set), with each municipality's vacant dwellings and share.
  Retrospective measurement, forward decision: the fortnight is closed, the grant is the 2027 programme's, and the
  regulation designates on that fortnight.
- **Shape.** 01, the candidates against a threshold: each municipality's vacant dwellings and share (two figures for each
  municipality), the designated set, the margin to the line, a chart of the shares against the threshold with named parts
  and the two files; with the asks, well over 25 criteria. Decision designation_set, answer set_of_items, question form
  whether (the call is where the grant should go).
- **Strategy.** classification_error. Gap objective first (the register's residents and the meter's level are correct
  records and are not what the regulation scores, which is whether anyone lived there), then population. Generators G3
  (record against operation: the meter's level records the heating, not the household) and G12 (absence of a registered
  resident against absence of residents). Gate G method_or_model_selection. Layer 2 family estimation_fit, pattern
  own:occupancy-from-the-household-daily-cycle-against-a-heating-load.
- **The ETL pincer, answered.** Of the five ETL moves this is the per-case input a second file pins: each dwelling's
  occupancy, pinned by its own hourly reads. The forcing file pins a condition (a household's daily cycle on some day of
  the fortnight). Reading the file correctly gives a level per hour and per day, and neither says whether anyone lived
  there; occupancy is the presence of the morning and evening rise over the dwelling's own night-time load, a model of a
  household's routine against a heating load that no field records, so a correct read is not sufficient. Nothing in the
  step is identity resolution, grain or time semantics.
- **Forum, event, organisation, role.** The ministry adopts the list (minister_or_cabinet); the regulation's delivery
  deadline forces it (statutory_or_regulatory_filing); the national statistics office certifies it
  (research_or_statistics_office), its dwelling statistics section head the stakeholder (statistical_office_head).
- **People** (`guard.py names --geo Norway --seed 470`, locale no_NO): Martine Strøm, head of the office's dwelling
  statistics section; Eirik Haug, the ministry's adviser on the scheme. Neither appears in the prompt.
- **Data-native sentence.** An empty dwelling in a Norwegian November is heated (a lowered thermostat or frost protection
  keeps the electric heating on), so its hourly load runs with the outdoor temperature at levels many lived-in flats never
  reach, while the population register still lists residents who have moved to care or abroad and omits students and
  workers who never re-registered; only a household's own morning and evening rise over its night-time load shows that
  someone lived there.
- **Abstraction sentence** (written against the nearest approved builds, not writable as the same): task182's "each
  bore's own lagged driver response" reads a unit's departure from its own response to a shared driver; here the step is
  the presence or absence of the users' daily rhythm in a unit's own record whose level a use-independent load carries,
  with no response to a driver estimated. Against task236 (a notified share read through a sentinel network's positivity)
  and task258 (each slow load rebuilt part by part), no second channel is used and nothing is rebuilt from components.
- **Sources.** The client's two-layer standard; register-based housing statistics (dwelling occupancy from the
  population register's registered residents, the official statistics convention this task's regulation sets aside);
  utility-data vacancy statistics (a dwelling counted vacant below a consumption floor over a period, the field's
  method at rung 1); smart-meter occupancy detection from load profiles (the household's daily activity cycle);
  Norway's centralised meter-data hub, its hourly reads and quality codes, and its meter point register;
  the Norwegian land register's public titles from before organisation numbers.

## Default path

The path a competent analyst takes after conforming every file correctly and reading both governing documents (figures
from the generator's checks on the built pack).

1. Read the regulation: the dwellings counted are the cadastre's Bolig units in use on or before 1 November 2026
   (Section 3); a dwelling is vacant when nobody lived in it on any day of 9 to 22 November 2026, whatever the register
   shows (Section 4); the office reads it from the hub's metered values with the cadastre (Section 5); 5.0 per cent or
   more of a municipality's counted dwellings qualifies it (Section 6).
2. Conform: 8,020 counted dwellings; each joined to its household metering points by the cadastre's unit ID, else by
   municipality and address for a single-unit house (Snøholt's points still under Fjordeid's old number 5809); the
   hourly values from UTC to Norwegian time, each hour once with the later delivery kept, a changed meter's two points
   added.
3. Apply the field's vacancy-from-meters rule, the utility-data vacancy statistic: each dwelling's average daily use
   over the fortnight, vacant under a consumption floor. A floor of 3 kWh a day finds 113 switched-off and fridge-only
   dwellings and no lived-in one; a floor of 10 finds 297, the lived-in dwellings' first percentile sitting at 9.3.
4. Validate it: 75 per cent of the dwellings under a 3 kWh floor have nobody registered on 1 November, against 9 per
   cent of the rest, so the floor agrees with the register where the register is right.
5. Share by municipality; the highest is Solmoen's 3.7 per cent at a 3 kWh floor.

Ends on: no municipality qualifies (none at any floor from 1 to 10 kWh a day).

Golden: five municipalities qualify (Tverrvika 7.3, Hesteby 6.4, Solmoen 6.5, Ørnevik 8.2 and Fjordeid 5.4 per cent).

## Stump sentence

A competent solver conforms the cadastre and the hub's hourly values, counts as vacant the dwellings whose average daily
use over the fortnight sits under a consumption floor, sees the floor agree with the register, and files that no
municipality qualifies at any floor from 1 to 10 kWh a day; an empty dwelling in a Norwegian November is left heated, so
the vacant dwellings use a median 20.5 kWh a day against 19.5 for the lived-in ones, and only a household's morning or
evening rise over the dwelling's own night-time use on some day shows that someone lived there, which designates five.

## Three rules

- **Task type:** census-register-administrative-data-quality in Survey Research & Official Statistics, which serves
  Data Extraction & Conformation: a register-based dwelling statistic conformed from the cadastre, the meter data
  hub's metering points and hourly values and the population register into one dwelling-level file under the
  regulation's contract, the designation read from it.
- **Domain test:** the quantity that decides is each dwelling's occupancy in the reference fortnight, the official
  statistics question of whether a dwelling is lived in; the field's two estimators for it are the register-based
  count (dwellings with no registered resident) and the utility-data vacancy statistic (a consumption floor on the
  metered electricity), and both sit at the bottom of the ladder here.
- **Swap:** put hospital wards for dwellings and admissions for residents and the call reads "which hospitals have
  5 per cent of their wards empty"; a ward's occupancy sits in the admissions system, no ward is heated empty because
  of the climate while its register lists the departed, and the household's own day against the building's heating has
  no meaning, so the task stops making sense.
- **Layer 1:** the hub's UTC hour stamps; days first delivered as estimates and replaced by a second delivery; hours
  missing after communication faults; meters changed in the fortnight under a new point; Snøholt's points still under
  Fjordeid's number because the grid company's records lag the 2024 split; addresses in capitals, unit numbers with a
  space or missing on single-unit houses, some points without the unit ID; communal points at block addresses; the
  register's events after 1 November; the land register's late registrations; the outage hours; every item as its
  system produces it, nothing placed to be caught.
- **Layer 2:** classification from a measured signal (estimation_fit): the choice of what in a dwelling's metered
  record shows that someone lived there, the household's daily cycle against the building's own heating load, rather
  than the level of use or the register.
- **Decisive step:** recognising that in a Norwegian November an empty dwelling's electricity is its heating, so the
  level of use cannot tell an empty dwelling from a lived-in one, and reading occupancy from whether, on any day, the
  dwelling's morning or evening use rose above its own night-time use, the household's day.
- **Not semantics:** every field read correctly (kWh per hour, UTC stamps, the E and M quality codes, the two
  deliveries, unit IDs, Snøholt's old number) gives a correct level for each dwelling and day, and the level is not
  occupancy; the floor route reads every field right and still files that no municipality qualifies.
- **Not rule application:** no filed rule says how occupancy shows in metered values (Section 5 names the source only),
  and executing every filed rule leaves the construction open: the enumerated family spreads from no municipality to
  all ten (the register all ten; floors of 0.5 to 10 kWh a day none; 10.5 kWh four, 11 six, 11.5 seven, 12 nine; 13 and
  over all ten; the register's empty dwellings with no household day Hesteby alone); the standing family, once Section 4
  rules the register out, still spreads from none to all ten across the floors; what rules the floors out is the data's
  own structure (vacant and lived-in dwellings with the same median use), silent, and the household-day members then
  agree on the golden five across a corridor of 0.29 to 1.00 kWh.
- **Analyst test:** a strong analyst who conforms every file and applies every filed rule takes the field's
  utility-data vacancy rule, a consumption floor anywhere from 1 to 10 kWh a day, sees it validate against the register,
  and files that no municipality qualifies.
- **Estimand:** Sections 3, 4 and 6 of regulation_vacant_dwelling_grant_2027.pdf: the counted dwellings (the cadastre's
  Bolig units in use on or before 1 November 2026), each vacant when nobody lived in it on any day of 9 to 22 November
  2026 whatever the population register shows, a municipality's share of its counted dwellings rounded to one decimal,
  qualifying at 5.0 per cent or more.
- **No decoy:** nothing is planted: no memo, briefing, draft or stakeholder figure argues the floor or the register; the
  regulation and the ministry's letter file the WHAT; the hub's, the cadastre's and the registers' files are what those
  systems produce.
- **No certified replay:** no certified, published or prior-year figure ships; nothing is recovered by reproducing a
  published share or count.
- **Lesson:** metered energy shows that a home is lived in through the shape of its use, not its level, wherever the
  building's own load runs with nobody there (heating in a cold climate); no build on file reads a household's daily
  cycle from a unit's own hourly record.

## Survivor anatomy

- **Actor:** the dwelling has rows (a cadastre unit, its metering points, their hours), and whether anybody lived in it
  has no column anywhere: the register's residents are another quantity the regulation sets aside, and no file holds
  a household, an occupancy flag or a vacancy code.
- **Link:** the signal is a relation between rows of one dwelling's own record, its morning and evening hours against
  its own night hours on the same day, a comparison no key offers and the field's vacancy statistic never makes.
- **Reflex:** the field's methods for the quantity sit at rungs 0 and 1: the register's empty dwellings designate all
  ten, and the utility-data consumption floor designates none at any floor from 1 to 10 kWh a day.
- **Back-test:** the textbook route validates: 75 per cent of the dwellings a 3 kWh floor calls vacant have nobody
  registered on 1 November, against 9 per cent of the rest, and none of them shows any use at all.
- **Second use:** every file the decisive step reads (the cadastre, the meter register, the hourly values) is the
  regulation's own evidence under Section 5 and is read by every route to the call; deleting the step drops no file.
- **Shock:** the golden five are the top or bottom five of none of 20 shipped statistics (the register-empty share, the
  mean and median use, the shares under and over floors from 1 to 30 kWh a day, the share of flats, the dwelling count,
  the holiday homes), asserted in checks.py.
- **Pins:** the WHAT is filed in the ministry's regulation (Sections 3, 4 and 6); no filed sentence names an hour of the
  day, a daily pattern, a consumption level, heating or a test (asserted on both governing documents), and the
  regulation's register sentence rules out rung 0 only.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the register's empty dwellings on 1 November | Section 4's register sentence | the register's rows | the official convention | none | none | a count | yes | readable |
| R1 a consumption floor on the fortnight's average daily use | none | the hourly values | the utility-data vacancy statistic | the register agrees with it | none | a filter | yes | readable |
| R2 the register's empty dwellings with no household day | Section 4 read as a pre-filter | the register's rows | none | none | none | a filter | yes | readable |
| R3 (decisive) the household day on any day of the fortnight | no sentence names an hour, a pattern or heating | no column holds occupancy | the field's statistic is the level, not the shape | the register and the floor agree with each other, not with it | the battery cleans the hours and stops | a within-dwelling comparison across hours of the day | the files are the call's own evidence | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | counted dwellings | Bolig units in use on or before 1 November 2026 | units with no date, units taken into use later, holiday homes | more dwellings, unmetered ones vacant | Section 3 (a date of taking into use on or before 1 November 2026) |
| SF2 | vacant | nobody lived in it on any day of the fortnight | no registered resident on 1 November | all ten | Section 4 (whether anyone was registered does not decide) |
| SF3 | the fortnight's clock | Norwegian time | the hub's UTC hours | same call | same call (asserted) |
| SF4 | an hour delivered twice | the later delivery | the first, or both added | same call | same call (asserted) |
| SF5 | a meter changed in the fortnight | both points added | the current point only | same call | same call (asserted) |
| SF6 | communal points | not a dwelling's | joined by address where one dwelling has it | same call | same call (asserted) |
| SF7 | Snøholt's points under 5809 | joined by unit ID | joined by address under 5809 | same call by ID | the meter register's unit IDs (asserted complete for Snøholt) |
| SF8 | the threshold | on the share rounded to one decimal | on the unrounded share | same call | same call (asserted, no share within 0.2 points of the line) |
| SF9 | the municipalities | the ten as they stood on 1 January 2026 | Fjordeid with Snøholt | same call | Section 2 |
| SF10 | missing hours | the day read on the hours present | a day with a gap left out | same call | same call (asserted) |
| SF11 | outage hours | read as recorded (zero) | left out | same call | same call (asserted) |
| SF12 | the household day | morning or evening over night on any day | morning only, evening only, highest hour over lowest, spread of hours (outage hours left out), any cut from 0.2 to 0.8 kWh | same call | same call (asserted, every member separates) |
| SF13 | on any day | a household on one day makes it lived in | the rise averaged over the fortnight | seven qualify | Section 4 (nobody lived in it on any day) |
| SF14 | a two-unit house | two dwellings | one | same call | Section 3 (dwelling units) |
| SF15 | holiday homes and care homes | not counted | counted | not in the extract | Section 3 |
| SF16 | table A, held on 1 November | the register's state that day | by event date against registration date | same persons | same call (asserted, no event straddles the day) |
| SF17 | table A, age | on 1 November | on 5 January | 26 of 30 cells move | the ministry's letter (by their age on that day) |
| SF18 | table A, a block's renumbering | a change of unit number | a move | the old ground floors' residents lost | the records (every resident, one day, one floor up, old numbers absent from the cadastre) |
| SF19 | table B, held on 1 November | by registration (tinglyst) date | by the deed's date | every figure moves | the ministry's letter (held on the land register); no transfer registered on the day |
| SF20 | table B, a company the municipality owns | KF, or all shares held itself or through such a company, together | one holder with all the shares | three municipalities move | the ministry's letter (itself or through such a company) |
| SF21 | table B, a title without an organisation number | the municipality when the name is its own | left out | every figure moves | the land register's holder name and the business register's names |
| SF22 | table B, how many | dwellings | titles | every figure moves | the ministry's letter (how many of its counted dwellings) |
| SF23 | table B, the inter-municipal company | not the municipality's | counted | Brekkevoll and Ravnsund move | the ministry's letter (all the shares) |

## Ladder

| Rung | Construction | Designates | Main figures kept |
|---|---|---|---|
| R0 | the register's empty dwellings on 1 November (the official convention) | all ten | 2 of 20 |
| R1 | a consumption floor of 1 to 10 kWh a day (the utility-data vacancy statistic) | none | 0 to 4 of 20 |
| R1b | floors of 10.5 to 12 kWh a day | four, six, seven, nine (Brekkevoll, Hesteby, Kvernhaug, Ravnsund first) | 0 to 2 of 20 |
| R2 | the register's empty dwellings with no household day | Hesteby alone | 0 of 20 |
| G | the household day on any day of the fortnight | Tverrvika, Hesteby, Solmoen, Ørnevik, Fjordeid | 20 of 20 |

Margins: the golden shares sit at least 0.27 points from the rounding line (Snøholt 4.68, Fjordeid 5.36); the counts are
exact because the household day separates every dwelling (lived-in minimum 1.00 kWh, vacant maximum 0.29). No floor from
0.5 to 30 kWh a day designates the golden five.

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the counted dwellings: Bolig units in use on or before 1 November 2026 (Section 3); units with no date, taken into use later, holiday homes and care homes out | filed in Section 3; C1 on the data (SF1) |
| 2 Unit of account | the dwelling (a cadastre unit), a two-unit house two dwellings; the municipality for the share | filed (Sections 3 and 6); SF14 |
| 3 Attribution window | 9 to 22 November 2026, every hour of the fortnight read; the hourly values cover exactly that fortnight | filed in Section 4; C1, nothing at the edges moves a dwelling (SF3) |
| 4 As-of dating | the dwellings as at 1 November (in-use date); municipalities as at 1 January 2026; table A on 1 November; table B on the land register on 1 November | filed in Sections 2 and 3 and in the ministry's letter; SF9, SF16, SF19 |
| 5 Version basis | the hub's later delivery where an estimated day was replaced | C1: first, latest and both give the same call (SF4) |
| 6 Denominator | the municipality's counted dwellings | filed in Section 6 |
| 7 Weighting | none: a count over a count | filed in Section 6 |
| 8 Window length | the whole fortnight, a dwelling lived in if any day shows a household | filed in Section 4 (on any day); SF13 records the averaged reading's other call |
| 9 Boundary inclusivity | 5.0 per cent or more qualifies | filed in Section 6; no share within 0.2 points of the rounding line (C1) |
| 10 Rounding path | each share rounded once to one decimal, the threshold read on the rounded share | filed in Section 6; C1, the unrounded reading gives the same call (SF8) |
| 11 Tie-break | none needed: the designation is a set, no ranking | C1 |
| 12 Maturity and censoring | none: the fortnight is closed and fully delivered; a few hours missing per meter | C1 (SF10) |
| 13 Order of operations | join, clock, deduplicate, classify, count | C1: each order prints the same call (SF3, SF4, SF5 asserted on every variant) |
| 14 Row order | none: every step is a set operation keyed by point and hour | C1 |
| 15 Duplicate resolution | an hour delivered twice (estimate then measurement): the later | C1 (SF4) |
| 16 Identity normalisation | point to dwelling by the cadastre's unit ID, else by municipality and address for a single-unit house; Snøholt's points under 5809 carry their IDs | the systems' own keys; C4 on the address-only join (SF6, SF7) |
| 17 Netting against gross | a dwelling's two points (a changed meter) added hour by hour | C1 (SF5) |
| 18 Dimensional units | kWh per hour throughout, one unit in the hub's file | units in the data |
| 19 Code and status semantics | kundekategori Husholdning against Fellesmåling; the quality codes E and M | the hub's own codes; C1 (SF4, SF6); never the stump |
| 20 Integerisation | whole dwellings and persons; nothing allocated | C1 by construction |
| 21 Clause scope | Section 4's register sentence decides vacancy only; the register is the source of table A | filed scope (Section 4, the ministry's letter) |
| 22 Forward window contents | the grant pays in March 2027 on the certified figures; nothing forecast | filed in Section 8; retrospective by the regulation's design |

## Literal reader

Executed word for word, the prompt and Sections 2 to 7 file the counted dwellings, the fortnight, the share, its rounding
and the threshold (SF1, SF8, SF9), and file vacant as nobody having lived in the dwelling on any day of the fortnight
whatever the register shows; Section 5 names the evidence and not how it shows occupancy, so the literal reader has to
decide what in a dwelling's metered values shows that someone lived there. Every reading that decides it from the record
itself, a household's day against the dwelling's own night hours in any form SF12 lists, gives the golden five; the
register's reading is ruled out by Section 4's last sentence, the averaged reading by Section 4's "on any day", and every
consumption floor by the records (C4): no floor separates the dwellings nobody lived in, which use a median 20.5 kWh a
day against the lived-in dwellings' 19.5, and floors over 9 kWh flag lived-in dwellings whose own hours show a household
every day. Each convention the call needs is closed in the fork table (SF3 to SF15 the same call, asserted), and each term
of the two tables by the ministry's letter or the records (SF16 to SF23). Every step of the write-up executes as written.

## Oracles

No shipped file ranks the municipalities on the call: no vacancy share, occupancy flag, household or count of empty
dwellings is filed anywhere. The register is the one second source on occupancy and the regulation sets it aside; it
agrees with the floor (the back-test), not with the golden. The outage log documents zero hours in three municipalities
that no household-day reading depends on (SF11), and the municipality list documents Snøholt's split (SF7). Table A's
only referee is the event log itself (every resident of a renumbered block moving one floor up on one day, the cadastre
holding only the new numbers); table B's are the land register's holder names against the business register's and the
shareholder register's counts. Nothing ties only under the golden.

## Ask sheet

**Table A, each municipality's persons registered in its counted dwellings on 1 November 2026, by age that day under
18, 18 to 66 and 67 and over** (30 figures). H18: the ministry's follow-up of the pilot (its letter of 1 December) wants
the population the counted dwellings held on the day the regulation fixes them; the call reads no register row. Primary
device D2 (a label stored before a silent switch): in November the cadastre renumbered 197 flats in blocks whose
residential floors had been numbered from a ground floor of shops, and the population register records the change as
each resident's move to the unit number one floor up on the day; the cadastre extract carries only the new numbers, so
undoing the register's events as written leaves the old ground floors' residents on numbers no dwelling has. The blocks
cover every age band in every municipality. Hazards: the snapshot as it stands (D2), the dead and the emigrated added
back (D4), the births and arrivals after 1 November (D5), ages on 5 January (D8), care home residents in units the
regulation does not count (D5). Path: the register of 5 January, the event log and the cadastre (3 files: the register's person, birth date and address
fields, the log's event, its two dates and its from and to addresses, the cadastre's address, unit, type and date of use). Stops: the register as it stands
-21 to +9 (27 of 30 missed); every event undone as written -16 to -1 (all 30); the dead and the emigrated left out -13 to
0 (20 of 30); ages on 5 January -12 to +12 (26 of 30). Realism: municipalities renumber flats to the national
unit-number standard block by block, and the register writes each change as a move.

**Table B, each municipality's counted dwellings held on the land register on 1 November 2026 by the municipality or a
company it owns** (10 figures). H18: the follow-up wants the municipalities' own housing among the counted dwellings, the
stock a municipality can bring back into use itself; the call reads no land register row. Primary device D7 (the true
key elsewhere): 52 titles from before the business register hold the municipalities' own houses and blocks under the
name of the day (a herredskommune, a bykommune, care of the chief executive or the property management) and no
organisation number, so a join by number misses them and the business register's exact names do not match them. Second
device D7 (names that lie both ways): private companies in a municipality's name (a builder, a landlord, a developer)
hold dwellings, an inter-municipal company two municipalities share holds a block in each, and in three municipalities
the housing company carries a name of its own and is owned 60 per cent through the municipality's holding company and
40 per cent directly. Hazards: transfers registered after 1 November (D2), deeds signed before the day and registered
after it (D8), the KF found by its parent (D5), titles at property level over many dwellings (D6). Path: the titles,
the transfers, the business register, the shareholder register, the municipality list and the cadastre (6 files). Stops: organisation numbers only, with the KF and the full chain, -14 to -4 (all ten missed); exact names the
same; every name beginning with the municipality's -49 to +63 (nine of ten); the titles as they stand -15 to +1 (all
ten); the deeds' dates -8 to -1 (all ten); one holder with all the shares -94 to 0 (three); the municipality and its KF
only -127 to 0 (six); no KF -97 to 0 (four); titles instead of dwellings -103 to -4 (all ten). Realism: the land register
still carries many public titles from before organisation numbers in the holder's name of the day.

Main population zero-counts: the call reads the cadastre's counted units, the meter register and the hourly values; no
register event, title, transfer, business or shareholder row is among them, and the call computed from those three files
alone is the golden (asserted). The cadastre and the meter register carry no old ground-floor number of a renumbered block
(asserted), so table A's device rows sit only in the register's files.

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| a block's renumbering read as moves (D2) | A | -16 |
| the snapshot as it stands (D2) | A | -21 |
| the dead and the emigrated left out (D4) | A | -13 |
| ages on 5 January (D8) | A | +12 |
| titles without a number left out (D7) | B | -14 |
| names beginning with the municipality's (D7) | B | +63 |
| the titles as they stand (D2) | B | -15 |
| the deed's date (D8) | B | -8 |
| one holder with all the shares (D7) | B | -94 |

Referee: the event log for the renumberings; the land register's holder names against the business register for the
old titles.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Table A, Brekkevoll, Tverrvika, Hesteby, Kvernhaug, Solmoen | the register of 5 January rolled back by undoing every later event as the register writes it, the dead and emigrated added back, ages on 1 November | miss |
| Table A, Ravnsund, Ørnevik, Langgrav, Fjordeid, Snøholt | the same | miss |
| Table B, the ten municipalities | transfers undone by registration date, the KF by its parent, the shares the municipality holds itself and through its own companies added together, holders matched by organisation number and, where a title has none, by exact name | miss |

Measured by: generator/ceiling.py on the cut pack: the cracker keeps 0 of the 40 table figures (table A 0 of 30, table B
0 of 10); the mirror (stopped at the 10 kWh floor, its best rung) keeps 0 of 40 and 6.0 of the 38 recommendation points.

Pair ceiling: 29.0 ((38 + 7 + 55 x 0) and (6.0 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each dwelling's occupancy in the fortnight, read from its own hourly electricity record as
   a household's day against the building's heating; with wards for dwellings there is no heating left on in an empty
   home, no register that lags, and no household's day, and the task stops making sense.
2. Two layers: Layer 1 (the hub's clock, deliveries, gaps and meter changes, Snøholt's old number, the address and unit
   formats, the communal points, the outage hours) is cleaned by the battery and moves nothing (SF3 to SF11 asserted);
   Layer 2, what in a dwelling's record shows that someone lived there, decides the call.
3. No plant, semantics or rule application decides: the floor reads every field right and every filed rule applied and
   files none; no sentence names the household's day; the register and the floor are the field's own methods.
4. Determinism: the WHAT filed in Sections 3, 4 and 6 and the ministry's letter; the household-day family converges on
   the golden five across every member and cut (SF12); the tables' terms closed (SF16 to SF23).
5. Gates on the final cut (target.zip sha256 26076f7e43ec0c97): generator checks 84 of 84, the verifier on every
   graded figure, two byte-identical builds, figures_check.py 123 of 123, precut.py 61 of 61, voice-check.py PASS,
   leak.py REVIEW with no LEAK, guard.py surface clean and heart WARN only on the question form (a gate asks
   whether); the leak reader and the determinism judge run from the main thread.
6. leak.py REVIEW, sweep 3: the regulation's 5.0 is the threshold Section 6 files, shared by every reading,
   harmless.
7. leak.py REVIEW, sweep 4: the regulation's section, statistics, fortnight, points, office and cadastre are its
   own nouns, none names the decisive step, harmless (ruled here, not sent to the reader).

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
- 2026-10-18, at design: based broadcasting airplanes laid up for the year counted among the never-recorded: the small
  count fields' ratios split (L08 2 airplanes to 5) and the family of rate estimators spread 3 per cent; dropped.
- 2026-10-18, at design: an N-number changed late in 2026 at a count field read as never recorded by its current
  address and moved L08's ratio; changes kept to fields without a count and before September (SF12 asserted).
- 2026-10-18, at design: piston helicopters in the fleet: Table 1 is airplanes only and would need a rotorcraft factor;
  the valley's helicopters are turbine.
- 2026-10-18, at design: field targets on whole kilograms gave leads of exactly 22.00 and 3.00; offsets added so no lead
  sits within 0.02 kg of a whole kilogram and no tower's operations on a hundred.
- 2026-10-18, at stage 4: W33 under R4b (the never-recorded share of based airplanes as the unrecorded share, reader
  round 1's route) sat 0.1 per cent under the line, so that rung named no set; W33's recorded lead raised 0.38 kg, R4b
  now 5.2 per cent over, the golden W33 at 14.1 kg.
- 2026-10-18, at stage 4: today's register as the ask's primary device (the moved addresses' piston months priced as
  the turbines): reader round 2 resolved MASTER and DEREG by issue and cancel dates and hit all twelve figures, so the
  honest cracker scored 100 and the pair 66.6; the device became the Registry's dates leading the swap.
- 2026-10-18, at stage 4: the Registry's dates trailing the swap (the turbine flying under the number before its
  certificate): the turbines visit fields without a tower in that window, so the register's dates would price
  untowered operations as piston and move the call, and four towers' turbines fly too little to clear the bins.
- 2026-10-31, architecture 1 spent at the batch 1 repair: `guard.py heart` BLOCKed it against task242, registered ninety
  minutes earlier in another session, on strategy composition_mix, calibration gold_standard_subsample, forum
  council_or_assembly, forcing event budget_or_appropriation and organisation family local_government, and on pattern E
  against task197. It is the same core puzzle as task242 (a detector's capture calibrated on a gold-standard subsample,
  corrected by the composition of what it misses), so the slot re-roots into another world, dataset and shell. The
  repair's lessons (no file describing the data, no count the data hold in the prompt, the shell under its quotas,
  metadata prose that says what the task decides) carry into architecture 2.
- 2026-10-31, re-root screens on the item-response-theory-test-equating cell, each dead on file: item position effects
  in pre-equating (task482 v6, landed at stage 4); rapid guessing in a low-stakes sitting (task479 v4); drifted or
  released anchors and non-equivalent groups (task450, task471); rater severity on a shared subset (task471 v2).
- 2026-10-31, re-root screen: a computer-based mode effect read against students' prior paper scores with the prior's
  measurement error corrected. Rejected before code: the correction is a model of the measurement (the sampled case of
  `guide-to-prompt`'s ETL pincer, whose estimate spreads across reasonable settings), and with schools opting in, the
  school's mean prior score (measured almost without error) removes most of the bias, so the contextual model a strong
  analyst writes first lands the golden.
- 2026-10-31, re-root screens on the payment-claims and register cells: ACA grace-period cures (task482 v11, rule-heavy);
  high-cost regression to the mean, bundles against a comparison group, contract-order reconciliation and risk-adjusted
  ratios of totals (task487's screen); register over-coverage by signs of life (task478, task482); the seasonal
  adjustment cell's patterns (task453, task463, task467, task477, task481 spent).
- 2026-10-31, the world's first form, an Irish county council's vacancy programme: Ireland was drawn hours earlier by
  task268, and local_government is banned against task181, so the world moved to a Norwegian county pilot run by the
  national statistics office, where an empty dwelling is heated in November and the field's consumption floor fails for
  a reason of the country's own housing.
- 2026-10-31, at design: the weather service's hourly temperatures as a distractor: a temperature file beside an
  occupancy question points at heating, the decisive step's own premise; replaced by the power exchange's day-ahead
  prices.
- 2026-10-31, at design: holiday homes' and building sites' metering points in the hub's extract: a set of homes
  everyone knows stand empty, heated in November, would calibrate the empty profile for the solver; the extract covers
  the household points from each dwelling's day of use, as the data agreement would.
- 2026-10-31, at design: table B on organisation numbers, the KF and a one-step chain: a careful solver executing the
  ministry's definition kept all ten figures; rebuilt on the municipalities' own titles from before the business
  register (no number, the name of the day), namesake companies holding dwellings, and housing companies owned through
  the holding company and directly together.
- 2026-10-31, at design: the outages in three golden municipalities read as a pattern beside the answer; moved to
  Brekkevoll, Solmoen and Snøholt. Range-type household-day readings (a day's highest hour over its lowest) take an
  outage's zero hours as use in a vacant dwelling; with the outage log's hours left out they separate (SF12).
- 2026-10-31, at design: the Shock screen found the golden five were the five municipalities with the fewest flats;
  Hesteby's housing given more blocks and Snøholt's fewer, so no sort of a shipped statistic gives the set.
- 2026-10-31, at design: table A's renumbering in one or two blocks per municipality: a careful solver kept a cell where
  a small municipality's renumbered ground floors held nobody of one age band; blocks are now chosen until every band
  lives on the old ground floors on 1 November, a household taking in a child, a lodger or a parent where none does.
- 2026-10-31, at design: a register move dated before 1 November and registered after it opened two readings of "held
  as resident on 1 November" (the registration or the event date); the October moves are registered by 31 October
  (SF16).
