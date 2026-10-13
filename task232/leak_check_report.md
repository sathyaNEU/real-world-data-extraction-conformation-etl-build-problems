# leak check, task232

**Verdict: REVIEW.** 18 files read, 22 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: infectious, follow-up, incubation, attendance, exposure, cd-st-, window, attribution, investigations, illness, closed, register, exclusion, caused, outbreak, childcare, investigation, contacts, child-hour, status, epidemiology, transmission, export, acquired, health

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `CD-ST-07_laboratory_feed_sla_lateness.docx`: golden figure 1.00 appears: ...d's expected secondary cases a year do not exceed 1.00. A feed whose expected secondary cases exceed 1.0...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `CD-ST-07_laboratory_feed_sla_lateness.docx`: 13 of 25 stump-paragraph terms appear (infectious, attendance, cd-st-, investigations, closed, register); read whether the document names the move
- **REVIEW** `GL-CD-11_enteric_ecec_response_guideline.pdf`: 15 of 25 stump-paragraph terms appear (infectious, follow-up, incubation, attendance, illness, closed); read whether the document names the move
- **REVIEW** `ncp_4-2_release_notes_sla_alerts.pdf`: 3 of 25 stump-paragraph terms appear (register, contacts, health); read whether the document names the move

## 6 ranking artifacts (REVIEW 1, INFO 3)
- **REVIEW** `cc_investigation_register_2021-2026.xlsx`: names 6 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `data_dictionary.xlsx`: names 6 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `lab_turnaround_returns_2025-26.csv`: names 6 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `ncp_feed_register.xlsx`: names 6 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `cc_investigation_register_2021-2026.xlsx`: 1 ISO dates after 2026-11-16, e.g. 2026-11-17

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### Read 1 (target.zip 2ef312f1)
# Reader answers (task 232, round 2)

1. Decisive step for getting from the files to each feed's SLA lateness.
No sentence names a move. The closest are procedural statements of the estimand:
- CD-ST-07 2.1: "A feed's SLA lateness is the longest of the platform's allowed settings (1, 2, 4, 6, 8, 12 and 24 hours) at which the feed's expected secondary cases a year do not exceed 1.00."
- CD-ST-07 2.2: "...the expected secondary cases from the feed's urgent childcare notifications in the basis period, had each reached the unit that many hours after the laboratory authorised it rather than at authorisation, divided by three."
- The release notes define lateness: "The lateness of a report is the time from the authorisation date and time in the report (OBR-22) to the platform's first acceptance of the report."
The standard tells you what to compute (the counterfactual delay and the cost model). It does not tell you which of the two lateness measures to use to describe a feed or how to handle the rate's estimand.

2. Which file already ranks or scores the six feeds.
None. ncp_feed_register.xlsx has the SLA column blank ("SLA lateness, hours (NCP 4.2)" is None for all rows). lab_turnaround_returns_2025-26.csv scores laboratories on collection-to-authorisation hours, not on lateness after authorisation. cc_investigation_register_2021-2026.xlsx lists the notifying laboratory with authorisation and receipt times per investigation, but no per-feed summary or expected cases.

3. A file that exists only to help the analyst.
None clearly. data_dictionary.xlsx is a normal data dictionary, and export_manifest.csv is a normal manifest. The one slightly helpful extra is the data_dictionary column note on ncp_condition_codes_2025 "urgent_childcare_list: Y for the conditions the unit acts on urgently..." which a real unit could plausibly have. lab_turnaround_returns, ecec_services_register and the incident log read as ordinary context or distractors.

4. Figure or name that reads as the answer.
None. The only number in the documents that looks like a cut-off is the "1.00" in CD-ST-07 2.1, which is a stated threshold, not a result. The docs give no per-feed value, no secondary transmission rate and no setting.

5. Filed sentences that fix the main figure, and what their literal execution gives.
- 2.1 (above): picks the largest allowed setting with expected cases a year <= 1.00; if even 1 hour exceeds 1.00, set 1 hour.
- 2.2: expected secondary cases a year at a setting = sum over the feed's urgent childcare notifications in the basis period of the counterfactual expected secondary cases, divided by three (years).
- 2.3: "The basis period is 1 October 2023 to 30 September 2026. A feed's urgent childcare notifications are the notifications that opened the unit's childcare investigations, as the childcare investigation register records them, with a result authorised in the basis period." Literal execution: the register rows (Result authorised between those dates), by Notifying laboratory. Selects only investigated notifications, 3 years.
- 2.4: "the expected secondary cases are the child-hours of contact the notified case would have added in their room, multiplied by the condition's secondary transmission per child-hour of contact" with child-hours between the calls at authorisation and at the delayed time; (a) calling hours 07:00 to 21:00 NSW time every day; (b) a case at the centre when called leaves one hour after the call, a case not yet there does not attend that day, no case attends a session starting after the call; (c) the case attends every booked or rostered session at booked times; (d) child-hours = hours at the centre x number of other children and educators who attended the case's room that day.
- 3.1: "A condition's secondary transmission per child-hour of contact is the number of secondary cases among room contacts in the unit's closed childcare investigations of the condition, divided by the child-hours of contact during those investigations' infectious attendance."
- 3.2: infectious attendance = "from the start of their infectious period to their exclusion, from the attendance records the centre supplied"; child-hours counted as in 2.4(d).
- 3.3: "Cases are confirmed and probable cases under the case definitions in the unit's guideline" (GL-CD-11 section 2: confirmed = positive lab result room contact; probable = room contact with diarrhoea epi-linked to a confirmed case, not tested or untestable).
What is not said: which of a room's recorded cases count as "secondary cases". The text says "secondary cases among room contacts" and "confirmed and probable cases", and the follow-up file has case_status Confirmed/Probable per contact, but nothing in the shipped text says whether a contact whose onset falls before or on the index case's onset (a co-primary), outside the infectious attendance or follow-up window, or with approximate onset counts; nor whether the 21-day pre-onset diarrhoea look-back counts. Literally, any Confirmed or Probable contact row in a closed investigation counts, which is what a literal reader would execute. Also unstated: how the room counts "other children and educators who attended" when the case was absent or when casual educators have separate numbers. The standard also says nothing about which timestamp (received vs authorised) defines "first acceptance" beyond the release notes, and nothing on preliminary vs final reports for the prompt's counts (reports "authorised" in the year, "first reached the platform").

