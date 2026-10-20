# leak check, task199

**Verdict: REVIEW.** 17 files read, 63 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: action, clause, sentence, protocol, window, decisive, golden, denominator, measured, definitive, extract, counts, population, volume, asserted, reading, baseline, published, record, pattern, activity, exposure, material, nothing, delivery

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `diccionario_datos.md`: 3 of 25 stump-paragraph terms appear (action, extract, material); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Where should the next verification mission go, and what rate of recorded collective actions per 100,000 residents should the watch note print for that city?'

## 6 ranking artifacts (REVIEW 4, INFO 3)
- **REVIEW** `envios_resena_andina.csv`: names 6 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rac_acciones_2024.csv`: names 6 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rac_acciones_2025.csv`: names 6 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rac_acciones_2026.csv`: names 6 of 6 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `incidencias_viales.csv`: names 6 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `resumen_mensual_rac_2025.csv`: names 4 of 6 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `tabla_municipios.csv`: names 6 of 6 answer-set candidates; confirm it does not rank them on the decision question

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

## Solver's-eye read, wave 6 audit (the shipped pack, target.zip 97dd76fb)

Run because `leak.py` overwrote this build's original reader section before that bug was fixed, so
no reader evidence survived. Pack and `prompt.txt` only, scored by `score_reader.py`.

### Gate F has failed on this build, measured

The reader filed **Tibu at 92.2 actions per 100,000 on 137 action-days**, which is the shipped call,
its rate and its window count. Confidence about 75 per cent. Every call figure scored hit.

It reached the decisive step unaided and described it in the build's own terms: whether the recorded
rise is activity or extra coverage. It then found the evidence, that delivered items rose six to
seven times from 1 April 2026 in three cities that each gained two new sources while Tibu's feed was
unchanged at 1.00 times against a 2.4 times rise in recorded actions. It named Sardinata as the
alternative and the coverage trap, and rejected it.

So the coverage correction, which is this build's whole mechanism, was found by a medium-effort
reader in a single pass from the data alone. The protocol sentence it quoted, "Los registros del
Observatorio son la evidencia de esa actividad y no su medida", points at the question without
answering it, which is the shape that is meant to hold; it did not hold here.

### Where it was unsure

Its answer to question 5 notes that the protocol never defines the measure of the rise, and that a
literal raw-count reading gives Sardinata. So the determinacy of the ranking measure is open on the
shipped text, which is a separate finding from Gate F and belongs to whoever repairs this.
