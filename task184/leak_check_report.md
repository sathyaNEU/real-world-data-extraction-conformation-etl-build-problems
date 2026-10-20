# leak check, task184

**Verdict: REVIEW.** 16 files read, 45 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: window, weight, decisive, occurred, records, nothing, checkpoint, airport, carries, covered, shipped, graded, construction, sentence, decision, occurrence, windows, architecture, pattern, document, summer, stand-down, ladder, timestamps, classes

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `harbourgate_patrol_tasking_contract_2027.pdf`: 5 of 25 stump-paragraph terms appear (occurred, records, nothing, covered, classes); read whether the document names the move
- **REVIEW** `kcp_rms_extract_notes.md`: 4 of 25 stump-paragraph terms appear (records, occurrence, timestamps, classes); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 6)
- **REVIEW** `kcp_cis_offence_extract_2025.csv`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `kcp_rms_offence_extract_2027-01-22.csv`: names 5 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `footfall_sensor_register.csv`: names 4 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `harbourgate_licensed_premises.csv`: names 3 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `harbourgate_location_register.csv`: names 5 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `kcp_rms_extract_notes.md`: names 3 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `kelverstoke_beat_map.csv`: names 3 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `kelverstoke_street_gazetteer.csv`: names 3 of 6 answer-set candidates; confirm it does not rank them on the decision question

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

One isolated reader at medium effort, twice: the first pass before the agreement's clause 4.4, the prompt's pins
and the widened window shapes, the second after them. It saw only a fresh unzip of `target.zip` and `prompt.txt`.

1. **Which sentence or file tells you the decisive step?** Nothing does. Pass 2: "No sentence names the
   construction. The contract only fences it in." It quoted 4.1, 4.2 and 4.4, which fix the population, the time
   that governs and the sources that may not be used, and none of which says how to treat a window.
2. **Which file ranks or scores the candidates?** "None." The 2026 patrol plan records the hours the patrol
   worked, which the reader read as last year's plan, not a ranking.
3. **Which file exists only to help the analyst?** The licensed premises register and the footfall feed, both of
   which it noted are exactly the proxies clause 4.4 bans for placing an offence in time, and both of which are
   declared distractors or ask organs. The 2026 plan read as a stub at pass 1 and was rewritten into the monthly
   return clause 5.1 of the 2026 agreement called for.
4. **Which figure or name reads as the answer?** "Nothing does." The nearest candidate it named was the 2026
   plan's six worked slots, which differ from the golden eight.
5. **Which filed sentence, read literally, fixes the figure?** Clause 4.1 with Annex B and clause 3.1: the five
   classes at the five registered locations, 25,020 offences over the two seasons. That is the golden's population,
   and the reader reached the golden's own figures from it.
6. **What decides the main answer?** "(a), an analytical choice: how to place a window offence inside its window."
7. **What settles the placement?** "No sentence prescribes a rule." It listed what the pack forbids (footfall,
   trading hours, premises, the 2026 plan, any other record) and what it leaves open, and chose the uniform spread
   because it "uses nothing outside the window".
8. **Its pipeline** landed the golden slate and every one of the 42 cell figures, which is the reproducibility
   check this read is for. At pass 1, before clause 4.4, it weighted the windows by footfall instead and filed a
   different slate, which is the fork the clause now closes.
9. **The three asks** reproduced the goldens, with two readings flagged and both now pinned in the question.

Nothing was quoted for question 1 at either pass, no file was named for question 2, and question 6 came back
analytical at both. The findings from pass 1 (the footfall weighting, the window regularity, the stub workbook) are
fixed in the generator and recorded in the design note's `## Tried and rejected`.


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

Run because this build shipped with no scored reader evidence, and because every shipped build measured
so far has failed. The reader held only a fresh unzip of `target.zip` and `prompt.txt`, with the figure
names (not values) from `generator/figures.json`, and was scored key by key by
`.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured

| block | hit |
|---|---|
| main call | **11 of 13** |
| ask figures | **75 of 97** (77.3 per cent) |

It landed the slate and the season total (about 4,050 contracted offences, 4,047.64 unrounded) and named the decisive step in its own words, spreading each offence uniformly over the slots its window overlaps and weighting by overlap time, then scoring the window-start, window-end and midpoint variants against it. It said a filed clause sent it there: clause 4.4, that where the record gives the earliest and latest time no other source may be used to place the offence within that period, read together with the recording standard's 3.3. That is readability screen test 1, a filed sentence naming the decisive quantity, and the reader quoted it.

```
call figures   11 of 13 hit
call inputs    2 of 2 hit (shared route figures, not the verdict)
ask figures    75 of 97 hit (77.3 per cent)

FAIL  the reader landed the call. Gate F has failed and the architecture is spent:
      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.
```

The repair re-sites the ladder, not the wording: a call a blind reader lands at medium effort is a ladder
whose decisive rung is readable, and `supplemental-stumping` 1.1c puts the reader above the author's own
cracker sheet wherever the two disagree.
