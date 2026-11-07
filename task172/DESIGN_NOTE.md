# task172 design note (architecture 2)

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task172.json`, architecture v2, registered 2026-10-31 and filed anew after
  the design screens (guard check WARN only: the question form repeats task191's, and the lineage shell repeats
  task256 v1's).
- **Pairing:** Biomedical & Clinical Research, task type `survival-time-to-event-analysis`, objective Forecasting &
  Predictive Modeling; biomedical x forecasting is a pairing no build has drawn.
- **Niche:** TALON-2, an investigator-led, charity-funded phase 3 trial coordinated by the Kesterton University Cancer
  Trials Unit (KUCTU), randomises patients with advanced biliary tract cancer 1:1 to ravolimab (an investigational
  immune checkpoint antibody from Halvorsen Therapeutics) or placebo, each with gemcitabine and cisplatin. The primary
  endpoint is progression-free survival assessed by blinded independent central review (BICR); the final analysis is
  the stratified log-rank test at 330 events. The Ashgrove Cancer Research Trust funds the trial in two tranches, and
  Schedule 2 to its funding agreement sets three bands on the interim conditional power: below 20 per cent the
  funding ends (stop for futility), from 20 to below 80 per cent the Trust funds an extension to 420 events, from 80
  per cent the trial continues to 330 events as planned.
- **Quantity:** the conditional power the DMC charter defines in section 4.1: the chance that the final stratified
  log-rank test at its 330th event rejects at one-sided 2.5 per cent, given the interim data, for the trial as it will
  run from the cut, with each arm's progression over the remaining follow-up as the interim data estimate it. Forward
  facing: the final analysis's events have not happened.
- **Decision:** continue as planned (golden, band C), extend (band B) or stop for futility (band A).
- **Shell:** question form whether (a gate with three outcomes), second-sentence opener "The", rounding opener "The",
  deliverables pdf+csv.
- **Setting:** first patient randomised 1 December 2025, last 25 September 2026 (all 450); the interim cut is
  17 November 2026, the date of the 165th BICR-confirmed event; the snapshot is 1 December 2026 and the DMC meets on
  9 December 2026.
- **Data-native sentence:** an event-driven look at half the information arrives while most patients have had only
  their first two or three scans, so the events it holds are early-follow-up events, and the events the final
  analysis still needs come from the same patients later in their follow-up: the look and the remainder sample
  different stretches of each patient's own clock.

## Survivor anatomy

Actor: the deciding property is where each patient still at risk at the cut stands in their own follow-up against the arms' change in progression rate between the week-12 and week-18 assessments, and no file stores it: the BICR export lists reads by timepoint, the IRT export randomisation times in UTC, the status workbook deaths and withdrawals, and the follow-up still to come is a forward relation across those files that no column holds (no column holds a follow-up period, an interval rate, a projected event or an effect estimate).

Link: the signal is read through a comparison the field's conditional-power route never asks for: each arm's events per patient-month at each assessment visit (BICR timepoints crossed with every patient's exposure, built from UTC randomisation times converted to the site's local date through the site register) set against the follow-up position of every patient still at risk; the B-value takes one z and one ratio, and no key, column or sentence crosses the interim's events with the at-risk set's future.

Reflex: the field's method for the deciding quantity sits at rung 0 and files a wrong answer here: conditional power from the B-value with the stratified log-rank z (or the stratified Cox ratio) as the trend gives 5.3 per cent, band A; its patient-by-patient version under one ratio gives 8.7 per cent and one constant rate per arm 13.6 per cent, both band A; the sample-size ratio the charter excludes gives 53.8 per cent, band B.

Back-test: the textbook route validates on the checks a DMC statistician runs before the conditional power: the stratified log-rank z and the stratified Cox ratio agree (0.58 and 0.91, 95 per cent CI 0.67 to 1.24), the eCRF strata, the UTC dates and the not-evaluable censoring rule each leave the band where it is, and the investigator reads point the same way; what separates the routes is a cut no step of the B-value route makes, the events per patient-month by assessment visit read against where the remaining patients stand.

Second use: every file the decisive step reads sits in the pack for a reason of its own: the BICR export, the IRT export and the status workbook are every rung's data (the event count, the cut, the log-rank test, the Cox ratio), the site register converts every randomisation time and names every site's central laboratory, and the charter, the SAP and Schedule 2 file what every rung computes and compares; deleting the decisive step drops no file.

Shock: the movement the step recovers reads as ordinary: the stratified ratio's confidence interval spans 0.67 to 1.24, ravolimab's early excess at the week-6 and week-12 assessments sits within what a 165-event look carries, and an immunotherapy added to chemotherapy whose arms run together for the first scans is the field's familiar picture; sorted on any shipped statistic (by arm, stratum, site, country or month of randomisation) nothing singles the later follow-up out.

Pins: the charter files the WHAT in its own genre (section 4.1: the stratified log-rank test of BICR progression-free survival at its 330th event, one-sided 2.5 per cent, given the interim data, for every patient still at risk and every patient still to be randomised followed to the 330th event, with each arm's progression over that remaining follow-up as the interim data estimate it, not under the sample-size ratio); Schedule 2 files the bands; no filed sentence names a follow-up period, a change in rate, a ratio that varies, proportional hazards, a model or a crossing (asserted on all three PDFs in checks.py).

## Default path

1. From the DMC charter (section 4.1 and Appendix A) and Schedule 2: the conditional power of the final stratified
   log-rank test at 330 events, one-sided 2.5 per cent, given the interim data, compared with the bands (below 20 per
   cent stop, from 20 extend, from 80 continue as planned); from the SAP, the PFS definition and censoring table and
   the IRT strata.
2. Build BICR progression-free survival from the BICR export and the Deaths sheet, convert the IRT's UTC times to the
   site's local date, apply the censoring table, find the cut as the 165th event (17 November 2026) and drop every
   read and death after it.
3. Run the stratified log-rank test (z 0.58) and the stratified Cox model with Efron ties (hazard ratio 0.91, 95 per
   cent CI 0.67 to 1.24).
4. Conditional power from the B-value at information fraction 0.5 with the observed trend: 5.3 per cent (the Cox
   ratio as the drift gives the same; simulated patient by patient under that one ratio, 8.7 per cent).
5. Band A: recommend stopping for futility.

Ends on: about 5 per cent conditional power and a futility stop (band A)
Golden: 99.96 per cent, 100 to the nearest 10 per cent, continue as planned (band C)

## Stump sentence

Carrying the interim's stratified Cox hazard ratio of 0.91 into the rest of the trial, as the B-value's trend
does, files a conditional power of about 5 per cent and a futility stop, because the look's 165 events fell mostly
in the first weeks of follow-up, where ravolimab's arm progresses no more slowly than placebo's (rate ratio 1.34
through the week-12 assessment), while 200 of the 267 patients still at risk are past the week-12 assessment, where
ravolimab's arm progresses at 0.38 times placebo's; followed forward on each arm's own rates, the final test rejects
in more than 99 per cent of continuations and the trial continues as planned.

## Three rules

Task type: survival-time-to-event-analysis in biomedical-clinical-research, which serves forecasting: the conditional power is a forecast of the outcome of an event-driven final analysis, made from the interim's time-to-event data by arm and the trial's remaining follow-up.

Domain test: the deciding quantity is the conditional power of an event-driven final analysis, worked inside the group-sequential machinery a data monitoring committee applies (the information fraction, the B-value, the stratified log-rank test at its final event count) from time-to-event data by arm (Kaplan-Meier curves, events per patient-month by assessment visit); the call compares it with the funder's bands.

Swap: "should the retailer keep its loyalty pilot, judged on the share of members who churn?" keeps the sentence's shape and loses its substance: a churn pilot has no event-driven final analysis, no information fraction and no conditional power band, and its members' remaining exposure is not a set of patients at known places on their own follow-up, so the deciding quantity stops making sense.

Layer 1: IRT randomisation times in UTC for sites from Perth to Oslo, the SAP dating randomisation by the site's local date; BICR reads, investigator reads and deaths beyond the cut in the snapshot; IRT strata keyed differently from the eCRF for nine patients; reads the BICR recorded as not evaluable; pharmacovigilance case versions, recoded terms and nullified cases; Nordic local liver panels in microkatal per litre with their own limits; the EDC's dosing pages behind the IRT. Nothing is planted, and the call's construction is mess-neutral (UTC dates, eCRF strata, no not-evaluable rule, no withdrawal, an unstratified final test: every reading keeps the golden's band and bin, asserted).

Layer 2: the data's real structure in a time-to-event comparison read forward: the arms' ratio of progression rates is not one number over follow-up, and the information still to come sits at a different place in each patient's follow-up from the information the look observed, so the forecast of the final test is a projection over the at-risk set's own follow-up, not the look's average carried forward.

Decisive step: recognise that the interim's one ratio averages an early stretch of follow-up holding most observed events with a later stretch holding most of the events still to come, so estimate each arm's progression rate per patient-month before and after the gap between the week-12 and week-18 assessments, carry every patient still at risk forward from the last adequate assessment on those rates (withdrawal at the observed rate) to the 330th event and recompute the final stratified log-rank test: 99.96 per cent of 20,000 continuations reject, 100 per cent to the nearest 10.

Not semantics: every field, code and definition read correctly (BICR rather than investigator reads, the censoring table, the local randomisation date, the IRT strata, reads and deaths after the cut dropped) still leaves the B-value route at about 5 per cent, because where the remaining patients stand in their follow-up is not a field: it is a relation the analyst has to see the forecast depends on and rebuild across three files.

Not rule application: no filed rule says the ratio changes over follow-up or tells the analyst how to project the remaining follow-up, so executing charter 4.1 and Schedule 2 word for word with the field's B-value files band A; the enumerated family (the B-value on the z or the Cox ratio, the patient-level projection under one ratio, one constant rate per arm, the sample-size ratio, the later-period ratio carried in the B-value, and the projection on each arm's rates split anywhere from 91 to 183 days, by assessment visit, at two breaks, with Weibull fits, without withdrawal, unstratified, on eCRF strata or UTC dates) spreads from 5.3 to 100 per cent and splits the call three ways; the standing family (every projection that follows each arm's own observed rates) spreads 96.9 to 100 per cent, unanimous on band C and the 100 bin.

Analyst test: a strong analyst who reads every field and rule correctly builds BICR progression-free survival under the SAP's table, converts the UTC times, applies the cut, fits the stratified Cox model (0.91), and computes the charter's conditional power from the B-value with the observed trend, files about 5 per cent, band A and a futility stop; followed forward on each arm's own rates from where each remaining patient stands, the final test rejects in more than 99 per cent of continuations and the trial continues as planned.

Estimand: the charter (`talon2_dmc_charter_v3.0.pdf`, section 4.1) files it: the probability that the stratified log-rank test of BICR-assessed progression-free survival at its 330th event rejects at one-sided 2.5 per cent, given the data at the interim analysis, for every patient still at risk at the cut and every patient still to be randomised up to 450 followed until the 330th event, with progression in each arm over that remaining follow-up as the interim data estimate it, not under the sample-size ratio; Schedule 2 and the charter's Appendix A file the bands, and the SAP files the endpoint, the censoring table and the final test.

No decoy: nothing is planted to be caught: no memo, briefing or stakeholder states a conditional power, a ratio by period or a recommendation; the protocol's sample-size ratio appears only in the SAP's power statement and the charter excludes it by name; the investigator reads and the EDC adverse event pages are distractors named in metadata.json that rank nothing.

No certified replay: no published or certified figure is reproduced: no table in the pack carries a conditional power, a ratio by assessment visit or a projected event count, and the projection is rebuilt from raw timepoint reads, UTC randomisation times and status pages.

Lesson: an interim estimate is an average over the follow-up the look has seen, so a forecast of an event-driven final test has to be made over the follow-up still to come, which sits later in each patient's clock than the look's; no build on file forecasts a sequential test's outcome from where the remaining units stand in their own exposure.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 B-value with the stratified log-rank z or Cox ratio as the trend | charter 4.1 invites a conditional power | `BICR_OVRL_RESP` and the strata | the field's conditional power | the z and the ratio agree | the UTC dates and the cut | one formula | none | readable |
| R0b patient-level projection under one ratio | charter 4.1 names the remaining patients | the reads and the status pages | an event-prediction reflex | validates with R0 | none | one simulation | none | readable |
| R0c one constant rate per arm | none | the reads | the blinded event-prediction reflex | none | none | one ratio of rates | none | readable |
| R1 the sample-size ratio | the SAP's power statement | none | the design-alternative reflex | none | none | one formula | none | readable |
| R2a the later-period ratio in the B-value | none | none | a delayed-separation reflex | none | none | one ratio in one formula | none | readable |
| R2 (decisive) each remaining patient followed forward on each arm's own rates before and after the week-12 to week-18 gap | silent: no sentence names a follow-up period, a change in rate, a varying ratio or a model (asserted on all three PDFs) | silent: no column holds a period, an interval rate or a projected event | silent: the field's conditional power takes one trend for the remaining information | silent: no file scores a projection, and the B-value route passes every check it runs | silent: no duplicate, clock or key issue points at it | silent: a projection of 267 patients' remaining follow-up to the 330th event, not one ratio | silent: the BICR export, the IRT export, the status pages, the site register and the three documents each serve every rung | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "BICR-confirmed event" | BICR progressive disease or death without it (SAP section 2) | the investigator reads | another event count and cut | the charter and SAP name BICR; the investigator file is a named distractor (asserted: 183 against 152 progressions) |
| SF2 | the censoring table | as filed, the not-evaluable rule included | the not-evaluable rule ignored | 167 events, PH 7.9 per cent, golden 100: same call | same call (asserted) |
| SF3 | data after the cut | not used (SAP table, last row) | reads and deaths after the cut kept | same band for the B-value route | SAP; same call (asserted) |
| SF4 | the randomisation date | the site's local date (SAP section 2) | the IRT's UTC date | 99.95 per cent: same call and bin | SAP; same call (asserted) |
| SF5 | the strata | as recorded in the IRT (SAP section 4) | the eCRF's | 99.95 per cent: same call and bin | SAP; same call (asserted) |
| SF6 | the final test | stratified log-rank at 330 events, one-sided 2.5 per cent | unstratified | 99.95 per cent: same call and bin | SAP section 4; same call (asserted) |
| SF7 | "as the interim data estimate it" | each arm's observed progression | the sample-size ratio of 0.70 | 53.8 per cent, band B | charter 4.1: "not computed under the hazard ratio assumed for the sample size" (asserted band B) |
| SF8 | the follow-up periods of each arm's rates | split in the gap between the week-12 and week-18 assessments | any split from 91 to 183 days, one rate per assessment visit, two splits, Weibull fits | 96.9 to 100 per cent: same call and bin | same call and bin (asserted for every member) |
| SF9 | withdrawal in the projection | the observed rate per patient-day | none | 100 per cent: same | same call (asserted) |
| SF10 | patients still to be randomised | none: all 450 randomised by the cut | none | same | the IRT export (asserted) |
| SF11 | "80 per cent or more" | inclusive | exclusive | same: 99.96 is far from 80 | same call (asserted) |
| SF12 | the nearest 10 per cent | 99.96 to 100 | none | same | the prompt's rounding sentence; the standing family's minimum is 96.9 (asserted) |
| SF13 | the Monte Carlo | 20,000 continuations, one seed | another seed, 2,000 runs | 100: same | same bin (asserted) |
| SF14 | ask A's source | the pharmacovigilance database (SAP section 6) | the EDC adverse event pages | other counts | SAP section 6; the EDC listing is a named distractor |
| SF15 | ask A's window | onset on or after randomisation and on or before the cut | the date received | equals the truth (asserted) | SAP section 6 |
| SF16 | ask A's coding | the latest report's preferred term and class | the initial report's | equals the truth (asserted) | SAP section 6 |
| SF17 | a nullified case | not an event | counted | equals the truth (asserted) | SAP section 6 |
| SF18 | a re-screened patient's earlier screening number | the same patient (site, sex, year of birth and initials) | a screen failure | equals the truth (asserted: 16 links, each unique) | the screening log's two attempts and the case dates after randomisation |
| SF19 | ask B's window | samples after the day of the first dose to the cut | the first dose day included | equals the truth (asserted) | SAP section 6 and the prompt |
| SF20 | ask B's limits | each laboratory's own upper limit, local units kept | one limit for all | equals the truth (asserted) | SAP section 6 |
| SF21 | the first dose | the earliest dose of any study treatment | the first ravolimab or placebo dose | same date for every patient (asserted) | SAP section 3 |
| SF22 | a central sample's date | its collection date (the EDC's central laboratory kit log) | the transfer's COLLECTION_DATE | equals the truth (asserted: Melbourne's dates follow collection, Edinburgh's equal it) | the SAP's baseline rule dates the sample taken |
| SF23 | "doses given" | every administered dose by the cut, once per patient and day | the EDC pages only | equals the truth (asserted: every EDC dose has its IRT administration) | the IRT's administration log |
| SF24 | "patients who received study treatment" | any dose of any study treatment by the cut | ravolimab or placebo only | equals the truth (asserted) | SAP section 3 |

## Ladder

| Rung | Route | Conditional power | Band |
|---|---|---|---|
| R0 | B-value, the stratified log-rank z as the trend | 5.3 | A, stop |
| R0b | patient-level projection under the stratified Cox ratio | 8.7 | A, stop |
| R0c | patient-level projection, one constant rate per arm | 13.6 | A, stop |
| R1 | B-value under the sample-size ratio (excluded by charter 4.1) | 53.8 | B, extend |
| R2a | B-value with the later-period ratio as the trend | 100.0 | C, by a shortcut that needs the step first |
| Golden | each arm's rates split in the week-12 to week-18 gap, every remaining patient followed forward, 20,000 continuations | 99.96 | C, continue as planned |
| Standing | splits from 91 to 183 days, per visit, two splits, Weibull fits, no withdrawal, unstratified, eCRF strata, UTC dates, another seed | 96.9 to 100 | C, 100 bin |

Separation: the highest band-A rung (13.6) sits 6.4 points under the 20 per cent edge and the sample-size rung 26.2
under 80; the lowest standing member (96.9) sits 16.9 over the 80 per cent edge and 1.9 over the 95 per cent bin edge.
No route that takes one trend for the whole follow-up reaches band C; R2a reaches it only after seeing that the ratio
changes, which is the decisive step's first half.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | every patient still at risk at the cut and every patient still to be randomised | filed: charter 4.1 (SF10) |
| 2 Unit of account | the final analysis's rejection, one trial | filed: charter 4.1 |
| 3 Attribution window | from the cut to the 330th event | filed: charter 4.1 |
| 4 As-of dating | data to the cut of 17 November 2026 | filed: charter section 4 and the SAP table; C1 (SF3) |
| 5 Version basis | one snapshot of each system | C1 |
| 6 Denominator | BICR events as the SAP defines them | filed: SAP section 2 (SF1) |
| 7 Weighting | each continuation counts once | C1 |
| 8 Window length | the whole interim record | C1 |
| 9 Boundary inclusivity | "80 per cent or more" | C1: same call (SF11) |
| 10 Rounding path | the simulated share, rounded once to the nearest 10 | filed: the prompt (SF12) |
| 11 Tie-break | no tie at a band edge or a bin edge | C1: 99.96 against 80 and 95 |
| 12 Maturity and censoring | the SAP's censoring table at the cut | filed: SAP section 2; C1 (SF2) |
| 13 Order of operations | rates, projection, final test | C1: the steps commute |
| 14 Row order | reads by scan date | C1 |
| 15 Duplicate resolution | one read per timepoint | C1 |
| 16 Identity normalisation | the randomisation number throughout the efficacy files | C1 |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | days and patient-months | C1 |
| 19 Code and status semantics | PD, NE, CR, PR, SD as RECIST 1.1 | filed: SAP section 2 |
| 20 Integerisation | a share, rounded once | filed: the prompt |
| 21 Clause scope | the bands apply to the conditional power alone | filed: Schedule 2 and charter 4.2 |
| 22 Forward window contents | each arm's progression over the remaining follow-up as the interim data estimate it; not the sample-size ratio | filed: charter 4.1 (SF7); C2: every member following each arm's own rates keeps the bin (SF8) |

## Literal reader

On paper and on the cut pack: the prompt asks for the call and the conditional power that decides it; charter 4.1
files the quantity and its WHAT (the final stratified log-rank test at its 330th event, given the interim data, for
every remaining patient followed to the 330th event, with each arm's progression over the remaining follow-up as the
interim data estimate it, not under the sample-size ratio), and Schedule 2 the bands. Executed word for word, the
WHAT leaves open only how each arm's progression over the remaining follow-up is estimated, and the record forces it:
the arms' events per patient-month run at 1.37 and 1.29 times through the week-12 assessment and at 0.47, 0.62 and
0.21 times from the week-18 assessment on, so one ratio is not what the interim data estimate for the remaining
follow-up, and every projection that follows each arm's own observed rates lands 96.9 to 100 per cent. Every literal
reading of a convention on the call (SF1 to SF13) gives the golden's band and bin or is ruled out by a quotable
sentence, and every ask reading (SF14 to SF24) equals the world's own truth. Pass.

## Oracles

- The world's own truth: the PFS the simulation generated equals the reader's PFS for every patient (asserted), and
  the clean-truth easy route files band A (z 0.61 on the true strata, asserted).
- The asks: every ask A, B and C figure equals the world's own truth (22 of 22, asserted).
- No shipped oracle: no file ties only under the golden reading; the sample-size ratio is excluded by name; the
  investigator reads and the EDC adverse event listing agree with the B-value route's picture and are distractors.

## Ask sheet

Pair ceiling: 28.5 (the cracker 45.0, the mirror 12.0, on the planning weights of 38, 7 and 55)
Mirror leakage: 0.0 per cent of the ask weight
Measured by: generator/ceiling.py, run on the cut pack

| Ask | Primary device | Golden | The cracker's figures | Cracker |
|---|---|---|---|---|
| A, serious adverse events by arm: patients, events, four system organ classes (12 figures) | D7: sixteen patients were randomised at a second screening; six had their serious adverse event forms filed under the first, screen-failed number, which the randomisation export does not carry; only the screening log's two attempts (same site, sex, year of birth and initials) and the cases' onset dates after randomisation tie them back | placebo 113 patients, 170 events; ravolimab 132, 222; classes 18 to 74 | every figure low by 1 to 5 (cases dropped as screen-failure events) | miss |
| B, liver tests by arm: ALT and AST above 5 x ULN, bilirubin above 3 x ULN after the day of the first dose (6 figures) | D8: the Melbourne laboratory's transfer carries the date it received each sample in COLLECTION_DATE, so a pre-dose sample taken on the morning of the first dose reads as on treatment; the collection date sits only in the EDC's central laboratory kit log | placebo 2, 1, 10; ravolimab 10, 10, 16 | every figure high by 2 | miss |
| C, exposure by arm: patients who received study treatment, ravolimab or placebo doses given (4 figures) | D4: the EDC's administration pages run behind the IRT, and three sites' pages stop when their research nurse post fell vacant; every administration sits in the IRT's log | placebo 223 and 1,455; ravolimab 226 and 1,501 | 220 and 1,378; 225 and 1,439 | miss |

The full includer (re-screen links, sample-tracking dates, IRT administrations, a stress row) keeps 22 of 22. Every
ask reads rows the call never reads (pharmacovigilance cases, central and local laboratory results, sample tracking,
dosing pages and the IRT's administrations), and no device sits on a BICR read, a randomisation record or a status
page (asserted). Hazards: case versions and nullified cases (filed, handled by the cracker), recoded terms on follow-up,
Nordic local panels in microkatal per litre with their own limits, replaced and withheld kits in the IRT log, reads
and deaths after the cut.

## Build record

- World seed 24 (`generator/world.py`), records streams 1 to 6 (`generator/records.py`); `generator/build.py` builds the
  pack, the goldens, metadata.json, figures.json and submission.md twice, compares them byte for byte, cuts
  target.zip, then runs `checks.py` (48 assertions) and `verify.py` (an independent recomputation with pandas,
  statsmodels PHReg and its own projection, against the golden CSV and PDF).
- Pack: 16 files in four formats (CSV, XLSX, PDF, JSON); the central laboratory transfer is the largest file
  (39,530 rows); distractors `talon2_investigator_tumour_assessments.csv` and `talon2_edc_adverse_events.csv`.

## Leak sweep

`leak.py --asof 2026-12-01` on the final cut (target.zip 0b377dd6): REVIEW, no LEAK. Each REVIEW line, ruled:

- Sweep 3, the final event count 330 in Schedule 2, the charter and the SAP: harmless. It is the design's filed event
  count, part of the WHAT the call executes; no document states a conditional power, a ratio by period or a
  direction.
- Sweep 3, the call's words in the same three documents (continue, final analysis, 330 events, as planned,
  conditional power, per cent): harmless. They are the bands' own wording; Schedule 2 and the charter's Appendix A list
  all three outcomes side by side and rank none of them.
- Sweep 4, stump-paragraph nouns in the charter and the SAP (record, months, stratified, log-rank): harmless. They are
  each document's own nouns for the endpoint and the final test; neither names a follow-up period, a change in rate, a
  varying ratio or a model (asserted in checks.py on all three PDFs).
- Sweep 1 flagged an earlier cut's file name for the EDC's central laboratory kit page (the word sample); the file is
  `talon2_edc_central_lab_kit_log.csv` on the final cut and the sweep is clean.
- The stage 4 reader appends its solver's-eye section to the report.

## Tried and rejected

- v1 draft A, the decision at the later of the review and the appointment plus the check (2026-10-18, on paper, never
  registered): the officer's review runs while the appointment waits, so the record's post-appointment time is the
  review's remainder and the forward wait is the later of the review and the new appointment plus the check. Sound
  on numbers (golden 5.5, every uncapped rival a bin or more away) but it is task127's lesson, concurrent waits where
  one change moves the total only by its excess over the other; dropped for uniqueness.
- v1 draft B, the quarter's mix of fingerprint reuse and new appointments read from each filer's capture history
  (on paper): the forward pool mostly needing appointments while the record mostly reused. The abstraction is
  task167's (two latent classes read from each unit's own early record, the forward pool dominated by the slow one,
  `test.same_puzzle` in the batch), and composition_mix is task165's; dropped.
- v1 draft C, the processing front (on paper): the wait set by where USCIS's receipt-order front stands and how fast
  it advances. task130 v2's queue rank against cumulative supply, solved on the portal, and the front's speed is
  estimated to only about a quarter of a bin from the company's own decisions; dropped.
- v1 draft D, the expedites stop and the natural wait is recovered by censoring at the request (on paper): task124's
  driver (an intervention held the analogs' values down and the forward units cannot join it), and the closed record
  would bless the naive method until the forward change; dropped.
- v1 draft E, a staggered rollout of a new process across service centres transported by difference in differences
  (on paper): task136's comparison against the sites not yet treated; dropped.
- v1 draft F, a 2025 episode of longer appointments kept in the record (prototype): its own cohort's 80th percentile
  (5.6 months) sat in the golden's bin, a generic analog that lands; the episode is not built, and the additive stage
  structure is shown instead by appointments rescheduled for an applicant's own reasons.
- v1 reschedules of 25 to 80 days (2026-10-18, world prototype): the common-exposure subset screen (stumping 1.2) killed
  it; decided post-rule renewals with appointment leads of 60, 80, 90 or 100 days or more gave 80th percentiles of 5.43
  to 5.57, each in the golden's bin, a filter and a quantile with no model. Reschedules cut to 7 to 21 days, as the
  card's G13 states (no decided renewal met the forward delay), leave none near the forward exposure.
- v1 expedite response of about three weeks (2026-10-18, world prototype): the constructions straddled the 5.25 edge
  (5.20 to 5.40 against a truth of 5.49), because a decision on an expedite and a decision in the normal course are
  indistinguishable in the record and the record's renewals passed their expiry by less than the response, so the
  response time was not identifiable. A response of about a week, short against that excess, makes every construction
  agree (5.46 to 5.53).
- v1 grading the share pending at expiry to the nearest five or ten per cent (2026-10-18): 0.63 under the golden and
  0.60 under the model sit within two points of an edge; the component is stated as more than half.
- v1 names Quillwater Software and Lindqvist Arceneaux LLP (2026-10-18, house fix H21): edit distance 2 from QuikWater
  (utility billing software) and 1 from Lindquist & Vennum (a former Minneapolis law firm); renamed Sallowmere Software
  (nearest real name Sealmere Limited, distance 4) and Marrowby Teale LLP (no firm of that name found).
- v1 the re-centre rule's first pass, PAPER_MEAN 23 (2026-10-18, rework round 1): carried a generator artifact, a
  request for evidence not yet issued at the team's expedite request still holding the decision back to its response,
  a forward-only floor no record shows; removed, and the rule run again on the whole range.
- v1 PAPER_MEAN 22, the rule's value nearest 5.50 on the process alone (2026-10-18): the constructions that read the
  quarter's category mix sat at 163 to 164 days, 0.11 from the 5.25 edge with one sigma; the rule's own gate, read over
  the range, chose 21 (`## Residual`).
