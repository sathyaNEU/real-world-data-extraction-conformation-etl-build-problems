# task265 design note

Architecture 1, drawn 2026-10-17 (wave 3, Descriptive lane, sathay3012). Seed DA15's connected-TV world was worked at the draw and set aside (`## Tried and rejected`); the slot draws a new world in the same objective. Brennick Valley Health, a regional health system in Wisconsin with three hospitals that replace hips, renews its hip implant contract on 1 July 2027. Its Implant Value Analysis Policy keeps a hip construct (one femoral stem with one acetabular cup) on the contract only if the system's own joint registry shows no more than 5.0 per cent of the construct's implants revised within ten years of the operation. The Brennick Valley Joint Registry began capturing every primary hip operation on 1 January 2018; hips replaced at the system before then were enrolled from 2018 to 2021 when their patients came to a registry follow-up clinic, so a hip done earlier is in the registry only if it had not been revised by the day it was enrolled. The value-analysis committee settles the contract list at its May 2027 meeting from the registry extract of 31 December 2026. The call is retrospective in its quantity (ten-year survival of hips already operated on) because the policy's benchmark is defined on observed ten-year survival; the contract it decides runs forward to 2031.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task265.json`, architecture v1, registered 2026-10-17, the set-aside connected-TV draw kept in its lineage with its fate. The system is a health provider (`hospital_or_health_provider`); the value-analysis committee decides (`committee_or_panel`); the contract renewal forces the decision (`purchase_order_or_contract`); the requester is the orthopaedic service line's outcomes analyst working for the committee (`procurement_lead`, value analysis sits in the system's supply chain); the context artifact is the registry's data-management log (`operations_log`); no calibration organ. `guard.py check`: WARN only. `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, task464 and five others in the last twelve): the label is shared, the mechanism is not (task464 places old scores on a new scale through a bridge study; here a survival curve needs delayed entry); no other Gate G key is honest for two standard Kaplan-Meier curves between which the record's own enrolment design chooses. `repeat.question_form` (which, against task155 and task464): the decision is a set of constructs to keep, so the question is which. `test.same_driver_older` is differentiated on the card against task139 and task452, and the card also differentiates task255 (truncation in the size of a loss) and task133 (a filed curve carried forward for units already partway through it).
2. Pairing: Biomedical & Clinical Research (client domain) / survival-time-to-event-analysis / Descriptive & Distribution Analysis. The task type's own object, an implant's revision-free survival estimated by Kaplan-Meier from a joint registry, decides the call; the setting is a health system's implant contract.
3. Niche: a single health system's joint registry, prospective from 2018 and backfilled by clinic enrolment for hips done from 2005 to 2017; six constructs in use across those years, two of them (an uncemented stem with its own cup, and the same stem with another maker's cup) used mostly before 2018 and so carried in the registry's ten-year range almost wholly by legacy hips.
4. Call and shape: the set of constructs that stay on the contract (`designation_set`, question form which). Shape 14 (cuts of a distribution): six constructs, each with its cumulative percent revision at three, five, seven and ten years, the ten-year cut deciding.
5. Gate G `method_or_model_selection`, strategy key `population_selection` (who is in the risk set: legacy hips are in the registry only as survivors of the years before it began), decisive generator G9 (the recorded population is the one that survived to be recorded), then G16 (which curve the record's design entitles) and G17 (supporting: the ten-year estimates' distance to the 5.0 per cent bar).
6. Data-native sentence: the registry met every hip done before 2018 only at a follow-up clinic between 2018 and 2021, and a hip revised before that visit was never enrolled, so every legacy hip arrives already free of revision for the years since its operation and can tell the curve nothing about those years.
7. Sources, one line each:
   - The two-layer design reference's `estimation_fit` family (censoring and truncation; survivorship): a survival curve from a record that admits units late must start each unit's risk at the time the record first saw it.
   - The client library's event-history pattern 4 (late entry needs left truncation; shortcut: the clock from the origin): this build's pattern is `own:legacy-enrolment-left-truncation`, the late entry made by a registry's backfill design rather than by an age at entry.
   - The client library's survival-time-to-event patterns (competing deaths; response landmarks): the policy files deaths as censored, so the competing-risk route is closed by the standard, not left as a fork.
   - task255 in this lane (severity fitted through each claim's deductible and retention): truncation in the size of a loss; here the truncation is in time and decides which hips the risk set holds at each year since surgery.
   - task133 (a filed cumulative curve carried forward for units that have already survived part of it): applies a known curve conditionally; here the curve itself has to be estimated from survivors.
   - task264 in this lane (visit-intercept weights): a selection proportional to frequency; here no weighting, the selection is survival to enrolment.
8. People, drawn with `guard.py names --geo "united states" --seed 265`: Melinda Boyd (the registry manager, author of the registry's data dictionary and data-management log), Richard Hart (the system's director of value analysis, who chairs the committee and owns the policy), Sara Gray (the orthopaedic outcomes analyst). Invented names (the health system, its registry, its three hospitals and their towns, the four implant makers and their stems and cups) are screened in `checks.py` against a near-miss register of US places, Wisconsin health systems and towns, and real orthopaedic implant makers and hip and knee brands (H21), with every name the draw first carried swept from the pack.

## Default path

1. Read the policy: a hip construct stays on the contract if its cumulative percent revision ten years after the operation, estimated on the registry by Kaplan-Meier with deaths and loss to follow-up censored, is 5.0 per cent or less; a revision is any operation that adds, removes or replaces a component.
2. Stack the registry's prospective export and the legacy enrolment workbook; map each hip's stem and cup catalogue numbers to its construct through the registry's crosswalk; keep one record per hip.
3. For each hip, the time from its operation to its first revision (the event), or to death, last contact or the extract date (censored).
4. Fit Kaplan-Meier for each construct from the operation date and read the cumulative percent revision at ten years.
5. Keep the constructs at 5.0 per cent or less.

Ends on: five constructs stay, Edvalt/Kelvarne at 3.1 per cent revised by ten years and Edvalt/Pellvoro at 3.2 (built).
Golden: three constructs stay (Askvane/Quarvel 3.7, Holbrin/Pellvoro 4.1 and Askvane/Pellvoro 3.5 per cent); Edvalt/Kelvarne at 7.0 per cent and Edvalt/Pellvoro at 5.7 go off the agreement with Kalvoran/Morvenne (7.6) (built).

## Stump sentence

The default path keeps Edvalt/Kelvarne and Edvalt/Pellvoro on the agreement at 3.1 and 3.2 per cent revised by ten years, because it counts each hip enrolled at a 2018 to 2021 registry clinic as at risk from its operation, so the years before its enrolment, in which any revision would have kept it out of the registry, enter the curve as revision-free; admitting each legacy hip to the risk set at its enrolment puts the two constructs, whose ten-year evidence is almost all legacy, at 7.0 and 5.7 per cent and off the agreement.

## Three rules

Task type: survival-time-to-event-analysis (Biomedical & Clinical Research), which serves Descriptive & Distribution Analysis in the taxonomy; the setting is a health system's hip implant contract.
Domain test: the deciding quantity is each construct's cumulative percent revision ten years after the primary operation, the joint registry's own Kaplan-Meier estimate with deaths censored, worked with left truncation (delayed entry) for hips enrolled after their operation; replacing it with the crude share revised, or with the same curve clocked from the operation for every hip, changes which constructs pass.
Swap: "which of six washing machine models stay on a retailer's range by the share still working ten years after sale" keeps a survival curve and a bar, but loses the registry that enrolled earlier implants only at a follow-up clinic with the hip still in place, the revision of a component as the event and the deaths censored under the registry standard, so the delayed entry the call turns on has nothing to attach to and the task no longer reads the same.
Layer 1: the registry in two exports with different layouts (the prospective capture from 2018 and the legacy enrolment workbook kept by the 2018 to 2021 clinics); stem and cup catalogue numbers, one maker's re-coded in 2020, mapped to constructs through the registry's crosswalk; bilateral patients with two hips on file, each hip its own record; deaths from the state death-index linkage, some with month and year only; dates written three ways across the exports and the visit log; follow-up visits logged at each hospital's clinic with patient and hip keys in the hospital's own format. Each is how the registry and the hospitals' systems hold their records; nothing is placed to be caught.
Layer 2: estimation_fit (survivorship and truncation): the legacy hips are in the record only because they survived unrevised to their enrolment, so the survival curve must admit each one to the risk set at its enrolment and not at its operation; the choice moves the ten-year estimate of every construct with legacy hips and flips the two constructs whose ten-year evidence is almost all legacy.
Decisive step: left truncation, delayed entry of each legacy hip into the Kaplan-Meier risk set at its enrolment visit, so that the years between its operation and its enrolment count neither as exposure nor as survival.
Not semantics: an analyst who reads every column, code and note correctly, including the data dictionary's statement that hips done before 2018 entered the registry at their first registry clinic visit, still has a correct date for each operation, revision, death and last contact and still fits the standard Kaplan-Meier from the operation date, which every field supports; nothing in a field is misread on that route, the error is in which hips the curve treats as at risk in the years before the registry saw them.
Not rule application: the policy files the estimand (cumulative percent revision ten years after the operation), the standard curve (Kaplan-Meier) and the censoring of deaths and loss to follow-up; no filed rule says when a hip enters the risk set, and executing every filed rule on the default path files the five-construct list.
Analyst test: a strong analyst who reconciles the two exports and the crosswalk, counts every hip separately, censors deaths and loss to follow-up as the policy files and runs Kaplan-Meier from the operation date for every hip ends on the default path's five constructs, Edvalt/Kelvarne at 3.1 per cent and Edvalt/Pellvoro at 3.2 kept, because those hips are in the registry only because they had not been revised when they were enrolled.
Estimand: the Implant Value Analysis Policy (section 4, shipped as the committee's policy document) files the population (every primary hip operation of the construct at the system's hospitals), the outcome (first revision, any operation adding, removing or replacing a component), the time (ten years after the operation, from the registry extract of 31 December 2026), the unit (the hip) and the comparison (5.0 per cent cumulative revision, Kaplan-Meier with deaths and loss to follow-up censored).
No decoy: no memo, draft, briefing, vendor claim or stakeholder figure argues for a construct or states a ten-year rate; the manufacturers' brochures are not shipped, and no national registry's published rate for these constructs exists, since the makers and constructs are fictional.
No certified replay: the method is not hidden behind published or certified figures; no shipped file states any construct's revision rate, and the policy names the standard curve outright, leaving the delayed entry to the analysis.
Lesson: a registry that took in older implants only when their patients came back with the implant still in place holds those implants as survivors, and a survival curve that clocks them from surgery counts years it never observed as years without failure; no build on file teaches delayed entry in a survival curve (task255 truncates the size of a loss, task133 carries a known curve forward for units already part way through it).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the crude share of each construct's hips revised | the policy names Kaplan-Meier with deaths and moves censored | none | dividing revisions by hips is the first move | none | none | one ratio per construct | readable |
| R1 Kaplan-Meier from the operation for every hip (the default path) | no sentence names an entry time; the policy's "ten years after the operation" reads as the clock for every hip | operation date in both exports | the standard registry curve from surgery | none | none | none | readable |
| R2 legacy hips at risk from the registry's start (1 January 2018) | the dictionary says each legacy hip was entered at its patient's first registry clinic visit (enrolled_on) | the enrolled_on column | delayed entry at the record's start is the textbook first fix | none | none | none | readable |
| (decisive) each legacy hip at risk from its enrolment visit | none: the policy files the estimand and the curve, the dictionary says when each hip was entered and what the registry links; no document speaks of a risk set, an entry time, truncation or the years before a visit | enrolled_on is one of eighteen workbook columns and has a plain registry meaning (the visit date), read by the default path as provenance | KM from surgery, the crude share and a prospective-only curve are the reflexes; none uses enrolled_on as entry | no published or certified rate for any construct; nothing ties to a ten-year figure | keys unique, exports join one to one through the crosswalk, every catalogue number maps, nothing for the battery to find | a product-limit over risk sets that change composition each year, no ratio of shipped figures | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | construct | one femoral stem family with one acetabular cup family, the six on the agreement as the crosswalk maps them | the stem alone, or the maker | other groupings, no bar for them | the policy's "one femoral stem family with one acetabular cup family" and the agreement's schedule of six |
| SF2 | revision | the first later operation that adds, removes or replaces any component of that hip, at a system hospital or at another Wisconsin hospital through the state's discharge data | aseptic revisions only, or every revision counted | fewer events, or a hip counted twice | the policy's "any operation that adds, removes or replaces a component" and "first revision"; the dictionary's linkage note |
| SF3 | time | years since the primary operation of that hip | calendar time, or years since the registry first saw the hip | no ten-year cut | the policy's "ten years after the operation" |
| SF4 | deaths | censored at death | a competing risk (cumulative incidence) | lower figures | the policy's "Kaplan-Meier, deaths and loss to follow-up censored" |
| SF5 | out-of-state moves | censored at the move date | followed to the extract | four figures move by 0.06 to 0.12 at one decimal, same call (asserted) | the policy's "Deaths and loss to follow-up are censored" and the dictionary's "the registry loses follow-up of a hip when its patient moves out of the state" |
| SF6 | unit | the hip, each side of a bilateral patient its own record | the patient | patients with two hips counted once | the policy's "the hip" |
| SF7 | population | every primary total hip of the construct at the three hospitals on the registry, prospective (2018 on) and legacy (2005 to 2017) | prospective hips only | no ten-year estimate (follow-up ends at 9.0 years) | the policy's "every primary hip operation of the construct at the system's hospitals", with no date limit |
| SF8 | as-of | the registry extract of 31 December 2026 | a later date | none available | same call: no later record ships |
| SF9 | the bar | 5.0 per cent or less stays | under 5.0 stays | same call | same call: no construct within 0.4 of 5.0 (asserted) |
| SF10 | ten years | 3,652.5 days | the tenth anniversary, or 3,650 days | same call | same call: no revision on day 3,651, 3,652 or 3,653 for any construct, and the 3,650 and 3,653-day horizons give every figure at one decimal (asserted) |
| SF16 | follow-up end | death, move out of Wisconsin or the extract, revisions found through the registry's forms and the state's discharge data | the last registry clinic visit | lower figures, a hip's later unseen years dropped | the dictionary: revisions are recorded from the registry form and the quarterly discharge-data linkage, whether or not the patient attends clinic |
| SF11 | death dates given as month and year | the 15th of the month | the 1st or the last day | same call | same call: no revision in the month of a month-only death, every figure equal at one decimal under each (asserted) |
| SF12 | catalogue numbers | old and new Thorvik numbers both mapped through the crosswalk | numbers absent from the main column dropped | Askvane constructs lose hips | the crosswalk's two number columns; every number maps (asserted) |
| SF13 | ties | events before censorings at equal times, entry exclusive | either order, entry inclusive | same call | same call: every figure equal at one decimal under each (asserted) |
| SF14 | a legacy hip's start in the registry | enrolled_on, the visit at which it was entered | 1 January 2018, the registry's start | R2 | the dictionary's "entered at the patient's first registry clinic visit, from 2018 to 2021" |
| SF15 | primary total hip | the first arthroplasty of that hip with a stem and a cup | hemiarthroplasties and conversions included | none on the registry | same call: the registry holds primary total hips only (asserted: every hip has a stem and a cup) |

## Ladder

Built from the shipped pack (asserted in `checks.py`, recomputed by `verify.py` on its own product-limit code); seed 6543 of the registry's simulated process (hips per construct and year, revision hazards highest in the first year, deaths rising with age, moves out of Wisconsin at about 0.6 per cent a year, about 55 per cent of surviving unrevised earlier hips enrolled at clinics that ran at Tollefson Lake in 2018 and 2019, at Brennick Valley Medical Center in 2019 and 2020 and at Kittelstad from July 2020 to December 2021, the pandemic pause excluded). Ten-year cumulative percent revision:

| Rung | Construction | Edvalt/Kelvarne | Edvalt/Pellvoro | Askvane/Quarvel | Holbrin/Pellvoro | Askvane/Pellvoro | Kalvoran/Morvenne | Stay | What kills it |
|---|---|---|---|---|---|---|---|---|---|
| R0 | revised hips over all hips | 3.8 | 3.0 | 2.1 | 2.4 | 2.2 | 4.3 | six | the policy's Kaplan-Meier with deaths and loss to follow-up censored |
| R1 (default) | Kaplan-Meier from the operation for every hip | 3.1 | 3.2 | 2.2 | 3.2 | 3.0 | 6.3 | five | the legacy hips' years before enrolment were never observed and every one of them is revision-free by the way the registry took them in |
| R2 | legacy hips at risk from 1 January 2018 | 6.2 | 4.6 | 3.3 | 3.8 | 3.3 | 7.1 | four | the dictionary: each legacy hip was entered at its patient's first registry clinic visit, so the years from 2018 to that visit are the same unobserved, survivor-only years |
| R1' | prospective hips only | none | none | none | none | none | none | no call | the policy's population (every primary total hip of the construct on the registry, no date limit); prospective follow-up ends at 9.0 years |
| Golden | legacy hips at risk from their enrolment visit | 7.0 | 5.7 | 3.7 | 4.1 | 3.5 | 7.6 | three | none |

Position and separation: every rung names a different set (six, five, four, none, three), asserted. Every golden figure sits at least 0.68 from 5.0 and at least 0.027 from a rounding edge, and stays at one decimal under every tie, horizon and death-date convention (asserted); every rung's figure sits at least 0.3 from the bar (R2's Edvalt/Pellvoro at 4.55 unrounded is the nearest). Dominance: the decisive move carries Edvalt/Kelvarne from 3.1 to 7.0 and Edvalt/Pellvoro from 3.2 to 5.7, against R2's half step (6.2 and 4.6), so a solver who corrects to the registry's start loses Edvalt/Kelvarne but keeps Edvalt/Pellvoro, and the half-correction cannot land on the golden set. Every correction walks one way (R0 to R1 to R2 to the golden raise both Edvalt figures, asserted per construct); the over-correction past the golden (dropping the legacy hips) leaves no ten-year estimate, so no cell between rungs files the golden set. Worth: R1 is the whole stump (two constructs), R2 one construct. Ten-year evidence: 422 Edvalt/Kelvarne and 315 Edvalt/Pellvoro hips at risk at ten years under the golden, 777 and 532 legacy hips on file.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every primary total hip of the six constructs at the three hospitals on the registry, prospective (2018 on) and legacy (operated 2005 to 2017) | filed: the policy, section 4 |
| 2 Unit of account | the hip | filed: the policy |
| 3 Attribution window | operations to 31 December 2026, followed to that date | filed: the policy's extract date; the dictionary |
| 4 As-of dating | the registry extract of 31 December 2026 | filed; C1: no record dated after it (asserted) |
| 5 Version basis | one extract of each export | C1: no superseded file |
| 6 Denominator | the hips at risk at each revision time | the design forces it (the decisive step); C4 against R0, R1, R2 |
| 7 Weighting | none, each hip once | filed: Kaplan-Meier on the hips |
| 8 Window length | ten years after the operation | filed; SF10 |
| 9 Boundary inclusivity | 5.0 per cent or less stays | filed; C1: no construct within 0.4 (asserted) |
| 10 Rounding path | the unrounded estimate against the bar, the reported figure rounded to one decimal | filed: the policy's one-decimal reporting; every figure mid-bin (asserted) |
| 11 Tie-break | none arises | C1: no construct's figure equals another's or the bar |
| 12 Maturity and censoring | deaths and moves out of state censored, every other hip followed to the extract through the registry's linkage | filed: the policy and the dictionary; C3 for month-only deaths (SF11) |
| 13 Order of operations | the product over revision times of one minus revisions over hips at risk | C1: commutes over hips (asserted on shuffled rows) |
| 14 Row order | none | C1: asserted over permutations |
| 15 Duplicate resolution | one record per hip; no hip in both exports | C1: hip identifiers unique across the exports (asserted) |
| 16 Identity normalisation | catalogue numbers to constructs through the crosswalk, Thorvik's 2020 numbers included | C4: every catalogue number maps (asserted) |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | days to years at 365.25 | C1: no revision on day 3,651 to 3,653 (SF10) |
| 19 Code and status semantics | side, hospital and revision reason codes | dictionary: the data dictionary's code lists |
| 20 Integerisation | none on the call | C1 |
| 21 Clause scope | the policy's section 4 applies to the 2027 hip agreement | filed: the policy's scope |
| 22 Forward window contents | the 2027 to 2031 agreement decided on survival already observed | filed: the policy's benchmark is observed ten-year survival (the header's retrospective reason) |

