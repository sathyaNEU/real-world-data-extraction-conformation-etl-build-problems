# task211: Larkhaven Health, which levetiracetam tablet goes to the laboratory re-test

Architecture 2, drawn and registered 2026-11-04 as a re-root of architecture 1 (Nordvig Marine's jack-up for five North
Sea sites, spent at stage 4 on Gate H: a withheld operating practice). One architecture per world: the offshore world,
its dataset and its prompt shell are left behind; nothing is kept from seed AD34 but the number and the objective.

## Draw

**Card.** `cards/task211.json`, architecture v2, registered 2026-11-04T16:56:55Z, architecture 1's identity in `lineage`
with its fate and its prompt shell (how-many, build, pptx+xlsx) in `lineage_shells`. Pairing
`pharmacology-pharmacoepidemiology-safety` / `safety-signal-detection` / Anomaly Detection & Diagnostics (the task type
serves AD only). Shape `other`, decision `pick_one_of_n` (or none, on a filed bar), answer unit `named_option`. Gap
population then objective, pattern none with G4 (attribution at transition) then G3 (record against operation) and G13,
Gate G `decomposition_attribution`, strategy `causal_design`, Layer 2 family `estimand_identification`, pattern
`own:tablet-appearance-change-transient-against-persistent-product-effect`, calibration none, context artifact
`monitoring_export`. Forum `committee_or_panel` (the pharmacy and therapeutics committee's formulary quality group),
forcing event `purchase_order_or_contract` (the contract laboratory's third-quarter slot is booked by purchase order),
org family `hospital_or_health_provider`, role `other` (director of pharmacy quality and formulary). Personas from
`guard.py names --geo "United States, Oregon" --seed 211`: Annette Yang, Mariah Guerrero, Lauren Byrd (Megan Cooper drawn
first and replaced: people.first WARN against task273). The as-of date of the fiction is 20 July 2026.

**Guard.** `check` on the draft and on the registered card: WARN, exit 0. Answered:
- `repeat.gate_g` and `overuse.gate_g` (decomposition_attribution, task401 and 6 of 12): the stump is an excess split
  between two causes, a response each patient carries after a change in what their tablet looks like and the product's
  persistent effect, which is the key's own definition; `method_or_model_selection` was probed and is the less honest
  label (no rival estimator is chosen between, a cause is removed).
- `repeat.question_form` (which, task401): the decision picks one product or none, so the form is whether and which;
  the shell is redrawn at the role level (second-sentence opener and deliverable set).
- Furniture redrawn against the live window: context artifact `register` (ban.artifact, task401) to
  `monitoring_export`; the structural triple (objective, G4, decomposition_attribution) repeats task398 inside the batch
  and (population, G3, decomposition_attribution) task399's lineage, so population leads with G4, and the older repeats
  (task121 v6, task129 v2, task232 v2, task243) carry differentiation lines on the card, with task162 v1 too.
- Nearest driver 0.07 (task98 v4 lineage); every other driver on file 0.07 or under.

**World.** Larkhaven Health, a fictional integrated health system in Oregon and southwest Washington with its own
pharmacies (620 of them in the pack) supplied from seven distribution centres. 60,000 members take levetiracetam
500 mg tablets. Six products are interchangeable on the formulary: Levaril (the reference brand), Corwen (its authorised
generic, identical blue tablets until Corwen's film coat turned beige on 1 September 2025), Halvorne Generics and
Pellbrook Pharmaceuticals (identical white oval tablets debossed M5, made by Marrowby Pharma Services), and Tessard
Laboratories and Wynfield Pharma (identical orange tablets made by Brennick Contract Manufacturing). Pharmacies dispense
the generic their supply contract names and move to its look-alike partner when it is out of stock. Halvorne moved
manufacture to its own site at Fort Wayne (approved 15 September 2025); the new tablets are pink, debossed H 500, and the
new stock reached each distribution centre and its pharmacies on a dated table in Halvorne's letter, from 1 December 2025
to 18 May 2026. Pellbrook was on wholesaler backorder from 2 February to 4 May 2026 (its pharmacies moved to Halvorne),
Tessard from 27 February to 10 April 2026 (to Wynfield).

**Decision.** In July 2026 the committee books one product into the contract laboratory's third-quarter assay and
dissolution re-test, or none. Which product goes, and how many seizure-related emergency visits per 1,000 patient-months
does it add over what the same patients would have had on tablets releasing levetiracetam as Levaril does? Retrospective
window, forward decision: the re-test examines the tablets now in supply, and the excess the tablets carry persists.

**The WHAT, filed in MS-12 (`ms12_interchangeable_product_surveillance.pdf`), no sentence naming a clock, a change, a
colour, a first fill, a distribution centre or adherence.** 2.1 the products, 2.2 the window (the prompt names January to
June 2026), 2.3 the outcome (first-listed G40 or R56.9, a transfer counted once, Pacific dating), 2.4 patients, fills,
supply and overlap, 30.4375 days a patient-month, 2.5 attribution by the covering supply, 2.6 the excess (the product's
patients' visits less what the same patients over the same days of supply would have had if the tablets released and
delivered the drug as the reference's do, per 1,000 patient-months), 3.1 the selection (the largest excess at 2.0 or
more, else none, the slot released), 3.2 the referral states the product and its excess.

**Data-native sentence.** The dispensing record names the product each fill supplied, but what a patient was handed, the
tablet's colour and marking, is set by which site made it and which distribution centre served the pharmacy on the
fill's date, and appears only in the product register's dated descriptions and the two manufacturers' letters; each
patient's first supply of a differently looking tablet carries an excess of seizure visits for as long as that supply
lasts, so Halvorne's rolling change, Pellbrook's backorder and every stock-out book an excess to products whose tablets
cause none.

**Abstraction sentence (against the nearest approved builds).** Against task196 (a second capture channel produced by
chasing the first) and task182 (each unit's own lagged driver response): here an excess is split between a response each
member carries through their own first supply of a changed version of the item, dated by the supply point that served
them, and the candidate's persistent effect; the driver with the nouns stripped is on the card.

**Sources.** Every file synthetic, generated from one seed (5007), invented organisations and people, CC BY 4.0,
recorded in `metadata.json`: the dispensing claims extract (parquet, 551,845 claim lines, April 2025 to June 2026,
across a claims-platform cut-over on 6 October 2025), emergency encounters from two hospital feeds (Larkhaven's CSV in
Pacific local time, the partner hospitals' JSON in UTC, both from 1 December 2025), the member file and the record-number
crosswalk, the pharmacy register (pharmacy to distribution centre), the product register's dated descriptions, the two
manufacturers' letters (PDF), MS-12 (PDF), the purchasing manual and wholesaler service schedule extract (PDF), the
wholesaler's invoice lines, backorder notices, item list, ship-to accounts and advance ship notices, the centres'
receiving log, the pack register, and three distractors named only in `metadata.json` (the laboratory's quotation, the
list prices, the supply monitor).

### The five go/no-go screens (real generator, 20 redraws, seeds 5000 to 5019; `t211/a2/seedscreen.py`, `screen_stats.json`)

The clean truth: each patient-day carries a base seizure-visit rate (age band and drug-resistant epilepsy), Tessard's
persistent effect (rate ratio 1.15 since July 2025) and, through the whole of each patient's first supply of a tablet that
looks different from their previous fill, a rate ratio of 2.5 (30 or 90 days, as dispensed); a move between look-alike
tablets carries none.

1. **Realistic levels and the lever against the rivals' estimates.** Levels, each cited: colour discordance at a refill
   raises the odds of stopping an antiepileptic 53 per cent (Kesselheim et al., JAMA Internal Medicine 2013;173:202-208),
   and generic cardiovascular drugs show the same (Kesselheim et al., Annals of Internal Medicine 2014;161:96-103); a
   formulation switch before a seizure-related ambulance, emergency or inpatient event carries an odds ratio of 1.81, 95
   per cent CI 1.25 to 2.62 (Zachry et al., Epilepsia 2009;50:493-500), the 2.5 here set near its upper bound for the
   supply in hand; nonadherence to antiepileptics raises emergency visits, admissions and mortality (Faught et al.,
   Neurology 2008;71:1572-1578); about a third of treated patients are not seizure free (Kwan and Brodie, NEJM
   2000;342:314-319), world-set as 22 per cent at 2.5 times the base; the reference's rate, 31.3 qualifying visits
   per 1,000 patient-months at the shipped seed, sits in the range treated epilepsy cohorts show in US claims (Faught
   2008; Zachry 2009). Tessard's 1.15 is world-set, the size a product at the low end of the bioequivalence window can
   carry; marketed generics found not to perform as the brand have precedents (FDA's 2012 withdrawal of Budeprion XL
   300 mg; FDA's 2014 reclassification of two methylphenidate extended-release generics from AB to BX). The lever: the
   golden names Tessard at 2.0 or more in 19 of 20 redraws (at 3.0 or more in 18), its lead over the
   runner-up at least 1.2 in 20 of 20 (lowest 1.33); the first look names Halvorne in
   20 of 20, ahead of Tessard by at least 6.8 visits per 1,000 patient-months (median Halvorne
   15.6 against Tessard 6.3). Every graded figure mid-bin at the shipped seed and the pack at 12.8 MB
   are asserted in `generator/checks.py`.
2. **The golden's own method holds the call at the shipped seed.** The first supply read on the whole description and on
   colour alone, with calendar month and centre added, split by its days of supply, the 90 and 120-day clocks after the
   change and fourteen-day bins to 182 days all name Tessard, from 3.76 to 4.28, one whole-visit bin (4),
   the tightest 0.22 from an edge, the lowest lead 1.41. Over the redraws: first supply after an appearance change, Tessard in 20; first supply after a colour change (narrow reading), Tessard in 20; first supply with month and centre, Tessard in 20; first supply split by its days of supply, Tessard in 20; days since the appearance change, 90-day clock, Tessard in 20; days since the appearance change, 120-day clock, Tessard in 20; days since the appearance change, fourteen-day bins, Tessard in 20. The 30, 60 and
   180-day clocks are refuted by the record against the first supply (log-likelihood gains of at least 250 on one
   partition over the redraws) and none is ruled out under each of them at the shipped seed (largest excess 30-day clock Halvorne 9.3, 60-day clock Halvorne 5.5, 180-day clock Pellbrook 3.4).
3. **The first look lands wrong**: 20 of 20 (crude rates against the reference name Halvorne).
4. **The careful readers land wrong** (20 redraws each): first look (crude rate against the reference), 20 of 20 wrong (Halvorne 20; margin over Tessard at least 6.8, median 9.0); (a) field-decomposing: age, resistance and centre standardised, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 6.9, median 9.2); (b) constructing: first 90 days on a product excluded, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 6.6, median 8.0); (b) constructing: 90 days after a change of product excluded, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 6.0, median 7.8); (c) per-record: product, month, centre, age, resistance, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 6.5, median 8.8); (d) switching: a transient after a change of product, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 7.0, median 9.2); (d) new site: the new site's stock as the cause, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 6.7, median 9.1); (d) colour dated by the register's approval date, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 1.3, median 3.2); (d) colour from the letter, dated by its centre date, 90 days, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 3.7, median 6.0); (d) colour from the letter, dated by its centre date, 180 days, 20 of 20 wrong (Pellbrook 12, Corwen 8; margin over Tessard at least 0.9, median 3.1); (d) switching and the letter date together, 20 of 20 wrong (Halvorne 18, Corwen 2; margin over Tessard at least 3.7, median 5.8); (e) literal joint replay: standardised excess against the reference, 20 of 20 wrong (Halvorne 20; margin over Tessard at least 6.7, median 9.1); temporal: the last two months' standardised rates, 20 of 20 wrong (Pellbrook 20; margin over Tessard at least 14.5, median 19.1).
5. **Literal execution** of the filed WHAT (each product's standardised excess against the reference: Halvorne 15.6, Pellbrook 10.8, Corwen 7.4, Tessard 5.7, Wynfield 0.8)
   lands Halvorne; the golden needs the patients' response to what they were handed estimated from the record, which no
   filed sentence names and no practice supplies.

## Default path

1. Take the paid claims in `dispensing_claims_2025-04_to_2026-06.parquet` net of reversals, map the legacy NDC-11 codes
   and the new platform's item codes through `claims_item_crosswalk.csv`, and run each member's supply under MS-12 2.4.
2. Date qualifying visits from both hospital feeds in Pacific time, count a transfer once on its first arrival and link
   merged records through `mrn_member_crosswalk.csv` (MS-12 2.3); attribute each visit to the product covering its day
   (2.5).
3. The field's method for the deciding quantity: each generic's qualifying visits per patient-month against Levaril's,
   adjusted for age band and drug-resistant epilepsy (a Poisson model with product terms, indirect standardisation on
   these strata), per 1,000 patient-months.
4. The pharmacoepidemiology reflex for interchangeable generics: allow for switching, a transient term after each change
   of product, or the 90 days after a change of product left out.
5. The largest excess per 1,000 patient-months, above MS-12's 2.0 bar, names the product.

Ends on: Halvorne, 11.2 excess visits per 1,000 patient-months.
Golden: Tessard, 4 excess visits per 1,000 patient-months.

## Stump sentence

A competent analyst nets the reversals, links both hospital feeds, adjusts each generic's qualifying visits per 1,000
patient-months against Levaril's for age and drug-resistant epilepsy, allows for changes of product and names Halvorne at
11.2 excess visits; the step that lands them there is reading the excess per product, when Halvorne's excess is the
first supply of its new pink tablets, filled as the Fort Wayne stock reached each distribution centre in turn, and with
every patient's first supply of a differently looking tablet held as it was, the excess the tablets themselves carry is
Tessard's, 4.

## Three rules

Task type: pharmacology-pharmacoepidemiology-safety / safety-signal-detection, which serves Anomaly Detection & Diagnostics (a product-level excess in active surveillance separated into what the product causes and what the dispensing around it causes).
Domain test: the deciding quantity is each interchangeable product's excess of seizure-related emergency visits over what its own patients, on the same days, would have had on tablets releasing like the reference, estimated the way post-market pharmacoepidemiology estimates a generic's performance from dispensing and encounter records (a rate model on patient-days of supply with the product as exposure).
Swap: "which supplier's part goes to the lab once the warranty claims that follow each customer's first box of a part that looks different are held as they were": no part's colour makes a customer skip using it and no breakthrough event follows, so the sentence stops making sense; the mechanism is missed doses of an antiepileptic during the first supply of an unfamiliar tablet.
Layer 1: the claims platform cut-over (NDC-11 before 6 October 2025, item codes after), reversals and resubmissions, two hospital feeds in two clocks (Pacific local and UTC) and two formats, inter-facility transfers recorded twice, merged medical record numbers, free-text register descriptions, a manufacturer's letter as a PDF table; each produced by the system that made it, none deciding the call (asserted per item, R2).
Layer 2: estimand_identification; the comparison MS-12 2.6 files holds each patient's days of supply as they were, so the excess that follows a patient's own first supply of a differently looking tablet is part of what the same patients would have had, not part of the tablet's effect; reading the excess per product books it to the products whose patients changed tablets.
Decisive step: recognise that the excess sits in each patient's first supply after a change of what the tablet looks like, rebuild that supply patient by patient from the register's dated descriptions, the manufacturers' dates by distribution centre, the pharmacy's centre and the patient's previous fill, and hold it as it was when the product term is set to the reference.
Not semantics: every field read correctly (the codes mapped, the clocks converted, the transfers counted once, the register's descriptions and the letters' dates read) still leaves the per-product excess on Halvorne, because no field states which fills changed what a patient was handed and no code marks a first supply; the reconstruction across four files and each patient's own sequence is analysis, not reading.
Not rule application: no filed rule computes a first supply or names appearance, and executing MS-12's stated facts (the adjusted excess against the reference) files Halvorne at 11.2; the enumerated family a competent analyst reaches for spreads from Halvorne 11.2 through Pellbrook and Corwen on the letter-date calendars to Tessard on the first supply, the standing family (the first supply on either reading, with month and centre, split by days of supply, the 90 and 120-day clocks, fourteen-day bins) spreads Tessard 3.76 to 4.28, one whole visit, and the ruling-out is the record's own fit: the first supply beats the site clock by 484, the switch clock by 673 and every fixed clock by at least 290 in log-likelihood on one partition.
Analyst test: a strong analyst who nets the reversals, links both hospital feeds, adjusts each generic's qualifying visits against Levaril's for age and drug-resistant epilepsy and allows for changes of product names Halvorne at 11.2 excess visits per 1,000 patient-months, when Halvorne's excess is the first supply of its new pink tablets and the excess that persists is Tessard's, 4.
Estimand: MS-12 2.6 (ms12_interchangeable_product_surveillance.pdf): a product's patients' qualifying visits in the window less the visits the same patients, over the same days of supply, would have had if the product's tablets released and delivered the drug as the reference product's do, per 1,000 patient-months; the window (January to June 2026) is the prompt's, the selection and the 2.0 bar MS-12 3.1.
No decoy: nothing is planted: Halvorne's site transfer, its letter and its pink tablets are an ordinary supply change, the Pellbrook and Tessard backorders ordinary shortages, Corwen's coat change an ordinary formulation change; no memo, dashboard or stakeholder figure ranks the products, and the supply monitor holds dispensing by centre and month for all products together.
No certified replay: no certified or published figure is reproduced to recover a method; the excess is estimated from the patient-days themselves and nothing in the pack states any product's excess.
Lesson: a generic's excess in post-market surveillance can be the patients' response to what their tablets look like rather than to what is in them; the response follows each patient's own first supply of the new look, dated by the supply chain that served them, and a change of manufacturer, a site or a calendar window is the wrong clock.

## Survivor anatomy

Actor: the deciding property, whether a patient-day sits in the patient's first supply of a differently looking tablet, has no column in any file: it is a relation between each fill and the patient's previous fill through the register's dated descriptions and the centre's date.
Link: the tablet a fill supplied is read through a link no key offers: the pharmacy's distribution centre (pharmacies.csv) against the centre's date in the manufacturer's PDF letter against the register's descriptions by site, then each patient's own sequence of fills.
Reflex: the field's method (adjusted rates against the reference, with the switching allowance pharmacoepidemiology takes for generics) sits at rungs 0 to 2 and files Halvorne.
Back-test: the easy route reconciles everywhere it is habitually checked: Halvorne's excess appears in every age band, every resistance stratum and every centre, the switching allowance changes nothing material, and the site transfer in the letter gives the excess a ready story.
Second use: every file the decisive step reads is in the pack for the main counts or the formulary's own records anyway: the register and the letters are the formulary's product identity and supply notices, pharmacies.csv carries the distribution centre the supply chain runs on, and the claims and encounters are the spine.
Shock: Halvorne's excess reads as the ordinary story of a new manufacturing site, and Tessard's persistent excess is moderate and steady; the golden's product is not the largest on any shipped statistic, and no sort of any column isolates it.
Pins: MS-12 files the WHAT (products, outcome and its codes, dating, transfers, patients, supply and overlap, attribution, the comparison, the bar and the selection); no sentence names a clock, a change, a colour, a first fill, a distribution centre or adherence, and deleting any one MS-12 sentence leaves the call forced by the record or opens a count convention, never the decisive step.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 rates against the reference | none | product column | yes, the field's method | none | none | one ratio | none | readable |
| 1 adjusted for age and resistance | none | two member columns | yes | none | none | a model term | none | readable |
| 2 a switching allowance | none | product changes are one lag of a column | yes, the generics reflex | none | none | one term | none | readable |
| 3 colour from the letter on the letter's dates | the letter names the new look and the dates | none | no | none | none | a calendar term | none | readable |
| 4 first supply after an appearance change (decisive) | none: no sentence names a change, a colour or a first supply | no column marks it | no | none | none | a per-patient reconstruction across four files | none: every file it reads has a second use | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a different tablet | any difference in the register's description | colour alone | same call, same fills | every change in the record changes colour, and same-coloured products are one tablet in shape and debossing (asserted) |
| SF2 | when a centre's pharmacies moved to the new tablets | the letter's date for the centre | first new-site receipt; first new-site dispense | same call, one date | the letter: the old stock is collected from the centre and its pharmacies on that date and every bottle dispensed after it is Fort Wayne stock (asserted) |
| SF3 | visit dating | Pacific arrival date | UTC date of the partner feed | same call, same counts | MS-12 2.3; asserted: every arrival on a boundary or turning day sits in the daytime, clear of the UTC shift |
| SF4 | transfers | counted once on first arrival | counted twice | same call | MS-12 2.3 (asserted, R2) |
| SF5 | reversed claims | not fills; resubmissions are | kept | same call | MS-12 2.4 (asserted, R2) |
| SF6 | a member's first fill in the extract | no change | a change | same call | the extract starts 1 April 2025, nine months before the window |
| SF7 | age | band on 2026 less birth year | band on 2025 less birth year | same call | asserted on the golden (R2) |
| SF8 | an overlap of two supplies | the later fill's | carried forward | same call | MS-12 2.4 (asserted, R2) |
| SF9 | merged record numbers | one patient | separate | same call | MS-12 2.4 (asserted, R2) |

## Ladder

| Rung | Reader | Construction | Names (20 redraws) | At the shipped seed |
|---|---|---|---|---|
| 0 | first look | first look (crude rate against the reference) | Halvorne 20 | Halvorne 15.5, Tessard 5.6 |
| 1 | the field's method | standardised excess against the reference | Halvorne 20 | Halvorne 15.6, Tessard 5.7 |
| 1 | field-decomposing | age, resistance and centre standardised | Halvorne 20 | Halvorne 15.4, Tessard 5.5 |
| 1 | per-record | product, month, centre, age, resistance | Halvorne 20 | Halvorne 15.4, Tessard 6.0 |
| 2 | generics reflex | a transient after a change of product | Halvorne 20 | Halvorne 11.2, Tessard 1.3 |
| 2 | constructing | 90 days after a change of product excluded | Halvorne 20 | Halvorne 11.7, Tessard 4.0 |
| 2 | constructing | first 90 days on a product excluded | Halvorne 20 | Halvorne 13.6, Tessard 6.1 |
| 2 | site story | the new site's stock as the cause | Halvorne 20 | Halvorne 15.6, Tessard 5.7 |
| 3 | colour by the register | (d) colour dated by the register's approval date | Halvorne 20 | Halvorne 9.1, Tessard 4.9 |
| 3 | colour by the letter | (d) colour from the letter, dated by its centre date, 90 days | Halvorne 20 | Halvorne 12.0, Tessard 5.7 |
| 3 | colour by the letter | (d) colour from the letter, dated by its centre date, 180 days | Pellbrook 12, Corwen 8 | Pellbrook 10.7, Tessard 5.7 |
| 3 | switch and letter | (d) switching and the letter date together | Halvorne 18, Corwen 2 | Halvorne 7.3, Tessard 1.4 |
| 3 | temporal | the last two months' standardised rates | Pellbrook 20 | Pellbrook 30.1, Tessard 6.6 |
| 4 (decisive) | the golden | each patient's first supply of a differently looking tablet held as it was | Tessard 19 | Tessard 4.25, next Pellbrook 1.10 |

## Closure table

| Axis | Name | Reading | Closure |
|---|---|---|---|
| 1 | Population | every interchangeable 500 mg product dispensed in the window; members only | MS-12 2.1 and 2.4 |
| 2 | Unit of account | patient-months of supply, 30.4375 days | MS-12 2.4 |
| 3 | Attribution window | 1 January to 30 June 2026, Pacific dates | the prompt; MS-12 2.3; C1 (SF3) |
| 4 | As-of dating | each fill's tablet as the register and the letters set it on the fill's date | the letters; C1 (SF2) |
| 5 | Version basis | the register's description in supply on the fill's date at the fill's centre | the letters' dates; C1 |
| 6 | Denominator | patient-months of the product's supply in the window | MS-12 2.6 |
| 7 | Weighting | patient-days, one model over all products | MS-12 2.6 states the comparison over the same days; C1 across the family |
| 8 | Window length | the first supply of the new tablet, no parameter | C3: the 90 and 120-day clocks and fourteen-day bins give the same bin; C4: the 30, 60 and 180-day clocks refuted by the record's fit |
| 9 | Boundary inclusivity | window inclusive at both ends | C1, nothing within a clock shift of an edge (SF3) |
| 10 | Rounding path | whole visits once, at the end | the prompt |
| 11 | Tie-break | none needed | the call leads by 1.41 or more under every specification |
| 12 | Maturity and censoring | visits to 30 June; supply truncated at the window | MS-12 2.4; the first supply is constant within, so truncation is inert |
| 13 | Order of operations | net reversals, run supply, attribute, model | MS-12 2.4 to 2.6 |
| 14 | Row order | fills sorted by date then claim | C1: one result over same-day orderings |
| 15 | Duplicate resolution | transfers once; reversal pairs removed | MS-12 2.3 and 2.4 |
| 16 | Identity normalisation | MRN to member through the crosswalk, merged records included | MS-12 2.4 |
| 17 | Netting against gross | negative excesses stand as estimated | MS-12 3.1 reads the largest |
| 18 | Dimensional units | days of supply as dispensed | MS-12 2.4 |
| 19 | Code and status semantics | G40 and R56.9 first-listed; PAID and REVERSED | MS-12 Appendix A; the claim status |
| 20 | Integerisation | whole visits after the estimate | the prompt |
| 21 | Clause scope | MS-12 applies to the 500 mg tablets reviewed | MS-12 1 and 2.1 |
| 22 | Forward window contents | the re-test examines tablets now in supply; the excess carried by the tablets persists | MS-12 1; no forward file needed |

## Literal reader

Executing the prompt and MS-12 word for word: the comparison holds each patient's days of supply as they were and changes
only what the tablets release, so a literal reader who models the visits per patient-day must decide what else differs
between the products' patient-days; the record makes the first supply after an appearance change the term that fits
(asserted against the site, switch and fixed clocks), and with it held the call is Tessard under every licensed reading of
SF1 to SF9; the easy answer (Halvorne) comes from leaving that term out, an easy method on the same literal estimand,
never from another reading of a term. The asks: 7.3 and clauses 4 and 9 file every counting unit (receipt day, later
amounts, Pacific days, the day before the next shipment, item numbers through the item list).

## Oracles

None ties only under the golden. The supply monitor (dispensing by centre and month, all products together) agrees with
both readings; the contract laboratory's quotation and the list prices are distractors; the letters date the change and
say nothing about visits; the receiving log and the invoice lines reconcile on every reading of the asks.

## Ask sheet

Ask 1, what was spent on each generic in each quarter of 2026 so far (ten figures, dollars to the nearest 10), filed by
purchasing manual 7.3 (a quarter's spend is the invoiced amount for bottles received in it, a bottle received on the day
the receiving log books it in, a later amount for bottles already received in their quarter).
- Primary D8 (clocks), evidence `dc_receiving_log.csv`: invoices are dated the Friday of the dispatch week, and the
  receiving log books each bottle on its own day; Halvorne's Monday and Corwen's Tuesday dispatches at both quarter ends
  straddle the line, and Corwen's 31 March deliveries to two centres arrive in two parts. Moves Halvorne and Corwen in
  both quarters (Corwen Q1 +4650 dollars by invoice date, Corwen Q2 +1770 dollars by invoice date, Halvorne Q1 -2240 dollars by invoice date, Halvorne Q2 +10260 dollars by invoice date).
- Primary D6 (grain), evidence `wholesaler_invoice_lines.csv`: two contract amendments reach back over deliveries already
  invoiced. The rise for Pellbrook, Tessard and Wynfield covers deliveries dispatched from 1 December 2025 and is billed on
  the 1 May invoices (Tessard, Wynfield) and the 29 May invoices (Pellbrook, back from backorder); the reduction for
  Halvorne and Corwen covers deliveries from 9 February 2026 and is credited on the 19 June invoices. Each is one
  `PRICE ADJUSTMENT THRU` line per centre with no delivery reference; its bottle count is that centre's last bottles of the
  generic invoiced before it, counted back line by line to the first covered delivery, and no quarter's receipts, so 7.3
  sends each covered bottle's share to the quarter it was received in. Moves every spend figure for a reader who files
  each line in the quarter before its invoice (Corwen Q1 -2800 dollars, Corwen Q2 +2800 dollars, Halvorne Q1 -6190 dollars, Halvorne Q2 +6190 dollars, Pellbrook Q1 +4840 dollars, Pellbrook Q2 -2090 dollars, Tessard Q1 +4350 dollars, Tessard Q2 -1790 dollars, Wynfield Q1 +4250 dollars, Wynfield Q2 -2830 dollars).

Ask 2, how many days each generic was on backorder at the wholesaler in each of those quarters (ten figures, whole
days), filed by service schedule clause 4 (from the notice's opening day to the day before the next shipment of that
product to any ship-to, Pacific calendar days, each day in its quarter) and clause 9 (item numbers through the item list).
- Primary D7 (keys), evidence `wholesaler_item_list.csv`: at the wholesaler's 2 March 2026 cut-over Halvorne's old number
  447120 went to Corwen and Pellbrook's 448193 to Wynfield; the list gives every other generic's former number and none
  for those two, so a pre-cut-over notice whose number is no product's former number belongs to whichever of the two
  stopped shipping when it opened (the ship notices show which). Moves Halvorne, Corwen, Pellbrook and Wynfield in the
  first quarter and Pellbrook in the second (Halvorne Q1 -14 days, Corwen Q1 +1 days, Pellbrook Q1 -59 days, Pellbrook Q2 -33 days, Wynfield Q1 +4 days).
- Primary D4 (absence), evidence `wholesaler_advance_ship_notices.json`: the first shipment after seven of the backorders
  goes out in full cases under a case-level barcode (indicator digit 1) that no register lists, and regular each-level
  shipments resume the next week; read as an orphan, the backorder runs on. Moves the other five figures (Corwen Q2 +4 days, Halvorne Q2 +7 days, Tessard Q1 +7 days, Tessard Q2 +6 days, Wynfield Q2 +7 days).

Shared hazards: notice openings and ship times in UTC (Pacific days under clause 4), two-part receipts, cases of 12.
Families D8, D6, D7, D4, none repeated; no two devices share an evidence file; separation asserted (no device row in the
main call's files). Ladder stops per ask: invoice dating (0 of 10 kept), receipt days with each adjustment in the
quarter before its invoice (0), the golden; expected release dates (1), next shipment with orphans set aside
(0), case barcodes decoded with legacy numbers read through the current list (5), the golden.

| Ask | Cracker's route | Cracker keeps | Full includer keeps | Mirror keeps | Cracker |
|---|---|---|---|---|---|
| 1 spend by quarter | receipt days per 7.3, each adjustment line in the quarter before its invoice | 0 of 10 | 0 of 10 | 0 of 10 | miss |
| 2 backorder days | clause 4 with case barcodes decoded, legacy numbers read through the current list | 5 of 10 | 0 of 10 | 1 of 10 | miss |

Full includer: keeps 0 per cent of the ask figures (at most two fifths).
Pair ceiling: 35.4 (the cracker on the call at 58.8, the full includer off it at 12.0); the cracker and the full includer both on the call 51.9; two crackers both on the call 58.8.
Mirror leakage: 5.0 per cent of ask weight.
Measured by: generator/ceiling.py (shares no code with the generator; reads target/ and figures.json).

## Leak sweep rulings

`leak.py` on the final cut: REVIEW, no LEAK. Ruled in the main thread (the stump-vocabulary lines never go to the reader):
- MS-12, the 2.0 bar: the filed referral bar, the selection criterion the WHAT requires, not the answer; harmless.
- The Corwen and Halvorne letters (centre, change, tablet, distribution): the letters state a coat change and a site change
  with their dates and stock movements, as such notices do; neither names adherence, a first supply or visits; harmless.
- MS-12 (product, patient, tablet, record, attribution) and the purchasing manual (product, centre, distribution): the
  estimand's and the counting units' own nouns; no sentence names the move; harmless.
- The prompt's first sentence (stump terms): the question's own nouns; harmless.
- MS-12 naming ordinary column words (approved, arrival, diagnoses, fills, month): the procedure's own vocabulary, no
  field list or file description; sent to the reader to confirm.

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
- 2026-11-04, architecture 1 (Nordvig Marine's one jack-up for five North Sea sites, the shared heavy-lift berth at Bramso Havn)
  spent at stage 4 round 1: the judge sent it back on Gate H (decisive step planted). The practice the golden needs, the later
  arrival at a taken berth going on to Kalvholm, was moved out of the governing documents at stage 2 so that a per-placement
  joint replay of stated facts would land wrong, and so became a withheld rule recovered from settled cases; filed, the same
  practice makes the literal replay of the plan reach the golden. The mechanism had no legal form. Re-root in another world.
- 2026-11-04, architecture 2 draw, candidates screened on file before any harness (`guard.py slots`, mechanism and setting
  nouns): a deductible's end-of-year response (task174: the dynamic-incentive identification is a fork; task486:
  accumulators executed member by member are rule application); a closure's patients redistributed to a neighbouring
  emergency department (task174: it reads the same for a store closure, the swap test); mortality displacement after a
  severe winter (task173, task401, task128: dead on lever at realistic excess mortality); build-up and wash-off,
  including insulator pollution flashover on coastal lines (task121: the rate-times-exposure reflex ranked the units as
  the truth); colonisation pressure on a ward (task177, task181, task210); a stratifying lake's cyanobacteria (task202's
  setting).
- 2026-11-04, vaccine failure read through the screening method against the exposed group's own coverage: the decisive
  step settles the comparison population, which the WHAT must file, and filed it makes the computation follow from the
  clause (the WHAT screen).
- 2026-11-04, prototype 2 (`t211/a2/proto/proto2.py`): a flat 90-day transient after the colour change let a 60-day
  golden window leave Halvorne's tail standing (1 of 4 redraws on Tessard); the transient is front-loaded (a rate ratio
  decaying with a 35-day constant), the shape missed doses after an unfamiliar tablet take.
