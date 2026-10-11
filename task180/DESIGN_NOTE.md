# task180 design note (architecture 3)

Seed AD03 (the revenue-protection crew), objective Anomaly Detection & Diagnostics. Architecture 1 (revenue protection,
the screen grain) was spent at in-house round 1. Architecture 2 (a lines company's transformer inspection slate, main-tank
acetylene attributed to its source) was spent at judge pass 2 (SEND_BACK, Gate C); its note is `DESIGN_NOTE_arch2.md`
and its reports and rounds carry the `_arch2` suffix (architecture 1's carry `_arch1`). This is the slot's third and last
architecture: a SEND_BACK or a third failed hardening loop retires task180. The seed's idea that carries over is the one
the whole lane shares: the loudest signal is not the cause.

Carried from architecture 2's send-back: the decisive separation must sit far above the noise of every lens a reviewer
can bring; every graded figure is stated with its window and method; no exact ties among graded figures.

## DRAW

```
Card filed with guard.py register before the ladder was written? yes (WARN: overuse.org_family government_agency,
  repeat.gate_g method_or_model_selection against task134; both answered under WARNS)
Shape: 18 hypotheses versus evidence (three signals, each a hypothesis the registries confirm or refute)
Gate G mechanism: method_or_model_selection (which comparison the registry data entitle: the medicine's users against
  other people, or each user against their own other time)
Gap: population (decisive: who the users are compared with), time (the month after the start)
Pattern: none (own); generator G17 (confounding: the association collapses once the person is conditioned on)
Domain: pharmacology-pharmacoepidemiology-safety / safety-signal-detection   Objective: anomaly-detection
Pairing repeated from a recent build? no (pharmacology x anomaly detection never built)
Stakeholder role: head of the medicines agency's pharmacovigilance unit (compliance_or_audit)
Context artifact: monitoring_export (the quarter's signal screen and its spontaneous-report line listing)
Calibration form: none
Decision type: pick_one_of_n   Answer unit: named_option   Opening move: evidence-first
Stump strategy: causal_design   Decisive rule filed? no (SOP-PV-14 files the case definitions, the new-user rule and the
  30-day window; it says nothing about what the month after the start is compared with)
Official decoy filed? no   Validated decoy? no   stump_class: analytical
Forum: committee_or_panel (the agency's medicines safety committee opens the formal assessment; filed as
  regulator_or_inspector until the stage 5 heart check, see DUPLICATE CHECK)
Forcing event: vote_or_meeting (the committee meets on Thursday 22 October 2026)
Org family: government_agency (the national medicines agency)
Layer 2: estimand_identification, own:self-controlled-signal-refinement
People (guard.py names, da_DK, seed 180): Helge Jørgensen (head of the pharmacovigilance unit, the requester), Janni Nielsen (registry data manager who wrote the extract notes), Frida Clausen (signal
  assessor, owner of SOP-PV-14), Kåre Holst (committee secretary), Iben Pedersen
  (pharmacoepidemiologist), Esben Olesen (medical assessor)
```

**Data-native sentence.** A new medicine's users are the patients doctors chose to start on it, and a new medicine is
channelled by its claims and its contraindications: the new orexin-receptor sleep medicine, sold as gentler for older
people, goes to frail patients who are already falling, and the new uricosuric, which is avoided in kidney disease,
goes to gout patients whose kidneys are healthy; the registries hold every dispensing and every hospital contact of the
same people for years, so each new user can be compared with their own other time.

**Layer 1 (realistic mess and the systems that produce it).** National registry extracts as a medicines agency receives
them through the national health data service: the patient registry's contacts (emergency, inpatient and outpatient) with
ICD-10 diagnoses in the registry's own form (a D prefix, no dot: DN179), an action diagnosis and secondary diagnoses per
contact, and transfers between departments recorded as separate contacts of one admission; the registry's 2019 change
from courses to contacts, so the extract carries two record structures; the prescription registry's dispensings coded by
ATC with package number, packages and defined daily doses per package, with one new product's ATC code reassigned in 2024
from a provisional code; pseudonymised personal numbers across the extracts, with deaths and emigrations in the civil
registration extract ending observation; the spontaneous reports line listing with suspect and concomitant medicines,
follow-up versions of one case and MedDRA preferred terms; the agency's standard matched comparator extract (non-users
matched on birth year, sex and the user's start date).

**Layer 2 (the analytical shortcut).** Comparing the people who started a medicine with other people. A strong analyst
compares each medicine's new users with matched non-users and then, as modern pharmacoepidemiology prefers, with new
users of the established alternative (zopiclone, allopurinol, orlistat), adjusted for every recorded comorbidity; both
designs name the sleep medicine's falls signal, because the new sleep medicine is channelled to frail patients already
falling and the uricosuric to patients with healthy kidneys, and frailty and kidney reserve are what no registry
variable records. An expert sees an acute effect of an intermittent exposure in a channelled population and uses the
self-controlled comparison, each patient's first 30 days on the medicine against the same patient's later time, which
cancels everything fixed about who is prescribed it: the falls signal disappears and the kidney injury signal stands.

**Similarity claim.** No build on file uses a self-controlled comparison. task68's matched panel removes entrants from a
movement (composition); task83 conditions a randomised holdout's effect on each unit's prior trend; task130 v3 forecasts a
group chosen on an extreme value (regression to the mean). Here the decisive step is the comparison design under
channelling. Nearest driver on file 0.07 (task41).

## THREE RULES (client, 2026-10-10)

- **Rule 1, the domain is used.** What decides the call is the self-controlled design pharmacoepidemiology uses to test
  an acute adverse reaction in registry data, under channelling of a new medicine. Swap test: with another field's nouns
  in there is no new-user cohort, no channelling by indication and contraindication, no acute risk window after an
  exposure start on the same person; the task does not survive the swap.
- **Rule 2, two layers.** Layer 1 above (registry structures, codes, the 2019 change, ATC reassignment, linkage,
  censoring, report versions). Layer 2: the comparison design under channelling.
- **Rule 3, the decisive step is analytical.** Class `analytical`. Analyst test: a strong analyst who links the
  registries correctly, restricts to new users and compares the 30-day admission rate after the start with matched
  non-users and with new users of the established alternative, adjusted for every recorded comorbidity, confirms the sleep
  medicine's falls signal; only the within-patient comparison of the first 30 days with the same patient's later time
  confirms the uricosuric's kidney injury signal. Rule application (the case definitions, the new-user rule, the window)
  and data semantics (the D prefix, the two record structures, the ATC reassignment) sit on lower rungs and in the asks.

## GATE G

- **Litmus.** Nothing reported is overturned: every report, dispensing and contact is correct, and no one in the pack
  claims any signal is real. The committee's question is open; the difficulty is which comparison answers it.
- **Primary mechanism:** method_or_model_selection (the comparison design), with statistical rigour (confounding)
  supporting.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Deletion test.** Delete the spontaneous reports and the extract notes: the cohort and active-comparator designs still
  name the sleep medicine and the self-controlled design still names the uricosuric.
- **Clean-data and instrument test.** No file is incomplete or stale. A perfect instrument (every fall and every kidney
  injury in the population recorded, every dose taken known) leaves the channelling exactly where it is: the people who
  start the sleep medicine still fall more before and after starting it. Nothing is repaired.
- **Lens swap.** Not one population under two lenses: the answer's quantity is a within-person rate ratio built from the
  timing of each case's admissions against their own start date (a group-and-order construction across the prescription
  and patient registries); the naive quantity is a between-person ratio.

