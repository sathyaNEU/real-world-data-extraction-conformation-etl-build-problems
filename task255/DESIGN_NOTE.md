# task255 design note

Architecture 3, drawn 2026-11-01 at the re-root after architecture 2 (a metro concession's Tier G reach) was spent at
its re-judge. Architectures 2 and 1 are kept below as `## Architecture 2 record` and `## Architecture 1 record`; both
worlds are closed.

## Draw

- **Card:** `cards/task255.json`, architecture v3, registered 2026-11-01 (guard check PASS; nearest cards task118,
  task198 and task270, each differentiated on the card). Pharmacology, Pharmacoepidemiology & Safety, task type
  medication-adherence-persistence, objective Descriptive & Distribution Analysis (the number's lane is kept; the
  marketing descriptive ground of architecture 2 is spent for this slot). Shape 10, a scorecard: every practice's
  persistence set against the programme line. Decision designation_set; gap objective and time; generators G1, G12
  and G2; Gate G method_or_model_selection; stakeholder the head of the regional medicines unit.
- **World:** Region Lindholt, a fictional Danish region: sixteen general practices in five towns, eight pharmacies that
  ran a 2026 pilot of pharmacist follow-up conversations, and the medicines unit, which holds the region's extract of
  statin dispensings (January 2024 to December 2026) from the national register. The practice planning committee
  adopted the 2027 statin follow-up programme on 26 January 2027. Personas from `guard.py names --geo DK --seed 255`:
  Hanne Overgaard (medicines unit, the golden's author), Laust Jessen (the ATC/DDD table), Britta Winther (the pilot's
  conversation log), Ester Poulsen (finance, the quarterly statements). As-of date of the fiction: Friday 12 February
  2027.
- **The call:** whether any practice joins the 2027 programme, and which. Golden: yes, six practices (041219
  Lægehuset Østergade 48, 041236 Klinikken Bredgade 53, 041248 Lægerne Skovvej 48, 041275 Lægeklinikken Kirkebakken
  48, 041307 Lægerne Møllevej 54, 041322 Lægerne Stationsvej 53 per cent); every other practice 65 per cent or more.
  The call faces forward (2027 membership) and is measured on a closed window the programme itself fixes (2.1); the
  descriptive tag stands because the deciding quantity is a distribution (the share of a practice's new users still
  supplied at a horizon), not a predicted value.
- **Shape arithmetic:** sixteen practices times persistence (16), the set and the verdict (2), the nearest practice
  above the line (1), the chart with its line (2), what each pilot pharmacy is entitled to for each quarter's
  conversations (32), each practice's continuing users of 2026 (16): 69 gradable figures, 48 of them asks.
- **Data-native sentence:** a Danish dispensing register records the packs, the product number and the date of each
  dispensing but no dose, so how long a dispensing lasts is not in the record; the field times it at one WHO defined
  daily dose a day, and nearly half of this region's new statin users with a refill take something else (two defined
  doses in one tablet, two tablets a day, half a tablet, a half-strength tablet), which only the rhythm of each
  patient's own dispensings shows.

## Survivor anatomy

- **Actor:** the deciding property, each patient's daily dose, has no column in any file: the register row holds a
  pseudonym, a date, a product number, packs, a prescriber and a pharmacy, the product list holds strength and pack
  size, and the dose is a relation between a patient's tablets and the days between that patient's own dispensings.
- **Link:** the signal is read through a comparison no key offers: each patient's tablets set against the intervals
  between their own successive dispensings, a within-patient rhythm the field's join (product number to ATC code to
  defined daily dose) never asks for.
- **Reflex:** the field's method for a register without doses, timing each dispensing at one WHO defined daily dose a
  day (atc_ddd_2026.xlsx is the region's copy of the index), sits at rung 1 and files 041236 and 041263 (Klinikken
  Bredgade and Lægerne i Vejlby), with Lægehuset Østergade at 67.9 per cent.
- **Back-test:** the easy route validates: on the commonest products (atorvastatin 20 mg, rosuvastatin 10 mg) a tablet
  is one defined daily dose and the typical patient refills a 98-tablet pack about every 94 days, so the DDD timing
  checks out on the bulk of the register; the region-wide share it gives (about 65 per cent) sits beside the national
  report's 64.
- **Second use:** every file the decisive step reads is in the pack for its own reason: the extract is the medicines
  unit's own record of dispensings, the product list maps product numbers to strength and pack size, and the practice
  register maps prescribers to practices; the step reads nothing that ships for it.
- **Shock:** the movement the step recovers reads as ordinary prescribing (high-intensity atorvastatin and two-tablet
  regimens at some practices, tablet splitting and half-strength tablets at others), not as anything anomalous; sorted
  by the DDD-timed share, the one-tablet-a-day share, cohort size or the patient survey's score, the golden set is not
  an interval of any shipped statistic.
- **Pins:** the WHAT is filed in programme 2.1, 3.1 and 3.2 in the region's own genre (the window, the lookback, the
  practice of the first prescription, the 365 days, the 30-day run, tablets in hand used first, the dose the patient
  takes); no filed sentence names a defined daily dose, tablets a day, a refill interval or a method, and deleting any
  filed sentence only unfixes the population, the window or the gap, never the step.

## Three rules

- **Task type:** medication-adherence-persistence in pharmacology-pharmacoepidemiology-safety, which serves
  Descriptive & Distribution Analysis: the distribution of new users' continuation on treatment, read as each
  practice's share still supplied at a fixed horizon.
- **Domain test:** the call turns on each practice's twelve-month persistence among new statin users, the
  pharmacoepidemiology measure built patient by patient from dispensings turned into exposure periods (supply carried
  forward, a permissible gap) and read at a fixed horizon; with another field's nouns there is no dispensing, no tablet
  supply, no daily dose and no permissible gap.
- **Swap:** "which schools join a reading programme, set by the share of new pupils still borrowing books a year on":
  no tablets, no strength, no defined daily dose and no supply to carry forward at a rate the record does not hold.
- **Layer 1:** (1) parallel-imported and generic products under their own names and product numbers beside the
  originals (the national product list); (2) the extract stitched from the register's old system, dates day-month-year
  to June 2024, ISO after (the medicines unit's extract); (3) hospital departments in the prescriber column beside the
  practices, on long-standing users' dispensings (the register); (4) the pilot's conversation log with cancellations
  entered weeks later, the last by 20 January 2027 (the pharmacies); (5) quarterly statements drawn on each quarter's
  last day (finance); (6) people whose personal number was replaced in 2026 under a second pseudonym from the change,
  the CPR person table carrying the earlier number (the register's pseudonymisation of the personal number); (7) list
  sizes reported per quarter (practice planning). Nothing is placed to be caught;
  items 1 to 3 and 7 move nothing on the call (asserted R2.1 to R2.3 and R2.7), items 4 to 6 sit only in the asks'
  rows (R2.4 to R2.6).
- **Layer 2:** estimation under a violated precondition: turning dispensings into exposure periods presumes a known
  daily dose; the register holds none and the defined daily dose the field substitutes is not what these patients
  take, so each patient's dose has to be estimated from their own record before any period is built.
- **Decisive step:** reading each new user's daily dose off their own dispensings (the tablets handed out before the
  last dispensing over the days from the first to the last, or the median of their refill rates) instead of assuming
  one defined daily dose or one tablet a day, and timing every dispensing at it.
- **Not semantics:** every field, code and unit read correctly (product numbers to strength and pack size, both date
  formats, the prescribers, the window, the lookback, the 30-day run) still leaves the dose open, because no field,
  code or definition holds a dose; the deciding fact is a rate in each patient's own dates.
- **Not rule application:** programme 3.2 says the tablets last "at the daily dose they take" and leaves how to know
  it to the analyst. Enumerated family (every construction a competent analyst reaches for): one tablet a day (nine
  practices: 041219, 041224, 041236, 041248, 041251, 041275, 041282, 041322, 041334), one defined daily dose a day (two:
  041236 and 041263, Kirkebakken at exactly 60.0), each product's typical rate across all its patients (the same
  nine), each patient's own rate (six): Østergade spans 45.2 to 67.9 and the family files three distinct sets. Standing
  family (what the record leaves defensible once the step is taken: the overall rate, the median refill rate, the last
  three refills, the first year only, the rate snapped to half, one, two or four tablets): the same status for all
  1,485 new users, asserted (SF7). The defined daily dose is ruled out by no filed sentence, only by the record, and
  loudly: a patient on 98 tablets of atorvastatin 40 mg who refills every 94 days takes one tablet a day, not two
  days per tablet.
- **Analyst test:** a strong analyst who cleans the extract, applies every filed rule (window, lookback, 30-day run,
  tablets carried forward) and times each dispensing at one WHO defined daily dose a day, the field's standard when the
  register holds no dose, files 041236 and 041263 (Klinikken Bredgade and Lægerne i Vejlby); only reading each
  patient's dose off their own refills files the six, Østergade at 47.6 instead of 67.9.
