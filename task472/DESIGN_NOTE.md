# task472: Ternmouth Port Authority, where the 2027 replacement quay cranes go

Architecture 2, a re-root drawn on 2026-10-20 in the same objective (Data Extraction & Conformation) and the same
number. Architecture 1 (the berth hours crane breakdowns cost a call, read through the slowest of its parallel crane
runs) was spent at stage 4 the same day, both scored readers landing the call; its record is the last line of
`## Tried and rejected` and the card's lineage.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task472.json` (architecture v2, lineage v1), registered 2026-10-20 after a
  pull. Guard WARN on `overuse.objective` (ETL in 4 of the last 12 builds): the lane is ETL by assignment (task468 to
  task477 are the ETL backlog), so the objective is not a free axis here. The structural NOTE against the slot's own
  architecture 1 (driver similarity 0.16) is differentiated on the card; the nearest other driver is task160 at 0.04,
  and the card is differentiated against task92 (a capped service valued only on the days a candidate receives it).
- **Seed:** ET29 (a port authority funds new ship-to-shore cranes at one of six container terminals on the berth time
  of large cargo vessels). Kept: the world (one authority, six terminals, AIS and the terminals' own records), the
  decision (where the cranes go) and the quantity (berth time of large vessels). The seed's mechanism (AIS stretches cut
  at midnight UTC and at hour-long gaps) stays Layer 1.
- **Pairing:** Supply Chain & Logistics (house domain, ports and terminals; card subdomain `transportation-network`)
  sitting in General Statistics & Data Science, task type `data-integration-record-linkage-entity-resolution`, the only
  ETL task type the house domain maps to. The ETL work is real linkage: AIS berth stretches keyed by MMSI, two terminal
  operating systems keyed by visit and crane, the pilot dispatch keyed by vessel name and call sign in local time, the
  bar's tide predictions in local standard time, and the vessel register keyed by IMO, conformed into one large-vessel
  call table. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the Crane Replacement Program places the 2027 order's six cranes at the terminal
  where they would have cut the most berth hours from the last closed fiscal year's large-vessel calls, the program
  taking a replacement set to cut each such call's cargo work (first container move to last) by a fifth and leaving
  everything else about the call as it was. Retrospective by design: the board places the 2027 order on 27 October
  2026 on the record of fiscal year 2026, the last closed year, as arch 1 did.
- **Strategy:** `binding_constraint`; Gate G `binding_constraint` (a filed operating window, the tide at the river bar,
  removes the natural pick while every reported figure is correct); gap `objective` (the call is scored on berth time,
  which the cargo time saved does not equal where the release is gated), then `time` (the window a ship makes);
  pattern none, generators G7 (operating window, pinned in the Harbour Master's directions, never the prompt), G13,
  G3; Layer 2 family `allocation_constraints`, pattern `own:tide-window departure in a cargo-time counterfactual`.
- **Data-native sentence:** at Ternmouth the two river terminals lie up the Salt River, where a ship leaving with a
  draught of 12.5 m or more must pass Salt Point inside a window around high water, so a large ship's stay there ends
  at a tide rather than at its last container move; Saltworks' planners finish cargo for the window, so its ships wait
  hours alongside, while at Millrace the old cranes overrun and ships miss the window they were worked to.
- **Sources, one line each:** seed ET29 (the world and the decision, never its mechanism); the slot's architecture 1
  (the counterfactual stay, solved by readers when the outcome named it, so here the outcome names only a cargo cut and
  the gate lives in a navigation document); task92 (a service valued only on the days it is received, recovered from
  history: here the windows are filed and the quantity is a departure); task87 and task229 (G7 operating windows on
  other ground); strategies F3 (binding constraints held when the limit is shared and died as a per-candidate argmax:
  here the limit is not a cap on a candidate's metric but a gate inside each call's counterfactual, and it moves the
  two river terminals in opposite directions).
- **Same-puzzle test:** gap objective, decisive generator G7, decision pick_one_of_n against the last twelve builds,
  lineage included: no match (task92 and task87 are older and carry pattern C or gap time first). Same-driver test
  (gap, G7, binding_constraint): no match in the last twelve; task92 differentiated on the card.
- **Abstraction test:** nearest drivers stripped of nouns (task160's lagged wave, task167's allotment schedule, task99's
  phased start delay) carry no release window gating a counterfactual saving; none maps onto this driver.

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
- Architecture 1, the slowest-crane counterfactual over a call's parallel crane runs (2026-10-20, spent at stage 4):
  both scored readers landed the call (score_reader exit 1 on each: Pine Neck 263 against Halyard 184, every
  terminal exact), each reading rule 2.4's "taken together, lengthened its stay alongside" as the instruction to
  take the latest crane finish with and without its stops, and the whole-hour terminal totals confirmed the
  construction to both; reader 1 also cracked ask A (the berth zone's gaps bridged, anchorage shifts kept apart)
  and reader 2 ask B (status history joined to the BD type, the parallel run's copies counted once). A quantity
  the filed outcome names outright is computed by asking the question; the next decisive step must be one a
  careful analyst who asks the right question still estimates wrongly, and no graded figure is tuned to a bin
  centre.
