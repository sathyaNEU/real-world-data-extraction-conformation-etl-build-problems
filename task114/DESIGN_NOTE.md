# task114 design note

Business & Operations Analytics (facilities and workplace) x Descriptive & Distribution Analysis.
Drawn 2026-10-08.

## DRAW

| Dimension | Draw | Against the last three (task110, task111, task109) |
|---|---|---|
| Domain / subdomain | business-operations-analytics / facilities-workplace | subdomain never drawn; 109 and 111 were back-office and field service |
| Niche | the meeting-room count for the one new office of a consultancy formed by merging two firms, replayed from both legacy offices' reference-year meetings | first workplace world in the corpus |
| Objective | descriptive-distribution (author's pairing, never built) | 109 ETL, 110 ETL, 111 RCA |
| Shape | 04 setting one dial (the room count, with days short stated at every allowed count) | 109 was 14, 111 was 18 |
| Decision type / unit | dial_setting / count of rooms | |
| Gap | time (decisive), population | 109 population, 110 population, 111 time |
| Pattern / generators | A, off-chain form (how a site layout treats a meeting decides whether it takes a room, and the decision buys a different layout), D below it; G6, G2, G10 | 109 B, 110 B, 111 G5 |
| Gate G mechanism | method_or_model_selection: two replay bases, room bookings or meetings on one floor, the right one pinned by a booking practice the records keep without exception | |
| Calibration form | prior_period_close_out: each office's quarterly utilisation close-outs for the reference year | 109 certified_matrix, 110 parallel_run_overlap, 111 gold_standard_subsample |
| Context artifact | capacity_report: the quarterly workplace utilisation reports | 109 filed_standard, 110 register, 111 operations_log |
| Stakeholder / family | workplace planning lead at the merged firm / capacity_planner | 109 operations_director, 110 compliance_or_audit, 111 field_unit_lead |
| Forum / forcing event / org family | the fit-out architect (customer_or_counterparty) / the room schedule frozen into the design-and-build contract (purchase_order_or_contract) / professional_services | 109 regulator, filing, 3PL; 110 executive, cutover, hospital; 111 operations desk, peak, other |
| World | Toronto, CAD; an engineering and planning consultancy formed by an April 2025 merger, two downtown offices moving into one office in mid-2027 | 109 Poland, 110 Australia, 111 Scotland |
| Spine | the calendar extract, one invitee on one meeting (meeting x invitee), synthetic | |

## Litmus and flags

The task overturns no reported number and no stakeholder conclusion: every room booking, every badge
entry and every quarterly utilisation figure is correct for the office it describes, and nobody in the
pack claims a room count. The difficulty is that the decision buys a layout the records never saw.

- `surface_read_dependency: no`
- `stumping_family: analytical_non_defect`
- `sole_data_defect: no`. Repair every file to perfection and the two offices' records still describe two
  offices; the new office's room demand is a replay no instrument could have observed.

**Why the forward window is not a forecast.** Nothing is estimated and no rate is carried forward: the
reference year's meetings are replayed on one floor under the booking practice the records show, and the
dial is read off that replay, which is what shape 04 calls a replay rather than a forecast.

## Decisive rung, from the measured catalogue

Measured trap 13, *validates on one population, applies to another*: the booking-based basis fits every
closed figure exactly (each office's quarterly reports) and is applied to a layout that differs on one
axis, whether a meeting's attendees share a site. Trap 2, *counts file rows instead of the real unit*,
carries the rung below it (two room bookings in two offices are one meeting on one floor).

**L1 sentence.** In every closed quarter, a meeting whose attendees sat in different offices used no
room, because no two of its attendees were in the same building; on one floor those attendees are
together, and every reference-year meeting with two or more attendees in the same office that day had a
room there.

**Corpus direction.** Under the naive path (both offices' room bookings on one timeline) the calibration
organ reproduces: every quarterly peak, room-hours and utilisation figure for both offices ties exactly.

## Stump sentence

A competent solver builds the booking pipeline that reproduces every busiest moment in both offices'
quarterly close-outs, puts both offices' meeting-room bookings on one timeline, sets the solo calls aside for
the booths, takes each working day's peak and files **24 rooms**, the fewest short on no more than twelve
working days; the step that lands it there is never asking which meetings booked no room only because their
people were in different offices that day (9,144 of them), when on one floor every meeting with two or more of
its people in takes a room, as the records show without exception wherever two of a meeting's people were in
the same office.

## Exemplars read

- *Adopt the arrival-based 2026 cover schedule with GMR at 50,670 minutes at p90* (mean 0.13): a dial cut
  from a rebuilt distribution; the model kept the row grain the layout invited.
- *Report 11,667 stalls traded at member markets* (mean 0.21): the unit of demand is not the record's grain
  (neighbouring lettings form one stall); the model counted rows.

What transfers is the shape of the miss (the record's own grain taken for the unit, a basis that fits every
closed figure), not the architecture: neither published-control reproduction nor a recovered unit rule
carries this build's decisive rung.

## Guard

`guard.py check`: one BLOCK on first pass, cleared by differentiation; WARN `repeat.gate_g`
(method_or_model_selection, task109). Answer: task109's selection is between two compilation rules a
control set arbitrates; here it is between two replay bases, and no control set can arbitrate it.

- Differentiation, task33: task33 truncates a measured elevation at a filed future intervention and picks
  one of eleven series by forward yield; this build adds demand a two-site layout never put on the
  resource and reads a capacity dial off a replay, so no series is projected and nothing is truncated.

## ENTITY, UNIT, DECISION

A Toronto engineering and planning consultancy formed by an April 2025 merger runs two downtown offices
(legacy firm A at the Adelaide Street office, legacy firm B at the Front Street office) and moves both into
one new office in mid-2027. The workplace planning lead owes the fit-out architect one number before the
design freeze: the meeting rooms the new office is built with.

Two quantities both read as "room demand": **room bookings** (what each office's platform held, which is
exact and is what every quarterly report counts) and **meetings that need a room** (two or more of a
meeting's attendees in the same building that day, which on two sites is the bookings and on one floor
is not). They part company only on meetings whose attendees were split between the offices.

**Decision.** The lowest room count at which, had the new office been running through the reference year
(1 October 2025 to 30 September 2026), it would have run short of meeting rooms on no more than twelve
working days. Shape 04: one dial, the outcome (days short) at every setting, the committed setting and
the one below it falling short. The committed figure is p13, the thirteenth-highest daily peak, which the
rule makes the unique answer (if p12 = p13 = p14 the rule still lands on p13; no tie can move it).

## LADDER (main call)

Readings off the shipped pack. The generator asserts each one; `verify_pack.py` recomputes R3 and R2 on a
code path that shares nothing with the generator.

| Rung | The competent pipeline | Count | Killed by |
|---|---|---|---|
| R0 | each office sized on its own meeting-room bookings (solo calls aside), the two counts added | 28 (15 + 13) | the offices' busiest moments do not coincide, and the split meetings are still missing |
| R1 | both offices' bookings on one local timeline, solo bookings kept | 29 | the brief: calls taken alone go to the booths |
| R2 | R1 with solo bookings set aside (the natural competent stop) | 24 | never asks which meetings need a room once both offices share a floor |
| R2b | R2 with paired bookings (one meeting holding a room in each office) merged | 23 | merges the split meetings that booked twice, never adds the 9,144 that booked nothing |
| R3 | **every internal meeting with two or more non-declined invitees badged into either office that day, one room each** | **31** | the answer |

At 31 rooms the replay runs short on 7 working days, at 30 on 14 (the brief allows twelve). Seven days sit at
exactly 31, so no single design day is graded. 27,607 meetings need a room on the one floor.

*A solver who does everything right up to R2 commits to 24*, 22.6 per cent under the answer. Satisfying to
stop at: the booking pipeline under it reproduces all sixteen published busiest moments, it follows the
brief's booth rule, and pooling the two offices on one timeline is the obvious consolidation step.

Sign discipline: the corrections below R3 walk the figure down (pooling, booths, merging) and the decisive
move turns it up by 29 per cent. The answer is the extreme of the reasonable cells (L5, asserted).

**Fork grid (C4, every cell asserted).** Separation floor 8 per cent for any cell one defensible reading
reaches.

| Cell | Count | Off the answer | Class |
|---|---|---|---|
| accepted and organiser only | 25 | -19.4% | defensible, clears the floor; the pin refutes it (4,151 exceptions) |
| accepted, tentative and organiser | 28 | -9.7% | defensible, clears; the pin refutes it (2,033) |
| tentative dropped, no response kept | 28 | -9.7% | defensible, clears; the pin refutes it (2,090) |
| optional invitees ignored | 28 | -9.7% | defensible, clears; the pin refutes it (2,115) |
| declined invitees counted | 35 | +12.9% | defensible, clears; the pin refutes it (3,904) |
| R0, offices sized apart and added | 28 | -9.7% | defensible, clears |
| R2, R2b | 24, 23 | -22.6%, -25.8% | the ladder |
| presence ignored | 59 | +90% | refuted by the badge records |
| solo bookings added to the replay | 34 | +9.7% | violates the brief (booths) |
| one person counts | 60 | | violates the brief (booths) |
| client meetings kept | 32 | +3.2% | violates the brief (client suite) |
| closed intervals | 41 | | violates the close-outs' method; breaks all sixteen busiest moments |
| cancelled items kept | 31 | 0 | converges |
| bookings plus split meetings, pairs not merged | 31 | 0 | converges |

Survival properties of R3: (1) no shipped sentence states that split meetings take a room on one floor;
(2) the close-outs are blind to it (each covers one office); (3) no arithmetic symptom, every booking total
ties; (4) not a per-row predicate, it needs each meeting's invitees joined to two badge systems through the
directory; (5) enumeration is arithmetic over 113,174 meetings; (6) no cutover date in the reference year;
(7) delete every wrong number and nothing changes, because nothing in the pack is wrong.

## ORGANS

- **Calibration (prior_period_close_out).** Each office's quarterly room pressure close-out: bookable meeting
  rooms and client rooms at quarter start, and the busiest moment (rooms in use and its date) on the all-rooms
  scope, each room under its type on the day. The method sheet states the conventions once (held to the end or
  to release; a booking holding more than one room counts each room once; each occurrence at the time it took
  place; cancelled and declined not counted; Toronto local; half-open). The booking pipeline reproduces all
  sixteen busiest moments only under those conventions, which certifies R1 and R2 (L7) without publishing a
  graded figure. Blind to R3 for a structural reason (L1): each close-out covers one office. Blind to the ask
  devices by construction: every cell reads the same on the legacy reading as on the correct one (asserted, and
  recomputed in verify_pack.py).
- **Empirical pin for R3.** Of 113,174 internal meetings, 18,463 had two or more non-declined invitees badged
  into one office that day, and every one has a room booking in that office (Adelaide by Outlook event id,
  Front Street by iCal UID and local start, tentative holds included). Every confirmed Adelaide booking for an
  item with two or more people of the firm on it had two in, and so did every Front Street booking for one (an
  outside party on a call's invite is on the line, not in the room); every released one (439) had fewer
  than two. Tested both ways, accepted-only counting breaks the pattern 4,151 times, counting declined
  invitees 3,904, dropping tentative responders 2,090, dropping no-responses 2,033 and ignoring optional
  invitees 2,115, which pins the response and invitee-type reading (C2). 3,697
  meetings between people of the two legacy offices booked a room on days two of them shared an office (the
  free training instance, O3).
- **Twin days.** 21 October 2025 and 2 April 2026: identical booked peaks (Adelaide 10, Front Street 10, both
  on one timeline 19), one-floor peaks 31 and 25, so no scaling of the booking peak reproduces the replay.
- **Filed pins (new_office_brief_stage2.pdf, Rev C).** The twelve-day rule; meeting rooms exclude the client
  suite, the town hall space and the booths; calls taken alone go to the booths, client meetings to the
  client suite, town halls to the town hall space; Adelaide's booking platform and room practices carry over.
  Stated once each, never argued.
- **Social layer (RE_meeting_room_number.eml).** Beliefs about the past only: a partner's view that either
  office has more empty rooms than full ones mid-morning, and the Front Street office manager's view that its
  rooms are busiest on Tuesday and Wednesday mornings and the Forum is only booked for town halls. All three
  are true and asserted; no voice endorses a basis or states a count.

## 22-AXIS CLOSURE (main call; asks in the ledger)

| # | Axis | Reading | Closed by |
|---|---|---|---|
| 1 | Population | internal calendar meetings, not cancelled, not all-day, not client-suite or event-space, two or more present | C1 (the filters select the same rows under every reasonable order) plus the brief |
| 2 | Unit of account | one meeting, one room | the brief (a meeting needs one room); C1 on cross-office pairs |
| 3 | Attribution window | the meeting's own local date | C1 (no meeting crosses midnight) |
| 4 | As-of dating | presence that day; directory as at each date (leavers, joiners) | C1 (no badge after a leaver's end date, none before a start) |
| 5 | Version basis | the event as it occurred (moved occurrences at their new time in the calendar extract) | C1 (the extract carries occurrences, not patterns) |
| 6 | Denominator | none graded | n/a |
| 7 | Weighting | none | n/a |
| 8 | Window length | the full reference year | filed (brief), and stated in the prompt by both dates |
| 9 | Boundary inclusivity | half-open meeting intervals; "more than R" short | C2 (quarterly peaks reproduce only half-open) and the brief's wording |
| 10 | Rounding path | integers throughout | n/a |
| 11 | Tie-break | p13 under ties | the rule's own arithmetic (proved above) |
| 12 | Maturity | the year is closed | n/a |
| 13 | Order of operations | filter then count | C1 |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one person-day per person whatever the swipes | C1 (multiple swipes collapse) |
| 16 | Identity normalisation | card numbers to people through the directory; UPN case | C1 (asserted unique mapping) |
| 17 | Netting | none | n/a |
| 18 | Units | minutes | n/a |
| 19 | Status semantics | response codes: declined out, the rest in | C2 (the pin holds only on this reading) |
| 20 | Integerisation | none | n/a |
| 21 | Scope of a clause | the twelve-day rule governs the whole year's working days | filed (brief), and stated in the prompt in the brief's own sense |
| 22 | Forward window contents | the reference year replayed on one floor | the brief (size on the reference year) plus the pin |

## ASK SHEET (rebuilt after the portal runs of 9 and 10 October 2026; prompt wording unchanged)

**Main call's declared row population.** Calendar events (internal, not cancelled, not all-day, not client
meetings or town halls) with two or more internal invitees, their attendee rows, staff access events at both
offices joined through the directory, the firm calendar's working days. Frozen in the generator: 31, 7, 14, 27,607,
9,144, the design day and a hash of all 246 daily peaks are asserted on every build. No device row enters it: the
cancelled standing calls are cancelled items, the moved standing calls carry one person, the added and re-timed
client meetings are Client meeting items, the calls with an outside party carry one person of the firm and their
guests map to no employee (all asserted), and the main call reads no booking export.

**Recommendation block (inheriting, kept narrow).** The committed count; the working days short at that count
(7) and at one room fewer (14); today's two offices' meeting rooms combined (61).

**Ask A, today's two offices (decoupled, device-carried; H18: the reconciliation of the committed count to
today's provision and use).** For each office and quarter: meeting-room hours held, the part of them one person
booked for a call, and the most meeting rooms in use at once; for each office: bookable meeting rooms on 30
September 2026 and the rooms its own bookings would have justified under the brief. 28 figures; the generated
rubric grades each office's four quarters as one criterion per measure, so ten criteria, the room count at 7 points
and the hours and call hours at 4 each. Portal run 1 came back at 62 with every one of them filed right; run 2, on
the first rebuilt layer, at 57, which fits a response reading every representation device right and losing only the
room counts; run 3, with S1 and the 15-hour floors, at 54 for both top responses, which passed both room counts and
Adelaide's hours and call hours: every Adelaide device and C1 read right, Front Street's fold read wrong. The layer
now carries three insight devices beside four representation devices, G1 carrying both room counts and every
call-hours figure, and every device misses each hours figure it moves by 15 hours or more. The old devices stay as
hazards (shadow rows, release at fifteen minutes, Outlook headcount, attendee_count with the room, same-room series
rows, tentative holds, dated room types, declined and cancelled rows).

| Device | Family | Where | Narrow path, and what it moves (least miss) | Pinned by |
|---|---|---|---|---|
| A1 a checked-in booking given back early at the panel: status stays Confirmed, released_at carries the time (1,027 bookings, 309 of them calls) | D5, silent | Adelaide export | release keyed on status: every quarter's hours and call hours, peaks Q1, Q2, Q4 (22.3 hours) | method sheet (held to the end or to the time the platform released it); notes (released_at is when the platform gave the room back) |
| A2 from the platform upgrade on 19 May 2026 a combined booking is one row, with no half rows (53 bookings) | D2, silent switch | Adelaide export | combined rows dropped, half rows kept: Q3 and Q4 hours (34.7 hours) | method sheet (each room it holds, once); register's Combinable With |
| F1 a cancelled occurrence of a series is an exception, and the series row stays at its slot (rows left by 90 cancelled meeting occurrences and by 176 of the 617 standing calls cancelled on days their owner was out) | D2, silent | Front Street export, calendar | cancelled rows filtered before the fold: every quarter's hours and call hours (17.5 hours) | notes (is_exception, original_start_utc); method sheet (each occurrence at the time it took place; cancelled not counted) |
| F2 a moved occurrence's series row stays in the series' usual room (221 in another room, 175 of them standing calls moved later that day; 63 in the same room) | D7, silent | Front Street export | the fold keyed on the room: hours, call hours, peaks Q2 to Q4 (18.0 hours) | as F1 |
| S1 a focus block held in a meeting room (308): one person booked the room, as for a call, but the calendar item is a Focus time block, offline | insight | both exports, calendar | every one-person booking read as a call: every quarter's call hours (62.0 hours) | the prompt (hours one person booked for a call); the calendar's subject and online flag |
| C1 client meetings held in a meeting room when the client suite was full (91, 11 of them on the days that set the room count) | insight | both exports, calendar | left in the room count: Adelaide 16 against 15, Front Street 14 against 13 | the brief (client meetings to the client suite); the calendar's Client meeting category |
| G1 a call with someone outside the firm on the line: one person of the firm on an online, uncategorised single item with one or two guests, named for the call and never "Call" (383 items; 196 Adelaide bookings with headcount 2 or 3, the booker counting the person on the line; 187 Front Street with attendee_count 3 or 4; 17 across the busiest minute of the days that set the room counts, 7 of them booked into a free room) | insight, silent | both exports, calendar | people read from the headcount: Adelaide 16 against 15, Front Street 14 against 13, every quarter's call hours at both offices (23.9 hours) | the brief (a call taken by one person goes to the booths); the notes (addresses outside harrowfield.ca are guests); the calendar's attendees and online flag |

S1 is closed both ways: every offline Focus time item and every online Call item is told apart on the calendar, the
rule (a one-person booking is a call unless its item is a focus block; an Adelaide app or kiosk booking has no item)
covers every one-person row with no exception, and the room count is the same with the focus blocks counted in it
(asserted), so the device moves the call hours and nothing else. Directions are checked on every composed reading:
A1 and A2 push Adelaide hours opposite ways, and the give-back rate is set so that the legacy reading still misses
every quarter by 20 hours or more.

G1 is closed both ways. Every item with a guest that is no client meeting carries one person of the firm and is
online and uncategorised, so on the room count the booking is out whether it is read as a booth call or as a client
meeting, and on the call hours it is an online call one person took in a room. The one-person rule becomes one person
of the firm on the booking's calendar item, a client meeting aside (an Adelaide app or kiosk booking has no item and
its headcount says), which on every other row reads exactly as headcount 1 and attendee_count 2 did (asserted). It
blends: 2.2 per cent of Adelaide's confirmed headcount-2 bookings and 4.6 per cent of Front Street's attendee_count-3
holds. Partial catches miss the same ten figures: a call told by a subject that is Call, or that says call (85 of
the 383 do, none of the 17 at the threshold), each call-hours figure by 15 hours or more. Composition: with people
read from the headcount, no other mishandling (A1, A2, C1 at Adelaide; F1, F2, tentative rows dropped, C1 at Front
Street) lands either count on the answer, which took lifting three days beyond the thirteen the rule needs. The
booking rung stays 24 for a headcount reader, and the own-count readings (Adelaide 15 or 16, Front Street 13 or 14)
never add to 31. The seven calls booked into free rooms are all at Adelaide Street, and taking them out moves no
busiest moment, no close-out and neither room count (asserted); they add only hours and call hours.

**The referee kept blind.** Each quarter's close-out busiest moment, value and date, is identical on the correct
and the legacy reading. Where a meeting-room peak sat on that moment, client meetings on the peak minute were
re-timed (8) or an ordinary client meeting earlier in the quarter took the busiest moment first (7). Peaks move in
six of eight office-quarters; Adelaide Q3 (23 rooms on 13 May, an outlier no earlier moment can be brought up to)
and Front Street Q1 (no standing call held across its 14:00 peak) are left as they are.

**Chart (series inheriting, one line decoupled).** The new office's busiest moment on every working day,
highest first, the committed count and today's 61 rooms as labelled lines, the 7 days above the count marked,
a title carrying the call. Byte-identical to the build the portal graded.

**Pair arithmetic (one criterion per office and measure, the quarters together; room count 7, hours 4 and call
hours 4 read off the run 3 rubric, busiest moment and rooms on 30 September taken at 4).** `generator/pairsim.py` on
the shipped bundle, ask points kept of 46: the legacy reading 8; give-backs read 12; every Adelaide device 27; every
Front Street device 27; every representation device handled with the focus blocks read as calls and the client
meetings kept 24; everything but the focus blocks 38; everything but the client meetings 32; everything but the calls
with an outside party 24, and the same with a call told by its subject; the run 3 kind of solver (Adelaide right,
Front Street's fold keyed on the room, people from the headcount) 16, against 34 for the same solver reading the
one-person rule right; everything 46. The pass condition rests first on the main ladder keeping both top responses off the call, then on
the three insight devices, G1 taking 18 of the run 3 solver's points (both room counts, Adelaide's call hours) and
Front Street's call hours from any solver that reads its fold right.

## PACK PLAN

| File | Role | Main path | Ask A path |
|---|---|---|---|
| calendar_events_fy2026.parquet | operating extract (IT's licence-review pull), one row per occurrence | yes | the Client meeting category (C1), Focus time items (S1), the online flag on a call with a guest (G1) |
| calendar_attendees_fy2026.csv | spine, one recipient on one item (348,587 rows) | yes | the guests on a call's invite (G1) |
| adelaide_access_events_fy2026.csv | operating extract, Adelaide card readers | yes | no |
| front_st_door_events_fy2026.csv | operating extract, Front Street door controller | yes | no |
| staff_directory_fy2026.xlsx | dimension: every employee in the year, both card ids, legacy firm, leavers | yes | no |
| firm_calendar_fy2026.csv | dimension: working days, holidays, the Christmas closure | yes | yes |
| room_register.xlsx | dimension: Rooms (as exported 1 October 2026) and the dated Changes log | no | yes |
| adelaide_room_bookings_fy2026.csv | operating extract, Adelaide booking platform | no | yes |
| front_st_room_calendar_export.csv | operating extract, Front Street room mailboxes (UTC) | no | yes |
| room_utilisation_close_outs_fy2026.xlsx | context artifact and calibration: quarterly room pressure close-outs, method sheet | no | referee |
| new_office_brief_stage2.pdf | governing document: the twelve-day rule, booths, client suite, town hall space, platform carries over | yes | yes |
| extract_notes.md | dictionary and provenance | yes | yes |
| RE_meeting_room_number.eml | social layer | no | no |

**Oracle discipline.** The close-outs publish rooms at quarter start and the busiest moment on the all-rooms
scope, never hours, so they certify the booking conventions without handing over any Ask A figure. Rooms at
quarter start are not the 30 September count at either office (Adelaide loses AD-6.05 on 31 August, Front
Street gains FR-4.06 on 14 September), and the Rooms sheet as exported already carries two changes dated 1
October 2026, so neither the Q4 close-out nor the register as it stands is copyable.

## Leak review (leak.py, as of 2026-10-08; rerun 2026-10-10 after G1, the same five lines and no new one)

- Sweep 3, extract_notes.md ("new", "office", "meeting", "rooms"): the title and the field notes name the
  subject of the folder; no count appears.
- Sweep 3, new_office_brief_stage2.pdf (the same words): the brief is about the new office's meeting rooms; its
  numbers are its own (410 workstations, 28 booths, 160 seats, six client rooms, room sizes, dates), never 31.
- Sweep 4, extract_notes.md (booking, close-outs, register, tentative, optional): field values and the files it
  registers; no sentence names a reading or a convention.
- Sweep 4, new_office_brief_stage2.pdf (booking, meetings, client): the brief's rule and its booth, client
  suite and platform lines, the filed pins; none says which meetings take a room on one floor.
- Sweep 8, front_st_room_calendar_export.csv (True and False): what an Exchange export through PowerShell
  writes; the notes spell the value the same way.

## Tried and rejected

- Published control set plus reproduction gate (measured traps 1, 3, 4, the top architecture): decisive
  pattern B is banned against task109 and task110, and task109 has just spent that architecture on
  percentile standards.
- Sales development, the lead-score cutoff or the SDR stage of a funnel, with added capacity working the
  lowest-ranked leads of each day's queue: the stump lives in a marginal conversion rate for leads never
  worked, which is an estimate applied forward, so the build reads as Opportunity Sizing or Experiment, not
  a replay; stripping the value side to keep a replay removes the trap.
- Desks for a consolidated floor, shift teams sharing desks across non-overlapping shifts (daily unique
  against peak concurrent): single_conceptual_flip, the same people on the same day under two lenses. Kept
  available as a lower rung only.
- Desks, the moving population taken from where people sit rather than from the move plan's cost centres:
  a forward population named by a filed clause (task100 v1); whichever the move plan names, the solver
  builds.
- Desks, re-laying each team's attendance on the 2027 anchor-day plan: a forward window whose every input
  is filed, so it is the solver's first simulation (task55).
- Desks, team neighbourhoods that cannot lend desks (sum of per-team peaks against the pooled peak):
  determinism rests on how the standard words the bar, and booking data from a floor with spare desks
  cannot show a restriction that never bound.
- Meeting rooms, a fifteen-minute reset held after every booking (booked plus reset concurrency): the reset
  is invisible in the booking records and inferred from gaps, a recovery of what the instrument did not
  record (task89 v6), and a per-room gap check surfaces it.
- Cross-office paired bookings merged into one meeting as the decisive rung: the driver reads as task98
  v7 (two separately keyed lists, an overlap subset counted twice, every closed sum exact). Kept as the
  rung below the decisive one, where it moves the count the other way.
- Two teams on alternating in-office weeks, one on a fourteen-day booking cycle and one on even ISO weeks,
  falling into step after ISO week 53 of 2026: the decisive move projects schedules onto 2027, a forecast
  under any reviewer's reading, against the author's Descriptive pairing.
- Absence trigger points (Bradford scores) for 2027: the committed figure is the output of a filed formula,
  dead shape (task67).
- First card label population / D / method_or_model_selection: `test.same_driver_older` reports the
  signature spent in seven earlier builds. The move is honestly a time gap (the records describe two
  offices, the decision buys one), so the card carries time / A first.
- UTC timestamps in the Front Street export as an Ask A device: inert, because every booking sits between
  08:00 and 18:30 local, so no UTC date differs from its local date and a uniform shift leaves every
  concurrency and every hour unchanged. Kept as a hazard only.
- Room register history shipped as one row per room per spell: the repeated room codes fan out on any join,
  which turned the as-of device into a visible work order. Replaced by the current Rooms sheet and a dated
  Changes log.
- Close-outs publishing booked hours and utilisation for each office and quarter: on the all-rooms scope they
  differ from Ask A's meeting-room hours only by the client rooms, so a solver backs every device out of them.
  Cut to rooms at quarter start and the busiest moment.
- Ask A at twenty figures (hours, busiest moment, rooms, own count) with ghost rows only in pattern slots
  nobody reused: pair simulation put the battery profile at 0.46 and the thorough profile at 0.79. Added the
  calls' hours with their two solo readings, standing calls, mid-morning moved occurrences, tentative holds on
  the approval-only rooms and two register changes dated 1 October 2026; 0.29 and 0.64.
- Monday and Friday attendance raised to 0.14 and 0.16 to thicken the year's tail: the count landed on a knife
  edge or a round thirty. Kept at 0.10.
- Ad hoc meetings at 2.0 a person-week: the count landed on 30, a round value. 2.1 gives 31.
- Declined invitees at the earlier response mix: the declined-counted cell sat at 33 against 31, under the
  floor. Declines at 20 per cent put it at 35.
- Client meetings left in the replay as a defensible cell: 32, inside the floor, so the cell is classed a
  filed-rule violation (the brief sends client meetings to the client suite).
- A close-out footer saying the close-outs do not size the new office: the author's voice steering the solver
  off a file. Replaced by a neutral compile line.
- Invitee responses at 65 per cent accepted, 7 tentative, 8 no response and 6 per cent optional invitees: the
  readings that drop tentative responders or ignore optional invitees landed on 29, 6.5 per cent off the
  answer and under the floor. Relabelled to 60, 10 and 10 with 13 per cent optional (labels only: the booking
  rule reads declines alone, so the count and every Ask A figure stay put); both readings now land on 28.
- Sizing rule carried only in new_office_brief_stage2.pdf, the prompt silent on it: the portal's prompt
  check P6 reads the prompt without the input files and failed both prompt versions as a room count with no
  sizing criterion. The prompt now states the twelve-day rule and the window, attributed to the brief; the
  booths, the client suite and the town hall space stay in the brief only, and nothing about which meetings
  take a room is stated.
- The first ask layer (shadow rows, release at fifteen minutes, Outlook headcount, attendee_count with the room,
  same-room series rows, tentative holds, dated room types, declined and cancelled rows): the portal run of 9
  October 2026 scored 62 with every Ask A figure filed right, because each device's rule was stated outright in the
  method sheet or the notes and the close-outs let a solver check its conventions against all sixteen busiest
  moments. Kept as hazards; the rebuilt devices sit on narrow implementations the close-outs cannot tell apart.
- Re-timing every client meeting (one office in the mornings, the other in the afternoons) to pull the all-rooms
  busiest moment off the meeting-room peak: decoupled at most five of eight quarters and reads staged. Replaced by
  re-timing only the client meetings on a peak minute and, where needed, one ordinary client meeting earlier in the
  quarter.
- The platform upgrade on any date before 13 May 2026: a combined booking sits on Adelaide Q3's busiest moment, so
  dropping it moved the published close-out, and no earlier moment could be brought up to 25. Moved to 19 May.
- Cancelled standing calls as the Front Street peak device: on peak days the callers are in and their rooms are
  taken, so no slot qualified. Replaced by moving a present caller's call later into another room, which leaves
  its series row on the peak.
- Client meetings in meeting rooms pushed against the legacy room count: the legacy count moved, but with every
  other device read right the client meetings alone moved nothing. Pushed against that reading instead.
- Peaks at Adelaide Q3 and Front Street Q1: no construction moves them with the close-outs left identical; left
  untrapped (4 points).
- A given-back combined booking from before the upgrade carrying its release on its own row only, with the half
  rows left at the booked end: no shipped document says which row governs when the two disagree, so it was a
  determinism exposure for about two points. The half rows carry the release like the booking.
- The first rebuilt layer (A1 at 2 per cent, A2, F1, F2 and C1): portal run 2 scored 57, which fits a response
  reading every representation device right and losing only the room counts, and the misses were small (about 5
  call hours a quarter on A1). Representation devices are caught by general code whatever their size, so the layer
  gained S1, an insight device on the call hours, and every device a 15-hour floor on each figure it moves.
- A1 at 4 per cent of meetings: at Adelaide Q4 the give-backs (+72 hours on the legacy reading) and the dropped
  combined bookings (-68) cancelled to +2.4. Raised to 7 per cent, so the legacy reading misses by 20 hours or more.
- Lifting the C1 room count only through client meetings already on a threshold day: after the rate change it
  stalled one day short at Adelaide, where no client meeting touched the remaining days' peaks; one ordinary client
  meeting was booked into a free meeting room across a threshold day instead.
- Town hall overflow rooms booked in meeting rooms as a second room-count device beside G1: caught by the same
  category filter that catches C1, and lifting the town hall days at noon pushes the meeting-room peaks onto them.
- Guests put on internal meetings as G1's over-cleaning half (so that "a guest makes it a client meeting" loses):
  device rows inside the main call's population, and it opens a reading of the main call that drops meetings with a
  guest. Left without; the category is the only client marker the pack carries.
- Meeting bookings whose headcount was updated to one at check-in: moves the room count down, opposite to G1 and C1,
  so a solver missing both lands back on the answer, and the S1 subject check finds it.
- A distribution list counted as one recipient in Front Street's attendee_count: the same opposite-direction
  cancellation, and the attendee file would have to carry the list expanded.
- Outlook bookings missing from the Adelaide export for a connector outage, the calendar's rooms carrying them: no
  shipped clause makes the calendar the record of a hold, so Adelaide's hours read two ways, and the R3 pin breaks on
  the missing bookings.
- Weekend and closure-day holds on Adelaide's hours: "the hours their meeting rooms were held, quarter by quarter"
  admits both every day and working days only.
- A room code reissued at the platform upgrade, for Adelaide's hours: the Changes log carries both spells, so a
  solver who builds spells from it lands right, and it moves the room count against G1. Adelaide's hold hours keep
  their two representation devices (A1, A2) and get no third.
- G1 lifted on exactly the thirteen days the rule needs: dropping post-upgrade combined bookings at Adelaide, or
  tentative holds at Front Street, as well took the count back to the answer (one day each). Lifted three days beyond.
- G1 subjects all "Call": a subject rule catches every one for free; subjects are named for the call and the
  threshold rows never say call.
- G1 subjects naming the counterparty ("Metrolinx coordination"): a real organisation's name in the calendar's
  subjects (house fix H21). Subjects name the call alone ("Design review", "Client call").
