# leak check, task303

**Verdict: REVIEW.** 11 files read, 40 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: ticket, tickets, breaker, supply, substation, minute, record, vegetation, sibling, probes, recorded, wildlife, section, lifetime, removes, outage, system, candidates, exports, losses, device, handheld, essentials, architecture, nothing

## 3 answer figures in the pack (REVIEW 13)
- **REVIEW** `commission_order_reliability_2024.pdf`: golden figure 2.10 appears: ...th calendar year 2024, the Company shall earn USD 2.10 for each customer-minute of sustained interruptio...
- **REVIEW** `oms_export_notes.txt`: golden figure 112 appears: ...ed tickets FDR feeder number (112 is feeder F-112) SUB_CD substation code: PLC...
- **REVIEW** `oms_interruptions_2019_2022.csv`: golden figure 13,540 appears: ...REE,FUS,FUS-208-32 22-02343,208,SRH,08/06/2022,16:13,540,6,TREE,TX,TX-208-0801 22-02446,208,SRH,08/06/2022...
- **REVIEW** `oms_interruptions_2019_2022.csv`: golden figure 14,450 appears: ...REE,TX,TX-112-2825 22-00985,112,PLC,07/10/2022,20:14,450,121,TREE,FUS,FUS-112-25 22-01005,112,PLC,07/10/20...
- **REVIEW** `oms_interruptions_2019_2022.csv`: golden figure 32,100 appears: ...IND,TX,TX-522-0804 19-00785,522,KTR,05/01/2019,15:32,100,64,UNK,FUS,FUS-522-13 19-00805,522,KTR,05/01/2019...
- **REVIEW** `storm_hardening_plan_2027.docx`: golden figure 2.10 appears: ...chanism (Docket E-2024-031) the company earns USD 2.10 for each customer-minute of sustained interruptio...
- **REVIEW** `storm_hardening_plan_2027.docx`: golden figure 114 appears: ...Creek 12.6 5.3 F-114 Pell Creek 11.2 4.7...
- **REVIEW** `storm_hardening_plan_2027.docx`: golden figure 205 appears: ...Creek 11.2 4.7 F-205 Sorrel Hill 14.4 6....
- **REVIEW** `storm_hardening_plan_2027.docx`: golden figure 301 appears: ...l Hill 12.4 5.2 F-301 Byers Mill 14.2 6.0...
- **REVIEW** `storm_hardening_plan_2027.docx`: golden figure 303 appears: ...s Mill 14.2 6.0 F-303 Byers Mill 10.5 4.4...
- **REVIEW** `storm_hardening_plan_2027.docx`: golden figure 208 appears: ...l Hill 14.4 6.0 F-208 Sorrel Hill 12.4 5....
- **REVIEW** `storm_hardening_plan_2027.docx`: golden figure 112 appears: ...Estimated cost (USD million) F-112 Pell Creek 12.6 5.3...
- **REVIEW** `storm_hardening_plan_2027.docx`: carries 13 of 15 distinctive words of the committed call: 'Convert the backbone of F-205 (Sorrel Hill) in 2027: it removes 237,600 customer-minutes of sustained interruption a yea'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `commission_order_reliability_2024.pdf`: 3 of 25 stump-paragraph terms appear (minute, record, system); read whether the document names the move
- **REVIEW** `mobile_workforce_export_notes.txt`: 8 of 25 stump-paragraph terms appear (ticket, supply, minute, record, recorded, outage); read whether the document names the move
- **REVIEW** `oms_export_notes.txt`: 13 of 25 stump-paragraph terms appear (ticket, tickets, breaker, substation, minute, record); read whether the document names the move
- **REVIEW** `storm_hardening_plan_2027.docx`: 12 of 25 stump-paragraph terms appear (breaker, substation, minute, record, vegetation, wildlife); read whether the document names the move

## 8 column names (REVIEW 2)
- **REVIEW** `oms_interruptions_2023_2025.csv`: columns a generator names and an organisation does not: protective_device_type, protective_device
- **REVIEW** `storm_crew_status_2023_2025.csv`: columns a generator names and an organisation does not: device

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 2. Isolated scored readers (sonnet, medium), each holding only prompt.txt and the unzipped pack, briefed
with the flat key paths of the call, the six candidates' figures and the 24 ask cells; no stump vocabulary and no
answer figure in the brief. Scored with score_reader.py against figures.json.

| Round | Pack | Reader | Call | Scored figures kept | Verdict |
|---|---|---|---|---|---|
| 1 | 66cc0eca | q7k303a | F-112 at 455,400 (miss) | 26 of 30 (both asks whole) | the ask layer leaked |
| 1 | 66cc0eca | m2w303b | F-112 at 455,400 (miss) | 14 of 30 (ask A whole) | the ask layer leaked |
| 2 | 784cd964 | k5r303c | F-112 at 455,400 (miss) | 2 of 30 (the two candidate figures the default path shares) | PASS |
| 2 | 784cd964 | w8n303d | F-112 at 455,400 (miss) | 2 of 30 (the same two) | PASS |

- The decisive step: no reader tested the breaker tickets' coincidence across sibling feeders; all four credited every
  breaker ticket to its own backbone and filed F-112.
- Round 1: both readers joined the storm crews' Restored time to every storm ticket (the outage system's restoration
  ran later on six storm tickets in ten), and one read the handheld durations as hours and minutes from fractions that
  never pass .59; both devices were re-sited one level below the repair.
- Round 2: both readers made the same repairs (the crews' Restored time; decimal durations) and read every crew status
  and every legacy OUT_DT as Eastern local dates and times, which the contract crews' devices and the handheld tickets'
  closing dates contradict; no ask cell kept.
- A ranking file: none; the plan's candidate table lists feeder, substation, miles and cost in feeder order.
- Realism tells raised: a round 1 reader noticed fifteen same-fuse pairs opened in the same minute, from storm tickets
  piled at 23:25; the pile-up is folded back into the evening in the shipped pack (no golden figure moved).

Verdict: PASS on the shipped design (round 2; measured pair 16.5, the ask layer at 0 of 24 cells for both readers).
