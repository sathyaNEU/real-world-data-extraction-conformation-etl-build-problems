# task211: Nordvig Marine, where the winter jack-up goes when two sites share one heavy-lift berth

Architecture 1, drawn 2026-11-04 from seed AD34 (which of five offshore sites gets the contractor's one jack-up for the
1 November to 28 February campaign, and the floating-vessel weather downtime it avoids, in days). Kept from the seed: the
world, the decision and the quantity. The seed's own mechanism (storm sequences against the shelter round trip) was
screened as a candidate and set aside as the decisive step (measured below); it stays as a lower rung. The pitfall was
re-found in the data: two of the sites shelter their floating vessels at one marshalling port with a single heavy-lift
berth, and the weather decides which vessel reaches it first.

## Draw

1. **Card:** `.claude/skills/fingerprint/cards/task211.json`, architecture v1, registered 2026-11-04 at PASS (two
   NOTE rows: same-puzzle and same-driver older collisions with task147 and task159, each differentiated on the card).
   Redrawn before filing: `ban.forum` executive_team (task403) moved to committee_or_panel, the campaign planning panel
   that signs vessel allocations, which is who signs this call; the deliverable set moved off pdf+xlsx (task403) to a
   planning-panel deck and a workbook; the decisive keying moved off (objective, G5, binding_constraint), which
   task399 holds inside the last twelve, to G8 decisive, the honest name for a call that turns on which vessel reaches
   the berth first rather than on each site's downtime magnitude.
2. **Pairing:** Supply Chain & Logistics (house domain), subdomain `transportation-network`, client domain General
   Statistics & Data Science, task type `exploratory-data-analysis-distribution-assessment`, which serves Anomaly
   Detection & Diagnostics. The deciding object is the joint distribution of the five sites' stand-downs in time (who
   stands down first in each front, and whose shelter call overlaps whose), not each site's marginal sea-state
   distribution that the planner's monitor summarises.
3. **Objective:** Anomaly Detection & Diagnostics. The anomaly every reader can see: the eastern site's floating vessel
   loses more days per stand-down than its sea states and its port passage explain. The diagnosis: on most of those
   stand-downs the western site's vessel already holds the shared port's one heavy-lift berth, so the eastern vessel
   steams on to the alternate shelter. What it implies for the campaign: the jack-up at the western site removes the
   western vessel's own downtime and those diversions, which no per-site figure credits to it.
4. **Strategy and family:** `binding_constraint` (the single heavy-lift berth binds and moves the pick); Layer 2 family
   `allocation_constraints` (capacity and queueing). Both are unspent on anomaly detection (0 of 35 cards). Gate G
   `binding_constraint`.
5. **Shape:** `other`. Criteria: each site's avoided downtime and its own floating-vessel downtime with every site
   floating (10); the pick, its avoided days, the runner-up and the gap (4); the chart (one bar per site, the pick marked,
   the axis in days: 3); the two files (2); the asks: acknowledged standby per developer and winter (8), the jack-up's
   weather standby per winter (3), shelter-call port dues per port and winter (5). Total 35.
6. **Decision and forcing:** `pick_one_of_n` with the quantity in days; the jack-up's mobilisation order under its
   charter must be placed by 9 October 2026 for it to stand at its site on 1 November (forcing event
   `purchase_order_or_contract`); the campaign planning panel signs it (`committee_or_panel`). As-of date of the pack:
   25 September 2026. The call faces forward: the 1 November 2026 to 28 February 2027 campaign has not begun.
7. **World:** Nordvig Marine A/S, a fictional Danish marine contractor installing offshore wind foundations. Five
   fictional North Sea sites: Skarvgrund (west, marshalling port Bramso Havn), Lillevig Banke (east of it, also Bramso
   Havn; alternate shelter Kalvholm), Osterrev (the exposed open-sea site, Tranevig), Molleflak (Tranevig, which has two
   heavy-lift berths) and Fjernhav (the far site, Hjortby Havn). One chartered jack-up (NM Atlas) and five floating
   heavy-lift vessels, one per site; the vessel at the jack-up's site is released. People
   from `guard.py names --geo Denmark --seed 211`: Andreas Jespersen (marine operations manager, who asks), Simone Schou
   (metocean planner, owner of the monitor), Gert Skov (port agent at Bramso Havn). Currency EUR.
