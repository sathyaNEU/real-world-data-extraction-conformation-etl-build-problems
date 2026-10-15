# task184 design note (architecture 2)

Re-root in oviya13ya's Anomaly Detection lane, same number and objective. Architecture 1 (a mobile screening team
posted among eight flagged airports, decided by the lanes each checkpoint actually opens) was sent back at judge pass
3 on Gate C and Gate G and is spent; its two architectures of the stump, the stand-down and then the counterfactual
arm, are in `## Tried and rejected` and in the card's lineage. Nothing of the airport world carries over.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task184.json` (v2), registered 2026-10-14 and re-registered
  2026-10-15 after task459 was drawn, verdict WARN.
- **Pairing:** Criminology & Justice, `crime-incidence-hotspot-analysis`, objective Anomaly Detection & Diagnostics.
  The domain has never been drawn (zero cards), and the task type is the one the client taxonomy lists against
  Anomaly Detection, so the structural WARN that dogged architecture 1 (a client domain with no task type serving the
  objective) is gone.
- **World:** Kelverstoke, a fictional city in a UK-like island state, and its community safety partnership. The
  Harbourgate quarter is the city's night-time economy: licensed premises, a taxi rank, two car parks and the streets
  between them. People (guard.py names, en_GB, seeds 1842 and 1843): Bethan Murray, Mitchell Webb, Rosie Kelly,
  Joshua Davies; roles fixed at design.
- **Stakeholder, forum, forcing event:** the partnership's community safety manager (role `programme_officer`) puts
  the 2027 patrol slate to the partnership board (forum `committee_or_panel`); the forcing event is the
  2027 season itself (`season_or_peak`): the quarter's trade and its offences run from April to September, the
  patrol is a seasonal one, and the slate has to be set before the season opens on 1 April. The contract that caps
  the slate at eight slots a week is standing, not the event that forces the call.
- **Shape 07 (grid of cells):** the graded object is the week laid out as a grid, seven days by six four-hour
  bands, with the offences the patrol would meet in each of the 42 cells; the eight the contract buys are the eight
  heaviest cells, read off the grid. Criteria: 42 cell figures, the eight slot names, the covered total, the
  runner-up and the gap, the chart's named parts and the two files, plus 36 ask figures. The cell grid is the
  decisive construction's own output, so a response on any wrong basis misses every one of the 42 (ladder, Worth),
  which is why the grid and not a ranked eight is the right shape here. Well over 25 criteria.
- **Strategy and gate:** `grain_or_unit` (the unit of analysis is the offence-hour, not the offence), gate G
  `method_or_model_selection`, gap population then time, generators G1 (unit of value) then G7 (operating window),
  pattern none, layer 2 `estimand_identification` (own:aoristic-weight-against-a-point-in-time), calibration none.
- **Data-native sentence:** a recorded offence carries three timestamps, the earliest it can have happened, the
  latest, and when it was reported, and for the offences this patrol exists to catch the first two are hours or days
  apart, because the victim was asleep, away or had left the vehicle, so each such offence belongs partly to every
  four-hour slot its window touches and the slate is set on that weight.
