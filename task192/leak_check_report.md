# leak check, task192

**Verdict: REVIEW.** 14 files read, 49 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, device, family, decisive, current, shipped, actions, record, counts, august, golden, reports, operations, sentence, screen, action, nothing, reflex, coding, minute, driver, register, window, measured, partner

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `procedures/DRP-04_distribution_reliability_procedure_rev6.pdf`: carries 12 of 17 distinctive words of the committed call: 'Send the overhead line patrol crew to MLR-2 for the week of 9 November 2026, walking the main line from the Millrace fee'

## 8 column names (REVIEW 3)
- **REVIEW** `assets/distribution_transformers.csv`: columns a generator names and an organisation does not: protective_device
- **REVIEW** `assets/protective_device_register.csv`: columns a generator names and an organisation does not: device_id, device_type, upstream_device
- **REVIEW** `oms/oms_outage_history_2025_2026.xlsx`: columns a generator names and an organisation does not: Device

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `procedures/DRP-04_distribution_reliability_procedure_rev6.pdf`: names 7 column(s) of the data files verbatim (Bluffview, event, feeder, gust, point, station): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 4 design-note vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 4, on a fresh copy of prompt.txt and target/ (target.zip sha256 a82127037dc5f8594d116ee6d5d69a517567df80f074ba62d3e8fa0ccbacf097). The answer-figure numbers were kept out of the brief, and sweep 8's field-term lines were ruled in the main thread.

# Leak read, task192 (read only, nothing solved)

1. Decisive step: none stated. Closest is DRP-04 5.2: "The patrol goes to the feeder where a component on the overhead line is breaking down, so that it is found and replaced before it fails outright. When no feeder has one, the crew is released to the construction section for the week." It states the purpose, not how to detect the component. 5.4 fixes the form of the stretch ("the zone of a breaker, recloser or fuse").
2. Ranking/scoring file: none. No file scores feeders on the patrol question. OMS carries Cause codes per ticket, vegetation lists work orders; neither ranks.
3. File existing only to help the analyst: none. The "Cotter Road 2026-03-14" sheet in assets/feeder_register.xlsx (Old feeder / New feeder / Old breaker / New breaker / Old SCADA point / New SCADA point) is a renaming crosswalk, and reads as the utility's own record of the 14 March 2026 renaming (matches in_service_to 2026-03-13 in the device register). Plain, no commentary.
4. Answer-like figure or name: none. Closest are context numbers: DRP-04 4.1 "TMED, is 38.03 minutes" and 4.2 "35,404", and the register's `terminal_phasing` values (e.g. R-3774 "C-B-A") which read as asset attributes.
5. Filed sentences fixing computation/population:
   - 2.1/3.2: "The customers served by a feeder are the service points it supplies on the last day of the reporting period"; "Its customers served, and the customers counted in its CEMI-n, are the service points it supplies on the last day of the period, each with every sustained interruption that customer had in the period." Fixes denominator = service points on 31 Oct 2026 (service_points_2026-10-31.csv), and CEMI population including customers' full history, even on feeder changes.
   - 3.2: interruptions "are those of the interruptions on the feeder as it stood when each began." Fixes numerator attribution to the feeder at interruption start.
   - 2.2: sustained >5 min, momentary <=5 min. 2.5: momentary interruption event = one or more momentary interruptions within five minutes of the first; those ending in a sustained interruption of that customer are not counted. 2.6 / 4.2: local Central day on which it began; MED = daily system SAIDI over 38.03 using denominator 35,404; every interruption beginning on a MED is excluded. 3.1: CEMI-n = number of customers with more than n sustained interruptions.
   - 5.4: stretch given "as the zone of a breaker, recloser or fuse: the line from it to the next ... beyond it, with the taps fused off that line."
   These fix the indices for the asks; they do not fix which feeder the crew walks.
6. What decides the main answer: file-wise, the analytical choice of reading the protection records (relay, recloser control, SCADA SOE) together with customer contacts and OMS cause codes to separate a failing component from storm/animal/tree causes (5.2/5.3 only name the exclusions). I find no sentence that names the discriminating signal or procedure, so it reads as analysis. Caution: 5.3 and 6.1 give the excluded cause classes and a storm-day definition, which narrow the route but do not execute it.