6. What decides the main answer.
Largely a stated procedure: CD-ST-07 2.1 to 2.4 and 3.1 to 3.3 give a fully specified calculation (calling hours, leave rule, child-hours, rate, divide by three, threshold 1.00). A careful literal reader executing them gets the answer; the analytical content is in the data handling (deriving the secondary transmission rate from closed investigations, building room attendance from three differently formatted attendance exports, time zones, counterfactual call times). There is no sentence that says the key insight. The weakest point is that the thresholding and rate both look like rule application, with data cleaning (formats, UTC vs NSW, hours) as the effort. The register's own "Notification received" gives the observed lateness for urgent notifications, and the message log gives lateness for all reports; the standard's counterfactual (hours after authorisation, not the observed delay) is stated in 2.2.

7. Machine-generated or exercise-constructed signals.
- Rounded or constructed structure: the register's "Notification received" is always the same day or next day and the "Exclusion call" falls about 1 to 1.5 hours after receipt on every row I saw (e.g. CC21-001 received 2021-07-29 14:03:38, call 15:26; CC21-002 received 18:06:13, call 19:07); the "Result authorised" minute-precision vs "Notification received" second-precision is a mismatch (e.g. "2021-07-29 12:09" vs "14:03:38").
- Perfectly regular quarter-by-test structure in lab_turnaround_returns ("2025-Q4, Enteric PCR/Enteric culture/Respiratory PCR"). Note "2025-Q4" for a file covering Oct 2025 to Sep 2026 (a fiscal quarter reading is odd).
- Register extract date 13 November 2026 and CD-ST-07 approved 6 November 2026, with later-dated rows (see sweep line below). The release notes are "Issued 14 October 2026" while today's pack is dated November 2026; fine for a future-looking set, but the pack reads as set in the future.
- Index person numbers in the register mix formats ("a65a0b31", "329776", "CH23733", "156229") which is plausible as different centre software.
- Names such as "Larkspur Pathology", "Halden Pathology", "Highfield Pathology Services", "Kestrel Pathology (Queensland)" and room names (Gumnuts, Kookaburras) read as invented but plausible.
- Incident log summaries use one template ("the laboratory found its interface engine stopped, restarted it and released the queued results"; "No messages for X hours;") repeated.

## Mechanical sweep lines

- CD-ST-07 golden figure 1.00: harmless. It is the threshold stated in 2.1, which any solver needs; it is not a result.
- CD-ST-07 13 of 25 stump terms (infectious, attendance, cd-st-, investigations, closed, investigation): harmless. These are the domain words of the standard itself; the document describes the estimand and procedure and does not name any move, pitfall or trap.
- GL-CD-11 14 of 25 stump terms: harmless. A clinical guideline's ordinary vocabulary (incubation, infectious, follow-up, closed, illness); it names no analytical move.
- NCP 4.2 release notes 3 of 25 terms (contacts, register, health): harmless. Generic words ("Laboratory contacts are shown on the feed register page").
- cc_investigation_register names 6 of 6 candidates beside numbers: harmless. Register rows list the notifying laboratory with times per investigation; it does not total, rank or score the feeds on lateness or expected cases (46/32/25/21/13/6 investigations per lab is a count, not a call).
- cc_investigation_register 1 ISO date after 2026-11-16 (2026-11-17): harmless in terms of the answer, but note it is the "Follow-up to" date of open investigation CC26-022 (a projected end of follow-up, future relative to the 13 November 2026 extract), which is consistent with GL-CD-11 4.4. It is not a leak; it is a plausible planned date.

### Read 2 (after the secondary case definition, target.zip f97b0bc1)
# Reader answers (task232 r3)

