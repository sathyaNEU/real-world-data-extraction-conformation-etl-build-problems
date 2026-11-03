# leak check, task479

**Verdict: REVIEW.** 16 files read, 23 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, screen, reader, decisive, screened, register, header, record, claims, sentence, county, minute, family, carried, method, golden, buildings, capture, driver, reflex, deductible, filing, oxidizer, records, capacity

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `PTO-2219-0447_R3_permit.pdf`: \bdesign note\b|\bgenerator\b x1: ...Steam boiler B-1, natural gas, 18.4 MMBtu/hr None S-4 EU-G1 Emergency generator GEN-1, diesel, 600 kW None S-5 Section B. EU-P1 process vents B.1 Lim...

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `BST-25-0418_RTO-1_destruction_efficiency_report.pdf`: golden figure 99.4 appears: ...A. The VOC destruction efficiency demonstrated is 99.4 per cent, the mean of the three runs. The combust...
- **REVIEW** `PTO-2219-0447_R3_permit.pdf`: golden figure 2.5 appears: ....1 Limit. VOC emitted from EU-P1 shall not exceed 2.5 tons in any calendar year. B.2 Control. Each EU-P...
- **REVIEW** `PTO-2219-0447_R3_permit.pdf`: golden figure 100 appears: ...ecorded monthly; EU-G1 shall operate no more than 100 hours a year for maintenance and readiness testin...
- **REVIEW** `rto1_dahs_1min_2026.csv`: golden figure 47,900 appears: ...FF 2026-07-29 12:46,902.6,905.4,OFF 2026-07-29 12:47,900.6,902.3,OFF 2026-07-29 12:48,903.9,900.8,OFF 2026...
- **REVIEW** `PTO-2219-0447_R3_permit.pdf`: carries 8 of 8 distinctive words of the committed call: 'EU-P1 did not keep within its 2026 VOC limit: it emitted 3.2 tons against the 2.5-ton calendar-year limit, over by 0.7 t'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `PTO-2219-0447_R3_permit.pdf`: 6 of 25 stump-paragraph terms appear (record, county, minute, method, oxidizer, records); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `PTO-2219-0447_R3_permit.pdf`: names 5 column(s) of the data files verbatim (Closed, Description, Equipment, Permittee, Unit): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader: one isolated thread (sonnet, medium) on fresh copies of prompt.txt and target/ (target.zip 43c1d6c4), 2026-11-03.

1. Decisive step: none. Closest is the permit's B.4 ("RTO-1's VOC destruction efficiency is the efficiency demonstrated in the most recent performance test accepted by the District"), a stated condition, not an announcement.
2. Ranking or scoring file: none. No file totals emissions or compares against the limit.
3. File that exists only to help the analyst: none. The operation-code table reads as a system lookup; the closed-vent register, LDAR, CMMS, boiler and generator files read as context or distractors.
4. Figure or name reading as the answer: none. The 2.5-ton limit and the 99.4 per cent efficiency read as a regulatory fact and a test result.
5. Literal-fixing sentences: B.1 (2.5 tons in any calendar year), B.5 (the calendar-year total is the sum of the quarters), D.1 (local time), B.4 (efficiency from the latest accepted test). Literal result: emitted VOC from EU-P1 summed over local-time quarters, each vented pound treated at the tested efficiency while RTO-1 is in RUN and uncontrolled otherwise.
6. What decides: not visible from the pack alone; the reader lists time and unit handling, B.2 bypass and B.3 block validity as the text it sees, and asks whether an analytical step sits above them. Ruled in the main thread (Gate H recomputation below).

Mechanical flags: (a) the generator row is the EU-G1 permit entry, harmless; (b) the numbers the answer-figure sweep found are shipped facts (limit, test efficiency, a DAHS temperature), harmless; (c) the permit is the governing document and must carry the call's vocabulary, harmless; (d) the permit is the District's own record, its column-like words are shared naming, harmless.

Realism notes: the BST report sentence comparing expected to measured inlet loading reads slightly analyst-facing (borderline); the permit's B.3 block-validity detail is unusually explicit. No LLM-signature words.

Main-thread ruling on question 6 (2026-11-03): analytical. RTO-1's 3,800 scfm maximum and PSV-31 appear only as ratings in the equipment register and no rule says what the excess does, so the decisive step is the minute-by-minute reconstruction of the vents' coincident flow against the fan's draw; the determinism judge's Gate H reads the same (decisive_step analytical).

Stage 4 pass (2026-11-03): the realism note on the BST report was closed in the generator (the process paragraph now gives the plant's calculated loading as process data, without the comparison to the measured loading); B.3 kept. The other two moved files are data only (the CMMS planned outage order on the DAHS's outage dates, the register's PSV-31 inspection date), so the reader was not re-run; leak.py re-run on the final cut above.
