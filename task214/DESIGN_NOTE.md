# task214 design note

Wave 8, Anomaly Detection & Diagnostics. A new draw in another client domain: the Larix world of seed AD37 is set
aside (see the tried and rejected log below) and nothing of that seed is used.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task214.json`, architecture v1, drawn and filed 2026-11-07. Guard:
  WARN only (org family government_agency overused; objective anomaly-detection 4 of the last 12, the lane's own
  objective; Gate G decomposition_attribution 6 of the last 12, kept because the decisive step does attribute each
  case's exposure among the assets that delivered its water, and no other key is honest). Nearest drivers 0.07 and
  under.
- **Pairing:** client domain Epidemiology & Public Health, task type `disease-surveillance-outbreak-anomaly-detection`
  (AD, DQ in the taxonomy), drawn as the client domain itself. Least spent on AD: one card in the cell (task188,
  pooled mosquito tests). Barred domains avoided: General Statistics & Data Science (task212), Banking (task213),
  Pharmacology (task211), Human Factors' safety-incident-error-analysis (task210).
- **World:** a fictional New Zealand district: the district council's drinking-water supply (six service
  reservoirs, sixteen supply zones fed through feed and link mains, eleven normally closed boundary mains between
  zones of different reservoirs) and the regional public health service. Spring 2027: a cryptosporidiosis outbreak in
  two zones that the supply-zone register puts on reservoir R4. The decision, on Tuesday 19 October 2027: which asset
  the council takes out of service before the 26 October renewal of the feed main to those zones. The call faces
  forward: the renewal will back-feed the same zones again.
- **The mechanism (clean truth):** while a zone's feed main is shut for a repair, crews keep it in supply by opening a
  boundary main from a neighbouring zone, so for those days the zone drinks another reservoir's water. Boundary main
  BM3 runs through a grazed paddock with a damaged air valve; when it carries water within two days of heavy rain,
  runoff is drawn in. On 4 to 6 October 2027, after 94 mm in three days, FM11 was shut for a burst repair and zones Z11
  and Z12 were back-fed through BM3 from Z05 (reservoir R2's network). Cases follow each zone's actual water through
  each case's own incubation period (1 to 14 days, median 7).
- **Golden:** each asset's attack rate, cases per 100,000 resident-days its water reached, with each case's incubation
  window laid over the supply path its zone actually had on each day (rebuilt from the valve operations through the
  network model): BM3, far ahead of everything else. **Default path's answer:** R4, the register's source for the two
  worst zones.
- **Shape:** 18 (hypotheses against evidence): each candidate asset with its cases carried and its attack rate, the
  call, the runner-up and the gap; arithmetic in ## Ladder at stage 2.
- **Strategy:** decomposition_attribution (each case's exposure attributed among the assets its water passed through
  on the days its incubation window covers). Layer 2 family estimand_identification, pattern
  `own:exposure-traced-through-network-operations`. Card: gap time then population, generators G5 (provision
  elsewhere) then G3 (record versus operation), Gate G decomposition_attribution, decision pick_one_of_n.
- **Data-native sentence:** in this network a zone's water comes from whichever reservoir the valves connect it to on
  the day, and crews back-feed a zone through a boundary main whenever its own feed main is shut, so the supply-zone
  register (the normal arrangement) and the water people drank part company exactly on repair days, which no
  notification, register or zone table records.
- **Abstraction sentence:** an event's source is the one whose output reached the event's area during the event's own
  exposure window under the configuration a switch log sets, not the one a register of normal assignments names. Not
  writable against an approved build: task162 (approved) reads valves in a water network too, but its insight is a
  control valve acting only while its inlet runs above its setting (pressure-conditional leakage); task156 (NZ
  wastewater) is infiltration below a water table; task181's tray-to-steriliser tracing finds a faulty processing
  step and judges units net of it, while here the register's own source is innocent and the decisive object is which
  path the water took in each case's window.
- **Furniture (live window task211 to task213):** forum committee_or_panel, executive_team, line_manager_or_team held;
  forcing events purchase_order_or_contract, season_or_peak, period_close held; org families
  hospital_or_health_provider, logistics_or_3pl, software_or_platform held. Drawn: forum regulator_or_inspector (the
  medical officer of health directs the supplier), forcing event incident_or_complaint (the outbreak), org family
  government_agency (the honest label; WARN answered above).
- **Guard probes (2026-11-07):** gap population with G3 and decomposition_attribution BLOCKs test.same_driver against
  task399 and older builds, and same_puzzle_older against task270, task275, task450 and task468; gap time with G5
  then G3 clears. Question form `which` warned against task212; the decision locates a source on the network, so the
  form is `where`.
- **Personas:** `guard.py names --geo new-zealand --locale en_NZ --seed 214`: Anna Gullery (medical officer of
  health), Rhys Cook (network operations lead). Elizabeth Morgan was drawn first and dropped (first name in task128).
- **Sources for the levels (screen 1):** cryptosporidiosis incubation 1 to 12 days, about 7 on average (US CDC,
  Cryptosporidiosis clinical overview; Health New Zealand, Communicable Disease Control Manual); New Zealand
  notifications about 25 to 30 per 100,000 a year with a spring peak at calving and lambing (ESR, Notifiable diseases
  in New Zealand annual reports); a damaged air valve in a grazed field drawing contamination into a main, about
  16,000 properties under a boil-water notice and more than 100 confirmed cases (Brixham, Devon, May 2024, UKHSA and the
  Drinking Water Inspectorate); a Cryptosporidium outbreak in a New Zealand town supply with about 70 cases
  (Queenstown, September 2023, Health New Zealand); water main failures of the order of 10 to 20 per 100 km a year
  (Water New Zealand, National Performance Review); average household size about 2.6 (Stats NZ, 2023 Census).
  Measured on the clean truth: 35 to 72 notified outbreak cases among about 10,000 back-fed residents (0.4 to 0.7 per
  cent, against Brixham's 0.4), 2 to 9 sporadic cases in the review window.

### The five go/no-go screens (clean truth, `generator/screens.py`, seeds 1 to 40)

1. **Levels and lead:** golden BM3 equals the truth 40 of 40; lead over the runner-up at or above 1.2 in 40 of 40,
   minimum 3.80, median about 5.7 (runner-up LM12 or FM11 by redraw).
2. **The golden's own method:** BM3 under every variant 20 of 20 on each block: incubation weights lognormal (median 7)
   or flat over 1 to 12, 2 to 14, 3 to 10 and 1 to 14 days; the served window opening 1 August or 1 September;
   residents or properties as the denominator (one constant per zone, same call).
3. **First look** (the zone with most cases, then its register source) wrong 40 of 40 (R4).
4. **Careful readers**, each wrong 40 of 40: (a) attack rates by zone and by register source, R4; (b) constructing:
   the onset-day path and the report-day path (FM11 or LM12, because the back-feed ended before nearly every onset),
   the dated event (the burst repair on FM11, repair-site ingress), the nearest reservoir to the cases and to the two
   worst zones (R4); (c) per-record zone-by-week cells on every joinable attribute (R4; the valve operations join to
   no case attribute); (d) mechanism-naming: waterborne attack rates by supply zone through the register (R4) and
   post-repair ingress at the burst (FM11); (e) literal replay of every stated fact, R4.
5. **Literal execution of the filed WHAT** (the asset whose water reached the cases, taken through the register as
   written) names R4, 40 of 40; the golden needs the step the WHAT does not tell anyone to compute: each zone's
   supply path day by day from the valve operations through the network model.

### What each spent AD driver spends (`guard.py mechanisms --objective anomaly-detection`, one line each)

task25 a second source's missing inflow completes a forward ranking; task28 the reachable share of a flagged excess;
task33 forward yield of a shift still in force, truncated at a filed intervention; task48 a gap visible only at a
two-sided pair grain; task54 loss borne by every unit in custody; task68 like-for-like change across identity
successions; task76 a look-back class with zero conversion; task85 each unit's own observation window from an
intermediary's lead time; task103 contacts fanned out through authorisations against records of service; task104 a
self-adapting scorer replayed at an unrun setting; task119 failed waits the unit could have shortened; task183 parts
that keep failing defeat trailing rates; task180 detection thresholds riding a daily noise cycle; task185 a device
conversion sized at the value; task186 shared local cycles inflating a within-unit test; task187 Jensen over a curved,
capped response; task188 pooled-test infection rates by maximum likelihood; task189 left-censoring under
instrument-specific limits; task195 a paired difference's uncertainty against overlapping intervals; task193 room for
an ordering set by first exposure in the window; task192 a validation batch covering only the window's opening;
task197 a unit's response to a shared signal along a scheduled trajectory; task196 two capture channels, the second
produced by the first; task194 a coding lag read through two vintages; task182 length-biased snapshots (lineage: a
lagged driver response, a background under a running source, residual deterrence screened dead in architecture 8);
task198 a value capped at the lesser of ask and entitlement; task199 events recorded only where watchers filed;
task201 exposure-time missing an opening interval set by the number of reporters; task184 a saturating container
indicator (lineage: interval-censored cycles); task204 a transport rate from a unit's own unsteady balance; task181 a
shared upstream processing step (trays through one steriliser) adding risk to the cases it handled (lineage: two
pooled sources, an arrival-delay nowcast, near-repeat runs, crossings, residence against workplace); task191
informative censoring of slow-closing rare outcomes; task125 scheduled occasions at a bordering site moved by the coming
calendar; task190 found errors scaling with second-record coverage; task210 a per-pass hazard set by the sun against
each heading; task211 a transient after each member's first encounter with a changed version, by supply point;
task212 each case's load from the cases scanned into its container after it; task213 control shown by flows that
return across two ledgers to their source. None reads where a network's operations sent each case's exposure.

### Slot screens (`guard.py slots`, mechanism nouns then setting nouns, before any harness)

- Seeding and carriers (driver sentence; care home, agency staff, shared staff; introduction, seeding, importation):
  no slot holds the insight; task234 mentions care-home outbreaks in passing. Set aside anyway on paper: every carrier
  design reads as task181's shared step adding risk to the cases it handles.
- Patrol, deterrence, Koper, hot spot: task182 architecture 8 screened residual deterrence and it failed; closed.
- Cryptosporidium, waterborne, supply zone, treatment works, valve, boil water; reservoir, attack rate, incubation,
  back-feed, district metered, exposure window: no slot. Supply zone and water supply: task271 v4 (insurance claims
  carried by a water authority's supply zone, a per-unit rate carried to new homes) and task402's rejected fluoridated
  zones; neither is this insight.
- Resume lines read (every slot touching the cell, the objective or the client domain): task188, task234, task236,
  task242, task248, task301, task304, task501, task149 (epidemiology), task156 (NZ water, forecasting), task211,
  task212 (in flight; its filed lowest-BIC criterion is not reused here), task213. None screened this mechanism.

## Default path

1. Read the terms of reference (section 4) and keep the line list's confirmed cases among residents with onset from
   1 September to 18 October 2027 (68 cases); probable cases and visitors fall out by the filed definitions.
2. Place each case in its supply zone through its 2023 meshblock and compute each zone's attack rate on its census
   residents, the field's routine for a waterborne signal: Kowhai Hills and Matai Valley stand far above every zone.
3. Take each zone's source from the supply zone register (issue 7, the normal arrangement) and apply section 4 on that
   arrangement for every day from 20 August to 17 October: each reservoir's cases and resident-days; the boundary
   mains, normally closed, supply nothing.
4. Rank the assets with five or more cases and confirm with the tap-water dose-response in the interviews.
5. Recommend taking the leader out of service before the renewal.

Ends on: Kowhai Hills Reservoir (R4), 9.8 per 100,000 resident-days on the register's arrangement.
Golden: boundary main WM55081 (BM3, Ferndale to Kowhai Hills), 189.5 per 100,000 resident-days, runner-up Kowhai Hills Reservoir at 10.6.

## Stump sentence

A competent solver maps the worst zones' attack rates through the supply zone register and recommends taking Kowhai
Hills Reservoir (R4) out of service, never laying each case's 1 to 12 days before onset over the supply its zone
actually had on each day, which the valve operations log rebuilds through the network model and which puts Kowhai
Hills and Matai Valley on boundary main WM55081 (BM3) from Ferndale Road's network for the wet days of 4 to 6 October,
189.5 per 100,000 resident-days against 10.6 for the reservoir.

## Three rules

- Task type: epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves anomaly detection in the taxonomy; the anomaly is the outbreak signal in two supply zones and the diagnosis names the asset that carried it.
- Domain test: the deciding quantity is each asset's attack rate among the residents its water reached in the cases' own incubation windows, the exposure-based attack rate a waterborne outbreak investigation computes; the field's routine reads exposure off the zone each case lives in and that zone's register source.
- Swap: "take the boundary main out of service, because the cases' water came through it in the days before onset" with hospital wards for zones and patients for residents stops parsing: no ward is fed through a normally closed main opened by a valve log, and no incubation window places exposure on days a ward drew from elsewhere.
- Layer 1: valve operations keyed by field tag against GIS asset numbers in the network model (the valve management system); timestamps with their offset across the 26 September daylight-saving change (the valve management system); probable cases and visitors on the line list (the surveillance system); addresses typed several ways in the CRM and the after-hours log (the customer systems); a supply zone register reissued in August with two zones renumbered (Three Waters); base-3 rounded census counts (Stats NZ). Each comes from its own system and decides nothing.
- Layer 2: estimand_identification, exposure assigned through each zone's operated supply in each case's incubation window, where the register's normal arrangement assigns it to the wrong asset; the field's method sits at rung 0.
- Decisive step: rebuilding each zone's supply day by day from the valve operations through the network model (which isolation valves were shut and which boundary valve open for most of the day) and laying each confirmed case's 1 to 12 days before onset over it.
- Not semantics: every field read correctly (the register's normal source, the valve log's tags and offsets, the case status, the census) still leaves the register route on Kowhai Hills Reservoir; no field, code or flag holds a zone's supply on a day.
- Not rule application: no filed rule names a back-feed, a supply path or a valve, and executing section 4 on the register's arrangement files Kowhai Hills Reservoir. The enumerated family (register arrangement, onset-day supply, report-day supply, the repaired main in the work orders, the nearest reservoir to the cluster, zone-week cells) spreads the call over Kowhai Hills Reservoir and the repaired feed main; the standing family (the operated supply under windows of 1-12, 1-14, 2-12 and 3-10 days, exposure from 20 August or 1 September, a case floor of 3 to 10) names WM55081 every time with the reservoir second, and the ruling-out is loud, 189.5 against 10.6.
- Analyst test: a strong analyst who cleans every file and reads every rule correctly computes zone attack rates, maps them through the supply zone register, applies section 4 on that arrangement and names Kowhai Hills Reservoir (R4), the default path's Ends on.
- Estimand: the Outbreak Control Team terms of reference (section 4, filed) fix the population (confirmed cases among residents with onset 1 September to 18 October 2027), the outcome (a case counted for an asset whose water its zone received for most of a day in the 1 to 12 days before onset), the denominator (census residents of each zone the asset supplied for most of a day, summed over 20 August to 17 October), the unit (per 100,000 resident-days), the floor (five cases) and the comparison (highest rate, runner-up next).
- No decoy: nothing is planted; the register states the normal arrangement truthfully, the repairs and back-feeds are the network's ordinary operations, no memo, draft or briefing names a suspect and the sampling results show nothing either way.
- No certified replay: no certified or published figure is reproduced to recover a method; every rate is computed fresh from the line list and the operations.
- Lesson: before naming the source of a waterborne outbreak, place each case's incubation window on the water its zone actually received, rebuilt from the valve operations through the network model, never on the zone's normal source; no build on file reads where a network's operations sent each case's exposure.

## Survivor anatomy

- Actor: the deciding property (which asset supplied a zone on a day) has no column: the register holds the normal source, the valve log tags and operations, the network model the mains; only a day-by-day reconstruction joins them.
- Link: the signal is read through a link no key offers: valve tag to GIS valve to main to zone inlet, a connected path back to a reservoir, then each case's own incubation window; no shipped key joins a case to an asset.
- Reflex: the field's method (attack rates by supply zone, sources from the register) sits at rung 0 and files Kowhai Hills Reservoir at 9.8.
- Back-test: the textbook route validates: on every day outside the repairs the register and the operated supply agree, so a solver who checks the register against the network model finds it right.
- Second use: the valve log and network model are the council's network operations record (repairs, valve exercising, the renewal plan's operations); the line list carries the case counts and the census every rate; nothing ships only for the decisive step.
- Shock: the movement the step recovers reads as ordinary operations, a three-day back-feed among dozens of repairs and back-feeds in the season; the outbreak zones are the pack's largest anomaly but the answer is no sort of any shipped statistic (a boundary main scores zero on every shipped column).
- Pins: the WHAT sits in the terms of reference (population, window, denominator, unit, floor, selection, the day convention in section 3); no filed sentence names a back-feed, a valve, an opening of a boundary main or a supply path.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 register attack rates | ToR section 4 | register source column | the field's method | none | no | yes | no | readable |
| 1 onset-day supply | no | valve log | partial | none | no | no | no | readable |
| 2 the repaired feed main | work order | work order main id | dated event | none | no | no | no | readable |
| 3 operated supply over each incubation window (decisive) | no | no | no | no | no | no | no, the log and model serve operations and the renewal | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | asset | each reservoir and each boundary main | every trunk main too | same call (feed mains rank under BM3) | ToR 4 "For each service reservoir and each boundary main" |
| SF2 | cases | confirmed, residents, onset 1 Sep to 18 Oct | probable cases counted | same call | ToR 3 and 4 case definitions |
| SF3 | attack rate | per 100,000 resident-days | per resident | same call | ToR 4 "per 100,000 resident-days" |
| SF4 | water reached | any of the 1 to 12 days before onset | weighted or 1-14, 2-12, 3-10 | same call | ToR 4 "on at least one of the 1 to 12 days" |
| SF5 | most of the day | majority of the day | noon state, any part of the day | same days (repairs straddle noon) | ToR 4 "for most of that day" |
| SF6 | day boundary | New Zealand time | UTC dates | same call | ToR 3 "a day runs from midnight to midnight, New Zealand time" |
| SF7 | residents | 2023 census usually resident | properties times occupancy | same call | ToR 4 "the 2023 census usually resident population" |
| SF8 | floor | five or more cases ranked | 3 to 10 | same pair | ToR 4 "fewer than five cases are not ranked" |
| SF9 | runner-up | next highest ranked rate | next reservoir | same asset (R4) | ToR 4 "the runner-up is the next highest" |
| SF10 | during the renewal | the planned arrangement between openings and closings | any instant of the works | one arrangement throughout | renewal plan revision B operations table |
| SF11 | each reservoir's cases | the section 4 count | cases in its register zones | different figures | ToR 4 count sentence |
| SF12 | rounding | attack rates to one decimal, counts whole | other | not the call | prompt |
| SF13 | typed since 1 July | collected 1 Jul to 17 Oct | to 18 Oct | same rows (nothing typed collected after 17 Oct) | ToR 6 month of collection |
| SF14 | complaints period | received July to September, at the customer's time | entry time | different figures | measures 4 "in the period in which the customer made it" |
| SF15 | call-out month | month notification was received | month entered | different figures | measures 3 "by the month in which notification was received" |

## Ladder

- Rungs on the shipped seed (checks.py): rung 0 register attack rates, Kowhai Hills Reservoir 9.79, every boundary main 0; rung 1 onset-day supply, Kowhai Hills Reservoir; rung 2 the repaired feed main from the work orders, FM11 (no candidate; its reservoir is R4); rung 3 operated supply over each case's window, WM55081 at 189.5, Kowhai Hills Reservoir 10.6 (lead 17.9), Ferndale Road 5.4 (R4 over R2 1.96).
- Position: the golden asset scores zero on rungs 0 to 2; every correction short of the decisive one stays on the reservoir.
- Dominance: the decisive rung moves the call by a factor of 17.9 against a carried advantage of nothing (the register gives the reservoir 9.8 and the boundary main 0).
- Pricing: (1) the residue the WHAT leaves is which water each case drank, a reconstruction, not a knob; (2) the move is the whole call, 189.5 against 9.8; (3) no one-group-by route, the supply is in no column; (4) the golden's rate rests on 61 cases, a Poisson error near 13 per cent against a lead of 17.9; (5) the lever is not the ranked quantity's noise; (7) no subset prints the supply; (8) the reflex sweep runs as code (checks S3 to S5).
- Screens (generator/screens.py, 40 redraws): golden = truth 40/40, lead min 3.80; golden variants 20/20; first look and every careful reader wrong 40/40 (## Draw).
- Graded set: 17 main figures (the asset, its rate, the runner-up and its rate, six reservoirs' cases and rates, the residents through it during the renewal) and 23 ask figures; tightest bin edge 0.077 (non-urgent attendance, August).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | confirmed resident cases, onset 1 Sep to 18 Oct | filed, ToR 3 and 4 |
| 2 Unit of account | a case per asset | filed, ToR 4 counts a case once per asset |
| 3 Attribution window | 1 to 12 days before onset | filed, ToR 4; C1 across windows |
| 4 As-of dating | records exported 07:40 19 Oct | filed, ToR 7 |
| 5 Version basis | the register's issue 7 | one issue ships; normal arrangement only |
| 6 Denominator | census residents of supplied zones, by day | filed, ToR 4 |
| 7 Weighting | none, cases counted | filed, ToR 4 |
| 8 Window length | exposure 20 Aug to 17 Oct | filed; C1 against 1 Sep (check S2) |
| 9 Boundary inclusivity | inclusive dates | filed wording "from ... to"; no record on an edge |
| 10 Rounding path | rate rounded once at the end | prompt |
| 11 Tie-break | none needed, lead 17.9 | C1 |
| 12 Maturity and censoring | cases notified by 18 Oct | filed population; same call under every window |
| 13 Order of operations | supply per day, then windows | one order reproduces |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | one row per case on the line list | surveillance system's own case ids |
| 16 Identity normalisation | valve tag to GIS valve | the network model's own valve sheet |
| 17 Netting against gross | none | not applicable to counts |
| 18 Dimensional units | residents and days | one unit throughout |
| 19 Code and status semantics | Confirmed and Probable | ToR 3 definitions |
| 20 Integerisation | counts | C1 by construction |
| 21 Clause scope | section 4 applies to reservoirs and boundary mains | filed |
| 22 Forward window contents | the renewal's planned operations | shipped plan revision B |

## Literal reader

Executing the prompt and section 4 word for word on the register's arrangement files Kowhai Hills Reservoir, and on
the supply each zone received for most of each day (the valve log read through the network model) files WM55081; the
register is filed as the normal arrangement in its own title, so "received the asset's water" reads as the operated
supply, and every other reading in the fork table gives the same call or breaks a quoted sentence.

## Oracles

None on the call: the sampling results, the treatment plant log and the rainfall agree with every reading; the
register agrees with the operated supply on every day outside the repairs, a second source that agrees with the wrong
reading too.

## Ask sheet

- Ask 1, testing (community laboratory export, reference laboratory typing report; 2 files, 27 columns): residents tested in July 112, August 117, September 166, 1 to 17 October 192; typed since 1 July, C. parvum 28 and C. hominis 3. Home: qualifier (the rise is not a testing change) and audit trail. Primary D7 on the tested block: residents with a dormant NHI on one specimen and the live NHI on another, the person worked out from name and birth date. Primary D2 on the typing block: the typing report supersedes the community "referred" result and reaches it only through the accession inside a free-text reference (five formats) or through name and birth date, NHI on 55 per cent of rows. Hazards: visitors' specimens, amended reports. Pin test: the ToR files residents, the month of collection and once a month; the devices sit in which rows are one person and which typing belongs to which specimen.
- Ask 2, complaints (CRM export, website reports, rating database; 3 files, 24 columns): July to September per 1,000 connections, clarity 1.73, taste 0.85, odour 0.47, pressure or flow 0.66, continuity of supply 0.60 (31,750 connections). Home: the regulator's measure for the quarter the outbreak follows. Primary D5 on pressure and continuity: contacts from rural-scheme and private-supply properties, out of scope only through the rating database's supply type, reached from addresses typed several ways. Primary D1 on clarity, taste and odour: website reports lost in the 16 August to 3 September integration outage, two thirds keyed again by hand days later as email or phone contacts with the address retyped and no case link. Pin test: the measures file the counting unit and the customer's time; the devices sit in which contacts are one complaint and which property a contact came from.
- Ask 3, call-outs (service requests, crew job times, after-hours call log, work orders; 4 files, 24 columns): July, August, September medians, urgent attendance 37, 38, 43 minutes, urgent resolution 193, 195, 197 minutes, non-urgent attendance 20.3, 27.7, 27.6 hours, non-urgent resolution 37.0, 42.7, 40.5 hours. Home: the regulator's response measure for the network that ran the repairs. Primary D8 on the urgent block: after-hours requests entered at the next morning's import, notification being the after-hours service's call, matched by address and night with no reference. Primary D4 on the non-urgent block: requests done with planned maintenance carry no crew job, their times only in the next planned work order on their street. Hazards: crew times in UTC across the daylight-saving change; imports from the website and email.
- Main population: no ask device row sits in the line list, census table, register, network model, valve log, renewal plan or terms of reference (checks X1).

| Ask row | Cracker figure | Full includer figure | Golden | Cracker |
|---|---|---|---|---|
| ask 1 tested, by NHI | 128, 128, 175, 199 | the same | 112, 117, 166, 192 | miss |
| ask 1 typing, joined on NHI | 16 and 2 | the same | 28 and 3 | miss |
| ask 2 scope and duplicates | 1.80, 0.88, 0.50, 0.79, 0.66 | 1.64, 0.76, 0.41, 0.57, 0.50 | 1.73, 0.85, 0.47, 0.66, 0.60 | miss |
| ask 3 urgent, import time with impossible rows dropped | every urgent median off | every urgent median off | 37, 38, 43 and 193, 195, 197 | miss |
| ask 3 non-urgent, requests without crew jobs dropped | every non-urgent median off | every non-urgent median off | 20.3, 27.7, 27.6 and 37.0, 42.7, 40.5 | miss |
| full includer, all 23 figures | | 0 of 23 | | miss |

Pair ceiling: 28.5 with one response on the call and one off (45.0 with both on); the full includer keeps 0 of 23.
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/ceiling.py, run on the cut pack.

## Build record

- **Pack.** 20 files in council/, laboratories/ and public_health/, as the three organisations supplied them; csv,
  xlsx, pdf and parquet; the rating database at 33,218 rows; distractors (rain gauges, compliance samples, plant log)
  in metadata.json. Each workbook and PDF carries its own issue or export stamp in the setting (checks H13).
- **Gates on the cut pack, 2026-11-07.** Generator checks 72 of 72; two consecutive builds byte-identical (target/,
  golden/, target.zip, figures.json, metadata.json); figures_check 54 of 54; precut 61/0/0; voice-check PASS; leak.py
  REVIEW, no LEAK (the terms of reference, the register and the renewal plan name the assets and places the question
  is about; no document ranks them); producer audit clean in the 2024 to 19 October 2027 band; guard surface 0
  promoted (nearest 0.040, task213, pct 17); guard heart WARN on overuse.org_family, overuse.objective and
  overuse.gate_g, each answered in the Draw, and on repeat.deliverables (docx and xlsx, as task211 v2 shipped):
  kept, because an outbreak control team's brief with its workbook is the genre's own pair and the shell differs
  from every held build on its question form (what) and second-sentence opener (before).
- **Goldens.** outbreak_source.xlsx (source assessment, testing, complaints, call-outs, notes) and a one-page
  incident_brief.docx whose chart marks the three days the boundary main fed Kowhai Hills and Matai Valley; every
  figure is read from figures.json, the same values block 4 states.

## Tried and rejected

- 2026-11-07, paper: data skew read from input size (a column; the Mantri reflex reaches it).
- 2026-11-07, paper: upstream lateness from the dependency log as the decisive step (one join; critical path is the
  field's own method, so it sits at rung 1).
- 2026-11-07, paper: the trigger's launch delay as the decisive step (a stated rule executed: rule application).
- 2026-11-07, paper: the backup's remote-read penalty (a locality column makes it schema-readable).
- 2026-11-07, paper: credits avoided across families through the dependency graph (the step settles which credits
  count, the population: the WHAT screen kills it).
- 2026-11-07, paper: the cap as concurrent slots in correlated bad nights (a stated cap executed: rule application);
  commit-lock waits (indeterminate); cold image pulls on deploy days (an aggregate spike around dated events).
- 2026-11-07, prototype v1 to v8 (scratch t214/proto): the golden's before and after windows starved on fail-slow
  hosts; the naive culprit rules (slowest co-tenant, contemporaneous magnitude) landed the call while disk-bound
  shards of the winning families shared fail-slow hosts with each other; fixed by the platform's own placement
  (anti-affinity within a job, the search index on its dedicated storage nodes) and workload mix (CPU-bound general
  families), not by wording.
- 2026-11-07, candidate 1 SPENT at screen 4(c), never registered: the reverse-causality straggler (a heavy
  card-settlement shard slows its own host's co-tenants while it runs, so the bad-machine check credits a backup
  that would rerun the same work; the golden read the host's co-tenants before the shard started and after it
  ended). v9, 20 redraws: golden = clean truth = payments clearing + regulatory reporting 20/20, lead min 1.197,
  median 1.391; credits paid, every late job with a straggler, the textbook replay, the host check, magnitude,
  slowest co-tenant, per-record host x hour residual and host-night straggler count all wrong 20/20; but the
  per-record reader with host x night cells, reading the residual as the shard's own work, reached the golden set
  20/20, and the golden's both-sides variant held only 14/20. v10 (skew 3 to 18 times, fail-slow 4 to 72 hours):
  host x 4-hour and x 8-hour residual readers 20/20, host x night 16/20, golden lead median 1.158 (14/20 under
  1.2), both-sides variant 0/20. Why it dies: the information that decides (the host's state outside the
  straggler's run) is a host-by-time aggregate, and any cell wider than a heavy shard's run and narrower than a
  fail-slow episode separates the two; no realistic setting separates them in time without starving the golden's
  own before and after test. A copy escapes exactly the host component, so a correct host-versus-rest
  decomposition by cells is a correct method, which is the blind route.
- 2026-11-07, queued on paper after candidate 1 (not yet screened): (a) a commit wait behind another family's write
  to a shared output table read from heartbeat trajectories (risk: output-table x time cells recover it); (b)
  shard-level input waits through the catalogue's shard-to-part mapping (risk: the field's critical path at shard
  level is a reflex); (c) a self-dependent job whose late night pushes the next night's start (risk: a careful
  dependency replay is the field's method). Preferred next: transient stalls (escaped by any fresh copy) against a
  shard's heavy nights set by its clients' own cycles through the client-to-shard table (repeated by every copy),
  which no host-time cell, day-of-month interaction or lag reveals (pipeline.json resume).
- 2026-11-07, the Larix world SET ASIDE (seed AD37 dropped) before any second candidate: its only honest Anomaly
  Detection home is General Statistics & Data Science's exploratory-data-analysis-distribution-assessment, held by
  task212 in flight; the draft card reached it through the house label business-operations-analytics, which clears
  ban.pairing only by its label, and a card is never relabelled to pass a ban. Candidate 1's measured death stands
  above. The build moves to Epidemiology & Public Health, a new world and dataset (## Draw); world.py, method.py and
  screens.py are replaced with the new world's harness.
- 2026-11-07, paper, at the new draw (each before any harness): residual patrol deterrence for hot-spot selection
  (dead in task182 architecture 8); care-home outbreaks seeded by staff working across homes, and float nurses
  carrying colonisation between wards (both read as task181's shared step adding risk to the cases it handles, and
  outbreak counts per home are too sparse for a 19 of 20 separation); a surgeon's learning curve counted across a
  national audit (healthcare delivery, more spent, and a career total is an aggregate view a strong reader takes
  first); physiotherapy visits after each patient's functional plateau (the plateau threshold is either filed, rule
  application, or open, a fork); releasees' loss of tolerance behind an overdose excess (excluding releasees lands the
  call); susceptible reconstruction after past epidemics (a time-since-epidemic marker reaches it); a food lot on the
  shelf by first-in first-out stock rotation (the practice is either filed, a replay, or withheld); a pool's
  contaminated days (pool-by-day cells reveal it); continuous blending at zone boundaries from inlet meters (a
  zone-by-hour aggregate of one table).
- 2026-11-07, stage 3: the flat target layout, promoted against task213 on guard surface at 0.100 (layout and format
  set only, both flat with csv, xlsx, pdf and parquet); the files now sit in the three organisations' folders.
- 2026-11-07, stage 3: the prompt's second sentence opening on "Send" (shell which, send, docx and xlsx repeated
  task186 v1 on guard heart); it now opens on the date ("Before then"), and the question asks what must come out of
  service (the form which repeated task212 v1).