8. **Data-native sentence:** fronts pass the sites from west to east, so Skarvgrund's floating vessel stands down and
   reaches Bramso Havn hours before Lillevig Banke's in almost every front and takes the port's one heavy-lift berth;
   Lillevig Banke's vessel then steams on to Kalvholm, and the progress reports book those extra passages at Lillevig
   Banke although it is Skarvgrund's vessel that causes them.
9. **Abstraction sentence (Part 6):** the benefit of placing one immune unit is the change in the system total, and at a
   resource two exposed units can use only one at a time the unit each shock reaches first imposes the other's delay,
   so the delay belongs to the first unit's placement although the record books it at the second. Not writable against
   any approved build: task302 nets a unit's loss against substitution inside its group (the system loses less than the
   unit's own figure, no shared one-at-a-time resource, no order of arrival); task177 forecasts a unit's failures from
   its team's state when two shortfalls coincide (no placement, no credit across siblings); task119 counts a unit's own
   waits it could have shortened (inside one unit).
10. **The nearest builds and the insight each spends** (from `guard.py mechanisms --objective anomaly-detection`, the
    guard's nearest drivers and the slot hits on spillover and capacity), and whether this build's decisive step is any
    of them in other nouns:
    - task181: a shared upstream resource adds outcome risk to the cases it handles, a confounder of unit outcomes. Not
      this: here no unit's outcome is confounded; one unit's demand delays another's at a resource, and the credit
      moves with the placement.
    - task119: each unit's own failed waits it could have shortened. Not this: inside one unit, no sibling, no order.
    - task54: loss per event borne by every unit in custody, an exposure integral under resequencing. Not this.
    - task210 (spent): exposure per record from a route state in the forward configuration, fitted per cell. Not this:
      the golden is not a per-record attribute; it is the difference between two system replays.
    - task177: team stops once two shortfalls coincide. Not this: coincidence on a team's capacity forecast from the
      team state; no placement credit across siblings.
    - task302: a unit's loss while unavailable netted against substitution inside its group. Not this: substitution
      lowers the system loss; here contention raises it, and the order of arrival decides who bears it.
    - task147: a run of consecutive units refused when one unit is full. Not this: capacity inside one unit's own run.
    - task159: a backlog built while services arrive short of room. Not this: no stock, no backlog.
    - task173 candidate B (rejected there): one pool of placements shared by five hospitals' lists. Closest in kind (a
      shared capacity across units); not this: there every unit draws on the pool at random and the hospital's own
      hazard carried the call; here the weather sets a fixed order at the berth, the first vessel never waits, and the
      whole delay is the second's.
    - task111 (nearest driver, 0.08): failures whose originating delay sits in earlier work. Not this.
    - task114 (0.04): demand that takes a resource only when two parties are present. Not this.
    - task472: a port's berth hours a faster crane finish saves. A port world, not contention.
    Answer: the decisive step is none of them in other nouns.
11. **Sources:** every file is synthetic, generated by `generator/` from seed 211 in an invented world, licence CC BY
    4.0, source and date recorded in `metadata.json`. Levels are set from published references, each cited in
    `metadata.json`: floating heavy-lift monopile installation working limits of significant wave height 1.5 to 2.0 m
    and shelter on forecasts above 3.0 to 3.5 m (DNV-ST-N001 weather-restricted operations, and published vessel
    operating limits); jack-up elevated survival far above any winter sea state in the record; central and southern
    North Sea winter climatology (mean significant wave height 1.6 to 2.4 m, 90th percentile 3.5 to 4.5 m, 18-winter
    maximum about 8 to 10 m); service speeds of 9 to 11 knots and marshalling-port passages of 4 to 12 hours.

### The five go/no-go screens (clean truth; 20 redraws, seeds 5000 to 5019, `t211/screen5.py`; the shipped record stream 2230, asserted in `generator/checks.py`)

