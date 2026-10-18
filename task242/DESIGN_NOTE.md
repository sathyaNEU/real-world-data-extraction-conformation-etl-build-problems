# task242 design note

Architecture 1, wave 3, seed DQ15 (whether an item's published prevalence carries a misclassification flag): the
seed's decision (which published prevalences carry the flag) and quantity (a prevalence corrected for the test's
sensitivity and specificity) only. The seed's survey world is the third survey pairing this wave would draw and its
pitfall (false positives ignored) is a formula executed, so the world moves to a city's dengue surveillance: the
Neithalpuram City Municipal Corporation (a fictional city in a southern Indian state) ran a post-season household
serosurvey in its 12 zones from 13 October to 7 December 2027 and published each zone's IgM-reactive share as its
dengue infection share for 2027 (indicator SERO-D1). Before the council's public health standing committee settles the 2028-29 vector-control allocation by
zone, the city epidemiology cell sets the quality flags on the indicators it publishes; a value that misstates the
quantity it stands for beyond the tolerance carries the misclassification flag.

## Draw

Card `cards/task242.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, each answered here:
repeat.gate_g and overuse.gate_g (method_or_model_selection against task469, a record-linkage dial, and in 8 of the
last 12: the key is the generic mechanism, the honest one for a choice between the panel's single sensitivity and the
sensitivity each zone's timing gives; no quantity or file is shared with any of them). test.same_puzzle_older and
test.same_driver_older (task229 v2, task461, task501 v4) and the nearest driver (task230 v2, 0.11) are differentiated
on the card.

- **Pairing.** Epidemiology & Public Health / disease-surveillance-outbreak-anomaly-detection, serving Data Quality
  Monitoring & Alerting. Not banned against the last three builds (task241, task469, task194). The object is the
  health of the surveillance programme's own published serosurvey indicator (whether each zone's value stands for
  what the indicator register says it measures), the call a monitoring decision: which values carry the flag.
- **Niche.** IgM serosurveys read recent infection: IgM to dengue appears around the fifth day of illness and fades
  over the following two to three months, so a post-season IgM survey sees a season's infections only through that
  window, and how much of a zone's season it sees depends on where the zone's epidemic sat against its fieldwork.
- **The call.** Which of the 12 zones' published 2027 dengue infection shares carry the misclassification flag (the
  share of residents infected since 1 January to their specimen's collection, estimated with the assay's measured
  accuracy, more than 1.5 times or less than two-thirds of the published value).
- **Shape.** 07, a grid of cells: one row per zone with its published share, the share infected since 1 January and
  the flag, beside the zone's columns for the asks (12 rows, the call picked per row), the flagged set, the chart
  (each zone's published and estimated share against the tolerance band, flagged zones marked) and the two files:
  well over 25 criteria before the rubric folds them. Decision designation_set, answer set_of_items, question form
  which.
- **Strategy.** composition_mix (the panel's sensitivity is the assay's curve averaged over the panel's own mix of
  days since onset; each zone's is the same curve averaged over its own mix, which its epidemic timing sets), G13
  decisive (the marker's window of detection against the indicator's window since 1 January), G6 (the mix of days
  since onset shifts from the panel to each zone), G14 (the sensitivity conditioned on days since onset); gap time
  first (when the infections happened against when they were read) then population (the panel's specimens are not
  the zones' infections); Gate G method_or_model_selection (a single sensitivity against the zone-specific one the
  data forces); calibration gold_standard_subsample (the laboratory's verification panel: sera from confirmed cases
  at known days since onset, and controls); context artifact published_series (the zone values the corporation
  published); layer 2 family field_method, pattern own:igm-serosurvey-attack-rate-through-the-detection-window.
- **Forum, event, organisation.** council_or_assembly (the corporation council's public health standing committee),
  budget_or_appropriation (the 2028-29 vector-control allocation by zone), local_government (a municipal
  corporation's public health department). All clear the last three.
- **People** (`guard.py names --geo India --seed 242`, locale en_IN): Vedika Varghese, the city epidemiologist who sets
  the quality flags; Shaurya Issac, the medical college microbiologist whose laboratory tests the survey's specimens
  and ran the kit's verification panel; Gauri Kant, the serosurvey's field coordinator; Onveer Acharya, the City Health
  Officer, who asks for the review.
- **Deliverables.** `dengue_igm_flag_review_2027.xlsx` (each zone's row: published share, estimated share since 1
  January, flag, Breteau index, household response rate) and `dengue_igm_flags_health_committee.pptx` (one slide: each
  zone's published and estimated shares against the flag's limits, flagged zones marked).
- **As-of.** Monday 10 January 2028: fieldwork closed on 7 December, the laboratory released the last results in mid
  December, the zone values were published in bulletin 52 of 2027, the case line list was extracted on 8 January, and
  the standing committee meets on 24 January.
  The call is retrospective by nature (a quality flag says whether a published value stands for its quantity, and the
  quantity is the season's infection share); what it settles is which values reach the committee with the flag.
- **Data-native sentence.** The zones were surveyed one after another from mid October to early December while their
  epidemics peaked anywhere from August to November (some zones carried both the south-west and the north-east monsoon
  waves), and the assay finds IgM in nearly every infection in the first six weeks after onset and in few after three
  months; so the share of a zone's 2027 infections still detectable at collection is set by where its own epidemic
  curve sat against its fieldwork, which the laboratory's panel, built from cases at follow-up visits, cannot carry.

Sources, one line each (what it teaches; how this build differs):
- Rogan and Gladen (1978): an apparent prevalence corrected for the test's sensitivity and specificity; here the
  sensitivity that enters is not the assay's alone but the assay's curve over the population's own days since onset.
- Recent-infection incidence assays (the mean duration of recent infection, Kassanjee and colleagues, 2012):
  incidence read from a marker whose detection fades with time since infection; their steady-state shortcut fails in
  an epidemic season, so here the curve is carried through each zone's epidemic, never named in the pack.
- Dengue IgM kinetics (WHO dengue guidelines, 2009: IgM from about day five, detectable for two to three months): the
  world's structure, generated, never a real dataset.
- Post-outbreak IgM serosurveys estimating attack rates: the field's practice; the timing correction is the analyst's
  to find from the panel and the case line list.

## Default path

1. Read the indicator register and SOP-EPI-07: SERO-D1's published value is the share of tested residents with a
   reactive IgM; it stands for the share of the zone's residents aged one year and over infected with dengue between 1
   January 2027 and the collection of their specimen; the M flag goes on when that share, estimated with allowance for
   the test's misclassification as the laboratory measured it, is more than 1.5 times or less than two thirds of the
   published value.
2. From the laboratory's verification panel: sensitivity is the reactive share of the confirmed-case sera collected
   from the fifth day of illness on (0.708; pooled over every case serum 0.677, over the kit's 5 to 60 days 0.868),
   specificity the non-reactive share of the 300 control sera (0.9867).
3. Each zone's published value from the results file (reactive over tested), matching the bulletin's Table 1.
4. The Rogan-Gladen estimate (p + Sp - 1) / (Se + Sp - 1) for each zone, and its multiple of the published value.

Ends on: no zone flagged (every multiple between 1.00 and 1.30 at 0.708; 1.05 to 1.37 pooled; 0.82 to 1.06 over the kit
window).

Golden: six zones flagged (Melmangalam, Vadakkupatti, Velliyanur, Chinnakulam, Periyamalai, Sengalur), from each zone's
effective sensitivity: the panel's sensitivity by days since onset averaged over the zone's cases by onset date from 1
January up to each specimen's collection, then over the zone's tested residents.

## Stump sentence

A competent analyst corrects each zone's published IgM share by the Rogan-Gladen estimator with the laboratory panel's
sensitivity from the fifth day of illness on (0.708) and its specificity, puts every zone between 1.00 and 1.30 times its
published value and ends on no zone flagged; the step that lands it there is taking the panel's sensitivity as the
assay's sensitivity in every zone, when the zones surveyed months after their epidemic had most of their 2027 infections
past the weeks in which IgM is found, so only the panel's curve averaged over each zone's own onset dates up to
collection gives the six.

## Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves Data
  Quality Monitoring & Alerting (the surveillance programme's own published indicators are the monitored data, the
  misclassification flag the monitoring decision).
- **Domain test:** the quantity that decides is each zone's dengue attack rate since 1 January, estimated from IgM
  serology the way serosurvey epidemiology estimates incidence from a recent-infection marker: the assay's detection
  curve by days since onset (the laboratory's panel) averaged over the zone's own epidemic curve (cases by onset date)
  up to each specimen's collection, then the Rogan-Gladen correction with that effective sensitivity and the panel's
  specificity.
- **Swap:** "which zones' published dengue infection shares carry the misclassification flag" rewritten as "which
  wards' published bed-occupancy shares carry the flag" with admissions for infections: there is no antibody whose
  detection fades after the event and no epidemic curve to carry it through, so the effective sensitivity has nowhere
  to come from and the task stops making sense; with megawatt-hours the same.
- **Layer 1:** the case line list (fed by hospitals, primary health centres and laboratories) carries day-month-year
  dates, onset and notification dates days apart, the 2026 season's tail, non-residents treated in city hospitals,
  repeat notifications of one case and zone names spelt as each reporting unit writes them; the panel export gives onset
  and collection dates rather than days since onset, with grey-zone readings repeated; the survey's specimens were
  collected across each zone's eleven-day fieldwork. Each is produced by the system that records it; none is placed to
  be caught, and the call is the same under every handling of each (SF1 to SF11, L1 rows in checks.py).
- **Layer 2:** field_method: the effective sensitivity of a fading recent-infection marker for a cumulative attack
  rate, the assay's curve carried through each zone's own epidemic timing, against the panel's single sensitivity.
- **Decisive step:** taking each zone's sensitivity as the panel's sensitivity by days since onset weighted by the
  zone's distribution of days since onset at collection, which the zone's epidemic curve gives, rather than one
  sensitivity for every zone (pooled over the panel, over a fixed window, or at a single day since onset).
- **Not semantics:** reading every field right (onset and collection dates, results, zones, the window since 1
  January) still leaves the single-sensitivity correction on no zone flagged: the panel's dates are plain dates, and
  reading them right does not say how the zones' timing enters.
- **Not rule application:** the indicator register files what the value stands for and SOP-EPI-07 files the tolerance;
  no filed rule or procedure says how the infection share is estimated from IgM results, so executing every stated rule
  with the panel's sensitivity files no flag.
- **Analyst test:** a strong analyst who reads every file right and applies the flag rule as filed corrects each zone's
  IgM share by Rogan-Gladen with the panel's sensitivity from the fifth day on (0.708) and its specificity, puts every
  zone between 1.00 and 1.30 times its published value and ends on no zone flagged, where the golden flags six; on the
  simulator's clean truth the same route flags none and the decisive step alone gives the six (R3a, R3b in checks.py).
- **Estimand:** the indicator register (`epi_cell_indicator_register.xlsx`, row SERO-D1) defines the zone value's
  quantity (the share of the zone's residents aged one year and over infected with dengue virus between 1 January 2027
  and the collection of their survey specimen) and the published value (reactive over tested); SOP-EPI-07
  (`sop_epi_07_quality_flags.pdf`, flag M) files the comparison and the tolerance (estimated share more than one and a
  half times or less than two thirds of the published value).
- **No decoy:** nothing is planted: no memo, draft or stakeholder figure argues a sensitivity or a flag; the panel is
  the laboratory's own verification export with no headline sensitivity; the bulletin's values are the figures under
  review, and no file ranks the zones on the flag.
- **No certified replay:** no certified or published 2027 attack rate exists for a method to reproduce; the method is
  found from the panel's structure and the zones' timing.
- **Lesson:** an IgM serosurvey measures a season's infections only through the marker's window, so its sensitivity
  for a cumulative attack rate depends on each population's epidemic timing against its fieldwork; no build on file
  reads a share through a detector whose sensitivity fades with the time since the event (task233 carries a gold
  standard's departure across base rates; task241 reads a sensor against a moving reference).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) one sensitivity from the panel (from day 5, pooled, or the kit's 5 to 60 days): none | SOP-EPI-07 says allowance for the test's misclassification as measured | arm and result columns | yes, Rogan-Gladen with the validation's sensitivity | none | no | one ratio | readable |
| 1 the city's epidemic curve for every zone: nine | none | the line list's onset dates | partly, a timing-aware analyst who pools the city | none | no | a weighted mean | readable |
| 2 one day since onset per zone (median four, peak five, mean seven) | none | onset dates | yes, a typical lag read off the panel | none | no | one lookup | readable |
| 3 a fixed window of 60 or 90 days times the kit's sensitivity: seven or three | none | onset dates | yes, IgM detectable for about three months | none | no | one share | readable |
| 4 (decisive) the panel's curve averaged over each zone's cases by onset up to each specimen's collection: six | no sentence names sensitivity by day, timing, a curve or a weighting | no days-since-onset column; onset and collection dates are ordinary columns | no: the reflex takes one sensitivity | no control, published sensitivity or earlier estimate | no | not linear: a curve, an average per resident over the zone's cases, then Rogan-Gladen | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | cases (repeat notifications) | every notification row of a resident | one per zone, onset, age and sex | same call | same call (asserted) |
| SF2 | zone of residence | every spelling mapped to its zone | the official spellings only | same call | same call (asserted) |
| SF3 | dengue cases | confirmed and probable | confirmed only | same call | same call (asserted) |
| SF4 | when an infection happened | onset date | notification date | same call | the dictionary; same call (asserted) |
| SF5 | the collection of their specimen | each resident's date | the zone's middle fieldwork day | same call | the register; same call (asserted) |
| SF6 | residents aged one year and over | every tested resident | none differs | converge | the protocol's eligibility; every tested resident is 1 or over (asserted) |
| SF7 | the published value | reactive over tested | the bulletin's one-decimal share | same flags | same call (asserted) |
| SF8 | more than 1.5 / less than two thirds | strict | inclusive | same call | no multiple within 0.15 of a limit (asserted) |
| SF9 | the test's results on the panel | final reading | first reading, grey zone negative | same call | the cover note; same call (asserted) |
| SF10 | specificity as measured | all 300 controls | blood donors only | same call | same call (asserted) |
| SF11 | specificity as measured | all 300 controls | febrile controls only | same call | same call (asserted) |
| SF12 | between 1 January 2027 and collection | cases with onset from 1 January | the line list from October 2026 | another set (nine) | the register's window, word for word (asserted) |
| SF13 | shares | per cent of residents | proportions | same call | the prompt's unit |
| SF14 | the estimate | Rogan-Gladen, positive in every zone | a negative estimate | converge | every reactive share exceeds the false positive rate (asserted) |
| SF15 | allowance for the test's misclassification | sensitivity and specificity as the laboratory measured them | sensitivity alone (specificity taken as 1) | another set (Kottaivayal added) | SOP-EPI-07's "the test's misclassification as the testing laboratory has measured it": the laboratory measured specificity on 300 control sera (asserted) |

## Ladder

Four wrong rungs and the golden, each a defensible way to correct a zone's IgM share, each dying to one fact of the
record (figures on the cut pack, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | one sensitivity from the panel: from day 5 (0.708), pooled (0.677) or the kit window (0.868) | none flagged (multiples 0.82 to 1.37) | the panel's sensitivity runs from 0.92 at two to four weeks to 0.46 at 75 days and 0.04 at 120; its mix of days is the clinic's, not a zone's |
| 1 | the city's epidemic curve averaged at each resident's collection | nine: Puthanpalli, Kizhakkoor, Kottaivayal and Aranmanai in, Velliyanur out | the zones' epidemics peaked from August to November; the city's curve is no zone's |
| 2 | one day since onset per zone: median, peak or mean | four (median), five (peak, Puthanpalli in), seven (mean, Kottaivayal in) | Vadakkupatti and Sengalur had an August wave and a November one; Kottaivayal a January wave; a single day stands for neither |
| 3 | a fixed window (60 or 90 days) times the kit's sensitivity | seven (60 days, Puthanpalli in) or three (90 days, Melmangalam, Periyamalai and Velliyanur out) | the panel shows no edge: 0.59 at 60 days, 0.46 at 75, 0.15 at 90 |
| 4 (golden) | the panel's curve averaged over each zone's cases by onset up to each resident's collection | six | |

- **Margins.** The flagged six stand at 1.85 to 3.28 times their published value; the largest of the other six is 1.29
  (Puthanpalli). Every reasonable implementation (steps, fixed bins, a fitted rise and fade, a kernel; confirmed cases
  only; repeat notifications dropped; each zone at its middle fieldwork day) files the same six, its flagged multiples
  above 1.76 and the rest under 1.34, and moves no estimated share by more than 5 per cent down or 10.2 per cent up.
- **Position.** The six are reached by no other rung: single sensitivities file none, the city's curve nine, a single
  day four to seven, a fixed window three or seven.
- **Dominance.** The decisive move takes every flagged zone from under 1.37 to 1.85 or more, and leaves the other six
  under 1.30.
- **Grid.** One sensitivity from day 5, pooled, the kit window or the first readings (none); the city curve (nine);
  median, peak or mean day (four, five, seven); 60 or 90 days (seven, three); the window opened to October 2026 (nine,
  another quantity); each zone's own curve by any of seven implementations (six). On the simulator's clean truth the
  single pooled sensitivity flags none and the zones' own timing gives the six (R3a, R3b).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | residents aged one year and over (register); every tested resident in the results file is (SF6) |
| 2 | Unit of account | one zone's published value and its estimated share (register, SOP-EPI-07) |
| 3 | Attribution window | infections from 1 January 2027 to each specimen's collection (register; SF12) |
| 4 | As-of dating | files received 10 January 2028; the line list extracted 8 January, a month after fieldwork closed |
| 5 | Version basis | the panel's final readings (SF9); the published value is the results file's reactive over tested (SF7) |
| 6 | Denominator | the zone's tested residents, for the published value and the estimate alike |
| 7 | Weighting | each tested resident equally within a zone; the zone's cases equally within the curve |
| 8 | Window length | from 1 January to each resident's collection (SF5, SF12) |
| 9 | Boundary inclusivity | more than 1.5 or less than two thirds; no multiple within 0.15 of a limit (SF8) |
| 10 | Rounding path | estimates from unrounded figures, one decimal at the close; no flag depends on rounding (SF7) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every onset before 7 December notified by the 8 January extract (the longest notification delay is under a month) |
| 13 | Order of operations | panel curve, each resident's sensitivity over the zone's curve, the zone's mean, Rogan-Gladen, the multiple, the flag |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | repeat notifications kept or dropped: same call (SF1); exact repeat rows in the asks' files dropped |
| 16 | Identity normalisation | zone spellings mapped to the 12 zones (SF2); non-residents out |
| 17 | Netting against gross | not applicable |
| 18 | Dimensional units | shares in per cent of residents; days since onset in days |
| 19 | Code and status semantics | REACTIVE and NON-REACTIVE final; CONFIRMED and PROBABLE (SF3); call outcomes 1 to 6; LOCKED |
| 20 | Integerisation | none for the call; whole households and containers for the asks |
| 21 | Clause scope | flag M applies to values computed from a diagnostic test; SERO-D1 is one (SOP-EPI-07) |
| 22 | Forward window contents | nothing is forecast; the committee's 2028-29 allocation is the value's use |

## Literal reader

Executing the prompt, the register's SERO-D1 row and SOP-EPI-07's flag M word for word: each zone's published value is
its tested residents' reactive share; the quantity it stands for is the share of the zone's residents aged one year and
over infected between 1 January 2027 and their specimen's collection; the flag goes on when that share, estimated from
the same data with allowance for the test's misclassification as the laboratory measured it, is more than one and a
half times the value or less than two thirds of it. The literal estimand needs the chance that an infection since 1
January still reads reactive at collection, which the panel gives by days since onset and each zone's cases give by
onset date; that reading files the six under every reasonable implementation, and the easy answer, none, comes from an
easy method on the same literal estimand (one sensitivity for every zone), never from another reading: every row of
the fork table files the six except SF12's window opened to October 2026, which the register's own words rule out.

## Oracles

None for the call: no published sensitivity, earlier attack-rate estimate or flag list ships; the bulletin's Table 1
is the published values under review and ties to the results file under every handling (asserted); the panel's cover
note gives no figure. For the asks, no published Breteau index or response rate ships; SOP-VC-02 defines the index and
the round's inspection and the protocol the response rate, and neither says anything about ward numbers, cool boxes or
rejected specimens.

## Ask sheet

**Ask A, each zone's Breteau index for the November 2027 round** (12 figures). H18: the larval index each zone
carries beside its value in the committee's table, which allocates vector control by zone; the call does not read
inspections. Use: the City Health Officer's request. Primary device D7 (codes reissued to other entities: the forms
dated before 16 November carry the ward numbers of the earlier ward map, and the 2027 map numbered its 192 wards afresh
from Velliyanur round the city, so every earlier number is a current ward in another zone; nothing on a form marks the
scheme, and the ward master's former_ward_nos and the premise's assessment number (zone first) corroborate);
hazards: LOCKED calls written as zero containers (SOP-VC-02 says they are not inspections), follow-up forms for
positive houses about a week later (the latest-form reflex keeps them), rows the inspectors' app sent twice. Path: the
inspections, the ward master, SOP-VC-02, the dictionary (4 files, 11 columns: record_id, inspected_on, ward_no,
premise_id, wet_containers, positive_containers, source_reduction, remarks, the master's ward_no, zone,
former_ward_nos). Stops: ward number on the current map, first inspections -3.8 to +5.2; current map, every form -2.4
to +5.9; current map, last form -12.7 to -4.3; zone right, a locked call as the first form -1.6 to -0.6; zone right,
every form +0.5 to +2.8; zone right, last form -12.8 to -5.3. Realism: Indian cities redraw and renumber wards, and
field forms switch to the new numbers on a date while property records keep the old ones.

**Ask B, each zone's household response rate** (12 figures). H18: the reliability of each zone's value, which the
committee will ask about; the call does not read the sample, the field app export or the laboratory register. Use: the
City Health Officer's request. Primary device D4 (absence as the signal, evidenced in a file no habitual join reaches:
the cool box from one of each zone's last fieldwork days reached the laboratory warm, most of its sera were haemolysed
after the team had moved on, so households whose every specimen was rejected have no row in the results file; the
laboratory register holds them as REJECTED); hazards: completed interviews where nobody gave blood (the outcome code
reads as a response), sampled households never called on (absent from the export; the protocol keeps them in), the
tablets' submissions sent twice. Path: the sample, the field app export, the laboratory register, the results, the
protocol, the dictionary (6 files, 10 columns: household_id, zone, start, visit_outcome, _id, barcode, condition,
action, specimen_id, collected_on). Stops: a tested resident as the response -4.1 to -1.2; a completed interview +2.3
to +7.6; the export's households as the denominator +0.4 to +1.4; both slips -2.8 to -0.3. Realism: haemolysis from a
warm box is the commonest field loss in serosurveys, and a team that has left a zone does not go back for one sample.

Main population zero-counts: the call's rows are the line list's resident cases, the results file's tested residents
and the panel's sera; no inspection, ward, sample, call or register row is among them, the results file holds only
accepted specimens (asserted), and the call computed without any ask file is the same (asserted); every Layer 1 slip
keeps the six (SF1 to SF11, L1 rows).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| ward numbers of the earlier map (D7) | A | +5.2 / -3.8 |
| LOCKED calls as zero-container forms (D4 sentinel) | A | -1.6 |
| follow-up forms (D1, latest-record reflex) | A | -12.8 |
| rows sent twice by the inspectors' app (D1) | A | under 0.1 |
| households whose every specimen was rejected (D4) | B | -4.1 |
| completed interviews without blood (D5) | B | +7.6 |
| households never called on (D4) | B | +1.4 |
| submissions sent twice (D1) | B | 0 at the household grain |

Referee: the premise's assessment number for the zone; the laboratory register for who gave blood.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, zones I to VI | exact repeats dropped, LOCKED calls and follow-ups set aside as SOP-VC-02 says, the ward number joined to the ward master | miss |
| Ask A, zones VII to XII | the same | miss |
| Ask B, zones I to VI | the protocol's definition executed with the results file as who gave blood, the sample as the base | miss |
| Ask B, zones VII to XII | the same | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 0 of the 24 ask figures, Lc 0; the mirror (stopped
at one sensitivity for every zone) keeps 0 of 24 whether careful or careless on the asks, Ls 0, and about 18 of the 38
recommendation points (the six unflagged zones' flags, five estimates its single sensitivity lands within the band,
the published shares).

Pair ceiling: 35.1 ((38 + 7 + 55 x 0) and (18.2 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each zone's dengue attack rate since 1 January, estimated from IgM serology through the
   assay's detection by days since onset and the zone's own epidemic curve; with hospital beds or megawatt-hours in
   place of residents and infections there is no antibody kinetics and no epidemic curve, and the task stops making
   sense.
2. Two layers: Layer 1 (the line list's day-month-year dates, spellings, 2026 tail, non-residents and repeat
   notifications; the panel's onset and collection dates and grey-zone repeats; collection across each zone's
   fieldwork) is neutral on the call: every slip keeps the six (SF1 to SF11, L1 rows). Layer 2 is each zone's
   effective sensitivity, asserted alone to move the default path to the golden on the simulator's clean truth (R3b).
3. No banned stump decides: nothing is planted (no headline sensitivity, earlier estimate or flag list ships); not
   semantics (every field read right, one sensitivity still flags none, R3a on the clean truth); not rule application
   (the register and SOP-EPI-07 file the estimand and the tolerance and name no method, asserted on their text).
4. Gate G: no shipped artifact ranks the zones; the bulletin's Table 1 is the values under review; the rain gauges and
   the fogging log carry no serology.
5. Determinism: the six hold under every reasonable implementation (steps, bins, a fitted rise and fade, a kernel,
   confirmed cases only, repeat notifications dropped, each zone at its middle day); flagged multiples 1.85 to 3.28, the
   rest at most 1.29; estimates graded within 15 per cent against an implementation spread of -5 to +10 per cent; the
   asks' figures sit at least 0.002 from a rounding edge; 15 fork rows asserted; the verifier recomputes by its own
   route (fixed bins) and reads back every format the pack ships.
6. Fingerprint: heart WARN (repeat.gate_g, overuse.gate_g, repeat.question_form, answered under Draw); surface
   promotes task241 and task240 (a shared README name; with task241 the same decisive gap and decision type, the pattern
   and Gate G different) and task501, task229 v2 (differentiated on the card); personas clean.
7. Judge (one isolated thread, Sonnet, medium, the bundle and the graded blocks only): pass 1 DETERMINISTIC, APPROVE,
   every figure reproduced (the six, all 12 estimates, the Breteau indices from 13,250 houses, the response rates from
   2,037 households); single sensitivities of 0.677, 0.708, 0.868 and 0.944 flag none; specificity ignored adds
   Kottaivayal (SF15 added on its note); the window opened to October 2026 flags nine (SF12); Gate G
   method_or_model_selection, analytical_non_defect; Gate H domain, layers and decisive step pass; spec gates all pass.

## Leak check

- leak.py: REVIEW, no LEAK. The published shares appear in the bulletin because they are the values under review; the
  documents' shared vocabulary is the field's own (survey, register, specimen, fieldwork); dates clean against 10
  January 2028.
- Reader 1 (Sonnet, medium, the prompt and a fresh unzip only): question 1 none; question 2 none; question 3 none (the
  README and the dictionary are ordinary handover files); question 4 none; question 5 every quoted sentence executes to
  the golden, and its own run with ten-day bins files the same six; question 6 an analytical choice (one sensitivity
  flags nothing). Realism: the cover note's list of panel features read as tidy (trimmed); the PDFs now carry subject
  lines of their own.
- Reader 2 (after those two document fixes, a fresh unzip): questions 1, 2 and 4 none; question 5 every sentence
  executes to the golden; question 6 an analytical choice. It read the request email, the README and the dictionary as
  analyst help (they are the City Health Officer's message and the folder's ordinary handover files) and a run-validity
  line as mildly pointed (a laboratory's standard line); harmless, one line each in the leak report.

## Tried and rejected

- The seed's pitfall (false positives ignored in a rare trait's prevalence): executing the Rogan-Gladen formula is
  rule application; it stays as a lower rung every route shares; dropped as the stump at the draw.
- The seed's survey world: a third survey pairing in this wave (task238, task240); dropped at the draw.
- Two-phase validation of a register flag (a validation subsample weighted back to the register): its honest label is
  population_selection, banned against the last three builds; dropped at the draw.
- Transporting a test's sensitivity and specificity from the validation population to another prevalence: too close
  to task233 (a departure carried across base rates) and task230; dropped at the draw.
- Brazil as the world: the surveillance system's records and documents would be in Portuguese; the district and city
  framings of an English-language surveillance system in India kept the field, and the city corporation clears the
  organisation-family ban (a state government agency repeats task159); dropped at the draw.
- A kit insert stating the assay's sensitivity: an official figure that gives the wrong answer is an official decoy;
  the panel ships as the laboratory's raw export with a cover note and no headline figure; dropped at stage 2.
- A panel weighted to late visits: its pooled sensitivity put the single-sensitivity route at 1.48 times, a hair under
  the limit; the panel follows the clinic's visit load, more sera in the first month; dropped at stage 2.
- The new ward map numbered in the old order: only boundary wards changed zone and two zones' indices came out equal
  on the wrong join; the 2027 map is numbered from Velliyanur round the city; dropped at stage 2.
- A warm cool box on a random fieldwork day: three zones had no household whose every specimen was rejected, so their
  response rates matched on the results file; the warm box falls on one of each zone's last days, after the team had
  left; dropped at stage 2.
- A two-wave zone left as the only case where the mean day misled: the mean-day rung landed on the six once the panel
  was rebalanced; Kottaivayal carries a January wave (the tail of the 2026 monsoon season) that drags its mean back;
  dropped at stage 2.