- v1 reschedules of 7 to 21 days for every appointment (2026-10-18, retired at rework round 1): read as tuned to the
  common-exposure screen. Replaced by applicants' reschedules of about one queue length (several weeks to a couple of
  months) before the rule, rare after it (a reschedule past the card's expiry now costs leave, so conflicts go to
  walk-in biometrics), and USCIS's own moves of one to three weeks in both regimes; the subset at the forward exposure
  stays thin (3 since the rule) for that reason, not by a band.
- v1 one appointment share for both categories (retired at rework round 1): (c)(9) renewals reuse the adjustment's
  biometrics far more often; with three in ten sent to an appointment the quarter's category mix enters the forecast
  and widens the family by four days, inside the half month.
- v1 a flat four-week lead for 31 months (retired at rework round 1): the lead now drifts by month and season, differs
  by support centre (the filer's state) and rises about a day a month after the rule, to five weeks by the summer of
  2026, before the autumn's seventeen.
- v1 expedite decisions about a week after every request, 95 per cent accepted, every request on the card's expiry
  (retired at rework round 1): now about 85 per cent accepted, a response drawn around nine days, and a quarter of the
  requests a few days before or after the expiry; the record still reads a week (the response is read on renewals close
  to their own natural decision) and the same week in busy and quiet months.
- v1 option B for the expedite response, a response growing with USCIS's load and estimated forward (2026-10-18, on
  paper): the forward load is a quantity the pack would have to file or the solver choose, a construction fork on the
  main call, and the response growing toward three weeks takes the golden to the 5.75 edge; option A kept (the record
  shows the response held across months of very different volume).