| Screen | Measured |
|---|---|
| 1. Levels and lead | Golden names Skarvgrund in 20 of 20 redraws, lead over the runner-up mean 3.37 days, minimum 2.48. Shipped: Skarvgrund 42.00 days, runner-up Lillevig Banke 38.72, gap 3.28. Levels at the shipped record: mean Hs 1.48 to 1.66 m, 90th percentile 2.90 to 3.60 m, 18-winter maximum 7.3 to 9.4 m; pack 11.3 MB. Every graded figure at least 7 per cent of a bin from its edge, tightest Tranevig 2024/25 port dues at 7.5 per cent; the main figures' tightest is Skarvgrund's own downtime at 14 per cent. |
| 2. The golden's method holds | Every specification the filed text leaves open keeps every figure in its bin at the shipped record: the window read in UTC (one hour later), the record cut at 28 February 24:00, model-filled hours interpolated (call held, 41.86), the sites taken in reverse order (identical figures: releases precede arrivals, no same-hour arrivals, minimum arrival gap 1 h). Departure one hour earlier or later moves the figure (40.90 and 42.71, call held) and is closed by section 3.2's sentence. The thin call ratio (1.085) re-asserted at the shipped record under every variant a judge can defend from the files (Skarvgrund figure, lead, whole-day edge, golden's bin): shelter trigger 3.0 m 44.38, lead 3.50 over Lillevig Banke, edge 0.12, outside; 3.5 m 37.67, lead 2.28 over Fjernhav, edge 0.17, outside; critical window 8 h 41.89, lead 3.28, edge 0.39, inside; 12 h 42.31, lead 3.17, edge 0.19, inside; departure one hour later 40.90, lead 3.25, edge 0.40, outside; one hour earlier 42.71, lead 3.28, edge 0.21, outside; window in UTC 42.01, lead 3.29, edge 0.49, inside; fills interpolated 41.86, lead 3.25, edge 0.36, inside. Smallest lead 2.28 (trigger 3.5 m); the trigger, the window and the departure hour are filed (vessel register limits, plan 3.2 and 3.3), so only the inside rows are open readings, and each keeps 42. |
| 3. First look | Every shipped statistic (mean, 90th percentile, exceedance of the working limit, severe storms declustered at 24 h, share of hours in 12-hour calm windows) names Osterrev: 0 of 20 land the golden. |
| 4a. Field-decomposing reader | Per-site replay of the procedure names Fjernhav 20 of 20; past downtime scaled per site names Lillevig Banke 11, Fjernhav 9: 0 of 20. |
| 4b. Constructing reader | The joint replay with each vessel credited its own downtime (Lillevig Banke's Kalvholm passages counted as its own) names Fjernhav 17, Lillevig Banke 3: 0 of 20. |
| 4c. Two-file joiner (coordinator) | Attributes joined from the progress reports and the registers (site, month, shelter port, berth count, sea-state band), per-cell rates with main effects and interaction: site by month names Lillevig Banke 11, Fjernhav 8, Skarvgrund 1; shelter port by sea-state band names Fjernhav 18, Lillevig Banke 1, Skarvgrund 1: 19 of 20 wrong each. |
| 4d. Per-placement joint replay with every stated fact (coordinator) | The whole campaign simulated once per placement, every vessel's procedure run jointly, the one heavy-lift berth at Bramso Havn honoured, a taken berth read as wait at the anchorage, berth anyway, or go to the nearest free heavy-lift berth (Sandvig): Fjernhav 20 of 20 under each, golden lead over its pick at least 2.72. |
| 5. Literal execution | Section 4.3 executed with the stated facts only gives the screen 4d rows: Fjernhav 38.11 days at the shipped record under every taken-berth reading the files allow. |

## Default path

1. Read `campaign_plan_2026_27.pdf`: the weather procedure (section 3) and the placement basis (section 4.3).
2. Stack the two buoy exports: old buoy names to station ids through `buoy_stations.csv`, centimetres to metres and
   tenths of a second to seconds, the 2016/17 winter kept once, each winter cut to 1 November 00:00 to 28 February 24:00
   Danish time (UTC+1).
3. Replay each site's floating vessel over each winter hour by hour with its limits from the vessel register and its
   passage hours from the port register: the hour it leaves, the hours alongside, the hour it sails back, the 10-hour
   lift; count its downtime as section 4.2 defines it. This is the field's planning method for weather-restricted
   operations (rung 1).
4. Credit each placement with the downtime of the vessel it releases, every other vessel's downtime being unchanged,
   and average over the 18 winters.
5. Name the site with the most.

Ends on: Fjernhav, 38 days avoided (38.11)

Golden: Skarvgrund, 42 days avoided (42.00)

## Stump sentence

A competent analyst replays each floating vessel's weather procedure over the buoy record, credits the jack-up with the
downtime of the vessel it releases and names Fjernhav at 38 days; the step that lands them there is treating the five
vessels as independent, when Skarvgrund's and Lillevig Banke's vessels shelter at the same port, whose one heavy-lift
berth goes to whichever arrives first, and the past progress reports show the later one going on to the Kalvholm storm
moorings, so the jack-up at Skarvgrund also removes Lillevig Banke's diversions and avoids 42 days.

## Three rules

- Task type: general-statistics-data-science / exploratory-data-analysis-distribution-assessment, which serves Anomaly
  Detection & Diagnostics; the build reads the joint distribution of five vessels' stand-downs in time, not each
  site's marginal sea-state distribution.
- Domain test: the deciding quantity is expected weather downtime of a weather-restricted marine operation, worked the
  way the offshore field plans it: operating limits, passage times and a critical lift duration applied hour by hour
  to an hourly significant-wave-height hindcast, averaged over the winters of record.
- Swap: "place the one immune ward where it avoids the most ambulance diversion hours" parses, but the hourly wave
  hindcast, the station-keeping limit, the passage plan and the 10-hour critical lift have no counterpart, so the figure
  stops being computable: the call is a marine weather-downtime estimate.
- Layer 1: the buoy record in two export layouts (centimetres and tenths of a second under old buoy names with compact
  UTC stamps; metres and seconds under station ids with ISO stamps), the 2016/17 winter in both exports, servicing gaps
  filled from the regional model and flagged, a UTC record against a Danish-time campaign, progress reports split at
  local midnight, statements in quarter days, a payables extract across an ERP change; each produced by the system
  named, nothing placed to be caught.
- Layer 2: allocation constraints, a single-capacity shelter berth shared by two exposed units in a fixed arrival
  order: the benefit of making one unit immune is the change in the system total, not that unit's own figure.
- Decisive step: seeing from the past progress reports that the two Bramso Havn vessels take turns at one berth in the
  order the fronts reach them, the later one going on to Kalvholm, and so pricing each placement as the fleet with and
  without it, which credits the jack-up at Skarvgrund with the eastern vessel's diversions it removes.
- Not semantics: every field read correctly (one heavy-lift berth at Bramso Havn, both vessels' shelter port, passage
  hours, limits) still leaves what a vessel does at a taken berth unstated, and every reading the files allow (wait at
  the anchorage, berth anyway, the nearest free heavy-lift berth at Sandvig) files Fjernhav 38.11; only a relation
  between two vessels' rows at the same hours settles it.
- Not rule application: no filed rule performs the step: the procedure names the shelter port and never a taken berth,
  and section 4.3 names the fleet without naming any interaction. Enumerated family (per-site replay; joint replay
  with anchorage, berth anyway or nearest free berth; joint replay crediting each vessel its own; joint replay with the
  recorded practice) spans Skarvgrund's figure from 35.00 to 42.00 days and names Fjernhav, Fjernhav, Fjernhav, Fjernhav
  and Skarvgrund. Standing family once the records are read: the recorded practice alone (23 Lillevig Banke and 3
  Skarvgrund diversions, every one with the other vessel alongside, none otherwise), spread zero; the ruling-out is
  quiet, a cross-vessel time relation in a file the procedure never sends the analyst to compare across vessels.
- Analyst test: a strong analyst who cleans the record, executes the procedure exactly and credits each placement with
  the released vessel's downtime files Fjernhav at 38 days, 4 days short of Skarvgrund's 42.
- Estimand: `campaign_plan_2026_27.pdf` section 4.3: "The downtime a placement avoids is the floating fleet's weather
  downtime over the campaign with every site worked by its floating vessel, less the fleet's weather downtime with NM
  Atlas at that site, as the procedure in section 3 gives it against each of the 18 winters of the buoy record (1
  November 2008 to 28 February 2026), averaged over those winters and stated in days of 24 hours", with section 4.2
  defining a vessel's weather downtime in hours.
- No decoy: nothing is planted: no memo, briefing or stakeholder figure argues for a site; the metocean monitor reports
  past sea-state statistics, says on its Version sheet it is not a downtime estimate and is declared in metadata.json as a
  wrong-basis distractor; Sandvig is a working port in the register with its own use as the crew-change port.
- No certified replay: no published, certified or validated figure of avoided downtime exists anywhere in the pack; the
  past progress reports are operating records of what the vessels did, never a validation of a method.
- Lesson: in a fleet that shares a capacity, the value of making one unit immune is the change in the system total, and
  the unit that reaches the capacity first imposes the other's delay, so the credit follows the first arriver while the
  record books the delay at the second; no build on file credits a placement with another unit's contention cost (the
  per-build lines in Draw item 10).

## Survivor anatomy

- Actor: the deciding property (Lillevig Banke's vessel goes on to Kalvholm because Skarvgrund's holds the berth) has no
  column: no diversion reason, no berth holder, no conflict flag anywhere; it is a relation between two vessels' rows
  in the progress reports at the same hours.
- Link: it is read through a cross-vessel time join no key offers, Lillevig Banke's Kalvholm passages against
  Skarvgrund's "Alongside Bramso Havn" blocks in the same hours; no file links the two sites and the procedure never
  asks for a comparison across vessels.
- Reflex: the field's method (each vessel's weather procedure replayed hour by hour against the hindcast) sits at rung
  1 and files Fjernhav 38.11.
