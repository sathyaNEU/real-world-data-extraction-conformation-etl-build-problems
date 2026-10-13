# task232 design note

A regional local health district in northern New South Wales, on the Queensland border. Its public health unit acts
on every laboratory notification of shigellosis, Shiga toxin-producing E. coli (STEC) infection or cryptosporidiosis in
a child attending, or an educator working at, a long day care centre while infectious: it calls the family and the
centre and excludes the case, and it investigates the case's room. On 1 December 2026 release 4.2 of the state's
Notifiable Conditions Platform (NCP) gives each pathology laboratory's electronic notification feed its own SLA alert:
a report that reaches the platform later than the feed's SLA lateness after the laboratory authorised it pages the
on-call public health officer. The unit's standard CD-ST-07 sets each feed's lateness from the allowed settings (1, 2,
4, 6, 8, 12 and 24 hours) by the secondary cases a year that lateness would let a notified case cause in their
childcare room before exclusion, priced at each condition's secondary transmission per child-hour of contact estimated
from the unit's closed childcare investigations. As of the extract (13 November 2026, request 16 November 2026).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task232.json`, architecture v1, drawn 2026-10-13. Epidemiology & Public
  Health (client domain), task type `disease-surveillance-outbreak-anomaly-detection`, objective Data Quality
  Monitoring & Alerting (the object is each laboratory feed's timeliness, the call is the lateness its SLA alert pages
  at). Shape `other`: a dial per laboratory, each feed's lateness and the expected secondary cases a year at that
  setting and at the next longer one. Decision `dial_setting`, question form how-many. Gap time then population; no A
  to E pattern, decisive generator G4 (attribution at the exclusion transition), then G13 (an illness dated days after
  the exposure that caused it). Gate G `decomposition_attribution`: the room's illnesses are split between the index's
  own secondary cases and everything else. Strategy `decomposition_attribution`. No calibration organ. Context
  artifact `operations_log` (the platform's interface incident log). Stakeholder: the manager of the unit's
  communicable disease surveillance team (`field_unit_lead`), deciding with the team and the unit's director
  (`line_manager_or_team`) ahead of the platform release (`cutover_or_migration`), in a local health district
  (`hospital_or_health_provider`).
- **Seed:** DQ05 (an upstream-lag threshold for a feed SLA alert, with the lag measured with error), kept as an idea
  seed only: upstream data feeds, a lateness threshold per feed for its SLA alert, and the downstream cost of
  lateness. The seed's pitfall (a covariate measured with error attenuates the slope of downstream error on lag) is a
  general-statistics method; set in any feed world it reads the same with another field's nouns, the backdrop the
  author's domain review returns (task229 v3's record), and it sits next to task228's measurement-error separation.
  The pitfall is re-found in outbreak epidemiology: the downstream cost of a laboratory's lateness is the secondary
  cases an infectious child causes before exclusion, and the transmission that prices it has to be read from closed
  investigations whose illnesses fall days after the exposure that caused them.
- **Data-native sentence:** enteric secondary cases fall ill between half a day and twelve days after the childcare
  day that infected them, and a room investigation's follow-up also records the children and educators who were ill
  before the index case was infectious (the index's own source and co-primary cases), community cases and the cases
  secondary cases went on to cause or a later introduction brought, so only the condition's incubation range after
  the index's infectious attendance separates the index's secondary cases from the rest of the room's illness.
- **Guard:** `guard.py check` PASS, no WARN. Nearest drivers 0.08 (task122 v2 lineage) and below.
- **Sources, one line each.**
  - Client Layer 2 patterns for the task type (seasonal baseline, nowcast of incomplete recent weeks, testing volume):
    none is this build's step; it is the outbreak investigator's attribution of contacts' illnesses to an exposure by
    the incubation range, the field's own method for counting secondary cases, filed as `own:`.
  - Client measured traps: habit 2 (the unit taken from the row grain) decided 11 of 64 tasks; here every case row of
    the room's follow-up reads as one secondary case, and the decided unit is an illness the index's attendance caused.
  - Family record: F8 (attribution) held where every booking partitions the same rows so every total ties (72); the
    room's case count ties under every attribution, only the split moves. Lane record: task231 estimated whether a
    silent unit was still in the population (maturity), task229 a convex conversion's bias, task230 a detection rate
    that falls with prevalence, task228 an error separation; none attributes outcomes to an exposure window.
- **Domain test:** the deciding quantity is each condition's secondary transmission per child-hour of an infectious
  case's attendance, which outbreak epidemiology estimates by counting as secondary only the contacts whose onset
  falls within the condition's incubation range after the exposure; a carrier's late tracking feed has no incubation,
  no illness days after the exposure that caused it and no window to attribute it by.
- **Conditions:** shigellosis (incubation 12 hours to 7 days), STEC infection (1 to 10 days), cryptosporidiosis (1 to
  12 days), each infectious from onset while the organism is shed. Hepatitis A was drawn at first and dropped (see
  `## Tried and rejected`).

## Default path

1. From the unit's childcare investigation register take each investigation's notifying laboratory and the time the
   laboratory authorised the result that opened it, keeping results authorised from 1 October 2023 to 30 September
   2026 (80 notifications: base hospital laboratory 13, Larkspur 22, Halden 22, Kestrel 11, Highfield 10, reference
   laboratory 2).
2. For each condition, take as the index's secondary cases (GL-CD-11 section 2: a room contact's case acquired from the
   index case) the confirmed and probable cases in the closed investigations' contact follow-up that fell ill after the
   index did, the ones ill earlier having been ill before the index could pass anything on (221 of the 319 cases in 140
   closed investigations), and divide by the child-hours of contact during the index cases' infectious attendance
   (index hours at the centre each day times the room's other children and educators that day, from the centres'
   attendance exports): shigellosis 11.33, STEC infection 4.61, cryptosporidiosis 12.16 per 1,000 child-hours.
