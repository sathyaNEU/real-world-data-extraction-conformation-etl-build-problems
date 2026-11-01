# leak check, task187

**Verdict: REVIEW.** 13 files read, 21 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: turbulence, shortfall, record, warranted, ten-minute, default, decisive, standard, sentence, comparison, turbines, generator, matched, schedule, october, nacelle, partial-load, domain, curtailment, normal, operation, spread, exchange, method, production

## 1 file names (REVIEW 1)
- **REVIEW** `lost_production_2024_25.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `OM-07_blade_campaigns_and_lost_production.pdf`: carries 11 of 13 distinctive words of the committed call: 'Book the summer 2027 leading-edge repair campaign on CH04; the repaired blades should recover 100 MWh (to the nearest 50'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `OM-07_blade_campaigns_and_lost_production.pdf`: 10 of 25 stump-paragraph terms appear (record, warranted, ten-minute, standard, turbines, schedule); read whether the document names the move
- **REVIEW** `TSA_schedule_3_warranted_power_curve.pdf`: 4 of 25 stump-paragraph terms appear (warranted, ten-minute, standard, schedule); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read, wave 6 audit (the shipped pack, target.zip 6f6e1174)

Run because `leak.py` overwrote this build's original reader section before that bug was fixed, so
no reader evidence survived. Pack and `prompt.txt` only, scored by `score_reader.py`.

### The call held. The ask layer did not.

| block | answered | hit |
|---|---|---|
| main call | 1 | **0** |
| the twenty per-turbine loss figures | 20 | **20** |

It filed **CH07** against a golden of **CH04**, at about 35 per cent confidence, so the ladder is
carrying the call. It also named the lure itself without being asked: CH09 "looks like the answer"
and is not, because its blades went up in April.

Then it took all twenty loss figures exactly, downtime and curtailment for all ten turbines. Its own
account of why is the finding: "the loss tables are rule application with Layer 1 mess", and it
executed the standard's clauses 4.4 to 4.6 literally to get them. So those figures are not holding
anything, and a response that files CH07 still banks the whole ask block.

### What it said about the decisive step

It quoted the campaign-valuation clauses and then said what they do not fix: "Section 2.4 fixes the
campaign estimand but not the 'as new' reference." That is the open method, and it is why its
confidence was 35 per cent: it built an as-new reference from CH09's own post-swap months and was
not sure that was intended.

## Solver's-eye read, 11-01 re-check (the 13-file pack and the reworded prompt)

1. Decisive step: none quoted. OM-07 2.3 and 2.4 fix the estimand (the energy the repaired blades would add, in the same winds, had the blades been as new) and no method.
2. Ranking file: none on the campaign. lost_production_2024_25.xlsx ranks last year's downtime and curtailment, a different quantity and year (the declared distractor).
3. Helper files: the state-code table, the register's two footer lines, the lost production Notes sheet and the pad key, each a plausible real artefact.
4. Answer-like figure or name: none.
5. OM-07 2.4 to 2.6 and 3.1 fix the window (twelve months to 30 September 2026), normal operation (states 10 and 20) and CH09's own blade-set months; the as-new reference is left open.
6. An analytical choice (the as-new counterfactual); the stated rules place the window and population only.

REVIEW verdicts: the lost production Notes sheet harmless (provenance, period, basis, units); OM-07 sharing the prompt's nouns harmless (the governing standard, no method); OM-07 and Schedule 3 domain vocabulary harmless. Realism: none (one shared commissioning date, plausible for one project). Ask readings raised: counter reads against SCADA energy for metered generation, gross export against export net of import, both read by the determinism judge.
