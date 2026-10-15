# Determinism check, task141 (stage 4)

The isolated judge's verdict, verbatim, then the disposition. The judge saw a fresh unzip of `target.zip`, the prompt
and the submission's graded blocks; it ran at medium effort.

---

# Judge verdict, task141 (Dorrance County presumptive release tier)

- **Verdict:** DETERMINISTIC.
- **Disposition:** FIX_NOW (optional, ask-side only). The main call and the stump are clean and need no rerun. I would pin two conventions in the prompt wording of the asks: boarded-out Halsey days count as bed-days in custody, and "within 90 days" is inclusive of day 90. Neither touches the main recommendation.

## Why
The draft's tier (2.2) releases every eligible defendant at or below the top score. Floor 2.3 therefore applies to that whole population, including the 26.0 per cent of eligible score-4 defendants the magistrates now hold.
- **Easy route:** the released-only rate (87.9 per cent at score 4) puts the top score at 4.
- **Data route:** the files carry a rota of four magistrates per shift taking appearances in turn, and release shares run from 64 to 99 per cent at score 4. They also show the selection directly: among released score-4 defendants, the arrest rate rises with the magistrate's leniency (slope 0.55, p < 0.001).
- **Result:** extrapolating to 100 per cent release gives score 4 at about 76 per cent, below the floor, and score 3 at about 90 per cent, above it. The top score is 3.

## Evidence (recomputed from the bundle)

| Item | Golden | My recomputation | File and field |
|---|---|---|---|
| Eligible appearances with a screen, 1 Oct 2021 to 30 Sep 2025 | 55,005 (7,439 at score 4) | 55,005 (7,439) | Legacy and new first-appearance files, crosswalk, Appendix B, holds, screens (booking number, else SID within 12 h; all 4,597 paper screens link) |
| Release share, score 4 | 74.0% (26.0% held) | 74.0% | jail_bookings, UTC to Eastern (booking-to-appearance gaps 0.75 to 7.3 h confirm the conversion), 24 h, releasing types WPA, UNSEC, CUST, BOND |
| Released-only safe rate, score 4 / score 5 | 87.9 / 78.0 | 87.92 / 78.00 | state_arrest_extract (type NEW), window ends on the day of the last disposition (see forks) |
| Extrapolated safe rate at 100% release, scores 1 to 6 | 95.1, 93.1, 90.3, 75.8, 63.6, 61.6 | 95.1, 93.1, 90.3, 75.8, 63.6, 61.6 | 32 magistrates, caseload-weighted line of arrests per appearance on release share |
| Ask 2, bed-days | 2,210 / 4,660 / 5,950 / 8,330 / 3,440 / 2,040 | 2,213 / 4,661 / 5,949 / 8,329 / 3,438 / 2,037, rounding to the golden | Midnight counts across the booking, annex and Halsey chain; Halsey date-out used where the jail has no release record (matched one to one to the 2,276 BO bookings) |
| Ask 3, EM days | 28,620 / 26,820 / 16,250 / 10,380 / 4,660 / 2,220 | 28,618 / 26,818 / 16,247 / 10,382 / 4,657 / 2,220, rounding to the golden | Union of calendar days per released appearance; Sentry handoff days double-billed; invoices without a court case linked by name and DOB to the latest prior release |
| Ask 4, releases and missed court dates | 260/6,860, 349/5,525, 340/3,364, 308/1,976, 78/338, 20/77 | Identical | FTA events on the appearance's cases, following district_case_ref to the superior case; 90 days from release |

Robustness of the main call:
- Release-share covariates are balanced within score (only calendar year trends); adding year fixed effects, a quadratic, or leave-one-out individual-level 2SLS gives score 3 at 90.4 per cent and score 4 at 70 to 76 per cent.
- Standard error at 100 per cent release is 0.8 points at score 3 and 1.6 points at score 4, so neither is a near-tie against 85.
- **Competing answers:**
  - Tier 4 comes from the released-only rate, or from observable-adjusted prediction (held and released are indistinguishable on screen items, 87.9 per cent). The leniency gradient refutes both, so this is the stump, not a fork.
  - Tier 2 comes from counting every held defendant as arrested. That is a worst case, not the "expected" rate that 2.3 asks for.

Minor forks (all on supplementary answers; none changes the main call):
- **Disposition boundary in 2.4:** counting an offense on the disposition day moves score 4 released-only from 88.05 to 87.92 per cent and the extrapolated score 5 from 64.8 to 63.6 per cent. The tier is unchanged.
- **Bed-days:** the jail codes BO as a release type and CJAC says its population excludes contract beds. A jail-only count (1,820 / 3,670 / 5,040 / 7,090 / 2,750 / 1,760) is a defensible misreading, while "in custody" and the Halsey invoices support the golden.
- **Missed court dates:** an exclusive day 90 gives 260/349/338/307/76/20 and shares 3.8, 6.3, 10.0, 15.5, 22.5, 26.0. Measuring from the appearance date instead of the release date moves score 3 to 339.
- **Defendants with several released appearances:** the EM score assignment (latest prior release) is unstated and moves some figures by a few days. Rounding mostly absorbs it.

