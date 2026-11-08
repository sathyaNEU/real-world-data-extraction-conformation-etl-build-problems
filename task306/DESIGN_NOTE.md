# task306 design note

Architecture 5, drawn 2026-11-08 after the portal returned architecture 4 FAILED_TO_STUMP on 2026-11-07 (both
responses filed the golden capacity call and all 24 ask figures). One architecture per world: energy (EV packs),
urban (regional GVA), actuarial (windstorm reinsurance) and quantitative finance (market impact) are spent in this
slot, so the build moves to pharmacology with a new world, dataset, generator and prompt shell. The author's five
conditions of 2026-11-07 bind the design and are argued in `## Author's conditions` before any data is cut.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task306.json`, architecture 5, registered 2026-11-08; architecture 4 moved
   into the card's lineage with its fate (the four earlier architectures sit there as spent).
2. Pairing: Pharmacology, Pharmacoepidemiology & Safety, task type benefit-risk-assessment, objective Opportunity
   Sizing & Decision Support (never carded on this objective). The headline is a sized opportunity, pool to
   realisable: each review's eligible patients (the pool), the patients a year of pharmacist reviews would take off
   the medicine for good (the realisable part) and the serious harms that avoids, which decides the call.
3. World: Marches Primary Care Collaborative, a GP federation in the West Midlands whose clinical pharmacist team
   serves its member practices under NHS Severn Marches Integrated Care Board's medicines safety contract. The team
   can run one structured deprescribing review across every member practice in 2027-28. In the first half of 2026 it
   piloted all three candidate reviews in the Clun Valley Primary Care Network's practices (rural, far from the
   specialist services) and followed each reviewed patient for six months. Specialist letters reach the practices
   from Wrekinside Teaching Hospitals NHS Trust and Marches Mental Health NHS Trust. People from `guard.py names --geo
   "United Kingdom" --seed 306`: Colin French (the federation's lead clinical pharmacist, who ran the pilot, runs the
   team across the practices and puts the 2027 review to the board), Leigh Bond (the federation's clinical director,
   who chairs the board), Sylvia McDonald (the board's medicines optimisation pharmacist, who manages the contract).
4. Candidates: (A) antipsychotics in people aged 65 and over (excluding psychosis, schizophrenia and bipolar disorder);
   (B) benzodiazepines and Z-drugs in people aged 65 and over; (C) gabapentinoids taken with an opioid.
5. Quantity: for each review, the serious harms a year it would avoid if run from April 2027 across the member
   practices outside the pilot network: the sum over the patients meeting its protocol on 31 December 2026 of each
   patient's chance of being off the medicine six months after review times the attributable harm rate per
   patient-year at their age (the programme specification's section 3 and table 1). The call is which review runs.
6. Shape: other. Three reviews, each with the patients it takes off and the harms that avoids (6 figures); the call,
   the runner-up and the gap (3); a two-panel chart (2 to 3); the letters each network's practices received in each
   half of 2026 (10); each network's patient consultations in each quarter (20); the two files: 43 to 44 criteria.
7. Default path: carry each review's pilot take-off rate (the share of reviewed patients still off the medicine six
   months on) to the federation's eligible patients and weight them by the harm table; it files antipsychotics.
8. Data-native sentence: the practices' records carry each medicine's first issue and the specialists' letters carry
   each recommendation to start one, so who started a patient's medicine is a relation between two systems that no
   field stores; the pilot practices' patients were mostly practice-started because the Clun Valley is far from the
   memory and older adults' services, while elsewhere in the federation most older people on an antipsychotic were
   started by a specialist service, and practice pharmacists almost never stopped a medicine a specialist had started.
9. Abstraction sentence, written against the nearest approved builds and found not to be the same: task258 carries a
   playbook only where the mechanism's precondition holds (the preload in the served head) and task309 carries a cut
   by a physical intensity; here the review reaches every eligible patient, nothing in the mechanism is absent and
   nothing varies in intensity: the measured success rate depends on a provenance, who started the medicine, which
   the pilot's population nearly all shared and the federation's antipsychotic users mostly do not. The card carries
   differentiation lines against task258, task309, task124, task141, task303, task137, task128, task304 and task98.
10. Furniture: forum board_of_directors (the federation's board approves its 2027 programme), forcing
   purchase_order_or_contract (the integrated care board's 2027-28 medicines safety contract names the review in its
   schedule), org hospital_or_health_provider (a GP federation providing the pharmacist service), role field_unit_lead
   (the lead pharmacist runs the team across the practices). Redrawn after registration: task482's architecture 17
   registered minutes before this card with committee_or_panel, launch_or_rollout and programme_officer, so those three
   were redrawn to the board, the contract and the team lead, each the honester description of who decides, what
   forces it and who asks, not merely the passing one. Redrawn at the draw: forum executive_team, forcing
   budget_or_appropriation and the stump strategy composition_mix each repeated a build in the primary checkout's
   window (task204, task142), and decomposition_attribution repeated task185 there. Two strategy keys describe this
   design honestly, composition_mix (the pooled rate does not fit this pool's mix on a property no column names) and
   forecast_method_backtest (`strategies.md` F6: the rate is stationary only in a constructed exposure, rebuilt from a
   log, and the natural carry fails forward); the card takes the second because the window bars the first, and the
   design note's step is exactly F6's: the take-off rate is stationary only within the provenance rebuilt from the
   letters. No back-test picks it (condition 2 below).
11. As of 6 January 2027, the extracts' pull date; the board meets on 14 January 2027 and the review starts in April.
12. Prompt shell: a how-much question (the harm each review would avoid), the second sentence opening on the paper
   for the board, the rounding sentence opening "Patients"; deliverables pdf and csv. None repeats a shell in this
   slot's lineage. Guard on main: PASS. Guard from the primary checkout: WARN repeat.gate_g (forecasting against
   task142), answered: the forecast here is a take-off carried across provenance, task142's is a population
   projection.

## Author's conditions

1. The field's full textbook method, done carefully, files the wrong call. The field's method for a deprescribing
   review's value is absolute harm at each patient's age times the patients the review takes off, the take-off read
   from the review's own pilot (benefit-risk card 1: absolute risks at each subgroup's baseline). Done carefully (each
   review's own pilot rate at six months, the protocol's eligibility and exclusions applied, ages banded, practice
   mergers conformed, the pilot checked for homogeneity across its practices, ages and sexes, which it passes), it
   funds antipsychotics. Only the step the data's structure demands files the golden: the take-off rate is stationary
   only within provenance, so it must be carried by who started each medicine, rebuilt from the letters. No sentence
   in the pack says that a specialist-started medicine is harder to stop or that provenance should be read.
2. The data does not reveal the right method by fit. No model is fitted. The pilot's pooled rate reproduces the
   pilot exactly and so does the provenance-stratified rate; neither is tested on the federation, whose 2027 outcome
   does not exist yet; the pilot is homogeneous on every recorded attribute (practice, age band, sex), so no residual,
   R-squared, back-test or reconciliation on any shipped column prefers the golden route.
3. The asks are not executable from filed rules: each rides a reconstruction across two systems or grains no sentence
   states (designed in `## Ask sheet`, `supplemental-stumping` Part 2.1), and on paper each of the top two keeps under
   two fifths of the ask weight.
