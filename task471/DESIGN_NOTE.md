# task471 design note: the 2027 small-municipality supplement on the register's adjusted resident population

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task471.json`, architecture v4, registered 2026-10-20T14:00:47Z after a
  pull. Lineage: v1 (the route pitch, Gate F), v2 (the licensure form, Gate G), v3 (the dual-frame well survey, Gate F).
  - Guard: WARN only.
    - ETL in 7 of the last 12: the lane's objective.
    - Gate G method_or_model_selection repeats task474 v3 and runs in 8 of 12: which post-strata carry a register's
      absence process is a model chosen on honest data, not a planted figure.
    - designation_set repeats task474 v3: the decision designates the municipalities that qualify.
  - Differentiation lines against task470, task167, task268, task30, task31, task448, task500, task53, task57, task69
    and task76 (the signature population, E, method_or_model_selection is spent in older builds; each line names how
    this driver differs: an over-count removed at audit rates set by a clock and a migration history).
  - Personas from `guard.py names --geo netherlands --seed 471`: Ilse Spreeuw (head of population statistics at the
    Bureau), Luka Bosman (the audit's methodologist), Kay Wolfswinkel (analyst at the ministry's municipal finance
    directorate). Nobody from v1 to v3 is reused.
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / ETL.
  - The integration: a municipal population register extract, its event history, the national Register Coverage Audit
    with its working extract of the audited persons' register records and histories, the merger crosswalk and the
    ministry's delivery specification, conformed into one adjusted-population file.
  - The deciding quantity: each in-play municipality's adjusted resident population on 1 January 2026, its register
    count less the registered persons estimated, from the audit, not to have been living there; a register's erroneous
    enumerations estimated within post-strata, the task type's own statistical object.
- **World:** an unnamed EU country modelled on the Netherlands. The National Bureau of Statistics (population
  statistics division) delivers adjusted populations to the Ministry of the Interior's municipal finance directorate.
  - Municipal Fund Regulation 2027: the small-municipality supplement goes to municipalities whose adjusted resident
    population on 1 January 2026 is below 5,000.
  - Register Coverage Audit 2026: a simple random sample of persons registered nationally on 1 January 2026, each
    verified in the field (visit and records check) as living, or not, in the registered municipality on that date.
  - The in-play municipalities: every municipality whose register count on 1 January 2026 lies between 4,500 and 6,000
    (two former municipalities merged on 1 January 2026, so the history carries their old codes).
  - Internal moves are registered when a person registers in the new municipality; a departure abroad must be
    reported, and many are not, so the register's over-count is persons who emigrated (or died abroad) unreported.
- **Decision:** which in-play municipalities qualify for the 2027 supplement, and how many. Faces forward: the 2027
  allocation, decided in December 2026 on the adjusted 1 January 2026 population.
- **Shape:** 10, a scorecard: each in-play municipality against the 5,000 line, with the asks per municipality.
- **Strategy:** composition_mix (`own:erroneous-enumerations-post-stratified-by-the-migration-career`), Gate G
  method_or_model_selection, generators G14, G6, G19, calibration form gold_standard_subsample, context artifact
  register.
- **Data-native sentence:** in a population register an internal move is always recorded (the new municipality
  registers the person) and a departure abroad often is not, so the records left behind belong to people early in a
  stay in the country and to people who have come and gone before; the register's own date at the current address is
  reset by every internal move and stops measuring the stay, and only the event history dates the latest arrival.
- **Sources** (one line each; what it teaches, how this build differs):
  - Client pattern census-register 1 (dual-system estimates within post-strata, after erroneous enumerations): the
    erroneous-enumeration rate must be measured within post-strata; here it is the whole estimate and the post-strata
    are the analysis.
  - Register-based population statistics (over-coverage concentrated among recent immigrants, by duration of
    residence and earlier migration): the field's model of silent emigration; here the clock must be rebuilt from the
    event history because the register's address date is reset by internal moves.
  - task473 and task470 in this lane (a rate taken at each unit's own level): here the over-count is removed, not
    completed, and the conditioning properties are a clock and a history, never a recorded level.

## Default path

1. Read `population_register_extract_20260101.txt` (pipe-delimited, its trailer's 126,655 matching the rows): the
   persons registered in the 24 municipalities in play at the start of 1 January 2026, Ravenmeer one municipality with
   its two former municipalities' addresses (Article 14(4)).
2. Took each sampled person's final result from `register_coverage_audit_2026_visits.csv` (the case's last record; 91
   is no contact) and counted results 20, 30 and 40 as not living there (report 3 and 4): 206 of the 12,000 in
   `register_coverage_audit_2026_sample.csv`.
3. Applied report 5 on the respects the sample and the extract both record: each registered person gets the share of
   sampled persons alike in country of birth (born abroad or in the country) and completed years at the current address
   (`ADDRESS_SINCE`: under 1, 1 to 4, 5 to 9, 10 or more), eight cells (born abroad 5.0, 10.1, 5.9 and 1.1 per cent,
   born in the country 0.3 to 0.5).
4. Summed the shares in each municipality, took them from its register count, rounded to the whole person and compared
   with 5,000 (Article 14(1) to (3)): the older immigrant towns Molenrade and Nijdorp come in at 4,967 and 4,968, the
   seasonal-work towns Eekhorst, Haverstede and Koudenbeek stay out at 5,075, 5,069 and 5,067.

Ends on: eight municipalities, Aldewolde, Borgermeer, Bremvoort, Dornhaghe, Hilderloo, Molenrade, Nijdorp and Zandloo.

Golden: nine municipalities, Aldewolde, Borgermeer, Bremvoort, Dornhaghe, Eekhorst, Haverstede, Hilderloo, Koudenbeek
and Zandloo.

## Stump sentence

The default path gives each registered person the audit's absence share by the respects the register extract and the
sample both record, country of birth by years at the current address, and qualifies eight municipalities, Aldewolde,
Borgermeer, Bremvoort, Dornhaghe, Hilderloo, Molenrade, Nijdorp and Zandloo: the older immigrant towns Molenrade and
Nijdorp come in because their long-settled residents moved house recently, and the seasonal-work towns Eekhorst,
Haverstede and Koudenbeek stay out because their residents' address dates are their arrival dates and nothing in the
register record says that four in ten of their migrants had left the country before; taken by the current stay since
the latest settlement from abroad and whether the person left the country before it, both rebuilt from the event
history, the shares qualify the nine.

## Three rules

Task type: census register administrative data quality (the register's over-coverage, its erroneous enumerations measured by a coverage audit and applied to each municipality's register count, conformed into the ministry's adjusted-population delivery), a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each municipality's erroneous enumerations on the population register (registered persons not living there on the reference date), estimated the way register-based statistics estimate over-coverage, a coverage audit's absence rates applied within post-strata (synthetic estimation), where the post-strata are the characteristics that carry a register's absence process, the migration career: the length of the current stay since the latest immigration and an earlier emigration.

Swap: "which of 24 general practices whose patient list held 4,500 to 6,000 patients qualify for a small-practice grant on the list less the patients an audit estimates have left" keeps the arithmetic and loses the structure: here the over-count exists because a departure abroad has to be reported while an internal move is registered by the next municipality, so the records left behind belong to people early in a stay in the country and people who have come and gone before, and the register's address date stops measuring the stay because every internal move resets it; a patient list has no settlement history, no event register and no address clock reset by a move the next practice records.

Layer 1: the register's extract layout (pipe-delimited, CRLF, a trailer with the record count), birth dates with an unknown day or month written 00, annulled events (a settlement entered twice, a departure entered in error), the merger of Ravensloot (0731) and Meerdijk (0744) into Ravenmeer (1987) on 1 January 2026 with every earlier event and address code under the old codes, moves into a municipality recorded only by the receiving municipality, the audit's no-contact attempts (91) before the final result and result 50 (living there on 1 January, left afterwards); each asserted neutral on the call (checks.py L1 and the SF rows).

Layer 2: estimation within post-strata (composition_mix): the audit's absence rate must be applied within the strata that carry the absence process; the fields both record layouts share stand in for the migration career and move the over-count between towns whose migrants differ in their current stay and in earlier departures.

Decisive step: post-stratifying the audit by each person's current stay since the latest settlement from abroad (completed years under 1, 1 to 4, 5 to 9, 10 or more) and whether the person left the country before it, both rebuilt from the register's event history, which brings Eekhorst, Haverstede and Koudenbeek under the line (4,947, 4,946 and 4,947) and keeps Molenrade and Nijdorp over it (5,042 each).

Not semantics: every field, code and definition read correctly (ADDRESS_SINCE the date at the current address, IMM a settlement from abroad, EMI a departure abroad, ANN an event that did not take place, 50 living there) still leaves the easy route post-stratifying on the fields both record layouts carry; no field marks a person's career, and the step is choosing which characteristics carry the absence, tested on the audit itself (log-likelihood -774.4 for the golden's nine cells against -834.4 for the default path's eight).

Not rule application: Article 14 files the population, the reference date, the subtraction, the rounding and the 5,000 line; report 5 files only that each person gets the share found among sampled persons like that person in the respects that bear on it; no filed sentence names a characteristic, so executing every filed rule on the register's own fields files the default eight.

Analyst test: a strong analyst who reads every file and rule correctly and post-stratifies the audit on the characteristics both record layouts carry (country of birth by years at the current address) files eight municipalities, Aldewolde, Borgermeer, Bremvoort, Dornhaghe, Hilderloo, Molenrade, Nijdorp and Zandloo (the default path's Ends on); a logistic fit on every register field files the same eight; only the stay rebuilt from the event history together with an earlier departure files the nine.

Estimand: Article 14(1) to (4) (municipal_fund_regulation_2027_article_14.pdf): the persons registered as residents at the start of 1 January 2026, less those estimated from the Register Coverage Audit 2026 not to have been living there on that date, rounded to the whole person and compared with 5,000, municipalities as constituted on 1 January 2026; report 2 and 5 (register_coverage_audit_2026_report.pdf): the comparison is the audit's sampled persons like each registered person in the respects that bear on living there, every registered person with the same chance of being sampled.

No decoy: nothing is planted to be caught: the register, its history, the audit and the hub's records are what each system writes; no memo, briefing, draft or stakeholder figure argues a method or a list; the 2024 pilot (two other municipalities, another reference date, a sample of addresses) and the waste-levy households (billing, not the register) are declared distractors that rank nothing on the decision.

No certified replay: no published municipal figure, earlier adjusted population or certified list ships to back a method out of; the report's national table (206 of 12,000 by final result) is the audit's own count and ties under every method.

Lesson: in a population register the over-count follows the migration career, a short current stay and an earlier departure, which only the event history dates because the register's own address date resets with every internal move; no build on file post-stratifies a register's erroneous enumerations by a career rebuilt from its event history.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, born abroad by years at the address (eight) | report 5's "respects" sends the solver to the fields both record layouts share: fires | BIRTH_COUNTRY and ADDRESS_SINCE in the sample and the extract: fires | post-stratifying on shared demographics is the reflex: fires | none | none | an eight-cell table: fires | readable |
| R1, one audit rate (six) | report 4 publishes it: fires | none | the national share is the first number to hand: fires | none | none | one ratio: fires | readable |
| R2a, born abroad or foreign nationality (seven) | none | BIRTH_COUNTRY, NATIONALITY: fires | the reflex: fires | none | none | two ratios: fires | readable |
| R2c, the current stay alone (six) | none | the IMM events: fires | duration of residence is a standard covariate: fires | none | none | a five-cell table: fires | readable |
| R2e, an earlier departure alone (seven) | none | the EMI events: fires | none | none | none | a three-cell table: fires | readable |
| R2f, years at the address by an earlier departure (ten) | none | ADDRESS_SINCE and the EMI events: fires | the address clock is the register's own: fires | none | none | a twelve-cell table: fires | readable |
| R2g, age and sex (six) | none | BIRTH_DATE, SEX: fires | age-sex cells are the demographer's reflex: fires | none | none | an eighteen-cell table: fires | readable |
| G (decisive), the current stay since the latest settlement by an earlier departure (nine) | no clause names a characteristic; report 5 says only "the respects that bear on it": silent | no column holds a stay or an earlier departure; both are built from each person's history (the latest IMM, an EMI before it): silent | the reflexes are the shared fields and the published rate; building a migration career is no battery step: silent | the audit scores the candidates only by a fit nobody asks for: silent | every file reconciles; nothing is anomalous: silent | a history walk per person and a nine-cell table: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | qualifies | the rounded adjusted population below 5,000 | the unrounded figure; 5,000 or less | same call: nearest municipality 38.3 from the line (asserted) | Article 14(1) and (3) |
| SF2 | registered at the start of 1 January 2026 | the extract's 126,655 persons | the levy's households; the sample's in-play persons | not a register count | Article 14(2); the extract's trailer |
| SF3 | municipalities in play | the 24 with register counts 4,500 to 6,000 | the bounds exclusive | same 24 (counts 4,561 to 5,944, asserted) | spec 2 |
| SF4 | Ravenmeer | one municipality, its events under 0731 and 0744 included | Ravensloot and Meerdijk separately | not candidates | Article 14(4); spec 2 |
| SF5 | not living there | final results 20, 30 and 40 | result 50 counted as absent | same call (asserted) | report 3, "they count as living there" |
| SF6 | the final result | the case's last record | its first record that is not 91 | same call (asserted) | report 3, "91 ... is not a final result" |
| SF7 | annulled events | removed with their annulment | kept | same call and every adjusted figure (asserted) | layouts, ANN "the annulled event did not take place" |
| SF8 | the sampled persons the shares come from | all 12,000, a simple random sample of the national register | the 186 sampled in the municipalities in play | eight municipalities, Hilderloo out | report 5, "too few in any one municipality"; report 2 |
| SF9 | completed years of the current stay | completed years from the latest settlement to 1 January 2026 | calendar-year difference | same call (asserted) | the bands carry the call; every banding with the earlier departure keeps it |
| SF10 | a settlement from abroad | IMM | VER, a move from another municipality | not a settlement from abroad | layouts, the event codes |
| SF11 | the adjusted population | the golden's whole-person estimate, charted and delivered, not graded | another estimator of the golden's family | same call: cell variants within 4.5 persons, logistic variants within 44 (asserted) | report 5; the prompt grades the call and each municipality's qualification |
| SF12 | birth dates with 00 | day or month unknown | read as invalid | same call: age is no stratum of the golden | layouts, BIRTH_DATE |
| SF13 | departures abroad in 2025 | departure date in 2025, sent in 2025 the country's time, accepted, not annulled; a person who left twice counts twice | the hub's UTC year; every message; annulled kept; persons | other counts (ask A) | spec 3 and DEPARTURES_ABROAD_2025; layouts (SENT_AT, the acknowledgements, ANN) |
| SF14 | deaths in 2025 | date of death in 2025, sent in 2025 the country's time, accepted, not annulled, registered there when they died | the hub's UTC year; every message; former residents; annulled kept | other counts (ask B) | spec 3 and DEATHS_2025; layouts; the non-resident records' DEPARTURE_DATE |
| SF15 | a removal after an address investigation | VOW, not a departure | counted with the departures | other counts (ask A) | spec, DEPARTURES_ABROAD_2025 |

## Ladder

- **R0, the default path: born abroad by years at the address (eight).** Aldewolde, Borgermeer, Bremvoort, Dornhaghe,
  Hilderloo, Molenrade, Nijdorp and Zandloo; Molenrade 4,966.9 and Nijdorp 4,967.9 in, Eekhorst 5,074.7, Haverstede
  5,069.1 and Koudenbeek 5,066.5 out. A logistic fit on every register field (country of birth, nationality, address
  band, age, sex, with or without interactions) files the same eight. Dies to the audit: log-likelihood -834.4 against
  -774.4 for the golden's cells, and within the sampled persons born abroad with one to four years at the address those
  who left the country before are absent at 26.9 per cent against 11.0 for the rest.
- **R1, one audit rate (six).** 1.72 per cent for everyone; Dalmeer in at 4,981.0, all four decisive towns out. Dies
  to the audit's own spread (0.28 per cent for those never settled from abroad, 26.9 for a 1-to-4-year stay after an
  earlier departure).
- **R2a, born abroad or foreign nationality (seven).** Molenrade and Nijdorp in, Eekhorst, Haverstede, Hilderloo and
  Koudenbeek out.
- **R2c, the current stay alone (six).** Hilderloo in at 4,928.3; the seasonal-work towns out at 5,014 to 5,021. Dies
  to the audit: within every stay band an earlier departure doubles or more the absence (log-likelihood -787.6).
- **R2e, an earlier departure alone (seven).** Molenrade and Nijdorp in, the seasonal-work towns and Hilderloo out
  (-826.7).
- **R2f, years at the address by an earlier departure (ten).** Builds the departure from the history but keeps the
  register's clock: Molenrade and Nijdorp in at 4,979 and 4,982, Hilderloo out at 5,003.5 (-792.0).
- **R2g, age and sex (six).** Dalmeer in, all four decisive towns out (-1,004.2).
- **G, the decisive move (nine).** The current stay since the latest settlement by an earlier departure, nine cells:
  Eekhorst 4,946.5, Haverstede 4,946.5, Koudenbeek 4,946.6 and Hilderloo 4,958.6 in; Dalmeer 5,038.3, Molenrade 5,041.6
  and Nijdorp 5,042.0 out.
- **The golden's family converges (asserted).** Single years, the bands crossed with country of birth, sex, address,
  nationality, age or the first settlement, the first settlement by an earlier departure, and every additive or
  saturated logit with the stay and the earlier departure (log-likelihood -772.6 to -780.8) file the nine; of the 1,024
  contiguous partitions of the stay with the earlier departure, 1,013 file the nine, and the 11 others (ten lumping five
  to nine years with ten or more, one the coarse 0-1, 2-9, 10+) all fit 15 or more below the golden's cells.
- **Margins:** the nearest qualifying municipality is Hilderloo, 41.4 under the line, the nearest left out Dalmeer, 38.3
  over; every wrong rung's set differs from the nine in two or more municipalities.
- **Position, separation and dominance:** every rung names its own set (eight, six, seven, six, seven, ten, six against
  nine); the corrections move towns both ways (the stay alone brings Hilderloo in and the older immigrant towns out,
  the earlier departure alone brings the older immigrant towns in), and only the stay with the earlier departure brings
  the three seasonal-work towns in while keeping Molenrade, Nijdorp and Dalmeer out.
- **Worth on the graded quantities:** the call (8) and the 24 qualifications (1.25 each): R0 keeps 19, R1 20, R2a 19,
  R2c 21, R2e 19, R2f 21 and R2g 20 of the 24; none lands the call (generator/ceiling.py).
- **Grid:** the Layer 1 items mishandled one at a time (annulments kept, the first result, result 50 as absent, the
  former codes left unmapped for the call's features, partial birth dates) leave the call in place (checks.py).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the persons registered in the 24 municipalities in play at the start of 1 January 2026 (Article 14(2), the extract); the audit's sample is drawn from the national register (report 2) |
| 2 | Unit of account | the municipality as constituted on 1 January 2026 (Article 14(4)); persons |
| 3 | Attribution window | the reference date 1 January 2026; the audit's results say where each person lived that day (report 3) |
| 4 | As-of dating | the extract as the register stood at the start of 1 January 2026 (extracted 5 January); the sample as it stood that day |
| 5 | Version basis | one version of each file; annulled events removed (SF7) |
| 6 | Denominator | each person's stratum share from the whole national sample (report 5, SF8); the decisive step (HOW), the golden's family agreeing |
| 7 | Weighting | none: a simple random sample with equal chances (report 2); each registered person counts once |
| 8 | Window length | one reference date |
| 9 | Boundary inclusivity | below 5,000 on the rounded figure (SF1); nothing within 38 persons of the line |
| 10 | Rounding path | shares summed unrounded, the adjusted population rounded to the whole person, then compared (Article 14(3)) |
| 11 | Tie-break | none: each municipality on its own figure |
| 12 | Maturity and censoring | the fieldwork closed on 29 May 2026 with every case resolved (report 3); the asks' year is closed in the hub's 2025 log |
| 13 | Order of operations | register count, each person's stay and earlier departure from the history, the strata's rates, expected persons not living there, subtraction, rounding, comparison |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | no repeated person key in the extract, the sample or the history (asserted); a settlement entered twice is annulled (Layer 1) |
| 16 | Identity normalisation | the person key is the same in every extract (layouts); Ravenmeer's former codes mapped to 1987 (SF4) |
| 17 | Netting | the estimate of persons not living there is taken from the register count (Article 14(2)); result 50 counts as living there (SF5) |
| 18 | Dimensional units | persons; completed years to 1 January 2026 (SF9); the hub's UTC stamps read in the country's time for the asks (SF13, SF14) |
| 19 | Code and status semantics | IMM a settlement from abroad, EMI a departure abroad, ANN an event that did not take place, OVL a death, 20/30/40 not living there, 91 no final result; never the stump |
| 20 | Integerisation | whole persons (Article 14(3)); every ask count a whole number |
| 21 | Clause scope | Article 14 for the 2027 supplement; report 5 for municipal figures; spec 3 for the delivery file and the asks' columns |
| 22 | Forward window contents | the 2027 supplement decided in December 2026 on the adjusted population of 1 January 2026: a closed reference date for a forward allocation |

## Literal reader

Executed word for word, Article 14 and the report fix the population (persons registered at the start of 1 January
2026 in each municipality as constituted that day), the outcome (not living there on that date: results 20, 30 and 40;
50 living there), the comparison pool (the audit's 12,000 sampled persons, a simple random sample of the national
register), the subtraction, the rounding and the line, and leave one thing open: which respects "bear on" living there
(report 5). The candidates are the fields both record layouts share (R0, R2a, R2g), a settlement clock alone (R2c), an
earlier departure alone (R2e), the address clock with the earlier departure (R2f), and a settlement clock with the
earlier departure (G). The audit separates them on its own records: the golden's cells fit at -774.4 against -787.6 to
-1,041.6 for the rungs, and once the stay and the earlier departure are in, no other field adds anything (every cross
or logit with country of birth, nationality, address, age, sex or the first settlement keeps the nine). Every member of
the golden's family files the nine; every write-up step names the file and the rule it executes.

## Oracles

None that ties only under the golden. The report's national table (206 of 12,000 by final result) ties under every
method; the 2024 pilot (two municipalities not in play, 1 January 2024, a sample of addresses) ranks nothing in play;
the waste-levy households are billing counts, not the register, and rank nothing on the decision. Both are declared
distractors in metadata.json. The hub's acknowledgements tie each message to its answer under every reading of the
asks.

## Ask sheet

- **Ask A, each municipality's departures abroad in 2025 (24 figures).** H18 home: the register's 2025 population
  account the ministry reviews beside the supplement (spec 1), a measure every municipality carries that the call does
  not turn on, on rows outside the main population (the hub's 2025 log). Path: `deregistration_messages_2025.csv`
  (SENT_AT, SENDER_MUN, PERSON_KEY, MESSAGE_TYPE, EVENT_DATE), `hub_acknowledgements_2025.csv` (MESSAGE_ID, RESULT),
  `population_register_events_extract.csv` (EVENT, EVENT_DATE, ANNULS_SEQ), the spec (3, DEPARTURES_ABROAD_2025), the
  record layouts (SENT_AT in UTC, the acknowledgements, ANN) and the codes workbook (the merger): six files, thirteen
  columns. Primary device: D2 with D9, the record is the register's current state. In every municipality one or two
  departures (33 in all) were recorded from an accepted message and annulled 18 to 60 days later as entered in error;
  the hub's log and acknowledgement show an ordinary accepted departure, and only the person's history (an EMI and an
  ANN voiding it, the person still on the 1 January 2026 register) shows it did not take place. Two-sided: in every
  municipality a resident left in 2025 and settled again within the year (an EMI then an IMM), a departure that
  stands, so dropping every departure of a person on the 1 January 2026 register is wrong the other way. No sweep sees
  it: every message is valid, accepted, unique and in scope. Hazards: the hub's log runs in UTC and each night's
  messages leave shortly after midnight in the country's time, so the New Year's night batch (two to four departures
  per municipality) is logged on 31 December and sent in 2026 (spec 3); rejected messages corrected and sent again;
  departures of persons already removed or dead, rejected and never sent again; December 2024 departures sent in
  January 2025; persons who left twice (counted twice); removals after an address investigation (not departures);
  Ravenmeer's messages under 0731 and 0744. Stops (asserted, generator/ceiling.py and checks.py): the annulled
  departures counted misses all 24; every departure of a registered person dropped misses all 24; the UTC year misses
  all 24; the golden equals the generator's truth.
- **Ask B, each municipality's deaths in 2025 (24 figures).** Same home and use. Path: the hub's log (OVL), the
  acknowledgements, the events extract (OVL, ANN), `non_resident_records_extract.csv` (PERSON_KEY, DEPARTURE_DATE), the
  spec (DEATHS_2025) and the layouts: five files, eleven columns. Primary device: D2 with D9 on another record, a death
  recorded for the wrong person (a namesake at the same address, a hospital's notice matched to the wrong record) and
  annulled within weeks: one or two in every municipality (29 in all), accepted in the hub's log, the person alive on
  the 1 January 2026 register with an OVL and an ANN voiding it. Hazards: the New Year's night batch (one or two of the
  holiday deaths per municipality, logged on 31 December, sent in 2026); former residents abroad whose death the
  municipality recorded (3 to 14 per municipality; their registration ended before the death); December 2024 deaths
  registered in January 2025; rejected and resent deaths; residents who died abroad (counted); Ravenmeer's codes.
  Stops (asserted): the annulled deaths counted misses all 24; the UTC year misses all 24; former residents counted
  misses all 24.
- **The construction layer:** the nine, the 24 qualifications and the chart; the cracker has them.
- **Main population zero-counts (asserted):** every ask device sits in the hub's log, its acknowledgements and the
  non-resident records, or (the annulled departures and deaths) after each person's latest settlement in the history,
  so the stay and the earlier departure of every registered and sampled person, the call and every adjusted figure are
  the same with and without them.
- **Hazard table (asserted):** the annulled departures move all 24 departures; the returners all 24; the year-end batch
  all 24 departures and all 24 deaths; the annulled deaths all 24 deaths; the former residents' deaths all 24; none moves
  the call.
- **Referee:** none; no total in the asks' files ties under one handling only.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each municipality's departures abroad in 2025 | accepted EMI messages with a 2025 departure date sent in 2025 in the country's time, Ravenmeer's codes mapped, persons who left twice counted twice, removals out; the annulled departures counted, since no rule or sweep sends it to the history | miss |
| B, each municipality's deaths in 2025 | accepted OVL messages with a 2025 date sent in 2025 in the country's time, former residents whose registration ended before the death out; the annulled deaths counted | miss |

- Mirror leakage: 0.0 per cent of ask weight (every rung reads the asks the cracker's way and misses all 48:
  generator/ceiling.py).
- Pair ceiling: 39.1 (weights 38 / 7 / 55: the call 8, each of the 24 qualifications 1.25, each of the 48 ask figures
  55/48; the cracker keeps the main block and instructions, 45.0; the best mirror, R2c or R2f, keeps 21 of the 24
  qualifications, 33.25; average 39.1), rerun from the generated rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own moves, a round-trip itinerary fare read as a one-way fare and the New York
  airports left as three markets: data semantics and a market definition (the estimand's unit), so neither may decide;
  kept as Layer 1 and as ask devices.
- 2026-10-18, at the draw: a windshield census (cards put on every car parked in the lots at sweep times), whose cards
  over-represent long stays in proportion to their length: population_selection, banned against task245 at the draw,
  and the label is not moved to pass the guard; replaced by the entry-plaza handout, a different mechanism (replies
  censored by the collection close, which thins the long stays instead of inflating them).
- 2026-10-18, at the draw: the fare premium over a log-log fare-distance benchmark, decided by retransformation bias:
  generic econometrics, and a clinic's charges against a severity curve read the same (swap test fails).
- 2026-10-18, at the draw: the three markets with the highest premium in thin ticket-sample cells, decided by
  shrinkage (the winner's curse): the shrinkage method is not forced by anything filed, a coin flip for determinism.
- 2026-10-18, at the draw: leakage read from an agency ticket dataset whose capture depends on the sales channel,
  measured where the ticket sample sees everything: the same lesson as task448 and task470 (capture by unit measured
  on the overlap).
- 2026-10-18, at the draw: a departure-lounge survey with a fixed quota of interviews per flight (unequal inclusion):
  a ratio within each destination sidesteps it, and by house precedent (task452) a design-weight stump is
  population_selection, banned at the draw.
- 2026-10-18, at the draw: capacity-censored (spilled) demand on full flights to the hubs: the demand turned away is
  model-dependent and every demand model is a fork.
- 2026-10-18, at the draw: the share of one-way tickets that are residents' trips (a one-way ticket's origin is not
  its traveller's home): turns on reading what the ticket origin field means, data semantics.
- 2026-10-18, at the draw: business travel by market from the fare-class proxy corrected for its false positives
  (Rogan-Gladen): the lesson task456 teaches (an imperfect record's false positives subtracted, not only its misses).
- 2026-10-18, at the build: the party verbatim beside the coded party in the cards file, with a filed rule sending the
  analyst to the verbatim for parties of nine or more: the rule pointed every careful solver at the verbatim column,
  where the sums sit in plain view; the verbatims moved to their own file and the cap dropped.
- 2026-10-18, at the build: home ZIPs keyed with a plus-four on 16 per cent of cards: matched as keyed they moved every
  trips figure out of its hundred, so a Layer 1 item carried figure difficulty; cut to a realistic 0.3 per cent and
  asserted neutral, with the two-county ZIP made a small rural office and the repeated batch chosen so its second copy
  moves no figure out of its hundred.
- 2026-10-18, at the build: passengers on the default path's weights ranked Washington, Phoenix and Tampa, the golden's
  three, so ranking on passengers was a shortcut to the call; the winter markets' parties cut to couples and singles
  (1.65 to 1.75) and Myrtle Beach's summer family trips raised to 3,000, so passengers on any weighting carry Myrtle
  Beach.
- 2026-10-18, at the build: the first realisation (seed 471) put New York within 1.12 of the third market once the party
  draw moved onto each card; New York and Dallas set lower in the world and a seed search run over 60 worlds; seed 504.
- 2026-10-18, at stage 4: seed 504's world, where New York led Dallas for the first market left out by 2 per cent and
  a reweighting or a dropped batch could swap them (reader round 1); the handout coverage reworked plaza by plaza and
  day by day with lot choice independent of the stay, and a 120-world search run with the fourth against the fifth at
  1.07 or more; one world passed, seed 512.
- 2026-10-18, at stage 4: the passengers device cut one way (a sum written on the card coded as its first number):
  reader round 2 read Q4 in the verbatims against `party` and recoded every party, the sums added.
- 2026-10-18, at stage 4: the same device cut both ways (the parties written with who they cover coded right, so adding
  every number written counts them twice): reader round 3 recoded every party right. Both cuts are mirror devices: the
  verbatims are documented beside the coded column (methods report 4.2), so reconciling them is the cracker's reflex,
  and no reading of Q4 the frozen documents leave open is both determinate and missed by a careful parser.
- 2026-10-19, re-root tried on paper: the same parking survey with the third pick held unless its lead over the first
  market left out clears twice its design-based standard error (cards clustered by handout day, weighted by the return
  window). Measured on the v1 pack it cannot bind: 73,909 returned cards put Phoenix, Tampa and Washington each 3.5
  standard errors clear of New York on the weighted card-level variance and 2.3 to 3.4 clustered by day; binding it
  would need a tenfold smaller sample and same-day group travel, a planted structure, and the clustering unit itself
  is arguable when the waves are consecutive days. Dropped before any data was cut.
- 2026-10-20, re-root: architecture 1 (the parking card survey, replies censored by the collection close) spent at
  Gate F, every reader landing the call, with its ask device a mirror device; by the author's rule (no retirement)
  architecture 2 is a fresh world in the least-drawn ETL task type, its decisive step one the record does not display.
- 2026-10-20, at the draw: repeat candidates who saw the anchor items on an earlier attempt, left in the equating
  sample: an anchor-contamination screen beside task450's, and the sample definition has to be filed anyway (a
  convention), which files the step; kept only as the filed sample (first attempts), with no exposure in the data.
- 2026-10-20, at the draw: Tucker against Levine under a large cohort difference (the anchor's reliability): the two
  differ by less than their sampling error at the cut and nothing a pack can carry forces one, a fork.
- 2026-10-20, at the draw: 2025 responses re-scored as a labelled trend sample: the label names the drift check, so
  the organ announces the step; replaced by the contractor's validity papers, which its QC summary reports only as
  agreement rates.
- 2026-10-20, at the draw (prototype 1): an anchor of 15 multiple-choice items and two of the three written
  assignments, heavier in written work than the test: the golden's methods split (Tucker 56 against chained
  equipercentile 57) and missed the generating truth; the anchor made proportional (20 items and one assignment, 44
  per cent written by points, as the test is).
- 2026-10-20, at the draw: filing the program's equating method (Tucker) in the 2025 technical report to close the
  equipercentile spread: its literal execution on the anchor as scored is the default path's cut, an official decoy;
  the method stays unfiled and the world is tuned so that Tucker, Levine and chained linear (each at three synthetic
  weights) and chained equipercentile agree on one cut with margin.
- 2026-10-20, stage 3: WA2's validity papers scored by the 2025 leaders' consensus (an audit set): `heart` blocked
  ban.calibration and ban.artifact against task473 once task249 was marked spent; redrawn as June 2025 responses
  carrying the score both of their 2025 reads gave, the two scoring regimes' overlap on the same responses and the
  operational metric the 2025 anchor scores are on (validity sample drawn on its own stream so the shift sits mid-bin:
  0.98 anchor points, raw 49 with 0.38 and 0.37 of margin, every rung and set unchanged).
- 2026-10-20, stage 4: architecture 2 itself, the rater-severity shift on the anchor's written assignment measured on
  the validity papers and taken out before the link. The judge (v2r1) found it DETERMINISTIC on the main call, but its
  Gate G disposition was SEND_BACK (planted_defect_flip, surface_read_rejection, sole_data_defect yes): on consistent
  scoring the anchor as scored is right and the task collapses, so the stump is catching that the as-scored anchor
  misleads. Gate H passed only as analytical (borderline planted). Both scored readers missed the call on the drop-WA2
  rung and all 32 ask figures, but a measurement bias in recorded values is a defect to catch, not an analysis on
  honest numbers. Spent; architecture 3 is a fresh draw on honest data.
- 2026-10-20, at the architecture 3 draw: a joint replacement registry whose earlier hips were back-loaded on each
  hospital's joining only if still in place, read by delayed entry. task265 already spends exactly that insight, so it
  was dropped before registering.
- 2026-10-20, at the v3 build: the parcel list alone (and the parcel-drawn share scaled to the wells on the lists)
  named the golden six by coincidence, because the parcel-only wells carried nearly every exceedance; Alderwick placed
  as a county whose permit-only wells run high (its parcel list alone gives 79), so no single list lands the six.
- 2026-10-20, at the v3 build: each county's estimate as a graded figure: the design-based estimators that all name
  the six differ by up to 59 wells in one county (Dunmere 164 to 223), so no figure is determinate; the estimate is
  charted and the graded grid is each county's verdict and its wells on the lists.
- 2026-10-20, at the v3 build: the retest ask's routing on one border town per county could not move every county's
  figures (several counties had no border retests); each county's border town drawn from its two smaller towns, and the
  search also kept the portal-only path off every figure, so the mirror keeps none of the 32.
- 2026-10-20, at the v3 build: results printed at 10.00, or Kinsale results between 44.0 and 44.27 mg/L NO3, would
  split the standard's "more than 10" from "10 or more" and the design report's factor from the fact sheet's; every
  result within 0.1 of the standard moved clear of it on its own side (SF1, SF12).
- 2026-10-20, stage 4: architecture 3 itself, the county estimate over two overlapping lists sampled separately,
  each tested well counted at one over its chance of selection from either list. The judge (run v3r1) found it
  DETERMINISTIC and APPROVE (Gate G method_or_model_selection, analytical_non_defect; Gate H analytical), but both
  scored readers landed the call and all 32 ask figures: reader A by the inclusion probabilities, reader B by the
  post-stratified estimator. The design report must describe the two lists and their separate draws for the estimate
  to be determinate, and once described the dual-frame estimator is executed as a work order; the routing county on
  the retest requests fell to a consistency check of the request's county against the first kit's. Spent on Gate F.
- 2026-10-20, at the v4 draw: a coarse privacy-preserving linkage key whose chance agreements inflate each county's
  linked count, corrected by the expected chance matches: the lesson task468 v4 teaches (false links for common
  identifiers), shipped in this lane today.
- 2026-10-20, at the v4 draw: the dual-frame world with a nonresponse weighting class added: stacks a second step on a
  rung both readers already executed, and the weighting class rests on a missing-at-random assumption a judge reads as
  open.
- 2026-10-20, at the v4 draw: an annual quantity read from a seasonal record: an annual estimand announces the season,
  and the driver is task476's (onset season against inspection timing).
- 2026-10-20, at the v4 draw: persons registered at crowded addresses as a second absence stratum: for the audited
  persons the address context would have to ship as a column or an address-member table, either of which displays it.
- 2026-10-20, at the v4 draw: school proficiency rates from point-estimate classification against expected counts
  (plausible values): the estimand would have to name an expected count, which files the method.
- 2026-10-20, at the v4 draw: chained volume components summed: reads as a unit's semantics (chained dollars are not
  additive), so the decisive step would be data semantics.
- 2026-10-20, at the v4 draw: the register's registration lag completed by its delay distribution: maturity_censoring,
  banned at the draw against task250.
- 2026-10-20, at the v4 build: the asks' first devices (rejected messages sent again, late reports, former residents'
  deaths): every one is executed by a careful solver who joins the hub's acknowledgements and applies the filed
  residency condition, so the cracker landed both asks; re-sited onto departures and deaths the register annulled as
  entered in error, found only in the persons' own histories.
- 2026-10-20, at the v4 build: the year-end batch as the deaths' primary: determinate only with a filed local-time
  convention, which a careful solver executes; kept as a hazard shared by both asks.
- 2026-10-20, at the v4 build: persons removed after an address investigation who had died before it (registered when
  they died), to make residency two-sided: with the year-end batch and the annulled deaths a three-error reading
  cancelled back to the golden in 21 of 24 municipalities; removed, residency now one-sided.
- 2026-10-20, at the v4 build: a third ask, former residents living abroad on 1 January 2026, with non-resident records
  never closed for persons who came back: determinate only with a filed re-registration condition, which hands the
  device over; dropped.
- 2026-10-20, at the v4 build: the national circular migrants' gaps of one to six years: the seasonal-work towns'
  long-gap migrants then sat in a seven-person cell of stay by earlier departure by first settlement, and that cross
  filed six with a municipality 0.1 from the line; national gaps widened to 1 to 14 years, every cross now files nine.