- 2026-11-04, one date for Halvorne's colour change at every pharmacy: its excess faded visibly by June, so a reader of
  the last two months' rates would land Tessard without the analysis; the change now reaches each distribution centre in
  turn, as a site transfer's stock does.
- 2026-11-04, the rollout run from 5 January to 25 May 2026: too much of Halvorne's transient fell after 30 June and the
  first look's margin over Tessard shrank to 1.6 to 1.8 visits per 1,000 patient-months; the wave starts 1 December
  2025 and ends 18 May 2026.
- 2026-11-04, card axes at the draw: context artifact `register` (task401 holds it, ban.artifact) redrawn to
  `monitoring_export`; the triple (objective, G4, decomposition_attribution) repeats task398 inside the batch and
  (population, G3, decomposition_attribution) task399's lineage, so population leads with G4, differentiated on the card
  against the older task121, task129, task232 and task243, and task162 v1.
- 2026-11-04, prototype 4's transient carried into the generator (a rate ratio 1 + 2.23 e^(-t/35 days) from the change
  fill): fixed-day clocks truncated it differently for 30 and 90-day supplies and the golden family spread past one
  whole visit; the response now lasts the patient's whole first supply of the new-looking tablet (rate ratio 2.5 for its
  30 or 90 days), the refill-level shape the colour-discordance literature measures.
