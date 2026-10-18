# leak check, task202

**Verdict: REVIEW.** 17 files read, 43 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: window, returns, domain, driver, stated, mechanism, decisive, printed, status, architecture, measured, generator, device, committed, partner-band, readable, shipped, abstraction, anomaly, average, spread, measures, rebuild, closure, asserted

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `DATA_DICTIONARY.md`: carries 4 of 5 distinctive words of the committed call: 'Set the 2027/28 referral ceiling for a four-person household at PHP 7,800.'
- **REVIEW** `hrg_operating_policy_2027_edition.pdf`: carries 5 of 5 distinctive words of the committed call: 'Set the 2027/28 referral ceiling for a four-person household at PHP 7,800.'

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 4 design-note vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the reworked pack, target.zip e94477d2)

# task202 reader answers

1. Decisive step sentence: none states it. Nearest: policy 9.2 "the scheme's awards are the awards of all accredited partners at the award volumes and award levels of the twelve months to 31 March 2027", plus request "only the two pilot provinces claim award by award on the portal".
2. none (no file ranks candidate ceilings; the annual report's province table gives averages only).
3. DATA_DICTIONARY.md (also export_manifest.csv).
4. Figure: none reads as the answer. Name: the request's "6.0 per cent"; the 'Partner claim portal provinces' band/component table in the annual report reads as an invitation to use the pilot mix.
5. hrg_operating_policy_2027_edition.pdf 9.1: "The ceiling for the 2027/28 scheme year is the lowest amount, being a multiple of one hundred pesos, such that ... the share of the scheme's awards that would be referred under clause 7 is at or below 6.0 per cent." with B.2 "taken to three decimal places" and 9.3 "An award is referred if it exceeds the ceiling for its band. Awards are counted gross." Literal result: my estimate PHP 7,800 (7,900 on a band-specific shape variant). Literal pilot-only execution gives PHP 6,600.
6. An analytical choice: only 2 of 8 provinces have per-award amounts, so the award-level distribution for the other six must be reconstructed from the returns' (count, total) cells. Deciding material: DATA_DICTIONARY.md "Partners claim monthly in aggregate" in the request, the portal file and the returns. Not semantics (although PRELIM/REVISED handling and band-code mapping are needed first).

### The main thread's scoring, against the goldens

The reader's stated confidence and its figures disagree, so I scored every annex figure against
`generator/figures.json` rather than taking its confidence as the measurement.

| Ask | Golden | Reader | Kept |
|---|---|---|---|
| A, transferred by quarter | 32,135,504 / 30,755,712 / 24,385,079 / 26,754,851 / 39,755,121 / 39,301,120 | 35,627,385 / 33,616,978 / 26,125,629 / 29,770,915 / 42,575,957 / 42,606,146 | **0 of 6** |
| B, held back by quarter | 267,012 / 147,874 / 270,559 / 165,711 / 275,978 / 228,163 | identical on all six | **6 of 6** |
| C, holds by reason | 17 / 30 / 36 / 46 / 76 / 73 | identical on all six | **6 of 6** |

**So the reader kept 12 of 18 ask figures, where the cracker model says 0 of 18.** Ask A's device held:
the reader summed the run lines as they stand, counted the doubled runs and is high on every quarter by
between 1.7 and 3.5 million pesos. Asks B and C did not hold. The reader found the register's
year-to-date convention by checking that passed plus held ties to the cumulative return total, and it
found the two meanings of the blank reason by cross-tabulating increments against reasons, which are both
ordinary hygiene moves rather than the cross-file comparisons the design assumed nothing would invite.

**The consequence, on the build's own arithmetic.** A response keeping 12 of 18 and landing the call
scores about 82, and because the asks are fully decoupled the mirror answers them the same way for about
49, so the pair is near 65 rather than 28.5. The ceiling the gate measured is therefore not the ceiling a
real response faces, and B and C need primaries from the silent list rather than from the seen list.

**The lesson, which is about method rather than this build.** The cracker sheet's stops are the author's
guesses at the opponent's routes, and its three modelled stops here (sum the run lines, sum the held
column, count blanks as a reason) were all shallower than what one reader at medium effort actually did.
A reader that beats the cracker has proved the cracker too shallow, so the reader's score is the
measurement and the cracker is only the model that gets the build to the reader.