- Back-test: the textbook route validates once calibrated: per-site replay plus each vessel's recorded alternate-shelter
  use reproduces every vessel's past downtime, Lillevig Banke's included, while still booking those passages to Lillevig
  Banke and naming Fjernhav.
- Second use: the progress reports re-date the developers' catch-up statement lines (ask 1); the buoy record carries the
  jack-up's code evidence (ask 2); the registers' tonnage and dues carry ask 3; deleting the decisive step drops no file.
- Shock: the movement reads as ordinary: Lillevig Banke's vessel loses more days than its sea states explain, but its
  recorded downtime is not the largest, and on every shipped statistic the sites sort Osterrev first; Skarvgrund leads
  no sort of any single column.
- Pins: the WHAT (fleet downtime with and without each placement, 18 winters, Danish-time window, days of 24 hours,
  section 4.2's hours) is filed in the campaign plan; no filed sentence names the berth count's consequence, the
  arrival order, Kalvholm or what a vessel does at a taken berth.

## Readability screen

| Rung | What the solver reads | Verdict |
|---|---|---|
| 0 Sea-state statistics | exposure columns (the monitor or their own): Osterrev first on every one | readable |
| 1 Per-site replay | the field's method on each vessel: Fjernhav 38.11 | readable |
| 2 Joint replay with every stated fact | the one berth honoured, a taken berth read as anchorage, berth anyway or nearest free berth: Fjernhav 38.11 | readable |
| 2b Joint replay crediting each vessel its own | Lillevig Banke's recorded Kalvholm passages booked to Lillevig Banke: Fjernhav 38.11 | readable |
| 3 (decisive) The recorded practice priced as a system counterfactual | a cross-vessel relation in the progress reports, no column, no sentence | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "site" | the five sites of plan section 1 | none in the files | same call | plan section 1 table |
| SF2 | "weather downtime" | section 4.2's hours (leave to back on site, and at-site hours above the working limit) | waiting on weather at site only | same call | plan section 4.2 |
| SF3 | "downtime it avoids" | fleet total with every site floating less fleet total with NM Atlas at the site | the released vessel's own downtime | Fjernhav | plan section 4.3, "the floating fleet's weather downtime ... less the fleet's" |
| SF4 | campaign clock | Danish time, record hour 0 at 31 October 23:00 UTC | the window read in UTC | same call, every figure in bin | plan section 1, "Danish time"; asserted |
| SF5 | the 2016/17 winter | counted once | counted from both exports | same call | plan section 4.3, "each of the 18 winters"; rows identical |
| SF6 | "days" | hours over 24 | working days, calendar days touched | same call | plan section 4.3, "days of 24 hours" |
| SF7 | departure hour | alongside by the start of the first hour above the limit | one hour earlier or later | same call, figure moves | plan section 3.2's sentence |
| SF8 | return | lift hours from the arrival hour, passage hours at or below the station-keeping limit | the lift after a settling hour | same call | plan section 3.3 |
| SF9 | the released vessel | takes no part in the campaign | kept as a spare | same call | plan section 2 |
| SF10 | a taken berth | the recorded practice: on to Kalvholm when the other vessel is alongside on arrival | diversion whenever the other was alongside at any hour of the passage | same call | the progress reports: 26 of 26 taken-berth arrivals went on to Kalvholm, every free-berth arrival berthed, the practice reproduces all 291 shelter rows; the passage reading is contradicted by 10 recorded berthings; asserted narrow and broad |
| SF16 | a taken berth, read as berth anyway | as SF10 | the vessel lies at Bramso Havn regardless | Fjernhav | 46 recorded shelter rows at Kalvholm, first `2023-11-12, NM Terne, Lillevig Banke, 15:00-24:00, On storm moorings, Kalvholm buoy K3`, after `2023-11-11, NM Terne, 14:00-24:00, Transit to Kalvholm`, while `2023-11-11, NM Havorn, Skarvgrund, 11:00-24:00, Alongside Bramso Havn, heavy-lift quay` runs to 02:00 on the 12th; asserted |
| SF17 | a taken berth, read as wait at the anchorage | as SF10 | the vessel waits off Bramso Havn until the berth frees | Fjernhav | the same 46 rows (the vessel is at Kalvholm, never off Bramso); no row records a vessel waiting off a port; asserted |
| SF18 | a taken berth, read as the nearest free heavy-lift berth | as SF10 | the vessel goes on to Sandvig, 2 hours from Bramso Havn | Fjernhav | the same 46 rows; no progress report row places any vessel at Sandvig; asserted |
| SF11 | arrival order and tie | the order the storms set; releases precede arrivals | another site order | identical figures | no same-hour arrival in any configuration; asserted |
| SF12 | record end | the look-ahead reads the record past 28 February 24:00 | record cut at the window end | same call, every figure in bin | asserted |
| SF13 | model-filled hours | used as shipped | dropped and interpolated | same call | asserted (41.86) |
| SF14 | limit equality | above 3.2 m leaves; at or below 1.8 m works | at or above, below | same call | plan sections 3.1 to 3.3 wording |
| SF15 | the average | mean of the 18 winter figures | pooled hours over 18 winters | identical | arithmetic; asserted |

## Ladder

| Rung | Construction | Pick | Skarvgrund | Fjernhav | Lillevig Banke |
|---|---|---|---|---|---|
| 0 | sea-state statistics | Osterrev | 3rd or 4th | 2nd | 5th |
| 1 | per-site replay (the field's method) | Fjernhav | 35.00 | 38.11 | 31.72 |
| 2 | joint replay, stated facts (anchorage, berth anyway, nearest free berth) | Fjernhav | 35.00 to 35.34 | 38.11 | 31.72 to 32.06 |
| 2b | joint replay, each vessel credited its own | Fjernhav | 35.64 | 38.11 | 38.08 |
| 3 | joint replay with the recorded practice, fleet difference (golden) | Skarvgrund | 42.00 | 38.11 | 38.72 |

Skarvgrund is never first before rung 3 and second on none; the final margin is 3.28 days on a 42.00 figure (1.085
times), under the 1.2 times guide, held instead by the whole-day grading (3.3 bins) and a minimum lead of 2.48 days in
20 redraws.

## Closure table

| # | Axis | Reading here | Move |
|---|---|---|---|
| 1 | Population | the five sites, the floating fleet of plan section 2 | C1, filed section 1 and 2 |
| 2 | Unit of account | the fleet's downtime in hours, reported in days | filed 4.2, 4.3 |
| 3 | Attribution window | 1 November 00:00 to 28 February 24:00 Danish time | filed section 1 |
| 4 | As-of dating | the 18 winters 2008/09 to 2025/26 of the record | filed 4.3 |
| 5 | Version basis | the two exports agree on 2016/17; one record | C1, asserted SF5 |
| 6 | Denominator | the 18 winters | filed 4.3 |
| 7 | Weighting | equal per winter | filed 4.3 ("averaged over those winters") |
| 8 | Window length | 2,880 hours every winter, 29 February outside | filed ("28 February 24:00") |
| 9 | Boundary inclusivity | hours from 00:00 1 November to the last hour before 1 March | C3, asserted SF4 and SF12 |
| 10 | Rounding path | unrounded hours to days, rounded once at the end | prompt's last sentence |
| 11 | Tie-break | none arises: no same-hour arrivals; releases precede arrivals | C1, asserted SF11 |
| 12 | Maturity and censoring | a vessel still in shelter at the window end counts to the end | filed 4.2 ("every hour of the campaign") |
| 13 | Order of operations | departure decisions, then arrivals, hour by hour | C1, site order inert (asserted) |
| 14 | Row order | export order irrelevant; keyed by station and time | C1 |
| 15 | Duplicate resolution | the 2016/17 overlap identical; dropped once | C1 |
| 16 | Identity normalisation | old buoy names to station ids through the lookup | lookup shipped |
| 17 | Netting against gross | the released vessel takes no part | filed section 2 |
| 18 | Dimensional units | cm to m, tenths of a second to s; days of 24 hours | column names and 4.3 |
| 19 | Code and status semantics | model-filled hours are record values | C3, asserted SF13 |
| 20 | Integerisation | whole hours of the record | the record is hourly |
| 21 | Clause scope | section 3 applies to every floating vessel, section 4 to the placement | plan wording |
| 22 | Forward window contents | the 2026/27 campaign replayed against each past winter, the record standing in for the forecast | filed 4.3 |

## Literal reader

Read word for word, the prompt and plan section 4.3 fix the population, outcome, window, unit and comparison; section
3 fixes every hour convention, and section 4.2 the hours counted. The one thing the text leaves to the records is what
a vessel does when its shelter port's heavy-lift berth is taken: the progress reports answer it (26 taken-berth arrivals,
every one on to Kalvholm; every free-berth arrival berthed), and each alternative reading is contradicted by those rows
(SF10). Every other literal reading gives the golden's call and keeps every graded figure in its bin (SF4, SF12, SF13
asserted); the readings that move a figure (SF7) are excluded by a quotable sentence. The easy answer, Fjernhav, comes
from an easy method on the same literal estimand (independent vessels), never from another reading.

