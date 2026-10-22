# leak check, task273

**Verdict: REVIEW.** 18 files read, 51 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: recorded, record, percentile, clients, request, sample, client, distribution, rebuilt, back-fill, mechanism, missing, pauses, readable, outcome, another, decisive, server, textbook, records, paused, population, balancer, nothing, arrivals

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `yearend_peak_loadtest_plan_2026.docx`: carries 20 of 23 distinctive words of the committed call: 'The platform teams should fix five of the 24 public API endpoints before the 4 December code freeze: EP01 (POST /v2/payr'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `yearend_peak_loadtest_plan_2026.docx`: 4 of 25 stump-paragraph terms appear (record, request, sample, client); read whether the document names the move
- **REVIEW** `yearend_readiness_standard_2026.pdf`: 6 of 25 stump-paragraph terms appear (record, clients, request, client, outcome, records); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Architecture 1 (target.zip 837ff5a0): two isolated scored readers, each on fresh copies of `prompt.txt` and `target/` (sonnet, medium).

- Reader r273a: named the golden five (EP01, EP02, EP05, EP16, EP22) by correcting the closed-loop test for coordinated omission: each sample's pause-free service time, open arrivals spread over the window and turned across the pods, each held by its pod's pauses from the GC log (uptime lines placed from the start-up lines after the restarts). Ask A 24 of 24 (monitors' requests taken off, the old route before each cutover, the 1 January plan mix rolled back from the CRM through the subscription events); Ask B 12 of 24. Q1 quoted standard 2.2's pause clause with 1.2's "thousands of clients, each working to its own schedule" and the plan's closed workload; Q6 an analytical choice. `score_reader.py --call-key call.fix --call-key call.count`: call 2 of 2, asks 36 of 48 (75.0 per cent), FAIL.
- Reader r273b: the same rebuild and the same five; Ask A 24 of 24 and Ask B 24 of 24 (the "Balance carried forward from legacy billing" notes excluded as restated legacy credits). Q1: no single sentence names the step, the pieces are 1.2, 2.2 and the plan's closed workload read together; Q6 an analytical choice. `score_reader.py`: call 2 of 2, asks 48 of 48 (100.0 per cent), FAIL.
- Verdict on the REVIEW lines: neither reader quoted the plan's Table 1, the generic vocabulary or any file as ranking the endpoints; both answered Q2 none and Q4 nothing.

Gate F failed on both readers: architecture 1 is spent. The determinism judge returned DETERMINISTIC and APPROVE (Gates G and H pass) on the same pack.
