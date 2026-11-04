# leak check, task488

**Verdict: REVIEW.** 17 files read, 87 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, segment, window, product, network, change, sentence, samples, tickets, line-up, golden, architecture, quality, agents, sections, population, reckoning, checks, record, volume, downstream, branch, notice, asserted, reader

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `QM-09_product_quarantine_and_recall.pdf`: 8 of 25 stump-paragraph terms appear (register, product, network, change, tickets, quality); read whether the document names the move
- **REVIEW** `farm_shift_log_2026-10-12_14.pdf`: 11 of 25 stump-paragraph terms appear (register, product, change, samples, tickets, quality); read whether the document names the move
- **REVIEW** `recall_notice_RN-2026-031.pdf`: 4 of 25 stump-paragraph terms appear (product, quality, record, notice); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `corbel_fuel_tickets_2026-10-12_14.csv`: names 3 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `northgarth_tickets_20261012-20261014.xlsx`: names 3 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 2, on a fresh copy of prompt.txt and target/ (target.zip sha256 c7c2288a9c35a0190bfd0d8bb6e7a15f7b4186fb56135095d9b1dbb0b182051b). Sweep 4's lines were kept out of the brief and ruled in the main thread.

# Leak read, task488 (no solving, no figures)

1. Decisive step stated? None. Closest: QM-09 3.2 "Every storage tank, hydrant section and refueller holding product from the recalled batch when fuelling is suspended is quarantined, and is drained before it is used again" and RN-2026-031 sec 3 recall-return field list. These state the standing duty and the output fields, not how to find where the batch stands.

2. File ranking or scoring candidates on the question: none. batch_certificates_register_2026.csv marks J-26-1187 "RECALLED 2026-10-14 05:12", status only. No file lists sections holding the batch or uplifts that got it.

3. File existing only to help the analyst: none clearly. stock_reconciliation_2026-09.pdf, pit_valve_inspections_2026-q3.xlsx, the filter-vessel and pit-valve sheets of hydrant_maintenance, and the Rack sheet are ordinary records that read as distractors/context.

4. Figure or name reading as the answer: none. Closest is the batch register's "RECALLED" status and density 795.4 for J-26-1187, which is a certificate value.

5. Filed sentence fixing how the main figure is computed or the population:
 - Prompt: "Where was fuel from recalled batch J-26-1187 still standing at the 05:30 suspension of fuelling on 14 October, section by section in the Windrell hydrant and refueller by refueller" fixes the point in time (05:30 PDT 14 Oct), unit (hydrant section, refueller), quantity (batch litres standing).
 - QM-09 2.2 "Hydrant section: a part of the hydrant network isolated by its section valve, as listed in the hydrant network register" fixes the section unit. 3.3 "Quantities ... are stated in litres at 15 C." 4.1 "from the batch's release to the suspension", "in any quantity" fixes the uplift population (every uplift with any batch fuel, release 13 Oct 06:00 to suspension), one row each, with the listed fields.
 - Prompt rounding: hydrant standing to nearest 100 L, other batch figures to nearest 10 L.
 Literal result: population is all uplifts between release and suspension that received any batch fuel (hydrant or refueller); standing stock is per section (register sections) and per refueller at 05:30 on 14 Oct; litres at 15 C. No sentence says how to apportion or trace the batch through the network or refuellers.

6. What decides the main answer: an analytical choice (how to trace batch fuel through the hydrant sections and the refuellers, and which uplifts received a blend), not a field reading or stated rule. No file or sentence states the tracing method; QM-09 states only the duty and RN the return fields. A dependent reading detail is time zone (PDT shift log vs UTC tickets, "Uplift start in UTC"), which is context, not the decider.

## Sweep item
a. harmless, because corbel_fuel_tickets and northgarth_tickets are ordinary delivery tickets (ticket no, status incl. one VOID, customer, flight, reg, pit/unit, gross and 15 C litres, temp, initials); airline names sit as customer fields, no batch, ranking or flag column.

## Specific files
b. farm_shift_log: ordinary shift log (handovers, pump duty, drain rounds, FV-2 dP, certificate receipt, tank line-ups, product-change check, apron closure). Tank line-up times (06:00 Tank 3 lined up, 15:40 hydrant to Tank 1, rack 12:20 to Tank 1), the P-A01 product-change check "matches J-26-1187" and the stands 27/28 closure are evidence a solver needs and are not worded to say which sections hold the batch. None declares any section clear. The 05:30 entry only states suspension and quarantine of Tank 3.
c. harmless: QM-09 and the notice state the standing procedure, the finding and action, and the return fields. Nothing defines when a section counts as clear, nothing steers to a method. QM-09 3.2/3.4 say drained before use and Committee approval; no clearance criterion.
d. Corbel daily checks, Northgarth QC checks, hydrant_maintenance drains read as ordinary quality checks (sump, shift start, idle pit flush, low point drains, C&B, water, density, flush litres). Some density readings of about 795 (e.g. Corbel P-C04 13 Oct 10:44, Northgarth stand 33 13 Oct 16:53, 14 Oct) and 801 values are consistent with batch/next batch fuel in the lines; this is natural trace evidence, not annotated, and no remark column calls it out. Mild observation only: the contrast of 795 among 803-804 readings is visible but undeclared. Harmless.
e. hydrant_network_register (segments, draw points, sections with line fill, rack) and SCADA (flow, totaliser, pressure, pumps, tank valve states) are plain registers/telemetry. No note or column names a step. Only quirk: the SCADA totaliser resets on 13 Oct 10:47 (matches shift log) and the Sections sheet carries a totals row; both ordinary.