## Oracles

- The Tranevig weekly statements' invoice totals equal the sum of their lines, the repeated charges included: they tie on
  the wrong read of ask 3 and arbitrate nothing.
- The jack-up owner's final hire statement covers 15 January to 15 February 2026 only, after the code change: it can fill
  the go-live gap (ask 2) and says nothing about the old codes.
- No control in the pack ties only under the golden of the main call: no certified downtime, no developer figure for the
  coming campaign, no published placement study.
- The monitor answers another question correctly (past sea states) and is declared a wrong-basis distractor.

## Ask sheet

Three asks, all on quantities the main-call files cannot compute (money, acknowledgements, the jack-up's own reports),
each a component of the placement's case. Families: D8, D7, D2, D4, D6, D1, none repeated; no two devices share an
evidence file (the progress reports, the statements' reference strings, the buoy record, the hire statement, the
registers' tariff and tonnage, the payables extract's own berth times).

- Ask 1, developer-acknowledged standby days per developer per winter (8 figures, days to two decimals; organ
  `developer_standby_statements.csv`). P1 D8: a developer's disputed February days are acknowledged on its next November
  statement under that month; the vessel on the line was working elsewhere that November (progress reports), so the
  days belong to the earlier winter; read by period and summed, every cell misses by 2 to 12 days. P2 D7: a revised statement
  restates one line of an earlier one under a new number, the earlier number in the developer's reference string; the
  per-chain latest-version rule drops the unrevised lines, summing double-counts the restated one; every cell moves.
- Ask 2, NM Atlas's weather standby hours per winter (3 figures, whole hours; organ `atlas_shift_reports.json`). P1 D2:
  before the reporting system's go-live on 15 January 2026, WS meant weather standby (wind) beside WW (waves) and SB was
  the supply wait; the current code list reads WS as waiting on supply; the old WS hours rise and fall with the buoy's
  sea state, the new ones do not; every winter moves by 28 to 40 hours. P2 D4: no shift reports from 15 to 25 January
  2026; the owner's final hire statement carries the reduced-rate hours for the period; 2025/26 moves.
- Ask 3, shelter-call port dues at Tranevig and Hjortby Havn per winter (5 figures, euros to the nearest 10; organ
  `ap_port_charges_2023_2026.csv`). P1 D6: Tranevig's weekly statements repeat a call's charge on every weekly line it
  touches, and equal charges of separate calls sit in consecutive weeks, so only the berth times split them (the
  tariff and tonnage confirm); summing over-counts by 3,227 to 8,067 euros a winter, the equal-charge merge
  under-counts. P2 D1: Hjortby's invoices open at the ERP change were re-keyed (number unpadded, whole euros) and its
  numbers restart each year; no de-duplication or exact de-duplication over-counts 2024/25, the invoice number as the key
  drops recycled 2026 invoices.

| Ask | Figures | Cracker route (battery, every filed rule, every control) | Cracker keeps | Mirror keeps | Cracker |
|---|---|---|---|---|---|
| 1 statements | 8 | latest version per chain, lines by period | 0 | 0 | miss |
| 2 jack-up standby | 3 | current code list, retired WW as weather, gap filled from the hire statement | 0 | 0 | miss |
| 3 port dues | 5 | equal consecutive charges merged, invoice number and date as the key | 2 | 1 | miss |

Pair ceiling: 33.7 (cracker on the call 51.9, keeping 2 of 16 ask figures, 12.5 per cent; best response off the call
15.4); with both responses on the call the pair is 51.9.

Mirror leakage: 6.2 per cent of ask weight (1 of 16 figures, Hjortby 2025/26, which no device moves on the natural read).

Measured by: generator/ceiling.py on the cut pack (shares no code with the generator).

## Leak sweep rulings

`leak.py` on the final cut (target.zip 3f239f1e): REVIEW, no LEAK. Each REVIEW line ruled in the main thread:
- Sweep 3, the plan carries the committed call's distinctive words: harmless; the plan names the jack-up, the five
  sites and the campaign dates as its scope and never ranks or picks a site.
- Sweep 4, stump-paragraph terms in the plan (record, Fjernhav, Lillevig, Skarvgrund, heavy-lift, Bramso): harmless;
  site names in the scope table, "heavy-lift" in "floating heavy-lift vessels", Bramso Havn as a load-out port in the
  timetable; no sentence relates the two sites, a berth, an arrival order or Kalvholm (asserted in checks.py). Not
  handed to the reader.
- Sweep 6, the developer statements name sites beside numbers: harmless; past standby days by vessel and month for
  ask 1; read as past downtime they name Lillevig Banke or Fjernhav, never the golden.
- Sweep 9, crew-rotation dates after the as-of date: harmless; the crew-change plan for the coming campaign, a
  declared distractor, on the forward allow-list.
- Sweep 12, the plan names data columns verbatim: harmless; the governing document's own scope table (sites,
  developers, vessels), not a note on the data.
