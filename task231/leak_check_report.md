# leak check, task231

**Verdict: REVIEW.** 14 files read, 47 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reading, architecture, vendor, export, district, network, co-movement, register, readable, judged, decisive, pooled, comparison, checks, sentence, records, settled, record, readings, profile, nights, october, reference, family, forecast

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `sdhd_ess_atmospheric_2026_27.csv`: golden figure 27,330 appears: ...scheduled ESS4702,2027-02-08T16:00:00Z,-67,-98,79,27,330,scheduled ESS4702,2027-02-08T17:00:00Z,-61,-117,6...
- **REVIEW** `sdhd_ess_atmospheric_2026_27.csv`: golden figure 33,118 appears: ...5,scheduled ESS4899,2026-10-02T00:00:00Z,67,12,67,33,118,scheduled ESS4899,2026-10-02T01:00:00Z,73,5,62,88...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `quillan_air_temperature_qc_configuration_v4_3.pdf`: 4 of 25 stump-paragraph terms appear (reading, district, network, readings); read whether the document names the move
- **REVIEW** `quillan_service_agreement_schedule_b.pdf`: 4 of 25 stump-paragraph terms appear (vendor, district, network, october); read whether the document names the move
- **REVIEW** `sdhd_road_weather_data_quality_standard_rev2.pdf`: 3 of 25 stump-paragraph terms appear (vendor, district, october); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `sdhd_rwis_preseason_checks_oct2026.xlsx`: names 8 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `sdhd_rwis_site_register.xlsx`: names 8 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question

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

One isolated reader (sonnet, medium) on a fresh copy of `prompt.txt` and `target/` only, 2026-10-13.

1. Decisive step: quotes standard section 4.2 ("A firm whose business ceased trading on or before the frame date is out of scope for the round, whether or not the Brevland Business Register yet records its closure.") with the register notes' "A company that has stopped trading but whose closure has not been registered does not appear."; says the denominator must be corrected beyond the register and that no method is given. Ruling: the estimand pin and the incomplete-source statement `determinism-check` section 1 requires (WHAT); the decisive step is how the unregistered closures are estimated (HOW), which no file states. Harmless.
2. Ranking file: none.
3. File only there to help: none; the register notes point at the gap "but a real register would plausibly write that note". Harmless.
4. Figure or name reading as the answer: none.
5. Literal reading of section 4.1: the population is the invited firms trading on 1 September; numerator the firms with a first return by 17:00 Brevland time on 25 September (15:00 UTC), each once; firms with no recorded status stay in the denominator unless shown ceased, while section 4.2 puts unrecorded closures out of scope, so the method for finding them is left open. Ruling: executes to the golden's estimand; the method stays open as designed.
6. What decides: an analytical choice (estimating the in-scope denominator when the register is incomplete); field readings and the time zone are Layer 1. Caution raised: a single clean signal (ceased call outcomes) could collapse it; ruling: the call records confirm a closure only when someone answers, the call-centre route is rung R2 and files four extension regions (asserted).

Review lines: the standard (harmless, the rate definition and scope rule, no method), the register notes (borderline, leaning harmless; a genuine extract limitation, no method), the June balances (harmless, opinions, no response data), the invitation list (harmless, row level), the calendar (harmless, real forward entries).

Realism tells and dispositions:
- Main closes on Christmas Day 2020 and 2026: fixed in the generator (the December close moves to 23 December when the Friday is the 24th or 25th; the post room keeps the holidays).
- Manifest entries with empty `extracted_at`, `rows` and `owner` for documents: fixed (documents carry their issue date and owner).
- A thin one-page questionnaire: fixed (the firm's details and how to return it).
- A tidy data dictionary, generic region names: harmless.

Ask readings raised: firms reached (BCB only or both teams and inbound) and calls placed (code 71 legs): closed by the outcome codes' notes (reached on either kind of call; code 71 continues the same call) and the dictionary's direction field. June late returns (time zone; denominator by the cut-off or by the close): standard section 2.4 and 4.3 fix 17:00 Brevland time and the reach time, and a share of the region's June returns counts every June return. Refreshment (Rev. 2 or Rev. 2.1 groups; which rounds count): the dictionary's crosswalk maps both to the survey's nine groups, and a recruit's returns can only be its own rounds from March 2026, the September round included. No change.
