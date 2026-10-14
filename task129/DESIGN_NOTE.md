# task129 design note

Architecture 2 is current: drawn 2026-10-14 at the author's request. Architecture 1 (Sønderå Medier's page-delivery
service level, shipped 2026-10-13) sat in a house domain (business operations, client domain General Statistics)
though its decisive method was web performance engineering, which no client domain carries, so its domain read as a
backdrop; its record is kept under the Architecture 1 record heading below and its identity in the card's lineage.
Architecture 2 keeps Root-Cause Analysis and moves to Energy Systems & Utilities, grid reliability outage analysis,
with two analytical layers on the call.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task129.json`, architecture v2, drawn and registered 2026-10-14.
  Domain Energy Systems & Utilities (client domain), task type `grid-reliability-outage-analysis` (serves Root-Cause
  Analysis and Anomaly Detection), objective Root-Cause Analysis: the call names the driver of each district's rise
  in tree-caused outages, every rival ruled out on evidence. Shape 07 (grid): each district's tree-caused outage rate
  per 100 miles of overhead primary in each year 2021 to 2025, beside the three district calls. Decision
  `root_cause_named`, question form what. Gap population (the units a rate is read on), then time (the regrowth
  clock); no A to E pattern; generators G4 (attribution at a handover), G14 (a rate read at the same time since trim
  and the same trees within falling distance). Gate G `decomposition_attribution`: the reported rise is correct, and
  the work is booking it to the right driver. Strategy `decomposition_attribution`. Layer 2 family
  `estimand_identification` (the right comparison: the outgoing contractor's work of the same months, and every unit
  read at the same time since trim). Calibration none. Context artifact `filed_standard` (the cooperative's
  right-of-way maintenance policy and its reliability reporting policy).
- **World:** Vessey County Electric Cooperative, a member-owned rural electric cooperative in a fictional United
  States county, serves its members over overhead primary lines in three districts (North, East, South). Its
  right-of-way is trimmed on a four-year cycle by contract crews, each district's trim units (about half a mile of
  line each) worked circuit by circuit. Trimming clears the right-of-way; a tree standing beyond it is reached only by
  the hazard-tree removal the policy describes. North's trimming passed from the outgoing contractor to a new one on 1
  July 2024, the outgoing contractor finishing the work orders it already held; East's passed on 1 April 2025 after the
  outgoing contractor stopped taking new work orders in January; South kept its contractor. The Manager of
  Right-of-Way and Vegetation Management sets the 2027 right-of-way programme for each district this autumn.
- **Pairing:** the deciding quantity is each district's tree-caused outage rate read as vegetation management reads it:
  on the regrowth clock (time since each trim unit was last trimmed, built from the trimming history) and against the
  trees within falling distance of the line (the span-level right-of-way survey), with the new contractor's work read
  against the outgoing contractor's work of the same months. A noun swap leaves nothing to stand on: no regrowth
  since a trim, no right-of-way with trees standing beyond it, no ash mortality falling in from outside it.
- **Data-native sentence:** trimming clears only the right-of-way, so ash dying beyond it falls onto the line whatever
  the time since trim, and in North that mortality reached the line in the months the new contractor took over; the
  rise therefore shows on the units the new contractor trimmed, and only the units the outgoing contractor trimmed in
  the same months, with every unit read at its own time since trim, show it as a shift no trimming removes. East's
  handover left the units due that spring past the four-year cycle, so East's rise sits on the regrowth clock, and
  South's follows the year's storms.
- **Personas:** drawn with `guard.py names --locale en_US --seed 129`: Lori Rodriguez (Manager of Right-of-Way and
  Vegetation Management), Dennis Garcia (Reliability Engineer), Wesley Thomas (Right-of-Way Forester), Brian
  Montgomery (Manager of Operations).
- **Guard:** `check` PASS at registration (ban windows against task230, task459 and task184); `heart` PASS. Two
  first names drawn first (Pamela, Jessica) warned against task131 and task104 and were redrawn from the same pool.
- **Sources, one line each.** The client's two-layer standard: its canonical expert move is a staggered rollout read
  against units not yet treated; here the not-yet-treated units are the outgoing contractor's units of the same
  months, and the move is only half the call, because the shift it uncovers still has to be read on the regrowth
  clock and the trees within falling distance. `strategies.md` F8 (attribution: a correct movement booked to the
  visible owner): the visible owner is the contractor that took over, the shared external driver is ash mortality
  beyond the right-of-way. F1's legal form (a clock process estimated from every unit that went through it) supplies
  the regrowth clock, which East's call stands on. The dead list's dated-cause warning: the handover is a dated cause
  whose step an event study finds, which is why it is the wrong answer here and the decisive driver is a chronic one
  with no date. task121 v3 (exposure set against the same unit's exposure at the same clock hours on other days) and
  task13 (outcomes re-attributed by physical evidence over a filed reason label) spend other insights: here every
  outage's cause code is right and no label is overturned.

## Default path

1. From the outage management export (restoration-step rows) take each outage once, keep the sustained outages
   (over five minutes) on overhead primary whose cause is TREE, and drop the major event days the reliability
   reporting policy identifies by the IEEE 1366 2.5 beta method from the five years before each year.
2. Divide each district's count by its overhead primary miles in service that year (trim-unit register, in-service
   and retirement dates) for the rate per 100 miles in each year 2021 to 2025.
3. North's rate steps up from the second half of 2024 and nearly doubles in 2025; East's jumps in 2025; South's
   rises a little.
4. Read the trimming contract register: North passed to a new contractor on 1 July 2024 and East on 1 April 2025;
   South kept its contractor. Read the weather: South's 2025 had more days of high gusts.
5. File the call: re-bid the trimming contract in North and in East; nothing new in South (storms).

Ends on: North re-bid the trimming contract, East re-bid the trimming contract, South nothing new
Golden: North hazard-tree removal beyond the right-of-way, East catch-up trimming, South nothing new

## Stump sentence

Reading each district's rise against the trimming contract register files a re-bid of the trimming contract in
North and East and nothing new in South (Ends on: North re-bid, East re-bid, South nothing new); the step that lands
it there is booking North's rise to the new contractor whose freshly trimmed units carry it, when the outages come
from ash dying beyond the right-of-way, rising by the same amount at every time since trim and with the ash standing
within falling distance, so the outgoing contractor's units trimmed in the same months fail alike, and booking East's
to the contractor, when its rise sits on the units the handover left past the four-year cycle.

## Three rules

Task type: `grid-reliability-outage-analysis` (Energy Systems & Utilities), which serves Root-Cause Analysis in the
client taxonomy; the call names each district's driver of a correctly reported rise in tree-caused outages.

Domain test: the quantity that decides each district's call is its tree-caused outage rate read the way utility
vegetation management reads it, on the regrowth clock (time since each trim unit was last trimmed, from the trimming
history) and against the trees within falling distance (the right-of-way survey), with the new contractor's work set
beside the outgoing contractor's work of the same months.

Swap: "what drove the rise in falls on each of the hospital's three wards, and should each ward's budget fund
catch-up rounding, a re-bid of the agency nurses, removal of hazards beyond the ward, or nothing" stops making sense:
no regrowth runs from a rounding, no cleared corridor has hazards standing beyond it, and nothing dies outside a ward
to fall into it.

Layer 1: an outage management export at restoration-step grain in local time across daylight-saving changes (the
cooperative's outage system); a trimming completions register with completion and acceptance dates, the contractor
and units renumbered where a line was rebuilt (the contractors' work-order system); a span-level right-of-way survey
by species group (the forester's survey); overhead mileage that changes as units go underground (the trim-unit
register); daily peak gusts in UTC from three weather stations; the IEEE 1366 major event day rule applied from each
year's five prior years (the reliability reporting policy); contractor invoices with credit memos and re-issued
invoice numbers (accounts payable). Nothing is placed to be caught; each mishandling is asserted to leave the three
calls where they are.

Layer 2: `estimand_identification`: the right comparison for a rise that begins with a handover is the outgoing
contractor's units of the same months, and every unit read at its own time since trim; North's rise is then a shift
the regrowth clock does not carry, scaling with the ash within falling distance, and East's sits on the units past
the cycle.

Decisive step: reading North's 2025 tree-outage rate at the same time since trim and the same months for both
contractors' units, and against the ash standing within falling distance, which shows a shift that no trim removes
(trees falling in from beyond the right-of-way) where the district series shows a step at the handover.

Not semantics: every outage's cause code (TREE) is right, every field reads as the dictionary says, and no field
separates a tree growing into the line from one falling onto it; read correctly, the district series and the
contract register still point at the new contractor.

Not rule application: the right-of-way maintenance policy files the four-year cycle and what trimming clears, and the
reliability reporting policy files the rate and the major event days; executing both gives each district's rate and
leaves the driver open, and no filed rule or procedure reads a rise against the outgoing contractor's concurrent
units, the regrowth clock or the trees within falling distance.

Analyst test: a strong analyst who counts outages (not restoration steps), drops the major event days, rates each
district per 100 miles in service, reads the rise against the contract register and checks the storms files the
default path's answer (Ends on: North re-bid the trimming contract, East re-bid the trimming contract, South nothing
new); `checks.py` runs it on the generator's clean truth.

Estimand: the reliability reporting policy defines the tree-caused outage rate (sustained outages on overhead primary
with cause TREE, outside major event days, per 100 miles of overhead primary in service in the year); the call names,
for each district, the driver that accounts for most of its 2025 rate above its 2021 to 2023 average, and the
programme the right-of-way maintenance policy assigns to that driver.

No decoy: no memo, briefing, draft or stakeholder figure argues for a re-bid, a cycle change or the storms; the
contract register records the handovers as the cooperative's own contract history, the invoices record billing, and
nothing in the pack names a cause for any district's rise.

No certified replay: no published or certified figure is reproduced to recover a method; the reliability report's
indices are the rule the rates are computed under, and the driver is estimated from the records.

Lesson: a rise that begins with a change of provider is read against the outgoing provider's work of the same months
and on the asset's own clock before it is booked to the newcomer; no build on file teaches vegetation outage
attribution or a handover read against concurrent outgoing work.

## Architecture 1 record (re-rooted 2026-10-14)

Architecture 1 (Sønderå Medier's page-delivery service level: which shipped change the operations squad fixes in Q4)
as it stood when it shipped on 2026-10-13; it binds nothing. Its generator, pack and goldens stay in git history.
The original title was "task129: which shipped change gets Sønderå Medier's Q4 operations squad".

Drawn 2026-10-10 from the world, decision and quantity of seed RC02 (`analytical_tasks/06_root_cause/`), the
pitfall re-found from the data. Reworked 2026-10-12 under the client's 10/10 rules (wave 1, resume 2): the
decisive step was always analytical and is kept; the organs that read as plants were cut (the closed-fix
roster's resemblance to the wrong answer, the service level's sentence licensing the page-weight basis, three of
four voices), the ask layer was rebuilt on silent devices, and the prompt was rewritten question-first. This is
the build's one design note.

### Draw

```
Domain: business-operations-analytics (house), subdomain service-operations-sla; client domain
  general-statistics-data-science, task type interpretability (root-cause)
