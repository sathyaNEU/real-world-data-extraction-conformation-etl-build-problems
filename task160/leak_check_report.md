# leak check, task160

**Verdict: LEAK.** 12 files read, 7 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: region, winter, southeast, closed, member, census, timing, winters, central, hospital, window, members, shifts, behind, staffing, cooperative, capacity, nights, asserted, agency, decisive, register, season, method, forecasting

## 1 file names (LEAK 1)
- **LEAK** `MSP26_Content_Release_Notes_v2026.2.pdf`: a file whose name says it describes the data (Release_Notes): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `Corvane_QRMC_Service_Schedule_B_rev3.pdf`: carries 10 of 14 distinctive words of the committed call: "Plan for about 300 more override reviews (to the nearest 100) from Quillfield's adult wards in the first 13 weeks of the"
- **REVIEW** `QRMC_CR-2291_MSP26_HospitalWide_GoLive.docx`: carries 9 of 14 distinctive words of the committed call: "Plan for about 300 more override reviews (to the nearest 100) from Quillfield's adult wards in the first 13 weeks of the"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `Corvane_QRMC_Service_Schedule_B_rev3.pdf`: 4 of 25 stump-paragraph terms appear (region, shifts, staffing, register); read whether the document names the move
- **REVIEW** `QRMC_CR-2291_MSP26_HospitalWide_GoLive.docx`: 4 of 25 stump-paragraph terms appear (region, census, hospital, register); read whether the document names the move

## 6 ranking artifacts (INFO 2)
- **INFO** `CRV_PointOfCare_Map_QRMC.csv`: names 13 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `QRMC_MedAlert_Rule_Register_20261026.xlsx`: names 13 of 13 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `QRMC_FY2027_Inpatient_Volume_Plan.xlsx`: 612 ISO dates after 2026-10-28, e.g. 2026-11-02, 2026-11-09, 2026-11-16, 2026-11-23, 2026-11-30

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)
