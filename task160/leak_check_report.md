# leak check, task160

**Verdict: REVIEW.** 12 files read, 7 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: background, alerts, duplicate, record, overridden, removal, history, silent-mode, decisive, nothing, orders, interacting, burden, shared, sentence, volume, removed, register, stream, readable, prices, census, schedule, answering, quantity

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `Corvane_QRMC_Service_Schedule_B_rev3.pdf`: carries 10 of 14 distinctive words of the committed call: "Plan for about 300 more override reviews (to the nearest 100) from Quillfield's adult wards in the first 13 weeks of the"
- **REVIEW** `QRMC_CR-2291_MSP26_HospitalWide_GoLive.docx`: carries 9 of 14 distinctive words of the committed call: "Plan for about 300 more override reviews (to the nearest 100) from Quillfield's adult wards in the first 13 weeks of the"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `Corvane_QRMC_Service_Schedule_B_rev3.pdf`: 7 of 25 stump-paragraph terms appear (alerts, overridden, volume, register, prices, schedule); read whether the document names the move
- **REVIEW** `Halverson_MSP26_Release_2026.2_Client_Bulletin.pdf`: 5 of 25 stump-paragraph terms appear (background, duplicate, nothing, orders, interacting); read whether the document names the move
- **REVIEW** `QRMC_CR-2291_MSP26_HospitalWide_GoLive.docx`: 7 of 25 stump-paragraph terms appear (background, duplicate, history, volume, register, census); read whether the document names the move

## 6 ranking artifacts (INFO 2)
- **INFO** `CRV_PointOfCare_Map_QRMC.csv`: names 13 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `QRMC_MedAlert_Rule_Register_20261026.xlsx`: names 13 of 13 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `QRMC_FY2027_Inpatient_Volume_Plan.xlsx`: 612 ISO dates after 2026-10-28, e.g. 2026-11-02, 2026-11-09, 2026-11-16, 2026-11-23, 2026-11-30

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader, two rounds)

Every REVIEW line above is ruled harmless by the reader in each round; neither round found a decisive-step sentence, a ranking file or a figure that reads as the answer, and both answered question 6 with an analytical choice.

### Leak reader, round 1 (2026-11-01, isolated, Sonnet at medium effort, on target.zip 2fd81ca5)

1. Decisive step: none stated; the closest is Schedule B 4.3 ("the reviews those units will send with the change live, prescribers answering its alerts as they have on any unit where it already runs, against the reviews the same units would send over the same weeks without it"), the estimand, not a method.
2. Nothing ranks anything.
3. No help-only file (the rule register is ordinary reference material).
4. Nothing reads as the answer (no forecast, net change or per-unit rate filed anywhere).
5. Schedule B 4.3 (the units' reviews over the first 13 live weeks with the change live, less the same units' reviews over the same weeks without it, priced at USD 6.40), with 2.1 (one overridden alert is one review), 2.2 (moderate-severity alerts not reviewed), 3.1 (a review counts where it is signed off); CR-2291 names the window and the units.
6. An analytical choice: 4.3 says to use the override behaviour on the live units, not the background-mode log; the background log and the counterfactual need a method the text does not give; nothing planted; the filed semantics (UTC against Eastern, department renames, one alert per active order) read as Layer 1.
Sweep flags: all harmless (Schedule B and CR-2291 state scope, definitions and the window; the vendor bulletin describes the rules in general and names no deciding step; the later dates are the planned go-live and planned weeks).
Realism: none seen (system-export features throughout); minor: the point-of-care map's effective_from of 2024-09-01 on nearly every row, plausible for a map.

### Leak reader, round 2 (2026-11-01, isolated, Sonnet at medium effort, on target.zip 5586cd17)

1. Decisive step: the nearest is Schedule B 4.3 (the reviews those units will send with the change live, prescribers answering its alerts as they have on any unit where it already runs, against the same units without it), which names the comparison and the behavioural basis, not the method or the count.
2. Nothing ranks or scores anything (the rule register lists status and routing, no counts).
3. Ordinary context files (the point-of-care map, the register's unit renames, the vendor bulletin); none walks through the method.
4. Nothing reads as the answer (no net figure or per-unit rate anywhere).
5. Schedule B 4.3 (the going-live units over the 13 weeks to 4 April 2027, with the change live and prescribers answering as on the live units, less the same units without it); 2.3 (one queue task per order and signing, each overridden alert on it a signed-off review) bears on counting.
6. An analytical choice: the background log shows what would fire, not what prescribers would do, so live-unit behaviour must be carried over, estimated from the alert history; no single field flips it; nothing planted; the mess reads as Layer 1.
Sweep flags: all harmless (Schedule B states the estimand and contract definitions; CR-2291 is a change request with dates and attachments; the vendor bulletin is generic, its "evaluates exactly as it would live" line a mild support of the counterfactual).
Realism: none; minor: the volume plan's Basis note reads slightly like a summary, plausible for a finance planning note.