## STUMP SENTENCE

A competent solver links the prescription and patient registries, takes each medicine's new users, compares their
admissions for the signalled event in the 30 days after starting with matched non-users and then with new users of the
established alternative, adjusts for every recorded comorbidity and names the sleep medicine's falls signal, the largest
ratio on both designs; the step that lands it there is comparing people with other people, when the sleep medicine is
channelled to patients already falling and the uricosuric to patients with healthy kidneys, and only the self-controlled
comparison of each patient's first 30 days with the same patient's later time confirms the uricosuric's kidney injury
signal instead.

## ENTITY AND UNIT OF VALUE

One signal (a medicine and an event). The committee opens one formal assessment this meeting; its value is an adverse
reaction confirmed (a label change, a direct healthcare professional communication) or a false alarm not chased.

## THE WORLD (build plan; every figure below is a target the generator asserts or replaces with its shipped value)

Medicines (fictional products, real ATC groups):
- Sleep medicine: tasorexant (Somnevo), a dual orexin-receptor antagonist, ATC N05CJ05, launched in Denmark 2022.
  Signal: falls. Comparator for the active-comparator design: zopiclone (N05CF01).
- Uricosuric: corinurad (Uralexa), a URAT1 inhibitor for gout, provisional ATC M04AX02 until 31 December 2023, then
  M04AB06. Signal: acute kidney injury. Comparator: allopurinol (M04AA01).
- Weight-loss medicine: velaglutide (Gravera), a GLP-1 receptor agonist, ATC A10BJ09. Signal: acute pancreatitis.
  Comparator: orlistat (A08AB01).

Channelling (latent, never a column):
- Tasorexant starters carry a latent frailty that raises fall admissions about fourfold against age- and sex-matched
  people; zopiclone starters carry about half that excess; prior fall admissions and recorded comorbidities are noisy
  indicators of it, so adjusting for them moves the ratios only partly.
- Corinurad starters carry a latent kidney reserve that halves their acute kidney injury rate against allopurinol starters
  (allopurinol is the gout medicine used in kidney disease); recorded chronic kidney disease codes capture only part of it.
- Velaglutide starters carry moderate obesity-related pancreatitis risk; no true effect.

True effects (the only causal effects in the world): corinurad raises acute kidney injury about 2.5-fold in days 1 to 30
after a new user's first dispensing, independently of NSAID co-use (the excess holds among starters with no NSAID
dispensed in the window, asserted). Tasorexant and velaglutide have no effect on their events. A prior acute kidney
injury lowers the chance of starting corinurad (contraindication), and a fall admission raises the chance of starting a
sleep medicine slightly (insomnia after discharge): both bias a full-observation self-controlled analysis in the same
direction as the answer (the kidney ratio up, the falls ratio down), and the exposure-anchored design (all observation
after the start) is immune; asserted.

## LADDER (shipped; each rung asserted by name in `generator/checks.py`)

| Rung | Construction | First | Shipped margin (thinnest cell) | Killed by |
|---|---|---|---|---|
| 0 | Spontaneous reports per signal in the quarter (the screen: latest version of each case, medicine suspected) | tasorexant falls, 34 cases | 1.62 over velaglutide 21 (corinurad 13) | reports are not incidence; the screen raises signals, it does not confirm them |
| 1 | New users against matched non-users, 30-day admission rate ratio: crude; Charlson groups; Charlson groups and prior admission for the event | tasorexant falls (3.76, 3.49, 3.13 in the thinnest cells) | 2.56, 2.37, 2.13 | channelling: the users were admitted for the event at their own rates before starting |
| 1b | Observed in the 30 days after the start against expected from the age- and sex-specific population rates | tasorexant falls (3.51) | 2.29 | as rung 1 |
| 2 | New-user active comparator (zopiclone, allopurinol, orlistat starters): crude, adjusted, propensity-weighted (IPTW and ATT) | tasorexant falls (2.25, 1.86, 1.81, 1.91) | 1.80, 1.38, 1.33, 1.38; corinurad 1.40 or less in every cell | the new sleep medicine is channelled to the frailest; the uricosuric to the healthiest kidneys |
| 3 (answer) | Self-controlled: each new user's days 1 to 30 after the first dispensing against the same person's days 61 to 180, conditional Poisson, each start its own stratum, Wald interval | **corinurad acute kidney injury, 2.52 (95% CI 1.92 to 3.31)** | tasorexant 1.01 (0.84 to 1.22), velaglutide 0.98 (0.51 to 1.85) | |