## Sweep items
a. harmless, because it is standing procedure (revision table, approver, scope, definitions); no passage names a feeder, date, device or this week's assignment. 5.2 and 5.3 are generic role text.
b. harmless, because it names reliability concepts (customer, interruption, SAIDI, MED, breaker/recloser/fuse), is signed by "Kelsey Sanford, Distribution Reliability Engineer; approved by Shawn Hartman", has a revision history and an extract note (sections 7, 8 not reproduced); reads as the utility's own document, not a note to the analyst. It does not name raw column names in a way that instructs.

## Specific files
c. protection/feeder_relay_events, recloser_control_events, soe: ordinary records. Relay: event_no, relay, utc_time, event_type ("BG T"), shot, phase and ground currents, trip_element (50G1/51G/50P1/51P), freq_hz jittering 59.98-60.02. Recloser: terminals "1-G/2-G/3-G", fault_ka, close_source AUTO/LOCAL, a few LOCKOUT/LOCAL CLOSE. SOE: all quality GOOD, CST stamps, OPEN/CLOSED pairs. No remarks, flags or comments column. Event volume varies by feeder (e.g. NYD-F2, MLR-F2, SYC-F2 heavy, R-2157, R-3774 busy), but that reads as differing exposure, not a pointer. Minor note: recloser terminals 1/2/3 need the register's terminal_phasing to become phases; that is conformation, not a hint. Harmless.
d. blinking_lights_contacts: ordinary log (contact_id, time, service_point, channel PHONE/IVR/WEB, reason LIGHTS BLINKING / CLOCKS RESET / FLICKER). No free text, no feeder column, spread across 16 feeders and the whole period; nothing written to point at a cause or feeder. Harmless.
e. feeder_register.xlsx and protective_device_register.csv: read as own registers. Feeder register columns: Feeder, Substation, kV, Overhead miles, Underground miles, Fused taps, Customers (2025 plan), Feeder breaker; plus the rename crosswalk sheet. Device register: device_id, type, feeder, pole, upstream_device, in_service_from/to, scada_point, shots_to_lockout, terminal_phasing, fuse_link, available_fault_slg_a. No notes column, no hidden sheets, no cell comments. Harmless.

## Realism
none that is decisive. Mild tells only: eight-digit service_point and ticket device IDs are uniformly random; xlsx zip timestamps are 1980-01-01 (library default); lightning file has near-duplicate stroke rows milliseconds apart (plausible network behaviour). No file reads as machine-narrated.

### Second read, after the FIX_NOW repair

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 db11592897be490e0f61871a317a9a9ba026450bd3d4167c18369ea7be270aa2), after DRP-04 gained 2.7 and the planned-interruption clause.

# Leak read, task192 r2 (read and quote only, nothing solved)

1. Decisive step: DRP-04 5.2 "The patrol goes to the feeder where a component on the overhead line is breaking down, so that it is found and replaced before it fails outright. When no feeder has one, the crew is released to the construction section for the week." This is the purpose of the patrol, and 5.3 ("Storm damage, animal contacts and contacts with trees are not the patrol's work") says which causes to exclude. It does not say how to detect the failing component. Prompt: "to find a component that is failing before it fails outright". None of these names a method.
2. Ranking/scoring file: none. The feeder register has miles and tap counts, with no scores. SOE, relay and recloser logs are raw events.
3. File that exists only to help the analyst: none. DRP-04 comes closest, but it reads as standing procedure. The Cotter Road tab of the feeder register (old to new feeder, breaker and SCADA names) is a plain rename crosswalk, which a utility keeps for a renaming.
4. Reads as the answer: none. No feeder, device or stretch is named as a candidate anywhere. The only figures that look like answers are TMED 38.03 and the denominator 35,404 (DRP-04 4.1, 4.2), and these are inputs to the indices, not the call.
5. Literal-fixing sentences:
   - 3.1 "SAIFI is the customer interruptions divided by the customers served; SAIDI is the customer minutes of interruption divided by the customers served; MAIFIE is the customers' momentary interruption events, summed over the customers, divided by the customers served; and CEMI-n is reported as the number of customers served who had more than n sustained interruptions in the period." This fixes the four index definitions for the asks (CEMI-2 for "more than two sustained"), per feeder, period January to October 2026.
   - 3.2 "A feeder's customer interruptions, customer minutes and momentary interruption events are those of the interruptions on the feeder as it stood when each began. Its customers served, and the customers counted in its CEMI-n, are the service points it supplies on the last day of the period, each with every sustained interruption that customer had in the period." This fixes feeder attribution at the time of the interruption, and the denominator and the CEMI population as service points on the last day. It matters for the Cotter Road rename and for service points that moved feeders.
   - 2.1 customers = metered service point, served on the last day of the period.
   - 4.1/4.2 "A day whose daily system SAIDI exceeds TMED is a major event day, and every interruption that began on a major event day is left out of the indices." This fixes the exclusion rule, with 2.6 (local Central day on which it began).
   - 2.2/2.5 define the sustained and momentary cut (5 minutes) and the event grouping.
   - 5.4 stretch = the zone of a breaker, recloser or fuse, the line to the next devices beyond it, with the fused taps. This fixes the unit for the stretch answer.
   The main call itself (which feeder/stretch) is not fixed by any filed sentence beyond the 5.2 and 5.3 definitions of the work.
