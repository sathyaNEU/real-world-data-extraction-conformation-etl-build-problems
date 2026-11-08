# task212 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1 (Brujula Paqueteria's six Spanish
sortation hubs, the pre-peak sorter survey read from each audited parcel's crush load) was spent at stage 4 round 3 on
2026-11-07: the judge's SEND_BACK on the weekly figure, because the family the programme's lowest-BIC sentence ranges
over was never listed and filing it would have named the load (`determinism_check_report_arch1.md`). Architecture 2
is a re-root into biomedical-clinical-research with a new world, dataset, generator and prompt shell: the Silverbirch
Health Cohort's 2026 genotyping release, read for the assessment centre whose own blood handling fails DNA. Its card
is registered (v2, v1's identity in `lineage`). The sections of architecture 1's design were removed with its
generator; git holds them.

## Draw

Architecture 2, drawn 2026-11-08 on branch batch4-task212-a2 at 5ca7a19 after the urgent-care screens below.

**The draw.** biomedical-clinical-research, task type `genomics-gwas-high-dimensional-association` (it serves
anomaly detection in the client taxonomy), objective anomaly-detection, shape 09 (the release's funnel per assessment
centre carries the asks; the call, runner-up and the decisive contrast carry the recommendation side), decision
pick_one_of_n, strategy composition_mix, Gate G decomposition_attribution, gap objective, generators G12 then G3,
layer 2 estimand_identification (`own:rack-pulls-before-each-aliquots-own-pick`). The world: the Silverbirch Health
Cohort, a fictional university-hosted Ontario population cohort whose seven assessment centres (Thunder Bay, Sudbury,
Kingston, London, Windsor, Barrie, Peterborough) collected blood from 2016 to 2020, and whose biorepository keeps every
participant's plasma, serum and buffy-coat aliquots in -80 C upright freezers, boxes of one aliquot type stacked in
racks that hold a participant range. In 2026 the cohort's first genotyping release took one buffy-coat aliquot for
47,800 participants (picked February to July, in participant order) while the cohort's plasma multi-omics study took
plasma aliquots from the same participants in four assay campaigns, sweeping the freezers in location order: the two
freezers that hold Kingston in January and February, then, after its lab paused, every other freezer from June to
September. The biorepository's ISO 20387 surveillance assessment in February 2027 asks for the corrective action on
the release's failures, collections restart for the follow-up visit in March 2027, and the biorepository director sends
one handling audit to the centre whose own blood handling is failing DNA. Personas from `guard.py names --geo Canada
--seed 212`: Valerie Boyd (biorepository director) and Brandon Summers (biorepository operations manager); the card is
`task212.json`, architecture v2, with v1's identity in `lineage`.

**The call.** Barrie. Kingston leads every reading of the release that takes each aliquot's recorded handling at face
value (its failure rate about 8.5 per cent against 4.4 to 6.0 elsewhere); Barrie sits third to fifth there. Read
within the structure that damages DNA after collection, Kingston's excess is the warming its buffy coats took when
the multi-omics pickers pulled their racks onto a trolley before the release reached them, and Barrie, whose racks
were pulled only after its picks, fails DNA at about 1.8 times the others' rate from its own handling.

**Data-native sentence.** Every pick from any box pulls the whole rack onto a trolley, so a buffy-coat aliquot carries
the warming of every plasma pick made from its rack before its own pick, which no record attributes to it: the LIMS
counts only the aliquot's own thaws, the custody log records each tube's own check-out, and the freezer map holds the
rack only as part of a location string.

**Abstraction sentence** (what a reviewer holding this build and its nearest approved build would say is the same):
units are compared on outcomes after removing an exposure each case inherits from other cases' handling events in a
shared storage unit before its own retrieval. It cannot be written against an approved build: task181's steriliser
added risk to the cases a shared resource handled (membership in its faulty cycles, no order and no inheritance), and
this slot's v1 (the load on each case from cases placed on top of it) never shipped and differs in the event (a
placement after it against a retrieval before it), the container (one cage against a rack of boxes no case shares) and
the world.

**Corpus reads, rerun on 5ca7a19.** `guard.py recent` holds task211, task213 and task214 as the last three live cards
(strategies causal_design, population_selection, decomposition_attribution; forums committee_or_panel,
line_manager_or_team, regulator_or_inspector; forcing events purchase_order_or_contract, period_close,
incident_or_complaint; orgs hospital_or_health_provider, software_or_platform, government_agency; artifacts include
task214's operations_log). `coverage` on anomaly detection by client domain: criminology 1, survey research 1,
biomedical 1 (task195), political science 2, healthcare delivery 3, physical and environmental 3, energy 4.
`mechanisms --objective anomaly-detection` returns the 39 drivers listed below, unchanged. The coordinator's
partition (2026-11-08) gives this slot genomics-gwas and healthcare delivery's payment-claims and provider-quality
cells, and task214's re-root environmental monitoring and conflict-protest; crime hotspots (dead four times in
task200's note) and survey anomaly detection (dead at task125, task202 and task228) are not drawn.

**Slot screens for this candidate** (`guard.py slots`, before the first harness). Mechanism words (freeze, thaw,
warming, retrieval, check-out, rack, excursion, time out, aliquot) returned task228 (soil-probe frost cycles and
fare-validator check-outs, another mechanism), task401 (weekly retrieval practice), task170, task134, task171, task190
and others on generic words only. Setting words (biobank, genotyping, call rate, GWAS, buffy coat, DNA extraction,
assessment centre, cohort, freezer) returned task195 (a Norwegian genomics core's contamination-screen cutoff on a
paired comparison, this cell's one card) and task200's third pass on this cell (one architecture measured dead,
eleven directions closed: selection corrections for discovery effects, nuisance variance out of signal mass, a shared
control panel, linkage-covariate regression, imputation weights, exact conditional nulls, averaging over discovery
uncertainty, transported allele frequencies, differential call rate as a data defect, pooled signal mass, latent
counts). None is pre-analytical storage exposure; task200's line on differential call rate (a data defect that
cleaning removes, so Layer 1) is answered here because nothing is cleaned away: every aliquot's record is correct and
the exposure is constructed. The `resume` lines of task195, task200, task146, task172, task260, task265 and task267
(every biomedical slot) were read; none touches storage handling.

**Screens, clean truth, 20 redraws (seeds 200 to 219)**, harness scratch `t212/a2/b1/h1.py` (summary
`summ.py h1_out_200_20.json`): seven centres sized 5,100 to 8,700 aliquots, the release's pick day uniform over
February to July in every centre, every rack pulled by the multi-omics study in four to eight trolley sessions of
about 12 minutes, the share of each centre's racks pulled before its picks fixed by the sweep order (Thunder Bay
0.50, Sudbury 0.30, Kingston 0.90, London 0.40, Windsor 0.25, Barrie 0.05, Peterborough 0.45), damage a saturating
step in cumulative trolley minutes above about three sessions' worth (odds about 4 at full exposure), Barrie's own
handling odds 1.8, base failure 2.5 per cent, the LIMS freeze-thaw counter set on 8 per cent of aliquots with its own
effect.
1. Levels and the lever: the golden (each centre's failure rate among aliquots whose rack the multi-omics study had
   not pulled before their pick) names Barrie 20 of 20, lead at least 1.37, none under 1.2.