Realism: none that read as machine-made. Minor tells for a careful reviewer: very uniform drain/filter values and the same tech initials repeated, and the Northgarth log mixing UTC with ISO "Z" against Corbel local time (plausible agent differences).

### Second read, after QM-09 2.3 gained its commingling sentence

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 dde9588d06276d40733dbca49a6148846424ec29678cc6024dea486d3e568532).

1. Decisive step: no file announces it. Closest are QM-09 2.3 "A refueller holds product from every batch it has received since it was last drained to empty, its contents mixed." and QM-09 3.2 "Every storage tank, hydrant section and refueller holding product from the recalled batch when fuelling is suspended is quarantined". Both are operator definitions, not instructions on how to compute.
2. None. No file ranks or scores candidates. batch_certificates_register_2026.csv only lists batches and statuses (J-26-1187 "RECALLED 2026-10-14 05:12").
3. None exists only for the analyst. Closest in feel: QM-09 (definitions) and the recall notice's section 3 "Recall return" field list, but both are what an operator and a supplier would really hold.
4. None reads as the answer. Nearest context: shift log "06:00 Tank 3 (J-26-1187) lined up to the hydrant pumps and the rack pump" and "15:40 Hydrant pumps moved to Tank 1 (J-26-1179)", and "12:20 Rack pump moved to Tank 1" (all timeline facts, no volumes or results).
5. Filed sentences fixing population/unit: QM-09 4.1 "from the batch's release to the suspension", "in any quantity", "litres delivered and the litres of the recalled batch among them"; 3.3 "stated in litres at 15 C"; 3.2 "holding product ... when fuelling is suspended". Recall notice 2.3 "every aircraft into which product from batch J-26-1187 has been delivered, in any quantity". The prompt fixes the moment (05:30 suspension, 14 Oct), sections and refuellers, one row per uplift with any batch fuel, and rounding (hydrant 100 L, others 10 L). Population: uplifts from release (13 Oct 06:00 local) to suspension that took any batch fuel; refuellers holding any batch since last drained to empty (mixed, per 2.3); sections holding batch at 05:30. No figure is given.
6. Analytical choice, reconstruction of what stands where (tracking the batch front through the hydrant sections and through refueller tanks over time, from SCADA, rack log, tickets, dips, transfers), not a single field reading. Textual aids are only QM-09 2.3 and 3.2 plus the data files; nothing planted is announced. Residual risk: 2.3 lets a reader execute a rule (any refueller loaded after release and not drained is a holder), see (b).

a. harmless, because they are plain ticket tables (ticket_no, status, account, customer, flight, reg, location, unit, litres, temperature, initials) with airlines beside litres as on any into-plane ticket; no flag, batch, ranking or recall column. Corbel has one VOID ticket (CB418335) and a reissue_of column, ordinary ticket hygiene. Northgarth has no batch column either.
b. QM-09 2.3 in full: "Refueller: a vehicle tank that carries product from the truck rack to aircraft, as listed in the into-plane equipment register. A refueller holds product from every batch it has received since it was last drained to empty, its contents mixed." It reads as a quality-manual definition of a refueller (with the register cross-reference typical of such manuals), consistent with 2.2 for hydrant sections, and the "mixed contents" sentence is a physical-state definition that any such manual would carry. It does lean toward which refuellers hold the batch (everything received since last drained to empty), so it is a mild steer on the refueller side: it names the holding rule but not which units, the drain history, or the mixing quantities. Leak level: low, arguably leak-adjacent as a rule statement. It says nothing about the hydrant in 2.3. Hydrant is only in 2.2 (sections are isolated by section valve per the register) and 3.2 (sections holding batch are quarantined); nothing on how batch moves or stands in the hydrant.

Realism: none that is clearly machine-made. Minor tells only: farm_shift_log (every entry plausible but each sets up a model fact, e.g. "Product change check at P-A01 ... matches J-26-1187", and "stands 27 and 28 closed", a tidy hint that the data are consistent); stock_reconciliation_2026-09.pdf has perfectly even percentages; hydrant register Sections total row is clean. These read as ordinary operator documents.
