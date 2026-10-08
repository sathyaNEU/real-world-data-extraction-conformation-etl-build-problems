# AD39 — Which security goes into this week's close-out programme, or none, when only an issuer-wide denominator reproduces the published lists

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · securities settlement compliance |
| Mirrors | Compliance monitors that may act only once they reproduce an authority's published determinations exactly (seller-suspension models at marketplaces that must reproduce policy-team rulings, payment-network compliance lists at card schemes, cloud quota enforcement against published limits), then apply that method where nothing is published |
| Decision shape | Hold, forced by a blocking quantity: this week's single close-out programme goes to one of the flagged OTC securities, or to none |
| Committed call | The security closed out this week, or that the programme holds, with the run length that decides it and the earliest date a close-out could fall due |
| Gap · Pattern | Gap 4 (rule recovered by exact reproduction) over Gap 2 (unit) · a reproduction-gated control set whose only reproducing construction sums the issuer's share classes behind a join, with the settlement-day panel (the file holds rows only on reportable days) as the unit below it |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #2 counts file rows instead of the real unit |
| Calibration form | Parallel-run overlap: 61 settlement days on which the firm's candidate monitor ran alongside the exchanges' published threshold lists for the same 4,800 listed securities |
| Driving force | The test's denominator is "total shares outstanding", and the published lists are reproduced on all 61 days only when that means the issuer's shares across every class as filed before each date, summed through the CUSIP-to-issuer map, on a settlement-day panel the fails file does not store. The obvious per-class denominator matches 58 of 61 days and puts S-C, a dual-class issuer, at 14 consecutive threshold days. With the issuer-wide denominator S-C's run began three days later and stands at 11, nothing in the book reaches 13, and this week's programme holds. |

## 1. Situation

A clearing firm closes out fail positions that persist in threshold securities for 13 consecutive settlement days, and its buy-in desk runs
one close-out programme a week. This week's candidates are twelve securities quoted on an OTC venue that publishes no threshold list, so
the compliance policy applies the regulation's test to them with the firm's own monitor, which may drive a close-out only if it reproduces
every exchange-published threshold list over the parallel-run window. The parallel run has just ended, so this is the first week the
monitor can act on the OTC names. The firm holds the public fails-to-deliver files, filed shares outstanding by class, the CUSIP-to-issuer
map, the settlement calendar, the published lists for the overlap and the regulation's text. An analyst's leaderboard ranks the twelve by
summed fails, and the committee meets Monday.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the fails quantities, the filed share counts, the published lists and the analyst's sums. The analyst
  is right that S-A carries the most fails. Nothing reported is overturned; the difficulty is which construction the published lists
  certify, and what it says where no list exists.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the leaderboard and both voices. A day-panel, point-in-time monitor that matches 58 of 61 published days is
  still the natural build and still closes out S-C.
* **Instrument repair.** Make every fails row and every filing complete and exact: they are. The rule's wording still leaves the denominator
  open, and only the overlap settles it.
* **Lens swap.** The naive denominator is one class's shares; the answer's is the issuer's across classes, which changes which days count and
  moves the verdict from a named close-out to a hold, a different population of threshold days.

## 3. The driving force

A strong solver discards summed fails, treats each day's figure as a balance, builds every settlement day for each security from the
settlement calendar with missing days read as below the reporting floor, uses shares outstanding as filed before each date, and runs the
monitor against the overlap: 58 of 61 days match. It names S-C at 14 consecutive days and calls the three misses noise. Every step is
correct except the stopping point. The three missed days all involve dual-class issuers, where the published lists omitted securities the
monitor included. The regulation says only "total shares outstanding"; the filings report shares per class; and the lists are matched on
all 61 days only when the denominator is the issuer's shares across every class, each as filed before the date and summed through the
CUSIP-to-issuer map. S-C has a large unlisted second class, so its fails cross half a per cent of the issuer's total on fewer days, its run
began three days later, and it stands at 11.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The file's rows as they come, a missing day carrying the last balance forward, latest filed shares, five-day threshold runs to the review date | Close out S-A (20 days) | The regulation's test, run on the file as it comes | The fails file's documentation: a missing row is a balance below the reporting floor, not yesterday's figure; on a settlement-day panel built that way S-A's run is 6 |
| 1 | Every settlement day built from the calendar, missing days read as below the floor, latest filed shares | Close out S-B (17 days) | Balance semantics right; matches 55 of 61 published days | The filing dates: S-B's tender offer retired 60% of its shares mid-window, and with shares as filed before each date its earlier days fail the half-per-cent test, leaving a run of 10 |
| 2 | The day panel with shares as filed before each date, class denominator | Close out S-C (14 days) | Matches 58 of 61 published days; the misses look like noise | The overlap: all three misses are dual-class issuers the lists omitted, and the policy requires every day to match |
| 3 | **Decisive:** the same with the issuer's shares summed across classes through the CUSIP-to-issuer map, which matches 61 of 61 | **Hold: no security has 13 days; S-C stands at 11** | — | — |

