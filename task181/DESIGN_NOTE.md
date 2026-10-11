# task181 design note: Larchmere Credit Union, the card reissue after the counterfeit wave

Seed AD04 (pump bearing overhaul) redrawn inside Anomaly Detection & Diagnostics. The seed's domain pairing
(energy-systems-utilities x anomaly-detection) is task180's, which `ban.pairing` blocks for the next draw. The seed's
calibration corpus (close-outs that recover the operating band) and its licensed wrong basis (the insurer's surveyor) are
blocked under the two-layer standard. What survives of the seed is its idea: send the remedy where the cause is, when
the loudest signal is not all cause.

Figures marked *target* are what the generator is tuned to; `checks.py` asserts the shipped values and the write-up
uses only those.

## DRAW

```
Card filed with guard.py register before the ladder was written? yes (WARN only, answered below)
Shape: 18 hypotheses-versus-evidence (every terminal a hypothesis; the committed figure is the exposed population)
Gate G mechanism: decomposition_attribution (counterfeit victims attributed to the terminals that read their cards)
Gap: population (decisive), rule        Pattern: none (own); generators G6 (the victims are a mixture of sources), G16
Domain: banking-credit-financial-risk / fraud-aml-detection   Objective: anomaly-detection
Pairing repeated from a recent build? no (banking x anomaly never built)
Stakeholder role: fraud and risk manager (compliance_or_audit)   Context artifact: close_out_summary (2025 incident)
Calibration form: none   Decision type: quantity_figure (cards to reissue)   Answer unit: count
Stump strategy: decomposition_attribution   Decisive rule filed? yes (the estimand and the exposure rule, card policy CP-14)
Official decoy filed? no (no screen threshold, no ranked list)   Validated decoy? no
Forum: committee_or_panel (the board risk committee, Thursday 8 October 2026)   Forcing event: incident_or_complaint
Org family: financial_institution
People (guard.py names, en_CA, seeds 1812026 and 181): Laurie Townsend (fraud and risk manager, the requester),
  Brenda Figueroa (chair, board risk committee), Stephanie Wise (card services manager, card history and reissue),
  Nicholas Rodriguez (fraud analyst, keeps the case workbook)
```

**Data-native sentence.** Skimming crews work more than one terminal in a season, and members who commute past a
compromised fuel pump also buy coffee and wash the car at the same highway exit, so a common-point screen run on all
counterfeit victims at once credits the exit's coffee counter and car wash with the pump's victims and buries a second,
smaller compromise among ordinary busy terminals; a fraud team traces victims source by source.

**Layer 1 (realistic mess and the system that produces it).** An issuer-side authorisation log (one row per ISO 8583
message: pre-authorisation and completion advice pairs at pay-at-pump, purchases, ATM withdrawals, reversals, declines)
with terminal IDs that change when a terminal is replaced; POS entry mode codes that need the codebook; merchant IDs
mapped to names, MCCs and towns through the processor's merchant directory; card numbers that change on reissue, linked
through the card history (renewals, lost and stolen, fraud reissues, closures); a fraud case workbook with one row per
disputed transaction, re-opened cases under new case numbers, amounts as written on the dispute form; a chargeback log;
member service timestamps in UTC.

**Layer 2 (the analytical shortcut).** Screening all counterfeit victims at once and keeping the terminals that stand
out. The pooled screen is the standard first pass and its arithmetic is right; an expert attributes victims to the
strongest source first, then screens the victims it leaves unexplained, because a pooled lift is an average over a
mixture of sources: it inflates every place the dominant source's victims also passed through and dilutes a second
source below them.

**Similarity claim.** No prior build turns on explaining away a dominant source before screening for the next. The
draft this card replaced (exposure counted on contact reads at the device) is kept as rung texture, not as the driver.

**WARN answers.** repeat.gate_g and overuse.gate_g (decomposition_attribution after task180 v1, 5 of the last 12): the
mechanism is honestly attribution (each counterfeit victim is attributed to the terminal that exposed the card), and
task180's architecture 1 is spent and being re-rooted on a different mechanism, so the repeat is with a dead build.

## GATE G

- **Litmus.** Nothing reported is overturned and no stakeholder read is corrected. Every authorisation, case, card
  history row and chargeback is correct; the pooled lift of every terminal is computed correctly. The difficulty is
  which terminals compromised members' cards.
- **Primary mechanism:** decomposition_attribution.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Deletion test.** Delete the manager's note and the 2025 close-out: the pooled screen still credits the coffee counter
  and car wash and buries the PIN pad; conditioning still finds the PIN pad.
- **Clean-data and instrument test.** Suspect files: none incomplete. The case workbook lists every counterfeit case
  (every counterfeit transaction is disputed: the members noticed the cash withdrawals); the authorisation log is the
  issuer's complete record. The instrument that observes the decision's own quantity (which terminals read which cards
  by contact, and when) ships whole; the difficulty is attribution across a mixture, not a repair.
- **Lens swap.** Not one population under two lenses: the rung-1 population is the cards read at one terminal; the
  answer's is the cards read at two terminals in two different windows.

## STUMP SENTENCE

A competent solver runs the common-point screen on the contact reads in each counterfeit victim's 60-day lookback,
finds the Ferrier Creek pump terminal, counts the open member cards it read by contact between the first and last
victim read and files that reissue count; the step that lands it there is stopping at the strongest common point, when
the victims the pump does not explain trace to the Lombard Market self-checkout PIN pad in Smiths Falls, which the pooled
screen ranks level with the car wash at the pump's exit and below its coffee counter.

## ENTITY AND UNIT OF VALUE

One card number. The policy (CP-14) reissues every open card read by contact at a compromise point while it was
compromised and not replaced since. The committed figure is a count of card numbers; members, accounts and messages are
not the unit.

## LADDER (targets)

| Rung | Construction | Files | Why a careful analyst stops | Killed by |
|---|---|---|---|---|
| 0 | Pooled screen, every terminal above a lift that looks clearly elevated (the pump, the coffee counter, the car wash; the PIN pad comes in with the car wash at any threshold below about 5.7) | about 3,150 (all four) or 2,230 (pump and coffee) | the standard common-point method, contact reads, 60-day lookback, member base rate, all filed | every coffee-counter and car-wash victim was also read at the pump in the pump's window: neither terminal accounts for a victim the pump does not |
| 1 | The pump alone | about 1,950 | the dominant source, 205 of 283 victims, lift about 45; the co-visited places explained away | 78 victims are unexplained, and 47 of them were read at one PIN pad in Smiths Falls (60 per cent against 2.9 per cent of members) |
| 1b | The pump, and the residual put down to travel (31 of the 78 have US or out-of-province card use in their lookback) | about 1,950 | a plausible story for a residual | the 47 Smiths Falls victims have no travel and share one terminal |
| 2 (answer) | Pump and PIN pad, each in its own window | **about 2,590** | | |

Discriminator: the twin pair. The car wash and the PIN pad carry the same pooled victim count (47) and the same member
base rate (2.9 per cent): any rule on pooled lift keeps both or drops both, and both are wrong.

Bracketing (L5): the under-count stops (rungs 1 and 1b) and the over-count stops (rung 0) sit on opposite sides, at
least 6 per cent from the answer (asserted, nearest cell named).

## GRID (asserted in checks.py, cell by cell)

Rows: pooled screen at thresholds 3, 5, 8, 10, 15, 20, 30 (lift) with and without a 10-victim floor; pump only; pump and
coffee; pump, coffee and car wash; pump and PIN pad (answer); all four; any conditional method (sequential attribution,
conditional logistic regression on terminal exposure, set cover). Columns: lookback 45, 60, 90 days; base rate over the
whole period or over the victim weeks; contact modes only or all card-present modes. Asserts: every conditional method
returns {pump, PIN pad} in every column; no pooled threshold returns {pump, PIN pad} in any column; the nearest wrong
reissue count is at least 6 per cent from the answer and needs a named rule violation.

## CLOSURE (the 22 axes)

1 Population: open member cards (CP-14 s2). 2 Unit: card number (CP-14 s2). 3 Attribution window: 60 days before the
first counterfeit use (CP-14 s4); 45 and 90 converge (C1). 4 As-of dating: card status on Monday 5 October (extract).
5 Version basis: card history is the record of replacement (CP-14 s5). 6 Divisor: member base rate over cards active in
the same weeks (CP-14 s4). 7 Weighting: none. 8 Window length: exposure window = first to last read of a later
counterfeit card at the terminal (CP-14 s4); the pump's terminal ID retires on 1 September and the PIN pads' on 15
September, so no member read sits between the last victim read and the retirement (C1). 9 Boundary inclusivity:
timestamps converted to Eastern time (CP-14 s1); no read within 12 hours of a window edge on the wrong side (C1).
10 Rounding: counts only. 11 Tie-break: none reached. 12 Maturity: every victim's first counterfeit use is before the
extract. 13 Order of operations: attribute then screen the remainder is the decisive move; pooled screen is the rung.
14 Row order: irrelevant. 15 Duplicates: pre-authorisation and completion pairs count once per card (distinct cards).
16 Identity: card numbers stay text; replacements linked through card history. 17 Netting: not applicable. 18 Units:
counts. 19 Code semantics: contact = chip insert 05, fallback 80, magstripe 90 (CP-14 s3 and the codebook); contactless
07 and 91, keyed 01 and e-commerce 81 do not expose a card. 20 Integerisation: none. 21 Scope: CP-14 applies to every
card the credit union issued. 22 Forward window: none; the reissue is of cards already exposed.

## ASK SHEET (devices, all off the main call's row population)

Main call row population (declared, asserted device-free): authorisation messages at card-present terminals from 1 June
to 4 October; card history; the case workbook's card numbers and first-counterfeit dates.

| Ask | Figures | Primary devices (silent) | Shared hazard |
|---|---|---|---|
| A. What the wave has cost so far: gross counterfeit loss, recovered, net, by card type (debit, credit), in CAD as posted | 6 | D3: the case workbook's amount is the dispute-form amount in the merchant's currency; US withdrawals are in USD and nothing in the workbook says so (the merchant directory carries the country; the authorisation log carries the CAD billed amount). D1: re-opened cases repeat a transaction under a new case number (same retrieval reference number); two genuine identical withdrawals minutes apart have different reference numbers (over-cleaning half). | H1 chargeback recoveries: a recovery later reversed at pre-arbitration appears as a second, negative row; the status of record is the latest |
| B. Member refunds: cases refunded within the 10-business-day promise, by card type, and the longest wait | 5 | D8: case open time is logged in UTC; business days count from the member's local reporting day (MS-3), excluding weekends and the holidays the credit union observes (Civic Holiday 3 Aug, Labour Day 7 Sep); evening reports cross midnight UTC | H1 (a refund reversed after the chargeback was lost is not a refund) |

Use test: both asks are what a risk committee reads next to a reissue request (what it has cost, how members were
treated). Decoupling: clearing the attribution changes no figure in A or B (asserted).

## PINS

Filed: CP-14 Card compromise and reissue (governing): scope, unit, contact exposure, the common-point screen as the
standard first pass (lookback, member base rate), the window rule, the reissue rule. MS-3 Member service standard:
the 10-business-day refund promise and the holiday calendar. Merchant directory and codebook (reference). Notes from
the fraud analyst (field semantics only). No sentence states that victims are attributed before screening again.

## PACK GATES (targets)

At least 12 files, at least 4 formats; `card_authorisations_*.parquet` above 1,000,000 rows; two distractors named in
metadata.json: the online banking login log (account takeover is a different fraud) and the ATM cash-replenishment
schedule (an operations file that mentions the same ATMs).

## SIX-POINT CHECK

1. Real work: ISO message pairs, entry-mode codebook, merchant directory, card history chains, re-opened cases, UTC
   timestamps, none planted. 2. The flip is a method choice: pooled against conditional attribution. 3. CP-14 defines
   population, unit, window, exposure and comparison. 4. No decoy memo; the manager's note is a true observation (the
   pump is the biggest source). 5. The method is not recovered from certified figures. 6. No earlier task teaches
   masking and co-visit confounding in a common-source screen.

## STOPPING RULE

Two rounds in which both solvers re-screen the residual unprompted file this architecture as at-ceiling; a miss that
lands anywhere other than rungs 0, 1 or 1b is read for a fork before any hardening.

## Tried and rejected

- Draft (never registered): which merchant location gets the acquirer's inspection, exposure counted only on contact
  reads at the device. Rejected before registration: pick-one-of-N is the spent shape on this objective, and contact-only
  exposure is applied by reflex by a fraud-literate solver.
- First fraudulent use anchored on unclaimed test transactions (the test site posing as the common point). Rejected:
  the claims file would be the narrower record the clean-data test repairs, so the defect would carry the stump.