- 2026-11-04, Tessard's persistent ratio 1.20 with the register's approval dated 17 November 2025: the approval-date reader
  named Tessard in some redraws; the approval is dated 15 September 2025, Pellbrook's contract share is 0.22 and Tessard's
  ratio 1.15.
- 2026-11-04, the 60-day clock listed as a careful reader: it is the decisive step with a clock shorter than a 90-day
  supply (Tessard in about half the redraws), so it moved to the refuted specifications with the 30 and 180-day clocks,
  each refuted by the record's fit against the first supply.
- 2026-11-04, 40,000 members on the molecule (16 redraws): the golden fell under the 2.0 bar in 1 and its lead under 1.2
  in 1, and the approval-date and letter-180 readers' margins over Tessard reached 1.2 and 0.9; the cohort is 60,000.
- 2026-11-04, the encounters extract from July 2025 at 60,000 members: the pack reached 17 MB; the feeds start on
  1 December 2025 (one month before the window) and both JSON feeds are written compact.
- 2026-11-04, a regular weekly shipment on the day a backorder's first case shipment went out: the full includer's
  orphaned case barcode cost it nothing on four figures; regular each-level shipments resume the following week, and the
  two Corwen first shipments that fell on Saturdays go out on the Fridays.
- 2026-11-04, a centre's first-quarter receipts of a generic equal to its receipts in another quarter (4 of 20 redraws,
  the golden's uniqueness assertion): the price catch-up's bottle count matched two quarters; the generator keeps each
  centre's first-quarter total distinct, and every Halvorne and Corwen spend figure moves at least four bins between
  invoice and receipt dating.