6. What decides the main answer: an analytical choice. The files give no rule for recognising a failing component. The decision rests on how the analyst reads fault patterns in the relay, recloser and SOE logs against 5.2 and 5.3, and no document says how. DRP-04 5.2 gives the purpose only. The index asks are rule application (3.1, 3.2, 4.x).

## Sweep items
a. harmless, because every passage is standing procedure with a revision history, scope, definitions and sections that do not concern this week (storm patrol, reporting). Nothing names a feeder, device or week, and 5.2 states the patrol's purpose without saying how to detect it.
b. harmless, because it is issued as Kestrel Falls Municipal Utilities DRP-04 Rev 6 (12 January 2026, named engineer and approver, revision table). Its terms (customers served, momentary events, CEMI-n, major event days) are the utility's own reporting definitions, and nothing is addressed to the analyst.

c. Quotes:
   - 2.2 "An interruption is the loss of supply to one or more customers. A sustained interruption lasts more than five minutes; a momentary interruption lasts five minutes or less. Planned interruptions, taken for work on the system, are counted like any other."
   - 2.5 "A momentary interruption event is one or more momentary interruptions of a customer's supply within five minutes of the first of them. Momentary interruptions of a customer that end in a sustained interruption of that customer are part of the sustained interruption and are not a momentary interruption event."
   - 2.7 "An interruption's start and end are the times the outage management system records for it. Interruptions the outage management system does not record, as with every momentary interruption, take their times from the SCADA sequence-of-events log, and a recloser's momentary interruptions from the recloser's own event log."
   None steers toward a feeder. They define timing and counting for the indices, in standard IEEE 1366 style. 2.7 names the data sources (a source-precedence rule), and it points to the SOE and recloser logs without saying what to look for in them. Not a leak.

d. Identifiers and tickets read as real systems output.
   - Service points: 8-digit, prefix by substation (10, 20, 30, 40, 50), the same as in OMS Device.
   - Transformers: T102060 (T plus the service-point prefix), as in the distribution register.
   - Fuses: F-10591, pole IDs like BLV1-P032, and fuse links 40K, 100T, 80T with fault-current values, as a protection register would have them.
   - OMS tickets: legacy sheet with T25-001545, local time MM/DD/YYYY, Circuit, Crew, causes like EQUIP and PUB. Newer sheet has INC-2026-00329 in UTC ISO, long cause names, and a Restoration Steps sheet for staged restorations. Two systems in two formats, with gaps in the numbering (-001545, -001547, -001548), is typical of a system change.
   - Nothing reads as placed to be caught. The same service point appears in OMS, the contacts file and the service point list. Mixed time zones and formats (CST text, UTC Z, MM/DD/YYYY local) are plausible Layer 1 mess.

Realism: none that I can see. Mild possible tells are the clean round counts in the feeder register and the uniformly tidy column sets across logs, and neither is a clear machine tell.

