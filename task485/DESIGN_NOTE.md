# task485 design note: the Employees' Group Health Plan's 2027 preferred drug list, each product's fiscal 2026 net cost with its manufacturer's remittances traced to the products that earned them (architecture 5)

Status lives in `pipeline.json`; this note holds the design. Architecture 5, drawn 2026-11-01 at the Batch 3 queue
reset: architecture 4 (an island Statistics Unit's provisional long-term immigration by employment sector) shipped
on 2026-10-26 with no portal result and was re-rooted with its world closed, one architecture per world. A fresh
client domain, world and mechanism on the lane's objective (Data Extraction & Conformation); the candidates screened
before this one are in `## Tried and rejected`, with the four earlier architectures' records below the design.

## Draw

- **Card.** `.claude/skills/fingerprint/cards/task485.json`, v5, registered 2026-11-01. Client domain
  healthcare-delivery-health-economics, task type payment-claims-health-plan-analytics, objective etl, shape 03,
  decision designation_set (one preferred product per reviewed class), gap objective and population, generators G2,
  G1 and G19, Gate G mechanism decomposition_attribution, strategy composition_mix, forum trustees_or_governors,
  forcing event season_or_peak (the list file is due before open enrollment), org family government_agency.
- **World.** A state's Office of Employee Benefits administers the self-funded Employees' Group Health Plan for four
  participating employer accounts (State Agencies, Higher Education, Local Government, Non-Medicare Retirees). Its
  pharmacy benefit manager, Halcroft Pharmacy Solutions, passes manufacturer rebates through under Exhibit C of the
  services agreement and remits them each quarter as one amount per manufacturer, plan account and quarter of service,
  never per product. The Pharmacy and Therapeutics Committee reviews six brand classes for 2027; policy EB-RX-04 puts
  on the preferred tier, in each, the therapeutically equivalent product with the lowest fiscal 2026 net cost per
  30-day supply. The Committee meets on 21 October 2026, the Board of Trustees on 28 October, and the PBM needs the
  list file by 6 November.
- **Fiction as-of date: 19 October 2026** (`leak.py --asof 2026-10-19`).
- **The call.** The preferred product in each reviewed class for 2027: Velantro (GLP-1 receptor agonists), Empriva
  (SGLT2 inhibitors), Glarvia (long-acting insulins), Apiqor (direct oral anticoagulants), Bevoria (inhaled
  corticosteroid and LABA combinations) and adalimumab-kvrn (adalimumab products).
- **Retrospective basis, forward call.** The tier placement governs 2027, a window not yet open; the deciding
  quantity is fiscal 2026 net cost because policy EB-RX-04 3.3 files the latest fiscal year with all four quarters'
  remittances as the basis. No forecast enters the call and it is not tagged Forecasting.
- **Personas** from `guard.py names --geo "United States" --locale en_US --seed 485`: Maria Burgess (director of
  pharmacy benefits), Brenda Cook (chair, Board of Trustees), Timothy Peterson (the PBM's account executive), Alyssa
  Fletcher (clinical pharmacist, author of the review).
- **Guard.** `guard.py recent`, `coverage`, `mechanisms --objective etl` and `slots` read before the draw; BLOCKs
  redrawn on their axes, never argued: pattern G14 to G2, shape 07 to 03, forum and forcing event off the last three
  builds, strategy decomposition_attribution to composition_mix, gap order objective first. Differentiation lines on
  the card answer task84 (a composite target key over live campaigns), task482 (one site meter's gas split by the
  physical driver each process burns by) and task65 (entities constituted from child records before a cap). The
  registered card is checked again as the draw's last act and again on the final cut (`pipeline.json` gates).
- **Candidates written before choosing** (the four set aside are in `## Tried and rejected`): (1) this draw, each
  product's rebate recovered from its manufacturer's pass-through remittances; (2) a health system's case mix across
  a grouper version change; (3) a Medicaid plan's incurred claims completed through a processing backlog; (4) a 340B
  contract pharmacy's replenishment accumulators; (5) a dialysis network's cost per treatment with shared supplies
  attributed from monthly invoices.
- **The field's method at the bottom.** The spend-weighted split of a manufacturer's rebate over its NDCs, the
  attribution a PBM rebate report uses when rebates arrive above the product, is rung 0 and files the wrong set
  (`## Default path`).
- **FINE-numbers test.** With every claim, statement line and roster row complete and correct (the clean truth,
  checks.py R3a) the split by ingredient cost still files Liraquent, insulin glargine-qmrt and Saltiva. Nothing is
  missing, withheld or planted; every remittance line is present and every statement ties to its own total.
- **Data-native sentence.** A pass-through PBM remits each manufacturer's rebates as one sum per plan account and
  quarter of service, and a manufacturer's contract terms differ by product (deep rebates where its product competes
  for a preferred tier, almost none on the sole-source specialty products that carry much of its spend), so its
  average rate misprices every product it supplies, and only the way its remittances move with each product's own
  30-day supplies across the accounts and quarters separates the terms.
- **Abstraction (the card's driver).** A total remitted for a group of items in each period and account is
  attributed to each item at the rate recovered from how the totals move with every item's own volume across periods
  and accounts, because the payer's rate differs sharply by item and a split in proportion to value moves its high
  rate on contested items onto the rest.
- **The WHAT names the quantity, never the procedure** (the coordinator's task304 lesson). Policy 3.2 files the
  rebates the product's manufacturer paid the Plan on the product's own claims; no sentence anywhere says how a
  remittance per manufacturer, account and quarter reaches a product, so joining the files leaves the estimate to
  make, and the standard route (the spend-weighted split) files a wrong set.

## Survivor anatomy

- Actor: the deciding property is each product's rebate per 30-day supply, and no file carries it: the claims carry
  ingredient cost and quantity per claim, the statements one amount per manufacturer, plan account and quarter of
  service, the drug file the labeler; the product's rebate is a relation between the statements' rows and the claims'
  account-quarter cells that nothing stores (checks.py R1b to R1d).
- Link: the claims and the statements share no product key; the link is each manufacturer's remittance in each
  account and quarter set against the 30-day supplies of every product it supplies in the same cell, a cross-file
  comparison the field's attribution never asks for (it spreads the year's total by spend), across an account key
  that changes on 1 January 2026.
- Reflex: the field's method for a product's share of a manufacturer's lump-sum rebate, the split in proportion to
  ingredient cost, sits at rung 0 and files Liraquent, Empriva, insulin glargine-qmrt, Apiqor, Saltiva and
  adalimumab-kvrn.
- Back-test: the textbook route validates: the split hands out every manufacturer's remittances to the cent, so it
  ties to the statements' lines, summary sheets and totals however they are added, and gives plausible positive net
  costs, so nothing a solver checks contradicts it.
- Second use: every file the decisive step reads is in the pack for the net cost on any route or for an ask: the
  claims (ingredient cost and 30-day supplies, the guarantee's brand claims, the members), the statements (the
  rebates on every route, the guarantee's remitted amounts), the drug file (product and labeler); deleting the
  decisive step drops no file.
- Shock: the movement the fit reads is ordinary: shares drift gently by account and quarter, no product's volume
  jumps, no remittance has an outlier quarter, and the preferred set is not an interval of any one-column sort
  (gross cost per 30-day supply ranks Velantro second, Empriva, Glarvia and Bevoria last, adalimumab-kvrn first;
  Velantro's manufacturer has the lowest average rebate share in its class).
- Pins: the WHAT is filed in the Board's own genre, policy EB-RX-04 (3.1 lowest net cost per 30-day supply; 3.2 the
  ingredient cost paid on the product's claims, before member cost sharing and without dispensing fees, less the
  rebates its manufacturer paid the Plan on those claims; 3.3 the fiscal year; 3.4 reversals; 4.1 the review's
  quantity), and Exhibit C files invoicing by quarter of service and plan account; no sentence names a fit, a basis, a
  grouping, the accounts or the quarters as the way to a product's rebate.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain:

1. Conform `pbm_paid_claims_fy2026.csv`: drop every paid claim a reversal row names in `reversal_of` (policy 3.4),
   read both platform layouts (US dates and hyphenated NDCs, ISO dates and plain NDCs), map the old group codes to the
   accounts through the statements' account names.
2. Join `pbm_drug_file_202610.xlsx` for product and labeler; take the clinical review's 30-day quantity (policy 4.1).
3. Sum each compared product's ingredient cost paid and 30-day supplies on its fiscal 2026 claims (policy 3.2).
4. Read the five `rebate_remittance_*.xlsx` statements, keep every current quarter and prior period line whose
   service period is a fiscal 2026 quarter, and match the statements' manufacturer names to the labelers.
5. Spread each manufacturer's fiscal 2026 remittances over its products in proportion to their ingredient cost, the
   attribution a PBM rebate report uses (the same set per account and quarter).
6. Divide each product's ingredient cost less its share by its 30-day supplies and prefer the lowest in each class.

- Ends on: Liraquent, Empriva, insulin glargine-qmrt, Apiqor, Saltiva and adalimumab-kvrn (Liraquent $570 against
  Dulavio $620 and Velantro $700; insulin glargine-qmrt $160 against Deglutra $190 and Glarvia $260; Saltiva $180
  against Vilaro $230 and Bevoria $310).
- Golden: Velantro, Empriva, Glarvia, Apiqor, Bevoria and adalimumab-kvrn (Velantro $510, Empriva $260, Glarvia $100,
  Apiqor $370, Bevoria $200, adalimumab-kvrn $1,190).

## Stump sentence

Spreading each manufacturer's fiscal 2026 remittances over its products by ingredient cost, as a PBM rebate report
does, files Liraquent, Empriva, insulin glargine-qmrt, Apiqor, Saltiva and adalimumab-kvrn, because Tamsford earns 49
per cent of Velantro's ingredient cost and 73 per cent of Glarvia's but 2 per cent of its oncology product's, Quorvia
53 per cent of Bevoria's and 5 per cent of its HIV product's, while Quillon pays 20 per cent on Saltiva against 47 on
Adalvane and Linmoor 20 per cent on insulin glargine-qmrt against 45 on its migraine product, so each manufacturer's
average moves its contested products' deep rebates onto its sole-source spend; solving each manufacturer's
remittances by account and quarter of service for one rebate per 30-day supply of every product it supplies files
Velantro, Glarvia and Bevoria.

## Three rules

- Task type: healthcare-delivery-health-economics / payment-claims-health-plan-analytics, which serves Data
  Extraction & Conformation (ETL): pharmacy claims and pass-through rebate remittances conformed into a product-level
  net cost comparison for a formulary decision.
- Domain test: the deciding quantity is each product's net cost per 30-day supply after manufacturer rebates, the
  formulary analyst's own figure, built from paid claims and the rebates remitted on them; the field's attribution of
  a manufacturer's lump-sum remittance to its NDCs is the split in proportion to spend.
- Swap: "prefer the supplier whose parts cost least after the volume rebate each supplier pays per plant and
  quarter" keeps the arithmetic but loses what decides it: there is no pass-through contract whose terms differ by
  product within one payer, no therapeutic class of equivalent products and no labelled 30-day supply, so nothing
  makes one payer's average rate the wrong rate for each item.
- Layer 1: the PBM's claims platform changed its export on 1 January 2026 (US dates and hyphenated NDCs before, ISO
  dates and plain NDCs after, a row in the layout of the platform that adjudicated it); reversals are their own rows
  naming the claim they reverse; the account restructure renumbered group codes, cardholder numbers and person codes
  on 1 January 2026; the statements carry prior period adjustments on the next quarter's statement and fiscal 2025
  lines on the first two; statement manufacturer names differ from the drug file's labeler names; compound claims are
  not invoiced; packages are pens, inhalers and millilitres against the review's 30-day quantity; the network file is
  the network on 1 October 2026. Each is produced by the system named and none is placed to be caught (R2a to R2k).
- Layer 2: estimation of item-level rates from aggregated remittances (per manufacturer, sixteen account-quarter
  equations in one unknown per product, which the remittances satisfy exactly): the methodological choice is to recover
  each product's rebate per 30-day supply from how its manufacturer's remittances move with every product's own
  supplies, rather than give every product its manufacturer's average.
- Decisive step: recognising that a manufacturer's remittance is a sum of product-specific contract terms, so its
  average rate belongs to none of its products, and solving each manufacturer's sixteen account-quarter remittances for
  one rebate per 30-day supply of each product it supplies, its products outside the reviewed classes included.
- Not semantics: every field read right (both layouts, the reversal pairs, the service periods, the renumbered
  accounts, the review's quantities, the cost basis) still leaves no product's rebate in any column, and with the
  clean truth's own claims and remittances the split still files the wrong three (R3a).
- Not rule application: policy 3.2 files what net cost is and no filed sentence says how a remittance per
  manufacturer, account and quarter reaches a product; executing every stated rule with the field's split files
  Liraquent, insulin glargine-qmrt and Saltiva. Enumerated family: gross cost; the split by ingredient cost, yearly or
  per account and quarter; the split by 30-day supplies; the fit on the compared products alone; the fit on every
  product (on 30-day supplies or ingredient cost, by account and quarter, quarters pooled, accounts over the year, non-
  negative): five distinct preferred sets, Velantro's net cost from $510 to $997, and the split by 30-day supplies and
  the fit on the compared products alone give negative net costs (Deglutra, Glarvia, Saltiva, Vilaro). Standing family
  once the remittances are read against every product's supplies cell by cell: every fit on every product, spread
  under 34 cents on every net cost, one set. The ruling-out is silent: the split ties to every statement total and
  summary sheet, and only a solve across the sixteen cells shows the products' own rates (largest residual under a
  cent).
- Analyst test: a strong analyst who nets the reversals, reads both layouts, maps the accounts, assigns every line to
  its quarter of service and spreads each manufacturer's remittances over its products by ingredient cost, as a PBM
  rebate report does, files Liraquent, Empriva, insulin glargine-qmrt, Apiqor, Saltiva and adalimumab-kvrn.
- Estimand: policy EB-RX-04 sections 3.1 to 3.4 and 4.1 (`pdl_policy_eb-rx-04.pdf`): each compared product's claims
  filled 1 July 2025 to 30 June 2026 net of reversals, the ingredient cost paid on them before member cost sharing and
  without dispensing fees, less the rebates its manufacturer paid the Plan on those claims, per 30-day supply as the
  clinical review lists it, the lowest in each class preferred.
- No decoy: nothing is planted: no memo, rebate report, draft or stakeholder figure states a product's rebate or
  ranks the products; the fiscal 2025 guarantee reconciliation and the April to June 2025 statement are declared
  distractors that rank nothing; no block is copied, backfilled or withheld (R3c).
- No certified replay: no certified, published or reported per-product rebate exists anywhere in the pack; the
  product rates come out of the remittances themselves and nothing is backed out of a stated figure.
- Lesson: a lump sum paid for a bundle of products is not a uniform rate on the bundle; where the payer's terms differ
  by product, the totals' movement against each product's own volume across accounts and periods identifies each
  term, and no build on file teaches a manufacturer's product rebates recovered from pass-through remittances.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Assertion |
|---|---|---|---|---|
| two export layouts (dates, NDCs) | the PBM's claims platform, changed 1 January 2026 | claims csv | a day-first date read; NDCs matched as typed | R2a, R2b (a hyphen strip maps every row; day-first fails outright) |
| reversal rows, some in the other layout | adjudication, reversals as own rows | claims csv | reversed claims left in | R2d (call holds), R2j |
| renumbered accounts and cardholders | the account restructure of 1 January 2026 | claims, statements, roster | old and new codes left apart | R2c (fit on raw codes exact) |
| prior period lines and fiscal 2025 lines | rebate invoicing (Exhibit C, C.2) | statements | current lines only; lines on their statement's quarter | R2e, R2f (call holds) |
| manufacturer names | the PBM's rebate system against the drug file | statements, drug file | exact name join | R2g (one mapping) |
| compound claims | claims adjudication (not invoiced, C.3) | claims csv | counted in the fit | R2h (exact) |
| packages against 30-day quantity | drug file and clinical review | drug file, review | days supply over 30 | R2i (call holds) |
| network snapshot | the PBM's network file of 1 October 2026 | network txt | read as every date's network | ask A device; R2k (outside the call) |
| reissued person codes | the new eligibility system | roster, claims | person code carried across | ask B device; R2k |

## Readability screen

| Rung | What the reader does | Test that could fire | Verdict |
|---|---|---|---|
| below 0 gross cost | ranks ingredient cost per 30-day supply, rebates ignored | policy 3.2 names the rebates | readable |
| 0 the split by ingredient cost (default) | spreads each manufacturer's fiscal 2026 remittances over its products by spend | the field's reflex, a rebate report's attribution | readable |
| 0b the split per account and quarter | the same split cell by cell | the reflex refined | readable |
| 1 the split by 30-day supplies | spreads by units | negative net costs for three products show it wrong | readable |
| 2 the fit on the compared products alone | solves the cells for the reviewed products only | needs the fit first; the manufacturers' other products leave residuals and negative net costs | silent |
| 3 the fit on every product (decisive) | solves each manufacturer's sixteen account-quarter remittances for a rate per 30-day supply of every product it supplies | no column, key or sentence holds a product rebate; the split ties to every total | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the fiscal year | 1 July 2025 to 30 June 2026 | calendar 2025, fiscal 2027 | not computable from the pack | policy 3.3 (latest fiscal year with four quarters' remittances; the April to June 2026 statement remitted 18 September 2026) |
| SF2 | claims filled in the year | date of service | date paid | same call, every band | same call |
| SF3 | a reversed claim | dropped with its reversal | reversal rows read as negatives | same call, same figures | same call (netting is the same arithmetic) |
| SF4 | ingredient cost paid | `ingredient_cost_paid` | with dispensing fees; plan paid after cost sharing | same call; fees keep every band, plan paid moves every band | policy 3.2 (before member cost sharing, without dispensing fees) |
| SF5 | the rebates paid on those claims | every line whose service period is a fiscal 2026 quarter | current lines only; lines on their statement's quarter | same call | policy 3.2 ("on those claims") and Exhibit C, C.2 (prior period lines belong to their quarter of service) |
| SF6 | a 30-day supply | quantity over the review's 30-day quantity | days supply over 30 | same call | policy 4.1 |
| SF7 | the products compared | the review's Table 1 | every product of the class on the claims | same call (no other) | policy 2.1 |
| SF8 | the product's manufacturer | the drug file's labeler | a statement name read separately | same call (one mapping) | same call |
| SF9 | the list's population | the whole Plan | per employer account | same call (every account prefers the same products) | same call; policy 1 (one list for the Plan) |
| SF10 | rounding | net cost to the nearest ten dollars, once | truncation | same call | "nearest" in the prompt; every value 4 dollars inside its band |
| SF11 | the year's net cost | ratio of the year's totals | mean of the quarters | same call, every band | same call |
| SF12 | compound claims | outside every compared product | counted | same call | same call (none in a reviewed class) |
| SF13 | partial supplies | none arise | prorated | same call | same call (every compared claim dispenses whole supplies) |
| SF14 | tie-break | none needed | any | same call | same call (nearest runner-up 49 dollars above) |

## Ladder

| Rung | Construction | GLP-1 | SGLT2 | Long-acting insulin | DOAC | ICS/LABA | Adalimumab |
|---|---|---|---|---|---|---|---|
| below 0 | gross ingredient cost per 30-day supply | Dulavio | Canivo | insulin glargine-qmrt | Ravelta | Saltiva | adalimumab-kvrn |
| 0 (default) | split by ingredient cost, yearly or by cell | Liraquent | Empriva | insulin glargine-qmrt | Apiqor | Saltiva | adalimumab-kvrn |
| 1 | split by 30-day supplies | Liraquent | Empriva | Deglutra | Apiqor | Saltiva | adalimumab-kvrn |
| 2 | fit on the compared products alone | Velantro | Canivo | Glarvia | Apiqor | Vilaro | adalimumab-kvrn |
| 3 (decisive) | fit on every product of each manufacturer | Velantro | Empriva | Glarvia | Apiqor | Bevoria | adalimumab-kvrn |

Margins: the golden's runner-up over the preferred product is 1.17x to 2.57x (Velantro $511 against Liraquent $599
the nearest); the default's three wrong picks lead by 1.09x, 1.23x and 1.27x. Every member of the golden family
(30-day supplies or ingredient cost, by account and quarter, quarters pooled, accounts over the year, non-negative,
raw group codes, date paid, compounds in) prints every net cost in its golden band (checks.py). Two non-compliant
readings keep the call and move at most one band each: current lines only (none) and every line on its statement's
quarter (Adalvane).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the product's claims filled in fiscal 2026, net of reversals | filed (policy 3.2, 3.4); C1 on date paid (SF2) |
| 2 | Unit of account | the product, per 30-day supply | filed (policy 3.1, 4.1) |
| 3 | Attribution window | date of service; remittance lines by service period | filed (3.2, Exhibit C C.2); C1 (SF2, SF5) |
| 4 | As-of dating | the latest fiscal year with all four quarters' remittances; the guarantee's channel on the date of service | filed (3.3; Exhibit C C.5) |
| 5 | Version basis | the final clinical review of 12 October 2026; the October 2026 drug file | the review is the only version shipped; C1 |
| 6 | Denominator | 30-day supplies from the review's quantity | filed (4.1); C1 on days supply (SF6, call) |
| 7 | Weighting | ratio of the year's totals | filed (3.2); C1 against the quarters' mean (SF11) |
| 8 | Window length | one fiscal year | filed (3.3) |
| 9 | Boundary inclusivity | 1 July 2025 and 30 June 2026 inclusive | C1 (no claim outside, SF1) |
| 10 | Rounding path | unrounded net cost, rounded once to ten dollars | asserted (every value 4 dollars inside its band) |
| 11 | Tie-break | none | C1 (nearest gap 49 dollars, SF14) |
| 12 | Maturity and censoring | every fiscal 2026 quarter's remittances received | filed (3.3); asserted (no April to June 2026 claim paid or reversed after the 14 August cut-off) |
| 13 | Order of operations | reversals out, rebates attributed, then divided | filed order (3.2, 3.4); C1 |
| 14 | Row order | sums only | C1 |
| 15 | Duplicate resolution | a reversal nets the claim it names | the claim-number link (R2j); C1 |
| 16 | Identity normalisation | NDC layouts, manufacturer names, account codes | the systems' own keys (R2a, R2g, R2c) |
| 17 | Netting against gross | prior period lines net into their quarter of service | filed (Exhibit C C.2, C.4) |
| 18 | Dimensional units | each, mL and g against the review's quantity | units in the data (drug file, review) |
| 19 | Code and status semantics | claim status, compound code, line type | read from their own files; none decides the call (R2) |
| 20 | Integerisation | whole 30-day supplies on every compared claim | C1 by construction (SF13) |
| 21 | Clause scope | 3.2's rebates are the product's own; C.4's shortfall is per quarter | filed |
| 22 | Forward window contents | none: the 2027 list rests on fiscal 2026 by policy | filed (3.3) |

