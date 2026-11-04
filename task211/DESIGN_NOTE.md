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
5. **Shape:** `other`. Criteria: each site's figure pair, the downtime the jack-up avoids if it stands there and the
   site's own floating-vessel downtime with the jack-up elsewhere (10); the call, its avoided days, the runner-up, its
   avoided days and the gap (5); each site's shelter passages a winter (5); the chart (one bar per site, sorted, the call
   marked, the runner-up labelled, axis in days, a title stating the finding: 6); the two files (2). Total 28 before the
   asks.
6. **Decision and forcing:** `pick_one_of_n` with the quantity in days; the jack-up's mobilisation order under its
   charter must be placed by 9 October 2026 for it to stand at its site on 1 November (forcing event
   `purchase_order_or_contract`); the campaign planning panel signs it (`committee_or_panel`). As-of date of the pack:
   25 September 2026. The call faces forward: the 1 November 2026 to 28 February 2027 campaign has not begun.
7. **World:** Nordvig Marine A/S, a fictional Danish marine contractor installing offshore wind foundations. Five
   fictional North Sea sites: Skarvgrund (west, marshalling port Bramso Havn), Lillevig Banke (east of it, also Bramso
   Havn; alternate shelter Kalvholm), Osterrev (the exposed open-sea site, Tranevig), Molleflak (Tranevig, which has two
   heavy-lift berths) and Fjernhav (the far site, Hjortby Havn). One jack-up and four floating heavy-lift vessels. People
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

### The five go/no-go screens (prototype `t211/proto2.py`, `variants.py`; clean truth, 20 redraws, seeds 3000 to 3019)

| Screen | Measured |
|---|---|
| 1. Levels and lead | Golden names Skarvgrund in 20 of 20 redraws; lead over the runner-up mean 4.67 days, minimum 3.84; lead over every rival reader's pick at least 3.84 days. Prototype levels: mean significant wave height 1.7 to 2.3 m, 90th percentile 3.7 to 5.0 m, downtime 37 to 50 days a winter; storm peaks ran high (maximum 13 to 18 m) and are recalibrated in the generator to the cited climatology. |
| 2. The golden's method holds | Skarvgrund under every specification of the golden's own replay on 4 redraws: critical window 8 and 12 h, shelter trigger 3.0 and 3.5 m, departure three hours earlier, the latest ten winters only, a fixed forward booking calendar at Bramso Havn; minimum lead 3.19 days. (The working limit is a filed vessel parameter, not a specification.) |
| 3. First look | Every shipped statistic (exceedance days of the working limit, mean, 90th percentile, severe storms over 4 m declustered at 24 h, share of hours in 12-hour calm windows) and persistence name Osterrev: 0 of 20 land the golden. |
| 4a. Field-decomposing reader | Per-site replay of the shelter procedure names Fjernhav, past downtime scaled names Fjernhav, persistence names Osterrev: 0 of 20 each. |
| 4b. Constructing reader | Storms times the shelter round trip, per-site downtime with the eastern vessel's observed diversions, placement totals built from independent per-site rates: all name Fjernhav, 0 of 20 each. |
| 4c. Two-file joiner (coordinator's screen) | Per-cell rates on attributes joined from two files, applied per site: Fjernhav, 0 of 20. |
| 5. Literal execution | The criterion executed per site under each natural operationalisation (exceedance, persistence, per-site replay): Fjernhav or Osterrev, 0 of 20. |

These are prototype numbers on the clean truth; `checks.py` re-asserts every screen on the generator's own truth at
the shipped seed (stage 2 and 3).

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
