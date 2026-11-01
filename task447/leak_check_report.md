# leak check, task447

**Verdict: LEAK.** 19 files read, 23 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: product, projection, capture, referral, placement, acquisitions, closed, placements, decisive, nothing, method, history, population, records, claims, estimand, sentence, analyst, carrier, patient, acquirer, service, benefit, ownership, reproduces

## 1 file names (LEAK 2)
- **LEAK** `apcd_extract_data_dictionary.pdf`: a file whose name says it describes the data (data_dictionary): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `export_manifest.csv`: a file whose name says it describes the data (manifest): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `N25-014_notice_of_material_change.pdf`: golden figure 014 appears: ...ost Review under s. 153.86 Item Notice number N25-014 Received 8 October 2025 (complete on receipt) Fil...
- **REVIEW** `N25-014_notice_of_material_change.pdf`: candidate 'Brightwater Medical Group' sits beside decision vocabulary: ...Jacob Murillo, Halloran Pike LLP, for Ledgestone Health Debra Prince, Administrator, for Brightwater Medical Group, S.C. 6 October 2025 Exhibit A. Entities owned or controlled by Ledgestone Health Entity...
- **REVIEW** `apcd_extract_data_dictionary.pdf`: golden figure 014 appears: ...dictionary, request OHCCR-MO-2025-031 (notice N25-014) 1 The files apcd_op_facility_claims_2024.csv (la...
- **REVIEW** `ohccr_rule_4_preliminary_review.pdf`: golden figure 4.06 appears: ...per cent and projects with the shares as stated. 4.06 Determination The projected increase is projected...
- **REVIEW** `ohccr_rule_4_preliminary_review.pdf`: golden figure 4.05 appears: ...ct stands in the projection year, estimated under 4.05; the part that moves is priced at the acquiring p...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `N25-014_notice_of_material_change.pdf`: 3 of 25 stump-paragraph terms appear (carrier, patient, service); read whether the document names the move
- **REVIEW** `apcd_extract_data_dictionary.pdf`: 6 of 25 stump-paragraph terms appear (product, claims, carrier, patient, service, benefit); read whether the document names the move
- **REVIEW** `market_oversight_technical_appendix.pdf`: 7 of 25 stump-paragraph terms appear (product, history, records, claims, carrier, service); read whether the document names the move
- **REVIEW** `ohccr_rule_4_preliminary_review.pdf`: 5 of 25 stump-paragraph terms appear (product, projection, history, claims, service); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: the N things: "those two counties" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: rounding opener 'give' at 46% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (LEAK 1)
- **LEAK** `apcd_extract_data_dictionary.pdf`: names 50 column(s) of the data files verbatim, 100% of apcd_medicare_advantage_facility_claims_2024.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)