* **Margins.** Rung 0: S-A 20 against S-B's 17 (1.18×). Rung 1: S-B 17 against S-C's 14 (1.21×). Rung 2: S-C 14 against S-B's 10 (1.40×).
  Every named run clears the 13-day trigger, and where several do, the policy's longest-run rule picks the name by at least 1.18×.
* **The blocking quantity.** On the only reproducing construction, the longest consecutive threshold-security run among the twelve at the
  review date is S-C's 11 settlement days, two short of the 13 that trigger a close-out; the next longest is S-B at 10. The earliest a
  close-out could fall due is S-C on the second settlement day after the review, if it stays on the test.
* **Partial correction priced (L3).** A solver who sums the issuer's classes but takes every class's shares from its latest filing, rather
  than as filed before each date, puts S-B back at 17 (a single class, so the issuer sum changes nothing for it), 1.55× S-C's 11 and four
  days past the trigger, and closes it out: a name, not the hold. A solver who sums the classes but keeps the file's rows as they come closes
  out S-A at 20.
* **Grid.** Missing days (carried or panel) × shares timing (latest or as filed) × denominator (class or issuer) = 8 cells. The four
  carried cells close out S-A (20 days), the two panel cells with latest filings close out S-B (17), and the panel, as-filed, class cell
  closes out S-C (14). Only the panel, as-filed, issuer cell holds, and it alone matches 61 of 61. The nearest wrong cell is rung 2's, one
  toggle and three days away.
* **Falsifiable.** S-C would have been closed out had its fails exceeded half a per cent of the issuer's total on the two settlement days
  before its run began, about 41,000 more shares each day.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The regulation's text says "total shares outstanding"; the filings report per class; no document says which the
   lists use or connects classes to issuers in this test.
2. **The corpus pins a construction, not a menu (Pattern B).** The issuer-wide construction matches all 61 published lists; the per-class
   construction 58, the latest-filing panel 55 and the carried-forward reading 44. Every rival errs by including securities the lists omit,
   so each overshoots the overlap's total listings as well. The denominator is a group sum over sibling classes behind a join from CUSIP to
   issuer, not a setting.
3. **No arithmetic symptom.** Fails rows, filings and the map reconcile; the per-class monitor's 58 days match exactly, and its three misses
   carry no arithmetic flag.
4. **Not a row predicate.** Each day's test needs a settlement-day panel built from the calendar, the issuer's classes found through the
   map, each class's shares as filed before the date, a sum, and a five-day run inside a thirteen-day run.
5. **The enumeration is arithmetic.** Threshold days for the OTC candidates are computed; nothing publishes them.
6. **No cutover date.** S-C's run moved because of where its fails sat against a larger denominator, not because anything happened on a
   date; S-B's tender offer is a dated event, and it only kills a decoy.
7. **Survives deletion.** Remove the leaderboard and both voices: the 58-of-61 monitor is still the natural stopping point.

## 6. The calibration corpus

* **Form.** The parallel run: 61 settlement days on which the firm's candidate monitor and the exchanges' published threshold lists both
  covered the same 4,800 listed securities.
* **What it pins.** The issuer-wide, as-filed construction on the settlement-day panel, 61 of 61. The policy's reproduction clause makes
  that the only monitor allowed to drive a close-out.
* **Every rule exercised.** The overlap holds mid-window tender offers and share cancellations, missing rows inside runs and nine
  dual-class issuers, so every component of the construction breaks at least one day when removed.
* **Twin pair.** Listed securities L-114 and L-207 have identical daily fails, identical listed-class share counts and the same market. L-114's
  issuer has one class and L-207's has a second, unlisted class 1.4 times as large, so the lists carry L-114 on 22 overlap days and L-207 on 11,
  2.0× apart, separated only by the issuer-wide denominator.