4. The ladder (`## Ladder`) keeps at least one of the top two off the call: every route that does not rebuild
   provenance files antipsychotics, including every reweighting by a recorded attribute; the pair is argued near 50
   and built under 60 against a bar of 70.
5. The three rules sit in `## Three rules`, each on its own line; `precut.py` exit 0 before data is cut.

## Default path

1. Read the federation's 2027 medicines safety programme specification: one review run from April 2027 across the
   member practices outside the Clun Valley network, valued at the serious harms a year it avoids, the sum over the
   patients in scope of each patient's chance of being off the medicine six months after review times the harm rate
   at their age in table 1 (section 3).
2. Run each review's protocol on the practices' issue, problem list and registration extracts on 31 December 2026:
   612 patients for the antipsychotic review, 1,239 for the benzodiazepine review and 1,636 for the gabapentinoid
   review.
3. Read the 2026 pilot from its close-out report and outcome log: the share of reviewed patients off the medicine six
   months on is 40.0 per cent for antipsychotics, 23.0 for benzodiazepines and 27.9 for gabapentinoids, the same
   across the pilot's practices, age groups and sexes (smallest p-value 0.21).
4. Carry each review's pilot rate to its patients in scope and weight by the harm rate at each patient's age: about
   24 harms a year for antipsychotics against 12 for benzodiazepines and 11 for gabapentinoids.

Ends on: the antipsychotic review, about 24 harms a year avoided.
Golden: the benzodiazepine review, 12 harms a year avoided against the gabapentinoid review's 8 (the runner-up) and
the antipsychotic review's 6; gap 4.

## Stump sentence

The default path carries each review's pilot take-off rate to the federation's patients in scope and funds the
antipsychotic review at about 24 harms a year; the step that lands it there is carrying the pilot's average rate to
every patient, when practice pharmacists almost never stopped a medicine a specialist service had started (4 of 96
in the pilot), the pilot's antipsychotic patients were mostly practice-started (136 of 160) and a specialist service
started 86 per cent of the antipsychotic patients in scope, so the antipsychotic review would avoid about 6 harms a
year against the benzodiazepine review's 12.

## Three rules