2. The golden's own method: every member names Barrie 20 of 20 (strata at 0, at most 1, 2 or 3 prior pulls, cumulative
   minutes under 10, 20 or 40, no prior multi-omics pull; logistic in pull count, minutes, log minutes, minute bins,
   any pull), minimum leads 1.20 (any pull) to 1.37.
3. The first look (each centre's failure rate): Kingston 20 of 20, lead at least 1.14.
4. The careful readers, each Kingston 20 of 20: (a) direct standardisation over storage-year band, sex and age band;
   (b) the constructing reader (storage years, the LIMS counter, each box's and rack's lifetime openings and minutes
   out, multi-omics pulls ever and their count, pick date); (c) per-record cells (lifetime openings by pick month by
   storage band) and main effects with interactions (pulls by pick date, minutes by storage years, month dummies);
   (d) the mechanism-naming readers (freeze-thaw read off the LIMS counter; lifetime rack openings; openings of the
   aliquot's own box before its pick, zero for every released aliquot because only the release opens buffy-coat boxes;
   racks never touched by the multi-omics study, an empty stratum because the study needed every rack); (e) the
   literal replay of the filed comparison (storage years and the LIMS counter).
5. Literal execution of the filed WHAT (each centre's release failures, with the filed adjustments): Kingston 20 of 20.
6. Fit parity: the easy route's AUC 0.596 to 0.622 against the golden's 0.674 to 0.695; neither is near-perfect, and
   no back-test, reconciliation or published figure in the pack touches the exposure.
Barrie's place on the raw rate: 5th in 11, 4th in 3 and 3rd in 6 of 20 (never 2nd). `corr(golden excess, centre
size)` is near zero (Barrie is mid-sized); Kingston, the largest centre, also leads the raw counts.

**Levels, cited.** Sample call-rate thresholds of 0.97 to 0.98 and exclusions of a few per cent per study (Anderson et
al. 2010, Nature Protocols 5:1564-1573; Turner et al. 2011, Current Protocols in Human Genetics 1.19); the world's base
2.5 per cent and centres' release failures 4.4 to 8.6 per cent sit at the high end for six- to ten-year-old frozen
buffy coats. Genomic DNA degrades with repeated freeze-thaw (Shao, Khin and Kopp 2012, Biopreservation and Biobanking
10:4-11; Ross, Haites and Kelly 1990, Journal of Medical Genetics 27:569-570), and warming above the glass transition
during retrieval is a recognised storage risk (Hubel, Spindler and Skubitz 2014, Biopreservation and Biobanking
12:165-175; ISBER Best Practices, 4th edition, 2018); the odds of about 4 after four to eight trolley sessions is a
design value at the upper end of that record. Participant-level aliquoting into -80 C storage and assessment-centre
collection follow UK Biobank's protocol (Elliott and Peakman 2008, International Journal of Epidemiology 37:234-244),
which genotyped 488,377 participants from 22 centres (Bycroft et al. 2018, Nature 562:203-209); pre-analytical
variables are coded as in SPREC (Betsou et al. 2010, Cancer Epidemiology, Biomarkers and Prevention 19:1004-1011).

**Guard.** `guard.py check` on the probe card: one BLOCK, ban.artifact (operations_log repeats task214), redrawn to
close_out_summary, the honest label for the release's QC close-out the quality lead works from; Kenneth Pierce (a first
name in task93) redrawn to Brandon Summers from the same draw; the deliverable set moved off docx plus xlsx (task211,
task214). WARNs answered: driver.near 0.17 against this slot's v1 and 0.12 against task181 (differentiation lines on
the card, the abstraction sentence above); overuse.objective (the slot's number fixes it); repeat.gate_g and
overuse.gate_g (decomposition_attribution is the honest label: a correctly reported excess assigned to storage warming
rather than to the centre; task214's v1 decomposed an outbreak's source through a water network and is spent);
repeat.decision (the slot audits one site). After the parent branch moved to bea2a97 (task214's card marked spent, so
the live window became task210, task211 and task213), the re-check raised ban.role (compliance_or_audit) and
ban.forcing_event (launch_or_rollout), both against task210; redrawn to the biorepository director (operations_director,
the honest owner of where the audit goes) and the accreditation surveillance visit that asks for the corrective action
(audit_or_inspection), with the March restart kept as the call's forward window. The re-check then gave WARN only:
overuse.objective, repeat.gate_g and overuse.gate_g, answered above.

**Earlier screens in this architecture (urgent care, set aside).** The corpus reads and slot screens of that pass
follow unchanged.

**The window and the bars (urgent-care pass).** Barred by client domain for this draw: general-statistics-data-science (architecture
1), epidemiology-public-health (task214, re-rooting on batch4-task214-a2), banking-credit-financial-risk (task213),
pharmacology-pharmacoepidemiology-safety (task211), human-factors-ergonomics (task210), education-learning-sciences
(task482). `guard.py recent` holds task211, task213 and task214 as the last three live cards (strategies
causal_design, population_selection, decomposition_attribution; forums committee_or_panel, line_manager_or_team,
regulator_or_inspector; forcing events purchase_order_or_contract, period_close, incident_or_complaint; orgs
hospital_or_health_provider, software_or_platform, government_agency). Architecture 1's shell (which, the "Make the
case in" opener, pdf plus xlsx) is barred by `shell.lineage`.

**Coverage on anomaly detection, read by inherited task type** (cards filtered on objective and subdomain, not the
pairing count): crime-incidence-hotspot-analysis 1 (task125; task184 v2 shipped there too), survey anomaly-detection 1
(task186), genomics-gwas-high-dimensional-association 1 (task195), payment-claims-health-plan-analytics 1 (task198),
provider-quality-risk-adjustment 2 (task181, task194), conflict-protest-event-data-analysis 2 (task192, task199),
environmental-monitoring-exceedance 3 (task180, task189, task204), grid-reliability-outage-analysis 4 (task183,
task187, task197, task201).

**What each spent driver on the objective spends** (`guard.py mechanisms --objective anomaly-detection`, lineage
included, one line each):
- task25: records a second source holds that the primary feed never received, added to a candidate's inflow.
- task28: the share of a flagged excess one intervention can reach, counted as single-source batch events.
- task33: forward yield of a shift still in force, cut at a filed intervention.
- task48: a population invisible at the reporting grain, recovered at a two-sided pair grain.
- task54: loss borne by every unit in custody when an event starts, an exposure integral over a re-sequenced plan.
- task68: a like-for-like change on a matched panel linked across identity successions.
- task76: a class that exists only as a per-unit look-back over a log of failed contacts.
- task85: each unit's own observation window from an intermediary's lead time and its own schedule.
- task103: an authorisation is a permission, not a record of service; one allowance a period.
- task104: what a self-adapting scorer would have flagged under a setting it never ran.
- task119: failed waits a unit could have shortened, its own resource free or held empty for planned work.
- task183: parts already failed twice keep failing (frailty across a unit's parts).
- task180: small events recorded only in the quiet hours of a daily noise cycle.
- task185: an instrument conversion sized at the value being converted.
- task186: an empirical null for local cycles shared within a place.
- task187: a capped, curved response averaged over a spread whose width depends on position.
- task188: a density from grouped tests where a positive group is not one case.
- task189: per-unit averages over results censored at instrument-specific limits.
- task195: the uncertainty of a paired difference, not of two marginal intervals.
- task193: orderings whose room depends on where each unit's first exposure falls in the window.
- task192: units that truly carry a property an instrument labels, validated only on the window's opening.
- task197: a unit's response to a shared signal along a trajectory archived as endpoints.
- task196: capture overlap where the second channel is produced by chasing the first.
- task194: counts that crystallise after their period, developed from the series' own vintages.
- task182: durations sampled from snapshots in proportion to their length.
- task198: a lesser-of rule that hides the entitlement behind a modest ask.
- task199: a rise read against the filing effort of the watchers who report it.
- task201: exposure-time short by an opening interval that falls with the number of possible reporters.
- task184: a per-item rate behind a container indicator that saturates; aoristic intervals in its lineage.
- task204: a transport rate from a unit's own unsteady balance across filed windows.
- task181: a shared upstream resource (a steriliser) that added risk to the cases it handled.
- task191: open cases that are mostly the rare outcome.
- task125: occasions at a bordering site moved by the coming schedule.
- task190: mislabels found only where a second record exists; PPS draws and thresholds in its lineage.
- task210: a per-pass hazard set by the sun's position against each direction of travel.
- task211: a transient after each member's first encounter with a changed version of the item.
- task212 v1: the load each case carries from the cases placed on top of it in its container (this slot, spent).
- task213: control seen only where coins received in one ledger return to their source through a second.
- task214: the source each event belongs to, traced through raw switch operations on a network.

**Slot screens** (`guard.py slots`, run before any harness): the mechanism words (urgent care, closure, early
closing, staffing, after hours; substitute, opening hours, closed, alternative; walk-in, capacity, turned away,
queue, deterred) and the setting words (Medicaid, managed care, health plan, primary care practice, attributed
members; urgent care, ED visits, emergency room, walk-in, primary care) returned no spent screen of the candidate.
They returned task137 (a walk-in clinic's run-outs deterring demand, forecasting), task119 v2 (beds held empty for
planned work) and task458's Medicaid plan world as neighbours read in full. The task202 slot's table of screened
anomaly-detection structures (its `## Tried and rejected`, architecture 6 pass) was read whole; it kills wetstock
reconciliation, shared upstream resources traced through time-ordered records, moving generators, open cases,
storage terms, coincidence excess and the sampling designs. The `resume` lines of task194, task198, task181 and
task458 were read: task194's linkage trichotomy (a computable mixture is one join plus one group-by) and its
resume condition (a records-exact decisive step no group-by reaches) frame what a survivor needs.

**Candidates screened in the urgent-care world** (a Medicaid plan's low-acuity emergency visits by attributed
practice, the navigator programme's 2027 placement; harnesses in scratch `t212/a2/proto/`, clean truth, two to four
seeds each before a set-aside): four structures, each set aside with its measurement in `## Tried and rejected`. The
structural lesson they share: an exposure that is the state of a shared resource at the moment of each record (a
centre open or shut, full or accepting) has an expected effect linear in the share of time that state held, so any
reader holding the share (a catchment cell, an annual shut share, a mean wait) adjusts the decoy away, and the true
unit either becomes the raw leader or is masked in a way the counterfactual estimand cannot license. What survives
needs the property architecture 1 had: the exposure comes from other records' attributes in an order relation, its
response is non-linear in it, and the decoy and the true unit share every aggregate of its ingredients while
differing only in how the records are arranged.

## Default path

The field's method for a centre's sample-quality excess, as a careful GWAS QC analyst runs it on the pack:
1. Take each genotyped buffy-coat aliquot's final run from `release1_sample_qc.parquet` and mark a DNA failure as the
   close-out defines it (quantity not sufficient, or a call rate under 0.97 on the final run).
2. Join the aliquot to its participant and enrolment centre (`lims_aliquot_inventory.parquet`, then
   `cohort_participants.csv`), with the recorded pre-analytical variables: storage years from accession to pick, the
   LIMS freeze-thaw counter, the collection's processing codes, sex and age band.
3. Risk-adjust each centre's failures on those variables (indirect standardisation, or a logistic model with the
   centre left out and observed over expected by centre), check plate and batch (balanced by centre) and the re-runs.
