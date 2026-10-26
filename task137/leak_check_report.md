# leak check, task137

**Verdict: REVIEW.** 12 files read, 26 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: records, arrest, decisive, architecture, demand, golden, deposit, landed, population, booked, special, stations, recorded, second, january, registered, maturity, another, detainee, record, months, deposits, service, agency, programme

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `custody_demand_model_v2.pdf`: \bthe model\b x3: ...ustody Services Planning, Force Headquarters, Wendle Cross. 1 Purpose The model gives each custody suite a planning figure: the detentions the suite...

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `custody_demand_model_v2.pdf`: golden figure 109 appears: ...ields 7,287 7,180 1.015 Wendle Cross 7,829 8,109 0.966 Every suite came within 4 per cent. Versio...
- **REVIEW** `tanner_street_hub_planning_brief.docx`: carries 7 of 8 distinctive words of the committed call: 'Calderwick Police should give the Tanner Street custody hub a planning figure of 4,000 detentions for 2027-28.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `custody_demand_model_v2.pdf`: 6 of 25 stump-paragraph terms appear (records, arrest, demand, record, service, programme); read whether the document names the move
- **REVIEW** `tanner_street_hub_planning_brief.docx`: 8 of 25 stump-paragraph terms appear (records, arrest, demand, population, booked, record); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `bank-holidays.json`: 2 ISO dates after 2026-10-26, e.g. 2026-12-25, 2026-12-28

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read (stage 4, architecture 3, on d1d38e72, 2026-10-26)

Two isolated scored readers, each on its own fresh copy of `prompt.txt` and `target/`, briefed with the emitted keys.
Architecture 1's read (Kaimai Building Society, round 2), which leak.py had carried across, is removed: it read
another world's pack.

### Reader A (Sonnet, medium)

score_reader (`--call-key call.planning_figure`): call figures 1 of 1 hit (4,000); ask figures 5 of 21 hit
(23.8 per cent), the five being the chart's financial years (3,472, 3,734, 3,615, 3,680, 3,732); 0 of the 16 remand and
assessment figures (remand cell hours 4,077, 2,512, 7,422, 5,298 and over 24 hours 165, 96, 281, 228, the files'
own detentions with the co-defendants left out; assessments 1,146 and 1,426, 558 and 714, 1,217 and 1,619, 1,469 and
1,974, the handover lines joined with the suites as labelled). FAIL: the reader landed the call (exit 1).