Task type: benefit-risk-assessment (Pharmacology, Pharmacoepidemiology & Safety), which serves Opportunity Sizing & Decision Support: each review's eligible patients are the pool, the patients a year of reviews takes off for good the realisable part, and the serious harms that avoids decide the call.
Domain test: the quantity that decides is the serious harm a deprescribing review avoids, worked the way benefit-risk works it: the absolute harm a patient's continued use carries at their age, from the programme's attributable rates, summed over the patients the review actually takes off; with another field's nouns there is no medicine, no specialist who started it, no harm per patient-year of use and no pharmacist's review to stop it.
Swap: "which of three loyalty campaigns should the retailer run, sized by the lapsed customers each wins back" keeps the arithmetic shape but loses what decides here, because no campaign's success depends on which body first put a customer on a product and no attributable harm per year of use weights the people it moves.
Layer 1: the systems' own records: practice prescribing coded by dm+d virtual product against trust letters naming medicines in free text, one row per medicine line, with strengths and brand names; two practices merged on 1 April 2025, their registrations carried by the survivor and the hospitals' practice field keeping the old code for some patients; two trusts' date formats; a minority of letters carrying only a hospital number, resolved through the federation's lookup; the pilot log's six-month row beside its review row; the mental health trust's April 2026 system change (an outage week's letters sent on 7 April, four weeks re-sent under new references); the hospital trust's GP Connect receipts from October 2026 with a message id and the message's date; letters dated over Christmas arriving in January; the hub booking system in UTC; hub appointments written into shared-record practices' systems on the day or the next working day; group reviews held as one booking with a separate register. Each is produced by the system that writes it, none is placed to be caught, and with every one handled the call is unchanged (checks.py R2).
Layer 2: estimand_identification, carrying a pilot's measured success to a different population: the pilot's take-off is stationary only within who started each medicine, so it must be carried by that provenance to the federation's own mix, not at the pilot's average.
Decisive step: for each patient in scope, reading whether a specialist service started the medicine (a hospital or mental health trust letter naming a medicine of the class shortly before the practice first issued it) and carrying the pilot's take-off for patients started that way, because the pilot's pharmacists took 196 of 604 practice-started patients off and 4 of 96 specialist-started, and the pilot's patients were mostly practice-started.
Not semantics: every field read right (the dm+d codes, the letters' recommendations, the six-month status, the harm table's bands) still leaves the pilot's average take-off, which is a correct figure for the pilot's own patients; no field records who started a medicine, and the take-off's dependence on it appears only when the pilot is split by a relation no column holds.
Not rule application: no filed rule says who can be taken off or how a pilot carries; the protocols file eligibility and the specification files the harm rates and the sum over patients, and executing every filed sentence with the pilot's reported rates funds antipsychotics. The enumerated family (the pilot's average; its rate re-weighted by age band or sex; carried by product; provenance read from any class letter at any time; the provenance carry under every window from 30 to 365 days, either date basis, hospital-number letters dropped or resolved, Start letters only, the specialist rate pooled across reviews, and stratified by age band or by sex) spreads the antipsychotic review's harms from 5.8 to 24.1 a year; the standing family (the routes the pilot's own outcomes leave defensible once provenance is read: 46 against 4 per cent off) spreads them from 5.84 to 6.15 and every rounded figure stays (checks.py M5); what rules the rest out is the pilot's own split, never a sentence.
Analyst test: a strong analyst conforms every record, applies each protocol, carries each review's pilot take-off (40.0, 23.0 and 27.9 per cent, the same across the pilot's practices, ages and sexes) to the patients in scope, weights them by the harm table and funds the antipsychotic review at about 24 harms a year; every field and rule is read right, and the call is wrong because a specialist service started 86 per cent of the antipsychotic patients in scope and the pilot's pharmacists took 4 of 96 specialist-started patients off.
Estimand: medicines_safety_programme_2027.pdf section 3: population, the patients registered at member practices outside the Clun Valley network who meet the review's protocol on 31 December 2026, every one of whom the team reviews; outcome, the serious harms a year the review avoids, the sum over those patients of each patient's chance of being off the medicine six months after review (no class issue in the 183 days after it) times the attributable harm rate in table 1 at their age on 31 December 2026; unit, harms a year, and patients taken off as the sum of the chances; comparison, the largest.
No decoy: nothing is planted to be caught: no memo, briefing or stakeholder argues for a review, the pilot close-out reports what the pilot measured and recommends nothing, and no document ranks the reviews by the harm they would avoid across the federation.
No certified replay: no certified or published figure reproduces the method; the close-out's rates are the pilot's own, true for its patients, and no file carries a federation-wide take-off, a provenance share or a harm estimate for any review.
Lesson: a programme's measured success carries to a new population only through what it depended on, and what a deprescribing review depends on most is who started the medicine; a model that learns to ask where each patient's arrangement came from before carrying a pilot rate sizes medicines programmes the way the field should, which no build on file teaches.

## Survivor anatomy