### Final read, on the cut with the 2.7 pin

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 dbbb2dcec36e7503caf5f7d3edf6f61273ad77df9f5879db75923ab6b57eb140).

# Leak read, task192 r3 (read and quote only; nothing solved)

1. Decisive step: none stated. Nearest is DRP-04 5.2, "The patrol goes to the feeder where a component on the overhead line is breaking down, so that it is found and replaced before it fails outright." That is the prompt's own question restated as the patrol's standing purpose; it names no method or evidence.
2. Ranking/scoring file: none. No file ranks feeders on the patrol question. (feeder_register.xlsx carries only miles, fused taps, planned customers.)
3. File that exists only to help the analyst: none clearly. The register sheet "Cotter Road 2026-03-14" (CR-12 to CTR-1 etc.) is a crosswalk, but it reads as the utility's own renaming record. DRP-04 is the nearest candidate and is read below (a, b, c).
4. Figure or name reading as the answer: none. No flagged feeder, device or pole anywhere. The only stated numbers are DRP-04's TMED "38.03" and denominator "35,404", which are procedure parameters (context for the indices ask, not the patrol call).
5. Sentences fixing the main figure/population: the main call is not fixed by one sentence (5.2 gives purpose only). For the indices: 3.1 "SAIDI is the customer minutes of interruption divided by the customers served; MAIFIE is the customers' momentary interruption events, summed over the customers, divided by the customers served; and CEMI-n is reported as the number of customers served who had more than n sustained interruptions in the period" with 3.2 "Its customers served, and the customers counted in its CEMI-n, are the service points it supplies on the last day of the period". Literal result: per-feeder denominator = service points on the feeder on the last day of the period (31 Oct 2026, matching service_points_2026-10-31.csv); numerators are interruptions on the feeder as it stood when each began; major event days (4.1-4.2, TMED 38.03 vs system daily SAIDI over 35,404) removed; sustained > 5 min, momentary events grouped within 5 minutes (2.2, 2.5). 5.4 fixes the stretch's unit: "the zone of a breaker, recloser or fuse: the line from it to the next breakers, reclosers or fuses beyond it, with the taps fused off that line".
6. What decides the main answer: the files point to an analytical choice (judging from relay/recloser/SCADA/OMS/contacts which feeder shows an escalating pre-failure pattern, vs the indices which are rule application). Nothing in the pack states the evidence rule. The only deciding text is 5.2/5.3 ("Storm damage, animal contacts and contacts with trees are not the patrol's work"), which defines scope, not method. The indices asks are rule application from 2.x-4.x, which is acceptable for asks.

## Flagged items
a. DRP-04 vocabulary overlap: harmless, because 5.1-5.4 read as standing assignment policy (weekly, Wednesday, release to construction if none); it names no feeder, device, date of this week or finding. Rev table entry "patrol assignment moved to Wednesday" is ordinary.
b. Column names in DRP-04: harmless, because it is the utility's own controlled document (authors/approvers named, revision table, extract note "sections 7 and 8 not reproduced", Scope 1.1 lists the substations) and the terms are standard IEEE 1366 vocabulary; nothing addressed to the analyst.
c. Section 2.7 in full: "An interruption's start and end are the times the outage management system records for it. Interruptions the outage management system does not record, as with every momentary interruption, take their times from the SCADA sequence-of-events log, and a recloser's momentary interruptions from the recloser's own event log. A sustained interruption the outage management system does not record runs, for the indices, from the opening that locked out its breaker or recloser, as the outage management system times those it records; the trips and recloses before that lockout are part of it under 2.5, not momentary interruption events, and do not move its start." Harmless, because it defines timing sources for the indices only and never mentions the patrol, a feeder, or failing components; it is procedure-voiced, though unusually detailed and a touch tutorial ("as with every momentary interruption"). Minor note only: it tells which logs time which events, which is data-source mapping the indices ask depends on, not the patrol call.

## Realism
Mostly none. Minor tells: DRP-04 2.7 is dense and bespoke for a municipal procedure; OMS workbook creator "omsreport" is plausible; line_clearance_work has tidy synthetic contractor names (low concern). Nothing machine-generated is evident; the legacy-vs-new OMS sheets, CST/UTC/local formats and feeder renaming read as system artifacts.
