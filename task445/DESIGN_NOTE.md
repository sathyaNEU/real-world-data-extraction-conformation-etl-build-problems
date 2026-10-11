# task445 design note

Seed ET02 (13F institutional ownership bridge). Objective Data Extraction & Conformation (ETL).
Client domain Quantitative Finance, task type `other` (institutional ownership analytics from
regulatory holdings filings). Architecture 1.

## DRAW

| Axis | Draw |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task445.json`, registered 2026-10-11, verdict WARN (answered below) |
| Shape | 03, bridge between two totals (raw information-table sum to the ownership the flag rests on) |
| Gate G mechanism | `method_or_model_selection` (how a period still inside its filing window is completed, chosen on a back-test the history supports) |
| Gap / pattern | time, then population / none of A to E |
| Generators | G12 (a manager with no Q4 filing yet is not a zero holder), G16 (completion method by back-test), G6 (late-filer mix differs by issuer), G19 on the asks |
| Decision type | designation set: which of the 12 watchlist issuers carry the crowded flag for 31 Dec 2022 |
| Stakeholder | head of ownership research (role family `product_manager`) |
| Context artifact | register (the firm's manager register) |
| Calibration form | `censored_or_lagged_release`: the Q2 and Q3 2022 filing windows, complete, with filing dates |
| Stump strategy | `maturity_censoring`; decisive rule filed: the estimand is filed, the completion method is not; no official decoy, no validated decoy |
| Forum / forcing / org | clients (`customer_or_counterparty`) / the quarterly flag file's fixed publication date inside the filing window (`other`) / `professional_services` |
| People | Nancy Henderson, Jonathan Richardson (guard.py names, seed 445) |

**WARN answered.** `repeat.decision` against task229: both commit to a set, but task229 fires an alert
per firmware build from a standard error built over the right unit; here the set is a threshold flag on
an ownership share whose numerator is censored at the extract and has to be completed holder by holder.
Different gap (time against population), different quantity, different construction.

**Similarity claim.** No prior build completes a filing period that is still open at the extract from
each reporter's last filed position; task130 v1 (lineage) built a future holding set forward from a past
snapshot, which is a forward roll of a known book, not a censored total with an issuer-skewed tail.

## Stump sentence

A competent solver conforms the Q4 2022 13F filings in hand perfectly (amendment types, value units by
filing date, option rows out, CUSIPs repaired) and flags the issuers whose institutional ownership on
file clears 80 per cent of shares outstanding, or, seeing that the window closes on 14 February,
scales every issuer by the aggregate share of value historically on file by the extract day; both file
the wrong flag set, because the step that decides it is completing the period holder by holder: a
manager that filed for Q3 and has not filed for Q4 is a holder not yet reported, and those managers
sit in a few issuers' registers far more than in the rest.

## Data-native sentence

13F holdings arrive over a 45-day window and the managers that file at the deadline (the large passive
complexes and multi-strategy funds) are a different slice of each issuer's register, so the share of an
issuer's final ownership on file on any day before the deadline varies issuer by issuer, and only a
holder-level completion recovers it.

## The two layers

- **Layer 1 (mess, carried by the asks):** the SEC Form 13F data sets organised by submission quarter,
  originals with RESTATEMENT and NEW HOLDINGS amendments, value in thousands before 2023-01-03 and dollars
  after (by filing date, with one filer still in thousands after the switch), put/call and principal rows
  on the share CUSIP, filer-keyed CUSIPs with dropped zeros and bad check digits, cover-page shares
  outstanding at different as-of dates, manager families under several CIKs. Every one of these is what
  EDGAR's structured extracts actually carry.
- **Layer 2 (decides the call):** the period is censored at the extract. The tempting shortcut is to
  treat the filings in hand as the period, or to apply one aggregate completion share; the expert move
  is a holder-level completion (each pending manager at its last filed share position), which the Q2
  and Q3 windows back-test.

## Tried and rejected

- Seed ET02 as written (amendment-type supersession and filing-date value units deciding the flag):
  rule application and data semantics as the decisive step, banned; kept as Layer 1 on the asks.
