# leak check, task303

**Verdict: REVIEW.** 16 files read, 9 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: claims, condition, lifetime, policy, history, policies, margin, change, continuing, references, essentials, expected, drives, replace, insurer, owners, family, carries, decisive, lapses, renewing, scheduled, nothing, prices, readable

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `pricing_note_2027.docx`: candidate 'Lifetime Dog' sits beside decision vocabulary: ...ed a corrective increase of 12 per cent on the 2027 renewals of one of our four products, Lifetime Dog, Lifetime Cat, Condition Year or Essentials, and asked the pricing team to recommend whic...
- **REVIEW** `pricing_note_2027.docx`: candidate 'Lifetime Cat' sits beside decision vocabulary: ...e increase of 12 per cent on the 2027 renewals of one of our four products, Lifetime Dog, Lifetime Cat, Condition Year or Essentials, and asked the pricing team to recommend which. The increas...
- **REVIEW** `pricing_note_2027.docx`: candidate 'Condition Year' sits beside decision vocabulary: ...12 per cent on the 2027 renewals of one of our four products, Lifetime Dog, Lifetime Cat, Condition Year or Essentials, and asked the pricing team to recommend which. The increase is applied to...
- **REVIEW** `pricing_note_2027.docx`: carries 6 of 8 distinctive words of the committed call: "Put the 12 per cent increase on Essentials' 2027 renewals: it adds about CAD 0.5 million to the 2027 underwriting result"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `data_dictionary.docx`: 8 of 25 stump-paragraph terms appear (claims, condition, lifetime, policy, change, essentials); read whether the document names the move
- **REVIEW** `pricing_note_2027.docx`: 8 of 25 stump-paragraph terms appear (claims, condition, lifetime, policy, policies, essentials); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 2)
- **REVIEW** `kestrel_tariff_2026.xlsx`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `policy_terms_2024-2026.csv`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `data_dictionary.docx`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `pricing_note_2027.docx`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `policy_terms_2024-2026.csv`: 51894 ISO dates after 2027-01-15, e.g. 2027-01-16, 2027-01-17, 2027-01-18, 2027-01-19, 2027-01-20
- **REVIEW** `renewal_invitations_2020-2026.csv`: 2664 ISO dates after 2027-01-15, e.g. 2027-01-16, 2027-01-17, 2027-01-18, 2027-01-19, 2027-01-20

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Two isolated scored readers (sonnet, medium) on the stage 4 pack (target.zip a2b4683c), briefed with the prompt's
Deliverable Answers keys; the critical-component keys withheld. Scored with score_reader.py against that pack's figures.

| Reader | Call | Call figure | Ask figures | Verdict |
|---|---|---|---|---|
| r303ra | Essentials (hit) | CAD 0.3 million (miss) | 12 of 12 keys, 48 of 48 cells | call landed: Gate F failed |
| r303rb | Lifetime Cat (miss) | CAD 0.2 million | 12 of 12 keys, 48 of 48 cells | ask layer leaks 100 per cent |

- Question 1, the decisive step: both quoted the pricing note's estimand ("the result with the increase less the result
  without it"); neither quoted a sentence naming who renews. Harmless: the estimand, filed by design.
- Question 2, a ranking file: none (both); the tariff and the policy terms rank nothing on the question.
- Question 5: reader A read the cost sentence as each policy's own 2025 policy year, and both noted that the 2026 new
  business has no 2025 year.
- Question 6: both called the main answer an analytical choice (the renewal response and whether it varies with claims).
- How reader A landed: a retention logit with claims in the expiring and prior terms by product found lifetime
  claimants almost never leave, a proxy for the continuing-condition split, and named Essentials.
- How both took the asks: the wrap codes cross-tabulated against the menu option (the 5 October swap), the case-number
  gaps against the letters file (171 letters-only cases, all renewal premium), and a same-amount debit 10 to 14 days
  after each returned item.
- Realism tells raised: the 171 missing cases all of one category; retry spacing rigidly 10 to 14 days; lapse a
  near-perfect logistic of the offered change; uniform sample sizes in the vet fee benchmark; lapse rates of 20 to 40
  per cent a year high for pet insurance.

Verdict: FAIL (Gate F on reader A; the ask layer on both).