Actor: the deciding property, who started a patient's medicine, has no column: the practices' records carry the first issue, the letters carry a recommendation and a date, and provenance is the relation between the two (a letter naming a medicine in the review's class shortly before the practice first issued it) that nothing stores.
Link: no key ties a letter to a medicine course; the link is the patient's pseudonym plus a time order plus a free-text medicine name read against dm+d, and no sentence invites reading letters for the call: the letters are in the pack for the board's letters workload (ask A).
Reflex: the field's method for a review's value, absolute harm at each patient's age times the patients taken off at the review's own pilot rate, sits at rung 1 and files the antipsychotic review.
Back-test: the textbook route validates: the pilot's take-off is homogeneous across its practices, age bands and sexes (asserted, smallest p-value 0.21), the close-out says so, and the pilot rate reproduces the pilot's own outcomes exactly; no record of the federation's 2027 outcome exists to refute it.
Second use: every file the decisive step reads has its own reason to be in the pack: the letters feed ask A, the medication courses and prescribing issues carry each protocol's eligibility, the pilot log carries the take-off, the registrations carry ages, eligibility and ask B's networks, the list sizes both asks' denominators.
Shock: the antipsychotic review's pilot rate is the highest and its pool harm the largest, which reads as ordinary; the golden (benzodiazepines) is not the top of any sort of the reviews by eligible patients, pilot rate, harm rate, pool harm or patients taken off at the pilot rate (asserted in checks.py, R0).
Pins: the WHAT sits in the programme specification (the population outside the Clun Valley network on 31 December 2026, the six-month definition of off, the harm table and the age it is read at, the sum over patients) and the protocols (eligibility); no filed sentence names who started a medicine, specialists, letters, provenance or a carry by subgroup (R1).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 eligible patients times the harm rate, no take-off | the specification's harm table | the courses' columns | the pool-harm reflex | none | none | one product | yes | readable |
| R1 the pilot's take-off times eligible times harm | the close-out's rates | the pilot log | the field's method | the pilot reproduces itself | the battery cleans the log | one product | yes | readable |
| R2 R1 re-weighted by age band, sex, practice or product | none | the pilot log's columns | a case-mix carry | the close-out's homogeneity table | none | one product | yes | readable |
| R3 (decisive) each patient's take-off by who started the medicine | none names provenance, specialists or letters | no column holds provenance | not the carry reflex | no file prices any review federation-wide | the battery stops at clean courses | not affine in any shipped column | the letters carry ask A | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | eligible | the protocol on 31 December 2026 (issues in the six months to and including that date) | issues in calendar 2026; the six months' first day read as 29 June, 30 June or 2 July | same call (asserted); the same patients in scope under every first day (asserted) | the protocols' search sentence and specification section 3.2 |
| SF2 | off the medicine | no issue of a medicine in the review's class in the 183 days after review | off at review | not the pilot's measure; every six-month row equals the 183-day rule (asserted) | specification section 3.4 and protocol step 5 |
| SF3 | the population | patients registered outside the Clun Valley network | every member practice | same call (asserted) | specification sections 1 and 3.2 |
| SF4 | the age a harm rate is read at | age on 31 December 2026 | age at review in 2027 | same call (asserted) | specification section 3.3 |
| SF5 | who started the medicine | a letter naming a class medicine in the 60 days before the first issue of the patient's earliest class course | 30, 90, 180 or 365 days; Start recommendations only | same call and rounded figures (asserted, C1) | convergence: every specialist-started course has its letter 5 to 26 days before its first issue and none earlier, and no practice-started course has a class letter in the 365 days before |
| SF6 | the letter's date | the trust's letter date | the practice's received date where the workflow log holds it | same call and rounded figures (asserted, C1) | convergence: every initiation letter was received before the first issue |
| SF7 | letters carrying only a hospital number | resolved through the lookup | dropped | same call and rounded figures (asserted) | no initiation letter carries only a hospital number |
| SF8 | the pilot's specialist-started take-off | each review's own | pooled across the reviews | same call and rounded figures (asserted) | convergence: the three reviews' rates are equal (1 of 24, 1 of 24, 2 of 48) |
| SF9 | a patient on two medicines in a class | one patient, the earliest course | one per course | same call (asserted; 74 patients, all practice-started) | the protocols: a search finds patients |
| SF10 | a patient in scope for two reviews | counted in each review | dropped from one | same call (asserted; 16 patients) | only one review runs |
| SF11 | the pilot's review row against its six-month row | the six-month row | the review row's outcome | not the pilot's measure; same call (asserted) | specification section 3.4, protocol step 5 and the close-out's off rate |
| SF12 | merged practices | their patients in the survivor's network | the old code's network | same call (each merged practice sits in its survivor's network, asserted) | the practice register's closed date and successor |
| SF13 | rounding path | each figure rounded once from its unrounded sum; the gap from the rounded figures | the gap rounded from the unrounded sums | same gap (asserted) | the prompt's rounding sentence |
| SF14 | a course's first issue | the courses extract's first_issue_date | the earliest issue in the issue extract | not a first issue: the issue extract starts on 1 July 2025 | the field's name; it equals the issue extract wherever that covers the date (asserted) |
| SF15 | a course begun before the letters feed opened (1 October 2019) | none exists: every class course began on or after 15 November 2019 | treated as of unknown start | same call (none exists, asserted) | the courses extract |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | patients in scope times the harm rate (pool harm) | antipsychotics (60.3 against 51.1 and 38.8) | the specification values what a review takes off, not the pool |
| 1 | the pilot's take-off times each patient's harm rate | antipsychotics (24.1 against 11.8 and 10.8) | a specialist service started 86 per cent of the antipsychotic patients in scope; the pilot's were mostly practice-started |
| 2 | rung 1 re-weighted by age band or sex, or carried by product | antipsychotics | the same fact: none of those attributes moves the take-off |
| 2b | provenance read from any class letter at any time | antipsychotics (15.8 against 12.0 and 9.2) | a letter after the medicine began did not start it; the pilot's antipsychotic split blurs to 23 against 47 per cent |
| 3 (decisive) | each patient's take-off by who started the medicine | benzodiazepines 12.0, gabapentinoids 8.1, antipsychotics 6.2 | the golden |

- Position and margins (measured, checks.py M3 and L1): the golden is second on rungs 0 and 1 and first on rung 3;
  rung 1's winner leads by 2.05 times; the golden leads the runner-up by 1.48 times and the runner-up the third by
  1.32 times.
- Pricing sequence. (1) The residue the filed WHAT leaves is how each patient's chance of coming off is carried from
  the pilot, a method, not a knob. (2) The antipsychotic review falls from 24.1 to 6.2 harms: its carried take-off
  falls from 40 to 10 per cent. (3) The one-group-by routes (the pilot by any recorded attribute, or by product) are
  homogeneous by construction and file rung 1. (4) The take-off rates are observed proportions over a pilot of 700
  patients with a six-month check; the standing family's spread (provenance alone, or by age band or sex) moves the
  antipsychotic review by 0.31 harms and no rounded figure. (5) and (6) No variance is corrected. (7) No subset of
  rows prints a review's federation-wide figure. (8) The reflex sweep runs as code (checks.py L0 to L5, R3).
- Bin test: the decisive step is worth about 18 harms on the antipsychotic review against a standing spread of 0.31;
  each graded harm sits within 0.16 of its whole number and each patients figure within 2.2 of its ten (M4).

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the protocol's patients at member practices outside the Clun Valley network on 31 December 2026 | filed (specification section 3); SF3 |
| 2 Unit of account | the patient; harms a year | filed; SF9 |
| 3 Attribution window | eligibility on the six months to 31 December 2026; letters by the half of first receipt (ask A); consultations by quarter of the consultation (ask B) | filed (protocols; the asking sentences); SF1 |
| 4 As-of dating | age and registration on 31 December 2026; the receiving practice (ask A); registration on the day of each consultation (ask B) | filed (specification 3.2, 3.3, 4.1); asserted |
| 5 Version basis | the pilot's six-month row | filed (pilot log header); SF11 |
| 6 Denominator | eligible patients; registered patients at the start of each half or quarter for the asks | filed (asking sentences) |
| 7 Weighting | each patient once at their own chance and age | filed (specification section 3) |
| 8 Window length | 183 days for off; the provenance window converges from 30 to 180 days | filed; SF2, SF5 |
| 9 Boundary inclusivity | 31 December 2026 inside; no course begins on a window edge | asserted |
| 10 Rounding path | once, from the unrounded sum | SF13 |
| 11 Tie-break | none needed: margins exceed 1.2 times | asserted |
| 12 Maturity and censoring | every pilot patient has six months of follow-up by 31 December 2026 | asserted |
| 13 Order of operations | conform, classify, carry, weight, sum | asserted |
| 14 Row order | none | asserted |
| 15 Duplicate resolution | the six-month row; a re-sent letter once, at its first receipt (ask A); a hub appointment and its practice-system record once (ask B) | forced by identity; asserted (K3, K4, K5) |
| 16 Identity normalisation | pseudonym, the hospital-number lookup, dm+d names | the systems' own keys; SF7 |
| 17 Netting against gross | none | n/a, asserted |
| 18 Dimensional units | patients and harms a year | filed |
| 19 Code and status semantics | the protocol codes, the recommendation words | the protocols' own code lists |
| 20 Integerisation | whole patients and harms printed from unrounded sums | SF13 |
| 21 Clause scope | the specification's population binds the call only | filed scope |
| 22 Forward window contents | the eligible patients on 31 December 2026 stand for 2027's reviews | filed (specification section 3) |

## Literal reader

Executed word for word, the specification asks for the sum over the eligible patients outside the Clun Valley network
of each patient's chance of being off six months after review times the harm rate at their age; the protocols fix who
is eligible and the pilot supplies the evidence for each patient's chance. A literal reader who estimates each
patient's chance from the pilot's outcomes for patients like that patient files the golden once the pilot is split by
provenance, because that is the only attribute the pilot's take-off depends on; the pilot's average is the easy method
on the same literal estimand, not another reading of it.

## Oracles

None on the main call: no file carries a federation-wide take-off, a provenance share or a harm estimate for any
review, and the close-out's rates are the pilot's own. The verifier (generator/verify.py) recomputes the call, every
figure and both asks with pandas from target/ alone.

## Ask sheet

Two asks on records the call never reads: the hospital medicine letters the practices received in 2026 (ask A, in the
paper) and the pharmacist team's 2026 consultations (ask B, the csv). Ask A counts every medicine letter any member
practice received in 2026, about any patient; ask B counts consultations. Neither touches the protocols' searches,
the courses, the pilot or the six-month rule.

**Ask A, the hospital medicine letters each network's practices received in each half of 2026, per 1,000 patients
registered at the start of the half (10 figures, one decimal).**
- H18 home: the board sizes the medicine-letter workload each network's practices carry before committing the
  pharmacist team to a review.
- Primary 1 (D1 and D2, one letter under two reference schemes): the mental health trust's April 2026 system change
  sent its outage week's letters on 7 April for the first time and re-sent the four weeks before under the new
  system's references, every one dated 7 April; a re-sent letter is the earlier letter, received first in March, and a
  held one is new, and only its content (patient, service, encounter date, lines) tells which is which. Keeping the
  batch moves every first-half figure by 0.60 to 0.74; dropping it moves them by 0.15 to 0.38.
- Primary 2 (D7, the true key elsewhere): from October 2026 the hospital trust's documents arrive through GP Connect,
  and the workflow log carries the message id for a reference and the message's own date for the document date, so a
  letter's receipt is found only as the next receipt from that sender for that patient. Re-keying on patient, sender
  and document date, or falling back to the letter date, moves every second-half figure by 1.3 to 18.
- Hazards: letters dated over Christmas received in January (the asking sentence's received basis), one row per
  medicine line, two date formats, hospital-number-only letters, merged practices' old codes.
- Pin test: the sentence pins the basis (received), the population (letters its practices received; specification
  4.3 files both trusts' letters as hospital medicine letters) and the denominator (registered at the start of the
  half, specification 4.2); both devices sit where the pins leave open which records are one letter and which receipt
  belongs to which letter.

**Ask B, each network's patient consultations with the team in each quarter of 2026, per 1,000 patients registered at
the start of the quarter (20 figures, one decimal).**
- H18 home: the board checks every network's patients had pharmacist time in 2026 before committing the team to one
  review across them.
- Primary 1 (D1, one appointment under two systems): hub pharmacists write a hub appointment into the patient's record
  at the 16 shared-record practices, on the day or the next working day, under the practice system's own id and the
  time of writing; the hub's export stamps its slots in UTC. One appointment is one consultation, and matching on
  patient and day leaves every next-day record standing: 0.41 to 1.07 per 1,000 too many in every figure.
- Primary 2 (D6, an event's quantity one grain below): a group medicines review is one hub booking with no patient,
  its patients in the group session register; specification 4.1 counts each patient at a group review. One per
  session misses 17 of 20 figures by 0.13 to 0.45.
- Hazards: did-not-attend and cancelled bookings, UTC, registration on the day for hub patients, genuine same-day
  call-backs at the practice (an over-matching trap for a patient-and-day key).
- Pin test: the sentence pins the unit (patient consultations, defined in 4.1, a patient counting towards the
  network of their practice on the day of the consultation), the denominator and the quarter; neither device's
  handling is named.

Main population zero-counts: no device row (a 7 April letter, a GP Connect receipt, a hub record, a group booking)
touches a protocol search, course, pilot outcome or provenance relation the call reads; dropping the whole 7 April
batch leaves every patient's provenance and the call unchanged (checks.py K6).

| The cracker (landed the call, ran the hygiene battery, executed every filed rule) | Verdict |
|---|---|
| A, 10 letter rates: receipt through the reference join, GP Connect re-keyed on patient, sender and document date, the 7 April batch dropped as a re-send | miss |
| A, the same with unmatched receipts on the letter date, or the batch kept | miss |
| B, 20 consultation rates: hub and practice records matched on patient and day after UTC conversion, attended group patients counted | miss |

The full includer (a stress row, outside the gate) matches each GP Connect receipt to the letter it follows, keeps the
first-time letters in the 7 April batch and matches a hub appointment to the same pharmacist's record on the next
working day: it keeps all 30 and scores 100 on the call; with the best miss off the call at 12, that pair is 56.

Pair ceiling: 28.5 (the cracker keeps 0 of 30 ask figures: 45.0 on the call, the mirror 12.0 off it)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack)

## Stage 4

Final cut: target.zip 0bacf975 (two byte-identical builds; checks.py 99 of 99, verify PASS, figures_check 88 of 88,
precut 61 checks with no FAIL or WARN, voice-check PASS, container audit clean on target and golden, pair ceiling 28.5).

leak.py on the final cut: REVIEW, no LEAK. Each line ruled:
- Sweep 3, the protocols and the specification carry the call's wording: it is review B's own name as both file it,
  and every review's name appears alike; harmless.
- Sweep 4, the close-out, the protocols and the specification carry four to seven stump-paragraph terms (antipsychotic,
  practice, programme, checks, outside, letter): the field's nouns, the specification's population and its section 4.3
  reporting line; none names specialists or who started a medicine (checks.py R1, which also holds letters to that one
  sentence); harmless.
- Sweep 4, a prompt sentence carries task nouns (practices, medicine); harmless.
- Sweep 6, the falls admissions file names the five networks beside numbers: the networks are the asks' units, not the
  decision's candidates, and the file prices no review; a declared distractor; harmless.

guard.py heart PASS and surface exit 0 on the final cut; surface promoted 8 pairs for the author's adjudicated clone
check (task304, task305, task307, task308, task310, task467, task169, task128), each on shared card axes (population
gap, pick_one_of_n, the pilot log as calibration) or batch-level surface; the card carries differentiation lines
against task304 and task128. Personas in the pack: the card's three.

Pending: the isolated leak reader and the determinism judge (both Sonnet at medium) were not run in the building
session, which had no Agent tool. Their briefs were written against target.zip 0bacf975; the build ships only after
both reports are in and every finding is fixed in the generator.

## Tried and rejected

- Pack 1 of the prototype (2026-10-24, seed 3061) hid each imported car's pack history before its Dutch registration (the log started at the Dutch registration), so a solver could not know an import's pack state and both probes repaired it differently (sonnet calibrated the imports down by 0.74, opus modelled the abroad replacements in expectation): a fork, not the stump. The log is now the OEMs' EU-wide record plus Voltwerk's own, and a car whose pack failed outside warranty abroad is scrapped there and never imported.
- The prototype's truth carried a scrappage and export rate that no file shows; the forecast now takes a car in use to stay in use through 2027, filed in the tooling plan.
- The first cut's imports arrived about six years old, inside the eight-year warranty, and moved the call by three per cent and one lot; the Mira city car is now the platform kept alive by old imports from abroad, as old cheap EVs are.
- A refurbished pack failing inside Voltwerk's two years was logged as an OEM warranty fit in the prototype (99 rows): fixed, a Voltwerk-warranty failure takes another refurbished pack under Voltwerk's cover.
- The first stage-2 world kept the Mira city car launched in 2014 with 520 imports a month and an eight-year warranty: its arrival stream still ramped through the replay windows, so the 6- and 24-month windows spread the Mira's forecast by 51 and the total straddled a hundred bin. The Mira is now launched in 2013 with a five-year warranty and a steeper wear-out, its stream flat over the last 36 months and its imports arriving as survivors on their original packs.
- An estimand counting only failures outside both warranties left out the packs Voltwerk itself replaces under its two-year warranty, which the line supplies too; the plan now counts every failure outside the OEM warranty.
- Grading each platform's forecast paid the wrong route: the register-only route files four of the five platforms' forecasts at the nearest hundred (only the Mira moves); the prompt grades the slots and the total.
- Ask B's re-keying first moved the naive share by under 0.1 point on the Volta hatch, the new ids passing at about the platform's own rate; the BMS is now replaced in seven reworks in ten and the line seed (31062, from 750 swept) keeps every platform's natural read and over-repair outside its bin on all three asks, worst golden edge 0.155 of a bin.
- The dealer rows of the replacement log first carried plates typed with dashes; a solver who joined without normalising them filed Mira 1,350 and Volta 1,000, so that mess could move the call (dataset-generation R2) and was cut: both sources now carry the register's own plate format.
- Ask C's first device, dock 2 setting its rejects aside without scanning them (absent from the intake export, present at the recycler without a core code), was landed 5 of 5 by the stage 4 reader: dock 2's zero rejects and the blank core codes sit on the path of anyone counting rejects, and the judge found the dock's practice stated in no file. Re-sited onto the grade's date (D2): the intake export carries each core's grade on 1 July 2026, so a core the line built on and scrapped reads AFGEKEURD, and only its work order in the MES shows it passed intake; every ask C figure is unchanged.
- The plan's "a car in use in the Netherlands is taken to stay in use through 2027" read to the stage 4 reader, and to the judge as its one soft spot, as freezing the register of 30 June 2026; the sentence now places the car in 2027 ("a car in use in the Netherlands in 2027 is taken to stay in use for the rest of the year"), the population the estimand already files, and names no import.
- The portal returned the build on determinism (both judges: Gates C, D and E, underspecified_objective, A, B and G passing): the plan as shipped named the register as its only source and its only dynamics clause was about exits, so both judges forecast the register of 30 June 2026 alone (3,448, 3,500 with a judge's renewals), and a judge also summed ask A's batch lines as written. Pinning the population to the register was refused (it makes the judges' answer the golden and spends the stump), and filing the projection (a twelfth a month at the trailing rate, mix and age) was refused (rule application, CLAUDE.md rule 3). Closed instead by the WHAT at authority: plan section 3 files the fleet of 2027 as the register and the cars first registered here from 1 July 2026 to the end of 2027 (SF25) and one pack per car (SF26), the projection left open and forced by C1 over 144 projections, and the line notes file the lot stock rule for ask A (SF27); no graded or stated figure moved (freeze.py). The cost: that the later registrations are in the fleet is now readable, so the decisive rung keeps only what no sentence says, which of them fall due; the default path's answer is now the easy route's on the literal estimand (the later registrations carried as new cars).
- 2026-10-31, architecture 1 spent at the batch 1 triage: shipped 10-24 and reshipped 10-26 after the portal's determinism block, its isolated cold reader reproduced the call cell for cell (Volta 900, Kestrel 250, Plover 350, Mira 1,450, Tern 50, 3,800) and named the decisive step a procedure, since the repair's population sentence and the plan's pack-age sentence read together as the method; the surviving risk the note recorded was that conditioning a survival curve on survival to the as-of date is reflex reachable. Re-rooted in a new world rather than hardened.
- 2026-10-31, re-root screen before this draw: an actuarial reinsurance-capital draw (a county mutual's 2027 windstorm programme, the vendor's year loss table loaded storm by storm for demand surge read off the market's index loss) cleared `guard.py check` and was set aside unregistered, because task309 (FORTIFIED roofs, one cut ratio across storms that varies with gust intensity, carried through a vendor event set) is the same insight in the same domain; regression to the mean in a health-services pilot and a healthy-adopter uptake were set aside as general statistical mechanisms readers name unprompted (task308's screen of six); stale-priced returns in a portfolio's risk budget were set aside as task135's cross-day covariance.
- 2026-10-31, architecture 2 (the development corporation's 2027 inward investment award between a logistics hub on the city region's boundary and an inland food plant, the induced round read where each project's staff live) drawn, registered and spent at stage 2 before any data was cut: the survivor anatomy's Actor test failed on paper, since where the hub's staff live is one join from a column (a roster postcode against the postcode directory's local authority), and every honest way to ship it (a roster, a travel plan's postcode survey, a commuting flow for the depot's zone) is a column or a sentence that sends a solver to it; the IO world offered no relation between rows that carries the induced round's leak.
- 2026-10-31, architecture 3 first cut (an occurrence cover against an annual aggregate cover): the two covers' releases separated by about 1.12 times under every loading of the storms, so no costing of the record moved the call; redesigned at stage 2 into the second-event cover, buy or not, on the occurrence cover's retained band.
- 2026-10-31, the second-event cover on the 50th worst year alone, an upper layer above the occurrence cover and a tall tower from 12 to 60 million were each priced: the single year was noisy enough to flip on the seed, the upper layer's release was small and noisy, and the tower closed the gap between the cheap routes and the golden; the capital policy's average of the 50 worst years and the 7.5 million xs 4 million band were kept.
- 2026-10-31, the first record draw (seed 498): the ratio of totals over the later storms of each season landed the call (worth plus 0.13 million) with the golden's release, and the mean of ratios over the later storms of each year landed it too; a stormier physics with more trains a season made the rank routes buy harder, and shifting a year's first train to clear the year end left nine gaps of exactly 70 days and one inside the window corridor. The record is now drawn with trains kept apart across the year end and searched over 7,500 seeds for one where every rank, year, season, size and pooled route under every estimator files the wrong call (seed 2703, worst route minus 0.06 million).
- 2026-10-31, an exposure ask on the home book (sums insured in force by county) was set aside: in-force by date, renewal terms under new numbers and lapses are rule application a careful solver executes, with no reconstruction left after noticing; the home extract ships as a distractor and the farm book carries the exposure ask.
- 2026-10-31, a reopened claim's further damage first came to some claims before they had been notified, which no claims system allows and which left the pairing of lines and instructions unrecoverable for those claims; further damage now comes only to a claim already open with its adjuster instructed.
- 2026-10-31, architecture 3 (Penwarden's second-event windstorm cover for the county mutual) spent at stage 4: the FIX_NOW failed its second pass. Pass 1 (DETERMINISTIC, FIX_NOW) found "worth" in two senses, cover B's one reinstatement missing from the working and the coinsurance share unpinned, all fixed; pass 2 (DETERMINISTIC, FIX_NOW) found the 2026 storms asks open, since 379 reopened /R1 claim lines with no instruction of their own took their original claim's instructed damage day in the golden, a rule filed nowhere, and the lines' own loss_date filed a recovery of 11,881,000 against 12,015,000. The main call (follow-on storms costing 1.62 times the model) held throughout. The lesson carried forward: a reopened, re-sent or amended record's date or owner is filed or unmistakable before any ask counts it. Reports kept as determinism_check_report_arch3.md and determinism_check_report_arch3_pass2.md.
- 2026-10-31, architecture 4 at its stage 4 judge (NOT_DETERMINISTIC, reconciled FIX_NOW): the call held in every variant, but the runner-up, the gap and the kept alpha moved with the curve's exponent (momentum 3.91 to 5.88 between 0.7 and 0.4), its weighting, a common intercept across the bands, the consolidation day left as a return and the ESG names dropped, because the desk's orders sat almost all under 3 per cent of a stock's day (1.2 per cent were event trades) and the data did not separate the forms (R2 0.4655 against 0.4630); the ESG list also took effect inside the log (15 January 2026) while 101 rebalance rows still traded listed names. Repaired in the generator, the call and the decisive step unchanged; the judge's verdict kept as determinism_check_report_arch4.md.
- 2026-10-31, the first repair raised liquid event trades to a tenth of the desk's orders (4 to 60 per cent of the day): the family converged, but those orders carried most of the desk's traded pounds, so the value-weighted band averages (57, 75 and 115 bps) converged on the curve and filed UK Mid Cap Value, and the default path no longer ended wrong. Rejected.
- 2026-10-31, kept: participation comes from thin names, as it does on a desk. Each lower band carries a tail of thinly traded names (52 in the FTSE 250, 100 in the SmallCap), where the books' ordinary orders, sized in pounds and scaled only mildly with liquidity, take a fifth to two thirds of the day; the desk's pounds stay in liquid names at about one per cent, so the band averages still file momentum (by 2.7 million) while about 1,550 small-cap orders above a tenth of the day pin the curve where momentum trades. The 12 least liquid small caps, which no book or candidate trades, carry the consolidations; the ESG list predates the log and no book or candidate trades a listed name; the books' orders begin on 1 April 2025 with 60 sessions of history; the Severnvale transition trades large and mid caps only, at five orders a day.
- 2026-10-31, a tail of 130 thin small caps was dropped: it left momentum's investable pool (5 million a day or more) too small to swap 18 names a month, and its kept alpha fell to under 1 million.
- 2026-10-31, a common intercept across the bands was not chased: the half-spread differs by band (3, 8.5 and 25 bps), so one intercept misprices each band's trades by 0.5 to 2.2 million, which no rounding bin absorbs; IC-07 now files the population a cost is estimated from (the desk's executions in the candidate's index band), the WHAT, and the golden fits band by band. A lower shortfall noise and a narrower or wider spread of order sizes were screened and left the family's width unchanged (it is form error, set by where the desk's orders sit), so the order sizes' spread was set at 0.6 for the wider stump margin.
- 2026-11-07, architecture 4 (Wealdmoor's GBP 400 million to one of three backtested UK strategies, the alpha each keeps once its rebalances are priced at that size) spent on its first portal round, FAILED_TO_STUMP: both responses filed the golden exactly (UK Mid Cap Value 8, UK Large Cap Quality 6, momentum 5, gap 2) by the field's own textbook, a per-band fit of shortfall on volatility times the square root of participation, validated on a July to November holdout where it beat the flat band costs (RMSE 13.6, 8.5 and 18.9 bps against 26.6, 12.7 and 40.2), so the data revealed the right method by fit; both also took all 24 ask figures, since the failover merge and the block allocation were filed in TCA standard section 1 and the allocation export. The participation-dependent cost carried to size is what a careful analyst executes by reflex; the market-impact world, the capacity driver and the which shell are spent.
- 2026-11-08, re-root screen before architecture 5 (paper only, no harness): a retention trial's spillover through referral or household ties (task127's reserved credit contagion is the same insight, and task131 v1 shipped household interference); an outpatient follow-up rollout netted of GP re-referrals and a DNA programme credited only with avoided rebookings (the first is a hidden overlap the author's lesson says both responses find, the second is one group-by once thought of); theatre overrun cancellations traced to a late start from the first patient's admission (task130, task111 and task137 screened the knock-on as a reflex); line infections split insertion against maintenance by days since insertion and an IV-to-oral switch netted of unswitchable courses (the options' own names announce the class, and the IVOS criteria are filed nationally); broadband full fibre's churn benefit by copper line length (the line's sync speed is one join from a column).
- 2026-11-08, architecture 5's first registered draft (a ward deterioration service, e-obs alerting with critical care outreach, validated at about a 43 per cent cut in arrest calls in two directorates and carried to an uncovered directorate whose arrests mostly had no e-obs escalation in the day before): rejected before registration on the abstraction sentence, because it is task258's insight in clinical nouns (a validated effect that works only through a per-unit precondition every past application met, carried to units that lack it, visible only by a join), and the guard put its structural signature on task127 v2 (the landed concurrent wait); the antecedent-arrest analysis is also the rapid-response literature's own (MERIT, NCEPOD), so a careful response would execute it.
- 2026-11-08, a shared-care rule filed in the federation's policy (practice pharmacists may not stop a specialist-started medicine without the specialist's agreement): rejected, because with the rule filed the decisive step becomes identifying a class from records under a filed rule, which is rule application; the provenance effect is left to the pilot's own outcomes.
- 2026-11-08, ask A first counted letters about each network's registered patients, the hospitals' stale practice
  field the device: the registration date (the letter's, the receipt's or the half's start) was unfiled, a fork, and
  filing it pinned the device; re-sited onto the letters each network's practices received, the asking sentence's own
  basis, with the devices in which records are one letter and which receipt is whose.
- 2026-11-08, the first GP Connect rows carried the letter's own date as the document date: the hygiene battery's
  re-key on patient, sender and date found every receipt and the cracker kept all five second-half letter figures.
  GP Connect messages carry their own send date, which the workflow log now holds.
- 2026-11-08, harms first graded to one decimal: a carry stratified by provenance and age band moved the antipsychotic
  review by 0.3 harms, so harms are whole numbers and patients the nearest 10, the precision the pilot carries; the
  specialist-started pilot patients who came off are the ones whose age band and sex leave the stratified carries
  inside those bins (checks.py M5), each review's rate unchanged (1 of 24, 1 of 24, 2 of 48).
- 2026-11-08, an initiation letter typed in the mental health trust's outage week went out in the 7 April batch, so a
  response that dropped the batch for ask A lost those patients' provenance on the call: such courses now carry the
  hospital trust's letter, and no initiation letter is held (checks.py K6).
- 2026-11-08, the first cut's gabapentinoid pool took 37 extra patients from texture opioid users overlapping texture
  gabapentinoid users, and palliative-care and epilepsy texture patients drawn from other reviews' pools left the
  protocol short of the truth by one or two: texture is now drawn outside every pool, and the protocol finds exactly
  the truth's patients (checks.py T1).
- 2026-11-08, read as a literal judge before stage 4: the close-out's take-up sentence (94 per cent of invitations)
  invited multiplying each chance by take-up, which moved review B to 11 harms and 270 patients; the sentence is gone
  and specification 3.2 files that the team reviews every patient in scope. Ask B's network read at the quarter's
  start moved 7 of 20 figures (newly registered patients drop out); specification 4.1 files the day of the
  consultation. "Hospital medicine letters" could be read without the mental health trust; specification 4.3 names
  both trusts. None names a device.