Objective: Root-Cause Analysis   Shape: 11 (before and after with a control)   Decision: root_cause_named
Gap: population (decisive), objective, time   Pattern: E (decisive), D   Gate G: decomposition_attribution
Stump strategy: composition_mix   Layer 2: estimand_identification,
  own:separating-group-effects-carried-within-a-state-built-from-record-order
Stakeholder: head of digital operations at a regional news group (operations_director), who owns the
  page-delivery service level and assigns the operations squad's quarter
Forum: committee_or_panel (the quarterly service review, 17 September)   Forcing event: budget_or_appropriation
  (the review's allocation of the squad's Q4, which opens 1 October)   Org family: media_or_publishing
Context artifact: close_out_summary (digital operations' Q3 service close-out, July and August by title)
Calibration organ: none   Opening move: question-first   Question form: which
World: Denmark, DKK; Sønderå Medier (three daily titles on one web platform, metered paywall, ad-free
  subscriber layout); Bølge, the redesign programme. People from guard.py names --geo Denmark --seed 129.
Spine: rum_mobile_views_2026.parquet, about 2.8 million beacon rows, one sampled page view per row
Deliverables: q4_squad_call.pptx (the call on the first slide), q4_squad_call_workings.xlsx (the asks)
Criteria (shape 11): the call 4 (change, its figure, runner-up, its figure); the three dated changes by
  title 9; image requests and kilobytes per mobile page view, March to August, 12; the first slide 1;
  the two files 2: 28
```

As-of date 2026-09-07. The August extract lands on 5 September, the review meets on 17 September and the squad's
quarter opens on 1 October. The call faces forward (the change Q4 fixes); its figure is valued at August's traffic
because the service level values a fix at the latest full month's traffic, a filed convention rather than a
forecast, so the objective stays Root-Cause Analysis.

**Data-native sentence.** A content-hashed platform bundle is re-issued at every release-train deploy, so each
device's first view after a deploy downloads and compiles the new bundle while its later views reuse it from cache,
and the two groups that separate the ad stack from the front end (daily puzzle players, signed-in subscribers) come
back many times between deploys while most ad-supported views are a device's only visit in that interval: the state
that moves each change's cost is a property of the order of each device's views, and the two groups and the base
hold it in opposite proportions.

**Guard.** `guard.py check` on the reworked card: WARN, exit 0 (neighbours in draw order task119, task122, task126).
The rework redrew the forcing event from vote_or_meeting (BLOCK against task122) to budget_or_appropriation, set
calibration_form none and validated_decoy false (the roster is gone), and added differentiation lines for task500 v2
(test.same_puzzle_older) and task73. WARN answered: repeat.gate_g (decomposition_attribution against task122): the
call apportions one joint effect between two changes that only shipped together, which is what the label names;
task122 scored an experiment's lift on borrowed orders, so the label repeats and the construction does not. Nearest
drivers 0.08 (task98 v4 lineage), 0.07 (task121 v1 lineage, task230 v1, task44 v2); `guard.py heart`: WARN.
`guard.py surface` promotes task36 on labels alone (population gap, pattern E, decomposition_attribution, root_cause_named; surface 0.077, corpus percentile 47): task36 names one standing cause of a distributor's delivery decline by removing the loud leader through a filed agreement and netting a dated candidate against a structural property a file records; task129 has no filed removal and no recorded property: it splits the joint effect of two changes that only switched on together, and the per-view state that decides the split is built from the order of each device's views against the release train.

**Similarity.** No build on file splits the joint effect of two co-shipped changes on a per-view state built from
the order of each unit's records against version changes, with the two changes costing opposite states. task73's
retention redraw standardises a partial-exposure group to the base's visible composition, which is this build's
default path and its wrong answer. task447 and task448 carry a rate within a stratum the records name (terms in
force, filing route); here the stratum is in no record and must be built. task44 v2 carries one pilot's pooled gain
across a moderator; here two separating groups carry two causes' effects and the moderator flips which cause leads.

**Sources.** RC02 gave the world (a publisher's slow mobile pages), the decision (which change to fix) and the
quantity (views brought back); its CPU-class standardisation through a device registry is kept as this build's
default path, not its stump. Measured traps #13 (validates on one population, applies to another) and #11 (beats the
headline trap, misses the quiet one) in `stumping/references/client/measured-traps.md` are the family; the in-house
record is FC01 and OS01's held calls on the same pairing.

### Default path

The pipeline a competent analyst builds from the prompt's words, the service level and the files' grain:

1. Read the service level (a view misses the line when its largest contentful paint exceeds 4.0 s, views with no
   paint timing are not scored, before-and-after reads use the 28 days either side of the release that switched a
   change on, a fix is valued on the mobile views it brings back at the latest full month's traffic), the paywall
   terms, the change register, the release train log and the Bølge rollout log.
2. Build the mobile view frame: phones through the device registry, scored views, each page view once, rows
   weighted by `sample_weight`, Copenhagen days.
3. Event study at the three dated releases (fonts 3 March, image pipeline 7 April, banner 5 May): the share's step
   over 28 days either side, valued at August's scored views (banner about 428,000, image pipeline 327,000, fonts
   271,000 views a month).
4. Align the six Bølge template groups on their switch-on releases: the ad stack and the front end together add
   4.74 points on ad-supported views, about 1,707,000 views a month at August's traffic.
5. Separate them with the puzzles pages (the ad stack alone from 24 June) and subscribers' ad-free views of the
   redesigned templates (the front end alone from 30 June, found through the subscription register): read raw the
   two effects sum to 4.27 points against the joint 4.74.
6. Standardise both groups to the ad-supported views' phone mix through the registry's benchmark band: the split
   now sums to the joint ramp to within 0.02 point.
7. Value each fix on the views it acts on (the ad stack on ad-supported redesigned views and the puzzles pages, the
   front end on every redesigned view) at August's traffic.

Ends on: A, the header-bidding ad stack, 1,230,000 views a month, runner-up C, the front end, at 800,000
Golden: C, Bølge's front end, 1,460,000 views a month, runner-up A, the ad stack, at 610,000

### Stump sentence

A competent solver aligns the six Bølge template groups for the joint effect of the ad stack and the front end,
separates the two with the puzzles pages (the ad stack alone) and subscribers' ad-free views of the redesigned
templates (the front end alone), standardises both groups to the ad-supported views' phone mix through the device
registry, which closes the joint ramp to within 0.02 point, and names the ad stack at 1,230,000 views a month with
the front end second at 800,000; the step that lands it there is carrying each group's effect to the ad-supported
views as one figure per phone class, when the front end costs a view mostly on a device's first view after a
release-train deploy and the ad stack mostly on its later views, and both separating groups are about a quarter
first views against about three quarters on the ad-supported views, so carried within that state the front end's
fix brings back 1,460,000 views a month and the ad stack's 610,000.

### Three rules

Task type: general-statistics-data-science interpretability (root-cause): attributing an outcome to two causes that
only ever occurred together, where a marginal reading of each cause's effect misattributes and the conditional one
is required (the library's correlated-features pattern), worked in a news group's page-delivery operations.

Domain test: The deciding quantity is each co-shipped change's attributable over-line rate on the mobile views its
fix acts on, which web performance engineering estimates from staggered real-user monitoring with partial-exposure
groups; the field knows a change's cost on a view depends on whether the view downloads and compiles a new bundle or
reuses it from cache, so the groups' effects travel to the base only within that state, and a generalist carries
them on the visible device mix instead.

Swap: "Which of five changes gets the operations squad's quarter, and how many mobile views a month does its fix
bring back under the line" rewritten for a hospital ("which of five process changes gets the improvement team's
quarter, and how many discharges a month does its fix bring back under four hours") loses the mechanism: no
content-hashed bundle is re-issued at every release, so there is no first-view-after-a-deploy state to split the two
changes' costs, and the call stops making sense.

Layer 1: The RUM collector's history in the rows (tablets forwarded until 4 May, one title's app-webview beacons
forwarded twice under one page-view key, a local-edition tag container that sent a second beacon from an older
library from 16 March to 6 April and again from the container version restored on 4 May to 26 May, a sampling change on 3 June carried in `sample_weight`), UTC beacons against a release train logged in Copenhagen time with offsets across
the summer-time change, device models resolved through a registry that lists tablets beside phones, subscriber
status from an effective-dated register by account, two local editions re-mastheaded in January (effective-dated, before the export opens), and an image CDN
log split by edge hits and origin fills with a fallback vendor reporting kilobytes and the group app's native screens
in the smartphone class; every item is what the collector, the CMS, the tag manager or the vendor produces, and none
moves the call (asserted per item).

Layer 2: Estimand identification by transport: the two separating groups' effects are carried to the views each fix
acts on, and the conditioning set decides the call; the visible phone class balances the groups and the base on the
registry's bands while the state that modifies each change's cost (a device's first view after a deploy against its
later views) stays at about a quarter in the groups and three quarters in the base, which flips the named change.

Decisive step: Build each view's state from the order of its device's views against the release train's deploy
times, measure each separating group's effect within phone class and state, and carry those effects to the
ad-supported views' own state and phone mix (the front end's also to subscribers' views, the ad stack's also to the
puzzles pages), so the front end, whose cost falls on first views, brings back the most views.

Not semantics: Every field in the export, the registry, the registers and the logs means what the field guide and
the headers say, and a solver who reads all of them correctly still standardises on phone class and names the ad
stack; the state is in no field, code, unit or definition: it is constructed from view order against a second
file's timestamps, and choosing it as the conditioning set is the analysis.

Not rule application: The service level files the line, the scored population, the 28-day reading window and the
valuation (views brought back at the latest full month's traffic), the paywall files which layout carries ads, and
executing every one of them on the phone-standardised split files the ad stack; no filed rule says how to separate
two co-shipped changes or what to carry the separating groups' effects on.

Analyst test: A strong analyst who cleans the export, reads every filed rule correctly, aligns the six template
groups on their releases, separates the ad stack and the front end with the puzzles pages and subscribers' ad-free
views and standardises both groups to the ad-supported views' phone mix so the split closes the joint ramp, still
names the header-bidding ad stack at about 1,230,000 views a month with the front end second at 800,000.

Estimand: page_delivery_service_level_v3.pdf: section 1 (a mobile view is a page view on a phone in the device
registry), section 2 (a view misses the line when its largest contentful paint exceeds 4.0 seconds; views with no
paint timing are not scored), section 3 (before-and-after reads use the 28 days either side of the release that
switched the change on) and section 4 (a fix is valued on the mobile views it brings back under the line at the
latest full month's traffic, so August 2026), across the five changes the prompt names; the paywall terms (4.2 and
4.3) fix which views carry the ad stack.

No decoy: Nothing is planted to be caught: no document ranks or argues for a change, the close-out reports July and
August by title without attributing anything, no document licenses page weight or any other basis, the prep thread
carries the review's timing and the export's contents and states no view on any change, and no copied block, memo,
draft or stakeholder figure carries the ad stack.

No certified replay: The method is not hidden and recovered from certified or published figures: the pack holds no
closed-case corpus, the close-out and the joint ramp tie under the default path and the golden alike, and the
state-conditioned transport is forced by the separating groups' own records (each group's effect differs sharply by
state once the state is built, and the base holds the states in another proportion), not by reproducing a figure.

Lesson: An effect measured on a partial-exposure group carries to another population only within every modifier
whose mix differs between them, including one no column holds that has to be built from the order of each unit's
records against version changes; no build on file teaches transport on a state constructed from record order
(task447 and task448 condition on a stratum the records name, task44 v2 on a moderator inside one pilot, task73
stops at the visible composition that is this build's wrong answer).

- **Litmus: no.** Every number in the pack is correct: the joint ramp, both separating groups' effects read on their
  own views, the dated steps, the close-out. Nobody quotes a ranking of the five changes. The difficulty is that the
  two groups are not miniatures of the views each fix acts on, on a state no column carries.
- **Deletion tests.** Delete the thread, the close-out and every distractor: the beacons still show a cohort-staggered
  joint ramp, both groups still read the ad stack ahead once standardised on phone class, and nothing says a view's
  cost depends on whether it is its device's first after a deploy. Clean-data test (asserted per suspect file): with
  the collector's history repaired (tablets, both kinds of repeated beacon, the tag gap), the answer and the default
  path's answer are unchanged and still apart. Lens swap: the default path carries each group's effect at that
  group's own state mix; the answer carries per-state effects to the base's state mix; different populations, not
  one population under two lenses. Identity test: the joint ramp closes over shipped quantities, the split does not.
  First moves (one-period group-by, the event study, the separating groups raw and standardised, every visible
  covariate) all land on the ad stack or on the banner.

### Decisive rung

Measured trap #13, validates on one population and applies to another: each separating group's effect fits every
view it can be checked on and is carried to views that differ on one axis, with the evidence of the difference left
in the record (the order of each device's views against the deploys). Behind it, #11, beats the headline trap and
misses the quiet one: the phone-mix residual is the headline trap, standardising on the registry's band closes the
joint ramp to within 0.02 point, and the solver stops confirmed. The decisive rung changes the named change, not
only its size: the default path's figure for the golden's change (800,000) and the golden figure (1,460,000) sit
44 per cent apart, and the named change moves from the ad stack to the front end.

### Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene battery | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the event study at the dated releases (names the banner) | fires: the service level's 28-day reading at each release | fires: the release train log dates each change | fires: the opponent's first field move | no | no | fires: one difference per release | readable |
| R1, the default path (stump): cohort-aligned joint ramp, separating groups, phone-standardised (names the ad stack) | fires: the rollout log and the paywall terms point at cohorts and the ad-free layout | fires: the registry joins on the model string, the subscription register on the account key | fires: standardise a group to the target's visible mix | no | no | no | readable |
| R2, the landing proxy: first view of a 30-minute visit as the first load, within phone class (names the ad stack) | no | no | no | no | no | no | silent |
| R3 (decisive): the state built from each device's view order against the deploy times, per-state effects carried to the base's state and phone mix (names the front end) | no: no sentence says a view's cost depends on a cached bundle, that a deploy re-issues it, or how often either audience returns between deploys | no: no column carries the state; it is a sort and rank on the spine against an as-of join to a second file's timestamps | no: standardising on phone class, referrer, connection, navigation type, title, hour or weekday leaves the ad stack in front (asserted per column) | no: nothing scores a transport, and every split ties to the joint ramp under the default path and the golden | no: counts, joins and control totals reconcile identically under R1 and R3 | no: a constructed state, effects per state inside two groups, then a reweighting to a third population | silent |

The decisive rung's honest exposure is the release train log's bundle hash column: a solver who asks what a new hash
means for a device that comes back finds the state. That is the intended discovery path; the log is an operational
record with no commentary.

### Semantic fork table

| Id | Term or convention in the main ask or computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "mobile views" | page views on a phone in the device registry | phones and tablets | same call: no tablet row from 4 May, before every main window (asserted zero) | service level section 1, "a device whose model the device registry lists with form factor phone" |
| SF2 | "under the line" | largest contentful paint at or under 4,000 ms, on scored views | back-forward restores (no paint timing) counted as under | C still named; every effect diluted by the restore share, both figures move out of their bins | service level section 2, "A view with no paint timing ... is not scored" |
| SF3 | "a month" | August 2026, the latest full month at the as-of date | the average of June to August, or each change's own 28-day post window | C still named; figures move | service level section 4, "at the latest full month's traffic" |
| SF4 | "bring back" | the views the fix's change acts on whose over-line status the change caused, summed over August | the share step applied to every mobile view, whether the change acts on it or not | C still named, A over-counted on subscribers' ad-free views | service level section 4, "the mobile views it brings back", and paywall 4.2 (subscribers never see the ad stack) |
| SF5 | the views each change acts on | the ad stack: ad-supported views of the redesigned templates and the puzzles pages; the front end: every view of the redesigned templates | the front end on ad-supported views only | same call: C on the base alone is about 1,250,000, still first (asserted) | paywall 4.2 and 4.3; the rollout log's ad-free row |
| SF6 | the reading window | 28 days either side of the release that switched the change on, per template group | 21 or 35 days | same call; C's figure moves one bin at 21 days | service level section 3, "the 28 days either side" |
| SF7 | "the release that switched it on" for the separating groups | the puzzles pages' release of 24 June (the ad stack), the ad-free layout's release of 30 June (the front end) | each template group's own release for subscribers | not a separating read: subscribers' views take the front end on 30 June for all six groups | the rollout log's ad-free row and the change register's puzzles line |
| SF8 | subscriber status | the subscription register at view time (start to end inclusive) | status at the pull date | same call: no main-population account changes status inside the main windows (asserted) | the field guide's register line |
| SF9 | "the closest other change" | the change with the second-largest figure on the same footing (the ad stack) | the runner-up on another footing (the banner, the event study's leader) | not the same footing | the prompt, "its figure on the same footing" |
| SF10 | phone class | the registry's `perf_band` | a class built from the model name or the operating system | same call (every main-row model resolves to one band, asserted) | the field guide's registry line |
| SF11 | deploy times | `deployed_at` with its UTC offset | local time read as UTC | not a reading: the offset is in the value; asserted that no view sits within ten minutes of a deploy and that the offset-ignoring order changes the state of no main-window view's interval by more than its bin | the field guide's release-log line, "local time with its offset" |
| SF12 | rounding | unrounded through, rounded once to the ten thousand | per-group figures rounded first | same call, same bins (asserted) | the prompt's closing sentence |
| SF13 | views (counting) | each row counts its `sample_weight` | each row once (sampled rows, not views: front end about 7,400, ad stack about 4,000) | same call, both figures far outside their bins (asserted) | the field guide: "`sample_weight` is the number of page views the row stands for; sum it to count views" |
| SF14 | valuation population | August's scored views the change now reaches (forside's from 1 August) | every August view, scored or not (front end about 1,470,000, ad stack 610,000); only views after each group's switch-on (about 1,440,000 and 570,000) | same call, both figures off their bins (asserted) | service level section 4: "counted over all of that month's scored views on the pages and layouts the change is live on today" |
| SF15 | window boundary | 28 days either side of the deploy instant | calendar days in Copenhagen time (front end about 1,470,000) | same call, the front end's figure off its bin (asserted) | service level section 3: "the 28 days either side of the moment the release that switched it on was deployed" |
| SF16 | subscriber | a view by an account with any active subscription that day, on every title's site | a subscription counted only on its own title's pages, an all-titles product everywhere (front end about 1,470,000) | same call, the front end's figure off its bin (asserted) | paywall terms 4.2: "on all three titles' sites whichever titles their product includes" |

The stump is none of these readings: the default path executes every golden reading and differs only in what it
carries the separating groups' effects on.

### Ladder

| Rung | Gap | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact or construction) |
|---|---|---|---|---|---|
| R0 | time | Event study at the dated releases, valued at August's scored views; the Bølge ramp has no single date and stays unattributed; the ad stack's puzzles step is read on puzzles views | **D, the banner** (427,600; image pipeline 327,200, fonts 270,800, ad stack on puzzles 157,500, front end unplaced) | it is the service level's own 28-day read, every step reproduces | the rollout log: the ad stack and the front end switched on together, template group by template group over six weeks, a ramp larger than any dated step once aligned |
| R1 | population (composition) | Cohort-aligned joint ramp on ad-supported views (4.74 points, about 1,707,000 views a month) split by the two separating groups; raw the split leaves 0.46 point unexplained, standardised to the base's phone mix it closes to within 0.02 point | **A, the ad stack** (1,232,900; front end 804,500) | two clean natural experiments, a composition correction a reviewer expects, a split that sums to the joint ramp | the order of each device's views against the deploys: the front end's cost falls on first views, the ad stack's on later views, and the groups are 23 to 24 per cent first views against 75 on the base |
| R2 | population (partial) | The landing proxy (first view of a 30-minute visit as the first load) within phone class | **A, the ad stack** (1,180,400; front end 860,600) | a session-based first-load reading is the habitual proxy | daily players and subscribers open visits on a bundle cached before the last deploy on most days, so the proxy mislabels the state |
| R3 | population (decisive) | Per-view state from each device's view order against the deploy times; each group's effect within phone class and state, carried to the base's state and phone mix, plus each group's own views at its own read | **C, the front end** (1,460,000; ad stack 609,900) | | none |

Position: C unplaced at R0, 2nd at R1 (1.53x behind A) and R2 (1.37x), 1st at R3 by 2.39x. No leader margin under
1.15x on any rung. Dominance: A carries 1.53x into R3; the state reweighting multiplies C by 1.81 and A by 0.49, an
edge of 3.67x against the 1.84x required (1.2 x 1.53). Worth on the graded quantity: R1 to R3 moves C by +81 per cent
and A by -51 per cent, and the named change.

Correction grid (each asserted at build): raw split, phone-blind (A 1,139,100, C 739,900: A); phone-standardised
(R1: A); standardised also on referrer class (A 1,126,900, C 835,000: A), on connection type or title (as R1: A);
landing proxy (R2: A); the state without phone class (C 1,330,200, 8.9 per cent off: a wrong figure); the decisive
cell (C 1,460,000, A 610,000). Every cell but the decisive one names A or lands C's figure outside its bin.

Why every split ties: within each phone class the two changes' joint cost is the same on a first view and a later
view and both groups carry the same first-view share, so any classification of views (the true state, the landing
proxy, any visible column, none) splits each phone class's joint ramp into two figures that sum to it; only the
phone-blind raw split leaves a residual, and the registry's band closes it, which is what makes R1 feel finished.

### Physical model (the generator's targets)

- One platform bundle per release-train deploy (content-hashed, re-issued at every deploy), shared by every Bølge
  template; the puzzles pages have their own bundle, re-issued at the same deploys. About two departures a week on
  irregular days, about 05:00 Copenhagen time; no view of any device within ten minutes of a deploy.
- State (no column carries it): a view is a first view if its device has no earlier view since the latest deploy,
  otherwise a later view. On a first view the critical path is the front end's download and compile with the
  wrapper's work overlapping the network wait; on a later view the bundle is cheap and the wrapper's main-thread work
  and auction land on the path.
- Per-state effects in points of over-line share at phone multiplier 1: front end 4.0 first, 1.0 later; ad stack 0.4
  first, 3.4 later (joint 4.4 either way). Phone multipliers: low 1.45, mid 0.92, high 0.55. Phone mixes (low, mid,
  high): base 0.42, 0.41, 0.17; subscribers 0.30, 0.40, 0.30; puzzles 0.30, 0.42, 0.28.
- First-view share: base about 0.75, subscribers 0.23, puzzles 0.24.
- Timeline (2026): extract 1 February to 31 August; fonts 3 March; image pipeline 7 April; banner 5 May; ad stack on
  the puzzles pages 24 June; the ad-free layout's front end on all six groups 30 June; ad-supported groups at the
  deploys of 30 June, 7, 14, 21, 28 July and 4 August (sektion, galleri, liveblog, artikel, sport, forside).
- Dated steps uniform across groups, states and phones (fonts 0.46, image pipeline 0.68 on hero templates, banner
  0.72 points, tuned per title). No secular trend between steps; volume seasonality only.
- Sampling: collector v1 one device in 200 to 2 June; v2 from 3 June, signed-out devices one in 600, signed-in and
  puzzles devices one in 50, carried row by row in `sample_weight`.

### Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the ad stack on ad-supported redesigned views and the puzzles pages, the front end on every redesigned view (paywall 4.2, 4.3; service level section 4); C4: the front end on the base alone still names C (asserted) |
| 2 | Unit of account | the page view (service level, field guide grain line) |
| 3 | Attribution window | 28 days either side of the deploy instant of the release concerned (service level section 3, SF15); C3 corridor: 21 to 35 days keep C first (asserted at 21 and 35) |
| 4 | As-of dating | subscription status at view time; C1: no main-population account changes status inside the main windows (asserted) |
| 5 | Version basis | one registry snapshot, one release log, one rollout log; C1 |
| 6 | Denominator | scored views (service level section 2); C4: restores counted as under move both figures out of their bins |
| 7 | Weighting | each view counts by its `sample_weight`, pinned by the field guide ("sum it to count views") under the service level's share of scored mobile views (SF13); a cell effect read with each device weighted once is another estimator of another quantity, noisy in the first-view cells (ad stack about 435,000, front end about 1,477,000, call unchanged, recorded) |
| 8 | Window length | 28 days, filed; C3 as axis 3 |
| 9 | Boundary inclusivity | over the line means strictly over 4,000 ms; after a deploy means after its instant; C1: no `lcp_ms` equals 4,000, no view within ten minutes of a deploy (asserted) |
| 10 | Rounding path | unrounded through, rounded once; headline 1,459,976 sits 4,976 from its bin edge, runner-up 609,889 sits 4,889 from its, every title figure and each change's total 2,190 or more from theirs (asserted) |
| 11 | Tie-break | none needed: every leader margin 1.15x or more |
| 12 | Maturity | August complete: beacons land within 48 hours and the extract is taken on 5 September (asserted none late) |
| 13 | Order of operations | reweight inside phone class and state, then scale by August's weights; C1: linear throughout |
| 14 | Row order | sort-invariant (asserted on two orders); no two views of one device share a second |
| 15 | Duplicate resolution | each page view once; C1: no repeated beacon of either kind inside the main windows (zero-count asserted) |
| 16 | Identity normalisation | device model to registry, exact; C1: every main-row model resolves to one band (asserted) |
| 17 | Netting | none: counts of views |
| 18 | Dimensional units | `lcp_ms` in milliseconds on every row; kilobytes are 1,000 bytes (field guide) on the ask path |
| 19 | Code semantics | navigation type, referrer and connection are context; C1: the state is decorrelated from each inside every group, so standardising on any of them leaves the call (asserted per column) |
| 20 | Integerisation | views a month to the ten thousand (call and dated changes), image figures to one decimal and to the ten kilobytes; mid-bin assertions |
| 21 | Scope of a clause | "latest full month's traffic" is all of August's scored views on the pages and layouts the change is live on today (service level section 4, SF14), forside's from 1 August; C1: `sample_weight` summed by title equals the close-out's August mobile views exactly (asserted) |
| 22 | Forward window contents | Q4 valued at August's traffic by the filed convention; no projection enters |

### Literal reader

Executing the prompt and the service level word for word, a reader values each change's fix on the mobile phone
views it acts on, scored views only, at August's traffic, with each change's effect read over the 28 days either
side of the release that switched it on. The text names no method for separating the two co-shipped changes, and
the design forces one (form 1): the separating groups are the only views where each change acts alone, each group's
effect varies sharply by the state its views are in once that state is built, and the base holds the states in
another proportion, so the effects travel only within state; every coarser conditioning set lands on the ad stack or
on the front end at a figure outside its bin (the correction grid), and every finer one adds nothing (asserted per
visible column). Every row of the semantic fork table is ruled out by a quotable sentence or converges, and the
default path's answer comes from an easy method on the same literal estimand.

### Oracles

- The joint ramp on ad-supported views: ties under the default path and the golden (complete-partition invariance);
  it confirms both splits and selects neither.
- The separating groups' own effects read on their own views: identical under both paths (they are the inputs).
- The Q3 close-out (July and August by title: mobile page views, scored views, over-line views, share): ties with
  the export under every handling of the call and of both asks (no device touches July or August).
- The release train log and the rollout log: operational records, read the same way on every path.
- No control total, published figure or corpus ties only under the golden or only on the wrong read. The closed-fix
  roster of the first draft (a record every method reproduced, with a planted resemblance to the ad stack's puzzles
  read) is cut.

### Organs and pack

- **Filed pins, one statement each.** Service level v3 (scope, the line, the 28-day reading, the valuation); paywall
  terms (the ad-free layout for signed-in subscribers, the ad-supported layout for everyone else); the registry header
  (phone class from the benchmark band); the field guide (grain, sampling, keys, the registers' meaning).
- **Voice.** None. The prep thread carries the review's date, the extract's contents and the image pipeline owner's
  request that the CDN log go in the folder; nobody states a view on a change or a figure.
- **Distractors (named in metadata.json only).** The desktop field summary (correct, desktop, outside the service
  level's mobile scope); the AMP landing-view report (AMP pages are served by the AMP runtime, outside the release
  train); the newsletter send log.
- **Files.** The beacon export (spine), the release train log, the Bølge rollout log, the change register, the device
  registry, the subscription register extract, the edition register, the service level, the paywall terms, the Q3
  close-out, the image CDN delivery log and its vendor appendix, the field guide, the prep thread, the export manifest
  and the three distractors: 18 files in six formats.

### Ask sheet

Two asks and the first slide, each a component of the call's case on rows the call never reads, each with a silent
primary riding something the organisation's own systems did, plus shared hazards. A third ask from the first draft
(the crawl's page weight by change and title) is cut with the crawl: all three of its devices were filed rules a
careful solver executes, and the crawl's only other role was a licensed wrong basis.

**Main call's declared row population** (zero device and hazard rows inside it, asserted on every beacon row from
the banner's release on 5 May, which covers it): beacon rows dated 27 May to 31 August, the release train log, the registry rows of models seen in those rows, the subscription register rows
of accounts seen in them, the rollout log, the change register's A and C lines, the close-out. Device rows live only
in beacons dated before 4 May and in the image CDN log.

| Ask | Figures | Use (H18) | Primary device (silent) | Hazards | Span (files on the golden's path) |
|---|---|---|---|---|---|
| T. What fixing the banner, the image pipeline and the fonts would each bring back on each title (views a month, nearest ten thousand) | 3 changes x 3 titles = 9 | every other candidate's case on the same footing as the call, per title, the figure each editor-in-chief reads for their own title | D1, a second beacon from an older library: from 16 March to 6 April, and again from the container version restored on 4 May to 26 May, the local-edition tag container also loaded an older RUM library on every title's local-edition pages, which sent its own beacon at the page's load event under its own page-view key and with the send time as `ts_utc`; the copies carry the original's device, account, URL and timings, and because a view abandoned before load sends none they are mostly views under the line, so every title's share falls while they run (E's post window, B's pre window, D's post window) | H1 tablets until 4 May (the service level's phone scope); H2 Sønderå Tidende's app-webview beacons forwarded twice under one page-view key, 16 March to 3 May (key uniqueness); T4 the same container sending nothing on Lindå Avis and Kærby Dagblad local pages, 27 April to 3 May; T1 two local editions re-mastheaded on 16 March (effective-dated edition register) | spine (February to early June), release train log, change register, device registry, edition register, field guide, service level, close-out (August views by title), 8 files, 13 columns |
| I. For each month March to August, the image requests and the kilobytes of images the CDN served to mobile page views, per mobile page view (one decimal; nearest ten kilobytes) | 6 months x 2 = 12 | the image pipeline's own delivery record, the picture side of the case against it | D5, a category crossed by label: the group app's native screens (article lists, push images and galleries) fetch images from the same CDN with its native HTTP clients (`CFNetwork`, `okhttp`), which the vendor classes as smartphones like any browser; they make no page view, so counting every smartphone row overstates requests per view by about a quarter and kilobytes by about a sixth in every month, more than every composition of the divisor hazards takes back | the fallback vendor's kilobytes, 9 June to 21 July (vendor appendix); requests split across edge hits and origin fills (vendor appendix); the T primary, tablets and H2 in the March, April and May denominators; scored views against all page views as the divisor | image CDN log, vendor appendix, spine (mobile page views by month), device registry, field guide, close-out (July and August views), 6 files, 11 columns |
| Slide 1 | the call | the review's one statement | carries the call | none | the call's path |

**Stops (design targets; measured values replace them at build).** T: the natural read (every row, view-time
titles); the cracker's read (tablets out, H2 deduplicated) with the older
library's beacons kept, which deflates the banner's and the fonts' figures and inflates the image pipeline's on every
title; the over-cleaned
read (one view per device, URL and day) dropping genuine reloads; the golden. I: the natural read (every smartphone
row, edge hits only, raw bytes, beacon counts); the cracker's read (both request columns, the fallback's kilobytes
converted, each page view once, phones only) with the native clients kept, every month off; native clients removed
but the older library's beacons kept in March and April; the golden.

**Hazard table.** H1 moves T (all 9) and I (March, April, early May denominators); H2 moves T (Sønderå Tidende's 3)
and I (March, April); the fallback units move I (June, July); the request
split moves I (all 12). Every subset of mishandlings is composed at build and asserted outside the bin.

**Separation.** No device moves the call or its runner-up: every T device that moves the banner moves it down (the
older library's copies sit in its post window, the tablets and the forwarder's duplicates in its pre window), the
banner's highest mishandled figure stays under the ad stack's 610,000 by 1.15x or more (asserted), and nothing on the
I path is read by the call. **Off path:** the image CDN log and the vendor appendix are files the call never reads;
the call's beacon rows start on 27 May, after every T device has ended. **Referee:** none needed; nothing ties only
under one handling. **No filed sentence adjudicates a primary:** the field guide says what a page view and `pv_id` are
and never that a page can send two beacons; the vendor appendix defines `ua_family` as the client's agent family and
never says which agents make page views.

**Cracker sheet.** The response that landed the call, ran the hygiene battery (key uniqueness, exact duplicates,
unmatched joins, fan-out, count ties), executed every filed rule (phones only, scored views, the 28-day windows,
the fallback's kilobytes, edge hits plus origin fills) and matched the
close-out:

| Ask row | What the cracker does | Against the golden | Cracker |
|---|---|---|---|
| T, the banner on each title (3) | keeps the older library's beacons (fresh keys, distinct send times, so no key or exact duplicate) | the post window's share understated, every title's figure low and out of its bin | miss |
| T, the image pipeline on each title (3) | as above, the copies only in the pre window | every title's figure high and out of its bin | miss |
| T, the fonts on each title (3) | as above, the copies only in the post window | every title's figure low and out of its bin | miss |
| I, image requests per mobile page view, March to August (6) | counts every smartphone row, the app's native clients included | every month about a quarter high, a fifth after the older library's beacons in the divisor | miss |
| I, kilobytes per mobile page view, March to August (6) | as above | every month off by more than half a ten-kilobyte bin | miss |

**Mirror sheet.** The response on R1 files the same ask values as the cracker (both asks are decoupled from the
call); its sheet differs only in the recommendation criteria.

Mirror leakage: 0 per cent of ask weight on paper (every row above misses for the mirror as for the cracker); the
measured figure replaces it at build.

Pair ceiling: 33.0 (the one-cracker case at a 0.10 ask allowance per top response, r about 3: (38 + 7 + 5.5 + 3 + 7 +
5.5) / 2)

### Realism debts

- Equal joint cost in both states and equal first-view shares in the two groups: forced by complete-partition
  invariance, without which a split leaves a residual that invites the search. Mitigation: neither shows without
  building the state; the physical reading is plausible.
- The state decorrelated from referrer, connection, navigation type, hour and weekday inside each group: deploys on
  irregular days at a low-traffic hour; the base's infrequent readers arrive by every route.
- Puzzles devices are puzzles-only, and subscribers' puzzles views follow an article view in the same deploy
  interval, so per-device and per-bundle state readings converge.
- No secular trend between steps; volume seasonality kept.
- First views and later views share one baseline before any change: physically a first view is a little slower; the
  generator keeps the baselines equal so the state shows only through the changes' costs.

### Leak check

- leak.py --asof 2026-09-07: REVIEW, no LEAK. Each line: "the model's band" in the field guide is a device model's benchmark band (harmless); the service level carries most words of the call because it files the decision's basis (a fix valued on the mobile views it brings back, one fix a quarter) and names no change, order or figure (harmless); the stump terms in the service level, the paywall terms and the field guide are their ordinary vocabulary (device, release, deploy, registry, puzzles) and no sentence names a view's place after a deploy (the reader is asked); `device_model` and `device_class` are the registry's join key and the CDN vendor's own class column (harmless); the subscription register's 181 dates after 7 September are end dates of subscriptions cancelled in September, which run to the end of the following month (harmless, forward-dated by nature).
- Reader, first read: nothing quoted for question 1, no file ranks or answers, the deciding step an analytical choice (question 6); every question-5 sentence fixes a WHAT. Realism tells fixed in the generator: the change register now lists every platform change the release log cites, the release notes carry change numbers, versions and a two-manager rota, the prep thread states no view on a change, the AMP report's constant column and the desktop summary's rounding are gone.
- Reader, second read (the shipped bundle): nothing quoted for question 1, no file ranks or answers, every question-5 sentence fixes a WHAT, the deciding step an analytical choice. Its mild tells are true to the fiction: the waves are the release train's weekly schedule, counts ending in 50 follow from the sampling weights, the thread's request for the CDN log is the image ask's own reason, and the AMP and desktop summaries are distractors.
- Reader, third read (after the section 4 and paywall 4.2 wording): clean on questions 1 to 6; its tells are the rollout log's weekly schedule and single signer, change numbers assigned when raised, and a thin prep thread, all true to the fiction.

## Tried and rejected
- The note's CPU-class standardisation as the decisive rung (draw, 2026-10-10): the registry join is visible from the schema and standardising a natural-experiment group on a joined covariate is reflex for this solver, so it would be executed as routine; kept as rung 2's partial correction.
- Cache state as a cost on the framework alone, the ad stack insensitive (draw): the state correction would then move C without moving A, so the phone-standardised split leaves a residual against the joint ramp, an arithmetic symptom that invites the search; replaced by opposite state dependence with equal surpluses, so every split ties.
- The image pipeline riding the redesign as a third co-shipped change, its go-live a null step (draw): the image service's request log by template family lines up with the rollout log on one key, a schema-visible join, and separating it from the framework needs a hero-against-text contrast that rests on an untestable equal-effect assumption.
- A paint-race replay (the paint waits for the slower of the image and the main thread, so removing one path's delay helps only where that path binds) (draw): once seen it is a per-row predicate, and web-performance knowledge of the LCP sub-parts can supply it.
- Transporting each effect in milliseconds rather than in share points, for groups with different baselines near the 4.0 s line (draw): it is the replay this solver runs at the finest grain, so it would be its starting method.
- The image pipeline's cost varying with edge cache misses as the news cycle concentrates traffic (draw): the bridge from spring to August would carry a residual equal to the pipeline's growth, an arithmetic symptom.
- The consent banner's cost fading as consents accumulate (draw): RC01 v1's self-healing shape, and the fade shows in the weekly series.
- A commercial weather portal as the world (draw): its free users check daily too, so the ad-supported views would not be first-load heavy and the contrast the decisive rung needs would not exist.
- Keeping Product Analytics with pilot_log, monitoring_export, product_manager, shape 07 or 18, executive_team and vote_or_meeting (draw): each is BLOCK against task121 or task122 on the corpus as filed.
- Pattern D first, or pick_one_of_n (draw): test.same_puzzle_older and test.same_driver_older collide with five to seven older builds; E with root_cause_named is the honest reading of the decisive move and needs three differentiation lines.
- Keeping published_series and budget_or_appropriation at registration: blocked against task126 and task127, filed after this draw; redrawn to the Q3 service close-out (close_out_summary) and the review's meeting (vote_or_meeting).
- The source note's crawl ask on first-view and repeat-view runs (stage 2): a lab file with a repeat-view run shows the front end's bytes vanishing on a warm cache and the wrapper's staying, which narrates the decisive state on the lab side; the crawl ships one cold-cache run per URL and the lab ask moved to bytes by change and title.
- A per-cohort pre-switch gap as the grid's third figure, and the two separating groups' own reads as graded components (stage 2): the gap is zero by construction or a level both top responses file, and the group reads are identical at rungs 3 and 4, so each would hand the mirror response recommendation credit; the grid is two figures per cohort and the group reads stay unasked.
- Back-forward restores as a dated-change device on the banner's window (stage 2): the same filed rule governs the main rows, so it is not a separate device, and inflating the banner's step could lift D over A as the call's runner-up, a separation breach.
- A release tag on every beacon (stage 2): the state would be a one-key group-by of device and tag; the deploys ship only in the release train log, joined by time.
- Fixed release-train weekdays (stage 2): the state would surface as a weekday pattern in the daily players' and subscribers' effects; the train leaves on irregular days.
- A uniform 1 in 300 device sample for every audience (stage 3a, on paper): the separating groups' first-load, low-end cells hold about 380 sampled views a window while the base's matching cell is 11 million August views, so one sampled view moves the front end's figure by about 27,000 and no rounding bin at the ten thousand is forced; replaced by a sample_weight column (collector v1 1 in 300 for everyone to 7 May; collector v2 from 8 May, anonymous devices 1 in 600, signed-in devices and the puzzles app 1 in 50) and systematic over-line allocation per stratum.
- First-load share 0.15 in the separating groups with per-state effects 3.5/1.5 and 0.9/2.9 (stage 3a, on paper): at a usable sample the low-end first-load cells stay too thin to pin the figures; retuned to a first-load share of 0.25 with effects 4.0/1.0 (front end) and 0.4/3.4 (ad stack), which keeps the joint cost at 4.4 points in both states and holds rung 3 at A over C by 1.32x.
- Per-cohort subscriber reads of the front end's effect (stage 3a, measured on a scratch build): each cohort's subscriber cells hold a few hundred first-load views, so per-cohort effects swing the sektion figure from 109,000 to 88,000 and move the headline across a ten-thousand bin; the subscribers' ad-free layout now takes the Bølge front end on all six template groups in one release (30 June, with wave 1), so the subscriber read is one date and pooled by construction, and the grid carries the pooled per-phone-class, per-state effects.
- Collector v2 (the sampling change) on 8 May inside the banner's windows (stage 3a, measured): the v1 and v2 audiences differ by sampling noise and the banner's per-title step moved by up to 12 per cent between two correct handlings; the forwarder fix (tablets, double forwarding) and the tag-container fix now land on 4 May, the banner on 5 May, and the sampling change on 3 June, after every dated-change window.
- Wide baseline gaps between phone classes, templates and audiences (stage 3a, measured): window-to-window drift in the audience mix moved per-title dated steps by 3 to 5 per cent; baselines narrowed (phone classes 21.0, 20.4, 19.8 points; templates within one point; ad-free layout minus 1.0; app webview plus 3.0) while the effects keep their phone multipliers, and the old collector samples 1 in 200.
- The closed-fix roster as the calibration organ (10/10 rework, 2026-10-12): every method reproduced its eleven savings and one 2024 puzzles fix was set beside the ad stack's puzzles read, a certified record built to bless the wrong answer; cut, calibration none.
- The service level's sentence that the ad-revenue committee reviews performance work on crawl page weight, with Gunnar Paulsen presenting that basis (10/10 rework): a filed advocate for a wrong basis; cut with the voice.
- Caroline Mortensen's pictures belief and Finn Thygesen's "subscriber pages hardly moved" (10/10 rework): beliefs filed to be refuted, Finn's carrying the wrong answer's intuition; cut, one belief left.
- The per-cohort grid of both fixes as an ask (10/10 rework): a split of the committed figure, banked whole by the cracker and lost whole by the mirror; cut.
- A chart of every change's figure, ordered and titled on the decision quantity (10/10 rework): the order and title fall to whoever lands the call; the deck carries the call on its first slide and its charts are not graded.
- The crawl's page-weight ask (10/10 rework): its devices (the June URL refresh, failed runs filed beside reruns, asset ownership by register prefix) are all filed rules a careful solver executes; cut with the crawl, the run configuration and the asset register.
- The old forwarder's double forwarding as the T ask's primary (10/10 rework): it keeps the page-view key, so key uniqueness finds it; kept as a hazard, the primary moved to the older library's own beacons under their own keys.
- A close-out reporting February to August (10/10 rework): its March and April counts would include the older library's beacons and tie only on the wrong read; the close-out reports July and August, the quarter it closes.
- The older library's beacons in one spell, 16 March to 26 April (stage 3, measured): the copies sat in the banner's pre window, so keeping them lifted the banner to 603,000 on the cracker's read, past the ad stack's 580,000, an ask device moving the call's runner-up; ending the spell earlier left the image pipeline's two windows near balance on Lindå Avis or cancelled the banner's move against the tablets on Kærby Dagblad. Two spells now (16 March to 6 April; 4 to 26 May, from the container version restored with the tag fix), so every T device moves the banner down and the image pipeline up.
- Device weighting closed by convergence for axis 7 (stage 3, measured): read with each device weighted once, the first-view cells are noisy (the ad stack's figure 435,000 against 580,000, the call unchanged); weighting is pinned by the field guide's "sum it to count views" under the service level's share of views instead (SF13).
- The app's native image requests at a tenth of page-view requests and their kilobytes at a few per cent (stage 3, measured): the divisor hazards (tablets, the forwarder's duplicates, the older library's beacons) took them back in March and April, so the cracker's kilobytes fell inside the bin; native requests now run at about a quarter and their kilobytes about a sixth, and the fallback vendor carries 40 per cent of its weeks so its kilobyte hazard (27 to 29 per cent) never cancels the native one.
- Ove Schmidt's belief that the consent banner did it (stage 4, leak reader): read as a planted suspect, and the change's own owner blaming it read oddly; cut, the thread carries no view on a change.
- The tag container's week without beacons on two titles' local pages (stage 4, judge FIX_NOW): with it the share read inside page classes and the pooled share split on four title figures, a fork on the T ask; the gap is gone, the golden reads each title's pooled share as the service level states it, and the page-class reading lands in the same bins (asserted).
- Two local editions re-mastheaded on 16 March (stage 4, judge FIX_NOW): view-time and current mastheads split the fonts on Kærby Dagblad; the move now dates from January, before the export opens, so both readings select the same rows.
- The window boundary and the valuation population left to the plain reading (stage 4, judge FIX_NOW): calendar days moved the front end to 1,470,000, every August view to 1,470,000 and 610,000, views after each switch-on to 1,440,000 and 570,000; the service level now files the deploy instant (section 3) and that month's scored views the change now reaches (section 4), the WHAT only.
- A change register listing only the review's five changes, release notes cycling a dozen phrases under one approver (stage 4, leak reader): the register now carries every platform change the release log cites, with the release managers' rota.
- The valuation population and the subscriber group left to the wording after the pass-1 pins (stage 4, pass 2 notes): "that month's scored views that the change now reaches" still let a per-view reading drop forside's views of 1 to 3 August (ad stack 600,000), and paywall 4.2 named no title, so a subscription counted on its own title's pages moved the front end to 1,470,000; section 4 now says "all of that month's scored views on the pages and layouts the change is live on today" and 4.2 "on all three titles' sites whichever titles their product includes", the WHAT only, the same forks closed further.
- Architecture 1 re-rooted at the author's request (2026-10-14): its decisive method was web performance engineering in a house domain (business operations, client domain General Statistics), so the domain read as a backdrop; redrawn in Energy Systems & Utilities, grid reliability outage analysis.
- A protection change (lateral fuses switched from fuse saving to fuse blowing) as the decisive cause (draw, 2026-10-14): a dated cause whose step an event study finds, and the cause code on every converted outage stays the initiating tree, so the move reads off one device column.
- An underground cable failure analysis by age and vintage (draw): the at-risk population is survivors (population_selection), banned against task459 in the last three builds.
- One network-wide vegetation call (draw): the handover read and the regrowth clock would carry a single answer each, so a careful analyst fixing one rung lands the call; three districts with three drivers make each one-story answer wrong somewhere.
- A utility owner with an executive team or a board deciding (draw): utility_or_infrastructure banned against task459, executive_team against task230 and board_of_directors against task459; the cooperative's manager of operations sets the right-of-way programme inside the approved budget.
- A UK distribution network operator in a fictional country with ash dieback (draw): the regulator's interruption incentive scheme would have to be described accurately to stay realistic; a United States rural cooperative under IEEE 1366 carries the same mechanism with a public standard.
