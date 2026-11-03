# leak check, task194

**Verdict: REVIEW.** 14 files read, 42 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, reader, carries, golden, sentence, boundary, record, pressure, closed, kestle, export, decisive, harmless, rejected, nothing, architecture, method, ordinary, checks, inside, reading, measured, thrushgate, shipped, counts

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `LP04_leakage_procedure_rev3.pdf`: carries 7 of 11 distinctive words of the committed call: 'Send the leak detection crew to Thrushgate in week 46, whose own leakage rose by 0.6 l/s, 0.3 l/s more than Ashworth Fol'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `LP04_leakage_procedure_rev3.pdf`: 6 of 25 stump-paragraph terms appear (register, record, pressure, export, reading, counts); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `dma_register_2026-09.xlsx`: names 11 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `large_user_accounts.xlsx`: names 10 of 12 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader (medium effort), fresh copies of prompt.txt and target/ only, nothing solved.

1. Decisive step announced: none. Nearest is LP04 6.1 ("the area whose own leakage rose most ... An area's own leakage is the water lost at night from the area's own mains and service pipes, normalised under 5.1"), the filed estimand.
2. File ranking or scoring the candidates: none.
3. File existing only to help the analyst: none.
4. Figure or name reading as the answer: none.
5. Filed sentences fixing the figure or population: LP04 2 (inlet flow summed over an area's meters; night dated by its 03:00), 3 (03:00 to 04:00 local, half-open, m3/h), 4.1 to 4.3 (night use taken off: households at 1.7 l/h per property, logged large users' metered use plus 6.0 l/h per unlogged non-household), 5.1 (pressure normalisation, N1 1.15), 6.1 and 6.2 (change in normalised own leakage, l/s), 7 (register issue at the start of the baseline nights), Appendix B (the night sets), and the prompt's ask windows and rounding.
6. What decides the main answer: the reader reads LP04 as a fully specified procedure and flags rule application as the risk; it did not identify any step beyond the procedure, and named the PRV raise at D4149 (29 September) as the one event that might read as planted.

Rulings:
- LP04_leakage_procedure_rev3.pdf shared words with the call: harmless, it states the method and night sets and ranks no area.
- dma_register_2026-09.xlsx: harmless, property counts, mains length, meter tags and PRV flags, no leakage, change, rank or score.
- large_user_accounts.xlsx: harmless, account, meter and supply-point listings with no consumption, rank or score.

Realism: names fictional; PDF a plausible Word print (35.7 KB, dated at issue); xlsx metadata human and consistent; works-order numbers ascending as a WMS issues them.

## Solver's-eye read (round 2, after the stage 4 repairs)

Isolated reader (medium effort), fresh copies of prompt.txt and target/ only, nothing solved.

1. Decisive step announced: none. Nearest is LP04 6.1, the definition of own leakage (the filed estimand); it does not say what to subtract or which areas or meters are affected.
2. File ranking or scoring the candidates: none; the find-and-fix outcomes are last year's finds, context.
3. File existing only to help the analyst: none; the register's Instrument units sheet and the accounts' Meter role column read as ordinary metadata.
4. Figure or name reading as the answer: none.
5. Filed sentences fixing a figure or population: LP04 2, 3, 4.2, 4.3, 5.1, 5.2, 6.1, 6.2, 7 and Appendix B, and the prompt's ask windows and units. Main thread: each literal execution is the golden's reading; LP04 4.1 to 6.2 executed with no boundary test names Kestle Hill and own leakage read literally names Thrushgate (asserted in checks.py).
6. What decides the main answer: an analytical reconstruction of each area's own leakage across systems, beyond the procedure's deductions; no planted decoy or hidden rule found.

Rulings:
- LP04 4.1 reworded: harmless, standard component analysis, no answer, no announcement.
- dma_register_2026-09.xlsx and large_user_accounts.xlsx with the Meter role column: harmless, rank nothing; the role column is ordinary asset-register metadata.
- PRV log, works orders and contacts around 29 September at D4149: harmless, routine operations with an ordinary CMMS trail.
- billing_account_events_extract.csv: harmless, an authentic-looking OCC/VAC/CONV extract with posted dates lagging effective dates.
- gis_boundary_valves.geojson: harmless, no record out of place.

Realism note fixed before ship: the billing extract's posted times (VAC rows at 10:00, CONV at 12:00) spread as a batch posting run would.

## Solver's-eye read (round 3, after the second repair)

Isolated reader (medium effort), fresh copies of prompt.txt and target/ only, nothing solved.

1. Decisive step announced: none. Nearest is LP04 6.1's definition of own leakage, the filed estimand.
2. File ranking or scoring the candidates: none.
3. File existing only to help the analyst: none.
4. Figure or name reading as the answer: none.
5. Filed sentences fixing the computation: LP04 2, 3, 4.1 to 4.3, 5.1, 5.2, 6.1, 6.2, 7 and Appendices A and B. The reader reads them as filing the whole method.
6. What decides the main answer: the reader reads it as following LP04 plus correct field and unit reading, and flags a rule 3 risk. Main thread ruling: executing LP04 3 to 6.2 literally with every field and unit read correctly names Kestle Hill (asserted in checks.py), which is the default path's wrong answer; the golden needs the area water balance across neighbouring inlet meters that no LP04 sentence states, to measure the 6.1 estimand (water lost from the area's own pipes). That the cold reader took the procedure as sufficient is the stump working, not rule application deciding the call; the judge ruled decisive_step analytical in r1 and r2.

Rulings:
- LP04 (sections 2 and Appendix A changed): harmless, no result, recommendation or ranking, no announcement.
- Historian quality codes and billing posting times: harmless, authentic SCADA and billing behaviour.
- AMR around the 14 October meter exchange: harmless, a real rollover and exchange overlap; the reconditioned register's non-zero start reads as a refurbished meter.
