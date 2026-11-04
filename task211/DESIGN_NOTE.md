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
first and replaced: people.first WARN against task273).

**Guard.** `check` on the draft and on the registered card: WARN, exit 0. Answered:
- `repeat.gate_g` and `overuse.gate_g` (decomposition_attribution, task401 and 6 of 12): the stump is an excess split
  between two causes, a transient each patient carries after a change of tablet appearance and the product's persistent
  effect, which is the key's own definition; `method_or_model_selection` was probed and is the less honest label (no
  rival estimator is chosen between, a cause is removed).
- `repeat.question_form` (which, task401): the decision picks one product or none, so the form is which; the shell is
  redrawn at the role level instead (second-sentence opener and deliverable set, stage 2).
- Furniture redrawn against the live window: context artifact `register` (ban.artifact, task401) to
  `monitoring_export`, the system's quarterly product surveillance export the director works from; the structural triple
  (objective, G4, decomposition_attribution) repeats task398 inside the batch and (population, G3,
  decomposition_attribution) task399's lineage, so population leads with G4, and the older repeats (task121 v6,
  task129 v2, task232 v2, task243) carry differentiation lines on the card, with task162 v1 (0.06, reports following each
  unit's first use of a new version) differentiated too.
- Nearest driver 0.07 (task98 v4 lineage); every other driver on file 0.07 or under.

**World.** Larkhaven Health, a fictional integrated health system in Oregon and southwest Washington (about 5 million
members, its own pharmacies supplied from seven distribution centres). About 24,000 members take levetiracetam 500 mg
tablets. Six products are interchangeable on the formulary: Levaril (the reference brand), Corwen (its authorised
generic, identical blue tablets until Corwen's film coat turned white on 1 September 2025), Halvorne Generics and
Pellbrook Pharmaceuticals (identical white oval tablets made by Marrowby Pharma Services), and Tessard Laboratories and
Wynfield Pharma (identical orange tablets made by Brennick Contract Manufacturing). Pharmacies dispense the generic their
supply contract names and move to its look-alike partner when the wholesaler backorders it. Halvorne moved manufacture
to its own new site in late 2025; the new site's tablets are pink, and its supply reached each distribution centre in turn
from 1 December 2025 to 18 May 2026 (the manufacturer's transition letter).

**Decision.** In July 2026 the committee books one product into the contract laboratory's third-quarter assay and
dissolution re-test, or none. Which product goes, and how many seizure-related emergency visits per 1,000 patient-months
does it add over what the same patients would have had on tablets releasing levetiracetam as Levaril does?

**The WHAT, filed at stage 2 in the committee's surveillance procedure (no sentence names a clock, a change, a colour or
a switch).** Candidates: every interchangeable levetiracetam 500 mg product dispensed in the window. Outcome:
seizure-related emergency department visits and urgent admissions (seizure codes as the first-listed diagnosis). Window:
1 January to 30 June 2026. Unit: per 1,000 patient-months of the product's dispensed supply. Comparison: the product's
patients' visits less what the same patients, on the same days, would have had if their tablets had released and
delivered levetiracetam as the reference product's do. Selection: the largest such excess is booked, none if no product
reaches the procedure's bar.

**Data-native sentence.** The dispensing record names the product each fill supplied, but what a patient was handed,
the tablet's colour, is set by which site made it and which distribution centre served the pharmacy on the fill's date,
and appears only in the product register's dated descriptions and the transition letter; a patient's first fill of a
differently coloured tablet brings weeks of missed doses and seizure visits, so Halvorne's rolling colour change books a
transient to Halvorne that no tablet content causes.

**Abstraction sentence (against the nearest approved builds).** Against task196 (a second capture channel produced by
chasing the first) and task182 (each unit's own lagged driver response), no sentence a reviewer holding both would call
the same: here an excess is split between a transient each member carries after their own first encounter with a
changed version of the item, dated by the supply point that served them, and the candidate's persistent effect; the
driver with the nouns stripped is on the card.

**Sources (planned).** Every file synthetic, generated from one seed, invented world, CC BY 4.0, recorded in
`metadata.json`: the dispensing claims extract (parquet, about 230,000 claim lines, July 2025 to June 2026, across a
claims-platform cut-over), emergency encounters from two hospital feeds (one in Pacific local time, one in UTC), the
member and record-number crosswalk, the pharmacy register (pharmacy to distribution centre), the product register's
dated descriptions, the manufacturer's supply transition letter (PDF), the wholesaler backorder log, the committee's
surveillance procedure (PDF), the quarterly product surveillance export (workbook, counts only, no rates by product), and
distractors named only in `metadata.json`.

### The five go/no-go screens (clean truth; 20 redraws, seeds 5000 to 5019, `t211/a2/proto/proto4.py`, `r4_summary.txt`)

The clean truth: each patient-day carries a base seizure-visit rate (age and drug-resistant epilepsy), Tessard's
persistent effect (rate ratio 1.20 since July 2025) and a transient after each fill whose tablet colour differs from the
previous fill's (rate ratio 1 + 2.23 e^(-t/35 days), averaging 1.8 over the first 90 days); a change of manufacturer
between look-alike tablets carries none.

1. **Realistic levels and the lever.** Levels, each cited: colour discordance at a refill raises the odds of stopping an
   antiepileptic 53 per cent (Kesselheim et al., JAMA Internal Medicine 2013;173:202-208), and generic cardiovascular
   drugs show the same (Kesselheim et al., Annals of Internal Medicine 2014;161:96-103); a formulation switch before a
   seizure-related ambulance, emergency or inpatient event carries an odds ratio of 1.81, 95 per cent CI 1.25 to 2.62
   (Zachry et al., Epilepsia 2009;50:493-500); nonadherence to antiepileptics raises emergency visits, admissions and
   mortality (Faught et al., Neurology 2008;71:1572-1578, RANSOM); about a third of treated patients are not seizure
   free (Kwan and Brodie, NEJM 2000;342:314-319), world-set here as 22 per cent at 2.5 times the base; the base, about 30
   seizure-related urgent visits per 1,000 patient-months (0.36 a person-year), is world-set within the range treated
   epilepsy cohorts show in US claims (Faught 2008; Zachry 2009). Tessard's 1.20 is world-set, the size a product at the
   low end of the bioequivalence window can carry; marketed generics found not to perform as the brand have precedents
   (FDA's 2012 withdrawal of Budeprion XL 300 mg; FDA's 2014 reclassification of two methylphenidate extended-release
   generics from AB to BX). The lever: the golden names Tessard in 20 of 20 redraws, its lead over the runner-up at least
   1.64 (90-day specification) and at least 1.26 across every supported specification; the first look's Halvorne exceeds
   Tessard in 20 of 20 by at least 1.65 visits per 1,000 patient-months (median Halvorne 11.5 against Tessard 5.8 on the
   first look; golden Tessard median 5.8, runner-up 1.2). Mid-bin at the shipped seed and the pack under 15 MB are
   asserted in `generator/checks.py` at stage 3.
2. **The golden's own method holds the call.** Eight specifications of the transient (90-day, 60-day, 120-day and 180-day
   windows, a two-piece 0 to 45 and 45 to 90 days, fourteen-day bins to 182 days, time since the first new-site fill,
   and the 90-day window with region and calendar month added) name Tessard in 20 of 20 each; within a redraw they agree
   on Tessard's excess to 0.17 visits per 1,000 patient-months or better. A 30-day window names Tessard in 16 of 20 and
   is outside the supported range: the record's own transient profile (fourteen-day bins) runs about two months.
3. **The first look lands wrong**: 20 of 20 (product rates against the reference name Halvorne).
4. **The careful readers land wrong**: (a) the field-decomposing reader, age, drug-resistance and region standardised,
   20 of 20 on Halvorne; (b) the constructing reader, each patient's first 90 days on a product excluded, 20 of 20, and
   the 90 days after any change of product excluded, 20 of 20; (c) the per-record reader, a Poisson model on product,
   calendar month, region, age and drug resistance, 20 of 20; (d) the mechanism-naming readers: a manufacturer-switch
   transient 20 of 20, the new site's stock as the cause 20 of 20, and the colour change dated by the register's approval
   of the new description (17 November 2025) for every patient 19 of 20; (e) the literal joint replay of the procedure's
   stated facts (standardised product excess against the reference) 20 of 20. A temporal reader (the last two months'
   rates) lands Halvorne 20 of 20.
5. **Literal execution** of the filed WHAT (each product's standardised excess against the reference, with or without
   the switch allowance) lands Halvorne in 20 of 20; the golden needs the transient estimated from the record, which no
   filed sentence asks for and no practice supplies: it is the patients' response to what they were handed.

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