## Files/Hygiene: PASS
- 20 files in six formats: csv (11), xlsx (4), pdf (3), docx (1), txt (1). Largest files are 294k, 200k and 194k rows.
- Every row-count claim and key (legacy case numbers with a space, booking numbers without B and hyphen, initials against employee numbers) is documented in the README.
- There is no authoring or benchmark language. The README is an in-fiction extract note.
- Temporal coherence holds: extracts to 30 Sep 2026, run 2 Oct, draft dated 6 Oct 2026. The last jail release timestamp is 23:57 Eastern on 30 Sep.
- The Halsey, CJAC and reported-crime files are usable distractors. Minor tell: the docx app.xml shows 0 words and a python-docx style set. This is non-exclusion level, in-house fix.
- Not exclusion-level. Licence and source records were not visible to me.

## Stump power
High. The released-only 87.9 per cent is a correct number, and a strong solver who cleans the data and applies the draft's definitions correctly lands on tier 4 or, if cautious, tier 2. Reaching 3 requires seeing the selective-release problem and using the magistrate rota as an instrument. The three supplementary asks add independent traps: Halsey boarded days with no jail release record, Sentry handoff double-billing, and superior-court case keys that differ from the district ones. I expect the top two to be held down by the asks as well.

## Stumping type
`mechanism: statistical_rigor` (selective labels, leniency-instrument extrapolation), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

No reported number is wrong, and on clean data the held group would still be unobserved. This is not the banned scaffold.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **Domain:** validating whether a risk tier meets a safety floor when outcomes are seen only for the released is the field's own work (pretrial risk-assessment validation). The swap test fails: "hospital" or "school" nouns do not fit.
- **Layer 1:** two court systems with different keys and codes, UTC against Eastern, paper screens without booking numbers, contract-bed invoices, double-billed handoffs.
- **Layer 2:** selective labels with quasi-random magistrate assignment.
- **Easy route:** released-only rate (or observable-adjusted prediction) gives 87.9 per cent and tier 4.

## Fix
- **Where:** prompt, ask side only. Optional one-clause pins: "including days boarded out to Halsey County" in the bed-days ask, and "within 90 days of release, inclusive" in the missed-court-date ask. Strip the docx metadata tells (zero word count in app.xml, python-docx style set).
- **Main call:** none.

---

## Disposition

**DETERMINISTIC, FIX_NOW optional on the asks, applied in one generator pass; no re-judge.** The main call, the
stump, the ladder and every graded figure are unchanged: `freeze.py check task141 --mode determinism` and `--mode
rubric` both exit 0. The prompt is unchanged (992 characters). Each finding:

| Finding | Ruling | Where it is closed | Asserted in `checks.py` |
|---|---|---|---|
| Bed-days: the boarded nights (BO coded as a release type, CJAC's population without contract beds) | fixed, by the WHAT | The README's detention note now reads "a stay runs from booking to release from the Sheriff's custody; a defendant boarded out stays in the Sheriff's custody while boarded out. Custody is counted at midnight, each count dated with the day it begins; one bed-day is counted for each midnight count at which the person is held." It names no contract county and no invoice. | SF18: the boarding read as a release (S1) and the detention center's own midnight counts (S8, the judge's 1,820 to 1,760) each miss all 6 figures |
| Missed court dates: day 90 inclusive or not; from the release or the appearance | fixed, by the WHAT | The README: "Days after a release are counted from the release date, and a period of days includes its last day: the 365 days after a release on 1 March 2024 run to 1 March 2025, that day included." The same convention is the one the call's 365-day window already follows. | SF23: the 90th day left out and the count from the appearance each move figures; the window's first day converges (no missed court date falls on a release day) |
| Disposition-day boundary in 2.4 | same call, closed as a fork row | Draft 2.4 left as filed (a document the call reads). | SF30: with the disposition day left out, every construction of the gradient files scores 1 to 3, score 4 under 80 per cent and score 3 at 90 to the nearest 5 on the shared constructions, and the released defendants' rate still files 1 to 4 |
| Monitoring days for a defendant with several released appearances | fixed, by the WHAT | The README: "Days on electronic monitoring are counted for each release: every day on which the defendant wore a monitor under that release's conditions, for all or part of the day." | SF35: a line with no case number put to the first release moves 5 of 6 figures, and every enrollment starts on or after its release and ends by the defendant's next release; SF36: a day once per defendant converges with once per release at every score; SF34: elapsed days (part days not counted) miss all 6 |
| The docx metadata tells (zero counts, python-docx style set) | fixed | Both Word documents, the draft under `target/` and the golden memo, are written in Word's own form by `postprocess.normalize_docx`: no styles-with-effects copy, preview picture, bibliography part or unused list definitions; the styles in use only; the document's own session and paragraph ids; Word's part order, relationships and XML declarations; words, characters, paragraphs, lines and pages counted from the text and its layout. Text and formatting unchanged. | realism block (template parts, declarations, statistics recounted, minute stamps); `verify.py` recounts the words on its own path |
| The judge's prompt-clause pins | declined | The prompt is at 992 of 1,000 characters and a clause naming Halsey points at Ask A's device; the conventions above sit at the README instead. | n/a |

The leak reader's readings were ruled in the same pass: the safety rate's population on a written promise against
any condition (SF31, the same call on the gradient either way), Ask A's eligibility with the no-detainer test (SF32,
draft 2.1's defined term), missed court dates across several cases (SF33, the prompt counts releases), and part days
of monitoring (SF34, the README).

**Cost to the asks.** The custody note makes Ask A's boarding device seen rather than silent: a reader who takes it
as a cue to look for the boarded defendants' ends finds them on Halsey's bills. The design's pair arithmetic already
plans for the strongest response cracking Ask A (pair 36.4); both top responses cracking it gives about 41.0, under
the 50 bar. Asks B and C keep their devices (the superior court continuation, the same-day equipment change).
