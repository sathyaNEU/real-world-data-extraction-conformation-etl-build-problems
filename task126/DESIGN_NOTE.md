# task126: the Morvane Patent Office's FY2022 headline pendency, realising analytical_tasks note DA02 (analytical_tasks/03_descriptive_distribution/DA02_pendency-median-docket-versus-application-grain.md)

Stage 1 (draw), drawn 2026-10-10. This is the build's one design note; the design stage extends it. The note is the idea and this build is its first realisation. Its world, its committed call and its corpus survive; its decisive rung (chaining dockets into applications along CX edges) is kept as rung 3, and a new decisive rung sits above it (see Changes and Tried and rejected).

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? Card filed: registered 2026-10-10 by the coordinator after task125 (WARN, answered under ## Guard)
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

## Stage 2: design (2026-10-10)

Every figure below is a target the generator builds forward and asserts. The targets come from a scratch paper model of the docket world (applications filed daily FY2016 to FY2026, first-docket and successor decision times by group, refusals, CX transfers by route, CN and DV children, grant lags, the 30 September 2026 censor, Kaplan-Meier quantiles). The model is not the generator and does not ship. Stage 3 tunes the generator to the same parameters, asserts every separation floor stated here, and records the realised figures beside these targets; a realised figure may move by a few hundredths, a separation floor may not be breached. Months are days divided by 30.4375 throughout.

### What the design stage settled

1. **The ladder is re-solved on the model, and every rung figure moves.** Rungs 0 to 4 file 23.2 / 20.9 / 25.7 / 33.9 / 28.9 months (the draw carried the source note's 22.4 / 19.0 / 23.8 / 31.4 and a provisional 27.9). The shape is unchanged: rungs 1 to 3 walk the figure up, and the decisive rung turns it back down.
2. **About one in four CX successions is a continuing application, not two in five.** At two in five the continuing applications are so many short new applications that rung 4 falls into the docket-grain rungs (within 2 to 4 per cent of rungs 0 and 2 on every parameter set tried). At 27 per cent of the successions docketed in FY2022 (7,986 of 29,845) rung 4 clears rung 2 by 11.3 per cent and rung 3 clears it by 17.0 per cent (Tried and rejected).
3. **The world that carries the ladder** has slow first-docket allowances and short successor examinations: first-docket decisions at a median of about 22 months (allowances about 26), successor dockets decided at a median of about 13 months, refusals on 48 per cent of first dockets, a transfer on 92 per cent of refusals, and 42.5 per cent of FY2022 applications transferred at least once. Filings ease about 2 per cent a year over the decade, so relatively more continuing applications reach FY2022, which keeps the nearest partial cell (continuing applications left out of the cohort) at 6.9 per cent.
4. **A refused docket closes on its refusal date.** Its end code is REF, rewritten to CX when the file passes to a new docket; the successor is docketed when the request for re-examination or the continuing application arrives, 5 to 60 days later. So the parent's end is the refusal notice whichever date a solver reads (notice or docket close), and that fork converges (it was +0.4 per cent when the docket closed on the request date).
5. **The decisive evidence is set.** The examiner production ledger credits each first action on the merits with a class: 1N (the first action on the merits in an application, credited once per application) or 1R (the first action on the merits after a refusal is set aside on a request for re-examination). The ledger is keyed on action id and examiner, so it reaches a docket only through the action history. A chain carrying two 1N credits is two applications. No sentence anywhere says that a CX succession can open an application.
6. **The ask layer is one wide device-carried ask, the eight technology groups on three figures each.** Its primary device is the 1 October 2023 restatement of the technology groups (the docket's group code is the code in force when the docket opened; the report restates on the structure in force at the extract), and its hazard is docket transfers between art units (the docket row carries the art unit at close). Both sit on columns and files the main call never reads. The group methodology lives in the report's table notes, never in the charter the main call reads.
7. **The programme's rules are not shipped.** The corpus is blind to the split by construction (no programme application in the corpus has a continuing successor, asserted), and no sentence explains why, because the explaining sentence (a continuing application may not be examined on a programme file) would tell every solver that continuing applications are examined on transferred files.
8. **The opening move is situation-first.** The draw's provisional number-first repeats task123, inside the last three builds.
9. **Kept as drawn:** the pairing, shape 14, the committed call, the two deliverables and their names, the forum, the forcing event, the six personas, the as-of date (23 November 2026) and the 30 September 2026 extract.

### Stump sentence (re-solved)

A competent solver chains every CX succession into one application, dates it from its first docket, ends it at its last docket's final decision notice, censors the undecided at the 30 September 2026 extract, reproduces every one of the Saravel office's 5,358 acknowledged final decisions to the day and files 33.9 months; the step that lands it there is reading every CX edge as the same application continuing, when about one in four of them carried a refused application's file to a continuing application filed on the successor's docketing date, whose first action the examiner production ledger credits as the first action on the merits in an application (1N, credited once per application), so each of those is a new application in its own filing year and its parent was finally decided at its refusal, and the FY2022 median is 28.9 months.

### Gate G

- **Litmus.** No. Every figure in the pack is correct at its stated meaning and stays correct: the docket table, the continuity table, the action history, the production ledger, the Saravel acknowledgements, last year's pendency tables. No stakeholder's claim about their own numbers is overturned: examiner docket pendency is a true statement about dockets, the deputy commissioner's belief is a belief, and the association's basis is stated as theirs. The task does not exist to correct a reading of a correct number; the difficulty is which records form one application.
- **Primary mechanism:** `method_or_model_selection` (the unit is constructed, and only one construction survives every shipped fact), with `decomposition_attribution` supporting.
- **Judge reading (stage 6 pass 1).** `etl_conformance`, `mixed`, no, no. Both mechanisms pass; the family differs because the judge counted the deputy commissioner's docket-series belief as a shallow rejection layer that the write-up led with. The write-up now opens on the construction and carries the rejected bases inside the steps, so the reading a reviewer meets first is the construction.
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** Delete the deputy commissioner's belief, the association's basis, last year's pendency tables and the social thread. The docket table still offers one tidy row per docket, the continuity table still chains CX edges, the Saravel file still certifies the fully chained build on 5,921 of 5,921 decided cases (6,300 of 6,300 with the open ones), and rung 3 still files 34.0.
- **Clean-data test, three depths.** Fill: no file on the main path is incomplete; the 13 per cent undecided are decisions that have not happened, all older than every graded quantile, so a later extract moves no graded figure (asserted: every undecided FY2022 application is at least 48 months old at the extract, above the largest group median and above 36 months). Semantics: every field means what its codebook says; the CX gloss (the examination file passed from a closed docket to a new docket) is true on both routes. Instrument: the judge's test is whether the task still stumps on perfectly clean, correct data, and it does, because every file here is already clean and correct. The house's stricter third depth (replace the instrument with one that observes the decision's own quantity) would swap the docket system for the application register, a different system recording a different unit; that is the exposure every unit-construction build carries (measured traps #2 and #13), recorded here rather than argued away. No repair of the docket system itself, short of adding the other system's key, moves any rung.
- **Lens swap.** Rung 3 and the answer cover different populations at different dates: 57,418 chained applications against 66,186 applications (the 8,768 continuing applications filed in FY2022 join, and the continuing parents end at their refusals). Not one population under two lenses.
- **Pre-draw identity.** The median of (final decision date less filing date) over FY2022 applications. Every input ships except the membership of "application", which no file states and which neither the corpus nor any count control forces.
- **Corpus direction.** Under the natural path (rung 3) the Saravel file reproduces: 5,921 of 5,921 acknowledged decisions to the day, the 379 open cases as open, and all 16 quarterly medians. It never refutes rung 3, because no programme application has a continuing successor.
- **No shipped artifact ranks or files the headline wrongly as its own claim.** Last year's pendency table reports examiner docket pendency, labelled as such, for closed docketing years FY2006 to FY2025, and computes no FY2022 application figure.

### Entity, unit of value and decision

- **Entity and unit.** The Morvane Patent Office examines patent applications and is scored, in its statutory annual performance report, per resolved case: the time each application waits from filing to the office's final decision.
- **Two quantities that both read as size.** A docket's time from docketing to close, and an application's time from filing to its final decision. And inside the application grain, a CX chain read as one application against the same chain split where a continuing application opened. They size FY2022 differently because 42.5 per cent of applications pass through at least one transfer and about one in four transfers opens a new application.
- **Decision.** The FY2022 headline median filed in the annual performance report with the Minister for Enterprise on 31 January 2027. Shape 14, cuts of a distribution.
- **Tense.** Retrospective, for the reason under the DRAW block: a statutory statement about a cohort still in flight, which no later decision can move.

### The answer

**28.9 months.** The Kaplan-Meier median of time from filing to final decision over the 60,266 FY2022 applications (52,280 applications whose first docket was opened in FY2022, CN and DV children included, plus 7,986 continuing applications filed in FY2022 on transferred files), undecided applications censored at 30 September 2026.

- **Its supporting figures:** lower quartile 19.8 months; 11.4 per cent of FY2022 applications undecided at the extract (6,840 of 60,266 in the model); 65.9 per cent decided within 36 months.
- **Bins.** Stage 3 tunes the seed so the median sits between 28.88 and 28.92 (mid-bin, never on 28.90 itself) and asserts no decision lands within three days of the crossing, so the calendar-month count and every month divisor between 30.4 and 30.5 file the same tenth.
- **Rank on the natural pipeline.** Rung 0 files 23.2; the answer is the fifth of five rung figures by ladder order and sits between rung 2 and rung 3 in value.

### The ladder

Five rungs on the FY2022 cohort, every figure computed by the model from docket-level records and asserted by stage 3. Distances are against 28.9.

| Rung | Construction | FY2022 median (months) | Against the answer | Gap it opens | Killed by (one shipped fact) |
|---|---|---|---|---|---|
| 0 | The production system's examiner docket pendency: the 82,125 dockets opened in FY2022, docketing to docket close (grant for an allowed docket), Kaplan-Meier | 23.2 | -19.7% | rule (the end event) | The Saravel acknowledgements: every acknowledged allowance is dated at the notice of allowance, 97 to 180 days before the grant; the docket-close construction misses all 3,976 allowed cases with a grant by the extract |
| 1 | The same dockets ended at their decision notice in the action history, a CX docket ended at its refusal | 20.9 | -27.7% | population (dockets against applications) | The docket end codes and the Saravel file: a CX close is no final decision; on the 2,165 decided re-examined programme cases the acknowledged decision falls on the successor docket, dated from the first docket's filing |
| 2 | CX dockets censored at the transfer, every other docket ended at its decision notice | 25.7 | -11.3% | population (the transfer is the wait continuing) | The same 2,165 cases: each acknowledged decision is a decision on the application whose first docket the censored docket was, so the censoring is informative and the cohort is applications, not dockets |
| 3 | Every CX edge chained into one application, dated from the first docket, ended at the last docket's final decision notice, CN and DV children kept as applications in their own right | 33.9 | +17.0% | population (which successions open an application) | The production ledger with the production standard: the first action on 7,986 of the 29,845 CX successors docketed in FY2022 (and on about 27 per cent of CX successors in every year) is credited 1N, the class credited once per application, so each of those successors is a new application filed on its docketing date and its parent was finally decided at its refusal |
| 4 | **Decisive:** chain only the CX edges whose successor's first action is credited 1R; each 1N successor starts a new application dated from its docketing; its parent ends at its refusal notice | **28.9** | answer | | |

**Why each rung is a place to stop.**

- **Rung 0.** It reproduces last year's examiner docket pendency table to the tenth for every docketing year both cover (FY2016 to FY2021), it is the office's twenty-year number, and it is the deputy commissioner's belief. (Measured trap #7, the ready-made measure.)
- **Rung 1.** It replaces the production system's grant date with the decision notice and so reproduces every Saravel decision on a programme case with one docket (3,193 of 5,358), every allowance among them to the day. (Trap #12, the first control that passes.)
- **Rung 2.** The textbook treatment of an exit that is not the event; every reconciliation a solver writes on dockets still passes. (Trap #2, the file's rows taken for the unit.)
- **Rung 3.** It builds the charter's application from the continuity table, reproduces all 5,358 acknowledged decisions to the day and all 16 Saravel quarterly medians, leaves no loose end (one filing, one final decision and one cohort per chain), and agrees with the examination practice manager that a refused file returning on a new docket is the same file. (Trap #13 behind #12: validated on the programme population, applied to the office's.)
- **Rung 4** is the answer.

"A solver who does everything right up to rung 3 commits to 33.9 months." "A solver who cleans perfectly and stops at rung 2 commits to 25.7 months."

- **Every rung a different figure:** yes (23.2, 20.9, 25.7, 33.9, 28.9), pairwise at least 2.3 months apart.
- **The rung that carries the stump:** rung 4. The strong solver stops at rung 3; a solver who never chains stops at rung 1 or 2.
- **The seven survival properties for rung 4.**
  1. *Written in no shipped sentence.* The CX gloss says the file passed to a new docket, true on both routes; the CN and DV glosses describe children opened on a new file; the production standard defines credit classes and says nothing about dockets, transfers or continuing applications; the charter says "application" and the corpus certifies chaining. No sentence says a CX succession can open an application, and the sentence that would explain the corpus's blindness is not shipped.
  2. *No sweepable corpus nominates it.* The Saravel file returns 5,358 of 5,358 under rungs 3 and 4 alike (asserted twice: no programme application has a 1N successor, and the two constructions agree case by case on every corpus case). It nominates the decoy.
  3. *No arithmetic symptom.* Docket counts tie to last year's report under every rung; every docket has one end; the action history reconciles to every docket; every chain has one filing and one final decision; the ledger's credits tie to the action history one to one. Nothing fails on the chained build.
  4. *Not a row predicate.* The split is a property of a chain (two 1N credits inside one CX chain), reached through the ledger's action id to the action history to the docket to the continuity edge. No docket, action or continuity column marks it; successor first actions carry the same action code and the same timing distribution on both routes (asserted).
  5. *The enumeration is arithmetic.* Which successors open applications is recovered by walking every chain and counting its 1N credits; 7,986 FY2022 successors and their own re-examination chains are re-dated and re-cohorted that way.
  6. *No cutover date.* Continuing applications run at about 27 per cent of transfers in every year FY2016 to FY2026 and no series steps.
  7. *Survives deletion* (Gate G above).
- **Worth of each rung on the graded quantity (the median):** 0→1 -9.9%, 1→2 +22.6%, 2→3 +32.0%, 3→4 -14.6%.
- **Sign:** rungs 1 to 3 walk the figure up; only the decisive rung turns it back. Rung 0 sits above rung 1 because it carries the grant lag.

### Position and separation

The answer is a figure graded to the tenth, so the separation floor binds rather than a ranking margin (stumping Part 3); the 1.20x rung-margin floor guards a winner in a ranking and has nothing to guard here. The nearest rungs are rung 2 at -11.3 per cent and rung 3 at +17.0 per cent, so the answer is bracketed and no rung lands within 11 per cent of it. The decisive rung is worth 5.0 months against rung 3 (14.6 per cent of the pre-decisive figure), which clears the separation floor by 2.4x on its own.

### The correction grid

Toggles: end event (grant, decision notice) × unit (docket with the transfer as an end, docket censored, CX chain, chain split at 1N) = 8 cells, plus the partial applications of the decisive rung, the family chain and the cohort readings. Every cell is computed by the model and asserted by stage 3 against its stated floor.

| Cell | FY2022 median (months) | Against 28.9 | Violates |
|---|---|---|---|
| dockets, grant end (rung 0) | 23.23 | -19.7% | the Saravel allowance dates |
| dockets, notice end, transfer as an end (rung 1) | 20.93 | -27.7% | the end codes and the re-examined corpus cases |
| dockets, notice end, transfer censored (rung 2) | 25.66 | -11.3% | the re-examined corpus cases |
| CX chains, notice end (rung 3) | 33.87 | +17.0% | the ledger's 1N credits read with the production standard |
| CX chains, grant end | 37.49 | +29.5% | the Saravel allowance dates |
| split at 1N, grant end | 32.10 | +10.9% | the Saravel allowance dates |
| split at 1N, notice end (answer) | 28.94 | | |
| partial: parents ended at their refusals, continuing applications left out of FY2022 | 30.95 | +6.9% | the charter's cohort (each fiscal year's filings) and its filing date (the date the office received the application) |
| partial: continuing applications added, parents still chained to their end | 31.51 | +8.9% | the 1N credit on the successor (a parent cannot run on through another application's examination) |
| partial: continuing applications dated from the parent's filing (the benefit claim), cohort by the parent's year | 32.69 | +13.0% | the charter: a priority or benefit claim does not move the filing date |
| partial: parent ended at its docket close instead of its refusal notice | 28.94 | converges | (C1: a refused docket closes on its refusal date) |
| decided applications only, the undecided dropped | 26.74 | -7.6% | the charter: an application not finally decided at the extract counts as still waiting |
| family chain: CX, CN and DV edges all chained | 34.76 | +20.1% | the codebook: CN and DV children are filed on a new examination file, so each is its own application, and the charter's filing date |
| CX chains, cohort by any docket opened in FY2022 | 39.46 | +36.4% | the charter: each fiscal year's filings |
| plain median with the undecided set to the extract | 28.94 | converges | (C1: every undecided application is older than the median) |
| calendar-year 2022 cohort | stage 3 computes; asserted at least 6% off or converging | | the charter's fiscal year (1 October to 30 September) |

The nearest wrong cells are the two partials at +6.9 and -7.6 per cent; both are single violations of a charter sentence, and both clear the 6 per cent floor. Stage 3 asserts every cell's distance and fails the build if either partial falls under 6.5 per cent.

### The calibration corpus

- **Form.** Counterparty acknowledgement: the Saravel Intellectual Property Office's acknowledgements of the office's final decisions on the 5,760 work-sharing applications filed FY2019 to FY2022 (5,358 decided by the extract, 402 open), each with the office's application number (the number of the docket opened at filing), the filing date, the decision acknowledged (allowance, refusal or abandonment) and its date; and a second sheet of the partner's quarterly medians of days from filing to the acknowledged decision for the 16 filing quarters.
- **What it certifies.** The decision notice as the end, and chaining across transfers. Rung 3 (and rung 4) reproduce 5,358 of 5,358 to the day and all 16 quarterly medians. Rivals: rung 0 misses all 3,976 allowed cases whose grant fell before the extract, by 97 to 180 days, every miss in the same direction; rung 1 misses all 2,165 decided re-examined cases (ended at the first refusal, short by 5 to 30 months); rung 2 has no decision on those 2,165; the aggregate gap on the quarterly medians is directional for each rival (rung 0 above, rungs 1 and 2 below, on all 16 quarters).
- **What it is blind to, and why.** The split. No programme application in the corpus has a successor credited 1N, so rungs 3 and 4 agree case by case on every corpus case. The blindness is constructed (the programme agreement bars a continuing application on a programme file, in the fiction and in this note only) and asserted twice: on the property itself (zero 1N successors among the corpus's chains) and by re-running the corpus under both constructions.
- **Every rule the golden composes has a case that would break if flipped.** The end event: the allowed cases. Chaining across a transfer: the re-examined cases. Censoring: the 402 open cases, which the partner's quarterly medians count as still waiting (the charter's convention), so a decided-only construction misses the FY2022 quarters' medians (asserted on at least three of the four). The split itself is the one rule the corpus cannot test, by design; it is pinned by the production standard's definition, not by the corpus.
- **Twin pair.** Two transfers identical on every docket, action and continuity column: same technology group, art unit and examiner, first dockets opened on 3 March 2022, refusals at 14.5 months (18 May 2023), successors docketed 2 June 2023, allowance notices at 29.3 months from filing (12 August 2024), the same action codes on the same dates. One successor's first action is credited 1R, the other's 1N. Under rung 3 both applicants waited 29.3 months; under rung 4 the first waited 29.3 and the second application was finally decided at its refusal, 14.5 months (2.02x), while its continuing application is an FY2023 filing. Only the ledger separates them.
- **Resemblance points at the decoy.** The FY2022 docket profile (allowance rate, transfer rate, group mix) resembles the programme's applications, and the programme's transfers are all re-examinations, which is the reading rung 3 transfers to the whole office.

### Pins and counter-pins

| Pin | Where (authority) | What it fixes |
|---|---|---|
| The headline is the median time from an application's filing to the office's final decision on it, for each fiscal year's filings (1 October to 30 September), in months to one decimal; months are days divided by 30.4375 | performance reporting charter (level 1) | the quantity, the cohort, the unit and rounding |
| An application's filing date is the date the office received it; a priority or benefit claim does not move it | charter (level 1) | the start for continuing applications and for CN and DV children |
| An application not finally decided at the extract counts as still waiting at the extract | charter (level 1) | censoring, and the denominator |
| An application is numbered by the docket opened when it was filed | docketing codebook (level 4) | the key the Saravel file uses |
| CX, CN and DV glosses; end codes ALW, REF, ABN, CX; action codes | docketing codebook (level 4) | code semantics |
| 1N: the first action on the merits in an application, credited once per application; 1R: the first action on the merits after a refusal is set aside on a request for re-examination | examiner production standard (level 2) | the decisive classification |
| Licensed wrong basis: the Morvane Patent Examiners' Association publishes examiner docket pendency from the production system beside the office's headline | charter (level 1), as a matter of record | named as theirs, a docket measure |
| Empirical: the decision notice is the end, and a transfer re-examined is the same application | the Saravel file, 5,358 of 5,358 | axes 3 and 21 |

**Counter-pins: none.** No document says every continuing application is a CN or DV edge (the CN and DV glosses describe what they are, not what a continuing application must be); no document says a CX succession is always the same application; last year's table is labelled examiner docket pendency; the examination practice manager's line in the thread ("a refused file that comes back on a new docket is the same file") is true of both routes and names the file, not the application. Stage 3 greps every shipped document for "continuing", "continuation", "re-examination", "same application", "new application" and "credited once" and asserts each hit is in the one place this table names.

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | FY2022 applications: first dockets opened in FY2022 (CN and DV children included) and continuing applications filed in FY2022 on transferred files | the decisive construction; C4 for every other population (rungs 0 to 3, the partials, the family and any-docket cohorts) |
| 2 | Unit of account | the application (a 1R-chained run of dockets), not the docket, the CX chain or the family | C4 (rungs 0 to 3, the family cell at +20.1%); pinned by the charter's "application" and the production standard |
| 3 | Attribution window | the fiscal year of filing, 1 October 2021 to 30 September 2022 | pinned (charter); the calendar-year cell asserted at least 6% off or converging |
| 4 | As-of dating | the 30 September 2026 extract; every date in the pack on or before it | C1 (nothing later ships) |
| 5 | Version basis | one extract; no corrected or superseded dates | C1 (every docket, action and credit appears once) |
| 6 | Divisor and denominator | all FY2022 applications, the undecided censored | pinned (charter); C4 for decided-only (-7.6%) |
| 7 | Weighting | one application, one observation | C1 (no weights exist; asserted no duplicate application) |
| 8 | Measurement window length | one cohort | C1 |
| 9 | Boundary inclusivity | the first time survival falls to 0.5 or below; "within 36 months" inclusive | C1: no decision within three days of any graded crossing, and no decision 1,090 to 1,102 days after filing in the FY2022 cohort, so strict and non-strict readings select the same rows (asserted) |
| 10 | Rounding path | unrounded days to months, round once to a tenth | C1: every graded figure at least 0.02 from its bin edge, asserted |
| 11 | Tie-break | none needed | C1 (no two graded crossings coincide) |
| 12 | Maturity and censoring | Kaplan-Meier with the undecided censored at the extract | C1: every undecided FY2022 application is at least 48 months old, above every graded quantile and above 36 months, so Kaplan-Meier and the plain median and share agree (asserted) |
| 13 | Order of operations | split the chains, then assign cohorts by each application's own filing date | C4 (the benefit-dated partial at +13.0%, the left-out partial at +6.9%) |
| 14 | Row order | not order dependent | C1, asserted under three row orders |
| 15 | Duplicate resolution | none needed | C1 (no duplicate docket, edge, action or credit, asserted) |
| 16 | Identity normalisation | docket numbers in one format in every file; the ledger's action ids match the action history one to one | C1, asserted |
| 17 | Netting against gross | not applicable | C1 |
| 18 | Dimensional units | days, then months at 30.4375 | pinned (charter); C1 for calendar months and any divisor between 30.4 and 30.5 (no decision within three days of a crossing) |
| 19 | Code and status semantics | REF closes a docket on the refusal; CX is a transfer, never a decision; 1N and 1R as defined | pinned (codebook, production standard); C4 for the transfer read as an end (rung 1) |
| 20 | Integerisation | not applicable | C1 |
| 21 | Scope of a stated clause | "final decision" is the decision that ends the application: a refusal set aside on re-examination is not one, a refusal followed by a continuing application is | pinned empirically (the corpus, for the re-examination half) and by the production standard (for the continuing half); C4 |
| 22 | Forward window contents | retrospective; no decision after the extract can move a graded figure | C1 (axis 12) |

Three axes outside the 22 that this build carries, all closed: **the end event** (the decision notice, not the grant: C2 on the corpus, 3,976 allowed cases), **the start of a continuing application** (its own receipt date: charter pin, C4 at +13.0%), and **the technology group of an application** (the ask's axis, closed in the ask ledger).

### Deliverables and the criteria arithmetic

Shape 14, cuts of a distribution. Two files, both written by the golden script.

1. **`fy2022_pendency_headline.docx`** (the committing file, the headline section as the Minister receives it): the headline sentence as the report will print it, carrying the median; a table of the eight technology groups (on the structure in force at the extract), each with its lower-quartile and median pendency in months and the share of its FY2022 filings decided within 36 months; and the share of all FY2022 filings still undecided at the extract.
2. **`fy2022_time_to_decision.svg`** (the chart the report prints beside the headline): a title that states the median, the share of FY2022 filings decided by each month after filing as a step curve, a line at 50 per cent, the median marked and labelled with its value, and the undecided share annotated where the curve stops at the extract.

Criteria arithmetic: 8 groups × 3 figures = 24, plus the headline median, the undecided share, 5 named chart parts and 2 files = 33. Planning weights 38 / 7 / 55: the recommendation block is the headline median with the undecided share and the chart's median label and title; the instruction block is the two files and the chart's three format parts; the ask block is the 24 group cells.

- **Script-generated:** both files. **Unit and rounding:** one convention sentence in the prompt (every figure to one decimal, months for pendency and percentages for shares) and the call's own unit inside its sentence.
- **Distinct findings:** the headline median, the spread across groups (each group's quartile and median), the share resolved within three years by group, and the share still in flight. **Named-parts visual:** yes. **Breakdown at an explicit grain:** technology group. **Robustness:** the undecided share annotated on the curve is the check that the censoring cannot move the median (every undecided application sits past the last graded crossing).
- **The ask set does not over-determine the split.** The group cells are quantiles and shares of one construction; no figure asked for is a count of applications, so a solver cannot back out the 7,986 continuing applications from its own answers, and nothing in the pack publishes an application count to reconcile against.

### The ask ledger (supplemental-stumping)

**H18 read.** The group table is a component of the committed call: the report prints it directly under the headline, and the Minister's office reads the headline through it. It is not a figure for another period, another population or another decision, and it is not keyed to the call by name.

**Main call's declared row population** (generator constant `MAIN_ROWS`): the docket table's docket_no, docketed_on, closed_on and end_code for every docket; every continuity edge; the action history's docket_no, action_id, action_code and served_on; the production ledger's action_id and credit_class; the Saravel file; the charter, the docketing codebook and the production standard. **Zero device rows and zero hazard rows inside it, asserted**: the devices live only on the docket table's tg and art_unit columns, the transfer log, the art unit table, the report's table notes and the group table in last year's report, none of which the main call reads.

**Ask A: lower-quartile and median pendency, and the share decided within 36 months, for each of the eight technology groups** (months and per cent to one decimal; 8 × 3 = 24 figures).
- **Use.** The Minister's office reads the headline through the groups, and the group directors answer for their own rows in the January estimates hearing.
- **Off the ledger, in the draw's sense.** No figure asked for is a ledger quantity, no device or hazard sits on the ledger or the production standard, and the wording names neither; the ledger enters ask A only through the construction layer, the same split the headline needs.
- **Construction layer.** Every cell is a cut of the decisive construction: under rung 3 all 24 cells move (each group's median by 3.5 to 5.5 months in the model), so a response on the chained build loses the whole ask.
- **Path (10 files, 13 columns):** the docket table (docket_no, docketed_on, closed_on, end_code, tg, art_unit), the continuity table, the action history (action_id, docket_no, action_code, served_on), the production ledger (action_id, credit_class), the production standard, the docket transfer log (docket_no, transferred_on, from_au, to_au), the art unit table (art_unit, tg, valid_from, valid_to), the report's table notes, the charter, the docketing codebook.
- **Primary device (D2, silent): a stored group code taken before a silent restatement.** The technology groups were re-cut on 1 October 2023: about half the art units moved group and several group codes now name different technologies. The docket table's tg column is the group code of the docketing art unit when the docket opened, so every FY2022 docket carries a code from the old structure under the same eight labels. The art unit table is effective-dated, so the solver's default as-of join (the art unit's group on the docketing date) returns the same old codes and agrees with the tg column (a false clean). The table notes state that group tables are restated on the structure in force at the extract, each application counted in the group of the art unit that docketed it at filing. Organ pair: the table notes (documentary) and the art unit table's current rows (structural). Nothing in the pack narrates the re-cut.
- **Hazard H1 (D8/D7, silent): transfers inside a docket.** About 12 per cent of dockets move between art units while open; the docket row carries the art unit at close (or at the extract), and the docketing art unit is the from_au of the docket's first transfer. Organ pair: the codebook's art_unit gloss (holding at close) and the transfer log.
- **D9 false clean.** Last year's Table P2 (dockets opened by technology group at docketing, FY2021 to FY2025) ties exactly to a count by the docket table's tg column, so the careless grouping reconciles to a published table; the table is correct at its stated meaning (at docketing) and counts dockets, not applications.
- **Stops (stage 3 asserts each value and its distance per cell):** S1 natural (group by the tg column): all 24 cells moved in the model; S2 the as-of join on the art unit table (identical to S1, the false clean); S3 half-handled (the current group of the art unit at close, transfers ignored): 20 of 24 cells moved; S4 over-corrected (the current group of the examiner's home art unit from the roster, a declared distractor): stage 3 asserts at least 16 of 24 moved; answer.
- **Lazy delta:** S1 wrong on 24 of 24 cells. **Composed deltas:** every subset of {primary mishandled, hazard mishandled} lands at least one bin away on at least 16 cells, asserted.
- **Decoupling, asserted.** Recompute the headline and the undecided share under every stop: unchanged to the hundredth. The cracker and mirror sheets differ on the 24 cells only through the construction layer.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta (stage 3 asserts) |
|---|---|---|---|
| H1 docket transfers between art units | examiners and work are rebalanced between art units while a docket is open; the production system keeps the holding art unit | Ask A, every group that sends or receives transfers | at least 16 of 24 cells one bin or more (20 in the model) |
| (primary) the 1 October 2023 group re-cut | the office's reorganisation of its technology groups | Ask A, all cells | 24 of 24 in the model |

One ask carries the layer, so the hazard table is short by design: every further hazard on this path would sit on the decision dates or the cohort, which are the main call's rows. One referee: the art unit table, byte-clean and never trapped; its current rows arbitrate the designed disagreement between the tg column and the restated structure, and it carries no figure.

**Pair arithmetic.** At planning weights (38 / 7 / 55), `r` read as the recommendation criteria a rung-3 response keeps (the chart's form parts that do not carry a figure, about 4 points): 55 × (Lc + Ls) ≤ 28 - 4 = 24, so Lc + Ls ≤ 0.44. Mirror sheet (rung 3): every group cell wrong through the construction, Ls about 0.02, so S = 4 + 7 + 1 = 12. Cracker sheet with the habitual battery applied (tg or the as-of join): Lc about 0.02, C = 46, pair 29. Cracker that also finds the re-cut but not the transfers: Lc = 4/24 = 0.17, C = 54, pair 33. A cracker that handles both devices takes the ask (C = 100, pair 56): that is the layer's exposure, it needs the strongest response to find both the restatement and the transfers, and it is recorded here rather than hidden. If no top response lands the call (the measured outcome on the client's trap #13 tasks), the pair is about 12.

### Assertion plan (generator and independent verifier, 46 planned)

- Rungs 0 to 4 by value, pairwise distinct, each rung's distance from the answer, the floors: rung 2 at least 10% below, rung 3 at least 12% above (5).
- The answer, its lower quartile, the undecided share and the 36-month share; the answer between 28.88 and 28.92; no decision within three days of any graded crossing; no FY2022 decision 1,090 to 1,102 days after filing (7).
- Every grid and partial cell by value against its floor; both nearest partials at least 6.5% off; the two converging cells equal to the answer to the hundredth (3, table assertions over 16 cells).
- The corpus: 5,358 of 5,358 under rungs 3 and 4; rung 0 misses all allowed cases with a grant by the extract, every miss in one direction, 97 to 180 days; rungs 1 and 2 miss all decided re-examined cases; each rival's direction on all 16 quarterly medians; decided-only misses at least three FY2022 quarters (6).
- Blindness twice: zero 1N successors among the corpus's chains, and rungs 3 and 4 equal case by case on the corpus (2).
- The decisive classification: every first action on the merits carries exactly one credit; every first docket and every CN or DV child carries 1N; every CX successor carries 1N or 1R; no programme successor carries 1N; the continuing share of CX successors between 0.25 and 0.29 in every docketing year FY2017 to FY2026 (no step) (5).
- No visible tell on the routes: successor first-action timing, action-code sequence, examiner, art unit and group distributions equal across 1N and 1R successors within stated tolerances (a two-sample test on timing at p above 0.2) (2).
- The twin pair: identical on every docket, action and continuity column, 29.3 and 14.5 months, the only difference the credit class (1).
- The undecided: every undecided FY2022 application at least 48 months old at the extract (1).
- Clean-data and lens-swap: no file repaired moves a rung (the refusal-to-transfer gaps, the transfer log and the ledger are complete); rung 3 and the answer differ in membership (2).
- Separation: zero device and hazard rows in `MAIN_ROWS`; the headline and the undecided share unchanged under every ask stop (2).
- Ask A: every stop's 24 cells and their distances, S1 equal to S2 (the false clean), Table P2 tied exactly by the tg count, the hazard moving at least 16 cells, every composed subset at least 16 (5).
- Input gates and greps: files, formats, the spine's rows, two declared distractors in `metadata.json`, the pin vocabulary grep (each sensitive phrase only where the pins table puts it), no input file named in any document beside its provenance line (5).

### Pack plan (stage 3 builds against it; names provisional, in the office's own idiom)

| Role | File (provisional) | Path |
|---|---|---|
| Spine | `examination_dockets_FY2016_FY2026.parquet`, about 835,000 rows, one docket (docket_no, docketed_on, art_unit, tg, examiner_id, closed_on, end_code) | main (and ask A through tg and art_unit) |
| Operating extract | `office_actions_FY2016_FY2026.parquet`, about 3.4 million rows (action_id, docket_no, action_code, served_on) | main |
| Operating extract | `docket_links.csv` (parent_docket, child_docket, link_type CX, CN or DV, linked_on) | main |
| Operating extract | `examiner_production_ledger_FY2016_FY2026.csv` (credit_id, examiner_id, action_id, credit_class, counts, pay_period) | main (decisive) |
| Governing document | `examiner_production_standard_2019.pdf` (credit classes, counts, quality factors) | main (decisive) |
| Governing document | `performance_reporting_charter.pdf` (the pins, the licensed wrong basis) | main |
| Calibration corpus | `saravel_ipo_acknowledgements_FY2019-FY2022.xlsx` (the partner's acknowledgements, and its quarterly medians sheet) | main |
| Context artifact | `annual_report_2025_tables_P1_P2.xlsx` (P1 examiner docket pendency by docketing year, reported once 98 per cent of a year's dockets have closed, FY2006 to FY2021; P2 dockets opened by technology group at docketing, FY2021 to FY2025) | context, ask A (P2, the false clean) |
| Ask A | `docket_transfers.csv`, `art_unit_groups.csv` (art_unit, tg, tg_name, valid_from, valid_to), `report_table_notes.docx` | ask A |
| Social layer | `headline_section_thread.eml` (the deputy commissioner's belief, the work-sharing coordinator on the partner file, the examination practice manager on refused files, the association's secretary on publishing docket pendency) | none |
| Dictionary and provenance | `docketing_codebook.md`, `extract_notes.md` (the production systems manager's extract record, sources, dates and licence) | all |
| Distractors (declared in `metadata.json`) | `examiner_roster_2026-09-30.csv` (each examiner's home art unit and group at the extract: a wrong route to the group cells, ruled out by the table notes' docketing art unit) and `international_pendency_comparison_2025.xlsx` (published pendency figures of the partner and three other offices, a different question about other offices) | none |

Sixteen files, seven formats (parquet, csv, xlsx, pdf, docx, md, eml). Every series is synthetic (a fictional office, so no real register can be used without fabricating its records); the provenance record says so, with dates and a CC BY 4.0 licence for the synthetic release. No shipped file carries an application number other than a first docket's number, and no shipped file carries a filing-date anniversary (renewal fees, term expiry or publication dates), because each of those would date a continuing application from its own receipt and hand over the split outside the ledger.

### Realism debts

- **42.5 per cent of applications pass through at least one transfer.** Higher than the source note's 27 per cent. Forced: rung 4 has to clear the docket-grain rungs by more than 10 per cent, and only a large re-examination mass lifts the application median that far above the docket medians. Mitigation: in Morvane a refusal is the normal close of a contested first examination and re-examination on request is routine (comparable to the share of US applications that see a request for continued examination).
- **The docket extract carries no application number beyond the first docket's own.** Forced, because an application number on every docket is the column the build exists to withhold. Mitigation: the extract comes from the examination production system, which is docket-keyed, and the application register is a separate system; the codebook says an application is numbered by the docket opened when it was filed.
- **Successor examinations are fast (a median of about 13 months against about 26 for a first allowance).** Forced: rung 4 needs short successors in the docket cohort and long first examinations in the application cohort. Mitigation: a successor examines a file the examiner already knows.

### Stopping rule (written before any round)

- **At ceiling:** the plain solver lands 28.9 by joining the production ledger to the chains, in three consecutive hardening loops.
- **One more repair licensed:** the solver lands the call by a route other than the ledger (a timing or code difference between the routes, a filing-date anniversary, an application count), which is a leak to close, not a discovery to harden against.
- **Ship:** the solver files any other figure, 33.9 or not.

### Guard, re-checked at stage 2

The card's opening move is now `other` (situation-first, which the vocabulary does not list); nothing else on the card changed. `guard.py check` on the card now returns three BLOCKs (ban.role, ban.forum, ban.forcing_event), all against task130, which was drawn later on the same day with the same role family (statistical_office_head), forum (minister_or_cabinet) and forcing event (statutory_or_regulatory_filing). The guard's window sorts every other card by draw date and number, so a later draw lands in this build's window. task126 was registered first; the repeat belongs to task130's draw and is that build's to clear. This build does not touch task130's card.

### Prompt

`prompt.md`, 217 words, situation-first ("Not all of our FY2022 filings have a final decision yet"), two files, `voice-check.py 126` clean: 21.7 words a sentence, context 42.9 per cent (under the 46 per cent flag), no rounding tag beyond one convention sentence ("Everything there is to one decimal, months for pendency and percentages for shares") and the call's own unit, no "because", a short sentence ("No ranges."), no calcified carrier. The call closes the context as one quotable sentence (the median pendency of our FY2022 filings, in months to one decimal, as the one figure the headline prints), and both later paragraphs open on "that figure" or "the same figure". One belief, the deputy commissioner's, as one clause. Nothing names an input file, the partner, the programme, the ledger, a credit class, a transfer, a continuing application, the extract's structure, the group restatement or a method; nothing fixes the cohort's membership, the end event, the start date or the censoring (the September extract is named only as the moment the undecided share is read).

Gradability walk after compression: the median (months, one decimal, in the call); per group the lower quartile and the median (months) and the 36-month share (per cent), all under the convention sentence; the undecided share (per cent, convention); five chart parts (title stating the median, step curve of the share decided by month, the 50 per cent line, the median marked and labelled, the undecided share annotated). Criteria re-counted off shape 14: 24 + 2 + 5 + 2 = 33.

## Build record

Stage 3a, 2026-10-10. Generator `generator/build.py <out>` (modules params, world, analysis, tables, workbooks, docs, writers, checks) writes `<out>/target/` and `<out>/metadata.json` and fails on any of its 74 assertions. Independent verifier `generator/verify_pack.py <target>` reads only the shipped files (plus `metadata.json` beside `target/` for the distractor gate), rebuilds every construction with pandas and its own Kaplan-Meier, and checks 47 claims against its CLAIMS block.

**Gate outcomes.** Generator 74 of 74 green. Two scratch builds byte-identical (16 files plus `metadata.json`, sha256). Task-folder build identical to the scratch build, verifier 47 of 47 green on it. Producer-metadata audit (`scrub_producer_metadata.py`, band 2018-01-01 to 2026-11-23) clean. Input gates: 16 files, 7 formats (parquet, csv, xlsx, pdf, docx, md, eml), largest file `office_actions_FY2016_FY2026.parquet` at 3,580,785 rows, two distractors in `metadata.json` (`examiner_roster_2026-09-30.csv`, `international_pendency_comparison_2025.xlsx`), nothing under `target/` names either. Bundle 64 MB.

**Tuning.** First-docket median duration 677 to 673.5 days, the one parameter moved, to put the answer's crossing on day 880.

**Realised figures against the stage-2 targets.**

| Quantity | Target | Realised |
|---|---|---|
| Rungs 0 / 1 / 2 / 3 / 4 (months) | 23.2 / 20.9 / 25.7 / 33.9 / 28.9 | 23.1 / 20.8 / 25.4 / 34.0 / 28.9 (rung 2 -12.0%, rung 3 +17.6%, decisive rung worth 15.0% of rung 3) |
| Answer | 28.9 | 28.912 (880 days); lower quartile 19.7 (600 days) |
| Undecided at the extract | 11.4% | 10.6% (6,994 of 66,186; 10.567 unrounded) |
| Decided within 36 months | 65.9% | 65.6% (43,431 of 66,186; 65.620) |
| FY2022 dockets / CX successors / continuing | 82,125 / 29,845 / 7,986 | 90,884 / 33,466 / 8,768 (26.2%) |
| Rung-3 applications / answer applications | 52,280 / 60,266 | 57,418 / 66,186 |
| Grid: chains grant end, split grant end | 37.49, 32.10 | 37.49, 32.03 |
| Partials: left out, parents chained, benefit dated | 30.95, 31.51, 32.69 | 30.95 (+7.0%), 31.51 (+9.0%), 32.76 (+13.3%) |
| Decided only, family chain, any-docket cohort | 26.74, 34.76, 39.46 | 26.84 (-7.2%), 34.83 (+20.5%), 39.56 (+36.8%) |
| Parent at close, plain median, calendar year 2022 | converge | 28.91, 28.91, 28.91 (all converge) |
| Corpus cases / decided / open / re-examined | 5,760 / 5,358 / 402 / 2,165 decided | 6,300 / 5,921 / 379 / 2,658 |

Corpus back-test (verifier, from the shipped workbook): rungs 3 and 4 reproduce 6,300 of 6,300 cases (decisions to the day, opens as open) and all 16 quarterly medians; rung 0 matches 906, rung 1 3,642, rung 2 3,927. Every allowed single-docket case is missed by rung 0 by 97 to 182 days (2,709 cases with a grant by the extract). On the quarterly medians rung 0 and rung 1 sit below the partner on all 16 quarters and rung 2 above on all 16 (it never decides a re-examined case). Decided-only medians miss all four FY2022 quarters. Zero continuing successors in any programme chain; rungs 3 and 4 agree case by case.

Ledger: one 1N or 1R credit on every first action on the merits and on no other action; continuing share of CX successors 0.261 to 0.276 in every docketing year FY2016 to FY2026. No route tell: successor first-action timing KS p 0.096, successor decision timing KS p 0.62, successor end-code mix chi-square p 0.20, every successor docketed to the examiner holding the refused docket. Twin pair: 22-138479 then 23-160047 (1R, 29.3 months) and 22-138427 then 23-159894 (1N, parent decided at 14.5 months), identical on every docket, action and link column.

Ask cells (answer): 1600 16.2 / 23.4 / 79.6; 1700 17.5 / 25.7 / 74.1; 2100 18.4 / 26.8 / 71.6; 2400 19.8 / 28.6 / 66.1; 2600 20.6 / 30.0 / 63.0; 2800 21.0 / 30.6 / 62.5; 3600 21.8 / 31.9 / 58.6; 3700 24.0 / 35.2 / 51.6. Cells moved of 24: S1 tg column 23, S2 as-of join on the docketing art unit 23 (identical to S1, the false clean), S2b as-of join on the art_unit column 24, S3 current group of the art unit at close (hazard alone) 20, S4 roster home art unit 23, rung-3 applications on the answer's groups 24. Table P2 ties exactly to a count of the tg column. Table P1 reports FY2006 to FY2020 and FY2016 to FY2020 reproduce from the 2026 extract to the tenth.

**Departures from the stage-2 plan, each with its reason.**

1. The production ledger ships as Parquet, not CSV: 1,819,133 rows would have been about 90 MB as CSV. The docket, action and ledger extracts are Parquet with zstd compression.
2. The world is simulated from FY2003 and shipped from FY2016, so the FY2016 docket year carries successors of earlier filings and P1's counts carry no burn-in ramp (asserted). Links whose parent was opened before 1 October 2015 are kept; the codebook and the extract notes say so. No FY2022 application's chain touches a pre-2016 docket.
3. "No decision within three days of any graded crossing" and "no FY2022 decision 1,090 to 1,102 days after filing" are replaced. With about 40 decisions a day both are a visible hole in the distribution. The closures shipped: the headline crossing sits on day 880, so 879 and 881 file 28.9 too; every quantile definition (Kaplan-Meier at or below and strictly below, lower, higher, midpoint, linear) files the same tenth on the headline and on all 16 group month cells; no FY2022 application is finally decided 1,095 or 1,096 days after filing (88 decisions moved one to four days later), so the day count, calendar 36 months and inclusive counting select the same applications for every 36-month share.
4. The thinnest margins in the pack, stated: the 1700 lower quartile is 534 days, 17.5441 months, 0.006 under the 17.55 edge, and the 3700 median is 1,070 days, 35.154 months, 0.004 over the 35.15 edge. Both hold under the charter's divisor however it is rounded (30.437 to 30.44); under a 365/12-day month the 1700 lower quartile would file 17.6. The charter's "a month being 30.4375 days" is the pin that closes it.
5. The successor first-action timing test is asserted at KS p above 0.05, not 0.2: both routes draw successor timing from one distribution, and the realised p is 0.096.
6. A transfer on an FY2022 application whose successor would have no first action by the extract is not made (the refusal stands), so every FY2022 application's status is determined by the ledger (verifier: zero unclassified successors on FY2022 chains). Elsewhere a successor with no first action yet chains to its parent: the split is made only on a positive 1N.
7. Successor dockets are never abandoned (allowed 58 per cent, refused 42 per cent), carried from the paper model; it is the same on both routes.
8. Table P1 carries its in-file label as one line ("A production measure: it describes dockets, not applications"). It points away from rungs 0 to 2 and towards chaining, which is rung 3.

**Stage 3b, 2026-10-10 (write-up and ship checks).** `generator/golden.py` reads only `target/` and writes `golden/fy2022_pendency_headline.docx` (one A4 page: the headline sentence, Table 1.1 with the eight groups and an all-filings row, the undecided share, three notes citing the charter, the production standard and the table notes) and `golden/fy2022_time_to_decision.svg` (monthly step curve with every FY2022 filing in the denominator, the 50 per cent line, the median marked and labelled, the 10.6 per cent undecided bracketed where the curve stops at the extract, a title stating 28.9). It asserts every first action on the merits has one 1N or 1R credit, one decision notice per docket, and that every undecided application has waited at least 1,461 days, above every graded quantile and 36 months. Printed figures equal the verifier's CLAIMS: 66,186 applications (57,418 new filings, 8,768 continuing), median 880 days (28.9), lower quartile 600 days (19.7), 65.6 per cent within 36 months, 10.6 per cent undecided, and all 24 group cells. Two runs byte-identical; the scrub audit runs inside the script (band 2026-11-01 to 2026-11-23). The golden-realism pass ran after the figures froze (table widths, one page, footer with page number, signature-free SVG ids, house font) and moved no figure. One pack regeneration in this stage: the thread's sign-offs repeated each first name above the full signature, which the surface screen read as two personas per name (`Stephen Stephen`, `Michael Michael`); the first-name sign-off lines were dropped in `docs.py`, the pack rebuilt (74 of 74 assertions), and only `headline_section_thread.eml` and its byte count in `metadata.json` changed.

**Stage 6, fix cycle 1, 2026-10-10.** Judge pass 1: DETERMINISTIC, FIX_NOW, Gate G `etl_conformance` / `mixed` / no / no (`determinism_check_report.md`). Every load-bearing figure reproduced; no competing answer survived. What changed, finding by finding:

1. Finding 1 (Gate G framing): `submission.md` block 1 opens on the construction (1R successors continue the application, 1N successors are continuing applications dated at their own docketing, parents decided at the refusal, each application ended at its decision notice, the undecided waiting at the extract). The four "Not X" clauses are gone from block 1; their bases sit in steps 2, 4 and 5.
2. Finding 2 (no first action yet): step 4 now states the rule exactly as `golden.py` and the verifier apply it, follow each CX edge unless the successor's first action is credited 1N, and says a successor with no first action at the extract leaves the application waiting. New assertion in `checks.py` and new verifier check: the 4 programme files whose successor has no first action (19-187170, 20-155620, 21-140669, 21-179413) are open in Saravel and waiting under the rule, and a stop at the refusal would decide them. The golden docx sentence "open cases included" is now true under the step as written.
3. Finding 3 (the inference): step 2 carries the forcing argument (a second 1N inside one CX chain would breach "credited once per application", so the 1N successor is a second application and the parent's refusal was never set aside). Nothing pinned in a shipped file.
4. Finding 4 (thin margins): watch only, no re-seed, so no change; the closures are the charter's 30.4375 divisor and the quantile-definition convergence already asserted.
5. Finding 5 (vocabulary): "continuing application" sits beside "first action on the merits credited 1N" in block 1, step 2 and the golden docx note 2.
6. Finding 6 (containers): `writers.py` now strips ReportLab's header banner and trailer comment from both PDFs (binary marker header, cross-reference offsets shifted, file parses strictly) and packages `report_table_notes.docx` as Word 2016 saves it (no thumbnail, customXml or stylesWithEffects; app.xml statistics counted from the text, editing time 52 minutes, AppVersion 16.0000); `golden.py` does the same for the golden docx (editing time 38 minutes).
7. Finding 7 (cross-year regularities): not regenerated (Tried and rejected).
8. Finding 8 (bookkeeping): the Stage 2 Gate G section now quotes the realised 5,921, 34.0, 57,418 and 66,186.

Gates after the fix: generator 75 of 75, two scratch builds byte-identical (17 files, sha256), the task-folder pack identical to the scratch build, verifier 48 of 48 on it, golden twice byte-identical, scrub audit clean on `target/` and `golden/`, `leak.py` REVIEW with the same nine lines answered under Leak review and no LEAK. Only `examiner_production_standard_2019.pdf`, `performance_reporting_charter.pdf`, `report_table_notes.docx`, their byte counts in `metadata.json` and the golden docx changed; no graded figure moved and the svg is byte-identical.

**Stage 3b re-run after fix cycle 1, 2026-10-10.** `golden.py` run twice from the shipped `target/` into scratch: both runs byte-identical to each other and to `golden/` (docx and svg), printed figures unchanged (66,186; 28.9 months, 880 days; lower quartile 19.7; 65.6 per cent within 36 months; 10.6 per cent undecided, none under 1,461 days; all 24 group cells), verifier 48 of 48 on `target/`. `submission.md` holds the five blocks with every figure owed and printed by the golden. Golden-realism read cold (docx one page with its notes resolving to charter section 2, standard EPD/PS/2019 section 2 and the table notes; svg rendered and inspected), no edit. Reduce-house-fixes: scrub audit clean on `target/` and `golden/` (band 2018-01-01 to 2026-11-23), one `submission.md` and one `prompt.md` in the tree, the golden holds exactly the two named files, every citation resolves. `leak.py` REVIEW with the same nine lines (Leak review), `guard.py surface` the same three promoted pairs (Surface review), `guard.py heart` WARN (overuse.org_family, repeat.decision against task125, the older same-puzzle differentiated against task82), card current and `guard.py validate` clean.

## Leak review

leak.py at as-of 2026-11-23: REVIEW (no LEAK), re-run at the stage 3b rebuild after fix cycle 1 with the same nine lines. Each REVIEW line, answered:
- `performance_reporting_charter.pdf` carries 4 of 5 words of the call: it is the pin that defines the headline (median, pendency, filings, fiscal year); a definition, not the figure, and no number of the answer is in it.
- `report_table_notes.docx` carries 3 of 5 words of the call: standing notes defining the tables under the headline; no FY2022 figure.
- `docketing_codebook.md`, 10 stump terms: field glosses (application, ledger, examiner, production are the extract's own nouns); the CX gloss says only that the file passed to a new docket, true on both routes, and nothing names a continuing application on a transferred file.
- `examiner_production_standard_2019.pdf`, 8 stump terms: defines the credit classes, which is the decisive pin by design; it says nothing about dockets, transfers or continuing applications.
- `extract_notes.md`, 10 stump terms: the file list and provenance record; names files, sources and dates, no method.
- `performance_reporting_charter.pdf`, 4 stump terms: the headline pins (application, filing date, still waiting at the extract) and the licensed docket measure; no split.
- `report_table_notes.docx`, 6 stump terms: the group restatement and table rules for the ask layer; nothing on applications versus dockets beyond P1's own label.
- `annual_report_2025_tables_P1_P2.xlsx` names the group codes beside numbers: P1 is docket pendency by docketing year and P2 dockets opened by group; neither ranks or files any FY2022 application figure.
- `art_unit_groups.csv` names the group codes beside numbers: an effective-dated reference table (art unit, group, dates); the numbers are art unit codes and dates, no pendency.

## Surface review

`guard.py surface task126` after the regeneration: personas clean (six, all on the card). Three promoted pairs, none a rename or regeneration finding:
- task125 (back to back, gap population and decision quantity_figure): mechanism axes, not surface; the pattern differs (none with G3 against task125's) and the shared decision type is the WARN answered under Guard.
- task73 (surface 0.143, corpus pct 99): driven by the shared pairing and subdomain on the cards, the flat layout and the docx plus svg deliverable species; zero shared file names, schemas, same-seed tables, entities or prompt wording. task73 is a retired build on a different mechanism (a capped slate under a binding processing allocation); nothing in the generator can be renamed to move it, and the deliverable pair is the prompt's.
- task82 (gap, pattern and decision family): the older same_puzzle signature, cleared by the differentiation line on the card at the draw.

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
- About two in five CX successions as continuing applications (the draw's share): at that share the continuing applications are so many short new applications that rung 4 falls into the docket-grain rungs, within 2 to 4 per cent of rungs 0 and 2 on every parameter set the paper model tried; set at about one in four (27 per cent of FY2022 successions).
- A refused docket closing on the date the request or the continuing application arrives: ending a continuing parent at its docket close instead of its refusal notice then lands 0.4 per cent from the answer, an open fork; every refused docket now closes on its refusal date.
- Shipping the programme agreement's clause barring a continuing application on a programme file, to explain the corpus's blindness: the sentence tells every solver that continuing applications are examined on transferred files, which is the decisive fact; the blindness is constructed and asserted, never explained in the pack.
- A renewal-fee ledger as a distractor (the source note's ask A file), or any file with a term expiry, a publication date or a filing fee per application: each dates a granted continuing application from its own receipt and hands over the split outside the ledger; none ships.
- A first-action pendency cut in the ask layer: "first action on the merits" is the production standard's own wording for the 1N class, so the ask points the solver at the ledger's classes.
- An applications-filed count per group as the third group figure: it makes the unit question salient and invites a count control the pack must not carry; the draw's lower quartile stays.
- The group restatement rule in the performance reporting charter: the charter is on the main call's path, so the ask's organ would sit in a document the main call reads (off path in prose); it lives in the report's table notes.
- A second device-carried ask beside the group table: every candidate either ran on the main call's rows (decision dates, the cohort, decision types) or was a figure for another period or decision (H18); one wide ask on the group path carries the layer.
- The number-first opening drafted at the draw: task123 opened number-first inside the last three builds; situation-first instead.
- No decision within three days of any graded crossing, and no FY2022 decision 1,090 to 1,102 days after filing (stage 2's closure plan): about 40 FY2022 decisions land on every day, so both carve a visible hole in the duration distribution; replaced by the day-880 crossing, quantile-definition convergence and a two-day hole at 1,095 and 1,096 days (Build record, departure 3).
- Every group month cell at least 0.02 months from its rounding edge: 16 integer-day quantiles each have about a 60 per cent chance of clearing it, so no single parameter set does; the day count and the 30.4375 divisor are pinned in the charter instead and every cell is asserted under every quantile definition.
- Pinning in a shipped file that a 1N successor on a CX edge is a new application (judge pass 1, finding 3, to close the Gate C/D exposure on the inference): the sentence states the decisive rung, and the pilot solvers execute every filed rule; the forcing argument lives in submission step 2 only.
- Regenerating to remove the cross-year regularities (judge pass 1, finding 7): unclassified CX successors on FY2022 roots would reopen the waiting-versus-decided fork that departure 6 closes, 1N successors in programme files would break the corpus's blindness to the split, and route-specific successor observables would hand over the split outside the ledger; all three stay as built.
