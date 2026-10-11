# leak check, task180

**Verdict: REVIEW.** 12 files read, 19 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: decisive, architecture, register, hydrogen, agency, comparison, design, heating, window, matched, method, acetylene, supply, graded, stated, channelling, driver, related, carried, pattern, domain, new-user, analytical, extract, analyst

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `SOP-PV-14_signal_refinement.pdf`: carries 6 of 8 distinctive words of the committed call: 'Open the formal assessment on corinurad (Uralexa) and acute kidney injury.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `SOP-PV-14_signal_refinement.pdf`: 3 of 25 stump-paragraph terms appear (agency, carried, extract); read whether the document names the move
- **REVIEW** `registry_extract_notes.md`: 4 of 25 stump-paragraph terms appear (register, agency, matched, extract); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt form (clean)

## Solver's-eye read

Pass 1, architecture 3: one isolated reader on Sonnet, 2026-10-11.

The reader saw only a fresh scratch copy of `prompt.md` and `target/`.

1. none. The nearest is SOP-PV-14 §1.2 ("The committee asks one question of each signal: does starting the medicine raise the risk of the event in the month after the start?"). It states the question, not the comparison group, reference window or estimator.
2. none. `pv_signal_screen_2026Q3.xlsx` scores the three pairs only by PRR on spontaneous reports, and that ordering happened to put corinurad/AKI first (17.74, tasorexant/Fall 10.37, velaglutide/Pancreatitis 6.35). Its About sheet says it does not measure how often an event happens. No file holds a registry rate ratio, the 2025 admissions or the caused count.
3. `atc_ddd_index_2026.csv`. A 12-row index of exactly the codes in the extract, carrying the remarks "Erstatter M04AX02" and "Midlertidig kode; afløst af M04AB06 fra 2024-01-01". Runner-up: `population_and_admissions_2022-2025.csv`, cut to the three annex A events.
4. none. The PRRs, Q3 counts and the PSUR's rates are spontaneous-report context. The only medicine the documents lean on is tasorexant (minutes §3), which reads as an expectation, not a result.

**Plan (summarised).**
- Definitions from the SOP and the notes.
- New users across both corinurad codes, with returns cancelled and residence applied.
- Events with transfers merged.
- Decide within person: days 1 to 30 against the same person's days -365 to -31, leaving out the month before the start because events trigger prescribing.
- Rough pass: corinurad/AKI about 2.5 to 2.6, the others about 1.0, users against matched non-users 3.8 for tasorexant/falls.

**REVIEW lines.**
- SOP-PV-14: harmless. The shared words are open, formal, assessment (§1.1, §8.1) and the event names listed side by side in annex A. No medicine is named as supported.
- registry_extract_notes.md: harmless. The terms are ordinary file-description words, and the notes name no comparison design.

**Realism notes (deferred to stage 6b).**
- Prescriptions are flat across weekdays and holidays (25 December, 1 January).
- 27.5 per cent of LPR3 contacts start at exactly 15:59.
- Round cohort and person counts (58,000, 74,000, 16,900, 446,700, 583,700), and no activity after death or emigration.
- Immigration dates are flat for 1972 to 2016, with none in 2017, 647 on 2 January, and no emigration before November 2021.
- The PSUR's Danish exposure (about 6,400 patient-years) is far above the registry's (about 1,350 tablet-years), and a one-page PSUR summary is not a real format.
- The notes date the extract delivery (4 September) "for the refinement of the Q3 2026 signals" before the Q3 screen ran (6 October).
- The SOP gives no design, reference period or criterion for "supported" (by design).
- The screen lists only 11 pairs out of 812,446 reports, and case numbers run in blocks by medicine.

**Disposition (main thread).**
- **Fixed before the solver round** (data only, no document changed, so no second read):
  - Q3: the code list keeps its validity dates and loses its narrated remarks. The notes already present it as the
    delivered code list for the extract's `atc` field.
  - Q2's ordering: the screen's cumulative case counts now put tasorexant/Fall first on the PRR too (13.85, against
    corinurad/AKI 11.18 at 24 cases and velaglutide 6.35); no screen count equals a golden figure. Picking by disproportionality now lands on the naive rung, not the
    answer.
- **Deferred to stage 6b:** every realism note above, plus fictional ATC codes that sit on real assignments (M04AX02
  is pegloticase).
- **Watch item for the solver round:** the reader planned a within-person comparison unprompted. The STOPPING RULE
  applies if solvers do the same.