Evidence the pack carries for the judge (asserted): in the year before the start tasorexant starters' fall admission
rate is 3.95 times matched non-users' and 2.32 times zopiclone starters'; corinurad starters' kidney injury rate is 0.46
times allopurinol starters'. In the month before the start falls run at 1.65 times the rate of days -395 to -31 for
tasorexant starters (211 events), and kidney injury at 0.41 for corinurad starters (12 events): the event-dependent
starts the design note planned, which bias a full-observation comparison (corinurad 2.573 with days -30 to 0 set
aside, 2.606 without; tasorexant 1.034 and 1.020) and leave the exposure-anchored one untouched (the golden cell reads
no time before the start, asserted by deleting every earlier event). Among corinurad starters with no NSAID dispensed in
days 0 to 30 (72 per cent) the ratio is 2.35 (1.71 to 3.23); NSAIDs are dispensed in days 0 to 30 to 28.3 per cent
against 6.1 per cent in the month before (flare cover). Corinurad: 58,988 new-user starts, 93 admissions in days 1 to
30 and 132 in days 61 to 180.
## GRID (shipped, asserted cell by cell)

- **Self-controlled, pinned conventions (deaths and emigrations end observation, transfers merged): 567 cells, 189
  per signal** (3 populations: all starts, starts from 2022, starts from 2023; risk windows days 1 to 30, 0 to 30 and
  1 to 28; control windows days 61 to 180, 31 to 180, 61 to 365, all time after day 30, and the full-observation design
  with days -30 to 0 set aside; no adjustment, five-year age bands, and age bands with calendar half-years in the
  full-observation design; conditional Poisson and Mantel-Haenszel). Corinurad 2.308 to 2.624 in every cell, every cell
  within 0.3 of the golden 2.52 and every lower limit 1.6 or more; tasorexant 0.960 to 1.083 and velaglutide 0.619 to
  0.996, every interval spanning 1. Misses 0.
- **The two convention variants: 1,134 cells.** Deaths and emigrations not ending observation: corinurad 2.333 to
  2.670, tasorexant 1.029 to 1.132, velaglutide 0.619 to 0.996. Transfers not merged: corinurad 2.195 to 2.567,
  tasorexant 1.010 to 1.138, velaglutide 0.621 to 0.821. Every cell keeps corinurad first with no rival within 25 per
  cent (closure asserted cell by cell).
- **Naive cells: 48, every one tasorexant falls** (matched non-users crude and two adjustment sets, observed against
  expected, active comparator crude, adjusted, IPTW and ATT, each over observation from 2022 or 2023 and with deaths
  ending observation or not); thinnest margin 1.33 (active comparator IPTW).
- **Mess neutrality of the main call (asserted):** every ask stop below keeps corinurad first with no rival within 25
  per cent; contacts linked within 1, 4, 12, 24 or 48 hours give the same admissions for every event; no dispensing gap
  of 336 to 394 days and no immigration within ten days of a start's 365-day boundary.
## CLOSURE (the 22 axes)

1 Population: new users 1 January 2022 to 31 March 2026 (no dispensing of the same substance in the 365 days before;
resident for those 365 days). 2 Unit: a signal (medicine and event). 3 Window: days 1 to 30 after the first dispensing
(SOP-PV-14). 4 As-of: registry data to 30 June 2026 (the extract); the committee meets 22 October 2026. 5 Version basis:
the latest version of each spontaneous report. 6 Divisor: person time. 7 Weighting: none. 8 Window length: 30 days. 9
Boundary: no rival within 25 per cent of the winner at any rung. 10 Rounding: ratios to two decimals. 11 Tie-break: none
needed. 12 Maturity: windows that end after 30 June 2026 excluded (starters after 31 March 2026 cannot complete a control
window). 13 Order: link, new-user rule, case definition, then the design. 14 Row order: irrelevant. 15 Duplicates:
transfers within one admission are one admission; report versions. 16 Identity: pseudonymised personal number across
extracts; the substance across its two ATC codes. 17 Netting: none. 18 Units: admissions, person-days. 19 Code semantics:
the registry's D-prefixed ICD-10; action against secondary diagnoses per the case definitions. 20 Integerisation: none.
21 Scope: the three signals. 22 Forward window: none.

## ASK SHEET (shipped)

| Ask | Figures | Shipped answer |
|---|---|---|
| The signal the committee opens (note) | 1 | corinurad (Uralexa) and acute kidney injury |
| Its rate ratio for the month after the start, with the 95 per cent interval (note) | 3 | 2.52 (1.92 to 3.31), days 1 to 30 against days 61 to 180; 2.36 to 2.62 over the 63 self-controlled cells on SOP-PV-14 6.1's days 1 to 30 (every control period, adjustment, estimator and population), which the submission carries; the 189-cell grid spans 2.31 to 2.62 |
| Its admissions in that month among people who started it in 2025 (note) | 1 | 21 |
| How many of those it caused (note; SOP-PV-14 8.2) | 1 | 13 (12.678); 12 or 13 across the band (12.11 to 13.00), carried in the submission |
| New users per medicine and calendar year, 2022 to 2025 (`new_users_by_year.csv`) | 12 | tasorexant 1,946, 3,895, 4,546, 4,625; corinurad 11,182, 12,903, 13,712, 13,461; velaglutide 6,153, 18,338, 21,376, 20,070 |

