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
Forum: regulator_or_inspector (the agency's medicines safety committee opens the formal assessment)
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

## LADDER (planned; each rung asserted by name in `generator/checks.py`)

| Rung | Construction | First | Target margin | Killed by |
|---|---|---|---|---|
| 0 | Spontaneous reports per signal in the quarter (the screen) | tasorexant falls | most reports | reports are not incidence; the screen raises signals, it does not confirm them |
| 1 | New users against matched non-users, 30-day admission rate ratio, crude and adjusted for recorded comorbidities and prior admissions for the event | tasorexant falls | first by 1.3 or more in every variant | channelling: the users fell (and the uricosuric's users had kidney injury) at their own rates before starting |
| 1b | Observed in the 30 days after the start against expected from the age- and sex-specific population rates | tasorexant falls | first by 1.3 or more | as rung 1 |
| 2 | New-user active comparator (tasorexant against zopiclone starters, corinurad against allopurinol starters, velaglutide against orlistat starters), crude, adjusted and propensity-weighted | tasorexant falls | first by 1.3 or more in every variant; corinurad 1.4 or less | the new sleep medicine is channelled to the frailest; the uricosuric to the healthiest kidneys |
| 3 (answer) | Self-controlled: each new user's days 1 to 30 after the first dispensing against the same person's later time on it (exposure-anchored control window), conditional Poisson | **corinurad acute kidney injury** | rate ratio 2.2 or more in every cell; tasorexant and velaglutide 1.25 or less with intervals spanning 1 | |

Evidence the pack carries for the judge (asserted): tasorexant starters' fall admission rate in the year before the start
is about four times matched non-users' and about twice zopiclone starters'; corinurad starters' kidney injury rate in the
year before the start is about half allopurinol starters'.

## GRID (planned, asserted cell by cell)

Self-controlled cells (all give corinurad): risk window days 1 to 30, 0 to 30 or 1 to 28; control window days 31 to 180,
61 to 180, 61 to 365, or all observed time after day 30 (exposure-anchored), plus the full-observation case series with a
30-day pre-exposure window removed; with and without five-year age bands and calendar half-years; estimator conditional
Poisson maximum likelihood or the Mantel-Haenszel ratio. Naive cells (all give tasorexant): matched non-users crude and
adjusted (comorbidity sets: none, Charlson groups, Charlson plus prior admission for the event), population
observed-against-expected, active comparator crude, adjusted and propensity-weighted. Variants: observation from 2022 or
2023; deaths and emigrations ending observation or not; transfers merged within 24 hours or treated as separate
contacts. Every cell keeps its winner.

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

## ASK SHEET (planned)

| Ask | Figures | Depends on the call |
|---|---|---|
| The signal the committee opens (note) | 1 | yes |
| For that signal: the rate ratio for the 30 days after the start, with its 95 per cent interval (note) | 3 | yes (the golden carries the self-controlled band the grid spans) |
| For that signal: admissions with the event in the 30 days after a start in 2025, and how many the medicine caused (note) | 2 | yes |
| New users per medicine and calendar year, 2022 to 2025 (`new_users_by_year.csv`) | 3 x 4 = 12 | no (Layer 1: the new-user rule, the ATC reassignment, residence, reversed dispensings) |

Ask stops (each asserted to move its figures): the current ATC code only (corinurad's 2022 and 2023 users vanish);
the washout ignored; reversed dispensings counted; transfers counted as separate admissions; secondary diagnoses counted
where the case definition says action diagnosis; deaths and emigrations not ending observation.

## PINS (planned)

SOP-PV-14 (the agency's signal refinement procedure, filed as a PDF): the case definitions (falls: an emergency or
inpatient contact whose action diagnosis is an injury, DS00 to DT14, with a fall code among its diagnoses; acute kidney
injury: an inpatient contact with DN17 as action or secondary diagnosis; acute pancreatitis: an inpatient contact with DK85
as action diagnosis; contacts of one admission linked by transfer count once), the new-user rule (365 days without the
substance, by substance across code changes), the 30-day window from the first dispensing, the end of observation
(death, emigration, 30 June 2026), and the committee's question in section 1 ("a signal is supported when starting the
medicine raises the risk of the event in the month after the start"). It names no comparison group and no design.
Registry extract notes: field semantics, the D prefix, the 2019 structure change, the ATC reassignment, the matched
comparator extract's matching rule.

## PACK (planned; the builder may rename within the organisation's own conventions)

1. `pv_signal_screen_2026Q3.xlsx` (context artifact: the screen's disproportionality table and the line listing of
   reports for the three signals; correct, labelled as reports)
2. `SOP-PV-14_signal_refinement.pdf` (pins)
3. `registry_extract_notes.md`
4. `prescription_registry_2018-2026.parquet` (dispensings of the six substances and the co-medication groups)
5. `patient_registry_contacts_2018-2026.parquet` (spine: hospital contacts of every person in the extract)
6. `patient_registry_diagnoses_2018-2026.parquet` (diagnoses per contact)
7. `civil_registration_extract.csv` (birth year, sex, death, emigration, immigration)
8. `matched_comparators.csv` (the agency's standard matched non-user extract)
9. `atc_ddd_index_2026.csv` (substances, ATC codes with validity dates, DDDs)
10. `population_by_age_sex_2022-2025.csv` (population denominators)
11. distractor: `psur_summary_tasorexant_2026.pdf` (the company's periodic report summary: exposure estimates and
    cumulative reports; same world, nothing it states decides the call)
12. distractor: `committee_minutes_2026-07-09.md` (the previous meeting's minutes on other medicines)

Goldens: `golden/signal_refinement_note.docx` and `golden/new_users_by_year.csv`.

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