- v1 ask A counting every card in hand (stage 4 round 1, judge NOT_DETERMINISTIC): no shipped text said which card
  counts, which category or which holders are current; GM-07 1.3 and 1.4 now pin each, and the golden is their literal
  execution. Under the pins the roster's category (A5) and the roster's gaps for renewals (counsel's approvals) are
  found by executing 1.4, so the identity device A6 was added beside A1; with every approval record taken and persons
  keyed by ID the cracker still misses five of the six cells.
- v1 the summer 2026 lead rise at 0.9 days a month (round 2, retired): medians of 37 to 41 days in June to August 2026
  raised the share of post-rule renewals expedited on the old lead; held to 0.4 a day (33 to 34 days), the re-centre
  rule run again chose the same value (21) and the margin held (0.128 and 0.214).
- v1 refile packets after Stop work (round 2, generator fault): the world simulated a renewal's packets before it knew
  the employee had left and voided only the receipt, so the mailroom log showed refiles of closed matters, three of
  them Receipted within 30 days of a Q3 2026 rejection (a judge's 17). The world now sends no refile after a stop, the
  first packet already with the mailroom still going out, and the mailroom marks a packet Receipted only where USCIS's
  receipt is on record.
- v1 children's benefits IDs drawn at random (round 2, generator fault): 11 children drew a spouse's dependant ID, one
  of them (D1329430) a card holder of household 925819, which gave a Benefits household that disagreed with Global
  Mobility's; Benefits now never repeats an ID.
- v1 the revision note naming sections 1.3, 1.4 and 2.4 as added in revision 4 (round 2 reader, a mild tell): the
  note keeps only the section 3 rewrite.
- v1 GM-07 1.3 reading "the person Global Mobility took into its care with the household, whether Benefits covers
  her as a spouse or as a domestic partner" (stage 4 round 3, judge SOLUTION_WRONG on September 2027 (c)(26), 769
  against 771): read as excluding the spouses known only by a Benefits ID, it let a judge drop the two spouses whose
  latest card the portal filed under that ID, and "whether Benefits covers her" could be read as taking in Benefits
  spouses never in Global Mobility's care; 1.3 now files the spouse as the one person Global Mobility took into its
  care with the household, however Benefits covers her, and no other dependant, and the golden stands at 771.
- v1 ask devices on the careful path (stage 4 round 4, scored reader 14 of 14 ask figures, `score_reader.py` exit 1):
  the roster's missing first (c)(9) cards sat in the register's approvals, a spouse's two IDs were joined by Benefits
  and GM-07 1.3's one spouse, the applicant-only rejections by the case log's forwarded notices and the applicants'
  own refilings by the register's receipts, every one on the path a careful reader takes once the pins are read;
  re-sited (the tracker's approvals, an employee's I-9 card under a spouse's, an employee's two HR IDs, the
  applicant's own case, the other filings' rejections), the asks, roundings and pins unchanged.
- v1 forwarded copies dated at a fixed offset (round 5 judge, Files/Hygiene, a regularity isolating device rows under
  law 7): every forwarded copy of a biometrics letter was dated receipt plus 12 days, counsel's copy of the same letter
  was not, and the other filing's rejection inherited the fixed date (16 of them exactly 12 days after receipt); now a
  copy carries counsel's date for the notice, or the date USCIS issues it, and the other filing's rejection its own trip.
- Architecture 1 (Sallowmere Software's work-permit renewal wait quote), retired 2026-10-31 by the batch audit before
  any portal result: it was designed before the survivor anatomy gate and its note carries no Actor, Link or Reflex
  line; the decisive cut (the team's expedite request filed at each card's expiry) was a deadline the case log shows
  rather than a quantity the record must be modelled to give, and its stump power was argued from the retired scored
  reader; re-rooted in a new domain so the portal sees one strong build.
- Architecture 2 draft A, extensive-stage small cell lung cancer with platinum-etoposide (2026-10-31, on paper): a
  control median near five months puts the 165th event before recruitment closes, so most of the events still to
  come are new patients' early events and the projection rides the early-period estimate; moved to advanced biliary
  tract cancer, where recruitment closes seven weeks before the cut.
- Architecture 2 draft B, the golden in the middle band (2026-10-31, design screen, never cut): with early harm and the
  interim ratio above 1, the projection landed about 45 per cent, but on one world the split point alone moved it
  from 0.4 to 99 per cent (a split at 3 or 4 months put the week-18 events in the late period); a free parameter a
  defensible value flips, so the golden moved to band C, where every projection on each arm's own rates agrees.
- Architecture 2 draft C, two bands with a 20 per cent futility bound (2026-10-31, design screen): the sample-size
  ratio, which a solver may take whatever the charter says, gave about 54 per cent and landed the call by an excluded
  route; Schedule 2 now carries the extension band from 20 to 80 per cent, which that route lands instead.
