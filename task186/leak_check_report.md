# leak check, task186

**Verdict: REVIEW.** 12 files read, 25 golden figures and 11 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: object, routes, export, golden, stations, population, register, record, library, decisive, images, station, tallis, measure, projection, objects, records, threat, sentence, catalogue, device, return, default, inside, nothing

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `SCS-04_screening_officer_competency_standard_rev6.pdf`: 6 of 25 stump-paragraph terms appear (record, images, projection, records, threat, return); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader, two rounds)

Every REVIEW line above is ruled harmless by the reader in each round; neither round found a ranking file, a helper file or a figure that reads as the answer, and both answered question 6 with an analytical choice. The round-2 reader itself took 'not shown before' at the image level, one of the build's live traps.

### Leak reader, round 1 (2026-11-01, isolated, Sonnet at medium effort, on target.zip b4586dea)

1. Decisive step: no file announces it; the closest is SCS-04 s4 (detection performance of every officer endorsed on 30 November, over the officer's CT-lane screening in that year) with s3 ("The probability that the officer detects a prohibited item carried in a passenger's cabin bag at the X-ray screen of a CT lane"); neither says how to estimate it from the TIP records.
2. Nothing ranks the officers (the TIP events are raw hit and miss rows).
3. No helper file (leave, queue times, CBT sessions and the TIP catalogue read as distractors or context; logins and the unit register are needed keys).
4. Nothing reads as the answer (the 80 per cent line and the 20-hour minimum come from the standard).
5. The standard's 80 per cent sentence (list the endorsed officers whose detection performance is below 80 per cent); s3's X-ray time apportionment and s5's 20 hours serve the monthly ask; s4 files the population and window, the estimation method stays open.
6. An analytical choice: the standard defines detection performance as a probability for real items, the only evidence is projected-image outcomes, so the estimand must be estimated from them; raw hit counts near 95 per cent separate officers only once the estimate is made properly; nothing planted.
Sweep flag: SCS-04 harmless (definitions, thresholds and records, no estimation method, interval, minimum sample or aggregation rule).
Realism: none clearly generated; minor: the projection settings JSON carries one projection probability and one category list on every lane.

### Leak reader, round 2 (2026-11-02, isolated, Sonnet at medium effort, on target.zip c1a98fb1)

1. Decisive step: SCS-04 s3 ("The probability that the officer detects a prohibited item they have not been shown before, carried in a passenger's cabin bag, at the X-ray screen of a CT lane") names no method; the reader took "not shown before" with the TIP image numbers to point at first-exposure images (the image-level reading, one of the build's remaining traps); s4 points to the login-to-staff mapping.
2. Nothing ranks the officers (raw hit and miss rows; CBT scores are context).
3. No helper file (the projection settings and queue times read as context or distractors).
4. Nothing reads as the answer.
5. s3 (X-ray time split among the officers on the lane; start-up test images are not passenger bags; the screening year and quarters; Sydney time), s4 (the population endorsed on 30 November; below 80 per cent comes off), s5 (20 hours a month); the main figure filed only as the probability of detecting an item not shown before over the year's CT screening, its construction left to the solver.
6. An analytical choice: each officer's detection rate on first exposures against 80 per cent; its caution: read as a definition to apply, it edges toward rule application or semantics; repeats, small samples and uncertainty still need analysis.
Sweep flag: SCS-04 harmless (the estimand, thresholds and definitions; it does not announce the trap or the computation; the test-image note serves the bag ask).
Realism: none; the identical projection probability and category list across lanes in the settings JSON plausible as a system default.