1. Decisive step for lateness: CD-ST-07 2.2 and 2.4 define the figure as child-hours added between the unit's call at authorisation and the call at that many hours later (the calling hours, the one-hour leave rule, the booked-or-rostered attendance rule), times the condition's transmission rate. The step from files to lateness itself: ncp_4-2_release_notes_sla_alerts.pdf, "The lateness of a report is the time from the authorisation date and time in the report (OBR-22) to the platform's first acceptance of the report." Nothing says how to handle preliminary/corrected reports, repeat messages for one specimen, or the feed's sending-code change; the prompt's "first reached the platform" is the only hint.

2. None. lab_turnaround_returns_2025-26.csv gives collection-to-authorisation medians and p90 by laboratory, not SLA lateness. ncp_feed_register.xlsx has the SLA column blank.

3. None clearly. The nearest is data_dictionary.xlsx, which is plausible for a data officer. ecec_services_register.csv and lab_turnaround_returns_2025-26.csv look like context or distractors, but a unit could hold them.

4. None reads as the answer. Only the tolerance "1.00" in CD-ST-07 2.1 and the allowed settings list are figures, and they are rules.

5. Filed sentences:
 - CD-ST-07 2.1: "the longest of the platform's allowed settings (1, 2, 4, 6, 8, 12 and 24 hours) at which the feed's expected secondary cases a year do not exceed 1.00. A feed whose expected secondary cases exceed 1.00 even at 1 hour is set at 1 hour." Executes to: pick the largest setting with expected cases at or under 1.00, else 1 hour.
 - 2.2: "divided by three" over the basis period; 2.3: basis 1 Oct 2023 to 30 Sep 2026, "the notifications that opened the unit's childcare investigations, as the childcare investigation register records them, with a result authorised in the basis period". Population = register rows by notifying laboratory and authorised date (the register only, so only observed investigations).
 - 2.4 (a)-(d): the call-time, leave-time, attendance and child-hours rules. Executes to a day-by-day computation from bookings/rosters and attendance counts.
 - 3.1: "the number of secondary cases among room contacts in the unit's closed childcare investigations of the condition, divided by the child-hours of contact during those investigations' infectious attendance." 3.2 and 3.3 add the attendance window and the case definitions.
 - GL-CD-11 section 2: "Secondary case. A confirmed or probable case in a room contact who acquired the infection from the index case." and "A room contact is a child or educator who attended the index case's room on a day the index case attended while infectious."
 Which of a room's recorded cases are secondary: read literally, the cases who "acquired the infection from the index case". No shipped sentence says how to tell which ones. The incubation periods in the GL-CD-11 table (section 3) and the contact follow-up onset dates are the only material, so the reader must infer a rule (for example, onset within the incubation period after exposure). The followup file marks confirmed/probable status and onset (with an approximate flag) but no "secondary" flag. Literal execution leaves this open; it would need a closing sentence.

6. An analytical choice mixed with procedure. Most of the main figure is executing the 2.4 rules, which is rule application. What is not given is (a) identifying secondary cases from the recorded room cases (acquired from the index, using incubation and onset, not all ill contacts), (b) which attendance to use across three differently formatted exports, plus bookings. Deciding which cases are secondary rests on epidemiological judgement (incubation window, co-primary cases) and is the analytical piece. The rest follows 2.4 word for word. Quote: GL-CD-11 "Secondary case. A confirmed or probable case in a room contact who acquired the infection from the index case."

7. Constructed signs:
 - cc_investigation_register: investigation ids "CC21-001" etc. and index person numbers mixing 6-digit, "CH23733" and 8-hex styles; read as three centre systems, plausible.
 - ncp_feed_register.xlsx Notes: "A feed is one laboratory's notification stream; a laboratory that changes its sending facility code keeps one feed." This is an explanatory sentence a register note would not usually hold.
 - Register 'Open' rows with "Follow-up to" dates and a data extraction of 13 November 2026 with docs dated 6 November 2026.
 - Animal room names (Gumnuts, Lorikeets), sequence-like ids; otherwise records read as organisational. CD-ST-07 section 2.4 is very precisely tailored, reads like a specification.

Sweep lines:
- CD-ST-07 docx golden figure 1.00 (tolerance in 2.1): harmless, it is the filed threshold, not an answer figure.
- CD-ST-07 docx 13 of 25 stump terms (infectious, attendance, cd-st-, investigations, closed, investigation): harmless, the document is the standard's own subject vocabulary; it states the procedure and the rate definition and does not name a trap or a method for identifying secondary cases.
- GL-CD-11 pdf 15 of 25 terms (infectious, follow-up, incubation, attendance, closed, illness): harmless, ordinary guideline wording. It includes incubation periods but does not tell the reader to use them to classify secondary cases.
- ncp_4-2 release notes pdf 3 of 25 (register, contacts, health): harmless, incidental words.
- cc_investigation_register names 6 of 6 laboratories beside numbers: harmless, it lists investigations by notifying laboratory with times, with no ranking or scoring on lateness or threshold. It does show authorisation and receipt times per investigation, which are raw inputs, not a ranking.
- cc_investigation_register 2026-11-17: harmless, it is the scheduled "Follow-up to" date of the open investigation CC26-022 (Open, extract date 13 November 2026), a planned end of follow-up, not a leaked later fact.
