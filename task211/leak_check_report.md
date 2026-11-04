# leak check, task211

**Verdict: REVIEW.** 22 files read, 21 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: halvorne, tessard, product, centre, change, patient, letter, tablet, golden, register, colour, sentence, pellbrook, record, decisive, corwen, second, distribution, patients, reader, attribution, redraws, method, window, reading

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `ms12_interchangeable_product_surveillance.pdf`: golden figure 2.0 appears: ...largest excess, provided that excess is at least 2.0 qualifying visits per 1,000 patient-months. If no...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `corwen_film_coat_notice.pdf`: 5 of 25 stump-paragraph terms appear (centre, change, tablet, corwen, distribution); read whether the document names the move
- **REVIEW** `halvorne_site_change_notice.pdf`: 5 of 25 stump-paragraph terms appear (halvorne, centre, change, tablet, distribution); read whether the document names the move
- **REVIEW** `ms12_interchangeable_product_surveillance.pdf`: 7 of 25 stump-paragraph terms appear (product, patient, tablet, record, patients, attribution); read whether the document names the move
- **REVIEW** `purchasing_manual_and_service_schedule.pdf`: 3 of 25 stump-paragraph terms appear (product, centre, distribution); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Should we send one of our levetiracetam 500 mg tablets to the contract laboratory's third-quarter re-test on the strength of January to June 2026, and if so, which one, and how many seizure-related emergency visits per 1"

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `ms12_interchangeable_product_surveillance.pdf`: names 11 column(s) of the data files verbatim (approved, arrival, diagnoses, fills, interchangeable, month): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

### Round 1 (stage 4, target.zip f7e348d0, one isolated reader at medium effort), and the main thread's rulings

- Q1 none: the closest is MS-12 2.6 (the visits the same patients, over the same days of supply, would have had if the
  product's tablets released and delivered the drug as the reference's do), which files the estimand and not how the
  baseline is built; the site-change notice and the product register show who made what and when, and nothing says to
  compare by site or by appearance. Ruling: no decisive-step sentence.
- Q2 none: the supply monitor gives fills and tablets by month and centre for every product, no visits and no ranking.
- Q3 the two notices and the key tables (claims crosswalk, item list, pack register, ship-to accounts), read as ordinary
  organisation records. Ruling: harmless.
- Q4 none: MS-12's 2.0 bar is policy and the list prices mark the reference, not a verdict.
- Q5 MS-12 2.1 and 2.3 to 2.6 and 3.1 fix the population, the visit definition, the patient merge, the supply and its
  attribution, the patient-month and the referral bar; the counterfactual method is not filed. Ruling: the estimand is
  filed and the method stays open where the data separate the candidates (the judge's family 4.07 to 4.45, one bin).
- Q6 an analytical choice (how the counterfactual visit rate is estimated); parts of the work are rule application
  (2.3 to 2.5), nothing planted. Ruling: rule 3 holds; the judge's Gate H reads the same (analytical).
- Q7 faint tells only (one live-from date in the claims crosswalk, the four-week spacing of the centres' change dates,
  identical scope text on the backorder notices). Ruling: kept; system exports carry such regularity and none decides.
- Q8 the backorder ask's open points (a notice opening while another is open, a backorder running past 30 June): none
  occurs in the shipped records, and the judge reproduced every backorder figure under the item list's own dates.
- REVIEW lines (MS-12's policy constants, its ordinary column words): harmless, the committee's own document.