Ask stops (each asserted to move its figures, shipped):
- New users: the current ATC code only takes corinurad 2022 and 2023 to 0 and 2024 to 22,905. Ignoring the washout
  (first dispensing ever) takes tasorexant 2025 to 4,422 and corinurad 2025 to 12,765. A first dispensing each year takes
  corinurad 2025 to 24,178. Counting returned dispensings takes corinurad 2025 to 13,567, and ignoring residence to 13,515.
- The 2025 admissions: transfers counted separately 26, secondary diagnoses 25, outpatient contacts 24, returned
  dispensings counted 22.
- The ratio moves under secondary diagnoses (1.79), outpatient contacts (1.94), the current ATC code only (2.00), the
  washout ignored (2.42), returned dispensings (2.49), residence ignored (2.51), transfers separately (2.53) and deaths not
  ending observation (2.53).
## PINS (shipped)

`SOP-PV-14_signal_refinement.pdf`, revision 3, effective 1 June 2026:
- 1.1 purpose. 1.2 the committee's question: does starting the medicine raise the risk of the event in the month after
  the start? A signal is supported when it does.
- 2.1 responsibilities.
- 3.1 the registry extract, linked on the pseudonymised personal number. 3.2 spontaneous reports frame the event and are
  not used to estimate risk.
- 4.1 annex A's case definitions on the registry's D-prefixed codes. 4.2 contacts linked by transfer make one admission;
  an event is dated by the start of its admission.
- 5.1 to 5.4 the new-user rule: 365 days without the substance, resident for those days; every ATC code the substance
  has carried; returned dispensings do not count; a person can be a new user again after 365 days.
- 6.1 the month after the start is days 1 to 30.
- 7.1 observation ends at death, emigration or the last day of data.
- 8.1 the note's figures. 8.2 ratios to two decimals, and admissions caused as admissions x (ratio - 1) / ratio,
  rounded to the nearest whole admission. 8.3 the note's deadline.
- Annex A:
  - falls: an emergency contact or inpatient admission whose action diagnosis is an injury (DS00 to DT14), with a fall
    code (DW00 to DW19) among its diagnoses;
  - acute kidney injury: an inpatient admission with DN17 as action diagnosis;
  - acute pancreatitis: an inpatient admission with DK85 as action diagnosis.

The SOP names no comparison group and no design.

`registry_extract_notes.md` (Janni Nielsen): field semantics in Danish with an English dictionary, the D prefix, the
change of record structure on 4 February 2019, the ATC reassignment, the matched comparator extract's matching rule.
The banned-word sweep (15 terms) over every shipped text file and the prompt is clean.
## PACK GATES (shipped)

| File | Format | Rows | Role |
|---|---|---|---|
| `pv_signal_screen_2026Q3.xlsx` | xlsx | | context artifact: the Q3 screen's disproportionality table and line listing |
| `SOP-PV-14_signal_refinement.pdf` | pdf | | governing procedure (pins) |
| `registry_extract_notes.md` | md | | field notes |
| `prescription_registry_2018-2026.parquet` | parquet | 3,598,588 | dispensings |
| `patient_registry_contacts_2018-2026.parquet` | parquet | 2,667,469 | hospital contacts (spine) |
| `patient_registry_diagnoses_2018-2026.parquet` | parquet | 3,725,191 | diagnoses per contact |
| `civil_registration_extract.csv` | csv | 583,700 | birth year, sex, death, emigration, immigration |
| `matched_comparators.csv` | csv | 446,700 | the data service's matched non-users |
| `atc_ddd_index_2026.csv` | csv | 12 | substances, codes with validity dates, DDDs |
| `population_and_admissions_2022-2025.csv` | csv | 128 | population and national admissions by age and sex |
| `psur_summary_tasorexant_2026.pdf` | pdf | | distractor (named in `metadata.json`) |
| `committee_minutes_2026-07-09.md` | md | | distractor (named in `metadata.json`) |

12 files, 5 formats (csv, md, parquet, pdf, xlsx), 130.1 MB; four files over 25,000 rows. Two distractors, asserted unused:
the golden recomputes unchanged with each removed. Goldens: `golden/signal_refinement_note.docx` (one page and a
little, to the committee from Iben Pedersen, approved by Helge Jørgensen) and `golden/new_users_by_year.csv`.

## BUILD RECORD

- `generator/build.py` runs everything:
  - the pack: `world.py`, `sim.py` (people, latent channelling, dispensings, events), `hospital.py` (contacts,
    transfers, diagnoses, the 2019 structure change), `records.py`, `docs.py`, `postprocess.py`;
  - the goldens: `deliver.py` over `golden.py`;
  - then `metadata.py`, `checks.py` (4,219 assertions), `verify.py` (OK on its own code path: the call corinurad at 2.52 (1.92 to 3.31), 2025 admissions 21,
    caused 13, tasorexant 1.01 and velaglutide 0.98, NSAID-free 2.35, the between-person rungs (matched 3.77, active
    comparator 2.29, observed against expected 3.53 for tasorexant), and the new-user table and the note agree);
  - then a second full build into a scratch folder inside the task (removed after) and the sha256 comparison
    (12 target files, 2 golden files and metadata.json byte-identical, combined sha256 b3ac114e0fabd58d).
- Containers: workbooks and the note repacked with in-fiction owners and saved stamps and fixed entry stamps. PDFs are
  issued on their in-fiction dates with the library banner blanked at equal length.
- Personas in the pack, the golden and the prompt (`guard.py surface` scan): Esben Olesen, Frida Clausen, Helge
  Jørgensen, Iben Pedersen, Janni Nielsen, Kåre Holst, all on the card.