- 2026-11-04, purchasing manual 7.3 saying that a delivery received in two parts can fall in two quarters: it narrated the
  receipt-day device; cut, the receipt day alone is filed.
- 2026-11-04, the Halvorne letter dating only the centres' stock: a pharmacy's shelf stock would lag the centre's date, a
  second reading of each patient's change date; the letter now has the old stock collected from the centre and from the
  pharmacies it supplies on that date, so every reading gives one date.
- 2026-11-04, the PDFs carried their writer's comment line in the header: blanked at equal length in the generator.
- 2026-11-04, a catch-up covering exactly the first quarter's receipts: a reader acting on 7.3's price-correction clause
  puts it in the first quarter and keeps every figure (the full includer at 50 per cent); the amendment now reaches back
  to deliveries dispatched from 1 December and forward to the 24 April invoices, so its bottles span three quarters and
  only the run of covered deliveries, counted back from the line's date, places it.
- 2026-11-04, wholesaler volumes a twelfth of what 60,000 members dispense: scaled to the dispensing, with the
  look-alike's orders rising while its partner is out.
- 2026-11-04, the prompt's shell (whether, if, docx+xlsx) repeated task244 on `guard.py heart`: the second sentence now
  leads with the use.
- 2026-11-04, the workbooks' property parts carried their writer and the build clock, and the memo a writer's description:
  rewritten in the generator to the organisation's own properties and the fixed date.