* **Resemblance points at the decoy.** S-C's fail pattern closely matches a listed security the firm closed out last quarter at 13 days.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The compliance policy: close out fail positions in securities that have been threshold securities for 13 consecutive
  settlement days; one programme a week, to the longest current run; a monitor may drive a close-out only if it reproduces every published
  list in the parallel run. The fails files' documentation of missing rows. The regulation's text, shipped as published. One sentence each.
* **Empirical pins.** The denominator, the shares timing and the reading of missing days, from the overlap.
* **Voices.** The analyst: "The leaderboard has never missed a big fail." The head of operations: "Ours is the monitor we've always run; three
  days out of sixty-one is rounding."
* **Licensed wrong basis.** The policy records that the firm's clearing broker escalates on runs built from the fails file's rows as they
  come and will bring its list to the committee.

## 8. Determinism by construction

* **Calendar.** Settlement days follow the filed holiday list; no run boundary falls on a holiday-adjacent day.
* **Filing timing.** Shares are taken from the latest filing dated before each settlement date; no filing in the window is dated on a
  settlement date itself.
* **Corporate actions.** No candidate changed CUSIP in the window, so CUSIP and security coincide for all twelve; S-B's tender offer changed
  its share count, not its identifier.
* **Run counting.** A run counts consecutive settlement days on the test up to and including the review date, and no run in the book stands
  at 12 or 13 on any construction, so counting the review date or not cannot move a verdict.
* **Floor.** No candidate's fails sit within 2% of 10,000 shares or of half a per cent on any day, so rounding the ratio cannot add a day.

## 9. Prompt sketch and deliverables

> The committee meets Monday to decide what goes into this week's close-out programme, and our analyst's leaderboard has four names on it.
> Tell me which security we close out this week, or that we hold, in a line the committee can minute, with the run length that decides it
> and the earliest date anything could fall due. Send `closeout_case.xlsx`, a chart `threshold_runs.png`, and a one-page `committee_note.pdf`.

* `closeout_case.xlsx` — each candidate's run under each construction with each construction's overlap match count (ask C), the lending sheet
  (ask A) and the volume sheet (ask B).
* `threshold_runs.png` — a strip per candidate across the last 20 settlement days, threshold days shaded under the per-class and issuer-wide
  denominators, the 13-day line marked, and S-C's three lost days annotated.
* `committee_note.pdf` — the committed verdict, the blocking quantity and what would have triggered a close-out.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve candidates, the 20-day average stock-loan fee from the lending feed. *Device:*
  some lenders quote in basis points a year and others as an indicative bucket from 1 to 10, whose bands the feed specification lists;
  averaging raw fields mixes the two and misstates seven securities. The verdict never uses lending data.
* **Ask B (device-carried).** For each candidate, average daily traded volume over the last 30 sessions. *Device:* halted sessions appear as
  zero-volume rows, and the market-data guide excludes them from averages; including them understates four securities.
* **Ask C (validity).** Each construction's overlap match count and each candidate's run under each construction.
* **Decoupling.** Clearing the issuer-wide denominator and the day panel changes no figure in asks A or B.

## 11. Rubric arithmetic

12 candidates × 1 (ask A) + 12 × 1 (ask B) + 4 constructions × (1 match count + 4 candidates' runs) (ask C) + the committed verdict, the
blocking quantity, the next-longest run and the earliest due date + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* Runs at the review date: S-A 20 carried forward / 6 on the day panel; S-B 17 with latest filings / 10 as filed; S-C 14 with the class
  denominator / 11 with the issuer's; S-E 8 on every construction. The reproducing construction tops out at S-C's 11, with S-B next at 10.
* S-A has missing rows inside its carried run and no share change; S-B is single-class with no missing rows; S-C has no missing rows and
  no share change, and its unlisted second class is 1.3 times its listed class.
* The overlap holds 61 days and nine dual-class issuers. The per-class construction misses three days, all dual-class; the latest-filing
  panel misses six (those three and three after share reductions); the carried-forward reading misses seventeen. Every miss adds a
  listing.
* L-114 and L-207 are identical on every per-security column.
* Lending quotes and volume summaries never touch fails files, filings, the map or the calendar.
