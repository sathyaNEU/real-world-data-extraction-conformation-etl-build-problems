# task472: Thornbay Port Authority, where the 2027 replacement quay cranes go

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task472.json` (architecture v1), registered 2026-10-20 after a pull, so
  task468 (architecture 4), task473 and task474, filed earlier the same day, were in the check. Guard PASS; the two
  structural NOTEs (gap objective, decisive generator G1, decision pick_one_of_n) are differentiated on the card
  against task198 v4 (an entitlement a lesser-of payment rule hides), task184 v1 (a shortfall split against a filed
  plan) and task253's lineage v2 (a congestible network re-solved after losing a link). Nearest driver task269 at 0.07.
- **Seed:** ET29 (a port authority funds new ship-to-shore cranes at one of six container terminals on the berth dwell
  of large cargo vessels; an AIS pipeline that cut calls at midnight UTC and ended a call at every hour-long gap
  reported dwells a third of the terminals' own). Kept: the world (one authority, six container terminals, AIS and the
  terminals' own records), the decision (where new cranes go) and the quantity (berth time of large vessels). The
  seed's mechanism (calls cut at midnight UTC, two ships sharing one MMSI) is carried as Layer 1 only.
- **Pairing:** Supply Chain & Logistics (house domain, ports and terminals; card subdomain `transportation-network`)
  sitting in General Statistics & Data Science, task type `data-integration-record-linkage-entity-resolution`, the
  only ETL task type the house domain maps to. The ETL work is real linkage: AIS berth segments keyed by MMSI, two
  terminal operating systems (TOS) keyed by visit and crane name, two maintenance systems (CMMS) keyed by asset number
  and local time, and a vessel register keyed by IMO, joined into one conformed large-vessel call table. Objective:
  Data Extraction & Conformation (ETL).
- **Shape:** `other`, written out: one pick among six terminals, each terminal's built figure graded (six), the
  pick, the runner-up and the gap (three), two ask grids over the six terminals (calls with their average hours
  alongside, twelve; breakdown hours, six), the conformed call file and the workbook (two), and the chart's parts
  (three to four). About 32 criteria before any rubric split.
- **Strategy:** `decomposition_attribution` (the vessel's stay is split into the part crane breakdowns caused and the
  rest, and the parallel structure of its crane sections decides the split); Gate G `decomposition_attribution`;
  gap `objective` (the decision is scored on vessel time, not crane time), then `population` (which stops fall on
  large-vessel work); generators G1, G3, G10; Layer 2 family `estimand_identification` (the right counterfactual),
  pattern `own:slowest-section counterfactual`.
- **World:** United States, the fictional East Coast port of Thornbay. The Thornbay Port Authority is a state port
  authority that owns its ship-to-shore cranes and operates its six container terminals: Ordway, Pinecastle, Gannet
  Point and Halyard in Thornbay Harbor, and Saltcote and Merriwether on the river, the last two bought from a private
  operator in 2024 and still run on that operator's terminal operating system and maintenance system. The Authority's
  Crane Replacement Program buys six new cranes in its 2027 order and places them at one terminal, chosen on the
  berth time breakdowns of each terminal's cranes cost large vessels (10,000 TEU and over) in the fiscal year ended
  30 June 2026. Personas from `guard.py names --geo "United States" --seed 472`: Nicole Bautista (Director, Terminal
  Equipment, who brings the recommendation to the board), Dennis Johns (Maintenance Planning Manager, who keeps the
  work orders) and Tanya Abbott (Vessel Operations Analyst, who keeps the berth records); Sarah Norman was replaced
  (her first name in task108).
- **Forcing fact:** the board of commissioners awards the 2027 crane contract at its 27 October 2026 meeting, and the
  supplier's order needs the receiving terminal named. As-of: 2026-10-06. The decision faces forward (where six cranes
  delivered in 2027 and 2028 go); the evidence is the closed fiscal year, which is what the program's rules score.
- **Context artifact / calibration:** `operations_log` (the TOS crane activity, the spine, with the CMMS work orders);
  calibration form `none`. Forum `board_of_directors`, forcing event `purchase_order_or_contract`, organisation
  `utility_or_infrastructure`, role `operations_director`; none repeats task468, task473 or task474.
- **Data-native sentence:** a large ship at Thornbay is worked by five or six quay cranes on one rail, each keeping its
  own run of bays from first box to last, so the ship sails when its slowest run is finished; a crane that stops for a
  breakdown delays the ship only by how far the stop pushes that crane's finish past the ship's other cranes, which is
  nearly the whole stop on a ship split evenly and often none of it where the stopped crane had a short run, and the
  terminals differ in exactly that: Ordway puts its two new cranes on the long runs of every large ship and its five
  old, breakdown-prone cranes on the short ones.
- **The WHAT screen.** Population: calls by vessels of 10,000 TEU and over at each terminal whose cargo work began in
  the fiscal year (filed in the program rules). Outcome: berth time lost to crane breakdowns, how much longer the vessel
  stayed alongside than it would have if the breakdown had not happened (filed). Window: 1 July 2025 to 30 June 2026.
  Unit: berth hours. Comparison: the six terminals' totals, the most chosen. The decisive step settles none of them: it
  is how the counterfactual stay is computed, and the data's own structure (each crane's moves confined to its run of
  bays, a stopped crane resuming its own run) forces the slowest-section construction over summed downtime or a pooled
  share.
- **Deliverables:** `thornbay_2027_crane_replacement.xlsx` (the call, each terminal's berth hours lost, the asks, a
  chart) and `thornbay_2026_large_vessel_calls.csv` (the conformed fiscal-year large-vessel call table).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data-integration-record-linkage-entity-resolution: the ETL
    task type the conformance sits in (pattern 1, linkage error propagates to estimates, is the family the AIS and TOS
    joins carry as Layer 1); no card holds a counterfactual over parallel work streams, so the pattern is the build's
    own.
  - `stumping/references/strategies.md` F8 (attribution: book a correct movement to the right driver; overlap or
    interaction decides the split): here the interaction is a maximum over parallel crane runs.
  - `guard.py mechanisms --objective etl` (50 builds) and `slots`: no driver turns on the finish of the slowest of
    several parallel streams; the nearest structures are task253's lineage v2 (a re-solved congestible network, dead
    at stage 2) and task198 v4 (a lesser-of rule), both differentiated on the card.
  - `dataset-generation/references/layer1-messiness.md`, general techniques 2, 3, 5 and 6: several sources for one
    picture, imperfect keys, local time against UTC, genuine overlap.
- **The draw in ten lines:**
  1. Pairing: Supply Chain & Logistics (ports) in General Statistics & Data Science, record linkage, ETL.
  2. Niche: crane replacement placed on the berth time crane breakdowns cost large vessels, from AIS, two TOS and two CMMS.
  3. Default path: charge every breakdown hour on a crane working a large vessel to that vessel's stay; ends on Ordway.
  4. Golden: Pinecastle, where the even splits make nearly every stop cost the ship its whole length.
  5. Stump sentence: below; the default path never asks whether the stopped crane's run was the one the ship waited on.
  6. Shape: other, one pick of six with each terminal's figure, runner-up, gap and two six-terminal ask grids.
  7. Deliverables: a workbook and the conformed call CSV.
  8. Nearest driver: task269 at 0.07; structural NOTEs differentiated against task198, task184, task253.
  9. Guard: PASS on the registered card.
  10. Lesson: a stop on one of several parallel runs costs the job only what it adds to the slowest run.

## Default path

1. Read the program rules for the population (vessels of 10,000 TEU and over, cargo work begun in the fiscal year) and
   the outcome (berth time lost to crane breakdowns).
2. Build the large-vessel calls from the AIS berth segments (stitching the midnight cuts and reception gaps, keeping
   the two vessels on the shared MMSI apart) and the register; link each call to its TOS visit.
3. Link each CMMS breakdown to its crane through the asset crosswalk, converting local times to UTC.
4. Keep the breakdowns that fell while the crane was working a large-vessel call (between its first and last move on
   the visit) and charge each one's downtime to that call's stay.
5. Sum per terminal and pick the largest.

Ends on: Ordway
Golden: Pinecastle

## Stump sentence

The default path charges every hour a crane spent broken down while working a large vessel to that vessel's stay and
recommends Ordway, which logged by far the most such hours; but each crane works its own run of bays and the ship sails
when its slowest run is done, and Ordway's breakdowns fall on old cranes it gives the short runs, so they rarely
delayed a ship, while Pinecastle splits its ships evenly and nearly every stop there cost the ship its full length.

## Tried and rejected

- AIS dwell itself as the decisive quantity (2026-10-20, screened before the draw): once the midnight cuts, reception
  gaps and the shared MMSI are resolved, a call's berth time is fixed by its first and last pings, and the AIS
  endpoint problem under sparse reception is bracketed by the dense moving-state pings; Layer 1 only.
- A queue counterfactual for vessels that left the anchorage (2026-10-20, screened): the would-be wait is fixed only by
  a filed berthing order, which makes the decisive step the execution of that order.
- Night-flow leakage scaled through a pressure exponent (2026-10-20, screened): a water world, and a rate re-read at
  the decision's conditions through a profile sits close to task459's and task460's drivers.
- The GS&DS record-linkage subdomain under its own domain (2026-10-20): `ban.subdomain` against task473, filed the same
  morning; the build sits in the house domain instead, which maps to the same task type.