- 2026-11-04, the asks at the coordinator's review: the cracker kept 12 of 20 (60 per cent), executing 7.3's receipt day
  for Halvorne and Corwen, keeping Pellbrook's second quarter (no device on it) and decoding the case barcodes for seven
  backorder figures. Reworked: a second amendment (a reduction for Halvorne and Corwen from 9 February, credited 19 June)
  and Pellbrook's rise billed after its backorder put a catch-up on every spend figure, and Halvorne's legacy item number,
  reissued to Corwen with no former owner listed, joins Pellbrook's, resolved by which product stopped shipping.

## Pre-ship check

Stage 4 round 1 and ship, 2026-11-04, final cut target.zip f7e348d0 (rebuilt on the merged branch in a clean copy and
again in place, byte-identical across the zip, the goldens and submission.md):

- The 10/10 rules re-read against the built pack: the decisive step is still holding each patient's first supply of a
  differently looking tablet as it was, so the release-attributable excess separates from the appearance-change
  transient; analytical, a response estimated from the record, and no field, rule or filed sentence performs it or
  ties appearance to adherence. The mess is still Layer 1 only (two claim code schemes, reversals, merged MRNs, UTC
  against local feeds, transfers, split receipts, the item-number cut-over).
- Judge round 1 (order kept): DETERMINISTIC, APPROVE, no fix. Every golden figure reproduced: patient-months, visits,
  spend by quarter received, backorder days, Tessard's excess 4 (4.07 to 4.45 on every adjusted estimator). Gate F
  good (the crude and the case-mix adjusted excess file Halvorne at 15.5), Gate G decomposition_attribution and
  analytical_non_defect, Gate H domain pass, layers pass, decisive step analytical.