3. For each notification and each allowed setting, work the unit's call had the result reached it at authorisation
   and that many hours later (calling hours 07:00 to 21:00), the booked hours the case would have spent at the centre
   between the two, times the room's other attendees that day, times the condition's rate; sum each feed's
   notifications and divide by three.
4. Set each feed at the longest allowed setting whose expected secondary cases a year do not exceed 1.00.

Ends on: base hospital laboratory 12, Larkspur 1, Halden 4, Kestrel 2, Highfield 12, reference laboratory 24 (hours;
Highfield's 12-hour figure sits at 0.997, so a variant of this path may file 8 there).
Golden: base hospital laboratory 12, Larkspur 2, Halden 12, Kestrel 4, Highfield 12, reference laboratory 24 (hours).

## Stump sentence

Counting as the index's secondary cases every follow-up case that fell ill after the index (221 of 319) gives 11.33,
4.61 and 12.16 secondary cases per 1,000 child-hours and sets the base hospital laboratory at 12 hours, Larkspur at 1,
Halden at 4, Kestrel at 2, Highfield at 12 and the reference laboratory at 24 (the default path's Ends on): the
follow-up runs two incubation periods past the exclusion, so it also records the cases the index's secondary cases went
on to cause and later introductions into the room, and only the cases whose onset falls within the condition's
incubation range after the index's infectious attendance (141 of the 319; 7.94, 3.07 and 6.98 per 1,000) can have
acquired the infection from the index, which sets 12, 2, 12, 4, 12 and 24. A solver who counts every follow-up case
keeps 319 and sets 2, 1, 2, 2, 8 and 24; one who counts only cases ill before the exclusion keeps 41 and sets every
feed at 24.

## Three rules

- Task type: `disease-surveillance-outbreak-anomaly-detection` (Epidemiology & Public Health), which serves Data
  Quality Monitoring & Alerting: the call is each laboratory feed's SLA lateness, priced by outbreak surveillance's own
  measure of what a late notification costs.
- Domain test: the deciding quantity is each condition's secondary transmission per child-hour of contact during an
  infectious case's childcare attendance, estimated the way outbreak investigation counts secondary cases, by room
  contacts whose onset falls between the index's first infectious attendance plus the condition's shortest
  incubation and its last infectious attendance plus the longest; the SLA lateness is then the expected secondary
  cases that lateness buys.
- Swap: "at how many hours late should each carrier's tracking feed page the duty manager, judged on the missed
  delivery slots the lateness causes" keeps a per-feed dial but loses the epidemiology: nothing incubates, no outcome
  falls days after the exposure that caused it, there is no room of contacts with its own earlier, community and
  second-generation illness, and no window attributes outcomes to the exposure; the task stops making sense.
- Layer 1: on the main path, attendance in three export layouts (each centre's management software: a CSV sign-in
  log, a workbook roll with 12-hour times, a JSON portal export), person numbers that differ by layout, casual
  educators covering absences under their own numbers, approximate onset dates in the follow-up; off it, laboratory
  timestamps with three UTC offsets, preliminary, final and corrected reports, a reference laboratory's typing reports
  on cases others notified, the 2025 condition code-set update, patient numbers that differ by laboratory, and the
  regional laboratory's 2024 acquisition, which changed its sending facility code. Each comes from the system that
  writes the file; none is placed to be caught and none moves the call.
- Layer 2: `decomposition_attribution` in the field-method family; how the room's recorded cases are attributed to the
  index's infectious attendance decides each condition's transmission and so each feed's lateness.
- Decisive step: attributing each room case to the index's infectious attendance through the condition's incubation
  range (onset no earlier than the first infectious attendance plus the shortest incubation and no later than the last
  infectious attendance plus the longest), instead of counting every case after the index's onset, every case in the
  follow-up, or only those before the exclusion.
- Not semantics: every field and definition can be read correctly (onset dates, case status, attendance, exclusion
  times, the incubation table, GL-CD-11's secondary case as a room contact's case acquired from the index) and the
  easy count of the cases ill after the index still includes the cases the secondary cases and later introductions
  brought; no field marks which case acquired the infection from the index.
- Not rule application: standard CD-ST-07 defines a feed's setting, the counterfactual call and the child-hour unit, and
  defines the transmission as secondary cases among room contacts per child-hour of contact; GL-CD-11 defines a
  secondary case by what it is (acquired from the index case), not by how to find one, and gives incubation ranges as
  facts about each condition, so executing every stated rule still files the default path's settings.
- Analyst test: a strong analyst who reads every date, status and attendance row and the secondary case definition
  correctly, drops the follow-up cases ill before the index and divides the rest by the index's infectious child-hours
  sets the base hospital laboratory at 12 hours, Larkspur 1, Halden 4, Kestrel 2, Highfield 12 and the reference
  laboratory 24 (the default path's Ends on); one who counts every follow-up case sets 2, 1, 2, 2, 8 and 24.
- Estimand: standard CD-ST-07 sections 2 and 3 fix it: a feed's SLA lateness is the longest allowed setting at which
  the expected secondary cases a year from the notifications that opened the unit's childcare investigations, with a
  result authorised from 1 October 2023 to 30 September 2026, do not exceed 1.00, had each reached the unit that many
  hours after authorisation rather than at it, at each condition's secondary cases among room contacts per child-hour
  of contact in the unit's closed childcare investigations.
- No decoy: nothing is planted; the room's earlier, community, second-generation and later cases are what a childcare
  enteric follow-up records over the guideline's follow-up period, no memo, draft, briefing or dashboard carries a feed
  setting, and no artifact ranks the feeds.
- No certified replay: no published or certified figure is reproduced to recover the method; the closed investigations
  are the raw material of an estimate, not controls a method must match.
- Lesson: a secondary case is an illness the index's exposure caused, identified by the incubation range after that
  exposure, not every illness in the room's follow-up, nor only those after the index's onset, nor only those before
  the exposure ended; no build on file teaches attribution by an incubation window.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 every follow-up case of the condition | GL-CD-11's secondary case (acquired from the index) rules out the cases ill before the index | the case status column | yes | none | passes | yes | readable |
| R1 drop the cases ill before the index (onset before its first infectious attendance plus the shortest incubation), the default path | the definition prompts it | onset beside the register's onset | yes, the careful solver's reading of the definition | none | passes | one filter | readable |
| R2 only cases ill before the exclusion | no | the register's exclusion time | a confusion of infection with onset | none | passes | one filter | readable |
| R3 the incubation window after the index's infectious attendance (decisive) | no: the standard names the quantity, the guideline defines a secondary case by what it is (acquired from the index) and gives incubation ranges as facts, and nothing says the follow-up's later cases may be a later generation or a later introduction | no column marks a later case; the follow-up end is a date in the register | no: the follow-up reads as the outbreak's case list | none | passes | a range per investigation from two register dates and two table entries | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternatives and the call under them | Ruled out by |
|---|---|---|---|---|
| SF1 | each feed | the six feeds of the NCP feed register, the regional laboratory one feed under both its facility codes | the register names each investigation's notifying feed by name: same call | same call |
| SF2 | the notifications the basis holds | the notification that opened each childcare investigation | every notification of an index case, or every childcare case's notification, adds notifications and moves feeds | CD-ST-07 2.3, "the notifications that opened the unit's childcare investigations" |
| SF3 | the basis period | results authorised 1 October 2023 to 30 September 2026 | by onset, specimen, receipt or call date, New South Wales or UTC: the same 80 | same call (C1) |
| SF4 | a year | the basis's expected cases divided by three | none other in the text | same call |
| SF5 | a case | confirmed and probable cases | confirmed only: 4.24, 1.54, 3.72 per 1,000, base hospital 24, Larkspur 12, Kestrel 8, Highfield 24 | CD-ST-07 3.3 and the guideline's case definitions |
| SF6 | the investigations the rate reads | the 140 closed | the 143 with the 3 open: same call | CD-ST-07 3.1, "closed"; same call |
| SF7 | the rate | the closed investigations' secondary cases divided by their child-hours, per condition | the mean of investigation rates: same call | CD-ST-07 3.1, "divided by"; same call |
| SF8 | child-hours of contact | the case's hours at the centre that day times the other children and educators who attended the room that day | each pair's overlapping hours: same call | CD-ST-07 2.4(d); same call |
| SF9 | infectious attendance | the index's attendance from the infectious period's start (onset) to the exclusion | none other in the guideline | guideline condition table; same call |
| SF10 | the counterfactual | the result reaching the unit at authorisation against that many hours after it | that many hours after the actual receipt: shifts every notification | CD-ST-07 2.4, "had it reached the unit at authorisation" |
| SF11 | the call and the exclusion | first calling-hours moment at or after receipt; a case at the centre leaves an hour after the call and attends no later session | leaving at the call: same call; a whole session lost or kept: Larkspur 8 | CD-ST-07 2.4(a) and (b) |
| SF12 | the case's hours in the counterfactual | the booked or rostered session | actual attendance pattern: none recorded after the exclusion | CD-ST-07 2.4(c) |
| SF13 | the room's others on a counterfactual day | the room's attendance that day | the room's bookings that weekday: same call | CD-ST-07 2.4(d); same call |
| SF14 | do not exceed | at most 1.00 | below 1.00: no feed's figure sits within 0.005 of 1.00 | same call |
| SF15 | the next longer setting | the next allowed setting, none for 24 hours | none | the prompt, "where there is one" |
| SF16 | rounding | expected cases two decimals, rates per 1,000 child-hours two decimals, from unrounded figures | rounding the rates first: same figures | CD-ST-07 4 |
| SF17 | that many hours | elapsed hours across a daylight saving change | wall-clock hours: same figures (no change falls between a weekday authorisation and a session) | same call |
| SF18 | the window's anchors | first and last infectious attendance | the infectious period's start and the exclusion date: same cases (no case onset in either edge zone) | same call (C1) |
| SF19 | the window's scope | the room's window | each contact's own shared days: the same 141 cases | same call (C1) |
| SF20 | ill before the index | onset before the first infectious attendance plus the shortest incubation | onset on or before the index's onset: the same cases (no case onset between) | same call (C1) |
| SF21 | the tolerance | 1.00 expected secondary cases a year | none | CD-ST-07 2.1 |
| SF22 | secondary case | a room contact's confirmed or probable case acquired from the index case | every confirmed or probable case among room contacts: 2, 1, 2, 2, 8 and 24 hours | GL-CD-11 section 2 (a secondary case acquired the infection from the index case); which recorded cases those are is the ladder, not a reading |

## Ladder

| Rung | Cases kept (of 319) | Per 1,000 child-hours (shig, STEC, crypto) | Settings (base hospital, Larkspur, Halden, Kestrel, Highfield, reference) | Killed by |
|---|---|---|---|---|
| R0 every follow-up case | 319 | 17.79, 5.38, 16.21 | 2, 1, 2, 2, 8, 24 | the 98 cases ill before the index's infectious attendance plus the shortest incubation and the 80 after the last plus the longest are not the index's |
| R1 drop the cases ill before the index (default) | 221 | 11.33, 4.61, 12.16 | 12, 1, 4, 2, 12, 24 | the 80 cases ill after the last infectious attendance plus the longest incubation |
| R2 only cases ill before the exclusion | 41 | 3.28, 2.30, 0.79 | 24, 24, 24, 24, 24, 24 | secondary cases fall ill one incubation after the exposure, mostly after the exclusion |
| R3 the incubation window (golden) | 141 | 7.94, 3.07, 6.98 | 12, 2, 12, 4, 12, 24 | the answer |

- **Golden margins** (expected secondary cases a year at the setting and at the next longer one, tolerance 1.00):
  base hospital 0.61 and 1.33, Larkspur 0.69 and 1.29, Halden 0.81 and 3.54, Kestrel 0.74 and 1.25, Highfield 0.61
  and 1.57, reference laboratory 0.15 (no longer setting). Nearest the tolerance: Halden at 12 hours, 23 per cent
  under; Kestrel at 6 hours, 25 per cent over.
- **Default path margins (R1):** on its three wrong feeds Larkspur 0.60 at 1 hour and 1.18 at 2, Halden 0.94 at 4
  hours and 1.18 at 6, Kestrel 0.46 at 2 hours and 1.16 at 4 (nearest 6 per cent, Halden at 4 hours); Highfield sits
  at 0.997 at 12 hours, so R1 lands the golden's 12 there or, on a variant, 8. R0's margins: nearest 21 per cent
  (Larkspur at 1 hour).
- **Separation:** R0 differs from the golden on five feeds, R1 on three, R2 on five; R0, R1 and R2 file three
  different settings vectors. The one-sided upper window (drop only the cases after the window) is a computed check,
  not a rung: 2, 1, 2, 2, 12, 24.
- **Worth on the graded figures:** every rung moves all three rates and all eleven expected-case figures; a response
  that lands five settings but not the rates loses the rates and every expected-case figure.
- **Arithmetic on the graded quantity:** R0 multiplies the rates by 1.75 to 2.3 and R1 by 1.4 to 1.75, and a feed's
  setting moves when that ratio carries its curve over 1.00; the curves step where the unit's call crosses the morning
  sessions (Kestrel's 03:30 to 08:30 Queensland authorisations), the end of the day (the daytime laboratories'
  plateau from 6 to 12 hours) and the next day (24 hours), so each rung lands on a named setting with room on both
  sides.
- **Bins:** the rates sit 0.0020 to 0.0042 from their rounding edges (two decimals per 1,000 child-hours; the nearest,
  STEC infection's 3.0730, flips at a 0.07 per cent rise in its child-hours) and the expected-case figures 0.0015 to
  0.0047 (the nearest, Larkspur's 0.6935 at 2 hours, flips at a 0.2 per cent fall); no graded figure is a whole or
  half number; every input is exact (whole minutes, quarter-hour bookings, whole cases) and the rounding path is
  filed.
- **R3a and R3b on the clean truth:** the default path (R1) with every filed rule applied files Ends on; the same
  path with only the attribution changed files the golden; R0 files 2, 1, 2, 2, 8 and 24 (asserted in
  `checks.py`).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the notifications that opened the childcare investigations, authorised in the basis period; the closed investigations for the rate | filed (CD-ST-07 2.3, 3.1); C1 on the date reading (SF3) |
| 2 Unit of account | a notification for the cost, a secondary case for the rate, a child-hour of contact for the exposure | filed (CD-ST-07 2.4(d), 3.1) |
| 3 Attribution window | the basis by authorisation date; a case to an investigation by its room follow-up | C1: no index's onset, specimen, authorisation, receipt or call falls on the other side of a basis boundary from the rest |
| 4 As-of dating | the register and follow-up as extracted on 13 November 2026 | filed (export manifest); open investigations excluded by status |
| 5 Version basis | the register's current record | one version shipped |
| 6 Denominator | child-hours of contact during infectious attendance | filed (CD-ST-07 3.1, 3.2) |
| 7 Weighting | pooled per condition | filed (CD-ST-07 3.1); the mean of rates gives the same call |
| 8 Window length | three years for the basis; every closed investigation since July 2021 for the rate | filed (CD-ST-07 2.3, 3.1) |
| 9 Boundary inclusivity | the incubation window's edge dates; "do not exceed" | C1: no case onset in an edge zone; no feed's figure within 0.005 of 1.00 |
| 10 Rounding path | rounded where reported, from unrounded figures | filed (CD-ST-07 4); rounding the rates first gives the same figures |
| 11 Tie-break | none needed | no two settings tie |
| 12 Maturity and censoring | investigations still in follow-up | filed: closed only (CD-ST-07 3.1); including them gives the same call |
| 13 Order of operations | rate from cases and child-hours, then cost, then setting | one order; asserted |
| 14 Row order | none | sums and counts; order-free, asserted |
| 15 Duplicate resolution | a room investigated twice | C1: no two investigations share a room within their export windows |
| 16 Identity normalisation | the index's person number in its centre's export | the register gives the number in the centre's own layout; one match each, asserted |
| 17 Netting against gross | none | cases and hours are counts |
| 18 Dimensional units | hours from sign-in and sign-out times in three layouts | each layout parses to the same hours, asserted per layout |
| 19 Code and status semantics | case status confirmed or probable | filed (CD-ST-07 3.3 and the guideline's case definitions); never the stump |
| 20 Integerisation | none | no figure is rounded to whole units |
| 21 Clause scope | the counterfactual's rules apply to every notification; the window to every closed investigation | filed (CD-ST-07 2.4) |
| 22 Forward window contents | the coming year's notifications | filed: the basis's three years stand for a year of notifications (CD-ST-07 2.2) |

## Literal reader

Executing the prompt, CD-ST-07 sections 2 to 4, the guideline's case definitions and condition table, and the release
notes word for word fixes the basis (the 80 notifications that opened investigations, authorised 1 October 2023 to 30
September 2026), the counterfactual call and leaving rule, the child-hour unit, the closed investigations, the case
statuses, the setting rule and what a secondary case is (GL-CD-11 section 2, a room contact's case acquired from the
index case); the one step the text leaves to the analyst is which of a room's recorded cases those are, and every
reading that takes them as the cases the index's infectious attendance could have
caused (onset within the condition's incubation range after a day the index attended while infectious, by the room's
days or each contact's own, edge dates in or out, anchored on attendance or on the onset and exclusion dates) keeps
the same 141 cases and files 12, 2, 12, 4, 12 and 24 hours (C1, asserted); counting cases the index could not have
caused is a rung of the ladder, not a reading of a term.

## Oracles

None for the call: no file states a case count, a rate, an expected-case figure or a setting for any feed; the release
notes give no default lateness; the investigation register carries dates, statuses and the notifying feed, never a
count of the room's cases. For the asks: the interface incident log records each incident's window and category and
never a count of re-sent messages; the case extract records each merge and never a count per feed; neither ties to an
ask figure under any handling.

Leak sweep (`leak.py --asof 2026-11-16`, REVIEW, no LEAK), one line per REVIEW:
- Sweep 3, the standard's 1.00: the tolerance in CD-ST-07 section 2.1, a stated input, not an answer figure.
- Sweep 4, the standard (infectious, attendance, investigations, closed): the estimand's own words in sections 2 and 3;
  no sentence names an incubation window, a later generation or which recorded cases are the index's.
- Sweep 4, the guideline (infectious, incubation, attendance, follow-up, closed, illness): the unit's response process,
  the case definitions (a secondary case is a room contact's case acquired from the index case) and the condition
  table's incubation periods as facts about each condition; it says the follow-up asks about illness from 21 days
  before the case's onset and follows the room to 14, 20 or 24 days after the exclusion, which is why the follow-up
  holds earlier and later cases, and never says how to tell which of them acquired the infection from the index.
- Sweep 4, the release notes (contacts, register, health): the platform's release text; nothing on the attribution.
- Sweep 6, the investigation register names the six feeds beside numbers: each investigation's notifying laboratory
  and dates, one row per investigation; no count, rate, expected-case figure or setting per feed.
- Sweep 9, 17 November 2026 in the register: the follow-up end of the one investigation still open (CC26-022), a
  planned date the guideline's section 4.4 sets.

Leak reader, two reads: the first executed the undefined "secondary cases" literally as every room contact's case
(fixed by the definition, see `## Tried and rejected`) and flagged the incident log's repeated summaries (now drawn
from a pool of causes, no normalised summary more than four times) and a feed register note that explained the feed
(now a grain statement); the second read found the WHAT literal (acquired from the index) and the HOW open, which is
the analysis the build rests on, and every sweep line harmless.

Duplicate guard: `guard.py heart` PASS (nearest 0.08, task122 v2 lineage); `guard.py surface` PASS, nothing promoted
(nearest task88 at 0.097, task229 at 0.096, both unpromoted).

## Ask sheet

Two asks, 18 figures, each decoupled from the call (none uses an investigation, an attendance row, a booking or the
standard's counterfactual) and each moved by silent primaries on rows outside the main population. Stops and misses
are recomputed from the shipped files by `generator/verify.py` and asserted in `generator/checks.py`.

**Main population (zero device rows, asserted):** the investigation register's 143 investigations, the contact
follow-up of the 140 closed ones, the attendance exports and bookings of the investigated rooms, standard CD-ST-07
and the guideline. The asks read the platform's message log, its case extract, the interface incident log and the
feed register; no index case and no follow-up case has a re-sent copy, an amended final report or a merged duplicate
case (asserted by count).

| Ask | Figures | H18 home | Use | Primary devices (family) | Hazards | Path (files, columns) | Stops (natural read, half-handled, over-corrected, answer) |
|---|---|---|---|---|---|---|---|
| A: each feed's reports in the year to 30 September 2026 and those that first reached the platform more than 24 hours after authorisation | reports (6), late reports (6) | a measure every feed carries that the call does not turn on: how late each feed runs today against the platform's existing 24-hour report | the letter to each laboratory confirming its new setting quotes its past year | D1: when a laboratory's primary interface engine failed, its disaster-recovery engine re-sent what the primary had sent since its checkpoint under fresh message ids, writing the accession number with its namespace (base hospital, Larkspur with Highfield, Halden), and when Kestrel's and the reference laboratory's engines stopped, the restart replayed from the checkpoint the same way; D1 over-clean half: every report the disaster-recovery engine or the replay sent for the first time carries the same namespace (that night's results, the results the primary had held in its error queue, released through the disaster-recovery engine more than a day after authorisation, and the results queued while an engine was stopped), and every laboratory issues some amended results as a second final report of the same test and accession, re-authorised (Kestrel and the reference laboratory most) | preliminary, final and corrected reports of one test count separately; the reference laboratory's UTC timestamps at the year's edges; the Kestrel +10:00 offset | message log (sending facility, message id, accession, patient number, test, status, authorised, received), feed register (codes to feeds, acquisition date), incident log (feed, category, opened, resolved), release notes (lateness from authorisation to first acceptance), dictionary (one report per message, dates in New South Wales time): 5 files, 14 columns | every message 12 of 12 high (2,386 and 17, 3,908 and 37, 2,503 and 39, 1,045 and 12, 1,180 and 20, 261 and 9); deduplicated on accession, test and status 12 of 12 off; on accession and test 12 of 12 off; every namespaced accession dropped 12 of 12 low (2,370 and 10, 3,874 and 20, 2,466 and 18, 1,037 and 6, 1,165 and 10, 254 and 2); namespace stripped and deduplicated on accession, test and status 12 of 12 low (amended finals merged); deduplicated on patient, test and status 12 of 12 low; the answer, one report per laboratory, patient, test, status and authorisation at its first receipt (the same keyed on the accession without its namespace), 2,377 and 12, 3,884 and 22, 2,473 and 19, 1,041 and 8, 1,167 and 11, 256 and 4 |
| B: the shigellosis, STEC infection and cryptosporidiosis cases each feed was first to notify in the year | cases (6) | the share of the urgent case stream each feed's setting governs | the same letter: how many urgent cases each laboratory was first to report | D7: duplicate cases the platform opened when a second laboratory's report did not match the patient, merged by the surveillance team into the later case that carries the investigation; the earlier case's reports stay under its retired number, so its laboratory notified the surviving case first; D1 over-clean half: patients with two genuine episodes of a condition in the year at one laboratory, two cases | the 2025 code-set update (Halden's urgent results carried retired codes until 17 November 2025); the reference laboratory's typing reports on cases others notified; receipt dates in UTC at the year's edges | message log (case number, sending facility, received, patient number, condition code), case extract (case number, condition, status, merged into), feed register, condition code set, dictionary: 5 files, 10 columns | every case number by its own first report 6 of 6 high (35, 90, 48, 25, 30, 2); merged cases dropped and survivors by their own first report 6 of 6 off (33, 88, 46, 25, 30, 2), as is the extract's stored notifying facility; merges followed and then one case per laboratory patient and condition 3 low (Larkspur 88, Halden 46, Kestrel 23); the answer, each case after merges by its first accepted report across its numbers, 34, 89, 47, 24, 29, 1 |

- **Span:** seven files and 21 column uses across the asks; the asks share the message log but no primary device or
  column path (A reads accession, test, status and authorisation; B reads case numbers, merges and conditions).
- **Shared hazards:** the reference laboratory's UTC timestamps move A (authorisation dates) and B (receipt dates) at
  the year's edges; preliminary and corrected reports are texture on B (they open no case).
- **Realism:** each device is a record the platform or a laboratory makes (a disaster-recovery engine re-sending from
  its checkpoint and releasing the primary's error queue, a stopped engine replaying from its checkpoint, a laboratory
  issuing an amended result as a new final, a case opened twice and merged, a child infected twice); none needs a task
  to exist.
- **Referee:** none; no ask turns on a designed disagreement.

| Ask figure | Where the cracker's path goes | Mirror (stops at R1) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A reports, four feeds with disaster-recovery copies | exact-duplicate and message-id checks pass the namespaced copies; dropping every namespaced row also drops the genuine reports the disaster-recovery engine sent | misses the same way | miss |
| A reports, Kestrel and reference laboratory | deduplicates on accession, test and status and merges the amended finals; dropping namespaced rows also drops what the replay sent for the first time | misses the same way | miss |
| A late reports (6) | the namespaced copies arrive a day or more after authorisation and count late; dropping every namespaced row also drops the late genuine reports the error queue and the replays released; the merged amended finals drop late reports | misses the same way | miss |
| B cases (6) | counts the case extract's live cases by their own first report, missing the retired case's earlier report, or counts every case number | misses the same way | miss |

- **Cracker keeps:** about 0.15 of the ask weight (a cracker who keys reports on patient, test, status and
  authorisation keeps A, one who follows merged cases' reports keeps B; no single habit keeps both).
- Mirror leakage: 15 per cent of ask weight (the mirror's ask path is the cracker's; the asks do not touch the call's
  construction).
- Pair ceiling: 36.8 (C = 38 + 7 + 55 x 0.15 = 53.3; S = 5 + 7 + 55 x 0.15 = 20.3; mean 36.8).

## Pre-ship check

1. Domain: outbreak epidemiology's own estimate of secondary transmission per child-hour of an infectious case's
   childcare attendance, counting as the index's secondary cases only the room contacts whose onset falls within the
   condition's incubation range after the index's infectious attendance (the secondary attack rate's incubation
   qualifier); with a carrier's tracking feed in its place nothing incubates, no room holds earlier, community and
   later-generation illness, and there is no window to attribute by.
2. Real work, nothing planted: the centres' three attendance layouts, casual educators under their own numbers and
   approximate onset dates on the call's path; off it, three timestamp offsets, preliminary, final and corrected
   reports, the reference laboratory's typing reports, the 2025 code set, per-laboratory patient numbers, the 2024
   acquisition's facility code, failover and replay re-sends, error-queue releases, amended finals, merged duplicate
   cases and second episodes; each is a record the unit's, the centres' or the laboratories' systems produce, and none
   sits on the call's rows (asserted by count).
3. The step that flips the call is methodological: attributing each room case to the index's infectious attendance
   through the incubation range, not counting every case after the index, every follow-up case, or only the cases
   before the exclusion.
4. Analyst test: the default path (every case ill after the index) files 12, 1, 4, 2, 12 and 24 hours; every
   follow-up case files 2, 1, 2, 2, 8 and 24; only cases before the exclusion files 24 for every feed (asserted on the
   clean truth, `checks.py` R3a and R3b).
5. CD-ST-07 sections 2 and 3 define the estimand (the basis notifications, the counterfactual call, the child-hour,
   secondary cases among room contacts in closed investigations, the tolerance) and GL-CD-11 section 2 defines a
   secondary case (acquired from the index case); the incubation ranges and the data force the window, and every
   window reading keeps the same 141 cases (C1 asserted).
6. No decoy: no memo, dashboard, prior list or default carries a feed setting; the release notes give none and no
   artifact ranks the feeds.
7. Nothing is recovered from certified figures: the closed investigations are evidence for an estimate, not controls
   to match.
8. The lesson (a secondary case is an illness the index's exposure caused, found by the incubation range after that
   exposure) is on no other card: nearest drivers 0.08.

## Tried and rejected

- Seed pitfall kept (regression of downstream error on a lag measured with error, corrected by regression calibration
  from replicates, or transported to a new lag monitor): a general-statistics method that reads the same in any feed
  world, the backdrop the author's domain review returns, and next to task228's measurement-error separation; rejected
  at the draw.
- Air quality monitor telemetry (PM2.5 NowCast under-warning in a reporting area, lateness coupled to smoke): the
  replay of the NowCast and the area rule is the filed rules executed, and the coupling of lateness to smoke reads the
  same for any outage coupled to load; rejected at the draw, and DQ19 to DQ21 hold the air quality alert worlds.
- Earthquake early warning station latency (pivotal fourth trigger, forward seismicity after declustering): the
  trigger rule is filed, and the coming year's seismicity forks between a declustered catalogue, the Omori tail of a
  recent sequence and a recent-years window; rejected at the draw.
- Tide gauge telemetry for storm-surge lead time (de-tided residuals, surge events against the tide's propagation): a
  strong solver measures lead time on the surge events the warning log lists; rejected at the draw.
- Product analytics feed freshness for experiment scorecards (randomisation protects lift from arm-symmetric loss):
  the replay of each scorecard finds it directly and the swap to any randomised trial reads the same; rejected.
- Psychometric response-time thresholds (rapid guessing) and experience-sampling latency windows: off the seed's world
  and model-dependent; rejected at the draw.
- Laboratory release times in single fixed batches (prototype, 2026-10-13): a batch feed's cost jumps from zero to its
  full value at one setting, so every attribution lands on the same setting; release times spread through each
  laboratory's working hours, as authorisation by scientists runs, keep the rungs apart.
- Hepatitis A as a fourth condition (2026-10-13): infectiousness two weeks before onset, an infectious period that ends
  a week after onset (so lateness after it costs nothing), and post-exposure vaccination of room contacts each open a
  convention the standard would have to file; dropped, leaving three conditions infectious from onset while shed.
- Whole-session exclusion in the counterfactual (prototype): the cost steps at session starts and Larkspur's setting
  moves with the convention; the standard files that a case at the centre leaves an hour after the call.
- Ill contacts who tested negative in the follow-up (2026-10-13): counting every ill contact would be a field read on
  the main path; the follow-up lists cases and contacts who were not ill, and the case status carries the rest.
- Notifications read from the message log on the main path (2026-10-13): Kestrel's +10:00 and the reference
  laboratory's UTC offsets would put a clock reading on the call; the register carries the triggering result's
  authorisation in New South Wales time and the message log serves the asks.
- A rejected-then-resent message device for ask A (2026-10-13): "first reached the platform" would fork between the
  first delivery and the first acceptance; the log holds accepted messages only.
- An interface downtime ask from the incident log (2026-10-13): hours out of service fork between the platform's
  monitoring times and the laboratories' own notices, and an ask wording that settles it names the double logging;
  the incident log stays the context artifact.
- A clock device in the message log for ask A (2026-10-13): the register's New South Wales authorisation times on the
  same index notifications would be its oracle; the log's offsets stay explicit, texture only.
- Replays that wrote the namespace on the re-sent copies only, and failovers that sent no late genuine report (stage 3,
  2026-10-13): dropping every namespaced row reproduced Kestrel's and the reference laboratory's figures and every
  feed's late count (8 of the 12 ask A figures). A restarted engine's replay now writes every message it sends with the
  namespace, a failover also releases the primary engine's error queue through the disaster-recovery engine, and the
  Kestrel replay and Larkspur failover checkpoints moved to 52 and 56 hours, where no stop ties any feed's figure.
- "Secondary cases among room contacts" left undefined (stage 4, 2026-10-13): the leak reader executed it literally
  as every confirmed or probable room contact (the old default path, 2, 1, 2, 2, 8 and 24) and the judge settled it
  only by the field's meaning of secondary, which our floor counts as open; GL-CD-11 section 2 now defines a secondary
  case by what it is (acquired the infection from the index case), never by how to find one, and the default path
  moves to every case ill after the index (12, 1, 4, 2, 12 and 24). The judge's suggested pin (the incubation window
  named in CD-ST-07 3.1) would file the method and is not taken.