- Invented names (H21): Somnevo, Uralexa, Gravera, tasorexant, corinurad, velaglutide (no such products or INNs); the
  agency is "the Agency" and the data service "the national health data service".

## DEVIATIONS FROM THE DESIGN (as built)

- **A salted stream.** The 2022 cohort of corinurad starters draws its after-start events from a salted stream (salt
  1); no other stream moves.
  - Why: the unsalted world passed every check except one. Its admissions-caused figure was 12.579, 0.079 from its
    rounding edge.
  - How it was chosen: a screen of ten salts against the checks' thresholds. This salt is the only one that held every
    graded figure off its edges (ratio 2.5235, limits 1.9222 and 3.3130, caused 12.678) with every margin.
- **The two convention variants are held to keep the winner, not to the 2.2 floor.** These are deaths and emigrations
  not ending observation, and transfers not merged.
  - The floor applies to the pinned cells only. The variants hold corinurad at 2.0 or more, rivals at 1.25 or less,
    closure at 1.25.
  - This matches the GRID line "every cell keeps its winner". Transfers not merged reach 2.195 at their lowest.
- **A last stay-separation pass.** `hospital.separate_stays` settles any clash left after its six rounds against the
  latest end of every earlier event stay of the person.
  - One person's kidney injury stay and pancreatitis stay sat 41 hours apart, so 48-hour linking changed an admission.
  - Now every linking window from 1 to 48 hours gives the same admissions, asserted.
- **Acute kidney injury counts on the action diagnosis only** (annex A), not "action or secondary" as the plan had it.
  Counting secondary diagnoses is an ask stop (2025 admissions 21 to 25, ratio 1.79).
- **The population file** carries national admissions beside the population (`population_and_admissions_2022-2025.csv`),
  which rung 1b's observed-against-expected comparison uses.

## LEAK CHECK (stage 4, mechanical half)

`python3 .claude/skills/leak-check/leak.py task180 --asof 2026-10-12 --quiet`: **REVIEW, no LEAK** (12 files, 19
golden figures). Each REVIEW line answered:
- `SOP-PV-14_signal_refinement.pdf` carries 6 of 8 words of the committed call. Harmless: the SOP names the formal
  assessment the committee opens (1.1, 8.1) and defines all three events in annex A (falls, acute kidney injury, acute
  pancreatitis); it never pairs an event with a medicine as supported and names no design.
- `SOP-PV-14_signal_refinement.pdf` has 3 stump-paragraph terms (agency, carried, extract). Harmless: the
  Agency's own name, and "carried" and "extract" in the SOP's description of the data service's extract; the SOP
  states the committee's question and never names a design, a reference period or an estimator.
- `registry_extract_notes.md` has 4 stump-paragraph terms (register, agency, matched, extract). Harmless: "matched"
  is the data service's matched comparator extract (a file the notes must describe), and "register", "agency" and
  "extract" are the organisation's nouns; the notes describe fields and never name a comparison design.
- Container metadata: INFO only (no writer signature).

Re-run after the reader's fixes (rebuild 92e0abb): the same lines, nothing new.

**Solver's-eye read (pass 1, Sonnet; the answers are in `leak_check_report.md`).**
- **Q1 and Q4: none.** No sentence names the decisive step, and nothing reads as the answer.
- **Q3: `atc_ddd_index_2026.csv`.** It narrated the corinurad code change ("Erstatter M04AX02"). The list now keeps
  its codes and validity dates without remarks; the notes already present it as the delivered code list for `atc`.
- **Q2: the screen's PRR ranked corinurad/AKI first.** It was 17.74, against 10.37 and 6.35. It now leads with
  tasorexant/Fall (13.85, corinurad/AKI 11.18 at 24 cases, velaglutide 6.35), as the report counts already did, and
  no screen count equals a golden figure.
- **Both fixes are data-only,** so there is no second read.
- **Realism notes, deferred to stage 6b:**
  - weekday-flat dispensings, with holidays;
  - a 15:59 start-time spike in the LPR3 contacts;
  - round cohort counts;
  - flat immigration dates;
  - the PSUR's exposure against the registry's;
  - the extract delivered before the screen ran;
  - the screen's 11 pairs and its case-number blocks;
  - fictional ATC codes on real assignments (M04AX02).
- **Watch item:** the reader planned the within-person comparison unprompted. The STOPPING RULE applies if the solver
  round does the same.
## DUPLICATE CHECK (stage 5)

**Heart (`guard.py heart task180`, 2026-10-11): BLOCK on two axes, both against task135.** task135 is another author's
build. Its card reached main at 10:46, after this card was registered on this branch at 10:14. Same-day draws sort by
task number, so task135 counts as a predecessor here, and neither card was on main when the other was checked.
- `ban.forum` (regulator_or_inspector). The deciding forum is the agency's own medicines safety committee, so the card
  now files `committee_or_panel`, which is the more accurate label and clears the block.
- `ban.pattern` (decisive G-code G17).
  - The only other honest label for the decisive step, G16 (the comparison design), is banned by task134, drawn the
    same day.
  - This is the slot's third and last architecture.
  - The card was re-registered with `--force` on the author's explicit instruction (AskUserQuestion, "Register anyway
    (Recommended)"), with the reason in its notes and a differentiation line against task135.
  - task135's G17 is a rating curve's retransformation bias in a sediment forecast; here it is confounding by
    indication that only a within-person comparison removes.
  - Domain, objective, decision type, shape, gap and driver all differ, and the heart's nearest driver on file is 0.04.

WARNs, answered:
- `overuse.org_family` government_agency: signal management belongs to the medicines agency (see WARNS).
- `repeat.gate_g` method_or_model_selection against task134: task134's method choice is a survival estimator for
  competing exits on a forecast; here it is the comparison design under channelling.