- **WARNs answered:** `three_rules.strategy_risk` (grain_or_unit) is answered by the analyst test, which files a
  wrong slate with every column read correctly, both recording systems reconciled and every duplicate dropped: the
  decisive quantity is one the solver builds (the weight a window puts on a slot), not one it reads.
  `repeat.decision` (`ranked_slate_under_cap` against task459): the cap is the contract's standing count and the
  graded structure is the 42-cell grid, not a ranked list, so the prompt and the deliverables read nothing like an
  emissions slate; the answer type is where the two touch and it is the one axis the decision itself fixes.
  `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, six of the last twelve): the mechanism here is the
  weight a windowed event puts on each candidate slot, not a model picked from a menu, and the batch's variation sits
  in the generators (G1 and G7, neither used on this objective since task85). `repeat.question_form` (which): the
  decision is a slate under a cap, so the leading question asks which slots.
- **Same-puzzle test:** no build on file shares gap population, pattern none and decision `ranked_slate_under_cap`;
  the nearest drivers are 0.08 (task121 v3, task180 v4) and the card carries a differentiation line against task180,
  whose hourly distortion is in which events reach the record at all, where this one's is in where recorded events
  are placed.
- **Sources (one line each):** strategies.md Part 4, G1 (the unit of value: the natural metric leads and the right
  unit flips it) and G7 (the operating window pinned in an operations file, never the prompt); the AD mechanism
  screen's 21 spent drivers, none of which turns on the precision of an event's recorded time.

## Default path

1. Read the extract notes and the counting rules: the offence classes, the two recording systems and the cut-over.
2. Load the legacy incident export and the new records management export, conform the columns, drop the offences that
   appear in both across the cut-over fortnight, and fix the gazetteer so every offence location maps to the
   Harbourgate quarter.
3. Keep the offence classes the tasking contract names and the Harbourgate locations.
4. Take each offence's occurrence time as `occurred_from`, the earliest time it can have happened, and bucket it into
   its day of week and four-hour slot.
5. Sum the offences per slot over the two seasons on record, divide by the seasons, and commission the six slots with
   the most offences.

Ends on: the week's seven 20:00 to 24:00 slots and Friday 08:00 to 12:00, filed as covering 7,838 contracted offences a season; the eight it names meet 3,355 of the 4,232 the golden's eight meet, 0.793 of it.
Golden: Saturday 20:00, Sunday 00:00, Friday 20:00, Sunday 04:00, Saturday 00:00, Saturday 04:00, Thursday 20:00 and Wednesday 20:00, covering 4,232 contracted offences a season, 4,250 to the nearest fifty.

## Stump sentence

A competent solver conforms the two recording systems, drops the cross-system duplicates, fixes the gazetteer, keeps
the contracted classes in the quarter, takes each offence's occurrence time as `occurred_from` and commissions the
week's seven 20:00 to 24:00 slots and Friday 08:00 to 12:00, filing 7,838 covered offences a season; the step that
lands it there is treating a window as the point in time it starts, when nine in ten of these offences have a window
over four hours long, 96 per cent of them cross a slot boundary, and the weight those windows put on the quarter's
after-midnight and early-morning slots is what the patrol is bought for.

## Three rules

- **Task type:** `crime-incidence-hotspot-analysis`, the client taxonomy's own task type for Anomaly Detection in
  Criminology & Justice: where and when recorded offences concentrate, and which concentration is real.
- **Domain test:** the deciding analysis is aoristic crime analysis, the field's own method for offences whose
  occurrence time is known only as a window: each offence contributes a fraction of itself to every hour its window
  touches, and a slot's weight is the sum of those fractions over the offence classes the patrol covers.
- **Swap:** "which six four-hour slots should the depot's relief crew cover, and how many breakdowns would they
  reach" has no offence discovered on return, no last-seen and found pair and so no window to spread: a breakdown is
  reported when it happens, and the task stops making sense.
- **Layer 1:** two recording systems across a cut-over with different column names and time formats; occurrence
  windows reported in round clock hours, as victims give them; the same offence in both exports under two reference
  numbers for one fortnight; a gazetteer with two spellings per street; four
  footfall sensors with outages; a tasking plan spreadsheet with hours as text; two clock changes inside the seasons;
  one offence class whose counts jump when a national counting rule changed, documented in the notes. Each is what
  these systems produce, none decides the call.
- **Layer 2:** the shortcut is to treat a recorded offence as an event at a point in time; the expert treats it as a
  distribution over the window it is known to lie in, and sums those distributions into the slot weights.
- **Decisive step:** spreading each offence's weight across the hours of its occurrence window instead of assigning
  it to one hour of it.
- **Not semantics:** the reading is given away for free, so nothing is left to catch. The records management
  system's data dictionary defines `occurred_from` as the earliest time the offence can have occurred and
  `occurred_to` as the latest, and the legacy export's layout note says the same of its two fields; both ship, and
  the analyst test reads them that way. A solver can therefore know exactly what the columns mean, know the time is
  uncertain, and still file the wrong slate, because what it gets wrong is the estimator it picks for an unobserved
  count, not the meaning of a field. The call flips on the construction and on nothing that a dictionary could
  settle.
- **Not rule application:** no filed sentence says how to treat an occurrence window, asserted by a word sweep over
  every shipped document for a weight, a share, a duration, a proportion, a spread and a slot attribution. The
  counting rules say when an offence is recorded and under which class; the contract says how many slots it buys and
  what makes an offence covered; the tasking schedule lists the slot boundaries; the dictionary says what the two
  timestamps mean. Executing all four word for word leaves the question of what a slot's offence weight is
  unanswered, which is why the literal reader reaches it only by reasoning about the records' structure, and the
  default path executes the same four sentences and files the wrong slate.
- **Analyst test:** a strong analyst who reads every column correctly, conforms the legacy export to the new records
  management export, drops the cross-system duplicates, fixes the gazetteer and keeps the contracted classes takes
  each offence's occurrence time as `occurred_from` and commissions the week's seven 20:00 to 24:00 slots and Friday
  08:00 to 12:00, filed as covering 7,838 contracted offences a season; wrong, because for nine in ten of these
  offences the window runs over four hours and a point in it is not where the offence happened.
- **Estimand:** how many offences of the contracted classes occurred in each slot in the Harbourgate quarter, per
  season over the two on record. Filed literally, and only as the WHAT: the tasking contract defines a covered
  offence as one of its scheduled classes that occurred inside the quarter while the patrol was on duty, the tasking
  schedule lists the 42 slot boundaries, the location register fixes the quarter and the contract fixes the season
  dates. No filed sentence touches the weighting, because none of these records holds the time an offence occurred:
  each holds the earliest and the latest time it can have occurred, so the count the contract defines is unobserved
  and has to be estimated. That estimation is the open HOW, forced by the data's structure (`determinism-check`
  section 1), and the sum of each window's overlap share is the only construction that returns the contract's
  quantity without assuming a time the record does not hold.
- **No decoy:** nothing is planted to be caught. No block is copied, no rule withheld, no memo argues a wrong slate,
  and no shipped artifact ranks the slots.
- **No certified replay:** no published slot ranking or covered-offence figure exists in the pack, so the method
  cannot be recovered by reproducing one.
- **Lesson:** an event recorded with a window is not an event at a time, and a decision scored over sub-daily
  windows has to be built on the weight each window puts on each one. No build on file teaches it: task180 turns on
  which events reach the record, task181 on the opportunities that generate them, task85 on each unit's own
  observation window, and none on the precision of a recorded time.

## Readability screen

Each rung is the move a solver makes to leave the rung below; the decisive rung has to be silent on all six tests.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 1, the window's other end, the discovery time | no | yes, `occurred_to` sits beside `occurred_from` | yes, "when was it found" is the first thing a reader asks of a window | no | no | yes, one column swapped | readable |
| 2, the window's midpoint | no | no, the midpoint is computed | yes, the statistically minded correction to a range | no | no | yes, one mean of two columns | readable |
| 3, the weight each window puts on each slot (decisive) | no: no shipped sentence says an offence contributes to more than one slot, names a weight, or says what to do with a window; the counting rules say when an offence is recorded and under which class, the tasking contract says how many slots it buys and that a covered offence is one that occurred in the quarter while the patrol was on duty, and neither says how to treat a window (asserted by word sweep over every document) | no: no column holds a weight, a duration or a slot, and the weight is built from two timestamps against a recurring grid the solver lays down itself | no: the window's start, its end, its midpoint and the precisely timed subset each name a different slate, and the first three are the three reflexes | no: no shipped figure ranks or scores a slot; the patrol's own tasking plan records the hours worked, not the offences they met | no: keys unique once the cut-over duplicates go, every join matched, no missing day | no: the weight is a sum over 42 recurring blocks of each window's overlap with them, and 96 per cent of the windows cross a block boundary | silent |

## Ladder

Built values from the generator's prototype at the registered draw. Contracted offences a season, the mean of the
two seasons on record; the figure each rung files is the figure its own basis gives for its own eight.

| Rung | Construction | Slate | Files | Meets, on the golden's basis |
|---|---|---|---|---|
| 0, default | each offence at `occurred_from`, the earliest time it can have happened | the 20:00 slot on all seven nights, and Friday 08:00 | 7,838 | 3,355 (0.793) |
| 1 | each offence at `occurred_to`, when it was found | the 08:00 slot on all seven mornings, and Friday 16:00 | 5,448 | 2,170 (0.513) |
| 2 | each offence at its window's midpoint | the 00:00 slot on all seven nights, and Friday 12:00 | 6,869 | 2,893 (0.684) |
| 3, golden | each offence spread across the slots its window touches, in proportion to the window in each | Sat 20:00, Sun 00:00, Fri 20:00, Sun 04:00, Sat 00:00, Sat 04:00, Thu 20:00, Wed 20:00 | 4,232 | 4,232 |

- **The golden's eight, in order:** Saturday 20:00 647.2, Sunday 00:00 642.5, Friday 20:00 590.2, Sunday 04:00
  557.4, Saturday 00:00 538.6, Saturday 04:00 455.2, Thursday 20:00 405.0 and Wednesday 20:00 395.7. Ninth is
  Tuesday 20:00 at 347.2, so the cap falls on a 14.0 per cent gap.
- **Why only the spread finds it:** each wrong basis puts the whole slate in one band, the evening starts, the
  morning discoveries or the after-midnight midpoints, and each files a figure between 1.3 and 1.9 times the
  coverage its own eight actually meet. The golden slate is the only one that spans three bands, and the two 04:00
  to 08:00 slots no reflex reaches are its fourth and sixth members.
- **Variants (asserted):** spreading in hourly, 15-minute or 5-minute steps gives figures identical to the exact
  overlap share to within 4e-10, because every window is recorded on the hour at both ends (SF7); spreading in
  proportion to the quarter's own hourly profile of precisely timed offences, the refinement in the literature,
  gives the same eight slots, because the quarter trades from 04:00 at the fish market and its taxi rank clears at
  05:00, so that profile is not empty in the early morning; and the slate computed from the offences' true times,
  which the generator holds and the pack never ships, is the same eight slots in the same order. The hygiene reflex
  has nothing to keep: every contracted offence's window runs at least two hours and nine in ten run over four, so
  dropping the imprecise records empties the population rather than cleaning it.
- **Worth:** every one of the 42 cell figures is wrong on every wrong basis, the covered total is 24 to 49 per cent
  low or 30 to 85 per cent high depending on which basis files it, and a rung-0 response keeps four of the eight
  slot names and not one figure.

## Semantic fork table

| SF | Term or convention | Golden reading | Alternatives | Call under each | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the offences the tasking contract covers | the five classes in the contract's schedule | every recorded offence in the quarter | a different slate, not a reading | the contract's schedule names the five classes (asserted present) |
| SF2 | would meet, a covered offence | an offence that occurred in the quarter while the patrol was on duty | an offence recorded as reported during the slot | the report-time slate, not a reading | the contract defines a covered offence as one that occurred while the patrol was on duty (asserted present) |
| SF3 | the week's four-hour slots | the 42 slots from midnight, Monday first, as the tasking schedule lists them | slots aligned to another hour | a different slate | the tasking schedule lists the slot boundaries (asserted present) |
| SF4 | the quarter | the five locations in the quarter's location register | a radius or a ward boundary | same slate under either (asserted) | the location register is the only boundary in the pack |
| SF5 | the seasons on record | 1 April to 30 September 2025 and the same months of 2026 | calendar years; the whole extract | same slate (asserted); the figures halve or change by a sixth | the contract's season dates and the extract's own span |
| SF6 | the figure's period | one season, the mean of the two on record | the two seasons added | same slate, every figure doubled | the question asks for the 2027 season and the contract buys a season |
| SF7 | an offence's weight on a slot | the share of its occurrence window that falls in the slot | the window sampled in hourly, 15-minute or 5-minute steps | identical to the last decimal place, so the same slate and the same 42 figures (asserted: the largest difference between the three grains and the exact share is under 1e-9 on every slot) | every window is recorded on the hour at both ends, so each whole hour of a window lies inside one slot and every grain dividing an hour returns the exact share; there is no grain to choose |
| SF8 | the hourly profile a weight might use | none: the weight is uniform across the window | the quarter's own hourly profile of offences, as the refinement in the literature | same slate (asserted) | no contracted record carries a point in time, so the contracted classes supply no profile, and the classes that do are other offences with their own hours |
| SF9 | rounding path | the figure rounded once at the end to the nearest fifty; shares to one decimal | each offence's share rounded to a decimal place first and the rounded parts summed | some cells differ by fifty (asserted: the paths part by up to 11.4 offences on a cell, because a share of a seven-hour window rounds down every time) | the question asks for the figures to the nearest fifty, which rounds once the figure it asks for; nothing in the pack reports or asks for a rounded part, and no graded figure is the sum of figures the pack rounds |

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the contracted classes' offences recorded in the quarter in the two seasons | SF1, SF4, SF5 |
| 2 | Unit of account | one recorded offence, weighted by its window | SF7 |
| 3 | Attribution window | the slot a share of the offence's window falls in | the contract's definition of a covered offence |
| 4 | As-of dating | the extract of 22 January 2027 | filed in the extract notes |
| 5 | Version basis | the new records management system for the whole of both seasons, the legacy export for the classes it still held | the extract notes' migration dates |
| 6 | Denominator | none for the slot figures; the quarter's contracted offences for the shares | the question |
| 7 | Weighting | the share of each window in each slot | SF7 |
| 8 | Window length | each offence's own, from `occurred_from` to `occurred_to` | the data dictionary defines the two as the earliest and the latest time the offence can have occurred; the legacy layout note says the same of its pair (asserted present) |
| 9 | Boundary inclusivity | a slot holds the time from its start up to its end | the tasking schedule's slot list |
| 10 | Rounding path | the nearest fifty from unrounded weights, rounded once at the end | SF9 |
| 11 | Tie-break | none; the cap falls on an 11.1 per cent gap | asserted |
| 12 | Maturity and censoring | both seasons closed and fully recorded at the extract date | the extract notes; no offence recorded after the extract |
| 13 | Order of operations | conform, de-duplicate, filter to the quarter and the classes, then weight | the construction |
| 14 | Row order | none | the weight is a sum |
| 15 | Duplicate resolution | one offence per crime reference; the fortnight both systems held the non-contracted classes carries each of those twice | the extract notes name the two systems and their dates |
| 16 | Identity normalisation | addresses to the quarter's five locations through the gazetteer | the gazetteer ships with both spellings of each street |
| 17 | Netting | none | not applicable |
| 18 | Dimensional units | offences, hours, pedestrians | the columns and the sensor file |
| 19 | Code semantics | class names differ between the two systems; the crosswalk maps them | the extract notes' class crosswalk |
| 20 | Integerisation | the weights are fractional by construction and rounded once at the end | SF7, SF9 |
| 21 | Clause scope | the 2027 season, 1 April to 30 September | the contract |
| 22 | Forward window contents | the slate and its figures, from the two seasons on record | the contract's season dates; no 2027 offence exists |

## Literal reader

Executing the question, the tasking contract and the tasking schedule word for word: the patrol covers eight of the
42 four-hour slots the schedule lists; a covered offence is one of the contracted classes that occurred in the
quarter while the patrol was on duty; so a slot's figure is the number of contracted offences that occurred in it.
For an offence whose record gives the earliest and the latest time it can have happened and nothing between, the
number that occurred in a slot is the share of that window the slot holds, and the slot figures are those shares
summed. Every reading in SF1 to SF9 returns the same eight slots. The default path comes from the same estimand by
taking the earliest time the offence can have happened as the time it did.

## Oracles

- The patrol's own tasking plan for the two seasons: the hours the patrol worked, not the offences they met, so it
  scores no slot and ranks nothing (asserted: it carries no offence figure).
- The pedestrian sensors: footfall by hour, which moves with the quarter's trade and not with the contracted
  offences (asserted: the sensor profile ranks the slots differently from every basis in the ladder).
- The counting rules and the class crosswalk: they say when an offence is recorded and under which class, never
  where in its window it happened.
- None ties only under the golden.
- The data dictionary and the legacy layout note define the two timestamps as the earliest and the latest time the
  offence can have occurred. They settle the reading, which is deliberate (`Not semantics:`), and they say nothing
  about attributing an offence to a slot: asserted by the word sweep over every document for weight, share,
  duration, proportion, spread and attribution.

## Ask sheet

The main call's declared row population: the contracted classes' offence rows in the new records management export
for the two seasons, their `occurred_from`, `occurred_to`, class and location code, the contract and its tasking
schedule. The legacy export, the gazetteer, the address text column, the five-location register, the pedestrian
counts, the sensor availability log and the patrol's tasking plan are outside it (asserted by count: no contracted
offence row carries a device, no contracted row has a blank location code, and the main path opens none of those
files). Each ask is a measure the tasking paper carries anyway and the slate does not turn on (H18), and no two share
a primary device or a file path.

**Ask 1. The quarter's recorded offences of each class, each season (18 figures, nearest ten).**
- Use: the volume behind the slate, the first table of any tasking paper.
- Primary device (D1, a replay under fresh ids with the key kept): the move to the new records management system ran
  class by class, so for the fortnight of 14 to 27 July 2025 the three classes still held by the legacy system,
  assault without injury, public order and shoplifting, were written to both, each offence under its own crime
  reference in each. The occurrence details match; the references do not, so a union double counts those three
  classes and a de-duplication on the crime reference changes nothing.
- Hazard: the two systems name the classes differently (the crosswalk in the extract notes), so a concatenation
  yields twelve class labels for nine classes.
- Span (5 files, 11 columns): the two exports, the extract notes' crosswalk, the counting rules, the location
  register.
- Stops (each asserted outside the bin at the classes it touches): both exports unioned; de-duplicated on the crime
  reference; the legacy export dropped; the golden, de-duplicated on the occurrence key across the two exports.
- Realism: a phased migration by crime class, with a fortnight of parallel running, is what a force's own extract
  notes describe.

**Ask 2. The share of the quarter's recorded offences at each of its five locations, each season (10 figures, one
decimal).**
- Use: where in the quarter the offences sit, the paper's second table.
- Primary device (D7, the true key elsewhere): the legacy export carries a free-text address and no location code,
  so those rows reach a location only through the gazetteer, which lists two of the quarter's streets under two
  spellings; and the location register's Harbourgate Street range stops at number 178, so the addresses above it,
  which read as in the quarter, are not.
- Hazard: a share of the legacy rows have no address at all and are reachable only through the beat code.
- Span (5 files, 12 columns): the legacy export, the new export, the gazetteer, the location register, the beat map.
- Stops: grouped on the raw address string; the gazetteer applied with the out-of-range addresses kept; the blanks
  dropped; the golden.
- Realism: a gazetteer with spelling variants and a register whose street ranges stop mid-street is what a city
  address list looks like.

**Ask 3. Each pedestrian sensor's count per trading hour, each season (8 figures, nearest hundred).**
- Use: the quarter's footfall beside the offence volume, the paper's context table.
- Primary device (D4, a reporter drained down in stages): each sensor's outages are in a separate availability log
  and the counts file simply has no rows for those hours, so a count over the season's hours divides by hours the
  sensor was not counting; the outages differ by sensor and by season.
- Hazard: the counts file holds genuine zero rows for hours the quarter was closed, which a repair that treats
  missing and zero alike destroys.
- Span (4 files, 9 columns): the counts file, the availability log, the sensor register, the trading-hours schedule.
- Stops: the count over the season's hours; the count over the hours with rows; the count over the hours with
  non-zero rows; the golden, the count over the hours the availability log shows the sensor up.
- Realism: a footfall feed with gaps and an availability log beside it is how these sensors are reported.

**The cracker sheet.** The cracker landed the slate, ran the hygiene battery (crime references unique, no exact
duplicates, every join matched, no fan-out) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, offences by class and season (18) | both exports unioned, de-duplicated on the crime reference | the parallel fortnight wrote each offence under two references | miss |
| Ask 2, location shares (10) | the gazetteer applied to the address text, every row in the quarter kept | two spellings per street and the register's range stopping at 178 | miss |
| Ask 3, sensor counts per trading hour (8) | the season's counts over the season's trading hours | the hours each sensor was not counting | miss |
| The 42 cell figures and the covered total (43) | the aoristic weights, which is the call | scored with the recommendation and its critical components | outside |

The mirror sheet (stopped at the window start, rung 0) shares no slot name's figure and no device figure with the
golden; it keeps four of the eight slot names and no figure.

Mirror leakage: 0 per cent of the ask weight (four slot names, no figure).

**Pair arithmetic.** The construction layer is the 42 cell figures and the covered total, and they are graded with
the recommendation and its critical components, not in the ask weight: they are the decisive construction's own
output, so a response on any wrong basis misses all 43 and a response that lands the call takes them with it. That
leaves 36 graded ask figures, all of them device figures, and the cracker sheet above keeps none of them: C = 38 + 7
+ 55 x 0/36 = 45.0 for the cracker, S = 5 + 7 + 55 x 0/36 = 12.0 for the mirror, which keeps four slot names and no
figure. The margin over the bar is in the construction layer: the mirror loses the 42 cells as well as the slate.

Pair ceiling: 28.5

## Tried and rejected

- The seed's idle lane positions as the decisive limit (2026-10-12, at the draw): a per-airport cap that removes the
  natural pick and re-places it, strategies.md F3's dead form (58 v3 and v4).
- Lane capacity observed only while a queue stands, so passengers per lane-hour measures demand at quiet airports
  (2026-10-12, at the draw): task127's driver (a team's capacity visible only as the ceiling it held through a surge).
- Transfer passengers who never reach the landside checkpoint, so departing seats overstate the hub's summer demand
  (2026-10-12, at the draw): the share of a flight's passengers who pass the checkpoint is one ratio per route, and a
  bottom-up build calibrated to last summer's checkpoint counts at airport level already lands close to the call, so
  the decisive step is one enumerable correction.
- The release at only Cullinvale, Ardcarrig and Faranloe, four hosts releasing nothing (2026-10-12, at build): the
  default path kept 15 of the 24 airport-period figures and the averaged path 21, so a response off the call banked
  most of the airport figures; every host but Halloran Bay now stands down two lanes all day.
- Dromkeel as last summer's realised-effect leader (2026-10-12, at build): on the simulated 2026 feed Cullinvale's
  deep queues give it the largest realised effect (1.48 times Eskerford) under every demand Dromkeel's checkpoint
  clears by close; the lateral rung lands on rung 0's answer and the ladder runs three rungs.
- Asking for each airport's figure by period (2026-10-12, at build): 24 construction figures the cracker holds put the
  pair near 44; the prompt asks each airport's summer figure.
- Sinusoidal design days with flat banks (2026-10-12, stage 4): the leak reader read them as synthetic-smooth and the
  same shape at every airport; the design days now carry a late-morning wave, an afternoon lull, a thinning last hour,
  cresting banks and rough 15-minute noise.
- "How far the chosen airport's forecast passengers could fall short before another posting would move more"
  (2026-10-12, judge pass 1): read as the last whole per cent still ahead or the first behind; the prompt asks the
  smallest whole per cent shortfall at which another posting would move more.
- Taking the stand-down as the whole decisive step (2026-10-14, the hardening): the first architecture's single layer,
  shipped 10-12. The portal left it off the approved list, so the posted-day gap against the roster pattern is now
  rung 2 and the decisive step is the counterfactual arm: both sides of the comparison read from the lanes each
  checkpoint actually opens. Every figure moved; the call moved from Halloran Bay to Eskerford.
- The host stand-down measured against matched non-posted weeks, with the crowd-out as the difference (2026-10-14, at
  the hardening): the quiet-hour closures a matched-week design nets out never breach the standard, so the correction
  was worth nothing on the graded quantity (stumping Part 3, a rung measured on the graded figure). The same
  comparison against the checkpoint's own days moves the baseline arm, where it is worth 23 to 40 per cent of every
  airport's figure.
- A chronic shortfall across the whole rostered peak window (2026-10-14, at the hardening): two lanes short through
  Eskerford's plateau put its 2027 design-day waits over 95 minutes and left 58 of 78 simulated 2026 days with a
  queue at close, which no national agency would run a summer on. The shortfall now sits on the pattern's shoulders,
  which keeps the 2026 sensor's 99th percentile at 50 minutes.
- A shallow-breach world (the banks just above the pattern's capacity) to make the shortfall cheap in queue time
  (2026-10-14, at the hardening): with the plan barely breaching, the unit's three lanes fully relieve every
  checkpoint, so the stand-down stops biting and rung 2 collapses onto rung 0's answer; the ladder needs the banks
  deep enough for a two-lane stand-down to leave a residual.
- The whole hardening: the counterfactual arm read from the checkpoint's own days against its filed roster pattern
  (2026-10-14, judge pass 3): built, green on every free gate and 1.26 times clear on the call, and sent back on the
  architecture. The forward lanes are not filed, so both arms rest on an inference from last summer, and the
  difficulty is the refusal of an official artifact, which Gate G bans at any depth. The repair that would close the
  fork (filing the persistence, or naming the lane sensor record as the basis) is the one `/fix-determinism` forbids,
  because it turns the decisive step into rule application. The number re-roots at stage 1: the next draw needs a
  Layer 2 family that does not turn on a plan the records contradict.
- Architecture 1 as a whole, the airport posting world (2026-10-14, re-root): spent at judge pass 3 (Gate C, the
  forward lanes are not filed; Gate G, surface_read_rejection). Architecture 2 draws Criminology & Justice, where the
  deciding quantity is the weight a recorded offence's occurrence window puts on a patrol slot, so no filed artifact
  is refused and no forward fact has to be inferred from a past regularity: every offence's window is in the record
  and the estimand is defined over it.
- Estimand filed as the window-weighted count, 2026-10-15: it read as the tasking contract filing the share weighting, which would make the decisive step rule application under the client's rule 3. Refiled as the unobserved count the contract defines, with the weighting attributed to the records' structure and the word sweep asserting no document states one.
