# leak check, task155

**Verdict: REVIEW.** 14 files read, 40 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: casual, roster, offers, camberwell, werribee, decisive, rostered, carries, nothing, published, register, forecasting, workforce, payroll, take-up, separate, rosters, history, system, driver, unfilled, december, season, analyst, another

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `relief_crew_placement_standard.pdf`: carries 5 of 6 distinctive words of the committed call: 'Place the relief crew at Camberwell; it will work 1,090 hours there.'
- **REVIEW** `wp05_casual_callin_procedure.pdf`: carries 5 of 6 distinctive words of the committed call: 'Place the relief crew at Camberwell; it will work 1,090 hours there.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `ea_2024_casual_employment_summary.pdf`: 5 of 25 stump-paragraph terms appear (casual, roster, rostered, payroll, system); read whether the document names the move
- **REVIEW** `relief_crew_placement_standard.pdf`: 10 of 25 stump-paragraph terms appear (casual, roster, camberwell, werribee, rostered, published); read whether the document names the move
- **REVIEW** `wp05_casual_callin_procedure.pdf`: 11 of 25 stump-paragraph terms appear (casual, roster, offers, camberwell, werribee, rostered); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `christmas_roster_2026_published.xlsx`: 17624 ISO dates after 2026-11-12, e.g. 2026-11-27, 2026-11-28, 2026-11-29, 2026-11-30, 2026-12-01
- **REVIEW** `vic_school_terms_public_holidays_2025_2026.csv`: 5 ISO dates after 2026-11-12, e.g. 2026-12-18, 2026-12-25, 2026-12-26

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader: one isolated general-purpose agent (sonnet, medium) on fresh copies of `prompt.txt` and `target/`, 2026-10-31,
after the reship replaced the module notes with the WP-05 call-in procedure and dropped the transmittal. It read every
file and solved nothing.

1. Decisive step: none stated. It quotes the placement standard sections 3 and 4 (the crew goes to the store where it
   will work the most hours that would otherwise go unworked, forecast as if the crew were placed at none) and notes
   that they name the quantity and "do not say how to forecast it".
2. Ranking or scoring file: none. The trading plan holds budgets and customer counts; the call-in files are history.
3. Helper-only file: none. No dictionary, manifest or field notes ships; the standard and WP-05 read as policy.
4. Answer-like figure or name: none. No store, hours total or forecast is stated anywhere.
5. Literal sentences: the standard sections 3 to 5, read as the store with the most forecast unfilled paid hours of its
   published open lines over the four weeks, with every store's open shifts posted to call-in, and the crew hours as
   the placed store's open lines' paid hours. This is the golden's estimand.
6. What decides: an analytical choice, forecasting each store's call-in fill from the history and the offer
   mechanics; field readings (UTC against store time, the cost-centre history, the legacy layout) and the WP-05 rules
   are secondary, and nothing reads as planted.

Sweep lines: the answer-figure lines on the standard and WP-05 are harmless (the prompt's own nouns; the documents
state the estimand, not the result); the roster workbook's dates after 12 November are the published forward roster;
the school terms file's dates are gazetted holidays. All harmless.

Realism: reads as real retailer exports (the legacy roster's mixed-case headings and 12-hour times, VACANT lines with
no employee number, the KWS file's ISO layout, the UTC call-in register, payroll's previous employee numbers and
cost-centre dates). Mild notes, each ruled harmless: the PDFs carry no producer metadata; the offers file opens on
14 August 2025, before its name's first shift date, because offers go out before the shift; the legacy RELIEF status
is the 2025 crew's own lines, which the standard's description of the crew covers.