## Literal reader

Executed word for word, policy 3.2 asks for the rebates the product's manufacturer paid the Plan on the product's own
claims; the statements give each manufacturer's rebates per plan account and quarter of service, so the literal
quantity is the part of those amounts the product's own claims earned. The split by ingredient cost gives each product
its manufacturer's average rate, which the cells show none of them earns (non-compliant on the literal reading); the
fit returns each product's own rebate exactly. Every other term is closed in the fork table: each alternative either
violates a quoted sentence or prints the same call and every band (SF1 to SF14, asserted). The asks read literally:
Exhibit C C.5's "the network of the dispensing pharmacy on the date of service" against a network file dated
1 October 2026, the claims' own dispensing fees dating the three pharmacies' move to 1 May 2026; "members" are the
roster's persons, a reversed claim not counting as paid (the prompt).

## Oracles

- The statements' summary sheets and totals tie to their lines; they confirm any attribution that keeps each
  manufacturer's total (the split and the fit alike) and arbitrate nothing.
- The fiscal 2025 guarantee reconciliation (a declared distractor) answers another year's guarantee and ranks no
  product.
- No per-product rebate, net price or ranking exists in any file (R1b, R1c, R3c); the fit's zero residual is the
  data's own structure, seen only by a reader who runs the solve.