- Sweep 1 earlier flagged the monitor's "About" sheet; renamed "Version" and cut to content, owner, refresh and
  version (the in-file line a context artifact carries), the storm-count definition removed.

## Tried and rejected

- 2026-11-04, the seed's own mechanism as the decisive step (storm sequences against the floating vessels' shelter round
  trip): measured on 20 redraws, its golden (each vessel's shelter procedure replayed per site over the buoy record)
  names Fjernhav in 20 of 20 and storms times the round trip names Fjernhav in 20 of 20, so the constructing reader
  lands it; and a replay of filed limits and a filed shelter procedure over the full-resolution record is the rule
  application task464's note records for an offshore service vessel. Kept as rung 1.
- 2026-11-04, swell sensitivity of the floating vessels (downtime driven by wave period the Hs limit ignores): task145
  records it dead (an estimator choice the motion log settles by reflex), and the joiner attaches the period to every
  stand-down.
- 2026-11-04, forecast-gated starts and aborted lifts: task170's G1 measured the family spreading 0.13 to 0.21 on which
  hindcast state stands in for a forecast; shipping a forecast archive makes the golden a filed go rule replayed.
- 2026-11-04, port approach closures, tidal sills and pilot boarding limits keeping sheltered vessels in port: filed,
  they are a port rule replayed (rule application); unfiled, a withheld rule; either way the delays align one to one
  with the port's closure log in the first look.
- 2026-11-04, storm gaps in the buoy record (buoys failing in the heaviest seas): the remedy is gap filling from a
  neighbouring buoy, the field's own MCP form (task170's seventh-cell law), and a data defect would decide the call.