**Clone pre-flight:** see `clone_check_report.md` (architecture 3, pass 1).

## WARNS (guard.py, answered)

- `overuse.org_family government_agency`: signal management belongs to the medicines agency; a university unit could
  run the analysis but could not open a committee assessment.
- `repeat.gate_g method_or_model_selection` against task134: task134's method choice is a survival estimator for
  competing exits on a forecast; here it is the comparison design under channelling on a signal.

## STOPPING RULE

Two rounds in which the solver uses a self-controlled comparison unprompted file this architecture as at-ceiling (the
slot then retires); a miss that lands anywhere other than rungs 0 to 2 is read for a fork before any hardening.

## Tried and rejected

- **Draws weighed for architecture 3 and not taken (2026-10-11).** A labour force survey movement read on the people
  interviewed in both quarters against the rotation groups: the guard's same-puzzle test and the driver both put it on
  task68 (a matched panel of continuing units against an aggregate moved by entrants), the same insight in the same kind
  of office. An airline's landing gear alert traced to one station's wheel changes within each airframe: with forty
  aircraft and many defects each, the chronically defective tails show in any per-aircraft table and controlling for the
  aircraft is a reflex, so the confounder announces itself. Signals passed at danger per approach at danger: the exposure
  either has to be named in the question (rule application) or is a fork against trains passing. An air-quality rise
  normalised for meteorology and a groundwater rise read within each well: attribution of a signal to its drivers, the
  architecture-2 move, and trends any analyst plots. A disproportionality signal unmasked by removing a dominant drug
  from the background: the comparator would have to be filed (rule application) or is a fork. Pre-bid abnormal returns
  under thin trading: the bias from a synchronous beta is swamped by the noise of the thinly traded share.

- **Judge pass 2 (architecture 2, loop 2, 2026-10-11): NOT_DETERMINISTIC, SEND_BACK; architecture 2 spent.** Gate C,
  competing_defensible_answer, in the judge's words: "LST-T2's hydrogen increments track its tap operations: r 0.81,
  permutation p 0.005. Rolleston T2's (RLS-T2) do not: r 0.14." The submission's own increment method, applied to
  hydrogen, keeps Leeston T2 as a main-tank fault, so SBG-T2 and LST-T2 (tied at 8.0674) then RLS-T2 is a defensible
  slate on these files. Companions: the 9.7 ppm-a-year pre-onset pace does not reproduce (9.63 by OLS over the year
  before 9 June 2025), the exact SBG-T2/LST-T2 tie reads as constructed, and the gas-source rule, stated nowhere in the
  pack, can be pressed as an external dependency. The loop-2 radiator hydrogen sat at the noise floor of the tap-linked
  increments, so the hardening that stopped round 4's ratio step opened a fork. Under build-pipeline (Retirement) a
  judge SEND_BACK spends the architecture; re-rooted to architecture 3, the slot's last. Carried forward: a decisive
  separation far above measurement noise under every lens a reviewer can bring, every graded pace stated with its window
  and method, and no exact ties among graded figures.

