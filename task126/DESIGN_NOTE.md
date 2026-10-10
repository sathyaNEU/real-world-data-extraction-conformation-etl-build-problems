# task126: the Morvane Patent Office's FY2022 headline pendency, realising analytical_tasks note DA02 (analytical_tasks/03_descriptive_distribution/DA02_pendency-median-docket-versus-application-grain.md)

Stage 1 (draw), drawn 2026-10-10. This is the build's one design note; the design stage extends it. The note is the idea and this build is its first realisation. Its world, its committed call and its corpus survive; its decisive rung (chaining dockets into applications along CX edges) is kept as rung 3, and a new decisive rung sits above it (see Changes and Tried and rejected).

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? Card filed: pending registration
    (drafted at scratchpad/cards/task126.json; the coordinator registers the batch in task-number order)
    Verdict: WARN (exit 0), checked against the corpus with task124 and task125 already filed
  Shape: 14 cuts of a distribution   Gate G mechanism: method_or_model_selection
  Gap: population (decisive); rule below it (the end-date convention the partner file pins at rungs 0 and 1)
  Pattern: none at the decisive rung (G3 carries it); D at rung 3
  Domain: policy-education   Subdomain (enumerated): public-administration   Objective: descriptive-distribution
  Pairing repeated from last build? No. The window is task122 (product-analytics x experiment-causal),
    task124 (business-operations-analytics x forecasting) and task125 (accounting-audit-forensic x anomaly-detection)
  Stakeholder role: head of performance statistics at the national patent office, who drafts the headline
    section of the statutory annual performance report (statistical_office_head)
  Context-artifact type: published_series, last year's annual performance report pendency table: examiner
    docket pendency, the office's own twenty-year series and the licensed wrong basis
  Calibration form: counterparty_acknowledgement, the partner office's acknowledgements of the office's final
    decisions on work-sharing programme applications filed FY2019 to FY2022
  Decision type: quantity_figure, the FY2022 median time from filing to final decision in months to one decimal
  Decisive mechanism: G3 record versus operation. A CX edge records that a refused application's examination
    file moved to a new docket, which happens both when the same application is re-examined and when the
    applicant files a continuing application on the transferred file; only the examiner production ledger's
    credit class on the successor docket's first action tells the two apart. G2 (dockets chained into
    applications along CX edges) carries rung 3 and G16 (censoring of CX exits) rung 2
  Repeats from prior builds: none inside the ban window. The decisive signature (population, G3,
    quantity_figure) repeats task82 v2, an older build, and is differentiated on the card

  Niche: a national patent office's statutory headline pendency for one fiscal year's filings, where the
    examination docket hands a refused application's file to a new docket both for a re-examination of the
    same application and for a continuing application filed on the transferred file
  Forum: minister_or_cabinet (the report is filed with the Minister for Enterprise)
  Forcing event: statutory_or_regulatory_filing (the annual performance report, due 31 January 2027)
  Organisation family: government_agency   Scoring unit: per resolved case
  World: fictional country (Republic of Morvane); no currency in the graded figures. Invented names: Morvane,
    Morvane Patent Office, Saravel, Saravel Intellectual Property Office (the work-sharing partner),
    Morvane Patent Examiners' Association
  People, drawn with guard.py names --geo "fictional country (Republic of Morvane)" --seed 126 (locale en_US):
    Stephen Brewer (head of performance statistics, the requester), Thomas Kennedy (deputy commissioner for
    operations, the prompt's one belief: our dockets are our applications), Cristina Turner (work-sharing
    coordinator, the corpus voice), Erica Ryan (secretary of the examiners' association, which publishes
    docket pendency beside the office's figure), Michael Cannon (production systems manager, keeps the docket
    extract and the production ledger), Lauren Mendoza (examination practice manager)
  Spine (planned): examination_dockets_FY2016_FY2026.parquet, about 820,000 rows, one examination docket
    (one examiner's file on one application from docketing to close, with its end code), grain docket,
    synthetic; the note's 2.9 million rows are rescaled at stage 2
  Deliverables (planned): fy2022_pendency_headline.docx (the headline sentence as the report will print it,
    the cuts by technology group, the share still undecided at the extract) and fy2022_time_to_decision.svg
    (time to final decision for the FY2022 filings, the 50 per cent line, the median labelled, the undecided
    share annotated, a title that states the figure)
  Opening move (provisional): number-first
  Criteria arithmetic (shape 14): 8 technology groups x 3 figures (lower-quartile time to final decision,
    median time to final decision, share decided within 36 months) = 24, plus the headline median, the share
    of FY2022 filings undecided at the extract, 5 named chart parts and 2 files: 33 before any
    device-carried ask
```

As-of date: 2026-11-23

Tense: the committed figure is retrospective, and that is legal here for a stated reason. It is a statutory statement about a cohort still in flight (13 per cent of FY2022 filings undecided at the 30 September 2026 extract), filed before the cohort closes, and the statute fixes which cohort the report carries. It stays Descriptive rather than Forecasting because the records already determine it: every undecided application is older than the median at the extract, so no later decision can move it.

Similarity claim: no prior build is this puzzle, because none splits units that a corpus-certified natural build has already joined, on a classification carried only by a separate credit ledger. The nearest signature, task82 v2 (population, G3, quantity), joins orphan records into holders through a credit ledger to carry them over a count threshold, the opposite move on a different quantity. The source note's own chaining (lineage v0 on the card) repeats task90's merge of work records into the customer's unit, and that is why it is a lower rung here and not the decisive one.

## Stump sentence

A competent solver chains every CX succession into one application, dates it from its first docket, ends it at its last docket's decision, censors the undecided at the 30 September 2026 extract, reproduces every one of the partner office's acknowledged final decisions to the day with that construction and files the fully chained FY2022 median (31.4 months in the source note's world); the step that lands it there is reading every CX edge as the same application continuing, when a designed share of them (about two in five) carried a refused application's file to a continuing application filed that day, which the examiner production ledger credits as a first action on a new application, so each of those is a new application in its own filing year and its parent was finally decided at its refusal, and the FY2022 median is about 27.9 months (a design target, fixed at stage 2).

## Decisive rung

Measured trap **#13, validates on one population, applies to another** (`.claude/skills/stumping/references/traps/_measured.md`): established, decided 3 of the client's 64 measured tasks, 2 of them under 0.50, and the trap behind the pilot's one held main call (task117, FC01). Its recipe is a field that fits every row it can be checked on, rows to be graded that differ on one axis, and evidence of the difference left in the record. Here the field is the CX edge read as "the same application continues". It fits every case the solver can check: in every corpus case a CX succession is a re-examination, because the programme's rules bar a continuing application on a programme file (a refused programme application that is continued leaves the programme). Outside the programme some CX successions are continuing applications. The evidence is the examiner production ledger's credit class on each successor docket's first action, and the production standard that defines the class.

Behind it stand **#12, stops at the first control that passes** (3 of 64, 2 under 0.50): the partner file is the control, and the fully chained build passes it on every case. Then **#5, takes the population a flag or filter suggests** (5 of 64, 3 under 0.50): the CX edge type is the flag, and the true population comes through the ledger.

Litmus, in a sentence: no reported number in the pack is wrong. The docket table, the continuity table, the action history, the partner's acknowledgements, the published docket pendency series and the production ledger are each correct at their stated meaning, and no one's reading of their own figures is overturned. The difficulty is which records form one application. Flags: surface_read_dependency no, stumping_family analytical_non_defect, sole_data_defect no. The CX label is right about the docketing, and the decision needs the legal unit behind it. The two populations at rungs 3 and 4 differ in membership and in dates, so this is not one lens on one population.

Constraints the design stage inherits: the CX gloss in the docketing codebook says the examination file moved to a new docket, not "continued examination requested". The action history codes a successor's first action the same way on both routes. No document says that a continuing application can be docketed as a CX succession. Every ask is kept off the production ledger. The production standard's credit-class definition is what makes the split determinate.

## Ladder sketch

Figures are design targets (the note's world for rungs 0 to 3; rung 4 to be set at stage 2). Each rung is killed by one shipped fact.

| Rung | Construction | Candidate (FY2022 median, months) | Killed by |
|---|---|---|---|
| 0 | The production system's examiner docket pendency: FY2022 dockets, Kaplan-Meier, an allowed docket ending at grant | 22.4 | The partner office's acknowledgements: every acknowledged final decision is an allowance or abandonment notice, never a grant |
| 1 | FY2022 dockets ending at the decision notice, a CX close read as an end | 19.0 | The docket end codes: a CX close is no decision, the file moved to a successor docket |
| 2 | CX dockets censored at the CX date, every other docket ending at its decision | 23.8 | The partner file's re-examined programme cases: each acknowledged final decision falls on the successor docket and is dated from the first docket's filing, so a CX exit is the application still waiting (informative censoring) |
| 3 | Every CX succession chained into one application, dated by its first docket, ended at its last docket's decision; reproduces every acknowledged programme decision | 31.4 | The examiner production ledger: the first action on about two in five CX successor dockets is credited as a first action on a new application, so those successors are continuing applications filed on their docketing date |
| 4 (decisive) | Chain only the successions that continue the same application; each continuing application is a new application in its own filing year, and its parent's refusal is its final decision | about 27.9 | none |

Direction: rungs 1 to 3 walk the figure up, and the decisive rung turns it back down. Rung 3 sits about 12.5 per cent above the answer and rung 2 about 14.7 per cent below, so the answer is bracketed. The partial splits are priced at stage 2: the continuing application kept in its parent's filing year because it claims the parent's benefit, and the parent ended at the continuing application's decision.

Twin pair (moved from the note to the decisive rung): two CX successions identical on every docket, action and continuity column. Same group and examiner, first docket on 3 March 2022, refusal at 14.5 months, successor docketed the same day, allowance at 29.3 months. One is a re-examination: the applicant waited 29.3 months. The other is a continuing application: its parent was finally decided at its refusal, 14.5 months. That is 2.02x apart, and only the production ledger's credit class separates them.

## Why it survives the solver

Read against the pilot's record, the decisive rung avoids every route the plain solver used. No shipped sentence describes the split. The CX gloss describes the file moving, which is true of both routes. The production standard defines credit classes, not dockets. In the solver's reading the charter's "application" is satisfied by chaining every CX edge, so there is no rule to execute. No reproduction check signals it: the partner office's file certifies the fully chained construction on every programme case, because the programme bars a continuing application on a programme file, and the annual report counts dockets, which tie under every rung. The chained build has no loose end and passes every reconciliation a solver writes for itself, with one filing, one final decision and one cohort per chain. The decisive fact is operational and sits in a record the pendency question gives no reason to open, the examiner production ledger, which is the shape of the FC01 hold. A solver that does open it meets a credit class that contradicts both the docketing label and the construction the corpus has just certified. That reads as a workload convention more readily than as a second application, which is the OS01 decline ("the files do not say whether..."). The residual risk is named here. The ledger joins on docket number, which is the key-lining-up join that cracked task121 (RC01 v2) from the schema alone. This build's defence at that join is motive, not concealment: by the time the ledger would be opened, the pendency question is already answered and certified at rung 3.

## Nearest exemplars

1. *Adopt the arrival-based 2026 cover schedule with GMR at 50,670 minutes at p90* (Supply Chain & Logistics, Replenishment Cover Standards), measured mean **0.13** over 4 runs (0.21, 0.21, 0.00, 0.21). It is nearest on the statistic and on the decisive move's form: a duration percentile on a unit built from records (one observation per depot arrival, timed from its earliest order), plus a population fixed only by comparing release dates against a register that carries no flag column. The model compiled at the file's natural grain and shipped a schedule its own run-back refuted. This build keeps the unit construction and drops the refuting control set, which the pilot shows the plain solver uses as a search signal.
2. *Estimate 2,591,394 applicant units eligible for the Winter Relief Grant at 185 percent of the poverty guideline* (Nonprofit & Grant-making, Means-Tested Grant Eligibility Estimation), measured mean **0.17** over 4 runs (0.16, 0.18, 0.18, 0.18). It is nearest on the direction of the decisive move: the record the data offers (an occupied housing unit) has to be split into the units the rule counts (applicant units), and the model explicitly declined to split. Here the record the natural build offers is the CX-linked chain, and the decisive move splits some chains into two applications.

## Guard

Verdict on the drafted card: **WARN**, exit 0, with task124 and task125 filed (the window is task122, task124 and task125). Nearest drivers: 0.09 for this slot's own lineage v0 and for task68, and 0.06 or lower for task119 v1, task66 and task82 v2. Nothing reaches the 0.12 near-driver line.

The note's draw as written was BLOCK. Four findings were raised, and each was cleared by redrawing the axis it named:
- card: world.people was empty. Six personas were drawn with guard.py names.
- ban.subdomain (policy-education/public-administration against task119): this fired at the first check, while task119 sat in the window. Once the coordinator filed task124 and task125, task119 left the window, and public-administration is both legal and the honest key.
- ban.artifact (monitoring_export against task121, then in the window): the context artifact is last year's annual report pendency table (published_series).
- test.same_puzzle_older and test.same_driver_older on (population, D), spent in 13 and 7 earlier builds: the decisive rung was redrawn to G3, with D kept for rung 3.

The redraw raised one BLOCK, test.same_puzzle_older against task82 v2 (population, G3, quantity_figure). It is cleared by a differentiation line on the card: task82 joins orphan purchase records to the member a credit ledger assigned them, adding volume over a count threshold. Here the natural build has already joined docket successions, and the decisive move splits the successions a credit class marks as new applications. That re-dates starts and ends in a duration distribution, and no record is attributed to a different holder.

WARNs answered:
- people.first (Connie, against task100): cleared by taking the next drawn name, Cristina Turner, not by typing one.
- overuse.org_family (government_agency, 21 builds): a national patent office is a government agency. That is the honest key, and the forum and forcing event differ from every build in the window.
- repeat.decision (quantity_figure, against task125): the single statutory figure is the note's committed call. The answer unit (months of pendency), the shape (14 against task125's 02) and the decision's subject (a reported duration, not a call-off count) all differ, and varying the type would replace the note's call.

## Changes from the source note

1. Decisive rung redrawn. The note's chaining of dockets into applications along CX edges is kept as rung 3 and is no longer decisive. The charter's "application", the CX code glossed as continued examination and the schema-visible continuity table hand it to a plain solver, and its driver repeats task90. The new decisive rung splits CX successions that opened continuing applications.
2. CX recast. A CX edge now records that a refused application's examination file moved to a new docket. It covers both re-examination of the same application and a continuing application filed on the transferred file. The docketing codebook glosses it that way, true at its stated meaning.
3. Corpus redesigned. Programme applications can be re-examined (so programme cases carry CX successions), but they are never continued on a programme file. The partner file therefore certifies rung 3 on every case and kills rungs 0 to 2. It is structurally blind to the split, and it nominates the decoy, not the answer. The note's partner file was blind to chaining itself.
4. Decisive evidence placed in the examiner production ledger, through the credit class on each successor's first action. The production standard defines the class. The note's ask B used the HR roster, and stage 2 keeps every ask off the production ledger.
5. Twin pair moved from the note's first-docket-against-CX-docket pair to the decisive rung: re-examination against continuing application, 29.3 against 14.5 months.
6. World filled where the note was silent. The office sits in a fictional country (Republic of Morvane), because a national patent office is unique to its country and a real one would carry fabricated records. The partner is the Saravel Intellectual Property Office, and six personas were drawn with guard.py names. The fiscal year stays October to September, and the scale is rescaled at stage 2, because the note's 2.9 million dockets and 380,000 FY2022 applications are USPTO-sized.
7. Context artifact named: last year's annual performance report pendency table, examiner docket pendency (published_series). This is the series the deputy commissioner's belief and the examiners' association's licensed basis rest on. It reports past years' docket pendency and computes no FY2022 figure.
8. Shape 14 chosen. The note's ask layer is re-cut at stage 2. Asks A and B (maintenance-fee shares, examiner headcount) are figures for other decisions (H18). Ask C names the four rung constructions with their match counts, which hands the ladder over, as the DA01 retirement recorded. The asks become the decisive construction's cuts by technology group, with silent devices on paths the main call never reads.
9. Deliverables changed from pendency_build.xlsx and pendency_curves.png to fy2022_pendency_headline.docx and fy2022_time_to_decision.svg: the headline section as the ministry receives it, and the chart the report prints. The docx/svg pair is unused in the last twelve builds.
10. The committed call kept as written: the FY2022 median in months to one decimal, retrospective for the reason under the DRAW block.

## Tried and rejected

- The note's chaining of dockets along CX edges as the decisive rung: a plain solver constructs it from the charter's "application", the CX gloss and the continuity table (pilot lessons: a charter definition and a join whose keys line up are executed), and its driver repeats task90; kept as rung 3.
- Keeping chaining decisive but hiding the link (no continuity table; the successor tied to its application only through shared file-wrapper documents, or through a compliance deadline that encodes the filing date): the shared-document match is task81's identical-set identity recovery, a deadline that encodes the filing date is a signpost the solver reaches while looking for each application's start, and with the start recorded directly the rung collapses, which the judge reads as recovering an unrecorded column.
- Examination done for the partner office in the office's own docket system as the decisive class: whatever records the class (a group code, a service invoice keyed on docket) is a visible flag or a join, and the sentence needed to make the class determinate tells the solver to exclude it.
- A national-phase or divisional start-date convention (international or deemed filing date against the docketing date) as the decisive move: one definition swap on the same population at the same moment (single_conceptual_flip), a Gate C fork unless filed, and executed once filed.
- Re-dating abandonments or refusals to a legal effective date or to the close of a review window: a reading of the end event (single_conceptual_flip), and the charter's "the office's final decision" points at the notice.
- The split evidenced by an application filing fee on the successor docket in a prosecution fee ledger: exact, but FY2022 filing fees are a natural control total for the cohort, so a solver reconciling its chained cohort against them finds the gap; moved to the examiner production ledger, which no pendency control uses.
- The split evidenced by the successor's first office action code (a first examination report against a re-examination report) or by the statutory timing of the two routes: both sit in, or are checked against, the action history the natural build already reads, so a validation the solver writes for itself finds them.
- The partner file left blind to chaining as the note had it: with chaining demoted to rung 3 a blind corpus leaves the stop rung unconfirmed; the corpus now certifies rung 3, which nominates the decoy.
- A forward-facing re-root of the call (a restated pendency standard for FY2027 filings, or the FY2024 cohort's median at the censoring edge) to host an FC01-style re-timing: it makes the graded figure a forecast and moves the build off Descriptive, an objective the pipeline assigns and does not redraw.