## Ask sheet

The asks sit on the guarantee check and the members, quantities the net cost route never computes (no channel and no
person identity enters it, R2k). Ask A: for each fiscal 2026 quarter, Exhibit C's brand claims by channel, the
guaranteed amount, the rebates remitted for that quarter's claims and the shortfall owed (28 figures). Ask B: the
members with a paid fiscal 2026 claim in each reviewed class under each employer account (24 figures). Ask A is the
audit trail of the rebate input the call consumes; ask B is the clinical review's members affected (its section 3).

- Pair ceiling: 43.3 (cracker 59.8 on the call with 14 of 52 ask criteria, mirror 26.8 with 14 of 52).
- Mirror leakage: 26.9 per cent of the ask weight (target two fifths; nothing in the asks comes from the call).
- Measured by: generator/ceiling.py on the cut pack.

| Ask | Primary device | Hazards | Cracker's handling | Cracker |
|---|---|---|---|---|
| Ask A guarantee check by quarter | the network file is the network on 1 October 2026; three hospital outpatient pharmacies it lists as specialty billed on retail terms (the retail dispensing fee) until 1 May 2026, so their earlier claims are retail on their date of service (D2, a label stored before a silent switch) | prior period lines on the next statement, fiscal 2025 lines on the first two, compound claims, the 84-day split | reads the network file as every date's network, lines by service quarter (keeps the mail counts and remitted amounts, 8 of 28) | miss |
| Ask B members by class and account | person codes reissued at the 1 January 2026 renumbering (spouse 02 and children by birth date, where the old system numbered in enrolment order), the roster linking only subscribers to their old cardholder number (D7, codes reissued to other entities) | old and new account codes, two date layouts, a reversed claim not counting | links the subscriber's old number and carries the claim's person code (keeps the retirees' cells, 6 of 24) | miss |

The full includer (each claim's network from its own adjudication, dependants matched on birth date and gender within
the family) keeps all 52 (stress row). Zero device rows sit in the main call's population: the net costs read no
channel and no identity (R2k). Golden: a shortfall in April to June 2026 alone ($50,151); the network file read as
every date's network puts one in all four quarters. Ask B: the carried person code misses 18 of 24 cells and the
unlinked count all 24 (checks.py).

## Leak review

`leak.py --asof 2026-10-19` on the final cut: see `leak_check_report.md`; every REVIEW line is answered here.

## Architecture 4 record (re-rooted 2026-11-01)

Zip c11307e9d8a0592f19e47aa823a6c293, shipped 2026-10-26: an island Statistics Unit's provisional long-term
immigration for the year to 30 June 2026 by employment sector, each stay still open at the 31 August cut completed on
the earlier arrivals with the same migration history, so the returning circular workers (whose previous stay under the
same registration number ended in the year before they arrived) were not counted at the first-timers' retention.
Gates at ship: precut 51 checks with no FAIL or WARN, pair ceiling 29.2 and mirror leakage 1.2 by ceiling.py, leak.py
REVIEW with no LEAK, guard heart WARN, surface five promotions answered on the card. Stage 4 round 1 (zip 86b54856):
both readers missed the call and kept the back series 40 of 40, re-sited; round 2 (zip 56904a09): readers C and D
missed the call and kept 1 of 80 ask figures each; the judge returned DETERMINISTIC and APPROVE. No portal result had
arrived when the Batch 3 queue reset re-rooted it; the island migration world closes with it (one architecture per
world), and its reports are kept as `determinism_check_report_arch4.md` and `leak_check_report_arch4.md`.

## Architecture 3 record (spent 2026-10-25)

Zip 9263b80dcd8ccb1c8722ce81d63f66d3 (checks.py 77 PASS, verify.py 48 of 48, byte-identical rebuilds, precut 51 checks
with no FAIL, pair ceiling 30.2 by ceiling.py, leak.py REVIEW with no LEAK, guard heart WARN, surface exit 0, the H21
rename of 33 invented names). Round 1: both scored readers (sonnet, medium, fresh copies) read the guidance's section 3.1
("less the sulphur dioxide its abatement plant removed over the year"), set the design and the one-day test removals
aside as not covering the year, and took each scrubber's removal from the limestone balance: the 2026 tickets plus the
first quarter's opening less the fourth quarter's closing silo stock, each ticket at its ISO week's certificate as
delivered, over the guarantee schedule's stoichiometry at 64.066 grams a mole. Both landed the golden six with all 18
boilers' tonnes and listings (score_reader FAIL on both); ask A held at 1 of 32 on both (the one coincidental share),
both counting Whinmoss's lines that bill a local contractor's collection beside the local's own record. Both called the
step an analytical choice nothing in the pack states and named "over the year" as the words that set the test aside.
The judge thread was stopped at the spend. Lesson: a reagent consumed in a fixed ratio to what the device removes,
recorded for the whole year beside a governing sentence that measures the year, is the careful analyst's first route to
the removal, not a step past a finished-looking default; the one-day test reads as a snapshot against the year, and the
silo stocks, the weekly certificates and the stoichiometry column lay the balance out. This draw's own screen had set
AdBlue dosing aside for the same reason (a fleet's reagent sits beside its fuel and reads at once); a stationary
scrubber's reagent sits beside its coal the same way. The readers' realism notes: load weights in narrow bands (coal 27.5
to 32 tonnes, limestone 26.0 to 29.6), one analysis shared by every truck of a certificate, weekly carbonate in a narrow
band, the tests evenly spaced, and Whinmoss's repeated 26.0 tonne lines (the device's standard loads, noticed and not
acted on).

## Architecture 2 record (spent 2026-10-25)

Zip 37f7e1986e84036128ca2496b64197b3 (checks.py 61 PASS, verify.py 66 of 66, byte-identical rebuilds, precut 51 checks
with no FAIL, pair ceiling 28.5 by ceiling.py, leak.py REVIEW with no LEAK, guard heart WARN, surface four promotions
answered on the card). Round 1: both scored readers (sonnet, medium, fresh copies) went straight to the bovine register,
rebuilt every animal's days by herd from HERD_AT_START and the arrival dates, charged Table 3's housed rate inside the
housing season of the region the animal was in and the grass rate outside it, and landed the golden six with every
regional tonnage (kilograms a hectare a hundredth off on three regions); both named the census at Table 5 as the easy
route that files a different list and set it aside. score_reader exited FAIL on both; ask A held at 0 of 24 on both
(the Countrywide lines that bill a local contractor's job counted twice). Reader B called the decisive step closer to
rule application than to an analytical choice, because the factor note's Table 3 caption and Table 4 and the rules'
sections 3 to 5 spell the construction out. The judge thread was stopped at the spend. Lesson: where the record covers
every unit for the whole window at the grain the estimand names, and the governing documents state per-day rates by
place and season, building the estimand from the record is the careful analyst's first move rather than a step past a
finished-looking default; the census at the annual factor was a lazy rung no reader took. Reader B also noted two
generator tells to fix in any reuse of this world: exit dates running past the extract date (to 23 November 2026) and
registration lags uniform on 1 to 27 days.

## Architecture 1 record (spent 2026-10-25)

Zip 237917da9ecb5387a7250b4fde842cf2 (checks.py 58 PASS, verify.py 10 of 10, precut 51 checks with no FAIL, pair
ceiling 28.5, leak.py REVIEW with no LEAK, guard heart WARN). Round 1: both scored readers (sonnet, medium, fresh
copies) landed the call, the golden five, and score_reader exited 1 on both (asks 6 and 2 of 25). Reader A held the
settled stock flat and fitted the share of the settled level a new dwelling holds to its age since completion on the
2022 to 2025 registers (about 0.08 in its first quarter, 0.45 at a year, 0.80 at two and a half years, 1.0 from about
six), applied it to every completion since April 2014 and every trajectory dwelling, and filed Kettermere +16.1,
Quenbrook +14.8, Caldenstow Park +13.9, Lorrimere West +13.2 and Ebborby -13.4. Reader B built the same
electors-per-dwelling curve by age and type and filed the same five. Both named the step an analytical choice nothing
in the pack states. Both also found ask A's device: the 2021 report's run date (4 March 2022) and the notices beside it
told them the report held the January to March 2022 alterations, and both backed them out, missing the golden on
handling only (reader A 4 of 23 wards exact; reader B also removed additions it took to be under 18). The judge thread
(v1r1) returned DETERMINISTIC and APPROVE (Gate G forecasting and etl_conformance, analytical_non_defect; Gate H domain
and layers pass, decisive step analytical); it was not taken to a report, the call being spent. The readers' realism
notes: the settled stock barely moves from 2020 to 2025, the ramp is a near-exact exponential alike in every ward and
type, the trajectory's site sizes are round, and no register row lacks a UPRN.

## Tried and rejected`. The slot's seed (ET42) was set aside at the
first draw and stays set aside.
- 2026-11-01, architecture 4 (each open stay completed on earlier arrivals with the same migration history), re-rooted
  at the Batch 3 queue reset with no portal result: shipped 2026-10-26, its world closes with it and survey-research-
  official-statistics carries several builds in flight, so architecture 5 moves to healthcare-delivery-health-economics.
- 2026-11-01, architecture 5 draw, set aside beside the rebate attribution: a health system's case mix across a grouper
  version change (regrouping executes the grouper's logic, rule application); a Medicaid plan's incurred claims
  completed through a processing backlog (the chain ladder is the field's reflex, a backlog-adjusted triangle forks,
  and completion draws are spent in this lane); a 340B contract pharmacy's replenishment accumulators (executing the
  accumulator rules is rule application, and an accumulator gap reads as planted); a dialysis network's cost per
  treatment with shared supplies attributed from monthly invoices (the same co-movement family without a contract
  whose terms differ by item, and task482's meter split sits on it).
- 2026-11-01, architecture 5 draw: guard BLOCKs from sibling registrations redrawn on their axes, never argued
  (pattern G14 to G2, shape 07 to 03, forum and forcing event off the last three builds, strategy
  decomposition_attribution to composition_mix, gap order objective first); the old prompt deleted so the shell's
  lineage reads the new build only.
- 2026-11-01, architecture 5 stage 3: 340B covered entities among the pharmacies (their claims rebate-ineligible) set
  aside: their concentration in one class let a filed exclusion decide the inhaler class, a rule carrying part of the
  call; every pharmacy is now rebate-eligible.
- 2026-11-01, architecture 5 stage 3: late adjudications at 0.16 per cent of claims paid and 0.15 per cent reversed
  after the invoice cut-off moved the non-compliant readings (current lines only, lines on their statement's quarter)
  two ten-dollar bands on the small adalimumab products and an account mix with flat profiles left the fit poorly
  conditioned; late events thinned to 0.06 per cent each, account and quarter profiles sharpened, one brand discount
  per product so the cost-basis fit agrees; the honest family is exact and the non-compliant readings keep the call.
- 2026-11-02, architecture 5 stage 3: statement lines carrying the statement's own account code (SEB codes on prior
  period lines for 2025 service) made the fit on raw codes lose those lines and move two bands; each line now carries
  the group code its claims were billed under, as a PBM invoice does, and the raw-code fit is exact.
- 2026-11-02, architecture 5 stage 3: the PBM's network change notice (a letter naming the three hospital outpatient
  pharmacies and the date they joined the specialty network) set aside: a careful solver applies a filed change notice,
  so the guarantee ask's device was a work order the cracker kept; the notice is out of the pack, the move is dated
  1 May 2026 so every quarter carries it, and the claims' own retail dispensing fees date it.
- 2026-11-02, architecture 5 stage 3: membership events drawn per person (a subscriber leaving while the dependants
  stayed) left 193 dependants unlinkable through any subscriber row, and same-sex twins made birth date and gender
  ambiguous in six families; events are now family-level and no family repeats a birth date and gender (checks.py).
- 2026-11-02, architecture 5 stage 3: a quarter's remitted rebates landed on a half dollar (3,469,210.50), a rounding
  tie under "to the nearest dollar"; the tail product Zolvera's rebate share (outside every reviewed class) steps a
  tenth of a point until no quarter sits within five cents of a half dollar; no graded net cost moves.
- 2026-11-02, architecture 5 stage 3: H21 renames: Arvelle (a real company), Ombrel (two letters from Ombrelle),
  Vantrel (one from Vantrela), Fenwick (a real retailer and law firm), Dulmira (two from Dulera), Brezara (two from
  Breztri), Virelda (two from Viread), Sumivex (two from Sumavel), and the St. Brigid and Mercy Ridge pharmacies (real
  institutions) renamed; an "ozanimod-like" nonproprietary name corrected; every figure unchanged.
- 2026-11-02, architecture 5 stage 3: the claims export wrote two date layouts inside one row (service date in the old
  layout, paid date in the new); each row now takes the layout of the platform that adjudicated it.
- 2026-11-02, architecture 5 prompt: the shell opened on "which" and its second sentence on "put", both over the
  corpus quotas; reworded to a "what" question and a "set out" sentence, every term and rounding unchanged.