- **Round 4 landed (architecture 2, loop 1, the re-run the judge's FIX_NOW required, 2026-10-11); hardened as loop
  2.** One solver, proxy 74.8, the slate exact. Its deciding step: "Main-tank fault screen (s5.1-5.2): DSL-T1 and
  LST-T2 (in-oil arcing tap changers) show C2H2 +9.8 and +8.2 ppm with H2 +1 ppm, read as tap-changer contamination
  and excluded; SBG-T2 (vacuum tap changer, H2 +16) and RLS-T2 (H2 +8) kept". The plain gas ratio carried the call.
  Brief: build the next rung so that exactly this step completes and returns the wrong slate. Leeston T2's radiators
  were replaced with new hot-dip galvanised panels on 12 November 2024 (in service, through the isolating valves; the
  log carries it as capital work under the projects office's own job number, so no work-order number moves), and new
  zinc gives off hydrogen, fast at first and easing (26 ppm towards saturation, time constant 0.8 years). Its hydrogen
  was rising at 9.7 ppm a year in the year before its first acetylene (June 2025), so the twelve-month C2H2/H2 reads
  0.91 and the ratio step keeps it (rung 3c: LST-T2 and SBG-T2 tied at 8.07, RLS-T2). What the ratio cannot see is
  that the acetylene brought no hydrogen of its own: over and above the pace it already had, Leeston T2's hydrogen
  did not move when the acetylene came, while Rolleston T2's hydrogen was flat for the year before its acetylene and
  rose with it. The decisive step is now per gas: tracking for the acetylene, the timing of the hydrogen against it.
  Every golden figure stays (asserted against the round-4 values); the verifier carries its own version of the rule.

- **Judge pass 1 (2026-10-11): DETERMINISTIC, FIX_NOW on hygiene.** The maintenance log's 176 annual inspections
  reused one sentence and five remarks ("T2 fan 3 noisy bearing, raised WO." 25 times at 16 sites with no follow-up
  order) and Burnham's battery bank was "8 years old" in 2019 and again in 2022. The remarks now vary on a random stream
  of their own (the draws that number the work orders are untouched, so every OLTC, breather and oil-processing row is
  byte-identical, asserted), defects are dealt with on the visit, a second battery job at a site is a discharge test,
  and the bookings sheet carries its 9 October save stamp. The judge's watch item stays a defence, not a change: the
  RLS-T2 split rests on the field's gas knowledge, and the in-pack contrasts are hydrogen flat at DSL-T1 and LST-T2
  through acetylene rises of about 22 and 13 ppm, RLS-T2 hydrogen from about 33 to 54 ppm after its onset, and SBG-T2
  as the control.

- **Round 2 landed (architecture 2, loop 0, 2026-10-11); hardened as loop 1.** One solver, proxy 74.6, the slate exact
  and every ask figure right. Its deciding step: "Main-tank test (5.2): joined monthly samples with tap ops from
  scada_tap_counters_daily (rollovers +100000; counters replaced -> reset). DSL-T1 and LST-T2 acetylene rises at a
  constant ~0.6 ppm per 1,000 ops in every interval (in-oil tap-changer leak) -> excluded; SBG-T2 (vacuum tap changer)
  and RLS-T2 acetylene rise in steps unrelated to ops." The confirming reader (pass 3, run beside the round) planned the
  same step off the 5.2 rewording: "Keep only code 3 units with a main-tank fault (s.5.1-5.2). That means dropping in-oil
  tap-changer units whose acetylene or hydrogen rise tracks tap operations." 5.2 stays as worded, because without it the
  literal reading is rung 1; the attribution is a work order and the hardening deepens it instead. Brief: build the next
  rung so that exactly this step completes and still returns the wrong slate. Rolleston T2's arc is now at the tap
  selector, which works in the main-tank oil: a little gas at every operation, so its acetylene follows its counter as
  closely as the leaks' (r 0.999 raw, 0.992 per day) and the tracking step drops it (rung 3b: Southbridge T2, Coalgate T1,
  Springston T2). What it cannot copy is the gas: an arc in the main-tank oil makes 1.6 times as much hydrogen as
  acetylene (twelve-month C2H2/H2 0.64), where the leaks bring diverter oil at 9.8 and 8.2. Construction: the gas per
  operation is held constant through the arc, the onset is just after the December 2024 sample, and Rolleston's tap
  changer follows the step loads of the processing plant on its feeder (its own random stream, so no other unit's
  draws move; plant seed chosen so all 18 grid columns keep the order with at least 5.3 per cent margin and the
  tracking r is at least 0.985 in every window and below-detection reading). Only RLS-T2's tap-operation figure moves
  in the goldens (27,534 to 49,897, still inside the interval). A first draw on the substation's ordinary load-swing
  switching, with the onset in January 2025, fell to r 0.884 from the last below-detection result and let Coalgate T1
  pass it on a 400-day base; both rejected.

- **Architecture 1 spent at round 1 (2026-10-11): screen grain (metering system against supply number).** Plain
  solver 81.3 and skeptic 85.6, both on Caithness 54 against Elgin 35. Plain: "rp_mart_weekly_import was rejected for
  screening because it sums each related point into its primary's metering system: mart = primary + related reads to
  within 0.2 kWh." Skeptic: "Supplies sheet (2,960 main MPANs) plus Related metering points sheet (699 heating-only
  MPANs, each with its own supply number) gives 3,659 supplies, matching the 3,659 MPANs in the reads parquet." The
  grain the procedure screens has to be filed for determinism, and once filed it is a work order: both rebuilt per
  supply from the reads and reconciled the mart before rejecting it. The ask devices (re-keyed jobs, appeals keyed to
  the raising system, the Scottish calendar, a mid-quarter start) were each executed off a filed rule. Not hardened:
  the only rung that would stop this step is a plant (withholding the glossary makes the grain a fork). Re-rooted.

- Seed AD03 as written (register split by each meter's switching regime, recovered from an operator acknowledgement
  corpus): the decisive rule withheld and recovered from a closed corpus is the capped Pattern B pin, and the
  acknowledgement file would refute the whole-house screen case by case (an alarm, not a stump).
- Register split from half-hourly data by time-of-use regime: if daily register reads ship the split is a lookup, and
  if they do not, the realistic route is the separate heating supply, which is how north-of-Scotland storage heating
  is actually metered, so the build uses related supply numbers.
- Account-level shortfall of heating diversions above 25 per cent (first parameter pass, heating 0.62 to 0.86 kWh per
  degree day): too close to the 30 per cent band for convergence across weather readings; heating sensitivity cut to
  0.42 to 0.62.
- Strathspey at 9 heating diversions tied Inverness City at 19 referrals, an ordering fork in the ranked chart; cut to 6.
- First cut of the pack (mart keyed by billing account and described as "the account's metered import", heating-only
  supply numbers listed inline on the Supplies sheet with a `related_mpan` column): the solver's-eye leak reader's plan
  of attack, before any solve, was "screen each MPAN separately, including the related heating-only ones" and "use the
  mart only as a sanity check, since it is per account". The decisive grain was announced by the file layout. The mart
  is now the metering-system table it would be at a supplier, keyed by the primary supply number, and the related
  metering points sit on their own CIS sheet, so the natural pipeline (Supplies sheet plus mart, or plus the reads) is
  keyed by supply number and silent everywhere. The same reader flagged RP-07's revision table (its two lines named the
  own-history degree days and the occupier window) and the DNO loss file ranking Lochaber top, echoing the belief; both
  rewritten.

- **Leak reader pass 1 on architecture 2 (2026-10-11), hardened before any solve.** The reader quoted nothing for
  question 1, but its plan of attack read "check that no code 3 rise looks like gas from the tap-changer compartment
  (1.2, 5.1)": the standard's scope sentence (the coding applies to the gases generated in the main tank), its
  clause on annual compartment sampling and the compartment results file together turned the attribution into a work
  order. Removed: the scope sentence, the sampling clause (and its revision-history mention) and the compartment file,
  which no ask needed. What stays filed is the remedy (5.1, an internal inspection is the remedy for a fault in the main
  tank) and the allocation to transformers whose main-tank gases point to such faults (5.2); the attribution rests on
  the tap-changer type, the counter tracking and the acetylene-to-hydrogen ratio, all of which the main call already
  reads for other reasons, and on IEC 60599, which the standard cites.

