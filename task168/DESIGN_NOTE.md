# task168 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task168.json`, registered 2026-10-18T06:47:15Z, guard WARN (no BLOCK) against the registered card.
- **Pairing:** Supply Chain & Logistics (house domain `supply-chain-logistics`, task type transportation network), client domain Urban & Regional Science, task type `forecasting` (transport demand forecasting). Objective Forecasting & Predictive Modeling.
- **Seed:** FC39. Kept: the world (an airline whose summer schedule upgauges nine routes that run full every summer), the decision (the figure the outstation handling tender and the summer budget are built on) and the quantity (the additional passengers those routes will carry over last summer). Not kept: the seed's planning standard (demand as carried plus denied bookings), which would be a filed basis whose literal execution gives the wrong figure.
- **Strategy:** `population_selection`. The decisive step completes each sold-out departure's demand from the booking build of departures that never sold out, and the population that build is read from is selected on the outcome: departures that never sell out are the slow-booking, slow-season ones. Layer 2 family `estimation_fit` (censoring and truncation). Decisive generator G16 (which build the data entitles), then G6 (the sold-out departures' month mix against the reference's) and G12 (a sold-out departure's later demand is absent, not zero).
- **Furniture:** forum executive_team; forcing event season_or_peak (the summer 2026 season the handling tender and the budget have to be in place for); organisation other (a passenger airline); role capacity_planner (head of network planning); context artifact filed_standard (the summer 2026 planning basis that files the estimand); calibration prior_period_close_out (the routes upgauged for summer 2025, before and after).
- **Personas** (`guard.py names --geo Italy --seed 168`): Ugo Pacomio, Concetta Gaito, Piero Turchetta, Vincenza Passalacqua. Damiano Caruso (a real cyclist's name) and the drawn names carrying famous surnames were passed over.

## Tried and rejected