- **Estimand:** statin_followup_programme_2027.pdf 2.1 and 3.1 to 3.2: a practice joins in 2027 when fewer than 60 per
  cent of its new statin users of the second half of 2025 (first statin dispensing, ATC C10AA, from 1 July to 31
  December 2025 with none in the 365 days before, at the practice that prescribed it) were persistent for twelve
  months (never more than 30 days in a row without tablets in the 365 days from the first dispensing, each
  dispensing's tablets lasting at the daily dose the patient takes, tablets in hand used first).
- **No decoy:** nothing is planted to be caught: no memo, draft, briefing, stakeholder figure, copied block or hidden
  rule ships; the ATC/DDD table is the WHO index a register extract comes with (a declared distractor), and the
  published regional use in DDD per 1,000 a day, the patient survey and the national report answer other questions.
- **No certified replay:** no shipped figure certifies a dose, a status or a practice's persistence; the national
  report's 64 per cent rests on another definition (a new pack within 180 days) and another population, so the method
  is not recovered by reproducing a published number.
- **Lesson:** an exposure period is only as good as the dose it is timed at; where the register holds no dose, each
  patient's own dispensing rhythm is the record of it, and a defined daily dose is a unit for counting consumption,
  not a patient's dose. No build on file times a supply at a rate read from each member's own handout rhythm.

## Default path

1. Take the new statin users of 1 July to 31 December 2025 (first dispensing in the window, none in the 365 days
   before) by the practice that prescribed the first dispensing: 1,485 patients.
2. Turn each dispensing into days of supply the field's way when the register holds no dose: tablets times strength
   over the WHO defined daily dose of the substance (atc_ddd_2026.xlsx), one defined daily dose a day.
3. Lay the supplies end to end from the first dispensing, tablets in hand used first, and call a patient persistent
   when no run of more than 30 days without supply falls in the 365 days.
4. Take each practice's share and set it against 60 per cent.

Ends on: two practices join, 041236 and 041263 (Klinikken Bredgade and Lægerne i Vejlby).
Golden: six practices join, 041219, 041248, 041275, 041307, 041322 and 041236.

## Stump sentence

The default path times every dispensing at one WHO defined daily dose a day and files 041236 and 041263 (Klinikken
Bredgade and Lægerne i Vejlby); at Østergade, Skovvej, Kirkebakken, Møllevej and Stationsvej many new users take two
defined doses a day in one tablet or two, so the DDD credits each of their tablets with two days, and at Vejlby many
take a half-strength tablet a day, so it credits each with half a day; only the rhythm of each patient's own
dispensings shows the dose, and the six practices under 60 per cent are 041219, 041236, 041248, 041275, 041307 and
041322.

## Readability screen

| Rung | 1 filed | 2 schema | 3 reflex | 4 control | 5 hygiene | 6 linear | 7 organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 one tablet a day | no | no dose column | yes, the usual statin label | no | no | no | no | readable |
| R1 one defined daily dose a day | no | atc_ddd_2026.xlsx | yes, the field's method | the commonest products validate | no | no | no | readable |
| R2 each product's typical rate | no | no | a product-level shortcut | no | no | no | no | readable |
| G each patient's own rate from their refills (decisive) | 3.2 names the dose taken, no sentence says how to know it | no column holds a dose | the reflex lands on R1 | no control certifies a dose | the battery never sets tablets against a patient's own intervals | every new user's dose is read from their own dates | the extract ships as the unit's own record | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the window's ends | 1 July and 31 December 2025 inclusive | exclusive | same call, 15 users start on an end | programme 3.1 ("between 1 July and 31 December"); same call |
| SF2 | the lookback | 365 days before the first window dispensing | 366 days; no earlier dispensing in the extract at all | same 1,485 users | same users (asserted) |
| SF3 | the new user's practice | prescriber of the first window dispensing | the last or the most frequent prescriber | same practice for every user | programme 3.1; every new user's dispensings carry one practice (asserted) |
| SF4 | "more than 30 days in a row" | a run of 31 days or more | 30 or more; part days rounded either way | same status for every user | same call (every status 15 days or more from the edge, asserted) |
| SF5 | the 365 days | days 0 to 364 from the first dispensing | days 1 to 365; the last run counted to day 364 or 365 | same status | same call (as SF4) |
| SF6 | tablets left from an earlier dispensing | used before a later one's | each dispensing starts afresh | same status (0 moves) | programme 3.2 |
| SF7 | the daily dose read from the record | tablets before the last dispensing over the days first to last | the median refill rate; the last three refills; the first year only; snapped to half, one, two or four tablets | same status for all 1,485 | same call (asserted per estimator) |
| SF8 | a new user with one dispensing | not persistent | persistent at some assumed dose | same status | the largest single supply (100 tablets) runs out by day 300 at any dose from a third of a tablet a day |
| SF9 | the line on the unrounded or rounded share | unrounded | rounded | same set | same call (every practice 5.45 points or more from 60) |
| SF10 | rounding a share | half up | half to even | same figures | no share on a half per cent (nearest 0.045) |
| SF11 | old-system dates | day first | month first | same call and shares | days above 12 occur, so no other reading parses; R2.2b |
| SF12 | tablets in a dispensing | packs times the product's pack size | packs alone | figures move | statin_products.csv pack_size_tablets |
| SF13 | conversations held in 2026 | every row of the log | none outside 2026 | same figures | every conversation dated 2026 |
| SF14 | a cancelled conversation | status aflyst with a cancellation date | status alone | same figures | the two always agree (asserted) |
| SF15 | each pharmacy's rate | each statement over the conversations it covered (not cancelled by its date) | over the conversations standing now | figures move | agreement 2.1 ("its agreed rate", one per pharmacy): only the first reading gives one whole-krone rate in all four quarters |
| SF16 | a cancellation on the statement day | none occurs | before or after the statement | same figures | no cancellation dated on a quarter's last day |
| SF17 | the statements' amounts | Danish format 1.234,00 | read as decimals of a thousand | figures move | every amount is a whole multiple of its rate only in the Danish reading |
| SF18 | one person under two pseudonyms | the CPR person table's previous personal number joins them | one pseudonym, one person; every pseudonym sharing a birth date and sex joined | figures move (2,116 and 2,210 against 2,151) | programme 3.3 ("each person counted once however the register numbers them") and cpr_persons_202612.csv; the record agrees (same birth date and sex, no overlap, same product line and practice, asserted) |
| SF19 | the quarters of 2026 | by dispensing date | none other | same figures | every 2026 row dated inside the year |
| SF20 | the last dispensing of 2026 | the person's latest 2026 row | two rows on the last day | same figures | no person has two prescribers on their last day |
| SF21 | a hospital-prescribed 2026 dispensing | a statin dispensed in that quarter | dropped with the hospital rows | ask B moves | programme 3.3 ("had a statin dispensed"); no person's last 2026 dispensing is a hospital's |
| SF22 | the quarter a later cancellation counts against | the quarter its conversation was held in | the quarter the cancellation was entered | ask A moves (26 of 32) | agreement 2.1 (a cancelled conversation is not paid) and the ask ("its conversations of each quarter") |

## Ladder

| Rung | Construction | Joins | 041219 | 041236 | 041263 | 041275 | 041358 |
|---|---|---|---|---|---|---|---|
| R0 | one tablet a day | nine practices | 45.2 | 49.1 | 66.0 | 55.7 | 62.7 |
| R1 | one WHO defined daily dose a day (the field's method) | 041236, 041263 | 67.9 | 54.4 | 51.5 | 60.0 | 69.1 |
| R2 | each product's typical rate over all its patients | the same nine as R0 | 45.2 | 49.1 | 66.0 | 55.7 | 62.7 |
| G | each patient's own rate from their dispensings | 041219, 041236, 041248, 041275, 041307, 041322 | 47.6 | 52.6 | 67.0 | 47.8 | 65.5 |

R0's nine are 041219, 041224, 041236, 041248, 041251, 041275, 041282, 041322 and 041334. Every rung is asserted on
the cut pack and on the clean truth (`checks.py` R3a, R3b, L2); the golden reproduces the world's own status for every
new user (L1) and the independent verifier reaches it by another estimator and a day-by-day count (`verify.py`). The
nearest practice to the line under the golden is 041358 Klinikken Vestervang at 65.45 (5.45 points). Under R1
Kirkebakken sits at exactly 60.0, so a DDD variant may file three practices; every variant stays wrong.

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | new statin users as programme 3.1 files them | filed; SF1, SF2 asserted |
| 2 Unit of account | the patient (pseudonym) | filed (3.1, 3.2) |
| 3 Attribution window | first dispensing 1 July to 31 December 2025 | filed (3.1); SF1 |
| 4 As-of dating | the extract to 31 December 2026, the programme of 26 January 2027 | C1, one extract ships |
| 5 Version basis | old-system and new-system rows | C1, both formats parse; R2.2 |
| 6 Denominator | every new user of the practice | filed (2.1) |
| 7 Weighting | none, each patient once | filed (2.1) |
| 8 Window length | 365 days from the first dispensing | filed (3.2); SF5 |
| 9 Boundary inclusivity | fewer than 60 per cent | filed (2.1); SF9, nothing within 5 points |
| 10 Rounding path | whole per cent after counting | C1, SF10 |
| 11 Tie-break | none needed | C1, no practice at the line |
| 12 Maturity and censoring | every new user's year ends by 30 December 2026, inside the extract | C1, follow-up complete |
| 13 Order of operations | cohort, dose, supply, status, share | C1 |
| 14 Row order | file order irrelevant | C1, rows sorted by date |
| 15 Duplicate resolution | no duplicated dispensing row | C1, R3c |
| 16 Identity normalisation | product numbers to products, prescribers to practices | C1, SF3, SF12 |
| 17 Netting against gross | none on the call | not applicable to the call; asks SF15, SF17 |
| 18 Dimensional units | tablets, days, per cent | units in the headers |
| 19 Code and status semantics | ATC C10AA, prescriber codes | filed (3.1); the product list |
| 20 Integerisation | patients counted whole | C1 |
| 21 Clause scope | general practices only; a hospital first prescription belongs to no practice | filed (3.1) |
| 22 Forward window contents | 2027 membership rests on the closed 2025 cohort | filed (2.1) |

## Literal reader

Executed word for word: the prompt asks whether any practice joins the 2027 programme; programme 2.1, 3.1 and 3.2
fix the cohort, the horizon, the 30-day run, the carry-over and the line, and 3.2 times each dispensing at the dose
the patient takes. Every literal reading of those sentences gives the golden once the reader establishes each
patient's dose, which the register leaves to its own dates: SF1 to SF12 show every convention converges or is ruled
out by a quoted sentence, and every estimator of the dose converges (SF7). The DDD answer is not another reading of
any sentence; it is the field's method applied where its precondition, that a patient takes one defined daily dose a
day, fails in the record. The asks read the same way: agreement 2.1 and 2.2 and programme 3.3 file the payment and the
continuing users, and SF13 to SF22 close their conventions.

## Oracles

- The DDD timing validates on the commonest products (a check that passes for the easy route, not an oracle for the
  golden).
- No shipped control certifies a dose, a status or a share; the national report (distractor) uses a 180-day refill
  definition on the 2023 national cohort, and the published regional use in DDD per 1,000 a day measures volume.
- Asks: each statement over the conversations it covered returns its pharmacy's whole-krone rate in all four quarters
  only when the conversations are counted as they stood on the statement date, an identity a grader can confirm once
  the later cancellations are noticed; a replaced personal number is filed in the CPR person table, and the record
  agrees with it (the same birth date and sex, the same product line continuing at the next refill).

## Ask sheet

Two asks on rows the call never reads (the pilot's log, statements and agreement; the register's long-standing users
in 2026 and the CPR person table); neither feeds the chart.

**Ask A, what each pilot pharmacy is entitled to for its conversations of each quarter of 2026 (32 figures, whole
kroner).** Home: agreement 2.1, the pilot's settlement, quarter by quarter as finance corrects its statements, before
the 2027 programme takes on the same pharmacies.
- Primary device (D9, a control true only in its scope): finance drew each statement on the quarter's last day over the
  conversations not yet cancelled, and 64 conversations (one to three in every pharmacy-quarter) were cancelled after a
  statement had covered them, the last by 20 January 2027; the rates sit in annexes that do not ship, so the only
  record of each is its statements over the conversations they covered, a rate that comes out whole and alike in all
  four quarters only when the log is read as it stood on each statement date, and no quarter is clean enough to read
  it off directly. Entitled is that rate times the quarter's conversations held and never cancelled.
- Hazards: cancellations entered inside the quarter; Danish amounts (1.234,00) and dates (31.03.2026); conversations
  late in a quarter cancelled a few days after it closed; the quarter a later cancellation counts against (SF22).

**Ask B, each practice's continuing statin users of 2026 (16 counts).** Home: programme 3.3, the baseline the 2027
follow-up capacity is planned on. A construction ask since the round-1 judge: 35 long-standing users (one to three at
every practice) had their personal number replaced in 2026, the register carries them under a new pseudonym from the
change, programme 3.3 counts each person once however the register numbers them, and the CPR person table
(cpr_persons_202612.csv) gives each new number's previous one. A response that counts pseudonyms (2,116) or joins
everyone sharing a birth date and sex (2,210) misses every practice; the cracker, executing 3.3, joins through the
person table and keeps the ask (2,151).
- Hazards: hospital-prescribed 2026 dispensings (a filter to practice prescriptions drops a quarter, SF21); 855 groups
  of people sharing a birth date and sex whose dispensings overlap; the practice of the last 2026 dispensing.

Pin test: the asking sentences pin the unit (whole kroner, a count), the grain (each quarter's conversations, each
practice) and the population; no pin names a statement date, a cancellation date, a rate, a pseudonym or a
replacement. Agreement 2.2 says only when statements are drawn and paid, not what they cover. The main population
carries zero device rows: no new user's pseudonym is joined (R2.6), no new user's row has a hospital prescriber
(R2.3b), and the call reads no pilot file (R2.4, R2.5).

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| A, every pharmacy and quarter (64 later cancellations, one to three in each) | takes each statement as its quarter's entitlement, or reads the rate off a statement over the conversations standing now | miss |

Ask B is kept by the cracker and counted in the leakage below. The response that also reads the statements as they
stood keeps all 48.

Pair ceiling: 46.8 ((38 + 7 + 55 x 0.333) and (5 + 7 + 55 x 0.333), averaged)
Mirror leakage: 33.3 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack)

## Build record

Generator under `generator/`: params.py, world.py (the clean truth), asks_world.py (the register rows, replacements
and the pilot, on its own stream), pack.py (thirteen files, three formats), analysis.py (every rung and figure from
target/ alone), golden.py, writeup.py, build.py (two byte-identical builds, metadata.json, figures.json,
submission.md, target.zip), checks.py (73 assertions), verify.py (independent: pandas, its own XLSX and PDF readers,
the median refill rate and a day-by-day count; 80 checks), ceiling.py. The spine is
statin_dispensings_202401_202612.csv, 61,788 rows.

Round 1 (judge on eb685de6): the call, the shares, the PDF and the pilot figures reproduced and held under windows of
364 to 366 days, gaps of 29 to 31 and no carry-over; Gates G and H passed, Gate F moderate. Ask 4 (continuing users)
failed Gate C: nothing shipped gave the replaced numbers' link. Repaired in the generator: programme 3.3 files that a
person counts once however the register numbers them, the CPR person table carries the previous number (sex and birth
date move there from the extract, as in the register), the pilot settlement is asked per quarter, every cancellation
is dated before the programme's adoption, the published series moves smoothly, and the English documents are the
region's working versions. The call and every share are unchanged; the continuing users are unchanged (2,151); the
pilot entitlements are now quarterly, and with a later cancellation in every pharmacy-quarter six pharmacies' annual
totals moved (A114 and A126 unchanged; the eight now total DKK 313,629 against 327,918 paid).

## Architecture 2 record (spent 2026-11-01)

Built 2026-11-01 (round 1 repaired to target.zip bbcaedf8) and spent the same day at the re-judge: Gate G banned (planted_defect_flip, surface_read_rejection: the stump rejected the planning model's line map, and on clean data the call collapses to executing rate card 3), Gate H3 failed as planted (the weekday-peak through-running was written in no shipped file and recoverable only from ride durations), and three reach figures (Overstappunten 45, Centraal 33, Binnenstad 32 against the shipped 47, 34 and 33) were not reproduced. Its note, kept for the record:

Architecture 2, drawn 2026-11-01 at the Batch 3 queue reset. Architecture 1 (an intergovernmental liability pool's
per-occurrence retention) is kept below as `## Architecture 1 record`; its world is closed.

### Draw

- **Card:** `cards/task255.json`, architecture v2, registered 2026-11-01 (guard check PASS, nearest cards task451,
  task135, task161 and task460, each differentiated on the card). Marketing & Consumer Research, task type
  media-reach-frequency-audience-measurement, objective Descriptive & Distribution Analysis (the number's lane is
  kept; the actuarial descriptive cell, claims-frequency-severity, is spent for a stump in this slot). Shape 10, a
  scorecard: each package's effective reach checked against the Tier G line. Decision designation_set; gap time and
  population; generators G7 (the operating window), G12 (two gates and nothing between) and G2 (the rider, not the
  journey row, carries the frequency); Gate G method_or_model_selection; context artifact a monitoring export (the
  player log); stakeholder the head of audience research.
- **World:** Spoorbeeld Media B.V. holds the advertising concession of the Ravelmond metro (a fictional Dutch city,
  three lines: M1 north-south, M2 west-east, both through Centraal, and the M3 ring between Ravelpark on M1 and
  Handelshaven on M2). It sells its digital screens in nine packages (the halls and interchange passages of rate card
  Annex A). From 1 January 2027 a package whose effective reach in the autumn audience window is 40 per cent or more
  is sold in Tier G with a reach guarantee and a 22 per cent surcharge. The operator, the Ravelmondse Vervoerbedrijf
  (RVB), re-exported its OV-chipkaart metro journeys of 1 October to 4 November 2026 on 5 November. Personas from
  `guard.py names --geo NL --seed 255`: Floortje Brugman (audience research, the golden's author), Evie Hondeveld
  (sales, the bookings workbook), Daphne Riem (RVB data warehouse), Brent Velderman (screen operations, the register).
  As-of date of the fiction: Friday 13 November 2026.
- **The call:** which packages are sold in Tier G in 2027. Golden: Overstappunten, Oosttak and Zuidtak (47, 47 and 46
  per cent); every other package standard tier. The call faces forward (the 2027 rate card's tiers) and is measured on
  a closed window, which the rate card itself fixes (3.2); the descriptive tag stands because the deciding quantity is
  the distribution of opportunities to see over a population, not a predicted value.
- **Shape arithmetic:** nine packages times reach and tier (18), the call and the nearest package below the line (2),
  the chart with its line and shading (3), make-good for each autumn booking (10), screens on sale for each package
  (9), net revenue for each package (9): 51 gradable figures, 28 of them asks.
- **Data-native sentence:** an OV-chipkaart journey records only its two gates and their times, so every pass in
  between is inferred from a route; here the route depends on the hour, because the operator interworks the
  branches through Centraal at the weekday peaks, and the check-out time less the check-in time is the only record
  that shows it.

### Survivor anatomy

- **Actor:** the deciding property, whether a journey changed trains at Centraal, has no column in any file: the
  journey row holds a card, two stops, two gates and two times, and the change is a relation between those times and
  the planning model's run and walking times, grouped by the hour of day and the pair of branches.
- **Link:** the signal is read through a comparison no key offers: each journey's duration against the network's own
  timings (Halls walks, Run times, the Interchanges passage walk, Frequencies for the wait), a cross-file reading the
  field's path assignment never asks for, since an assignment takes the route from the network and the duration
  from nowhere.
- **Reflex:** the field's method for the deciding quantity, assigning each origin-destination trip to its path on the
  published network and crediting every frame on the path (the way transit out-of-home audience measurement credits
  passages), sits at rung 1 and files Tier G for Centraal, Binnenstad, Overstappunten, Oosttak and Zuidtak, with
  Centraal at 63 per cent.
- **Back-test:** the easy route validates: every journey's fare in the extract reconciles to the line-map route's
  stop count, off the peak and at weekends every journey's duration fits the line map, and the Frequencies sheet
  lists one service per line.
- **Second use:** every file the decisive step reads is in the pack for its own reason: the journeys extract is the
  operator's fare and ridership record, the planning model is how RVB schedules its timetable (run times, walks,
  frequencies, the gate inventory), and the rate card is the price list the decision amends.
- **Shock:** the movement the step recovers reads as ordinary: Centraal's and Binnenstad's reach fall because riders
  change elsewhere, not because anything anomalous happens; sorted by the line map's reach (Overstappunten 76,
  Centraal 63, Binnenstad 56, Oosttak 47, Zuidtak 46) or by the gates alone (Zuidtak 41, Oosttak 40, Eindhaltes 35),
  by price or by screen count, the golden set is not an interval of any shipped statistic.
- **Pins:** the WHAT is filed in rate card section 3 and Annex A in the concessionaire's own genre (the window, the
  regular rider, the passes, effective reach, the line); no filed sentence names the peak, the service pattern, a
  duration or the interworking, and deleting any filed sentence only unfixes the population, the window or the
  count, never the step.

### Three rules

- **Task type:** media-reach-frequency-audience-measurement in marketing-consumer-research, which serves Descriptive &
  Distribution Analysis: the distribution of opportunities to see across a rider population, read at an effective
  frequency.
- **Domain test:** the call turns on each package's effective reach, the share of the regular riders who had three or
  more opportunities to see over a four-week flight, built rider by rider from where each journey took them; that is
  the media field's reach and frequency distribution read at an effective-frequency threshold, worked on smart-card
  trips by assigning each trip to its path through the network's halls and passages.
- **Swap:** "which hospital wards go into the guaranteed-staffing tier, set by the share of regular nurses passing a
  ward's screens three times a month": no flight, no opportunity to see, no effective frequency, and no trip whose
  path between two recorded gates carries the frames.
- **Layer 1:** (1) the RVB extract re-exported after the gate-firmware update of 19 October, so four stations carry
  two name spellings and their gates two code formats (the operator's export); (2) staff and service cards beside
  passenger products (the card system); (3) 951 window journeys with no check-out, riders who forgot to tap out
  (the gates); (4) local clock times across the 25 October change from summer time (the extract); (5) the screen
  register kept as a log of hangings, moves and take-downs, with the supplier's replacement units of 3 to 5
  November under new tags (screen operations); (6) the player log in UTC (the content management system); (7) the
  billing system replaced on 15 October, legacy invoices gross of VAT in Dutch number format, credit notes on legacy
  invoice numbers (finance). Nothing is placed to be caught; items 1 to 4 move nothing on the call (asserted R2),
  items 5 to 7 sit only in the asks' files.
- **Layer 2:** estimand identification under a violated precondition: path assignment presumes the published network
  is the service ridden; here the service differs by hour, so the population of riders who used the interchange
  passage has to be identified from the journeys themselves.
- **Decisive step:** recognising that on weekday peaks the trains passing Centraal run north with east and west with
  south, so the published line map is not the service ridden then, and placing each Centraal change of trains from
  the journey's own duration against the walking and run times rather than from the map.
- **Not semantics:** every field, code and unit read correctly (gates to halls in both formats, product classes, the
  local clock, the window, the annex) still leaves the line map's routes, because no field, code or definition says
  how trains ran at an hour; the deciding fact is a pattern in the durations.
- **Not rule application:** no filed rule says where a rider changes trains; rate card 3.4 credits "the interchange
  passage of any station where the rider changes trains on the way" and leaves the route to the analyst. Enumerated
  family (every construction a competent analyst reaches for): the gates only (Tier G Zuidtak alone, Centraal 16),
  the line map (five packages, Centraal 63), every journey through Centraal credited (five packages, Centraal 66),
  the peak pattern on every weekday hour (three packages, Centraal 29), each journey read from its own duration
  (three packages, Centraal 34): a spread of 50 points on Centraal and three distinct tiers. Standing family (what
  the durations leave defensible once the step is taken: a cut anywhere in the empty band, the pattern read off the
  clock at check-in, at Centraal or at check-out, the route by fewest changes, by time, with the halls' walks or the
  expected waits): the same riders in every package, by construction. The line map is ruled out by no filed
  sentence, only by the record, and loudly: the minutes a journey through Centraal took over its walks and runs leave
  an empty band from 5.7 to 7.7 minutes, every north-south and west-east journey of the weekday peaks above it and
  every north-east and west-south one below it.
- **Analyst test:** a strong analyst who cleans the extract, applies every rate-card rule and assigns each journey to
  its line-map path, the field's way of placing the passes no gate records, files Tier G for Centraal, Binnenstad,
  Overstappunten, Oosttak and Zuidtak with Centraal at 63 per cent; only reading the durations moves Centraal and
  Binnenstad to 34 and 33.
- **Estimand:** rate card 2027 (Spoorbeeld_tariefkaart_2027.pdf) section 3: a package is sold in Tier G when its
  effective reach in the audience window (5 October to 1 November 2026, the operator's OV-chipkaart metro journeys)
  is 40 per cent or more, effective reach being the share of regular riders (passenger cards with a journey in each
  of the window's calendar weeks, dated by check-in) whose journeys passed its Annex A halls and passages three
  times or more, passes counted at the check-in hall, the check-out hall and the passage of any station where the
  rider changes trains.
- **No decoy:** nothing is planted to be caught: no memo, draft, briefing, stakeholder figure, copied block or hidden
  rule ships; the fares follow the planned route as a distance fare does in any OV-chipkaart system, and the
  distractors (published boardings, a passenger survey, an industry benchmark) answer other questions.
- **No certified replay:** no shipped figure certifies a reach, a pass count or a route, so the method is not
  recovered by reproducing a published number; the decisive pattern is found in raw durations.
- **Lesson:** a path assignment is only as good as the assumption that the published network is the service run;
  where a trip's own clock times exist they test that assumption, and an analyst who checks them finds the service
  that was actually ridden. No build on file reads a route from trip durations against a timetable.

### Default path

1. Take the passenger cards of RVB_metro_ritten_20261001_20261104.csv with a journey checked in during each
   calendar week from 5 October to 1 November 2026 (rate card 3.3): 1,901 regular riders.
2. Map each journey's check-in and check-out gates to halls through the planning model's Gates sheet.
3. Route each journey over the published lines by the fewest changes (the field's path assignment) and credit the
   interchange passage of every station where the route changes line: every north-east and west-south journey
   changes at Centraal, every north-south and west-east journey rides through.
4. Count for each Annex A package the regular riders passing its places three times or more and set each share
   against the 40 per cent line.

Ends on: Tier G for Centraal, Binnenstad, Overstappunten, Oosttak and Zuidtak, Centraal at 63 per cent.
Golden: Tier G for Overstappunten, Oosttak and Zuidtak, Centraal at 34 per cent.

### Stump sentence

The default path puts every change of trains where the line map puts it and files Tier G for Centraal, Binnenstad,
Overstappunten, Oosttak and Zuidtak, Centraal at 63 per cent; on weekday peaks the north and east branches run
through Centraal into each other and the west and south likewise, so the big north-east and west-south commuter
flows never use the interchange passage, which only each journey's duration against the network's timings shows,
and Centraal and Binnenstad fall to 34 and 33 per cent.

### Readability screen

| Rung | 1 filed | 2 schema | 3 reflex | 4 control | 5 hygiene | 6 linear | 7 organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 gates only | no | the gate columns | yes, the halls | no | no | no | no | readable |
| R1 line-map path assignment | 3.4 asks where riders change | Run times and Interchanges | yes, the field's method | fares reconcile | no | no | no | readable |
| R1b every Centraal through-journey credited | no | no | yes, a station-level shortcut | no | no | no | no | readable |
| R2 peak pattern on every weekday hour | no | no | no | refuted by the shoulder hours | no | no | no | silent |
| G durations read at Centraal (decisive) | no sentence names a peak, a service or a duration | no column holds a route or a change | the reflex lands on R1 | no control scores routes | the battery never sets durations against run times | the reach needs every rider's passes rebuilt | times and timings ship for fares and timetabling | silent |

### Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a regular rider's four weeks | calendar weeks Monday to Sunday | seven-day blocks from 5 October | same call, same 1,901 riders | same call (the window starts on a Monday) |
| SF2 | the date a journey counts on | check-in | check-out | same call and figures | rate card 3.3, and same call |
| SF3 | staff and service cards | left out | kept | same call, figures one point up | rate card 3.3 ("not a staff or service card"); RVB_productcodes.csv card_class |
| SF4 | a journey without a check-out | its check-in hall only | dropped | same call and figures | rate card 3.4, and same call |
| SF5 | "passes ... each time" | per place passed | once per journey | same call, three figures move | rate card 3.4 counts each hall or passage the journey takes the rider through |
| SF6 | the hall a gate stands in | the Gates sheet | the stop alone | same call and figures | same call (no package lists one Centraal hall alone) |
| SF7 | the route between two gates | fewest changes, then time | time alone; the journey's own hall walks added; the expected waits of the peak or the quiet hours added | same riders in every package | same call (the regular riders travel only station pairs every costing routes alike; asserted) |
| SF8 | where a journey's own duration says it changed | above the empty band in the excesses | a cut at either edge of the band | same riders in every package | same call (no journey's excess falls in the 5.7 to 7.7 minute band; asserted) |
| SF9 | the minute the service pattern is read at | each journey's own duration | the clock at check-in, at Centraal from either end, or at check-out | same riders in every package | same call (no regular rider's trip through Centraal spans a change of pattern; asserted) |
| SF10 | the line on the unrounded or the rounded reach | unrounded | rounded | same call | same call (every package 5.18 points or more from 40) |
| SF11 | the journeys' clock | local | an hour off after 25 October | same call and figures | same call |
| SF12 | rounding a reach | half up | half to even | same figures | same call (every reach 0.16 of a point or more inside its bin) |
| SF13 | the player log's clock | UTC read in Ravelmond time | read as local | make-good moves | the column header event_time_utc; general terms 6.1 local time |
| SF14 | when a taken-down screen goes dark | the day's opening | the start of the date the register gives | same make-good | same figures (its player was switched off the evening before) |
| SF15 | part of an hour of make-good | counts as an hour | rounded to nearest | make-good moves | general terms 6.3 |
| SF16 | booked screen-hours | the bookings workbook | opening hours times booked screens | same figures | same figures (they agree) |
| SF17 | on sale on 1 January 2027 | hung by then and not taken down by then | none falls on the day | same counts | same counts |
| SF18 | a screen held outside the packages | in no package | its old package | counts move | its register row carries package "-" |
| SF19 | legacy invoice amounts | split out the VAT | gross | revenue moves | the header bedrag_incl_btw; general terms 8.3 excluding VAT |
| SF20 | the agency commission | each agency's contract rate | the rate card's standard 15 per cent | revenue moves | rate card section 2 and general terms 8.2 ("the rate in the agency's contract") |
| SF21 | the VAT split | rounded to the cent | unrounded | same 10-euro figures | same figures |
| SF22 | when a screen moved off a dead player connects to the receiving player | the receiving player's first report counting it among its displays | the register's entry (the work order's closing) | make-good moves | general terms 6.2 ("connected ... from the player's first report in the content management system that counts the screen among its displays") |
| SF23 | the register's connection times | Ravelmond local time | read as UTC | same make-good | same figures; the header says connected_from_local |
| SF24 | a player whose first status in the log is ONLINE | offline from before the log began | online until its first OFFLINE | make-good moves | the log's own events: an ONLINE report ends an offline spell |
| SF25 | two open register rows at one position | one screen (the replacement unit) | two screens | counts move | both tags sit on one player output, and the player reported as many displays after the night's work as before it |

### Ladder

| Rung | Construction | Tier G | Centraal | Binnenstad | Overstappunten |
|---|---|---|---|---|---|
| R0 | the gates only (halls of check-in and check-out) | Zuidtak | 16 | 17 | 0 |
| R1 | the line map's changes (path assignment, the field's method) | Centraal, Binnenstad, Overstappunten, Oosttak, Zuidtak | 63 | 56 | 76 |
| R1b | every journey through Centraal credited with the passage | the same five | 66 | 59 | 80 |
| R2 | the peak pattern on every weekday hour | Overstappunten, Oosttak, Zuidtak | 29 | 29 | 42 |
| G | each Centraal journey read from its own duration | Overstappunten, Oosttak, Zuidtak | 34 | 33 | 47 |

R2 lands the call with three wrong figures and is refuted by the shoulder hours (`checks.py` L5). Every rung is
asserted on the cut pack and on the clean truth; the golden reproduces the world's own passes for every rider, and
every classification and routing the record licenses gives the same riders in every package (SF7 to SF9). The
nearest package to the line under the golden is Eindhaltes at 34.82 (5.18 points).

### Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | regular riders as rate card 3.3 files them | filed; SF1, SF3 asserted |
| 2 Unit of account | the passenger card | filed (3.3) |
| 3 Attribution window | journeys dated by check-in, 5 October to 1 November | filed (3.2, 3.3); SF2 C1 |
| 4 As-of dating | the extract as re-exported on 5 November | C1, one export ships |
| 5 Version basis | gate codes before and after the firmware update | C1, both formats map to halls (R2) |
| 6 Denominator | all regular riders | filed (3.5) |
| 7 Weighting | none, each rider counts once | filed (3.5) |
| 8 Window length | four calendar weeks | filed (3.2) |
| 9 Boundary inclusivity | 40 per cent or more | filed (3.1); SF10, nothing within 4 points |
| 10 Rounding path | whole per cent after counting | C1, SF12 |
| 11 Tie-break | none needed | C1, no package ties at the line |
| 12 Maturity and censoring | journeys without a check-out | filed (3.4); SF4 C1 |
| 13 Order of operations | population, then passes, then shares | C1 |
| 14 Row order | file order irrelevant | C1, counts are order-free |
| 15 Duplicate resolution | no duplicated journey rows | C1, asserted no copied history |
| 16 Identity normalisation | stop codes and gate codes | C1, SF6 |
| 17 Netting against gross | none on the call | not applicable to the call; asks SF19 to SF21 |
| 18 Dimensional units | minutes and per cents | units in the headers |
| 19 Code and status semantics | product classes, gate formats | the product list's card_class; the Gates sheet |
| 20 Integerisation | riders counted whole | C1 |
| 21 Clause scope | Annex A places per package | filed (3.4, Annex A) |
| 22 Forward window contents | the 2027 tier rests on the closed autumn window | filed (3.1, 3.2) |

### Literal reader

Executed word for word: the prompt asks what belongs in Tier G; rate card 3.1 to 3.5 and Annex A fix the
window, the regular rider, the passes, effective reach and the line. Every literal reading of those sentences gives
the golden once the reader establishes where riders changed trains, which 3.4 leaves to the records: SF1 to SF12
show every convention either converges or is ruled out by a quoted sentence, and the routes converge (SF7). The
line-map answer is not another reading of any sentence; it is the field's method applied to a network the journeys
show was not running at the peaks. The asks read the same way: general terms 6.1 to 6.3 and 8.1 to 8.3 file the
make-good and net revenue, and SF13 to SF25 close their conventions.

### Oracles

- The fares reconcile to the line-map route on every journey (the operator charges by planned distance): a check
  that passes for the easy route, not an oracle for the golden.
- No shipped control counts passes, reach or routes; the published boardings, the passenger survey's screen-notice
  shares and the benchmark (distractors) cannot arbitrate a package.
- Asks: each agency's statement amount over the value it was struck on returns the agency's round contract rate
  (13.5, 12.5, 17.5 per cent) only on the value net of the credit notes issued by 31 October, an identity a grader
  can confirm once the dating of the three later credit notes has been noticed; the receiving player's display
  report is the evidence for each re-cabling, not a control that ties only under the golden.

### Ask sheet

Three asks on the files the call never reads (the register, the player log, the bookings, the terms, the two
billing systems and the statements); none feeds the chart.

**Ask A, make-good owed per autumn booking (10 figures, whole hours).** Home: general terms 6.3, the first quarter of
2027.
- Primary device (D4, absence evidenced in the log's own first record): the players behind seven of the 5 October
  bookings had been offline since late September, and the player log's export starts on 1 October, so each one's
  first status there is ONLINE in the flight's first days; only reading that ONLINE as the end of an outage makes
  those days dark (20 to 70 hours a screen).
- Second device (D8, a recorded date for the event date): every booking had one player die and its screens re-cabled
  to a working player a day or two later; the register enters the move when the work order is closed, one to six
  days after the job, and terms 6.2 files that a screen connects from the receiving player's first report counting it
  among its displays, so the reconstruction joins the register's moves to the player's display counts.
- Hazards: the player log in UTC across the 25 October change (6.1 local time); Wilgenhof's player switched off the
  evening before its screens came down (6.2); the 0.5 per cent allowance and rounding up (6.3).

**Ask B, screens on sale on 1 January 2027 per package (9 counts).** Home: the 2027 inventory behind the rate card.
- Primary device (D7, the true key elsewhere): the supplier's replacement units, swapped at night from 2 to 4 November
  at eight halls and passages, came in under new asset tags while the old units' rows and connections were never
  closed, so one position carries two open rows; the position is the screen, as the cabling shows (both tags on one
  player output) and the player log confirms (each player reported as many displays after the night's work as
  before it). Every package has a replaced screen.
- Hazards: the status column as of 12 November against the planned December take-downs and hangings; moved screens
  (the same tag on a new row, the old row closed); a screen held outside the packages (package "-").

**Ask C, net revenue from the autumn bookings per package (9 figures, nearest 10 euros).** Home: the revenue base
the Tier G surcharge is priced on.
- Primary device (D9, a control true only in its scope): each agency's statement of 31 October settled commission on
  the value net of the credit notes issued by then, and three credit notes (one per agency) came in early November;
  commission due under 8.2 is the contract rate, recovered as the statement's amount over the value it was struck
  on, applied to each booking's value net of every credit note.
- Hazards: legacy invoices gross of VAT in Dutch number format; a credit note against a legacy invoice number; the
  year's other invoices in both systems.

Pin test: the asking sentences pin the unit (hours, counts, euros), the rounding, the date (1 January 2027) and the
population (the autumn bookings); no pin names an outage open at the log's start, a position, a tag or a statement
date. Terms 6.2's sentence on when a screen connects files the WHAT of the re-cabling device, so the cracker takes
that device; the open-start outages carry ask A. The main
population carries zero device rows: the call reads the journeys, the planning model, the product list and the rate
card, and no ask reads any of them (`checks.py` R2 and SEP).

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| A, the seven 5 October bookings | builds offline spells from OFFLINE and ONLINE pairs only | miss |
| B, every package | keeps each tag's latest row, so a replaced position counts twice | miss |
| C, the seven agency packages | shares each statement's amount over its bookings | miss |

Pair ceiling: 38.3 ((38 + 7 + 55 x 0.179) and (5 + 7 + 55 x 0.179), averaged)
Mirror leakage: 17.9 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack)

### Build record

- Generator: `generator/` (params, world, asks_world, pack, io_util, analysis, golden, checks, verify, ceiling,
  writeup, build). World from SEED 25502, the commercial records from their own stream (salt 298) and the season's
  operations from theirs (salt 187); 2,183 habitual riders drawn, 1,901 of them regular in the window.
  Deliverables: tier_g_2027.xlsx (four sheets) and tier_g_2027.svg (the reach chart, titled with the call).
- Free gates on the final cut after the round 1 repair: see `## Judge record`.

### Leak record

- REVIEW, Spoorbeeld_tariefkaart_2027.pdf carries most words of the call: the rate card defines Tier G and lists
  every package by name in its price table and Annex A; it ranks nothing and selects nothing. Harmless.
- REVIEW, the rate card carries six stump-paragraph words (Centraal, journey, window, service, nothing, trains):
  they come from 3.2 to 3.4 (the window, a journey, "a staff or service card", "changes trains", "and nothing
  else") and Annex A; no sentence names a peak, a service pattern, a duration or through running. Harmless.
- REVIEW, schermregister_2026-11-12.xlsx holds dates after the as-of date: the planned hangings of 7 to 10
  December, the booked take-downs of 14 and 21 December and Wilgenhof's re-hanging on 1 February 2027, a register's
  forward-looking rows (the allow-list of `reduce-house-fixes` H16). Harmless.
- The booking numbers (0411 to 0437) appear in the agency statements and in block 4 as identifiers; they are listed
  under `stated_inputs` in metadata.json.

### Judge record

- Round 1 (stage 4, main session): leak reader clean, question 6 analytical. Judge NOT_DETERMINISTIC, SEND_BACK, with
  the call forced under every variant it ran (Gate F strong, G and H pass, H "analytical, borderline planted"; the
  rate card's "where the rider changes trains" kept word for word as the estimand). Failures on component figures
  and asks, all repaired in the generator:
  1. Reach cells: the per-journey duration test the write-up describes gave Centraal 31, Binnenstad 32 and
     Overstappunten 48 against the shipped 33, 33 and 49, and Zuidtak moved with the halls' walks in the route. The
     golden is now that per-journey test, its cut read from the empty band in the record; the world gives every
     regular rider's trip through Centraal a clean duration (M1 and M2 every 3 to 5 minutes, the Centraal passage 8.0
     minutes), keeps every such trip wholly inside or outside a peak window, and lets regular riders travel only
     station pairs that every costing routes alike. Each classification and routing gives the same riders in every
     package (SF7 to SF9).
  2. Make-good: terms 6.2 now files when a screen connects (the player's first report counting it among its
     displays), so the register's work-order dates are a wrong basis; Wilgenhof's player is switched off the evening
     before its screens come down, so the take-down's hour no longer moves a figure (SF14); the register's headers
     carry their zone (SF23); every figure 0.21 of an hour or more inside its whole hour. With the re-cabling filed,
     ask A rests on outages already open when the log begins (SF24).
  3. Screens on sale: the replacement units now sit on the old units' player outputs, and the player log shows each
     player's display count unchanged across the night's work (SF25).
  4. The repeated asset tag was a moved screen whose old row was left open; every moved screen's old row is now closed
     on the day it moved (B4).
- Free gates on the repaired cut (target.zip bbcaedf8): checks.py 78 of 78; verify.py 7 of 7 on its own code path
  (it finds the empty band from the data); two builds byte-identical over 18 files; figures_check.py 64 of 64;
  precut.py 61 checks, 0 FAIL, 0 WARN; voice-check.py PASS; leak.py --asof 2026-11-13 REVIEW (the three lines of the
  Leak record); guard.py heart WARN only (repeat.gate_g against task125 v4, drawn 2026-10-31, which became one of the
  last two draws when task133 and task138 re-registered; method_or_model_selection is this build's honest mechanism,
  so it stands); guard.py surface 10 pairs for the author's adjudication, nearest task254 back to back on G7;
  ceiling.py pair 38.3, mirror 17.9.

## Architecture 1 record (spent 2026-11-01)

### Draw

- **Card:** `cards/task255.json`, registered 2026-10-13. Actuarial Science & Insurance, task type
  claims-frequency-severity, objective Descriptive & Distribution Analysis; shape 04 (setting one dial: each quoted
  attachment); decision dial_setting; gap population; G12 then G16; Gate G method_or_model_selection; strategy
  maturity_censoring (here limit censoring at the pool's retention with deductible truncation, no maturity element).
- **World:** Fallowmere Intergovernmental Risk Pool, a Washington pool of 62 cities and special districts. The pool
  shares its members' liability occurrences above each member's deductible ($10,000, $25,000, $50,000 or $100,000,
  elected yearly) up to its per-occurrence retention, inclusive of the deductible ($250,000 for occurrences in 2014
  to 2017, $500,000 from 2018); its excess insurer pays above the retention, outside the pool's claims system. For
  1 January 2027 the broker gathered indications at seven attachments from $1.0 million to $5.0 million, and the
  trustees' risk financing policy keeps every layer the pool expects to be reached more than once a year. The
  trustees set the 2027 retention at their meeting of 18 November 2026 (forcing event vote_or_meeting).
- **People** (guard.py names --geo US --seed 255): Laura Williams, finance director; Larry Hodge, consulting actuary;
  Matthew Klein, the broker's account executive; Caleb Payne, claims manager.
- **Data-native sentence:** a pool's claims record is a window on its members' losses: an occurrence enters it only
  once its member has paid the deductible in force that year, and stops at the pool's retention, beyond which the
  excess insurer pays and the pool records nothing; both thresholds were fixed in each year's dollars, so at 2027
  cost every occurrence carries its own floor and its own ceiling; and the occurrences that pierced the retention are
  suits the excess insurer goes on defending for years after the pool has paid its layer, so the pool's files on
  exactly those occurrences stay open long after the small ones close (20 of the 108 from 2014 to 2021 are open).
- **Loop 1 (2026-10-13, the author's request for a second layer of stumping):** the world no longer forces every
  occurrence of 2014 to 2021 closed; an occurrence past the retention runs a suit about three years longer (the excess
  insurer's defence), and once it has used the pool's layer the pool's file stays open until the excess insurer
  closes its own. Twenty such suits of 2014 to 2021 are open at 30 September 2026, every one with the layer paid in
  full and nothing reserved. The policy's window is now named without closure ("the eight accident years before the
  latest five"), so the record of those years holds open files. The golden is unchanged ($4.0 million, 0.74 and
  1.25): the loop-0 construction on every file. The loop-0 construction on the closed files alone, the natural way
  to fit severity to final costs, drops a fifth of the occurrences that reached the retention and files $3.0
  million. No file, column or sentence was added; the strategy stays maturity_censoring (open files of the window,
  beside the retention's censoring), the second layer a selection by settlement.
- **Loop 2 (2026-10-26, after the portal's FAILED_TO_STUMP):** both portal responses filed the loop 1 golden, so the deductible-truncated, retention-censored likelihood is now the reflex rung. The world keeps its pool, files and asks; its liability occurrences now come from two severities, law enforcement liability (police civil-rights and use-of-force suits, a far longer tail) and the other four coverage parts, and the actuary's Exhibit 6 projects 2027 frequency above $25,000 on each group's own exposure (police department payroll 85.5, all other payroll 364.3). The retention history is $500,000 for 2014 to 2017 and $1,000,000 from 2018. The policy files the estimand (expected 2027 occurrences above each attachment from the actuary's expected number above $25,000 and the estimated probability) and the family (lognormal, maximum likelihood, the record of 2014 to 2021 at 2027 cost), never a single curve or a curve per part. One curve over the pooled record, the route both portal responses and both call-only probes took (p255a, p255b, 2026-10-26), files $2.0 million (0.92); a curve per group weighted by the two projections files $4.0 million (1.20 above $3.0 million, 0.83 above $4.0 million). The record rejects the pooled curve (likelihood ratio 158 on 2 degrees of freedom) and a common spread with a shifted log mean (29 on 1; it files $2.5 million). The executive director now sets the retention in the 2027 budget under the trustees' delegated authority (card: executive_team, budget_or_appropriation, local_government; the old forum, event and family were blocked by drift in the guard window). Heart WARN: the people's first names, Gate G, decision type and deliverable set repeat older builds, answered here: the people stay (no full name is reused), the Gate G and dial are this slot's own and the two files are what a retention decision produces.
- **Guard:** WARN repeat.gate_g and overuse.gate_g (method_or_model_selection after task450 and task501): the
  mechanism here is a loss model's observation process, deductible truncation and retention censoring in the
  likelihood, against task450's emissions grain and task501's transmission model; the vocabulary's nearest honest key.
  Question form how-much: the attachment is the amount of each occurrence the pool keeps.
- **Pairing and shape:** the field's own analysis decides (a loss distribution fitted to data observed through
  deductibles and a retention), the objective is the shape of that distribution's tail, and the call is a dial over
  seven quoted attachments (shape 04). Criteria: seven attachments, each with its expected 2027 count above it and its
  2027 premium (14); the call, the runner-up ($3.0 million), the gap and the flip (4); the rated exposure by member
  class, operating expenditure and vehicles for seven classes (14); the chart's named parts (5); two files (2). 39.
- **Sources, one line each.** `guard.py mechanisms --objective descriptive-distribution` (26 builds): none fits a
  size distribution through an observation process; task254 v2 (spent at stage 2) cut a time-to-event distribution
  censored by a lock date, differentiated on the card; task139 (the other actuarial claims-frequency-severity card in
  the last twelve) read a nurse intervention per assigned intake, a causal design; task185 converted a station's
  instrument change for a heat cover. `layer2-rigor-patterns.md` has no actuarial patterns, so the family comes from
  `two-layer-task-design.md` ("the data's real structure such as censoring"); the pattern is this build's own. The
  seed DA05 gave the number only.
- **Forward facing:** the call is the 2027 retention, a window not yet open; the curve is fitted to closed years and
  brought to 2027 cost with the actuary's projected index.

### Default path

1. Read the current administrator's loss run (csv) and the legacy administrator's closed-claim archive (xlsx, one
   sheet per accident year) and keep every liability occurrence of accident years 2014 to 2021: 1,071 (8 still open).
2. Take each occurrence's ground-up cost as its member's deductible plus the pool's payments and reserves (damages and
   defence) and bring cost, deductible and retention to 2027 cost with the claim cost index.
3. Fit the lognormal by maximum likelihood to the 1,071 costs at 2027 cost, each truncated at its deductible and the
   25 at the retention censored there: log mean 8.09, log standard deviation 1.86.
4. Expected 2027 occurrences above each quoted attachment: the actuary's 432.7 above $25,000 (Exhibit 6's total)
   times the fitted probability of exceeding the attachment over that of exceeding $25,000.
5. Take the lowest quoted attachment where that is one or fewer.

Ends on: $2.0 million
Golden: $4.0 million

### Stump sentence

The default path fits one lognormal, deductible-truncated and retention-censored at 2027 cost, to all 1,071
occurrences of 2014 to 2021 and carries Exhibit 6's 432.7 occurrences above $25,000 by that curve, which ends on $2.0
million (0.9 expected 2027 occurrences above it), because law enforcement liability, under a third of the record and
every one of the 25 occurrences that reached the retention, runs a far longer tail than the other four coverage parts
and one curve takes its shape from the 757 others; giving law enforcement its own log mean but one spread still ends
on $2.5 million; fitting the two groups apart and carrying the actuary's 85.1 law enforcement and 347.6 other
occurrences by their own curves files $4.0 million (1.2 above $3.0 million, 0.8 above $4.0 million).

### Three rules

- **Task type:** claims-frequency-severity in Actuarial Science & Insurance, serving Descriptive & Distribution
  Analysis: the call reads the tail of the ground-up severity distribution at each quoted attachment.
- **Domain test:** the deciding quantity is the ground-up severity tail at each attachment, priced the way excess
  layers are priced: a severity per coverage whose losses differ in kind (law enforcement civil-rights and use-of-force
  suits against general, auto, public officials' and employment practices claims), each fitted through the record's
  deductible floor and retention ceiling and weighted by the actuary's frequency for that coverage on its own exposure.
- **Swap:** with a hospital's nouns ("how much of each patient's stay the ward funds before the regional fund pays")
  there is no coverage whose verdicts run a longer tail, no deductible floor, no retention ceiling and no quoted
  attachment to choose, so the estimator and the decision stop making sense.
- **Layer 1:** the legacy administrator's closed-claim archive (one sheet per accident year, title blocks, dates as
  text, currency formats) written by the system the pool left on 1 July 2020; the current administrator's loss run,
  claims open at the conversion carried under new numbers with the legacy number kept; coverage codes in two
  vocabularies (GL, AL, LEL, POL, EPL against GENL, AUTO, LAWE, PUBO, EMPL); member codes against member numbers;
  costs in each year's own dollars beside the actuary's index; for the asks, the vehicle schedule kept as a log since
  its opening load and a consortium's bulk load, and declarations taken online and on paper. Nothing is placed to be
  caught; every main-path item leaves the call and the components where they are when mishandled (asserted).
- **Layer 2:** estimation_fit: the severity of a pool whose occurrences come from two coverage kinds with different
  tails is a mixture, and one lognormal fitted through the record's truncation and censoring is shaped by the
  short-tailed majority; the record rejects one curve (twice the log likelihood difference 158.2 on two degrees of
  freedom) and one spread (28.8 on one); each group fitted apart and carried by the actuary's own projection for it
  moves the expected count above $4.0 million from 0.2 to 0.8 and the call from $2.0 million to $4.0 million.
- **Decisive step:** fitting the law enforcement occurrences and the other parts' occurrences apart through the
  record's own observation process and adding each group's projected 2027 occurrences above $25,000 carried by its
  own tail ratio, rather than one curve over the pooled record carried by the total.
- **Not semantics:** every field reads plainly (the coverage code, the deductible, the pool's payments and reserves,
  the status, the retention in the memorandum, the two projections in Exhibit 6), and a solver who reads them all,
  censors the capped occurrences and truncates at each deductible still files $2.0 million with one curve: no field,
  code or definition says whether the coverages share a severity.
- **Not rule application:** the policy files the family (lognormal), the estimator (maximum likelihood), the record,
  the window, the cost level, the expected-number formula from the actuary's count above $25,000, and the line; it
  files no curve count, no grouping and no likelihood, and executing every filed rule with one curve files $2.0
  million; testing whether the coverages share a severity and carrying each group's frequency by its own tail is the
  step no rule performs.
- **Analyst test:** a strong analyst who cleans both loss runs, reads every field and rule, brings the record to 2027
  cost and fits the lognormal by maximum likelihood with each deductible as truncation and the capped occurrences
  censored at the retention, then carries Exhibit 6's 432.7 by that one curve, files $2.0 million (0.9 above it);
  both portal responses to loop 1 and both call-only probes on this pack (p255a, p255b) took that route.
- **Estimand:** the trustees' risk financing policy fixes severity as the distribution of what a member's liability
  occurrence of the coverage year costs from its first dollar, damages and defence together, at 2027 cost, over all
  the members' liability occurrences, estimated by maximum likelihood from the pool's claims record for accident
  years 2014 to 2021, and the expected number above an attachment as the actuary's expected number above $25,000 times
  the estimated probability that an occurrence above $25,000 costs more than the attachment; the retention is the
  lowest quoted attachment whose expected 2027 number above it is one or fewer (risk_financing_policy_2026.pdf).
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states an attachment, a fit or a
  count; the loss runs are the administrators' own records and every row is a real occurrence; the actuary's
  exhibit projects frequency by coverage group because law enforcement exposure is police payroll, the way such
  studies are laid out, and states no severity.
- **No certified replay:** no certified or published figure is reproduced by any method: the actuary's exhibits file
  the index and the counts above $25,000 and no severity parameter, count above any other amount or layer cost.
- **Lesson:** a pool's liability severity is two curves, not one: the coverage whose suits run longest is a minority
  of the record and the whole of the tail, and one curve fitted through the record's floor and ceiling is shaped by
  the many short claims, thinning the tail exactly where an excess attachment sits.

### Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 to R2, one curve without the full observation process ($2.0m) | the memorandum's tender and excess sentences | capped costs sit at $500,000 or $1,000,000 | the textbook truncated and censored fit fixes these | none | no | no | readable |
| R3, one curve, truncated and censored ($2.0m) | none names a curve count | the coverage column sits on every row | the reflex itself: both portal responses and both probes stop here | none | no | a likelihood | readable |
| Shift, own log mean, one spread ($2.5m) | none | the coverage column | a regression reflex once coverage is seen to matter | none | no | no | silent |
| G (decisive), the groups fitted apart, each carried by its own projection ($4.0m) | no sentence names a grouping, a mixture or separate curves; policy 3.1 says the actuary projects the two groups on their own exposures, which is how frequency studies are laid out | Exhibit 6 has two rows and a total; the loss runs carry a coverage code | not a reflex: the reflexes fit one curve to the record and carry the total | nothing scores a fit: no severity parameter, no count above any amount, no excess experience ships | the battery sees no defect | a likelihood per group and a weighted sum | silent |

### Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | attachment | from the first dollar, inclusive of the member's deductible | excess of the member's deductible | each count read above attachment plus deductible | policy 2.3 and the indications: attachments are from the first dollar, inclusive of the member's deductible |
| SF2 | occurrence | one row of either loss run | one claimant | same call | same call: both loss runs are one row per occurrence |
| SF3 | cost | the deductible plus the pool's paid and reserved damages and defence | damages only ($1.0m) | $1.0 million | policy 2.2: damages and defence costs together |
| SF4 | 2027 cost | the 2027 index over the accident year's | no trend ($2.5m) | $2.5 million | policy 4.2 names the index and the ratio |
| SF5 | the record | the legacy archive and the current run together | the current run alone (no attachment passes) | none | the extract notes: the archive holds the claims closed before 1 July 2020, the current run every claim handled since |
| SF6 | the record of 2014 to 2021 | the 1,071 files of those years, open and closed | the closed files of every accident year ($2.5m) | $2.5 million | policy 4.2 names the years |
| SF7 | expected number above an attachment | Exhibit 6's expected number above $25,000 times the estimated probability that an occurrence above $25,000 exceeds the attachment | counts read off the record | not a count of 2027 occurrences | policy 4.3 |
| SF8 | one or fewer | at most 1.0, inclusive | strictly under 1.0 | same call: 1.20 and 0.82 at $3.0m and $4.0m | same call |
| SF9 | thresholds' cost level | each deductible and retention at 2027 cost with the occurrence | the likelihood in each year's own dollars, the log mean moving with the index | same fit to the fourth decimal in both groups (asserted) | same call; thresholds left nominal against trended costs mixes two cost levels in one likelihood (a rung, $5.0m) |
| SF10 | the deductible of an occurrence | the one on the loss-run row, in force on the date of loss | the member's current deductible | not on any row | the memorandum: the deductible in force on the date of the occurrence applies; the loss runs carry it |
| SF11 | the quoted attachments | the seven in the broker's indications | an interpolated attachment | not quoted | policy 5.1: the lowest attachment quoted for the year |
| SF12 | rounding | counts unrounded until compared, shown to one decimal; premiums rounded once at the total | rounded before comparing | same call; every count, golden and five-part, at least 0.2 of the last place from its edge; every layer loss at least $20,000 from its edge | same call |
| SF13 | the anchors | Exhibit 6's 85.1 and 347.6 above $25,000 from the first dollar at 2027 cost, total 432.7 | at each year's cost | not the actuary's figures | Exhibit 6 states its counts at 2027 cost from the first dollar |
| SF14 | maximum likelihood | the maximum over each lognormal's two parameters, one optimum | a local optimum | same call | same call: five starting points reach one optimum in each group (asserted) |
| SF15 | an open file's recorded cost | the deductible plus what the pool has paid and still reserves | the deductible plus payments to date | same record (asserted): every open file of 2014 to 2021 is a law enforcement suit with its layer paid and nothing reserved | same call and same counts |
| SF16 | a vehicle on the schedule (the asks) | one vehicle by its VIN, or its serial without a VIN, on the schedule at 30 September 2026 by effective date, a consortium vehicle by its FMC- record | the last row across every number the vehicle holds, any number in force (6,387), every unit number in force (8,233) | other premiums and class vehicles | the extract notes file a vehicle's identity and how the consortium's numbers relate to the earlier ones |
| SF17 | "severity is modelled as lognormal" | a lognormal for each group the record separates | one lognormal for every occurrence ($2.0m) | $2.0 million | the record: one curve is rejected at twice the log likelihood difference 158.2 on two degrees of freedom and one spread at 28.8 on one (asserted, the design forcing the method); the policy files the family, never one curve (4.2, asserted) |
| SF18 | the groups | law enforcement liability and the other four parts, Exhibit 6's two projections | a curve per coverage part, the other four weighted by their share of the record above $25,000 | same call, the same seven counts at one decimal and the same seven layer losses to the hundred thousand (asserted) | same call |

### Ladder

| Rung | Likelihood | Expected 2027 occurrences above $3.0m and $4.0m | Call |
|---|---|---|---|
| R0 | one curve, the recorded costs as a complete sample | 0.15, 0.05 | $2.0 million (0.67) |
| R1 | one curve, the capped censored, no truncation | 0.20, 0.07 | $2.0 million (0.84) |
| R2 | one curve, each deductible as truncation, caps read as exact | 0.24, 0.12 | $2.0 million (0.61) |
| R3 | one curve, truncation and censoring at 2027 cost (the reflex, both portal responses, both probes) | 0.39, 0.21 | $2.0 million (0.89) |
| Shift | law enforcement's own log mean, one spread | 0.56, 0.31 | $2.5 million (0.79) |
| G_closed | the groups apart, the 8 open suits set aside | 0.75, 0.48 | $2.5 million (0.99) |
| G | the groups apart on every file, each carried by its own projection | 1.20, 0.82 | $4.0 million |

- **Position:** the golden is the sixth of seven attachments; the reflex takes the third. Every correction short of the
  decisive one stays at or below $2.5 million.
- **Margins:** at $4.0 million 0.82 (1.22x under the line); at $3.0 million, the runner-up, 1.20 (1.20x over it).
- **Worth:** the decisive move (R3 to G) multiplies the expected count above $4.0 million by 3.8 (0.22 to 0.82) and
  moves the call two attachments.
- **Convergence asserted:** the same likelihoods in each accident year's dollars give the same two fits; a curve per
  coverage part with the other parts weighted by their share above $25,000 gives every count at one decimal; a
  common floor at $215,600 files $4.0 million; an open suit read at its payments or at payments and reserves is the
  same record.
- **Flip:** with the other parts' projection held, $3.0 million would pass if Exhibit 6's law enforcement count were
  71.0 or lower; $4.0 million fails only above 103.2.

### Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | severity over every members' liability occurrence; the fit's population the record of the 2014 to 2021 occurrences | filed literally, policy 4.1 and 4.2 |
| 2 | Unit of account | the occurrence | policy and indications per occurrence; one loss-run row each (SF2) |
| 3 | Attribution window | accident year by date of occurrence | the memorandum's occurrence basis; dates on every row |
| 4 | As-of dating | the loss runs at 30 September 2026 | C1: every uncapped fit occurrence closed by 30 June 2026; the 8 open suits have the layer paid (SF15) |
| 5 | Version basis | the record as it stands at the evaluation | C1: closed values are final; the archive was cut at conversion |
| 6 | Denominator | the probability above $25,000 in each group | policy 4.3 and Exhibit 6 |
| 7 | Weighting | one observation per occurrence; groups weighted by Exhibit 6 | maximum likelihood filed (policy 4.2); Exhibit 6 |
| 8 | Window length | eight accident years, 2014 to 2021 | policy 4.2 |
| 9 | Boundary inclusivity | "one or fewer" inclusive; a cost at the retention reached it | C1: no count within 0.18 of 1.0; no uncapped cost within $10 of a retention |
| 10 | Rounding path | counts unrounded until compared; premiums once at the total | SF12, same call |
| 11 | Tie-break | none: one lowest passing attachment | by construction |
| 12 | Maturity and censoring | censoring at the retention is the record's structure; the 8 open suits with the layer paid are censored there | the memorandum's facts |
| 13 | Order of operations | thresholds and costs at one cost level before the fit | C1: the accident-year-dollar likelihood gives the same fits (asserted) |
| 14 | Row order | none | C1: each fit is the same under shuffled rows (asserted) |
| 15 | Duplicate resolution | a converted claim appears once, in the current run, its legacy number kept | C1: no claim number in both runs (asserted) |
| 16 | Identity normalisation | member codes against numbers (not needed for the call); coverage codes in two vocabularies (the notes map them); VINs and serials for the asks | the extract notes; ask device D7 |
| 17 | Netting against gross | no recovery on any fit occurrence | C1: asserted none |
| 18 | Dimensional units | dollars; the index a ratio | the actuary's exhibit (2014 = 100.0) |
| 19 | Code and status semantics | "CL" in the archive, "Closed" or "Open" in the current run; five coverage parts, law enforcement one of them | the extract notes |
| 20 | Integerisation | none; vehicles are whole units | by construction |
| 21 | Clause scope | 4.2's window for severity, 4.3's anchor for frequency, 5.1 for the attachment | filed per clause |
| 22 | Forward window contents | 2027's counts above $25,000 and its index value | the actuary's exhibits file both |

### Literal reader

Executed word for word, the policy fixes severity as the distribution of all the members' liability occurrences from
the first dollar at 2027 cost (4.1), modelled as lognormal and estimated by maximum likelihood from the pool's claims
record for accident years 2014 to 2021 (4.2), and the expected number above an attachment as the actuary's expected
number above $25,000 times the estimated probability that an occurrence above $25,000 exceeds it (4.3); Exhibit 6
gives that expected number as 85.1 law enforcement and 347.6 other occurrences, 432.7 in all. The record of those
years holds 1,071 files, 8 of them open law enforcement suits whose payments have reached the retention; the
memorandum files how the record came to exist (truncation at the deductible in force, nothing above the retention).
The text files the family and the estimator and is silent on whether one lognormal or one per coverage group; the
record separates the readings (one curve rejected at 158.2 on two degrees of freedom, one spread at 28.8 on one), so
the design forces the groups, and their literal execution gives $4.0 million. Every other row of the fork table
violates a quoted sentence or converges on $4.0 million; the easy answers ($2.0 million, $2.5 million) come from a
model the record rejects, not from another reading.

### Oracles

- The actuary's 85.1 and 347.6 occurrences above $25,000: inputs of every rung (the reflex uses their total); they tie
  to nothing.
- The claim cost index: an input; it ties to nothing.
- The liability triangles (distractor): the pool's paid and incurred, net of deductibles and limited to its
  retention, by accident year and evaluation, with the counts tendered and closed; they carry no coverage split, no
  ground-up cost, no count above any amount and no severity parameter.
- The member deductible history (distractor): agrees with the deductible on every loss-run row; it scores no fit.
- The open accident years 2022 to 2026 in the current run: outside the policy's window and immature; the pack carries
  no development pattern to bring them to ultimate, so they score no fit.
- The ask layer: the declarations' department payroll is the benign twin of the repeated expenditure; the police
  department payroll in Exhibit 6 ties to the declarations' Police lines; no 2026 rated exposure, premium or
  expiring programme ships (Tried and rejected).

### Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, each quoted layer's expected 2027 losses | 7 | the cost side of each attachment the call chooses among | the board sets each layer's expected losses beside its quote | the construction: each layer's expected losses carry each group's projection by its own severity between the attachment and the attachment plus the $10,000,000 limit | the limit (an unlimited excess cost is ruled out by the indications' limit) | the golden fit, the indications' limit | the pooled curve 3.3, 2.1, 1.5, 1.1, 0.8, 0.6, 0.4 million; the one spread and the groups on the closed files lower at every attachment; the answer | an excess layer's expected losses set beside its quote |
| C, the policy's test per attachment and the chart | 7 counts (in the call's question) and 5 chart parts | the construction | the call's own table | none | none | the golden fit | R3's values (3.3, 1.6, 0.9, 0.6, 0.4, 0.2, 0.1) and the one spread's (3.9, 2.0, 1.2, 0.8, 0.6, 0.3, 0.2) | the actuary's exhibit layout |

- **Loop 2 ask history:** the exposure asks (premiums by attachment, expenditure and vehicles by class) were solved to
  the dollar by both loop 1 portal responses and, after their devices were re-sited (D9 a member leaving on 31
  December 2026, D10 re-declarations on adopted budgets, D11 vehicles moved between members), by both loop 2 readers
  (21 of 21 figures each, 75 per cent of the ask figures). Exposure arithmetic does not hold against a careful
  reader, so the graded asks follow the severity construction (the ledger's lesson that decoupled asks pay only
  while their leakage is under a half). The declarations and the schedule log ship as distractors with D9 to D11 in
  them; the actuary's payroll ties to the 2027 members' last declarations.
- **Main population zero-counts:** no ask reads a file the call does not.
- **Hazard table:** the limit moves every layer loss; nothing else.
- **Referee:** none; the indications state the limit.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A layer losses at seven attachments | the golden's construction when the call lands | right | outside |
| C counts and chart | the golden's construction when the call lands | right | outside |
| A layer losses (mirror) | the pooled curve | 3.3 million against 8.3 at $1.0 million, off at every attachment | miss |
| C counts (mirror) | the pooled curve | off at every attachment | miss |

Measured by: task255/generator/pair.py (the readers' measured path, off the call, run on the built records).
Mirror leakage: 0 per cent of the ask weight (every layer loss and count of the pooled curve and the one spread
misses at the graded rounding, asserted).
Pair ceiling: 56.0 (the cracker at 100.0 on the call and every ask, the mirror at 12.0).

### Build record

- Generator: `world.py`, `analysis.py`, `records.py`, `docs.py`, `golden.py`, `checks.py`, `verify.py`, `build.py`,
  `postprocess.py`; `python3 task255/generator/build.py` builds the pack, the goldens, `metadata.json` and
  `generator/figures.json`, runs the checks and the independent verifier, rebuilds into scratch for the byte
  comparison and cuts `target.zip`.
- Pack: 12 files in 4 formats; the vehicle schedule log 43,855 rows; the legacy archive 467 occurrences in six
  accident-year sheets; the current loss run with 353 occurrences in the fit's years among all its open and closed
  occurrences; distractors the member deductible history and the actuary's triangles.
- Gates: 196 assertions with the three-rules block and SF1 to SF14; the verifier recomputes the fit (log mean 10.1769,
  log standard deviation 1.7102), the call, every count, the premiums and the class exposure from `target/` alone with
  its own parser and optimiser; two builds byte-identical; figures_check 88 figures; precut 49 checks; voice-check
  PASS; scrub audit clean on target and golden; leak.py REVIEW (no LEAK: the quoted attachments are declared stated
  inputs; the policy's own vocabulary; 26 schedule changes keyed before they take effect, allow-listed); guard
  surface 0 promoted; heart WARN (Gate G overuse, answered in the Draw).

- Loop 2 (2026-10-26, after the portal's FAILED_TO_STUMP). World: each occurrence draws its coverage part first and
  its cost from that part's severity (law enforcement lognormal 8.6 and 2.45 at 2027 cost, the other parts 9.2 and
  1.35), 2,000 ground-up occurrences a year at the 2027 membership, the retention $500,000 for 2014 to 2017 and
  $1,000,000 from 2018; Exhibit 6 projects 85.0 law enforcement and 375.0 other occurrences above $25,000 on police and
  other payroll. Record: 1,071 occurrences (610 legacy, 461 current), 314 law enforcement with all 25 capped and the 8
  open suits, 757 others. Asks re-sited: D9 (a water-sewer district declared and then gave notice to leave on 31
  December 2026), D10 (eleven re-declarations on adopted budgets, the first in every class a cut), D11 (eight vehicles
  sold between members inside the pool, keyed as a change of member). Counts graded to one decimal (a curve per
  coverage part reproduces every count there; at two decimals it parted at $1.0 million). 281 assertions; the
  independent verifier fits both groups from target/ alone (8.5158 and 2.3713; 9.8851 and 1.1352) and reprices the
  exposure; two builds byte-identical; figures_check 93; precut 51; leak.py REVIEW; heart WARN; surface PASS;
  pair.py ceiling 35.4. Then, after stage 4's readers solved every exposure figure, the anchors moved to 85.1 and
  347.6, the premium ask gave way to each quoted layer's expected losses (a downstream ask), the quotes were
  rescaled by one market factor, same-day occurrences were separated; 282 assertions, pair.py ceiling 56.0.

### Judge record

- Pass 1 (stage 4): DETERMINISTIC, APPROVE. The isolated thread recomputed the record (820 occurrences, 108 at the
  retention), the fit (10.1769, 1.7102), the seven counts and premiums and the class exposure from the bundle alone,
  and tested the competing estimators: censoring without truncation ($2.5 million) and truncation without censoring
  ($2.0 million) each conflict with a memorandum sentence (2.3, 3.2); thresholds left nominal with costs trended
  still give $4.0 million; an untrended fit is inconsistent with the policy's record brought to 2027 cost. Ask-only
  fork: vehicles keyed on entered_date (5,602 on the judged pack) against effective_date, closed by the extract
  notes' definition. Gate G statistical_rigor, analytical_non_defect, no surface read, no sole data defect; Gate H
  domain pass, layers pass, decisive step analytical. Cosmetic: the class rows rounded one by one foot to a thousand
  above the total (the golden's notes say so; the write-up's total line now says it is rounded from the exact sum).
- After the judge: the leak reader's realism tells were fixed in the generator (member numbers in joining order, each
  unit's own depreciation with some values held, slower closings for claims tendered in 2019 to 2022, a market's
  uneven rate ladder, the log note's entry date; the consortium is now the largest fleets in each class, loaded
  4 March 2024). A second read's tells were fixed in the same way: a member admitted in 2024 had schedule rows dated
  from 2022 (now from its admission), unit numbers ran in member blocks (now in the order units were keyed),
  revaluations followed one formula (now the class's depreciation, steeper in a unit's first years, held at some
  renewals, an appraisal at a few, keyed in one batch per member), the rate ladder was one smooth curve (the auto
  rate now stops at the market's minimum above $3.5 million) and the triangles closed at the same pace every year
  (each accident year now has its own pace). The fit, the call and every count are the judged ones to the last
  digit; the ask figures and the archive split (467 and 353) moved and were rechecked by the 196 assertions and the
  independent verifier. No re-judge: the disposition was APPROVE and no estimand, rule or sentence the call reads
  changed.

- Loop 1 (2026-10-13, the author's request for a second layer). Stage 3: the world lets an occurrence past the
  retention run a suit about three years longer, the pool's layer paid by about three and a half years after tender
  and its file left open until the excess insurer closes its own; no clamp closes those suits by mid-2026, the
  uncapped files of 2014 to 2021 still close by then. 20 open suits in the window (8 converted from the legacy
  administrator, 18 from 2019 to 2021), every one with the layer paid and nothing reserved; the legacy archive now
  421 occurrences, the current run 399 of the window's. Policy 4.2 names the window without closure. The golden fit,
  call, counts, premiums and class exposure are the loop-0 values to the last digit; the closed files alone file $3.0
  million. 202 assertions (the analyst test now runs the closed-file construction on the clean truth, R3 at $3.0
  million, and the golden only with the open suits in); the verifier reads open files at payments and reserves and
  finds the twenty; two builds byte-identical; figures_check 93 figures.

- Loop 1, stage 4. Leak reader, first read: no decisive-step sentence; it quoted the memorandum's "once the pool's
  share is paid, the pool's administrator closes the pool's file on the occurrence", which the twenty open suits
  contradict: the clause is cut (the memorandum now says only that the excess insurer's payments are not entered),
  and the extract notes' "The documents beside them are as issued" reads "Filed with them as issued". Second read: no
  decisive-step sentence, no contradiction, nothing names the open suits. Judge pass 1 (one isolated thread):
  NOT_DETERMINISTIC on the asks only, the main call forced and reproduced (820 files, 20 open, 108 at the retention,
  10.18 and 1.71, $4.0 million; closed files alone $3.0 million): the vehicle count behind the premiums and the class
  vehicles turned on a rule no file stated (the consortium's FMC- numbers against the members' earlier numbers, which
  still take the revaluations). Fixed in the generator: the extract notes file a vehicle's identity (its VIN, or its
  serial without one) and how the consortium's numbers relate to the earlier ones (SF16, asserted); no figure moved.
  Third read (on the fix): no decisive-step sentence; it asked whether the unit count is by effective or entered
  date, which the notes file (effective_date is when the change applies to coverage). Judge pass 2 (the one re-judge):
  DETERMINISTIC, APPROVE; every figure reproduced, the premiums and the class figures included; the competing fits
  (closed files alone, the open suits read as exact, no truncation, censoring alone, no trend) all miss; entered dates
  for the vehicles would move each premium by about $825, against the notes' effective-date definition; Gate G
  analytical, Gate H domain, layers and decisive step pass.

### Leak record

- leak.py REVIEW, no LEAK: the policy carries the call's own nouns (retention, attachment, occurrence), harmless; four
  documents use ordinary domain words (record, deductible, likelihood, closed), none names a truncation or a
  censoring (asserted); 25 schedule changes keyed before they take effect, allow-listed in metadata.json.
- Reader 1 (fresh copy of prompt.txt and target/): no decisive-step sentence (the memorandum's tender and excess
  sentences make the structure discoverable, neither says to adjust for it); no ranking file; no analyst-only file;
  no answer-like figure. Question 5: it read policy 4.2 as leaving the likelihood open and computed the three
  likelihoods to the golden's own figures ($2.0 million, $2.5 million, $4.0 million); ruled: the curve of 4.1 is over
  all occurrences at their full cost and the memorandum files how the record arises, so the record's likelihood is
  the truncated and censored one (the judge reached the same reading on its own). Question 6: an analytical choice.
- Reader 2 (after the realism repairs, fresh copy): no decisive-step sentence; the extract notes describe files and
  name no pitfall. Its tells were repaired as the judge record says; two did not hold on checking (every cleaned VIN
  is free of I, O and Q and carries its model year in the tenth place) and three are the record as such a pool keeps
  it (the pool's share stopping at the retention less the deductible, a member's deductible changing often, a bulk
  load keyed on one day).

### Pre-ship check

- Call: keep the first $4,000,000 of each 2027 liability occurrence (the $4.0 million quoted attachment), 0.74
  expected 2027 occurrences above it and 1.25 above $3.0 million; curve log mean 10.18, log standard deviation 1.71
  on the 820 files of 2014 to 2021 (800 closed, 20 open suits with the layer paid), 108 stopped at the retention.
- Default path: the complete-sample fit to the closed files files $2.0 million; censoring alone $2.5 million;
  truncation alone $2.0 million; truncation and censoring at 2027 cost on the closed files $3.0 million; thresholds
  left nominal $4.0 million (convergent call); a common floor at $215,600 $4.0 million.
- 10/10 rules re-read against the built pack: the deciding quantity is the ground-up severity tail fitted through the
  record's own observation process (the field's construction); the mess (two administrators, converted numbers,
  member codes, text dates, the schedule's bulk load, the declarations' repeated totals) leaves the call and the
  components where they are when mishandled (asserted); the decisive step is analytical (the likelihood of a
  truncated, censored record over every file, the open suits being the censored observations a closed-file fit
  drops); no planted figure, no withheld rule, nothing flips on reading a field.
- Gates: 204 assertions with the three-rules block and SF1 to SF16; the independent verifier from target/ alone; two
  builds byte-identical; figures_check 93 figures; precut 49 checks; voice-check PASS; leak.py REVIEW (no LEAK); guard
  heart BLOCK in task-number order on task229 v3 and task231, both registered after this build's draw (06:41 and 17:18
  against 00:38 on 13 October), WARN in registration order (Gate G overuse, answered in the Draw).
- Deliverables: retention_2027.xlsx (the test and premium at seven attachments, the rated exposure by class, notes)
  and attachment_test_2027.png; target.zip from the final rebuild, 12 files.
- Card current: answer, spine rows, stump and driver at the built values.

## Tried and rejected

- DA05's seed world (a hospital trust's weekend day-surgery team and 52-week waits): no Descriptive task type in the
  client taxonomy fits that world's decision, so the number was redrawn inside Descriptive with a new world.
- A competing-risk design (time to resolution with withdrawals as non-returners): task134 v1 spent Kaplan-Meier with
  competing exits as the golden; rejected at the draw.
- High member deductibles across the board: the complete-sample fit and the truncated fit cancelled toward one
  attachment; rejected in the feasibility search.
- A $500,000 then $1,000,000 retention history: fewer capped occurrences and a better-seen tail, but the complete
  fit and the censoring-only fit crossed the line too close to the golden to sit on other attachments; the $250,000
  then $500,000 history kept (feasibility search, not rebuilt).
- A line of two expected occurrences a year: the censoring-only fit crossed close to the golden and shared its
  attachment in the search; one a year kept.
- An actuary's count anchored above $100,000 or $250,000 (inside the observed range): the tail's sampling error
  barely moved in the search and the nominal-threshold fit split from the golden onto $3.0 million; $25,000 kept.
- A ten-year window (2012 to 2021): the tail's sampling error fell only a little in the search; eight years kept.
- The legacy archive without the deductible, joined from the effective-dated history: the natural mishandling (the
  member's current deductible) moved the log mean by more than three in the search, not mess-neutral; both loss runs
  carry the deductible on each row and the history ships as a distractor.
- An ask on the open years' large occurrences (the underwriters' large-loss listing): immature counts set beside a
  fitted tail can bless the thinner curves, a validated decoy; dropped.
- Members declaring in thousands of dollars as the expenditure device: a thousandfold value shows on any sort;
  dropped for the repeated member figure.
- The expiring 2026 programme summary as a distractor: its premium and rated exposure would refute the repeated
  expenditure at a glance (an oracle for the ask); not shipped.
- The loop-0 design as the final rung: every occurrence of 2014 to 2021 forced closed by mid-2026 (the window named
  "the latest eight accident years in which every occurrence has closed"), so the likelihood of the record decided
  alone; at the author's request for a second layer the clamp was lifted for the suits past the retention, which
  the excess insurer goes on defending, and the closed-file construction became R3 ($3.0 million).
- Open suits carrying a case reserve to the rest of the pool's layer: reading them at payments to date as exact costs
  files $3.0 million, but censoring them at their payments (the ultimate is at least what is paid) gives the golden
  call with other counts at two decimals, a fork on the seven graded counts; the window's open suits have their
  layer paid in full (a suit past the retention has used the layer within about three and a half years of tender),
  so every reading of an open file is the same record.
- A window extended to the open years 2022 and 2023 with their reserves developed: the development of individual
  large files from aggregate triangles is the actuary's judgment, several defensible factors and several counts;
  the window kept at 2014 to 2021, where the only open files are the paid-up suits.
- Loop 1 as shipped (portal 2026-10-26, FAILED_TO_STUMP): both responses filed USD 4,000,000 with 0.74 above it and
  the premium to the dollar. The deductible-truncated, retention-censored likelihood is the field's textbook reflex
  for a pool's loss run (readability test 3 fires on R2, R3 and G, recorded silent), and an open suit whose layer is
  paid reads as a censored observation to anyone who has already censored the caps, so the settlement selection
  added no rung. The observation-process likelihood is demoted below the new decisive step.
- Loop 2 prototype with five distinct coverage severities: the per-part fits were unstable (the truncated lognormal
  with a hundred or two rows a part ran its log mean far below the deductibles) and the groupings disagreed on the
  call; rejected for two severity groups, law enforcement against the rest, with the record grown to 2,000 ground-up
  occurrences a year.
- The $250,000 then $500,000 retention history under loop 2: a common spread with a shifted log mean was not rejected
  by the record (twice the log likelihood difference 2 to 14 on one degree of freedom across seeds) and filed another
  call, an open fork; the history raised to $500,000 and $1,000,000 and the record enlarged until it is rejected at
  28.8.
- The prototype anchors 85.5 and 364.3: the counts above $2.5 million and $5.0 million sat within a hundredth of a
  rounding edge; 84.7 and 364.7 kept the call and cleared every count's edge.
- Counts at two decimals under loop 2: a curve per coverage part, the other four weighted by their share of the record
  above $25,000, matched the golden at six attachments and parted at $1.0 million (4.59 against 4.57); counts graded
  to one decimal, the precision the record carries.
- The prototype's loss dates: every occurrence of an accident year drew the same day (a probe noticed it); fixed, no
  fit moved.
- Loop 1's ask layer under loop 2: both portal responses reproduced the $4.0 million premium to the dollar, so the
  repeated-total and consortium devices were solved; re-sited with D9, D10 and D11.
- The anchors 84.7 and 364.7 under the layer-loss ask: the golden and the five-part fit put the $1.0 million layer's
  expected losses either side of a $100,000 edge (8.24 and 8.25 million); 85.0 and 375.0 keep the call, the counts
  and every layer loss in one cell for both, at least 0.23 of the last place from each edge.
- The premium ask beside the layer-loss ask: a careful reader prices the exposure right, so a reader who lands the
  call keeps every ask and the pair ceiling sits at 65; dropped from the prompt, the quotes kept as the layers' terms.
- The loop 1 rate ladder at loop 2's severities: premiums a fifth of the layers' expected losses, a ratio no market
  quotes; one market factor of 7.3 on the ladder puts the expected losses at 58 to 64 per cent of each premium.
- Two same-member, same-day occurrences in the record (thirteen pairs before the fix): a careful reader merges them
  under the memorandum's one-occurrence clause; each member's second occurrence of a day is now dated the next free
  day, no fit moved.
- The anchors 85.0 and 375.0: a stage 4 reader read the two round projections as reverse-engineered; 85.1 and
  347.6 keep the call, every count and every layer loss in its cell (at least 0.2 of the last place from each edge).
- The same unit rate at $4.0 million and $5.0 million (a market minimum): flagged by two readers; the $5.0 million rate
  is now $222.50.

- Architecture 1 as shipped (loop 2): re-rooted 2026-11-01 at the Batch 3 queue reset. The portal's responses filed
  the pool's retention through the truncated and censored likelihood, the field's reflex for a loss run; the liability
  pool's world is closed and the actuarial descriptive cell (claims-frequency-severity) is spent for this slot.
- Draw candidate, actuarial claims-frequency-severity in another world: every stump that cell offers (truncation,
  censoring, maturity, a coverage mix) is the field's reflex, already landed here; dropped.
- Draw candidate, a loyalty programme's segments (segmentation-market-structure): the decisive step reduces to an
  estimation grouping (stumping 1.1c), a reflex or a fork; dropped.
- Draw candidate, television reach from a people-meter panel: the deciding step is the panel's weighting, an
  estimator choice whose textbook form is the reflex; dropped.
- Draw candidate, billboard reach from mobile location pings: the step is identity resolution across devices (data
  semantics) or a capture-recapture estimate (the field's method at the top of the ladder); dropped.
- Interchange walks of 4.0 minutes at Ravelpark and 4.5 at Handelshaven: the fastest and the fewest-change routes
  differed on 54 station pairs and moved five packages' reach a bin (138 riders); lengthened to 9.0 and 8.0 minutes
  (the ring's platforms across the square), every pair now routes the same.
- Commuters between the ring line and the north or west branches: at the peaks a through train to the other ring
  interchange beats the line map's route, a second route model with no record to settle it; those flows set to nil
  and occasional riders' ring trips through Centraal kept out of the peak windows.
- 2,130 habitual riders: Centraal and Oosttak sat 0.16 and 0.14 of a point from a whole-per-cent edge; 2,232 clear
  every package by 0.18 or more.
- The first ask layer (re-cablings entered on the day of the job, three re-tagged halls, statements struck after
  every credit note): the cracker kept about 25 of 28 ask figures, a pair near 77; re-sited to the work-order dating,
  the eight-hall replacement programme and the credit notes after the statements.
- Net revenue to the nearest 100 euros: the credit notes after the statements moved some agency packages by 30 to 60
  euros, inside a bin; graded to the nearest 10 euros, the precision the arithmetic carries.
- A make-good allowance of 1.0 per cent: bookings with short outages fell to zero hours; 0.5 per cent kept.
- The take-down dated from the register's date alone: 00:00 to 00:30 of that date belongs to the previous day's
  opening hours, a half-hour fork per screen; the player's last display report (05:10) dates it.
- Gate numbers drawn one to six at every hall: every hall showed the same gate count; each hall now has its own.
- Sunday staff trips from 06:30: nine check-ins before the metro opened; they start after 07:00.
- The first booking prices: Centraal's revenue sat at 9,105.00 and Oosttak's at 5,985.00, half a bin; nine prices
  moved within two euros.
- The question as "which packages": the shell quota (35 per cent of prompts on file); recast as a whether-question,
  "none" grammatical.
- A golden one-page PDF beside the workbook: the guard's recent window held pdf+xlsx (task138), docx+xlsx (task133)
  and pptx+xlsx (task273), and png+xlsx sits over its corpus quota (21 per cent); the chart ships as an SVG.
- The question as "whether we should sell any package in Tier G": the guard found the form in one of the last two
  prompts (task138); recast as a what-question.
- Round 1's golden (duration read only in the three-minute hours, the clock pattern elsewhere): the per-journey test the
  write-up stated gave other whole per cents for three packages, and the route with the halls' walks moved a fourth;
  replaced by the per-journey test on a record whose every regular trip through Centraal reads cleanly.
- Round 1's make-good dating left open by terms 6.2: two licensed sources (the register's entries and the display
  reports) gave two sets of figures; 6.2 now files the second.
- Round 1's take-down at a register date with no time: the start of the date added half an hour per screen; the
  player now goes dark the evening before.
- Round 1's swaps on 3 to 5 November with nothing to tell a replacement from an addition: the units now share their
  output and the display counts show it; the swaps moved to 2 to 4 November, inside the player log.
- Commuter times spread evenly from 07:00 and 16:00: trips that began before a pattern change and passed Centraal
  after it read differently on the check-in clock; the commute is centred in the peaks and the few trips near a
  change are moved clear of it.
- 2,189 habitual riders: Overstappunten and Oosttak came out at the same rider count; 2,183 kept.
- Architecture 2 (Spoorbeeld Media's Tier G reach on the Ravelmond metro, the weekday-peak through-running read from
  journey durations) spent at its re-judge on bbcaedf8, 2026-11-01: Gate G banned (planted_defect_flip,
  surface_read_rejection), Gate H3 planted (the through-running written in no file), three reach figures not
  reproduced, ask 3 open to several readings, ask 4 inferable; re-rooted as architecture 3 in another client domain.
- Draw candidates for architecture 3: a political-science small-area estimate by multilevel regression and
  poststratification (the field's method would be the golden); activity-space segregation read from mobility traces
  (a route inferred from timings, architecture 2's driver again); nonresponse follow-up weighting of a survey (a
  standardisation reflex the screen reads); an anthropometric size-chart fit (a backdrop under the swap test); kept:
  statin persistence on a register that holds no dose.
- Agreement 2.2 saying the statements covered "the conversations held in the quarter and not cancelled by then": the
  sentence filed the device's handling (the pin test); cut to when statements are drawn and paid.
- Personal numbers replaced at fourteen practices only: two practices' counts carried no device; every practice now
  has one to three.
- Later cancellations at five pharmacies: three pharmacies' figures equalled their statements' sum; every pharmacy now
  has some.
- Hospital prescribers on new users' later dispensings: dropping hospital rows (a filter to practice prescriptions)
  moved eleven shares; hospital rows now sit only on long-standing users' dispensings, in the old system's months and
  in 2026 (never a person's last of 2026).
- The old system's day-month-year dates running to December 2024: dropping those rows made 105 long-standing users
  read as new; the old system now ends in June 2024 and the extract reaches back to January 2024, outside every
  lookback.
- No patient starting a statin outside the cohort window: the register read as built around the window; starters from
  November 2024 to June 2025 and during 2026 added on their own stream.
- Two people sharing a birth date and sex whose dispensings never overlap: they read as one person under two numbers;
  the later one's birth date is redrawn.
- A DDD-per-pack or dose column in the product list: it hands the reflex a column; the list carries strength and pack
  size only.
- Ask A to the nearest 10 kroner: one pharmacy's figure sat a krone from a bin edge; whole kroner, the precision the
  arithmetic carries.
- Round 1: continuing users with the replaced numbers' link left in no file (Gate C: sex and birth date alone gave 825
  coincidental pairs, and the linked count rested on unfiled tests); the link now ships in the CPR person table and
  3.3 files the WHAT, which spends the device, so the pilot settlement moved to quarterly figures with a later
  cancellation in every pharmacy-quarter to carry the ask layer.
- Round 1: cancellations entered up to 8 February 2027, after the programme's adoption on 26 January; the log now
  closes on 20 January.
- Round 1: the published town series drawn as independent noise (130.3, 85.7, 108, 131.9 at one town); each town now
  keeps its level with a small seasonal swing.
