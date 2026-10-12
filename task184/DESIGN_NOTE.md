# task184 design note (architecture 1)

New build in oviya13ya's Anomaly Detection lane (wave 2), from seed AD07. The seed's world, decision and quantity are
kept: a national screening agency posts its one mobile screening team to one of eight airports its throughput detector
flagged this spring, judged by the passengers the team moves through screening within the 20-minute standard. The
seed's pitfall (the team opens lanes only where a lane position stands idle) is a per-airport cap that re-places the
pick, the dead form of strategies.md F3 (58 v3 and v4), and its pick-one shape 01 is banned for this slot; the pitfall
is re-found from the data.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task184.json` (v1), registered 2026-10-12. `guard.py check`: WARN
  overuse.org_family only (government_agency in 24 builds): a national screening agency is the organisation that owns
  this decision in every country that has one, and the axis is not banned. A first card (shape 07, forum
  executive_team, question form which) was blocked against task180 and task136; the shape is 13, the forum the head of
  screening operations' line management, the question form where.
- **Pairing:** Supply Chain & Logistics (house domain; client domain Urban & Regional Science), aviation passenger
  screening operations, objective Anomaly Detection & Diagnostics. Supply chain by anomaly detection is built once
  before (task54, a different world). The anomaly is each flagged airport's spring queue breach; the diagnosis is which
  breach the mobile team can actually relieve, separating the team's real added capacity from the artifact of its own
  lanes' throughput.
- **World:** a fictional North Atlantic island republic (Kestland), its national screening agency (Kestland Aviation
  Security) and eight airports with one central checkpoint each. The mobile team (24 officers on two shifts) staffs
  three lanes from 05:00 to 21:00 at whichever airport it is posted to. People (guard.py names, en_IE, seed 184):
  Ruairi Barnett, Alana Marnan, Fergus Rynne, Leon O'Boyle; roles fixed at design.
- **Stakeholder, forum, forcing event:** the head of screening operations (role `operations_director`) posts the team
  for 15 June to 31 August 2027, put to their line management (forum `line_manager_or_team`); the forcing event is the
  posting's start (`launch_or_rollout`).
- **Shape 13 (scenarios and the flip point):** each airport's posting is a scenario, graded on the passengers the team
  moves within the standard in each summer period and the peak wait it leaves; the flip is the number of its own lanes
  the chosen airport's managers could release at peak before another posting moves more. Arithmetic fixed at design.
- **Strategy and gate:** `causal_design` (interference: the host's response to the posting), gate G
  `decomposition_attribution` (the team's added capacity net of the host's release), gap objective then time,
  generators G1 then G3, pattern none, layer 2 `estimand_identification`
  (own:host-release-crowd-out-of-a-posted-team), calibration `pilot_log` (last summer's postings).
- **Data-native sentence:** a duty manager handed three extra lanes for a week sends officers to the recurrent training
  the summer otherwise leaves no room for, and the lane sensors count each lane's own passengers, so the mobile team's
  lanes show their full throughput while the host's own lanes go dark, all day at some airports and only in the quiet
  hours at others.
- **Same-puzzle test:** no build in the last twelve shares gap objective, pattern G1 and decision pick_one_of_n; nearest
  drivers 0.06 (task128 v2, task89 v9, task67 v1), none with a host withdrawing its own resource when a shared one
  arrives. task51 (additionality over a baseline a standing rule moves) and task88 (an added booking displacing
  full-rate demand) are the nearest structures and neither has the host's response.
- **Sources (one line each):** strategies.md F9 (interference between units sharing a pool; here the pool is the host's
  own officers, released while the team is there); measured-drivers.md Part 2 (a dimension that lives on another
  entity: the host's lanes, not the team's, carry the effect; and a conjunction, the release and its timing, where the
  day-averaged fix lands on a third airport).

## Tried and rejected

- The seed's idle lane positions as the decisive limit (2026-10-12, at the draw): a per-airport cap that removes the
  natural pick and re-places it, strategies.md F3's dead form (58 v3 and v4).
- Lane capacity observed only while a queue stands, so passengers per lane-hour measures demand at quiet airports
  (2026-10-12, at the draw): task127's driver (a team's capacity visible only as the ceiling it held through a surge).
- Transfer passengers who never reach the landside checkpoint, so departing seats overstate the hub's summer demand
  (2026-10-12, at the draw): the share of a flight's passengers who pass the checkpoint is one ratio per route, and a
  bottom-up build calibrated to last summer's checkpoint counts at airport level already lands close to the call, so
  the decisive step is one enumerable correction.
