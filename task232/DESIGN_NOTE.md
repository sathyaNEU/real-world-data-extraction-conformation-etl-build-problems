# task232 design note

A regional local health district in northern New South Wales, on the Queensland border. Its public health unit acts
on every laboratory notification of an enteric condition in a childcare attendee or staff member by excluding the case
from the centre. On 1 December 2026 the state's notifiable-conditions platform moves to a release that gives each
pathology laboratory's electronic notification (ELR) feed its own SLA alert: when a result has not reached the unit
within the feed's set lateness after the laboratory authorised it, the alert pages the on-call public health officer.
The unit sets each feed's lateness from the allowed settings (1, 2, 4, 6, 8, 12 and 24 hours) by the secondary cases
that lateness would let an infectious child or staff member cause in their childcare room before exclusion.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task232.json`, architecture v1, drawn 2026-10-13. Epidemiology & Public
  Health (client domain), task type `disease-surveillance-outbreak-anomaly-detection`, objective Data Quality
  Monitoring & Alerting (the object is each laboratory feed's timeliness, the call is the lateness its SLA alert pages
  at). Shape `other`: a dial per laboratory, each feed's lateness and the expected secondary cases a year at that
  setting and at the next longer one. Decision `dial_setting`, question form how-many. Gap time then population; no A
  to E pattern, decisive generator G4 (attribution at the exclusion transition), then G13 (an illness dated days or
  weeks after the exposure that caused it). Gate G `decomposition_attribution`: the room's illnesses are split between
  the index's own secondary cases and everything else. Strategy `decomposition_attribution`. No calibration organ.
  Context artifact `operations_log` (the platform's interface incident log). Stakeholder: the manager of the unit's
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
  investigations whose illnesses fall days or weeks after the exposure that caused them.
- **Data-native sentence:** enteric secondary cases fall ill one to fifty days after the childcare session that
  infected them, and a room investigation's follow-up also records the children who were ill before the index became
  infectious (the index's own source and co-primary cases), community cases and cases the secondary cases went on to
  cause, so only the incubation range after the index's infectious sessions separates its secondary cases from the
  rest of the room's illness.
- **Guard:** `guard.py check` PASS, no WARN. Nearest drivers 0.08 (task122 v2 lineage) and below.
- **Sources, one line each.**
  - Client Layer 2 patterns for the task type (seasonal baseline, nowcast of incomplete recent weeks, testing volume):
    none is this build's step; it is the outbreak investigator's attribution of contacts' illnesses to an exposure by
    the incubation range, the field's own method for counting secondary cases, filed as `own:`.
  - Client measured traps: habit 2 (the unit taken from the row grain) decided 11 of 64 tasks; here every ill
    contact row reads as one secondary case, and the decided unit is an illness the index's attendance caused.
  - Family record: F8 (attribution) held where every booking partitions the same rows so every total ties (72); the
    room's illness count ties under every attribution, only the split moves. Lane record: task231 estimated whether a
    silent unit was still in the population (maturity), task229 a convex conversion's bias, task230 a detection rate
    that falls with prevalence, task228 an error separation; none attributes outcomes to an exposure window.
- **Domain test:** the deciding quantity is each condition's secondary transmission per child-hour of an infectious
  case's attendance, which outbreak epidemiology estimates by counting as secondary only the contacts whose onset
  falls within the condition's incubation range after the exposure; a carrier's late tracking feed has no incubation,
  no illness weeks after the exposure that caused it and no window to attribute it by.

## Default path

1. From the platform's ELR message log (`elr_messages_2022_2026.csv`) keep each case's first notification (the
   platform case number) of shigellosis, STEC infection, cryptosporidiosis or hepatitis A, and join the case register
   to keep the cases who attended or worked at a childcare centre while infectious; count each laboratory's urgent
   childcare notifications from 1 October 2023 to 30 September 2026 with their authorisation times.
2. For each condition, take the secondary cases of every closed childcare investigation as the room contacts the
   contact follow-up records as ill with the same laboratory-confirmed condition, and divide by the child-hours the
   index attended while infectious (sessions attended times session hours times the room roster).
3. For each laboratory and each allowed setting, count the sessions each notified case would still have attended had
   the result reached the unit that many hours after authorisation (the unit's calling hours and the centre's session
   start), multiply by the room roster, the session hours and the condition's rate, and scale to a year.
4. Set each feed's SLA lateness at the longest allowed setting whose expected secondary cases a year stay within the
   standard's tolerance.

Ends on (design target, fixed with the generator at stage 2): the hospital laboratory at 6 hours, the larger private
group at 8, the second private group at 12, the Queensland border laboratory at 1, the regional laboratory at 8 and the
state reference laboratory at 24.
Golden (design target): the hospital laboratory at 8 hours, the larger private group at 12, the second private group at
12, the Queensland border laboratory at 2, the regional laboratory at 12 and the reference laboratory at 24.

## Stump sentence

The default path counts every room contact the follow-up records as ill with the condition as the index's secondary
case and sets four feeds tighter than they need to be (the hospital laboratory at 6 hours, the larger private group and
the regional laboratory at 8, the Queensland border laboratory at 1); the follow-up also holds the children ill before
the index was infectious, community cases and the cases secondary cases went on to cause, and attributing each illness
to the index's infectious sessions through the condition's incubation range puts the hospital laboratory at 8 hours,
the larger private group and the regional laboratory at 12 and the border laboratory at 2. A solver who counts only the
contacts ill before the exclusion loses the cases that fall ill days or weeks after it and sets the hospital, border
and regional feeds at 24 hours.

## Three rules

- Task type: `disease-surveillance-outbreak-anomaly-detection` (Epidemiology & Public Health), which serves Data
  Quality Monitoring & Alerting.
- Domain test: the deciding quantity is each condition's secondary transmission per child-hour of an infectious
  case's childcare attendance, estimated the way outbreak investigation counts secondary cases, by contacts whose
  onset falls between the index's first infectious session plus the condition's shortest incubation and the exclusion
  plus its longest; the SLA lateness is then the expected secondary cases that lateness buys.
- Swap: "at how many hours late should each carrier's tracking feed page the duty manager, judged on the missed
  delivery slots the lateness causes" keeps a per-feed dial but loses the epidemiology: nothing incubates, no outcome
  falls days or weeks after the exposure that caused it, there is no room of contacts with its own earlier, community
  and second-generation illness, and no window attributes outcomes to the exposure; the task stops making sense.
- Layer 1: laboratory timestamps in three clocks (New South Wales time with daylight saving, Queensland time without
  it, UTC from the state reference laboratory); one case notified by several laboratories and corrected reports
  re-sent; the platform's 2025 condition code-set update; each centre's own roster export layout; patient identifiers
  that differ by laboratory, linked by the platform's case number; approximate onset dates in the follow-up; the
  regional laboratory's 2024 acquisition by a private group, which changed its sending facility code. Each comes from
  the systems that make the files; none is placed to be caught, and none sits on the decisive path.
- Layer 2: `decomposition_attribution` in the field-method family; how the room's recorded illnesses are attributed to
  the index's infectious attendance decides each condition's transmission and so each feed's lateness.
- Decisive step: attributing each contact's illness to the index's infectious sessions through the condition's
  incubation range, instead of counting every ill contact in the follow-up as a secondary case or only those ill
  before the exclusion.
- Not semantics: every field can be read correctly (onset dates, sessions, exclusion times, conditions, laboratory
  confirmation, the incubation table) and the easy count still includes the children ill before the index was
  infectious and the cases secondary cases caused; no field marks which illness the index caused.
- Not rule application: the unit's SLA standard defines a feed's lateness by the secondary cases expected from the
  extra sessions, at each condition's transmission per child-hour estimated from the closed childcare investigations,
  and leaves open which of a room's recorded illnesses are the index's secondary cases; the control guideline gives
  incubation ranges as facts about each condition, not a procedure, so executing every stated rule still files the
  default path's settings.
- Analyst test: a strong analyst who keeps each case's first notification, reads every date and code correctly and
  divides each investigation's ill contacts by the index's infectious child-hours sets the hospital laboratory at 6
  hours, the larger private group and the regional laboratory at 8 and the border laboratory at 1 (the default path's
  Ends on), and one who counts only illnesses before the exclusion sets three feeds at 24 hours.
- Estimand: the unit's ELR SLA standard (to be named at stage 2) defines a feed's SLA lateness as the longest allowed
  setting at which, had each urgent childcare notification the laboratory sent in the three years to 30 September 2026
  reached the unit that many hours after authorisation, the secondary cases expected among the index's room contacts
  from the extra sessions would not exceed the tolerance in a year, at each condition's secondary transmission per
  child-hour of infectious attendance estimated from the unit's closed childcare investigations.
- No decoy: nothing is planted; the room's earlier, community and second-generation illnesses are what childcare
  enteric investigations record, no memo, draft or dashboard carries a wrong feed setting, and no artifact ranks the
  feeds.
- No certified replay: no published or certified figure is reproduced to recover the method; the closed
  investigations are the raw material of an estimate, not controls a method must match.
- Lesson: a secondary case is an illness the index's exposure caused, identified by the incubation range after that
  exposure, not every illness in the contacts' follow-up nor only those before the exposure ended; no build on file
  teaches attribution by incubation window.

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