- **Section 5.2 reworded for determinism (2026-10-11).** With the scope sentence gone, section 4 codes the main-tank
  results as reported, so DSL-T1 and LST-T2 are code 3, and the old 5.2 ("the outages go to the transformers whose
  main-tank gases point to the most severe such faults") could be read as plain code 3 by severity, which lands rung 1.
  5.2 now allocates the outages "to the code 3 transformers with such a fault", the fault being 5.1's fault in the
  main tank, and the goldens report the literal section 4 code, so the code column has one reading and the slate turns
  only on where the fault is. The board paper says both stay code 3 and need tap-changer work instead.

- **Re-root candidates weighed for architecture 2 and not drawn (2026-10-11).** A heat-pump drop told from a diversion
  by its day and night registers, with the heating measures register as the convenient record: the register would be
  the narrower file the clean-data test repairs, so the defect would carry the stump. A weekly referral queue replayed
  run by run: a filed lifecycle is a filed formula, executed. Re-tampers hidden by a baseline that includes the earlier
  diversion: the use-versus-recorded distinction has to be filed in RP-07's glossary, which is where architecture 1 was
  read. Evaluating a new screen on a verification sample: inverse weighting is reflexive once the sampling is stated.
  Revenue protection was left for a transformer fleet, where the decisive step is a diagnostic attribution no filed
  sentence names.

- **Build of architecture 2 (2026-10-11), approaches dropped on the way to the shipped pack.** Leeston T2's last
  tap-changer service in February 2022 put both leaking units past their tap-changer interval (72,409 and 87,696
  operations), so the ask table pointed at the two tap changers the main call turns on; the service moved to May 2023
  (54,294, not past). Attribution signatures computed for every unit with detectable acetylene swept in stable traces
  (SBG-T1, GLT-T1) and the thermal units' crumbs, with C2H2/H2 undefined where hydrogen fell; the signatures are now taken
  only where acetylene rises faster than its rate limit. Thermal survey temperatures to the half degree collided with
  graded figures (33.1, 34.9, 12.5, 27.0, 28.5) inside a document; whole-degree maxima and fixed rises now, with a sweep
  asserting no graded figure in any shipped document. The extract log's "first hour 01/01/2021 00:00" against a parquet
  whose first timestamp reads 2020-12-31 11:00 announced the UTC export in one line; dropped. Interval-length confounding:
  with quarterly and monthly samples mixed, any steady gas source correlates with tap operations through interval
  length, so the vacuum unit's increments are designed in bursts and asserted uncorrelated raw and per day.
- **Severity distance "at least 0.005 from a two-decimal edge" (the build brief).** 0.005 is the half-width of a
  two-decimal bin, so only an exactly round severity meets it, which determinism-check reads as a receipt. Asserted at
  least 0.002 from the edge and at least 0.0003 off the round value instead (worst 0.0021, BNM-T1; naive 9.6415 and
  8.0674).
- **Personas the guard's people sweep read into the pack (2026-10-11).** The substation at Tai Tapu read as a person
  (first name Tai) and blocked against task123, and "Karl Fischer" in the water-content method line read as another
  persona; the substation is Ladbrooks (LDB) and the method line cites IEC 60814. No figure moved (per-unit draws are by
  fleet position, not by name).
- **Architecture 3, round 6 (2026-10-11): landed, proxy 81.6, decision harden (loop 1).**
  - **The solver's own sentence:** "Comparisons between different people ... give tasorexant 2.27 / 3.77 / 3.51,
    but tasorexant users already had 3.43 times the national rate in the year before starting and corinurad users
    0.60, so these mix up who starts the drug with what the drug does; rejected."
  - **Its landing step:** a self-controlled case series over all observed time, age-adjusted: corinurad 2.58 (2.10
    to 3.18), tasorexant 0.99, velaglutide 0.93.
  - **Why the between-person rungs fell:** the national-rate table lets a solver measure the channelling directly.
  - **Why the plain SCCS was enough:** it needed none of rung 3's exposure anchoring, because the event-dependent
    starts moved it only from 2.52 to 2.58.
  - **Stopping-rule count:** 1 of 2.

- **Hardening loop 1, the brief's contraindication at the shipped effect size (2026-10-11): rejected on its
  arithmetic.** Velaglutide starters' pancreatitis before the start thinned to a share q, measured on the simulated
  world with the self-controlled comparison over all observed time from 2018:
  - **The adjustment eats the deficit.** Every start sits in the last two years of a person's observation, so age
    bands (and the solver's age by calendar year) take up most of the step. At q 0.1: 3.02 unadjusted, 2.07 with
    five-year age bands, 1.97 with age by calendar year. At q 0 (no starter ever admitted with pancreatitis): 3.98,
    2.79 and 3.18, against corinurad 2.73, 2.59 and 2.55. No margin survives, and from 2022 velaglutide reaches only
    2.13 to 2.36.
  - **The alarms.** At q 0.05 and below, the comparison with days -365 to -31 alone reads 15 to 45 for velaglutide,
    and the 30-day profile shows nothing at all before the start.
  - **A 2024 to 2026 weight-loss boom helps but not enough.** It puts more of each starter's time before the start:
    q 0.015 gives 3.10, 2.98 and 2.89 (five-year bands, age by calendar year, bands with half-years), against
    corinurad 2.59, 2.55 and 2.57, which is 1.13 to 1.20 on an empty pre-start.
- **A lagged kidney injury to start dependence for corinurad (2026-10-11): rejected.** The idea was that an injury
  brings on a gout attack, and the attack gets urate lowering started 60 to 365 days later. Three times the start
  hazard deflated corinurad's all-time ratio only to 2.29, 2.24 and 2.23. It also painted kidney injury admissions
  before the start at twice the post-start level, the story of a medicine avoided in kidney disease turned upside
  down. Calendar adjustment still named corinurad.