- 2026-11-04, the jack-up's own supply chain (weather-limited feeder barges capping its output) and its jacking moves:
  filed limits replayed, rule application.
- 2026-11-04, a capped buffer's benefit (the partial expectation of concurrent demand below a filed capacity, in a
  hospital cohort area): the cap is filed, so the literal execution computes the concurrency and lands it.
- 2026-11-04, exposure that reacts to the outcome (worked against planned staffing on wards): the choice between the
  two exposures is a definition, so the sentence closing the fork names the decisive step (the WHAT screen).
- 2026-11-04, the berth conflict filed as a stated rule (a vessel finding its berth taken goes to the storm moorings):
  the per-placement joint replay with every stated fact then lands the golden; moved to a practice only the past
  progress reports reveal, the berth count filed as a plain register fact.
- 2026-11-04, port bookings at Bramso Havn as a second contender for the berth: a stated booking calendar is a fact the
  joint replayer executes, and it blurs who displaces whom; removed, no other contender.
- 2026-11-04, the site order breaking same-hour arrivals (record stream 211): one tie at Bramso Havn moved the golden by
  0.91 days; the record stream was redrawn to one with no same-hour arrival in any configuration (2230), and berths
  left in an hour are freed before that hour's arrivals.
- 2026-11-04, a Tranevig dues device resting on the tariff alone (weekly lines without berth times): 6 equal-charge
  pairs and 8 runs of three split two ways, so the golden was not recoverable; berth start times added to the lines.