## Literal reader

Executed word for word, the policy keeps a construct whose cumulative percent revision ten years after the operation, estimated by Kaplan-Meier on the registry with deaths and loss to follow-up censored, is 5.0 per cent or less; the dictionary says the registry captured every operation from 1 January 2018 at the time and entered each earlier hip at its patient's first registry clinic visit from 2018 to 2021; the one Kaplan-Meier those files support counts each hip at risk only from the day the registry saw it (its operation, or its enrolment visit), which gives the golden; every other reading violates a quoted sentence (R2 the dictionary's "entered at the patient's first registry clinic visit", R1' the policy's population) or converges (SF5, SF8 to SF13, SF15), and R1 is the same literal estimand estimated with a biased risk set, not another reading of it.

## Oracles

- No shipped file states any construct's revision rate, survival, number at risk or ranking; the agreement's schedule lists the six constructs and their prices only.
- The registry's data-management log records extract runs, linkage batches, the 2020 Thorvik re-coding and form chasing, with no outcome figure.
- Ask referees: the case's operated side in the implant log (Ask A) and the HIM merge list (Ask C); each arbitrates its own device and ties under every handling elsewhere.

## Ask sheet

The asks are decoupled from the call: neither reads the policy, the legacy workbook, the revisions, the deaths or the follow-up status, and the main population (the registry's two exports, its revisions, the death-index linkage, the follow-up status, the crosswalk, the policy and the dictionary) carries zero device rows (asserted: the call computes from the main files with every ask file deleted). Ask C reads the registry's 2026 prospective rows as its control (the trail from an input the call consumes to another system's record); its devices sit in the operating rooms' record and the merge list.

**Ask A. How many primary total hips each construct went into at each of the three hospitals in 2026 (eighteen figures).**
- H18 home: the agreement's 2026 volume by construct and hospital, the base the renewal's committed volumes are set on.
- Use: the scorecard's volume columns.
- Path: the perioperative implant log for 2026 (case, hospital, surgery date, procedure, laterality, action, manufacturer, catalogue number, description, lot, quantity), the 2026 case list (case, hospital, room, date, procedure with its side, surgeon, MRN), the component crosswalk: three files, fourteen columns.
- Primary device (D2, an anchor on the documenting encounter): when a patient with an earlier hip replacement on the other side has a primary in 2026, the circulating nurse often records the existing hip's components from the patient's implant card in that case's implant documentation, action Implanted, with its side; the case list names the one side operated on. Read on the implant log alone, the case holds two hips. Forty-eight such hips (built), one to four in every construct and hospital cell (asserted); the existing hips are pre-2018 hips never enrolled or hips done elsewhere, so no registry row matches them; about 70 per cent carry no lot number, beside more than a hundred genuine implants entered without one.
- Hazards: bilateral same-day hips under one case (procedure BILATERAL), wasted components and intraoperative exchanges (actions Wasted and Explanted), revision and hemiarthroplasty cases that use contract components, knee and spine implants in the same log.
- Stops (built): the natural read (each side with an implanted stem and cup in a primary total hip case) misses all eighteen, one to four high in each cell (1,057 hips against 1,009); each case counted once misses more (bilateral); implanted stems counted misses (exchanges and wasted stems); the answer leaves out implants on a side the case did not operate on.
- Realism: an EHR's implant record holds a patient's existing devices, entered during a later procedure for MRI safety and device tracking; an extract filtered by case date carries them with the case.

**Ask C. How many of each hospital's and each construct's 2026 primary total hips are missing from the registry (nine figures).**
- H18 home: the audit of the registry the call rests on, its 2026 capture against the operating rooms' record.
- Use: the scorecard's capture columns and the memo's evidence paragraph.
- Path: Ask A's hips (implant log, case list, crosswalk), the registry's prospective export (2026 rows: hospital, MRN, side, operation date), the HIM merge list: five files, fourteen columns.
- Primary device (D7, a prior-id chain): duplicate medical records merged by HIM during 2026 re-point every system record to the surviving MRN, so the case list carries the surviving MRN while the registry keeps the MRN it captured with the form; matched on MRN, side and date, those hips read as missing. Twelve hips (built), at least one at each hospital and for each construct (asserted), among 381 merges in the list.
- Hazards: Ask A's existing implants (each reads as a missing hip), bilateral cases (two registry hips for one case).
- Stops (built): the natural read (Ask A's natural hips unmatched on MRN, side and date) gives 88 (hospitals 30, 27, 31) and misses all nine; merges applied with the existing implants kept gives 76 and misses all nine; existing implants removed with merges unapplied gives 40 and misses all nine; the answer is 28 (Brennick Valley Medical Center 12, Tollefson Lake 5, Kittelstad 11).
- Realism: HIM merges duplicate registrations every week; a registry keeps the identifier captured with the form.

Main population zero-counts: device rows in the registry exports, revisions, death-index linkage, follow-up status, crosswalk, policy and dictionary: 0 (asserted).

| Hazard | Asks moved | Per-ask delta (design) |
|---|---|---|
| existing implants recorded in a 2026 case | A, C | A every cell 1 to 6 high; C every hospital and construct high |
| bilateral same-day cases | A, C | A cells with bilateral cases low under a case count; C low under a case match |
| wasted and exchanged components | A | stems counted high |
| MRN merges | C | every hospital and construct high |

Referee: the case list's operated side for Ask A, the HIM merge list for Ask C; neither ties only under the golden, and no file states a 2026 volume or a capture count.

| Ask figure | Cracker (lands the call, runs the battery, executes the policy and the dictionary) |
|---|---|
| A, each construct at each hospital (18) | miss |
| C, each hospital (3) | miss |
| C, each construct (6) | miss |

Mirror leakage: 0 per cent of ask weight (the mirror stops at R1 on the call and takes the same natural reads on the asks; `checks.py` asserts the cracker's path hits no ask figure).
Pair ceiling: 31.5 (cracker 45 on the call and instruction-following plus 3 for the chart, 0 of the asks; mirror 5 plus 7 plus 3 for the chart's form; to be rerun on the generated rubric).

## Build record

- Generator: `common`, `world` (the clean truth), `records` (the registry's files), `ops` (the 2026 operating-room record and the HIM merges), `docs`, `analysis` (every figure from the shipped pack), `deliver`, `checks` (170 assertions), `verify` (independent), `build`. Seed 6543 chosen from a search over worlds of the same process for one whose rungs land as designed with every graded figure clear of a rounding edge; no row is edited after it is drawn.
- Pack: 15 files (CSV, XLSX, PDF), the implant log 32,416 rows; distractors the agreement's Schedule B and the registry clinic visits (`metadata.json`).
- Gates: checks green, `verify.py` agrees, two builds byte-identical, `target.zip` cut from the final build.
- leak.py (2027-01-27): REVIEW, every line harmless: 4.1 is the policy's clause number; the three hospitals sit in the policy's scope sentence; the agreement's Schedule B names the six constructs with prices only (Gate G clean, a declared distractor); the dictionary's enrolment and death-linkage sentences are the registry's own provenance and name no risk set or entry time; the data-management log, the legacy workbook and the case list name hospitals beside dates and counts and rank no construct.
- Leak reader (first read): Q1 none (the policy files the bar and the estimator, not the entry), Q2 none, Q3 the crosswalk (needed), Q4 none, Q5 4.3's sentences execute to every registry hip, the first revision, deaths and loss to follow-up censored, Q6 an analytical choice (the risk set's entry for hips entered after their operation). Fixed from it: the move-out reading (four figures moved 0.06 to 0.12 at one decimal without it) closed by the dictionary's "the registry loses follow-up of a hip when its patient moves out of the state"; the log's HO prefix (KO); metronomic linkage dates varied; ten abstraction notes in place of four; the crosswalk's uniform column replaced by the year each construct came into use.
- Determinism judge (round 1): DETERMINISTIC, APPROVE; Gate G analytical, not a defect, no surface read; Gate H domain pass, layers pass, decisive step analytical; every figure reproduced (six ten-year figures, 18 cells, 28 missing); nit HO/KO, fixed.

## Pre-ship check

- Rule 1: the call turns on each construct's Kaplan-Meier cumulative percent revision at ten years, the joint registry's own estimand; a washing machine range has no registry that took in older units only when they came back intact.
- Rule 2: the mess (two export layouts, Thorvik's renumbering, bilateral hips, month-only deaths, three date styles, Kittelstad's own MRNs) is how the registry and the hospitals hold their records, and each item mishandled leaves the call or fails loudly (asserted); the decision rests on the risk set, Layer 2.
- Rule 3: no memo, decoy or planted block; no field or code read differently flips the call (R1 reads every field correctly); no filed rule says when a hip enters the risk set, and executing the policy as written on the default path files five constructs (asserted on the clean truth).

## Tried and rejected

- Seed DA15 connected-TV world, worked at the draw 2026-10-17 and never registered: the capped home-screen trailer's audience is fully observed in profile-level logs, so the cap, the broadcast day and kids profiles are rules to apply; the one estimation step, the age of profiles with no typed birth year, inverts the age model's per-age error rates measured on typed profiles (the typed profiles' precision carries their younger mix), which is task446's lesson, and the guard blocked its signature (population, G6) against six builds. Co-viewing, panel projection, reach modelling and the novelty of new TVs were each considered: a fork-prone panel estimate, task264's weighting family, a model-dependent projection, and task134 v2's time-since-entry hazard.
- Spike-in normalisation of per-cell expression across cell lines (RNA-seq with ERCC controls), considered as the redraw: the insight (the sample's own total moves with the thing measured, an external reference added per unit does not) is task236's, and the guard blocked the signature (population, G16, designation_set) inside the batch against task236.
- Residential or school segregation by the dissimilarity index with its small-unit bias, considered as the redraw: the correction (excess over random placement, or the bootstrap-corrected index) has several defensible forms with different figures unless the policy names one, and naming it makes the decisive step the execution of the named comparison.
- The draw's maker, construct and hospital names (Orvane, Kessick, Teraluma, Hollis-Ward; Talvenn, Ardis, Merrow, Fenrow, Venro, Solvane, Brecken, Pellamy; Tamsen Lake, Harwick), replaced at stage 3: Harwick sits one letter from Warwick and Hardwick, Teraluma two from Petaluma, Ardis two from the Arcos hip stem, Solvane two from Solvay, Brecken one from Bracken and inside Breckenridge, Pellamy two from Pelham.
