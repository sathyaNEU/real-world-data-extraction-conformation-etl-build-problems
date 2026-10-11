# task181 design note: Larchmere Credit Union, the card reissue after the counterfeit wave

Seed AD04 (pump bearing overhaul) redrawn inside Anomaly Detection & Diagnostics. The seed's domain pairing
(energy-systems-utilities x anomaly-detection) is task180's, which `ban.pairing` blocks for the next draw. The seed's
calibration corpus (close-outs that recover the operating band) and its licensed wrong basis (the insurer's surveyor) are
blocked under the two-layer standard. What survives of the seed is its idea: send the remedy where the cause is, when
the loudest signal is not all cause.

Every figure below is the shipped value: `generator/checks.py` asserts it on the files under `target/` (537 assertions
in the final run, all passing) and `generator/verify.py` recomputes the graded ones from the shipped bytes on a
separate code path.

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
  Nicholas Rodriguez (fraud analyst, keeps the case workbook). Pack furniture (guard.py names, seed 1813): Erika
  Jenkins (MS-3 owner), Eric Snyder (Brockville branch, 2025), Donna Keller (cash operations); the documents carry
  initials only.
```

**Data-native sentence.** Skimming crews work more than one terminal in a season, and members who commute past a
compromised fuel pump also buy coffee and wash the car at the same highway exit, so a common-point screen run on all
counterfeit victims at once credits the exit's coffee counter and car wash with the pump's victims and buries a second,
smaller compromise among ordinary busy terminals; a fraud team traces victims source by source.

**Layer 1 (realistic mess and the system that produces it).** An issuer-side authorisation log of 1,257,657 ISO 8583
messages (pre-authorisation 0100 and completion advice 0220 pairs at pay-at-pump on one retrieval reference, 0200
financial requests, 0420 reversals for short dispenses and timeouts, declines with their response codes) with terminal
IDs that change when a terminal is replaced (95 positions re-terminalled, among them OPT 6 on 2 September and Lombard's
six self-checkout pads on 15 September; OPT 6's dispenser also sat out of service from 29 June to 24 July on the same
reader); POS entry mode, processing and currency codes that need the codebook; merchant IDs mapped to names, MCCs and
towns through the processor's merchant directory, with one merchant ID per business at a shared address; card numbers
that change on renewal (a 2023 conversion cohort expiring 09 and 10/2026), loss, theft, damage, fraud and closure,
linked through the card history; a fraud case workbook with one row per disputed transaction, re-opened cases under new
case numbers and dispute-form amounts in the merchant's currency; a chargeback event log; case timestamps in UTC.

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

## LADDER (shipped)

Main column of the screen: contact reads (05, 80, 90), 60-day lookback, member base rate over the cards with any
authorisation in the screen's span (16,487 cards). Victims: 283 counterfeit cards, 205 read at the pump in their
lookback, 47 at the PIN pad, 31 at neither.

| Rung | Construction | Cards | Why a careful analyst stops | Killed by |
|---|---|---|---|---|
| 0 | Pooled screen, every terminal above a lift that looks clearly elevated: the pump (lift 38.78, 205 cards, base 1.87 per cent), the coffee counter (11.95, 95 cards) and, below any threshold under 4.59, the car wash and the PIN pad together | 1,139 (all four, +194.3%) or 502 (pump and coffee, +29.7%) | the standard common-point method, contact reads, 60-day lookback, member base rate, all filed | every coffee-counter and car-wash counterfeit card was also read at the pump in its window: neither terminal accounts for a card the pump does not |
| 1 | The pump alone | 174 (-55.0%) | the dominant source, 205 of 283 victims, lift 38.78; the co-visited places explained away | 78 victims are unexplained, and 47 of them were read at one PIN pad in Smiths Falls (60.3 per cent against a base of 3.52 per cent, lift 17.13; next terminal with 3 or more cards 9.73 on 5 cards) |
| 1b | The pump, and the residual put down to travel (31 of the 78 have US or out-of-province card-present use in their lookback) | 174 | a plausible story for a residual | the 47 Smiths Falls victims have no travel and share one terminal |
| 2 (answer) | Pump and PIN pad, each in its own window | **387** (174 + 228, 15 at both) | | |

Windows (CP-14 s5, Eastern): pump terminal LT723511, 5 August 2026 06:28 to 31 August 2026 18:01; Lombard Market
terminal 02417158, 13 August 2026 07:56 to 14 September 2026 19:25. No member message at either terminal ID after the
last counterfeit-card read, none from 20:00 the evening before the first, and every edge falls on the same date in UTC
and Eastern time, so instant, Eastern-date and UTC-date windows all give 387.

Discriminator: the twin pair. The car wash and the PIN pad carry the same pooled victim count (47) and the same member
base (597 cards, 3.62 per cent): identical pooled lift 4.59, so any rule on pooled lift keeps both or drops both, and
both are wrong. Every other terminal that read 10 or more counterfeit cards has lift at most 2.78 (Larchmere ATM
Merrickville, 36 cards). After both sources, no terminal with 3 or more of the last 31 cards stands above 1.91.

Bracketing (L5): the under-count stops (rungs 1 and 1b, 174) and the over-count stops (rung 0, 502 and 1,139) sit on
opposite sides of 387; the nearest pooled cell is 502 (+29.7%).

**Deviation from the targets the design was drafted with.** The draft paired a pump lift of about 45 with about 2,300
pump-exposed cards and a reissue of about 2,590 out of about 15,000 cards. Under CP-14's lift (victim share over member
base share) those cannot coexist: a lift of 45 on 205 of 283 cards needs a member base of 1.6 per cent, about 240 other
cards, while 2,300 exposed cards put the base at 14 per cent or more and the lift near 5, below the coffee counter and
the twin. The build keeps the lift structure the ladder needs (pump about 39, coffee 12, twin 4.6, others under 3) and
lets the exposure follow: 400 cards read at the pump in its window (205 of them victims), 283 at the PIN pad, 387 to
reissue.

## GRID (asserted in checks.py, cell by cell)

Columns: lookback 45, 60, 90 days; base over the screen's span or the whole extract; contact modes only or all
card-present modes (12 columns). Rows: pooled screen at thresholds 3, 5, 8, 10, 15, 20, 30 with and without a 10-card
floor (168 cells); pump only; pump and coffee; pump, coffee and car wash; pump and PIN pad (answer); all four;
sequential attribution (floor 10, stop at lift 3), greedy set cover and a joint logistic on terminal exposure.

- Sequential attribution and set cover return {pump, PIN pad} in all 12 columns; the joint logistic returns them in
  the 6 contact columns (pump z 29, PIN pad z 10 in the main column). In the all-mode columns, which count contactless
  taps that CP-14 s3 says do not expose a card, the logistic keeps the pump and returns the PIN pad at 45 and 60 days
  only; at 90 days the taps of Lombard's other shoppers bury it. Those columns' own count (all-mode exposure at the two
  terminals) is 701, +81.1%.
- No pooled cell returns {pump, PIN pad}: the coffee counter stands above the PIN pad in every contact column (10.98 vs
  5.73 at 45 days, 11.95 vs 4.59 at 60, 12.44 vs 3.70 at 90). Every pooled cell is at least 6 per cent from 387; the
  nearest is 502 (+29.7%).
- Other readings of the count: cards not filtered on status 667 (+72.4%, CP-14 s6); only the counterfeit cards removed
  415 (+7.2%, CP-14 s6, renewals and closures since); all card-present reads 701 (+81.1%, CP-14 s3); the two terminals
  summed with the 15 shared cards counted twice 402 (+3.9%, a unit violation of CP-14 s2, not a reading).
- Converging readings: chip-only (no fallback or stripe read inside either window), approved-only (no decline inside
  either window), Eastern-date and UTC-date window edges: all 387.

## CLOSURE (the 22 axes)

1 Population: open member cards (CP-14 s6). 2 Unit: card number (CP-14 s2). 3 Attribution window: 60 days before the
first counterfeit use (CP-14 s4); 45 and 90 converge on the terminal set and the count (C1). 4 As-of dating: card status
on Monday 5 October (card history). 5 Version basis: card history is the record of replacement (CP-14 s6).
6 Divisor: member base rate over cards with any authorisation in the screen's span (CP-14 s4); whole-extract base
converges (C1). 7 Weighting: none. 8 Window length: exposure window = first to last read of a later counterfeit card at
the terminal (CP-14 s5); the pump's terminal ID last reads on 31 August and the PIN pad's on 14 September, and no member
read sits between the last victim read and either retirement (C1). 9 Boundary inclusivity: no member read from 20:00 the
evening before a window opens to its first victim read, every edge between 04:00 and 20:00 Eastern (C1). 10 Rounding:
counts only. 11 Tie-break: none reached. 12 Maturity: every victim's first counterfeit use is before the extract.
13 Order of operations: attribute then screen the remainder is the decisive move; pooled screen is the rung.
14 Row order: irrelevant. 15 Duplicates: pre-authorisation and completion pairs count once per card (distinct cards).
16 Identity: card numbers stay text; replacements linked through card history. 17 Netting: not applicable. 18 Units:
counts. 19 Code semantics: contact = chip insert 05, fallback 80, magstripe 90 (CP-14 s3 and the codebook); contactless
07 and 91, keyed 01 and e-commerce 81 do not expose a card; declined reads count (CP-14 s3) and none occurs inside a
window (C1). 20 Integerisation: none. 21 Scope: CP-14 applies to every card the credit union issued. 22 Forward window:
none; the reissue is of cards already exposed.

## ASK SHEET (devices, all off the main call's row population)

Main call row population (declared, asserted device-free): authorisation messages at card-present terminals from 1 June
to 4 October; card history; the case workbook's card numbers and first-counterfeit dates. Asserted: re-opened rows change
no victim or first-use date; no disputed transaction sits inside any lookback; the first counterfeit date agrees between
the workbook and the log for all 283 cards; removing every read at the four screened terminals leaves both asks
unchanged (decoupling).

| Ask | Shipped figures | Primary devices (silent) | Shared hazard |
|---|---|---|---|
| A. What the wave has cost so far, CAD as posted, by card type | Debit: gross $246,792.17, recovered $78,330.45, net $168,461.72. Credit: gross $35,217.25, recovered $11,845.28, net $23,371.97 | D3: the workbook's amount is the dispute-form amount in the merchant's currency, USD at US merchants, with no currency column (the directory carries country; the log carries currency 840 and the CAD billing amount). D1: 8 claims re-opened under new case numbers repeat their transactions on the same retrieval reference; 58 groups of genuine identical-looking withdrawals (same card, ATM, amount, day) carry different retrieval references | H1 chargebacks: 6 credits taken back at pre-arbitration as later negative rows; the log also carries chargebacks on card-not-present fraud and merchant disputes |
| B. Counterfeit cases refunded within MS-3's ten business days, and the longest wait, by card type | Debit: 195 of 215 refunded, longest 20 business days. Credit: 21 of 25, longest 16 | D8: case_opened is UTC with Z; MS-3 counts from the member's Eastern reporting day, weekends and the MS-3 holidays excluded (Labour Day 7 September falls inside); evening reports cross midnight UTC. A re-opened claim is the same claim (MS-3 s4) | the re-opened claims of ask A (the longest debit and credit waits are both re-opened claims, asserted) |

Ask A stops (each moves debit and credit by $50 or more, asserted): workbook amount taken as dollars: debit gross
$204,104.00, credit $29,377.28; no de-duplication: $254,521.10 and $38,279.84; de-duplicated on card, merchant, amount
and date: $221,385.95 and $30,789.22; credits only (pre-arbitration ignored): recovered $80,644.26 and $13,330.38; every
chargeback and case in the files: gross $263,408.47 and $96,798.50, recovered $87,242.23 and $38,382.03.

Ask B stops (each moves debit and credit, three or four of the four figures, asserted): UTC day as the report day:
debit 199 within / 19 longest, credit 23 / 16; calendar days: 161 / 29 and 18 / 23; no holidays: 189 / 21 and 19 / 17;
a re-opened case as a new claim: 201 / 13 and 23 / 11. A federal calendar that adds 30 September moves credit to 22
within (MS-3's list governs).

Use test: both asks are what a risk committee reads next to a reissue request (what it has cost, how members were
treated); CP-14 s8 lists both in the request. Decoupling asserted as above.

## PINS

Filed: CP-14 Card compromise and reissue (governing): scope, unit, contact exposure, the common-point screen as the
standard first pass (lookback, member base rate), the window rule, the reissue rule, loss reporting (posted CAD, each
disputed transaction once, recoveries net of amounts taken back). MS-3 Member service standard: the ten-business-day
promise, the counting rule, the re-opened claim rule and the 2026 holiday list. Merchant directory and codebook
(reference). Notes from the fraud analyst (field semantics only). No sentence states that victims are attributed before
screening again, and no document gives a lift threshold.

## PACK GATES (shipped)

13 files, 7 formats (parquet, csv, xlsx, pdf, docx, md, txt). `card_authorisations_2026-06-01_2026-10-04.parquet`
1,257,657 messages on 16,869 card numbers (debit 12,213, credit 4,656) from 15,137 member card slots (debit 10,643, credit
4,494) of 9,840 members; merchant directory 1,316 merchants; card history 16,951 card numbers and 1,814 replacements;
case workbook 1,012 disputed transactions in 458 cases; chargeback log 992 events. Distractors named in metadata.json:
`online_banking_logins_2026-08-01_2026-10-04.csv` (101,424 sessions; account takeover is a different fraud) and
`atm_cash_replenishment_q3_2026.xlsx` (127 visits; operations at the same branch ATMs). Two consecutive builds
byte-identical on all 13 files and both goldens (sha256). Goldens in `golden/` (the repo's ignored build folder, cut
with the pack): `card_reissue_request.pdf` (three pages, chart of the pooled and residual screens) and
`common_point_trace.xlsx` (one sheet per page with the screen, the 387 card numbers, the transaction and claim trails).

## LEAK CHECK AND SURFACE (stage 4)

`leak.py task181 --asof 2026-10-05` on the final pack: REVIEW, no LEAK (13 files read; 11 golden figures and 3 candidate
names from submission.md; 25 stump terms from this note). Answers to each REVIEW line:
- golden figure 02417158 appears in the authorisation parquet: it is a terminal ID, one of 3,150 in the log, and
  finding it is the task.
- CP-14 carries 6 of the 25 stump-paragraph terms (window, exposure, screen, history, device, counted): it is the
  governing policy and defines the screen, the window and the reissue; it does not say to attribute victims or screen
  again, and gives no threshold.
- the 2025 close-out carries 4 (window, exposure, device, decision; the last only in its timeline row "Last chargeback
  decision received"): a single-terminal incident told as timeline and cost; it says nothing about how the common point
  was found beyond naming it.
INFO: the merchant directory names the three candidates (a directory, no ranking); the container audit found no writer
signature.

`guard.py surface task181`: one pair promoted for adjudication, task103 (a community foundation's food-security reserve;
surface 0.143, corpus percentile 99; both cards file population as the decisive gap), carried by the flat layout, the
format mix and the pdf+xlsx deliverable pair the prompt fixes; no shared file names or file contents, one short generic
prompt shingle, and a different domain, decision and spine. Nearest not promoted: task131 (0.096). People found in the
cut pack: Laurie Townsend and Brenda Figueroa (on the card). `guard.py check` on the synced card: WARN only
(repeat.gate_g, overuse.gate_g, answered under DRAW).

Prompt: one sentence split ("The committee approves a number of cards. That number is what I need.") so the voice-check
ECONOMY row is clean (206 words, 22.9 per sentence, a sentence under eight words); page three asks for "the counterfeit
cases we refunded", the population ask B counts.

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
- Targets of about 2,300 pump-exposed cards and a pump lift of about 45 on about 15,000 cards. Rejected at generation:
  the two are arithmetically incompatible under CP-14's lift (see LADDER); the lift structure was kept and the exposure
  followed it (answer 387).
- Random pump choice by commuters with the victims' pre-August OPT 6 reads moved to OPT 5 as inserts. Rejected: OPT 5
  became a 62-lift terminal and step one of the attribution picked it; the moved visits are taps at other pumps instead.
- Every plaza pump tap-capable at the same habit as the coffee counter, and commuters' Ottawa favourites including ATMs.
  Rejected: other pumps and an Ottawa ATM reached 10+ victims at lifts of 13 to 20 in the 90-day column and outranked
  the pump; pumps now take taps by habit, Ottawa ATMs left out of commuters' favourites, and OPT 6's July dispenser
  outage lowers its pre-window users.
- Victims drawn only from cards with no replacement due in August to October. Rejected: the non-victim exposed cards
  were then half renewals and the answer fell to 244; a renewal due after the skim is now superseded by the fraud
  reissue, and the renewal cohort is 13 per cent of debit cards.
- Lombard Market at its first calibration (self-checkout 68 per cent of lanes, baskets at the grocery median). Rejected:
  in the all-mode columns the PIN pad's taps diluted it below a joint logistic's bar; bigger weekly baskets (more inserts
  over the $100 tap limit) and fewer self-checkout visits keep contact and all-mode bases closer.
- Background travellers chosen without a destination cap. Rejected: five of the 31 had been to Erie, Pennsylvania, and
  its parking lot entered the all-mode logistic; at most two background cards now share a destination in a lookback.
