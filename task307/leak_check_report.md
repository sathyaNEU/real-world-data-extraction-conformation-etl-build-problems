# leak check, task307

**Verdict: REVIEW.** 15 files read, 33 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: dropped, output, nesvik, harmless, architecture, driver, decisive, register, honest, record, standard, prototyped, banned, operating, counters, inside, generator, choice, default, programme, credited, reflex, hourly, running, readable

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `outage_planning_note_2027.docx`: \bdesign note\b|\bgenerator\b x1: ..., in each of the last five winters, 2021/22 to 2025/26, in MWh at the generator terminals. 4 Cost 4.1 Refurbishment cost is the runner s...
- **REVIEW** `production_report_2025.pdf`: \bdesign note\b|\bgenerator\b x1: ...02.4 Nesvik 541.8 541.4 Definitions Generation is gross energy at the generator terminals, taken from the station historian with each hour's mean out...

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `runner_refurbishment_quote_2027.pdf`: golden figure 400 appears: ...K) Total (NOK) OSD-G1 R-301 shop refurbishment 18,400,000 4,600,000 23,000,000 OSD-G2 R-302 shop refurb...
- **REVIEW** `runner_refurbishment_quote_2027.pdf`: golden figure 650 appears: ...,000 SDL-G1 R-205 shop refurbishment 14,600,000 3,650,000 18,250,000 SDL-G2 R-410 shop refurbishment 13...
- **REVIEW** `runner_refurbishment_quote_2027.pdf`: golden figure 501 appears: ...bishment 14,200,000 3,550,000 17,750,000 NSV-G1 R-501 shop refurbishment 14,400,000 3,600,000 18,000,00...
- **REVIEW** `runner_standard_TS07_rev3.pdf`: golden figure 400 appears: ...e runner's blades and band. The repair limit is 2,400 cm2 of pitting. 5 Repairs 5.1 A weld repair is re...
- **REVIEW** `outage_planning_note_2027.docx`: carries 7 of 11 distinctive words of the committed call: 'Sørdal Kraft should spend its 2027 summer runner refurbishment on Nesvik G1, sparing 67,000 MWh of generation in the 202'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `outage_planning_note_2027.docx`: 3 of 25 stump-paragraph terms appear (nesvik, inside, generator); read whether the document names the move
- **REVIEW** `production_report_2025.pdf`: 3 of 25 stump-paragraph terms appear (output, nesvik, generator); read whether the document names the move
- **REVIEW** `runner_standard_TS07_rev3.pdf`: 4 of 25 stump-paragraph terms appear (nesvik, register, record, standard); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader (Sonnet, medium), fresh copies of prompt.txt and target/ only, nothing solved.

1. Decisive step announced: none. Nearest is the planning note 2.4 ("each unit is assumed to run in each year of the planning window as it ran in 2026"), a stated planning assumption, not a pointer.
2. File ranking or scoring the candidates: none. The quote lists prices; no file holds generation per million kroner or a ranking.
3. File existing only to help the analyst: none. TS-07 and the planning note are governing documents; the register, tag map and counters are ordinary reference files.
4. Figure or name reading as the answer: none; no unit is singled out.
5. Filed sentences fixing the figure or population: TS-07 4.2 (total pitted area, limit 2,400 cm2), 2.1 (history follows the runner), 5.1 (pitting after weld repair), 6.1 and note 3.1 (14 weeks from 1 December of the crossing year), note 1.1 to 1.3 (present runners, condition at 31 December 2026, outages beginning 2027 to 2031), 2.1 to 2.4 (one refurbishment, refurbished runner does not reach the limit, others keep their runners, 2026 duty carried forward), 3.2 (mean generation over the 14 weeks of the last five winters, Norwegian time, at the terminals), 4.1 (quote excluding VAT), the production report definitions. The reader notes no filed sentence gives a pitting growth rate: the projection from the inspection history is left open. Main thread: every literal execution above is the golden's reading (fork table SF1 to SF7); the projection is the analytical step, forced by the inspection pairs.
6. What decides the main answer: the stated sentences fix valuation, window and cost; the one open element is projecting each runner's pitting from its inspection history to the crossing year, which no file announces. Main thread: that projection (wear per hour inside the part-load band, read from each unit's own output) is the analytical decisive step; the stated rules alone do not pick the unit, since the default per-running-hour projection under the same rules picks Nesvik G2 (checks.py analyst test).

Rulings on the REVIEW lines:
- outage_planning_note_2027.docx, "generator terminals": harmless, the plant-engineering metering point.
- production_report_2025.pdf, "gross energy at the generator terminals": harmless, the gross basis definition.
- runner_refurbishment_quote_2027.pdf, three numbers coinciding with golden figures: harmless, ordinary quote content (ex-VAT, VAT, total); inputs, not answers.
- outage_planning_note_2027.docx, shared words with the call: harmless, the note states conditions and rules, ranks nothing and names no choice.
- Stump-vocabulary lines (production_report_2025.pdf, runner_standard_TS07_rev3.pdf; output, nesvik, record): ruled in the main thread, harmless, common words; neither document ties pitting to an output band.

Realism: nothing reads planted. One tell to fix: the docx's word/styles.xml and stylesWithEffects.xml are the python-docx default template (350 to 440 KB). The planning note reads terse but plausible.

## Solver's-eye read (round 2, after the asks rework)

Isolated reader (Sonnet, medium), fresh copies of prompt.txt and target/ only, nothing solved.

1. Decisive step announced: none. Nearest are TS-07 6.1 and note 3.2 (they define the quantity) and note 2.4 (a stated assumption).
2. File ranking or scoring the candidates: none. The quote lists prices only.
3. File existing only to help the analyst: none. Tag map, the register's Driftsomrader sheet and the counter readings are ordinary support.
4. Figure or name reading as the answer: none; prices are inputs.
5. Filed sentences fixing the figure or population: TS-07 4.2, 2.1, 5.1; note 1.1 to 1.3, 2.2, 2.3, 3.1, 3.2, 4.1; the production report's definitions of generation, a start and a trip; the prompt's "since the start of 2016". Together they fix the population, unit and comparison and leave the projection to the limit to the analyst. Main thread: every literal execution is the golden's reading (fork table SF1 to SF16).
6. What decides the main answer: an analytical choice, the year each runner reaches the limit projected from an irregular inspection series with repairs and runner swaps; the semantic layers around it are closed by filed text; nothing reads planted.

Rulings:
- "generator terminals" in the planning note and production report: harmless, the measurement point.
- Quote numbers coinciding with golden figures: harmless, prices are inputs, nothing derived appears.
- Planning note's shared words with the call: harmless, it states basis, window, valuation and cost convention, no recommendation or ranking.
- protection_log_2016_2026.csv: harmless, reads as an authentic control-centre log (mixed event types, generator and 132 kV line objects, relay codes, no flag or count column, no counting hint).
- Production report's start and trip definitions: harmless, they define the quantities and give no counting procedure.

Realism: nothing reads LLM-generated; toolchain metadata plausible (Word for Microsoft 365, named authors, revision 7, no default-template tell); no dates after the setting.
