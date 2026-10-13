# task454 design note

Architecture 1, drawn 2026-10-13 (wave 3, oviya1301), from seed ET11 (a state Medicaid pharmacy team extending its maximum-allowable-cost list by one drug class, comparing what fee-for-service pays with acquisition cost). Kept: the world, the decision (one class added to the list) and the quantity (each class's ingredient spread). Not kept: the seed's mechanisms (NDC formats, effective dates and the dispensing fee inside the total), which are data semantics. They survive here only as Layer 1, neutral to the call. The pitfall is re-found in the data: the claims that fail to link to the price survey are a selected subset.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task454.json`, architecture v1, registered 2026-10-13; `guard.py check` WARN only. Each WARN is answered here.
  - `two_layer.pattern_reused` (the record-linkage pattern, as task449): task449 inverted false links (a record attached to the first of several equally plausible targets, diluting a share). This build is the other half of the pattern: missed links are selected, and the fill for the records that do not link has to condition on the variable that drives both the missed link and the outcome.
  - `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, as task452):
    - task452's mechanism is the estimator of an unsampled day's concentration.
    - Here it is how the integration fills the cost of the claims the price survey does not cover.
    - The two share no file shape, unit or default path.
  - `overuse.objective`: the lane is ETL.
  - `repeat.question_form` (which, as task453): the call is a pick of one class from a shortlist, and a pick asks which.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data Extraction & Conformation (ETL).
  - The setting is a state Medicaid fee-for-service pharmacy program; the field is data integration.
  - Swap of the method (the test for this domain): replace the conditioned fill of the unlinked claims with the generic fill (the product's average price) and the call changes.
  - Health economics' payment-and-claims task type, the seed's natural home, is banned by the pairing rule (task451 among the last three).
- **Objective:** ETL. The conformed dataset is one row per shortlisted class with its twelve-month ingredient spread, built from four sources:
  - the pharmacy claims (eleven-digit NDCs, reversals, effective dates);
  - the State's acquisition cost rates (effective-dated, one NDC at a time);
  - the drug file (ten-digit NDCs in three hyphen configurations, products and package descriptions);
  - the class list (classes assigned to generic products, not NDCs).
  - The decision reads off that dataset. Retrospective by design: the State's rule ranks the shortlisted classes on the twelve months to the last closed quarter, and the list update takes effect on 1 July 2027.
- **Shape:** 07, a grid of cells (one row per shortlisted class, three figures each). Criteria arithmetic:
  - the call, the runner-up and the gap (3);
  - each class's ingredient spread (12);
  - two ask figures per class (24);
  - the chart's parts (4);
  - the two files.
  - About 45.
- **Strategy:** composition_mix. The claims paid at WAC (no State rate in effect) are not a random draw from the class's claims: they concentrate on the packages the surveyed pharmacies do not buy. The decisive move fills their cost within the right composition cell.
- **Mechanism:**
  - Gap: population. The linked claims are not the population whose spread is wanted.
  - Pattern C: the class's spread is a share built behind a join, and the winner's edge has to clear what the decoy carries in the wrong fill.
  - Generator G4.
  - Gate G: method_or_model_selection. Layer 2: field_method, the client's pattern `general-statistics-data-science/data-integration-record-linkage-entity-resolution/1` (propagate linkage error to the estimate: missed links select).
- **World:** an unnamed US state's Medicaid fee-for-service pharmacy program, whose claims are processed by a contracted pharmacy benefit administrator. Under contract, the administrator also maintains the State Maximum Allowable Cost (SMAC) list and proposes one drug class a year for it.
  - The State reimburses the ingredient at the lesser of the usual and customary charge, the State actual acquisition cost (AAC) rate in effect for the NDC, or, where no AAC rate is in effect, the WAC; a professional dispensing fee is paid separately.
  - A survey contractor sets the AAC rates monthly from invoices that sampled pharmacies submit. An NDC is priced when enough invoice lines arrive.
  - The surveyed pharmacies rarely buy the unit-dose cartons long-term care pharmacies dispense, so most of those NDCs have no rate and are paid at WAC. A unit-dose carton costs more per unit than the retail bottle of the same product.
- **As-of:** fills from 1 April 2026 to 31 March 2027, the claims extract of 21 April 2027, the AAC rates published to 1 April 2027, and the proposal due to the State on 3 May 2027 for the 1 July 2027 list update.
- **Furniture:**
  - Forum customer_or_counterparty: the administrator proposes and the State's Medicaid pharmacy director approves.
  - Forcing event launch_or_rollout: the 1 July 2027 list update.
  - Organisation professional_services.
  - Role procurement_lead: the administrator's MAC pricing lead; the prompt names no one.
  - Context artifact published_series: the State AAC rate file. Calibration none.
- **People:** drawn with `guard.py names --geo "United States" --seed 454`, on the card:
  - Sonya Burton, the State's Medicaid pharmacy director;
  - Todd Allen, the administrator's account director;
  - Carrie Arellano, the administrator's MAC pricing lead;
  - Jeff Strickland, the survey contractor's project manager, who signs the AAC methodology.
- **Data-native sentence:** the AAC survey sees only what the sampled pharmacies buy, so the NDCs it leaves unpriced (and the State pays at WAC) are the unit-dose cartons long-term care pharmacies dispense. Those cartons cost more per unit than the retail bottles of the same product. Costing each unpriced NDC at its product's rate books the cartons at the bottle's cost and swells the spread of the classes long-term care dispenses most. On a survey that priced every NDC, or one whose gaps fell at random, the trap would not exist.
- **Sources, one line each:**
  - `layer2-rigor-patterns.md`, data integration 1 (false links attenuate, missed links select; the shortcut takes the links as truth): the links here are exact NDC matches. The error is in what the integration does with the records that do not link.
  - `strategies.md`, every reflex lands wrong. Each reflex for a missing price files a wrong class:
    - the product's average or median rate;
    - the product's cheapest or most-dispensed NDC;
    - scaling the linked spread up by coverage.
    - Only costing within the product and package type reaches the golden, and every variant of that does.
  - `layer1-messiness.md`, claims and pricing (NDC formats, effective-dated rates, reversals, pricing units): Layer 1, every item neutral to the call and asserted so.
  - task449 (false links in a complaints desk): the same task type, the other half of its pattern, a different world, decision type and file shape.

## Tried and rejected

- 2026-10-13, draw: health economics' payment and claims analytics as the task type (the seed's natural home). Rejected by the pairing rule: task451 holds it among the last three builds.
- 2026-10-13, draw: test equating (education) as the task type. Rejected: task450 drew it four builds ago, and a second form-linking task in one lane reads as a template; data integration is the other ETL task type open.
- 2026-10-13, draw: the State's Medicaid agency as the deciding organisation. Rejected by the guard (government agency among the last three); the administrator the State contracts proposes the class, as such contracts run.
