# leak check, task181

**Verdict: REVIEW.** 13 files read, 11 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: victims, exposure, screen, window, rejected, attribution, decisive, pooled, history, exposed, population, decomposition, decision, device, victim, carries, counts, answered, attributed, mixture, sources, domain, manager, incident, analyst

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `card_authorisations_2026-06-01_2026-10-04.parquet`: golden figure 02417158 appears: ...01 12:52:06+00:00,125.1,124,125.1,882084246162166,02417158,5411,07,00,615212104748,025996 31870000012212,1B4...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `CP-14_card_compromise_and_reissue.pdf`: 5 of 25 stump-paragraph terms appear (exposure, screen, window, history, device); read whether the document names the move
- **REVIEW** `close_out_2025_brockville_atm_skimmer.pdf`: 4 of 25 stump-paragraph terms appear (exposure, window, decision, device); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `merchant_directory_2026-10.csv`: names 3 of 3 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt form (clean)

## Solver's-eye read (pass 1, isolated reader)

1. none. "CP-14 sets out the method as ordinary policy ('the fraud desk runs the common-point screen as the first pass'), with the same weight as sections 3 and 5-7. The version-3 line ('Member base rate taken over active cards in the screen's span') is a normal change-log entry."
2. none. Parquet is raw authorisation messages; merchant_directory has no terminal IDs and no scores; fraud_cases shows cash-out places (mostly NJ ATMs), not read places.
3. none. Nearest: fraud_desk_notes.md ("Pulled Monday 5 October 2026 for the card reissue request"), a normal hand-off data dictionary (fields, not method).
4. none. Brockville figures ("Cards reissued 1,184", "52 of 57") are a labelled 2025 precedent; 283 counts victims; "Nicholas traced the first cases to the pumps" reads as a lead to test; merchant_directory lists three Ferrier Creek merchant IDs and favours none.

Plan: counterfeit cards' first disputed date, 60-day lookback; contact reads 05/80/90 any message type; common-point screen vs member base rate over the span; "test the pumps against the plaza's other terminals, watch for replaced terminal_ids, allow for more than one common point"; windows first-to-last counterfeit-card read; count distinct cards read by contact in window less replaced/closed per card_history; losses deduped by retrieval_ref at amount_billing_cad as posted, recovered from chargebacks net of pre-arbitration debits; MS-3 refunds from case_opened UTC to local, re-opened as one claim, business days with appendix holidays.

REVIEW lines:
- parquet 02417158: harmless (one of 3,150 terminal IDs, 2,417 of 1,257,657 rows, in no other file; quoted row is contactless 07; merchant 882084246162166 MCC 5411 is not at the plaza's address).
- CP-14: harmless (defined terms; general rule; never says a busy site can look like a common point, never questions a first trace, never points to a merchant or terminal).
- Brockville close-out: harmless (2025 ATM incident; obvious site was the common point; if anything nudges toward trusting the first site named).
Follow-up on "allow for more than one common point": from CP-14 s2 ("a card is reissued once however many compromised terminals read it") and s8 ("each compromised terminal with its exposure window"), plus own practice (pump skimmers often hit several pumps at one site).

## Solver's-eye read (pass 2, isolated reader, after the idiom fixes)

1. none. CP-14 s4 "gives the method as ordinary policy ... Nothing marks it as the step the answer turns on."
2. none. No file scores terminals.
3. none. Closest: fraud_desk_notes.md, "a normal hand-off note that defines fields and gives no method" (it documents the dispute-form `amount`, `case_opened` in UTC, and that "a replaced terminal gets a new one").
4. none. "Nicholas traced the first cases to the pumps" is a lead ("A pay-at-pump on a highway will have a high base rate"); the plaza's three merchant IDs, the 2025 close-out figures and 283 are context or inputs.

Plan: contact reads (05/80/90) in each counterfeit card's 60-day lookback against the member base rate (CP-14 s4); "Rank terminals by that ratio, and test the Ferrier Creek lead across all three plaza merchant IDs and any replacement terminal IDs. For each common point, set the exposure window (s5)"; count open cards read by contact in each window (s6); losses at amount_billing_cad netted by retrieval_ref, recovered from chargebacks; MS-3 refunds from case_opened in Eastern time, re-opened claims from the first report. No residual re-screen.

REVIEW lines: parquet 02417158 harmless ("raw evidence the analyst has to find with the screen, and nothing points to it": 2,417 messages, 44th busiest of 3,150 terminals, one of 16 at its merchant, in no document); CP-14 harmless (its own section vocabulary; a general rule naming no merchant, terminal or date); 2025 close-out harmless (a different incident; "if anything it steers the reader toward ATMs, away from the answer").
