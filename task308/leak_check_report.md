# leak check, task308

**Verdict: REVIEW.** 14 files read, 25 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reader, peaker, record, section, screen, replay, golden, readers, claims, asserted, severn, sentence, forced, carried, plan-only, planning, import, outages, availability, re-root, ketchum, default, decisive, catastrophe, weather

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `2027_capacity_rfo_offers_received.pdf`: golden figure 300 appears: ...ortation (IT) service. Manufacturer's EFORd 4.5%. 300 MW USD 6.45 per kW-month Red Willow import Red Wi...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `2027_capacity_rfo_offers_received.pdf`: 3 of 25 stump-paragraph terms appear (planning, import, ketchum); read whether the document names the move
- **REVIEW** `RA-3_resource_adequacy_standard_rev4.pdf`: 7 of 25 stump-paragraph terms appear (record, replay, forced, planning, import, outages); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `2027_capacity_rfo_offers_received.pdf`: names 4 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `delivery_point_register_2025.xlsx`: names 8 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `member_load_forecasts_2027.xlsx`: names 8 of 12 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `fleet_list_2027.xlsx`: 4 ISO dates after 2026-10-30, e.g. 2026-12-31, 2029-12-31, 2035-05-31, 2041-06-30

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader (sonnet, medium), 2026-10-27, on the cut pack only (prompt.txt and target/).

1. Decisive step: none announced. The nearest text is RA-3 section 7 ("counted in each replayed hour at its expected available capacity in that hour, judged from the evidence the record holds"), which files the quantity and leaves the method open.
2. Ranking or scoring file: none. The RFO paper states the evaluation basis with no results.
3. File that exists only to help the analyst: none. gads_cause_codes.csv is a plausible lookup; the forward curve, member load forecasts and meter service orders read as distractors or context.
4. Figure or name that reads as the answer: none. No computed EUE, net value or allocation figure appears anywhere.
5. Filed sentences fixing the computation: RA-3 sections 4 to 7 (replay every forced event whatever its cause, latest revision; tie outages remove the import; EUE the equal-weight mean of ten weather years; each offer alone against the planning-year fleet; expected available capacity judged from the record) and MS-12 sections 1 to 4 for the member figures. Their literal execution is the golden's construction; section 7 leaves the evidence-to-capacity method open.
6. What decides the main answer: an analytical choice (how an offer's expected hourly capacity is judged from the record). The ancillary member figures are rule application under MS-12, as asks may be.

Mechanical-sweep rulings: answer-figure sweep harmless (offered MW, prices and the manufacturer's EFORd are inputs); ranking sweep on the RFO paper harmless (capacity and price only, no ranking); ranking sweep on the delivery point register harmless (no energy or peak figures); date sweep on fleet_list_2027.xlsx harmless (a retirement date and contract end dates).

Realism notes: substation names in the delivery point register run in near-alphabetical order and meters repeat from four models; uniform event_id formatting; mixed time formats across files read as deliberate mess. No placeholders, hidden sheets or toolchain signatures.
