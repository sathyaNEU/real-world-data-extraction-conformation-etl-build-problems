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

## Default path

The pipeline the measured opponent builds unsteered, from the prompt's words and the files' grain:

1. Read Attachment C (smac_program_terms_2026.pdf): C.4 proposes the candidate class with the largest ingredient spread over the twelve months of fills ending with the last closed quarter (April 2026 to March 2027), compared unrounded; C.5 makes the spread the ingredient cost paid on the class's claims, net of reversals, less what the dispensing pharmacies paid their suppliers for the units.
2. Conform the claims (corvane_ffs_claims_paid_2026-04_2027-04.csv): keep the fills from 1 April 2026 to 31 March 2027, net the B2 reversals, and place each NDC in its class through the drug file (state_drug_file_2027-04.xlsx, its ten-digit NDCs in three hyphen configurations converted to eleven digits) and the class list (state_drug_class_list_2027.xlsx, by GPC).
3. Cost each claim's units at the State AAC rate in effect for its NDC on the fill date (state_aac_rates_2025-04_2027-03.csv).
4. For the NDCs with no rate in effect (43 per cent of the candidates' ingredient cost), cost the units at the product's rate that month: the median rate of the product's priced NDCs.
5. Sum each class's ingredient cost paid less the acquisition cost and propose the largest.

Ends on: propose Antipsychotics, spread $65,405, 1.30 times Dementia agents' $50,473, with Anticonvulsants third at $50,061.
Golden: propose Anticonvulsants, spread $43,097, 1.43 times Antipsychotics' $30,124.

## Stump sentence

The default path proposes Antipsychotics at $65,405 because step 4 costs the claims no AAC rate covers at their product's rate, which the priced retail bottles set, while 86 per cent of those claims' ingredient cost is on unit-dose cartons the surveyed pharmacies rarely buy and which cost about 1.9 times the bottle per unit; costing each unpriced NDC from the priced NDCs of the same product and package type (a carton with no priced carton at its bottle's rate times the carton-to-bottle ratio of the products with both priced, 1.90) proposes Anticonvulsants at $43,097, 1.43 times Antipsychotics' $30,124.

## Three rules

Task type: General Statistics & Data Science / data-integration-record-linkage-entity-resolution, serving the ETL objective: the conformed class table (each candidate class's twelve-month ingredient spread) built from the claims, the AAC rates, the drug file and the class list.
Domain test: the deciding quantity is each class's ingredient spread, whose acquisition cost is observed only for the claims that link to a priced NDC; data integration's own analysis of the records that fail to link (the client's pattern general-statistics-data-science/data-integration-record-linkage-entity-resolution/1: missed links select, so the fill for the unlinked records conditions on what drives the miss) decides the call, and the generic fill (the product's average rate for every unlinked claim) files another class.
Swap: in this domain the swap is of the method: put the generic fill in place of the conditioned one and the call moves from Anticonvulsants to Antipsychotics; put a retailer's store margins in place of the classes and the object goes, because nothing there is linked to a price file whose misses fall on the costlier packages.
Layer 1: the drug file's ten-digit NDCs in three hyphen configurations against the claims' eleven digits; effective-dated rates with gaps and new entrants unpriced for months; reversals and rebills; usual and customary claims at discount pharmacies; the extract cut by paid date, so it carries earlier fills' late payments and reversals; the FY2026 summary by NDC and month with the class label stored when it was made; the class list by GPC; the managed care encounters and the PDL status beside them (inventory below).
Layer 2: field_method: the claims that do not link to a priced NDC are not a random draw of the class's claims, they are the packages the survey's pharmacies do not buy, so their acquisition cost is filled within product and package type, not at the product's average.
Decisive step: filling the acquisition cost of the claims with no rate in effect within their product and package type (a unit-dose carton costed from priced cartons, or from the bottle at the carton-to-bottle ratio the products with both priced show), not at the product's rate.
Not semantics: every field, code and unit read right (the NDC configurations, the effective dates, the reversals, the basis of cost, the package descriptions) still leaves the unpriced claims' acquisition cost to be estimated; the default path reads every field right and still proposes Antipsychotics.
Not rule application: C.5 files what the spread is and the methodology what a rate is, and nothing filed says how a unit with no rate is costed, so executing every filed rule with the natural fill (the product's rate) proposes Antipsychotics.
Analyst test: a strong analyst who conforms the claims, rates, drug file and class list and costs each unpriced NDC at its product's median priced rate that month proposes Antipsychotics, spread $65,405, 1.30 times Dementia agents' $50,473, against Anticonvulsants.
Estimand: Attachment C, C.4 and C.5: the candidate class with the largest ingredient spread over the twelve months of fills ending with the last calendar quarter closed before the proposal (April 2026 to March 2027), compared unrounded; the spread is the ingredient cost the Program paid on the class's fee-for-service claims, net of reversals, less what the dispensing pharmacies paid their suppliers for the units; the candidates and their class list are the Department's request letter's, and the claims are those paid through 20 April 2027 (the prompt).
No decoy: nothing is planted to be caught: the unpriced cartons are how a survey of community pharmacies' invoices sees the market, and no memo, draft, briefing or stakeholder figure states a spread, a fill or a carton's cost.
No certified replay: no published spread, acquisition estimate or carton price ships; the rate file is the survey's own publication, used as filed.
Lesson: a fill for the records that fail to link must condition on what drives the failure to link when it also drives the value, here the survey's blindness to the cartons that cost more; no build on file teaches it (task449 took the other half of the pattern, false links diluting a share).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the priced claims alone | C.5 puts the spread on every claim | the rates join | yes (complete case) | no | no | no | readable |
| R1 the product's rate for the unpriced NDCs (default) | C.2 and the methodology price NDCs one by one | the GPC ties a product's NDCs | yes | no | no | no | readable |
| R2 the product's highest rate (a cautious fill) | no | the GPC | yes | no | no | no | readable |
| R3 (decisive) the fill within product and package type | no: no document names a package type, a carton's cost or which pharmacies the survey samples | no package column: the type is read from the drug file's package description | no: the reflex fill is the product's rate | no control scores an acquisition cost | the battery does not find it | no: a fill within a cell built from text, then a ratio for the cells with no priced carton | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | ingredient spread | the ingredient cost paid less the units' acquisition cost | the dispensing fee counted in the paid amount | Anticonvulsants under every fill, the default's included: the fees, a fixed sum a claim, outweigh every spread and rank the classes by their claims (asserted); the reading moves every spread by hundreds of thousands | the prompt's "ingredient spread" and C.5: "the ingredient cost the Program paid"; the extract files the fee in its own column |
| SF2 | net of reversals | B2 reversals netted against their claims | reversals left in as paid claims | same call (asserted) | C.5: "net of reversals" |
| SF3 | over fills from April 2026 to March 2027 | fill dates in the window | the transactions paid in those months, whatever the fill date | same call (asserted) | the prompt and C.4 say fills |
| SF4 | the class | through the drug file's GPC and the class list in force from 1 January 2027 | none left: every claim places | every claim placed (asserted) | the request letter names the list |
| SF5 | the rate a priced unit costs | the AAC rate in effect for the NDC on the fill date | the NDC's latest rate for every fill | same call (asserted) | C.2: "the State AAC rate in effect for the NDC on the fill date" |
| SF6 | usual and customary claims | kept, at what was paid | left out | same call (asserted) | C.5 counts the class's claims |
| SF7 | the unpriced NDCs' claims | kept in the class and costed | left out (the priced claims alone) | no class carries a spread to rank: every spread within $50 of zero (asserted) | C.5 counts the class's claims and the units they dispensed |
| SF8 | the comparison | unrounded (C.4), reported to the nearest thousand | rounded first | the same class leads (asserted) | C.4: "The comparison is made on unrounded figures" |
| SF9 | how the package-type fill is carried out | the median priced rate of the same product and package that month; a carton with no priced carton at the bottle's median times the class's carton-to-bottle ratio | the mean; every carton at the bottle's rate times the class or the pooled ratio; priced cartons first with the pooled ratio; the whole window's median | the call by 1.43 under every one, every class's spread in the golden's thousand, 200 or more from an edge (asserted) | C1: the records make every implementation converge |
| SF10 | the claims in hand | those paid through 20 April 2027, nothing completed for payments to come | the window's fills completed for late payments | the figures would move | the prompt: "now that the claims paid through 20 April 2027 are in" |
| SF11 | an FY2026 claim's class | through the drug file and the list in force from 1 January 2027 | the summary's stored label | the workbook misses every figure (asserted) | the request letter: "The classes are those of the drug class list in force from 1 January 2027" |
| SF12 | the FY2026 payments | the summary's (paid through 20 April 2026) and the extract's later ones, the 1 to 20 April 2026 payments once | the summary alone; the extract's FY2026 fills added from its first paid date | the workbook misses every figure (asserted) | the data delivery note (the summary holds the transactions paid through 20 April 2026; the extract every transaction paid from 1 April 2026 to 20 April 2027, whatever the fill date) |
| SF13 | units dispensed | the claims' metric decimal quantities as filed (each, or millilitres for liquids) | none credible | same figures | the record layout's quantity_dispensed |

## Ladder

As built (`generator/checks.py` asserts each rung by name; `verify.py` recomputes the golden and the default from the bundle alone).

| Rung | Method | Proposes | Dies to |
|---|---|---|---|
| R0 | the priced claims alone | none: every class's spread within $50 of zero | the spread lives on the claims paid at WAC |
| R1 (default) | the unpriced NDCs at the product's median priced rate (the mean and the lowest rate likewise) | Antipsychotics $65,405, 1.30 over Dementia agents (1.27 on the mean); Anticonvulsants third (fourth on the mean) | the cartons cost 1.9 times the bottle per unit |
| R2 | the product's highest priced rate | Antiparkinson agents, 1.04 over Dementia agents; Anticonvulsants fourth | the highest rate is a carton's only where the carton is priced |
| R3 (golden) | the fill within product and package type | Anticonvulsants $43,097, 1.43 over Antipsychotics $30,124 | none |

- **Separation.** R1 and R2 name different wrong classes; the golden adds a third.
- **Position.** On the default path Anticonvulsants is third ($50,061 against Dementia agents' $50,473).
- **Dominance.** The default fill overstates Antipsychotics' spread by $35,281 and Anticonvulsants' by $6,964: the long-term care share of the class decides how much of its unpriced cost sits on cartons.
- **Worth.** Package type alone takes the default path to the golden on the clean truth (R3b asserted); the mean, the lowest rate and the highest rate each stay wrong.
- **Bins.** Every class's spread sits in one thousand under every implementation of the fill (SF9), at least $200 from an edge.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the candidate classes' fee-for-service claims on fills from 1 April 2026 to 31 March 2027, paid through 20 April 2027 | C.4, C.5, the prompt |
| 2 | Unit of account | a claim transaction, reversals netted | C.5; SF2 asserted |
| 3 | Attribution window | the fill date | C.4 and the prompt; SF3 asserted |
| 4 | As-of dating | the extract of 21 April 2027 (paid through 20 April 2027); the rates as published to 1 April 2027 | the prompt; SF10 |
| 5 | Version basis | the class list in force from 1 January 2027 | the request letter; SF11 asserted |
| 6 | Denominator | none: the spread is a sum | not applicable |
| 7 | Weighting | each claim's units at its rate | C.5 |
| 8 | Window length | twelve months | C.4 |
| 9 | Boundary inclusivity | 1 April 2026 to 31 March 2027 inclusive | C.4 and the prompt |
| 10 | Rounding path | compared unrounded, reported to the nearest thousand dollars; the FY2026 money to the dollar and units whole | C.4 and the prompt; SF8 asserted |
| 11 | Tie-break | none needed (1.43) | asserted |
| 12 | Maturity and censoring | payments after 20 April 2027 not in hand | the prompt files the as-of; SF10 |
| 13 | Order of operations | net the reversals, cost each claim, sum by class | C.5 |
| 14 | Row order | none | not applicable |
| 15 | Duplicate resolution | a rebill is a new claim after its reversal | netting handles it; SF2 |
| 16 | Identity normalisation | ten-digit NDCs to eleven digits by configuration | every claim places (asserted); never the stump |
| 17 | Netting against gross | ingredient cost net of reversals | C.5 |
| 18 | Dimensional units | rates per pricing unit (each or millilitre), quantities in the same unit | the methodology and the record layout; SF13 |
| 19 | Code and status semantics | B1 and B2; AAC, WAC and U&C bases | the record layout; SF6 |
| 20 | Integerisation | money and units rounded once, at the end | the prompt |
| 21 | Clause scope | C.2's pricing covers every claim, C.5's spread every claim of the class | filed once in Attachment C |
| 22 | Forward window contents | the decision is the 1 July 2027 update, taken on the closed twelve months | retrospective by C.4: the terms rank on the last closed quarter's year |

## Literal reader

Executed word for word, C.4 proposes the candidate with the largest ingredient spread over fills from April 2026 to March 2027, compared unrounded, and C.5 makes the spread the ingredient cost paid on the class's claims, net of reversals, less what the pharmacies paid their suppliers for the units; the methodology says a rate is an NDC's average invoice price per unit and that not every NDC has one. For a unit with no rate nothing filed says how it is costed: that is HOW, and the data force it (the unpriced NDCs are overwhelmingly unit-dose cartons, whose priced siblings cost 1.9 times the bottle), and every implementation of the package-type fill gives the same call and every spread in the same thousand (SF9). The prompt fixes the claims in hand (paid through 20 April 2027). For the FY2026 workbook the request letter's list defines the classes, and the claims paid through 20 April 2027 on FY2026 fills are the summary's (paid through 20 April 2026) and the extract's later payments, the overlap counted once.

## Oracles

None. The summary's control totals tie to its own detail under any class mapping and any paid-date handling; the data delivery note's row counts tie to the files; no published spread, acquisition estimate or carton price ships.

## Ask sheet

**The FY2026 workbook.** Figures: for each of the twelve candidate classes, its claims (net of reversals), units dispensed and ingredient cost paid over fills from April 2025 to March 2026 (36 figures; claims and units whole, money to the dollar). H18 home: C.6's budget figures, which the proposal sets out beside the spreads. Use: the Department's budget for the update. Primary device: D2, a label stored before a silent switch: the FY2026 summary carries each NDC's class as the list then in force gave it, and the 1 January 2027 revision moved 16 products, so every candidate class gained or lost one. Secondary device: D8, a clock against a cutoff: the summary holds the transactions paid through 20 April 2026, the FY2026 fills' later payments (1,265 transactions: late claims and reversals) sit only in the extract, and the extract repeats the 1 to 20 April 2026 payments (3,131 transactions). Path: the summary, the extract, the drug file, the class list, the request letter, the terms (C.6), the record layout and the data delivery note (eight files; the columns NDC, Drug class, Claims, Units and Ingredient cost paid; fill_date, paid_date, transaction_code, quantity_dispensed, ingredient_cost_paid and ndc; the GPC; the class code). Stops: the summary by its stored label (Anticonvulsants 50,508 claims against 40,046); the summary alone with the current classes (39,823); the stored label with the later payments (50,731); the later payments added from 1 April 2026 (40,247). Realism: an administrator's year-end summary is cut a few weeks after the year closes and labels classes as they stand that day; pharmacies submit claims months late for retroactive eligibility or after a rejection.

Main population zero-counts (asserted): the stored labels sit in the summary, which the main call never reads; the FY2026 payments in the extract are fills before the window, which the main call's population (window fills) excludes.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| FY2026 workbook, 36 figures | maps the summary's NDCs to the current classes but takes the summary as the year: every class short by its later payments (Anticonvulsants 39,823 claims, 2,398,040 units and $201,943 against 40,046, 2,412,350 and $203,083) | miss |

Mirror leakage: 0 per cent (the mirror, on the default fill, reads the summary by its stored label and keeps no FY2026 figure).

Pair ceiling: 36.1 (planning weights 38 / 7 / 55, r = 5; the cracker keeps the main block, its twelve spreads and no FY2026 figure, 38 + 7 + 55 x 12/50 = 58.2; the mirror keeps r, instruction-following and about one chart criterion, 5 + 7 + 55 x 1/50 = 13.1; (58.2 + 13.1) / 2 = 35.7, plus 0.4 for a chart criterion either may keep).

Criteria: the call, the runner-up and the gap, twelve spreads, about four chart criteria, 36 FY2026 figures and two files, about 57.

## Layer 1 inventory

Each item, the system that writes it, its file and its natural mishandling; the R2 block in `checks.py` asserts the golden with the item mishandled.

| Item | System | File | Mishandled | Effect (asserted) |
|---|---|---|---|---|
| ten-digit NDCs in three hyphen configurations | the FDA's labeler, product and package code lengths | the drug file | padded on the left | most claims lose their product: loud, no route stops there |
| effective-dated rates | the survey's monthly publication with a 2 per cent update threshold | the rate file | the latest rate for every fill | same call |
| reversals and rebills | claims adjudication | the extract | reversals left in as claims | same call |
| usual and customary claims | discount pharmacies' charges below the rate | the extract | left out | same call |
| the extract cut by paid date | the administrator's extract by payment | the extract | every row taken as a window claim, or the payments of April 2026 to March 2027 taken whatever the fill | same call |
| new entrants unpriced for months | the survey's purchase-count rule | the rate file | (part of the fill) | the golden family converges |
| the summary's stored class label | the administrator's year-end summary | the summary | read as the current class | the FY2026 workbook only (D2) |
| the summary's paid-through cut | the summary's date | the summary | read as the year | the FY2026 workbook only (D8) |

## Pre-ship check

- **Three rules.** Domain: data integration's own analysis of the records that fail to link, the acquisition cost of the claims no AAC rate covers filled within product and package type because the misses fall on the costlier cartons (the swap of the method in the Three rules section moves the call). Two layers: the Layer 1 inventory (NDC configurations, effective-dated rates, reversals, U&C, the paid-date cut, stored labels), each asserted neutral to the call or confined to the FY2026 workbook; Layer 2 the conditioned fill. Decisive step analytical: the strong analyst who reads every field right and executes every filed rule files Antipsychotics (R3a on the clean truth, asserted).
- **Gates.** 12 files in 4 formats (csv, docx, pdf, xlsx); the claims extract at 229,247 rows; two distractors (the managed care encounters and the PDL status) the solution never reads; 102 checks; `verify.py` from the bundle alone; two builds byte-identical; `figures_check.py`, `precut.py` and `voice-check.py` exit 0; `leak.py` REVIEW (no LEAK); guard surface clean, heart WARN (answered in the Draw); the containers carry the fiction's people and dates.
- **The main call after stage 4.** The fixes (step 4 states the spreads rounded; the record layout without its file-level rows, which moved to the delivery note; each organisation's own page frame; the managed care summary priced by class) moved no graded figure: the call, every class's spread and every FY2026 figure in `figures.json` are the ones the judge reproduced.

## Leak check

- `leak.py`: REVIEW, no LEAK (the terms carry the call's vocabulary as the governing contract; the terms, the methodology and the delivery note carry stump-paragraph terms without naming the move).
- Reader, first pass (2026-10-13): no decisive-step sentence, no ranking file, no answer-like figure; the literal reading of C.4 and C.5 leaves the cost of a unit with no rate open (as designed); question 6 an analytical choice, the reversals, fill dates and effective dates it names asserted neutral (R2). Realism tells fixed in the generator: the record layout's "(file)" pseudo-rows, one page frame on three organisations' PDFs, the managed care summary's class-blind prices.
- Reader, second pass on the rebuilt pack (2026-10-13): questions 1 to 4 none; question 5 as designed; question 6 the analytical choice of how to value the units with no AAC rate. Realism: the delivery note's line limiting claims to the candidate classes now names the claims extract alone (the summary is the full generic summary). No third pass: that sentence is not near the decisive step.

## Determinism judge

- Stage 4 (2026-10-13): DETERMINISTIC, APPROVE. Every graded figure reproduced from the bundle (the 224,851 window transactions, 43.4 per cent of the cost unpriced and 86.2 per cent of that on cartons, the carton-to-bottle ratio 1.897 to 1.900 across 68 products, all twelve rounded spreads, all 36 FY2026 figures with the 1,265 later payments); the call holds across the median or mean, monthly or whole-window peers and carton ratios of 1.8 to 2.0, and the package-blind fill gives Antipsychotics at $65,000. Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no (borderline: the missing rates are the survey's documented structure). Gate H domain pass, layers pass, decisive step analytical. Findings: step 4's unrounded Antiparkinson figure ($23,177 against the judge's $22,804 to $22,929, the same thousand) fixed by stating the spreads rounded; the unfiled cost of a unit with no rate is the design's HOW, closed by the data (SF9), and kept unfiled. Report: `determinism_check_report.md`.

## Tried and rejected

- 2026-10-13, draw: health economics' payment and claims analytics as the task type (the seed's natural home). Rejected by the pairing rule: task451 holds it among the last three builds.
- 2026-10-13, draw: test equating (education) as the task type. Rejected: task450 drew it four builds ago, and a second form-linking task in one lane reads as a template; data integration is the other ETL task type open.
- 2026-10-13, draw: the State's Medicaid agency as the deciding organisation. Rejected by the guard (government agency among the last three); the administrator the State contracts proposes the class, as such contracts run.
- 2026-10-13, the ask: one device (the summary's stored class labels) with C.5 also saying which list defines a class. Rejected: a filed sentence adjudicated the device. C.5's sentence came out (the request letter alone names the list), and a second device was added: the extract is cut by paid date, so the FY2026 fills' later payments sit only in it and its 1 to 20 April 2026 payments repeat the summary's.
- 2026-10-13, the spreads at the nearest thousand: the package-type fill's implementations (median or mean, priced cartons first or the bottle times a class or pooled ratio, month by month or the whole window) split Antipsychotics (28,000 or 29,000) and Antiparkinson agents (23,000 or 24,000), and left Benzodiazepines, Loop diuretics and Anticonvulsants within $120 of an edge. Rejected: shipping that, since the task448 judge flagged the same fragility on one figure. The carton premium and the labelers' price factors were drawn tighter (repackagers price off the same bottles), lacosamide's price drift was halved to 5 per cent a year, and five classes' volumes were re-centred, so every class sits in one thousand under every implementation, 200 or more from an edge (SF9).
- 2026-10-13, the pack's surface: a field-description CSV with task453's exact column set and a text transmittal, back to back with task453 (guard surface promoted the pair). Rejected: kept the administrator's record layout with data types (file_name, column_name, data_type, definition) and a Word data delivery note.
