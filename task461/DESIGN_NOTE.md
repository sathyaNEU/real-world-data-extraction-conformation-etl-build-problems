# task461 design note

Architecture 1, drawn 2026-10-15 from seed ET18 (the world, the decision and the quantity; the pitfall re-found from
the data).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task461.json`, registered 2026-10-15. Guard PASS; the older same-driver
  signature (gap time, G13, method_or_model_selection) against task229 v2 and task501 v4 is differentiated on the card.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL, own pattern
  short-record-extension-through-overlap. Energy Systems & Utilities has no task type serving ETL, and emissions
  accounting (the ETL home of the last build) is barred back to back; data integration is the ETL task type whose own
  statistical object decides this call: combining a short direct record of the target with a long record of a
  correlated source through their overlap. The setting is the power market's, as General Statistics requires, and the
  swap is of the method.
- **Why this task type:** task449 (false links to the first plausible target), task454 (cost filled where a survey
  covers one presentation) and task456 (prevalence read through three erring feeds) spent linkage, coverage and
  multi-source misclassification; none carried a short record over a long one through their overlap.
- **Shape:** 04, one dial set from an allowed menu. Arithmetic: the threshold picked, the next lower setting and why it
  is passed over (3); for each setting on the menu, the expected 2027 cycling days at the node (9 settings); the node's
  overlap relationship with the hub (2); the conformed daily-spread file (1); the asks on the battery's 2026 operation
  (about 12): 27 or more.
- **Strategy:** population_selection (the days the spread distribution is taken over: the node's one observed year
  against the full weather record carried to the node) on the time gap (the evidence at the node covers one mild,
  windy year; the decision bets on an ordinary 2027), the population gap behind it (the hub's days are not the node's).
  Generators G13 (horizon) decisive, G14 (conditioned yield) and G16 (the overlap's functional form) behind.
- **World:** Tallgrove Storage Partners, an independent storage owner (invented), runs Redrock Draw Energy Storage, a
  100 MW / 400 MWh battery at its own settlement point in the Midplains Power Market (invented), created in September
  2025 when the project's substation was energised; the market's North Hub has day-ahead prices back to 2019. The
  battery cycles once on each day whose day-ahead spread at its node clears a threshold the owner sets in its trading
  system each year from a menu of settings; the supply warranty allows 300 full cycles a contract year.
- **Forcing fact:** the trading services agreement requires the 2027 operating parameters by 1 December 2026, for the
  contract year starting 1 January 2027. The call faces forward (2027's cycling).
- **Forum and forcing event:** executive_team (the owner's management team approves the 2027 operating plan),
  purchase_order_or_contract (the trading services agreement's parameter deadline). Organisation
  utility_or_infrastructure; role portfolio_manager (the asset manager for storage). Personas from `guard.py names
  --geo "United States" --seed 461`: Stacey Garrett (asset manager for storage), Hailey Cooper (market analyst).
- **Data-native sentence:** a node created with its battery has a direct price record only as long as the battery has
  run, and that stretch is one draw of weather; the hub's record spans the weather the market has seen, and the node's
  spreads move with the hub's in proportion (the congestion that widens them scales with the swing), so only the hub's
  years carried through that proportion show what an ordinary year looks like at the node.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data integration: propagate the integration's error to the
    estimate; here the integration is a record extension and its error is the form of the relationship.
  - `stumping/references/client/two-layer-task-design.md`, estimation that fits the data: the relationship the overlap
    shows (proportional, through the origin), not the market's additive basis convention.
  - `dataset-generation/references/layer1-messiness.md`: hour ending 24:00 on prevailing time, 23- and 25-hour days,
    a yearly archive whose layout changed, a renamed settlement point, test-period prices; none on the decisive step.
- **Same-puzzle and abstraction:** gap time, G13, Gate G method_or_model_selection, decision dial_setting. Nearest
  drivers on file 0.04 to 0.05 (task255, task457 lineage, task256, task135); none extends a short record through a
  long one.

## Tried and rejected

- 2026-10-15, draw: the seed's own stump, a replay grouped by UTC dates that moves the charge and discharge hours across
  the operating day. Rejected: catching the clock is reading a field correctly (data semantics), banned as the decisive
  step; the clocks stay as Layer 1 mess and must leave the call where it is.