1. Decisive step: custody_suite_allocation_2027.xlsx, Notes sheet, item 2: "A detainee is taken to the custody suite that serves the ward where the arrest was made, whichever force or agency the arresting officer belongs to, and the custody officer there decides whether to authorise detention." Together with the arrests file description in the brief ("one row per arrest by a Calderwick Police officer"). The step is noticing that bookings include other agencies' arrests (British Transport Police at Calderwick station, Abbey Fields) which the arrest file does not hold.
2. Nothing ranks candidates for this question. custody_demand_model_v2.pdf is the nearest: "A suite's demand is the people arrested in the wards it serves" with a validation table of forecast against records. It scores a method, not the hub figure.
3. lsoa21_to_ward_lookup.csv exists only to map street-crime LSOAs to wards. (Quote: "2021 LSOAs to the wards they sit in (best fit).")
4. The validation table in the PDF ("Every suite came within 4 per cent.") reads as an endorsement of the cube-root carry-forward method. No single figure reads as the answer.
5. PDF 2.3: "The ward's arrests in the latest full year are carried forward at its average annual change over the three years to that year ... capped at 10 per cent a year in either direction." Applied literally to the six wards from 2025-26 for two years it gives 3,754, i.e. 3,750 (arrests by Calderwick officers only). It is a model for the Harrowdown force's suites, filed as approved by a board, not as the estimand.
6. An analytical choice: what population "detentions the hub will book" covers (arrests by other agencies in the wards are booked too, per allocation note 2, and must be estimated from the street crime file's British Transport Police rows), and whether to carry the old trend forward when the Kingsway decline coincides with licence surrenders that ended in June 2024. Not a planted defect; the keys and handover splits are layer-1 mess.

#### Mechanical scan items
- custody_demand_model_v2.pdf, "the model" three times: harmless, it is the document's own subject.
- custody_demand_model_v2.pdf, a number matching a graded answer: harmless, the table holds 2025-26 suite arrest forecasts and records (5,493, 3,010, 7,287, 7,829 and so on) in different units to any figure I committed to; none equals one of my answers.
- tanner_street_hub_planning_brief.docx sharing most distinctive words with the answer sentence: harmless, the brief restates the request and defines the quantity, it gives no number.
- bank-holidays.json, dates after 2026-10-26: harmless, genuine GOV.UK future holidays, unrelated to the figures.

#### Method
Main figure: arrests by ward-of-arrest, converted from UTC to UK time and grouped into financial years, for the six wards (3,472 / 3,734 / 3,615 / 3,680 / 3,732 for 2021-22 to 2025-26; 2026-27 to date is flat on last year, 1,890 against 1,926 for April-September). The Calderwick-officer trend carried to 2027-28 is about 3,750 to 3,800 (the PDF method gives 3,754; Kingsway's decline looks to have stopped after the last licence surrender in 2024, Mill Bank is running up). Allocation note 2 says suites book detainees whichever force arrests them, and the street-crime file shows British Transport Police crimes at the Calderwick station (1,600 a year, Abbey Fields) and Kingsway station (102). Calderwick arrests run at about 0.16 to 0.17 per recorded crime in those wards, so I added about 280 BTP bookings a year, giving about 4,030 to 4,080, so 4,000. I considered 3,750 (no uplift); I chose the uplift because the brief asks for detentions the hub will book, not Calderwick arrests. The uplift is the least certain element.
Ask A: the remand files' linked_arrest is wrong on 122 of 1,309 rows (they point to released arrests). The charge time equals booked-in time plus the PACE detention clock exactly, so I re-linked each row to the remanded arrest in the same suite with that charge time (one tie broken by elimination), then took booking-in from that arrest. Charged 1 April 2025 to 31 March 2026 (UK time): 1,129 holds. Over 24 hours is handover minus booked-in.
Ask B: 614 initial-assessment rows are repeat rows in an episode. 291 are the same assessment split at the 07:00/19:00 shift handover (next row starts exactly when the last ended), counted once and classed by the first start time. 323 are fresh assessments after conveyance to the emergency department, counted as separate assessments. Counting those once would reduce each figure slightly.
Odd: a few episodes show a clinician from another suite on medication rows; the suite for assessments is consistent. Late-night licence rows labelled "(Upstairs)" sit in other wards.

### Reader B (Opus, medium)

score_reader (`--call-key call.planning_figure`): call figures 1 of 1 hit (4,000); ask figures 5 of 21 hit
(23.8 per cent), the five being the chart's financial years (3,472, 3,734, 3,615, 3,680, 3,732); 0 of the 16 remand and
assessment figures (remand cell hours 4,077, 2,512, 7,422, 5,298 and over 24 hours 165, 96, 281, 228, the files'
own detentions with the co-defendants left out; assessments 1,146 and 1,426, 558 and 714, 1,217 and 1,619, 1,469 and
1,974, the handover lines joined with the suites as labelled). FAIL: the reader landed the call (exit 1).

#### Part 2

1. **Decisive step.** No sentence states the decisive step. It comes from putting two filed sentences together. One is custody_suite_allocation_2027.xlsx, Notes, item 2: "A detainee is taken to the custody suite that serves the ward where the arrest was made, whichever force or agency the arresting officer belongs to, and the custody officer there decides whether to authorise detention." The other is tanner_street_hub_planning_brief.docx: "The force's arrest records, pulled on 6 October 2026: one row per arrest by a Calderwick Police officer". Together they show that the arrest file does not hold the whole population. The British Transport Police crime rows in police_uk_street_crime_2025-26.csv ("On or near Calderwick (station)", Abbey Fields, and Kingsway station) show where the missing detainees come from.

2. **File that ranks or scores the candidates.** None. custody_demand_model_v2.pdf scores its own past forecasts against the records ("Every suite came within 4 per cent."). It does not rank any candidate planning figure for the hub.

3. **File that exists only to help the analyst.** None. Every file reads as an operational extract or register. ward_population_mid-2024.csv and late_night_licences_2026.csv look like the distractors, but they are realistic context.

4. **Figure or name that reads as the answer.** None. No 2027-28 figure appears anywhere in the pack.

5. **Filed sentence that fixes the method or the population.** custody_demand_model_v2.pdf, 2.1 and 2.3: "A suite's demand is the people arrested in the wards it serves, as set in the suite allocation." and "The ward's arrests in the latest full year are carried forward at its average annual change over the three years to that year (the cube root of the latest year's arrests over the arrests three years earlier, less one), capped at 10 per cent a year in either direction." Read literally, on the arrest file (base 2025-26, change from 2022-23, carried two years to 2027-28), the six wards give 3,754, which rounds to **3,750**. That covers Calderwick Police arrests only. The brief fixes the population: "the detentions the hub will book from 1 April 2027 to 31 March 2028, to the nearest 250". Allocation note 2 says those detentions include other forces' arrests.

6. **What decides the main answer.** The deciding step is the population: whether the figure counts other agencies' detainees, which no arrest record covers. Once you include them, estimating how many there are is analytical: arrests per recorded crime by crime type, applied to the BTP crimes. But the choice that flips the answer between 3,750 and 4,000 is announced by two filed sentences: the arrest file's scope ("one row per arrest by a Calderwick Police officer") and allocation note 2 ("whichever force or agency the arresting officer belongs to"). In practice it is close to reading a definition and following a stated rule. The estimate itself barely matters: every reasonable arrest rate gives 245 to 290 extra detentions, and all of them land on 4,000.

#### Mechanical scan items
- `custody_demand_model_v2.pdf`, "the model" three times: harmless. It is the document's own subject ("The model gives each suite...", "The model was run...", "The model is reviewed..."). It says nothing about the hub figure.
- `custody_demand_model_v2.pdf`, a number matching a graded answer: harmless. The document's figures are 2024-25-based validation forecasts and 2025-26 suite totals (5,493, 5,407, 3,010 and so on). None is the 2027-28 hub figure, and the six-ward series has to be cut from the arrest file. Any match is coincidental and gives nothing away.
- `tanner_street_hub_planning_brief.docx`, shares most of the answer sentence's words: harmless. The brief is the source of the request and restates its definitions (six wards, the dates, remand cell hours, day and night). It gives no figure and does not mention other forces.
- `bank-holidays.json`, ISO dates after 2026-10-26 (2026-12-25, 2026-12-28): harmless. The GOV.UK feed publishes future bank holidays in advance, so these dates are normal content and say nothing about the answer.

#### How I reached the main answer

My figure covers every detention the hub would book for arrests made in Abbey Fields, Castle, Cathedral, Kingsway, Mill Bank and St Peter's in 2027-28. That includes British Transport Police arrests, because allocation note 2 sends every force's detainees to the ward's suite and the arrest file holds Calderwick officers only.

**Calderwick arrests.** I counted the six wards' arrests by financial year on UK local time, converted from UTC: 3,472, 3,734, 3,615, 3,680 and 3,732 for 2021-22 to 2025-26. I ran the approved demand model ward by ward: base 2025-26, cube-root change from 2022-23, capped at 10 per cent, carried two years. That gives 3,754. My run of the model reproduces its validation table exactly. As a cross-check, April to September 2026 (1,890) is about 2 per cent below April to September 2025 (1,926), which would give roughly 3,660. Every arrest in the six wards was booked at Northgate or Eastmoor, so no displaced bookings needed adding back.

**Other forces.** The only other agency in the pack is BTP, with 1,702 street crimes in the six wards in 2025-26, almost all at Calderwick and Kingsway stations. I applied Calderwick's 2025-26 arrests per recorded crime, by crime type and from the six wards, to BTP's crimes, which gives about 265 detentions a year. I assumed BTP volume stays flat; nothing in the pack shows a trend. The alternatives (the force-wide rate 245, the overall rate 275, including warrants 290) all keep the total in the same 250 band.

**Result.** 3,754 + 265 ≈ 4,020, which rounds to **4,000**. I rejected the model's literal Calderwick-only 3,750 because it leaves out detentions the hub will book. The model was validated against Calderwick arrest records, so it says nothing about other forces' volume.

**What looked odd:**
- The demand model PDF is headed "HARROWDOWN POLICE", not Calderwick, although its owner sits at Wendle Cross, Calderwick's headquarters. The licence numbers also carry an "HDL" prefix.
- Four arrests at the spring clock change have a booking time before the arrest time.
- 122 remand files link to an earlier arrest that ended in release under investigation or bail. I re-linked each to the remanded arrest that actually held the defendant (same ward and offence, booked before charge), which also fixes 12 suite mismatches.
- 291 initial health assessments are split across a 07:00 or 19:00 shift handover into two records. I counted each as one, at its first start time.
- Assessments repeated after a return from the emergency department I counted as separate assessments.
- Cell hours use DST-aware elapsed time.

### Ruling

Gate F failed: both readers landed the call, each through allocation note 2 read with the brief's coverage line
("one row per arrest by a Calderwick Police officer"), which reader A quoted for question 1 and reader B named as close
to reading a stated rule and a field's definition. The judge's Gate H read the decisive step the same way
(data_semantics), so architecture 3 is spent (design note, `## Tried and rejected`). The asks held both readers at 0 of
16. Both readers ruled the four REVIEW lines harmless, as stage 3 did. Their realism findings (the model PDF's
HARROWDOWN POLICE header, the HDL licence prefix, four spring clock-change bookings timed before their arrests) are
recorded and not fixed, the architecture being spent.