- Known stump-power risk, ruled by the coordinator: the judge's own blind derivation found the appearance-change
  transient and filed Tessard before it opened the graded blocks, by an adjustment beyond the natural route. The judge
  rated Gate F good, the bar needs one of the top two responses stumped, and the portal is the only stump oracle; a
  same-day re-root waits for the portal's word unless the judge has killed the version, and this judge approved it.
  Shipped with the risk named here and in the ledger row.
- Leak reader round 1: no decisive-step sentence, no ranking or helper file, nothing reads as the answer, the decisive
  step analytical (round and rulings in leak_check_report.md).
- Coordinator's rulings on the build's flags:
  - The refuted 60 and 180-day clocks name Halvorne and Pellbrook at the shipped seed: the record's own fit refutes
    them (likelihood gains of 383 or more), and the judge's family stayed in one bin.
  - The judge's residual fork 1 (the backorder ask's reissued item numbers): the golden's reading is the only one
    consistent with the item list's effective date, its former-number column and the ship notices; the naive lookup
    contradicts the list's own columns. Its optional hardening line declined (it would execute the reconstruction).
  - The judge's residual fork 2 (whole-visit rounding of 4.07 to 4.45): every estimator it ran stays in the bin; the
    steady-state-only additive standardisation (4.9) drops the first-supply days the estimand keeps.
  - Realism: 60,000 members on the molecule and 620 pharmacies is large for the stated region. Neither reviewer
    flagged it, and it is left as is rather than change the judged pack.
  - guard.py surface promotes four pairs on card axes (task129, task232, task121 and one more), each carrying the
    same-driver signature and a differentiation line on the card; no surface tell; nearest driver 0.07.
- Gates re-run on the final cut: `checks.py` 75 checks, 0 failed; `verify.py` 0 mismatches; two builds byte-identical;
  `figures_check.py` 37 figures, 0 absent; `precut.py` 61 checks, 0 FAIL, 0 WARN; `voice-check.py` PASS; `ceiling.py`
  (inside checks) cracker 5 of 20, full includer 0 of 20, pair 35.4 one on the call, 58.8 two crackers on it;
  `leak.py --asof 2026-07-20` REVIEW, 0 LEAK (the answered lines); `guard.py heart` WARN, no BLOCK; `guard.py surface`
  exit 0.