4. Read the custody log for the storage side the way the field reads it: the aliquot's own thaws (the counter), the
   box's and the rack's openings in 2026, whether the multi-omics study touched the rack; none separates the centres.
5. Send the audit to the centre furthest above expectation.

Ends on: Kingston.

Golden: Barrie.

Kingston sits at about 1.4 times expectation on the default path, its lead over the next centre at least 1.14 in 20 of
20 redraws; on the golden Barrie's first-opening failure rate is about 1.8 times the other centres' pooled rate and
Kingston's sits at their level.

## Stump sentence

A competent analyst risk-adjusts each centre's Release 1 DNA failures on storage time, the LIMS freeze-thaw count,
the processing codes, sex and age, reads the custody log for each aliquot's own thaws and its rack's 2026 openings,
finds Kingston furthest above expectation and sends the audit there; the step that lands them on Kingston is never
rebuilding, from the custody log against the freezer map, how many trolley pulls each aliquot's rack took before the
aliquot's own pick, under which Kingston's excess is the warming its racks took when the multi-omics study swept them
first and Barrie fails DNA at about 1.8 times the others' rate from its own handling.

## Three rules

Task type: genomics-gwas-high-dimensional-association, the anomaly-detection flavour of GWAS sample QC: which
centre's genotyped samples carry a real handling defect, separated from an artefact of the samples' storage.
Domain test: the quantity that decides is each centre's DNA-failure rate on the Release 1 genotyping run read within
the pre-analytical exposure that damages DNA after receipt (cumulative time out of storage, SPREC's long-term storage
axis), estimated by standardising or modelling failures on the samples' pre-analytical variables.
Swap: "the biorepository sends its handling audit to Barrie, whose buffy coats fail genotyping beyond what each
aliquot's rack pulls before its pick explain" with a warehouse's nouns keeps the arithmetic and loses the reason a pull
of the rack harms a tube that was never picked, which is the thaw physics of frozen leukocytes and DNA call rates.
Layer 1: the custody log in UTC against the LIMS and the lab in Eastern time; location strings in two formats after a
2024 re-rack; duplicate scanner reads at check-out; one genotyping batch exporting call rates as per cents; re-run
aliquots with two QC rows; participant study identifiers against aliquot barcodes; each produced by the system named.
Layer 2: estimand_identification; the centre comparison is confounded by a storage exposure no record attributes to
the aliquot, so the comparison must be read within the exposure each aliquot inherited before its own pick.
Decisive step: rebuild each aliquot's exposure from the trolley pulls its rack took before its own pick (other
aliquots' check-outs from any box in the same rack, ordered against the aliquot's own check-out) and compare centres
within it.
Not semantics: every field is read at its filed meaning (the counter counts the aliquot's own thaws, the custody log
records each tube's own check-out, the location string names the rack) and the easy route still files Kingston,
because no field holds the exposure; it is a relation between other rows ordered against this one.
Not rule application: no filed rule or procedure computes the exposure or tells the reader to; executing every filed
sentence (the close-out's failure definition, the SOP's 20-minute limit, the terms' comparison) files Kingston. The
enumerated family (raw, standardised, counter-adjusted, lifetime-openings, ever-touched, own-box, the field's
pre-analytical model) names Kingston 20 of 20 each; the standing family (every construction of pulls before the pick:
any pull, multi-omics pulls, counts or minutes, linear, log, bins, strata at 0 to 3 pulls) names Barrie 20 of 20,
leads 1.20 to 1.37 at their weakest, so its spread on the call is zero and the ruling-out is the data's within-centre
contrast (aliquots picked after their rack's pulls fail at about three times those picked before, in every centre).
Analyst test: the strong analyst who cleans the release and reads every rule correctly risk-adjusts the centres on the
recorded pre-analytical variables and the custody log's own-thaw and opening counts, and files Kingston.
Estimand: the handling audit's terms of reference (`handling_audit_terms_2027.pdf`) file the population (each
participant's buffy-coat aliquot genotyped in Release 1, final run), the outcome (a DNA failure as the close-out
defines it), the window (Release 1), the unit (the enrolment centre) and the comparison (the centre's own handling from
the draw to receipt, against the other centres).
No decoy: nothing is planted to be caught; no memo, draft, briefing or stakeholder figure carries Kingston, and no
document ranks the centres.
No certified replay: no certified or published figure is reproduced to recover the method; the close-out's totals tie
under every basis.
Lesson: a centre comparison on samples is confounded by what happened to each sample after it left the centre, and the
exposure has to be rebuilt per sample from other samples' handling in the same storage unit, ordered against the
sample's own retrieval; no build on file teaches an exposure inherited from other records' retrievals.

## Survivor anatomy

Actor: the exposure (trolley pulls of the aliquot's rack before its own pick) has no column in any file; the counter
holds the aliquot's own thaws, the custody log one row per tube moved, the location string the rack only as a prefix.
Link: the signal is read through the rack prefix of other tubes' locations (plasma boxes the release never opened)
ordered against this tube's own check-out, a cross-row comparison the field's per-aliquot freeze-thaw bookkeeping
never asks for; no key joins a buffy coat to the plasma picks that warmed it.
Reflex: the field's method (standardised or modelled failures on recorded pre-analytical variables, the LIMS counter
included) sits at rung 0 and files Kingston.
Back-test: the easy route validates: the counter's own effect shows (aliquots thawed once before fail more), the
model's fit is ordinary (AUC about 0.61) and the close-out's totals reconcile; nothing in the pack refutes it.
Second use: the custody log is the release's chain-of-custody record (pick dates reconcile the plate runs) and the
inventory's location strings carry ask A; deleting the decisive step leaves both files in the pack.
Shock: Kingston's excess reads as an ordinary centre effect and Barrie is third to fifth on raw failure rate; Barrie
tops no shipped statistic and the answer is not an interval of any sort.
Pins: the terms file the WHAT (population, outcome, window, unit, comparison) in the biorepository's own genre; no
filed sentence names racks, pulls, the custody log, an exposure or a time window, and deleting any filed sentence leaves
the construction equally forced.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 raw and standardised centre rates | fires (close-out) | fires | fires | no | no | fires | no | readable |
| 1 plate, batch and re-run handling | no | fires (plate ids) | fires | no | fires | no | no | readable |
| 2 counter, lifetime openings, ever touched | no | fires (counter column) | fires | no | no | fires | no | readable |
| 3 pulls before each aliquot's own pick (decisive) | no | no | no | no | no | no | no | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | DNA failure | quantity not sufficient or call rate under 0.97 | identity failures (sex mismatch, unexpected duplicate) included | same call | close-out section 3 defines DNA failures; asserted inert |
| SF2 | final run | the aliquot's last QC row | first row, or failed on any run | same call | close-out: "the final run stands"; asserted inert |
| SF3 | centre | the participant's enrolment centre | the accessioning centre on the aliquot | same call | identical for every release aliquot (C1), asserted |
| SF4 | genotyped aliquot | every release buffy coat with a QC row, QNS included | QNS aliquots left out of the base | same call | terms: every aliquot sent for genotyping; asserted inert |
| SF5 | own handling | from the draw to receipt at the biorepository | every failure charged to the centre | Kingston | terms: "from the draw to its receipt"; storage after receipt is the biorepository's |
| SF6 | rate | failures per genotyped aliquot | failures per participant | same call | one aliquot per participant in Release 1 (C1) |
| SF7 | clock | custody log in UTC, LIMS and lab in Eastern time | either clock for both | same call | no rack pull within a day of its pick (C1), asserted |
| SF8 | a pull | a check-out session on any box of the rack | each tube row a pull; multi-omics sessions only | same call | every construction names Barrie (C1 on the call), asserted |

## Ladder

| Rung | Construction | Names | Lead (min over 20) |
|---|---|---|---|
| 0 | raw failure rate; standardised on storage years, sex, age | Kingston | 1.14 |
| 1 | plus plate, batch, re-run handling | Kingston | 1.14 |
| 2 | plus the counter, lifetime box and rack openings and minutes, multi-omics ever and count, pick date | Kingston | 1.15 |
| 3 | pulls before each aliquot's own pick (decisive), any form | Barrie | 1.37 (stratum) |

Position: Barrie third to fifth on rung 0 (5th in 11, 4th in 3, 3rd in 6 of 20). Dominance: every wrong rung's top
(Kingston) clears its runner-up by at least 1.14; the golden clears its runner-up by at least 1.37. Worth: the decisive
step moves Kingston from about 1.4 times expectation to about 1.0 and Barrie from about 1.15 to about 1.8.
Pricing sequence: (1) the residue the filed WHAT leaves is a construction, not a knob; (2) the move needed (Kingston's
excess, about 3 points of failure rate) against the ceiling (its exposed share, 0.9, at about 6 points each) is
reachable; (3) the one-group-by route (rates by centre by rack) is not affine in any shipped column; (4) the
standard error of Barrie's first-opening rate is about 0.3 points against a 2-point excess; (5) the lever (exposure)
and the ranked quantity's noise are different variances; (7) no subset of rows prints the exposure; (8) the reflex sweep
runs as code (`generator/checks.py`, screens block).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | Release 1's genotyped buffy coats, final run | filed in the terms; C1 on the call across SF2 and SF4 |
| 2 Unit of account | the enrolment centre | filed; SF3 C1 |
| 3 Attribution window | Release 1 picks, February to July 2026 | filed; every pick inside it |
| 4 As-of dating | the custody log as exported on 2026-10-30 | stated on the export; nothing after it is read |
| 5 Version basis | the close-out's final run | filed (SF2), asserted inert |
| 6 Denominator | genotyped aliquots, QNS included | filed (SF4), asserted inert |
| 7 Weighting | per aliquot | one aliquot per participant (SF6) |
| 8 Window length | pulls before the aliquot's own pick, any lookback | C1: every pull of 2026 precedes or follows by more than a day |
| 9 Boundary inclusivity | a pull on the pick day | none occurs (SF7), asserted |
| 10 Rounding path | rates computed on counts, rounded once | asserted on every graded figure |
| 11 Tie-break | none needed | the call's lead at least 1.37 |
| 12 Maturity and censoring | none: every pick is complete | asserted |
| 13 Order of operations | final run, then failure, then centre | asserted inert |
| 14 Row order | none | assertions run on shuffled rows |
| 15 Duplicate resolution | duplicate scanner reads collapse to one session | SF8 C1 |
| 16 Identity normalisation | barcode to study identifier through the inventory | C4: every release aliquot resolves |
| 17 Netting against gross | none | no offsetting rows |
| 18 Dimensional units | call rate as a fraction; one batch in per cents | converted (Layer 1), asserted |
| 19 Code and status semantics | close-out status codes at their filed meaning | filed codes, asserted |
| 20 Integerisation | counts are whole aliquots | by construction |
| 21 Clause scope | the terms' comparison covers every centre | filed |
| 22 Forward window contents | the March 2027 restart; the call is a site, not a forecast | no forward figure is graded on the call |

## Literal reader

Executed word for word, the terms name the centre whose own handling from the draw to receipt accounts for the highest
DNA-failure rate; a literal reader who charges every failure to the centre files Kingston (SF5, ruled out by "from the
draw to its receipt"), and one who nets out what happened after receipt files Barrie under every construction of the
rack's pulls before each pick; no filed sentence reads to a third answer.

## Oracles

none: the close-out's totals tie under every basis, the counter's effect is the same on both routes, and no control,
published figure or corpus ties only under the golden or only on the wrong read.

## Ask sheet

Stage 2, in progress (devices re-priced against the full includer; built in the generator and measured on the cut pack
by `generator/ceiling.py`, which shares no code with the generator). The prompt draft asks two blocks beside the call.
- Ask A, the 2027 pool per centre (seven counts and their total): participants not genotyped in Release 1 whose BC1
  aliquot is in storage and usable and whose consent is in force. Primary D7: study identifiers freed by the 2024
  re-keying re-issued to 2025 enrolments, so every key matches and the habitual join hangs an old aliquot on the new
  holder (consent in force) while the old participant's withdrawal sits under their new identifier; the remedy is
  identity by accession date against enrolment date through `previous_study_id`. Primary D4: the 2025 inventory audit's
  exceptions (empty or cracked tubes) listed by box position, resolved to barcodes only through the location history
  across the 2024 re-rack. Hazards: duplicate consent rows; re-consent after a withdrawal (latest event rules).
- Ask B, late shipments per centre (seven whole per cents and the overall, 2016 to 2020): shipments that reached the
  biorepository more than 24 hours after the earliest draw they carried. Primary D6: multi-box shipments, one row per
  box in the courier file and one shipment in the receiving manifest, received when its last box is delivered (filed in
  the receiving SOP as the WHAT). Primary D8: to be re-sited onto a recorded-date pair the asking sentence can name
  without naming the handling. Hazard: courier scans in UTC.
Separation: zero device rows in Release 1's genotyped aliquots, the 2026 custody log or the audit terms (asserted by
count in `generator/checks.py`).
Pair ceiling: 52 (paper; the script measures it on the cut pack)
Mirror leakage: 35
Measured by: task212/generator/ceiling.py

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A pool | joins aliquots to participants on the study identifier as stored, reads the audit exceptions by current position | miss |
| B late share | counts courier rows, dates arrival from the field the manifest names | miss |

## Tried and rejected

- 2026-11-04, the seed's title mechanism (the FY2027 final rule's severity tables remove the largest excess by
  themselves): regrouping FY2026 claims under the published rule is rule application; it can stand only as a lower
  rung (the literal replay), never decide the call.
- 2026-11-04, the severity-validation family (peer benchmark on the MCC-level share, risk adjustment on observable
  case mix, length-of-stay and in-hospital mortality validators, one patient coded by two providers): every plain
  improper practice is visible to one of the validators or to the benchmark, so a strong analyst's own validator
  reaches whatever cell carries plain upcoding; task190 architecture 7 already measured the two-provider and
  look-back members dead (filter-and-difference reaches the designed set 18 to 20 of 20; the attaining subset is
  the fully enrolled patients).
- 2026-11-04, diagnoses repeated onto same-hospital readmissions from the patient's previous stay there (a
  documentation carry-over present at every hospital at its own rate), read against the same kind of patient
  readmitted to a different hospital, where the earlier record cannot carry over. Seven parameter sets, 20 redraws
  each. Truth named the designed cell 20 of 20 every time. The mechanism's naive count (every repeated diagnosis
  that moves the DRG on a same-hospital readmission) named the golden cell 17, 17, 19, 11 and 12 of 20 in the first
  five sets, and the acute-only naive count 15, 18, 15 and 16 of 20; the golden family (family by prior-diagnosis
  matching, pooled, by family, by class) held 15 to 20 of 20. The sixth set added large genuine-recurrence cells
  (dialysis patients' N18.6 on every stay, acute-on-chronic respiratory failure recurring at 0.75): the naive
  counts then landed wrong (20 and 19 of 20) but the golden collapsed to 1 to 8 of 20, because the matched
  other-hospital recurrence cannot subtract a recurrence volume that large. Earlier single-seed versions measured
  the deniable contrast at 20 to 36 claims a cell against binomial noise of 5 to 14 claims. It also sits beside the
  client's own example of a planted copied block, which a judge reading Gate H may take it for.
- 2026-11-04, bed occupancy on the admission day setting the admission threshold (a crowded hospital admits only
  its sickest medical patients on its full weekdays, so its genuine severity excess reads as upcoding, and every
  benchmark, the hospital's annual occupancy as a covariate and both validators land on it). On one seed the ladder
  formed exactly (flagged payment A, FY2026 decomposition B, every benchmark and the annual-occupancy reader C,
  golden D). Over 20 redraws it fails: truth split 10, 8 and 2 across three cells, the golden named the academic
  sepsis cell 9 of 20, because the benchmark excess of a cell of about 5,500 claims carries binomial noise of about
  36 claims, about 0.36 million at that cell's payment step, against a designed signal near 0.2 million; making the
  golden cell's upcoding loud enough to clear that noise makes every benchmark reader name it too.
- 2026-11-04, forward behaviour as the decisive step (the sentinel effect under review, code substitution after a
  severity downgrade, a coding programme's ramp): each is a practice a governing document would have to file, and
  filed it is executed (the withheld-rule trap the brief records from task211's architecture 1).
- 2026-11-04, probe-sample and close-out extrapolation (a targeted probe weighted back to its stratum,
  probability-proportional-to-size draws): spent as drivers (task482's lineage on stratified audit weighting,
  task190 architecture 3 on PPS draws).
- 2026-11-04, re-root screens on paper before the draw, each set aside before a harness: concurrency or crowding at
  the moment of each case (a sorter's throughput, a station's gate flow, a guard on shift) dies on granularity, since
  an hourly count either reaches the golden or breaks it, so the per-case state has to be categorical rather than a
  finer cut of a continuous one; a back-fed circuit's headroom at the fault time needs the control room's back-feed
  practice filed, and filed it is replayed to the golden; storm-overflow spills during pump trips are a visible
  breach of the pass-forward condition (rule application); transformer overload from EV clusters is task164's and
  task402's ground; a bathing water's spill transient and a stagnation clock are task211's live driver in other nouns.
- 2026-11-04, the stacking candidate's first calibrations (scratch `proto_stack.py` to `proto_stack6.py`): crush linear
  in the weight on top put audited damage at 6 to 9 per cent and split the golden's forms (the linear and banded
  forms named Zaragoza in some redraws); a steeper response made the linear forms worse (11 to 14 of 20); a Poisson
  number of cartons stretched the loaded cluster past saturation (linear forms 16 to 18 of 20); placing each cage's
  carton batch at a Beta-drawn position broke the masking, Ribarroja took crush of its own and its raw rate led in 13
  of 20. The kept calibration (`proto_stack7.py`): light e-commerce parcels near 0.6 kg so a light-only stack stays
  under the crush range, a consignment of seven to nine cartons of 15 to 21 kg placed by the trunk timetable 97 per
  cent of nights, a crush response centred on 60 kg on top.
- 2026-11-05, the first ask draft (sorter stoppages with one standstill recorded by both the PLC and the safety
  controller, and stoppages inside the event logger's heartbeat gaps; claims with a reopened case's cumulative
  approval and the case export's delivering hub): every device but the gaps was executed by a filed WHAT or the
  hygiene battery (the claims note files the sorting hub, the transfer runs pay only the top-up, a PLC that logs every
  standstill makes setting the safety rows aside correct), and heartbeats that stop announce the gap, so the cracker
  kept most of the layer; replaced by the four primaries in `## Ask sheet`.
- 2026-11-05, the three business accounts' own sectors (automotive parts, ceramic tiles, olive oil and wine) were each
  unique to one hub, so a sender-sector dummy absorbed that hub's cartons and moved Ribarroja's figure by 4.7 per
  10,000 at the shipped seed; the accounts now carry sectors e-commerce senders share and the sector reader holds.
- 2026-11-05, cartons placed at a fixed share of each cage's scan sequence put a hub's cartons into its cages over 42
  to 142 minutes a night, which one dedicated trailer cannot produce; each hub-night now has one trailer arrival and
  the cartons enter every cage as it is unloaded. With Dos Hermanas's trailer at 00:32 the wrong-reason reader landed
  Ribarroja 3 of 20; at 01:20 it lands Dos Hermanas.
- 2026-11-07, closing the forward figure's load form by "the best-fitting estimate stands" (raw fit or AIC): the
  step with the constructing reader's position, cage-weight and carton-count terms added fits best on both and puts
  Ribarroja at 16.6 per 10,000 (about 300 a week), because a cage of cartons with little on a parcel occurs almost
  only at Ribarroja, so cage terms stand in for the hub; a second carton-first hub (Basauri, tried in the world)
  narrowed it to 39.7 against 51.7. A sentence naming BIC alone, in the world without the twin, picked a supported
  load form in 18 of 20 redraws and the kitchen-sink in 2; with Basauri kept as a carton-first hub (its paper account a
  2026 customer) the lowest BIC picks a supported load form in 20 of 20, setting the kitchen-sink aside by 41 or more
  (100 at the shipped seed) and the log by 66 or more (145).
- 2026-11-07, a flat-rate case's grain left unfiled (D6 riding silent on the approved amount over the account's rate):
  died at the stage-4 judge, who counted one damaged parcel a tracking number (1,101 / 772 / 827 / 1,232 / 935 / 411),
  read the golden's counts as more than the approved parcels that exist and found nothing shipped saying a flat-rate
  case covers several cartons; CS-FIN 07 section 2 now files the case's grain and approval basis in Customer Service and
  Finance's voice (SF17), the golden counts unchanged, and the device holds nothing.
- 2026-11-07, the safety system on its own clock, its stamps 34 to 426 s earlier than the PLC's and drifting over the
  quarter, with the golden
  reading its STOPs through a straight line fitted to the paired offsets, beside work orders keyed to the nearest
  minute: died at the stage-4 judge, who put San Fernando at 38.0 h (earliest stop to latest run), 33.6 h (the raw
  safety STOP) or 32.8 to 33.0 h (a mean or median offset) against the golden's 32.7, El Prat and Basauri unpinned too,
  while the same earliest-to-latest reading added 0.2 to 0.3 h at the older hubs through the nearest-minute orders. The
  safety system now keeps the controller's time and logs TRIPs only (with RESET rows, a lost spell ended at its RESET
  left San Fernando 0.04 of a bin from its edge and TRIP to RESET moved three hubs), each order keys its minutes inside
  its logged spell, and every reading is one figure (SF18). Moved, accepted with `freeze.py --allow hours_ZAZ,hours_VLC`:
  Zaragoza Plaza's hours stood 32.2 to 32.0 and Ribarroja's 39.5 to 39.4, because the older hubs' spells recorded only
  in the orders (7 and 6) are now keyed inside their minutes, each about a minute shorter, and each hub is re-seated
  mid-bin; every other graded figure is unchanged.
- 2026-11-07, architecture 1's PDFs written by a library with a Microsoft Word producer string: set aside at stage 4
  round 2 for genuine LibreOffice Writer exports (Producer LibreOffice, Creator Writer, a real Subject and the
  organisation as Author), the rule on main (`SKILLS: a PDF input is exported by an office application`).
- 2026-11-07, "the 60 kg step is the lowest BIC" in the note and the notes sheet: set aside at stage 4 round 2, the
  judge found BIC flat from about 40 to 100 kg on top, so no step was singled out; the sentence was reworded and the
  answer did not move.
- 2026-11-07, architecture 1 itself, spent at stage 4 round 3: the weekly figure turned on the family the programme's
  filed lowest-BIC sentence ranges over, which no document listed; adding the cage's total weight to a step in weight
  on top gave Ribarroja about 37 per 10,000, about 600 parcels a week against the golden's 800, with BIC gaps of 2.7 to
  7 and the golden's own form on the 750 rounding line at wider edges. Filing the family would have named the load, so
  the fork was the stump (`determinism_check_report_arch1.md`).
- 2026-11-08, architecture 2 candidate U1 (a Medicaid plan's 2027 emergency-department navigator placed at the
  practice whose members' low-acuity visits most exceed expectation; each visit read against whether the member's
  in-network urgent care was actually open at that hour, from the operator's daily log): set aside on the harness
  (scratch `t212/a2/proto/proto1.py` to `proto3.py`, three revisions, two to four seeds each). Whenever the true
  practice's after-hours steering deficit was large enough to separate in the golden (open-hour excess lead 1.9 to
  3.2), it was also the raw leader (risk-adjusted excess picked it 3 to 4 of 4); whenever the decoy's closures were
  large enough to lead the raw ranking, a reader holding the centre's annual shut share by band, or catchment-by-band
  cells, adjusted the decoy away and landed the true practice. The exposure is the state of a shared resource, so its
  expected effect is linear in the shut share and every aggregate of the log carries it.
- 2026-11-08, candidate U2 (U1 with closures triggered by demand, every centre shut on the same share of evenings and
  only the decoy's centre shutting on its busiest ones): set aside (scratch `proto4.py`, one revision, four seeds).
  With equal annual shut shares no aggregate distinguishes the decoy's centre, but the alignment of closures with
  busy evenings moved the decoy by only about 3 per cent of its after-hours visits; the true practice stayed the raw
  leader (3 of 4) and the golden separated it in only 2 of 4.
- 2026-11-08, candidate U3 (U1 with both catchments' centres unreliable and the true practice's members insensitive
  to closures, so its excess is masked in the raw ranking): the harness passed every coded reader on four seeds (raw,
  bands, contract hours and shut-share readers on the decoy at 2.1 to 2.7; catchment cells on noise; the open-state
  golden on the true practice at 2.8 to 3.8), and it was set aside on paper. Its masking makes the true practice's
  members wait more when their centre is shut, so the counterfactual estimand (visits its members would not have made
  attributed elsewhere) nets to about zero for it, and the only estimand that picks it ("visits the navigator can
  redirect to an open centre") hands over the step; the true practice's near-zero urgent-care share is also visible
  to a reader comparing emergency against urgent-care use.
- 2026-11-08, candidate U4 (availability as the centre's own walk-in queue against its stated cap, rebuilt from every
  patient's check-in and provider-start times, the decoy's centre a small waiting room with variable service times so
  its mean wait looks ordinary while it turns patients away): set aside after three revisions (scratch `proto6.py` to
  `proto8.py`, two or three seeds each). The decoy's centre reached 0.75 to 0.80 acceptance with a mean wait inside
  the other centres' range (27 to 30 minutes), but the per-centre loads set by practice sizes kept other centres in
  the same range of acceptance, the decoy led the raw ranking in only 1 of 3, and the golden picked the true practice
  in 2 of 3; the acceptance share, once rebuilt, is again a linear aggregate of the exposure. Two candidates in the
  urgent-care world failing their screens moves the next draw to another world.
- 2026-11-08, architecture 2 candidate B1 with box-level exposure and the multi-omics study touching 85 per cent of
  boxes (scratch `t212/a2/b1/h1.py`, runs 1 to 8): set aside on paper before the 20 redraws, because a reader comparing
  centres among the boxes the study never touched (a lifetime stratum, no order relation) reaches the golden: both
  strata are unexposed. Moved to rack pulls with every rack pulled (the study takes plasma for the same participants),
  which empties that stratum, and to plasma and buffy coat in separate boxes, which puts every own-box count at zero.
- 2026-11-08, B1 with single-session visits and background openings at 0.15 a box: the at-most-one and at-most-two
  prior-opening tolerances landed Kingston 4 of 4 (single sessions inside the tolerance), and a model on "any prior
  opening" was diluted by harmless background openings (Kingston 1 of 4). Moved to visits of four or more sessions,
  each inside any stated time limit, damage above about three sessions' worth, background openings at 0.06 a box.
- 2026-11-08, B1 with the other centres' exposure redrawn every seed (0.35 to 0.60, then 0.05 to 0.25, then 0.25 to
  0.55): the first look landed on other exposed centres in 3 of 4 at the widest setting, and Barrie's raw place swung
  from 2nd to 7th; the shares are a property of the world (the study's sweep order), fixed at design values, after
  which Barrie sits 3rd to 5th and the first look lands Kingston 20 of 20.
- 2026-11-08, the first ask draft's two weak devices, priced against the full includer before any data is cut (stage 2,
  this session): ask A's D4 as a consumption list (the 2023 DNA pilot's samples named as used up) is a stated record a
  full includer executes on reading it, so it keeps the figure; ask B's D8 (the LIMS accession time against the
  courier's delivery scan) forks unless the arrival is filed, and filing "the courier's delivery to the dock" performs
  the remedy. Replacements to price next: D7 with study identifiers re-issued to 2025 enrolments after the 2024
  re-keying (every key matches, the habitual join attaches an old aliquot to the new holder, the remedy is identity by
  accession date against enrolment date through `previous_study_id`); D4 with the 2025 inventory audit's exceptions
  listed by box position (empty or cracked tubes), resolved to barcodes only through the location history across the
  2024 re-rack; D8 re-sited onto a clock or recorded-date pair the asking sentence can name without naming the handling.
  Ask C (failed reference controls per genotyping batch) and a freezer-hours ask were set aside on paper: the control
  file's own type column performs the layout device, and two probes per freezer fork the hours unless the monitored
  probe is filed.
- 2026-11-08, the stage-2 resume plan, priced on paper before any generator code (paused by the author before a harness
  ran): the freezer sweep in the resume line (Kingston 12 January to 27 February, then Thunder Bay, Peterborough, London,
  Sudbury and Windsor in sequence from late April, Barrie late July to August) makes each middle centre's exposure a step
  in pick date (its racks picked after its sweep are the exposed ones), a dated rise that a centre-by-pick-week failure
  table shows; `h1.py` never modelled it, since it places each rack's multi-omics visit 5 to 40 days before or after that
  rack's own pick with a centre-specific before-share, independent of pick date. A January and August split outside the
  release window keeps pick date clean but makes the January phase a dated split of racks that shows the effect in every
  centre. Ask B's D6 as filed is performed by the receiving SOP's own WHAT (group the pieces, take the latest delivery), so
  the full includer keeps its block; ask A's D4 by box position through the location history is a walk back through a
  change log, which the hygiene battery makes (supplemental-stumping 1.1c, 464 at 72).
