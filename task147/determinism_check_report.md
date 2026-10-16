# Verdict (task147, re-judge, fresh)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No rerun is needed. One optional pin is listed under Fix; it touches only supplementary answers 4 and 5, not the call.

**Why:** The shipped book forces the call. On the 06:12 book, Friday 13 and Saturday 14 August 2027 are each at 480. Stays are whole, so no later stay can cross either night. Replaying the five past seasons' later bookings under that constraint gives the closing week about 410 room-nights above 380 (400) and the concert week about 205 to 210 (200). The next-best weeks are Monday 2 to 8 August at about 65 and Monday 16 to 22 August at about 140. The per-night pickup route puts the concert week at about 556 to 600 and is wrong for a stated reason. The files back this up: the five past concert weekends (diary rows 2023-05-19 to 2026-06-05) were full at 480 five weeks out. Their neighbouring nights ended at 310 to 350, nowhere near the 420 to 470 of festival weeks. The supplementary tables reproduce exactly.

## Evidence (recomputed from target/)

| Value | Source | Result |
|---|---|---|
| Fri 13 and Sat 14 Aug 2027 book = 480 each | pms_reservations_extract (created before 06:12, not cancelled by then) | Reproduced |
| Whole 2027 book by night (26 Jul to 29 Aug) | same | Max elsewhere is 310 (Sun 15), then 284 (Sat 7) |
| Past-season book at the Thursday 5 weeks before opening night, dates as then stood | amendment log, reversed after the cut | Built for 2022 to 2026 |
| Replay of later stayed bookings in booking order, whole stay or nothing, 480 cap, 5-season mean | extract plus amendment log | Weeks 1 to 5 above 380: 9 / 66 / 209 / 140 / 411. Rounds to 0 / 100 / 200 / 100 / 400 |
| Variants: share = 0.9 flat, median over seasons, release 40 | same | Concert week 202 to 233, closing week 396 to 424. Same ranking |
| Omit attrition of the book (full-book stays) | same | 72 / 103 / 259 / 208 / 476. Closing rounds to 500, concert to 300. See Fork 2 |
| Naive routes: per-night additive pickup, multiplicative pickup, historic final average | extract | Concert week 502 to 555 (556 capped), closing week 406 to 432. Concert week would win |
| "About 420 room-nights of the other five nights carried by later stays that ran through the Friday and Saturday" | extract | 423 if a stay touches either night. 155 if it must cover both. Wording is loose, but it is explanatory and not decisive |
| Task counts by roster week, crew and Brennock, departure and stayover | hk_task_log, users, timesheets, notes | All 20 cells match the golden. Completed only, Re-clean excluded, DND and Refused excluded, notes mapped to timesheet names by day, `blockNN` logins counted as Brennock |
| Crew overtime by date worked in the reference | payroll lines | 17.25 / 20.75 / 15.25 / 11.25 / 14.25, matches |
| Billable hours 10 to 16 Aug 2026 | day-badge join, first IN and last OUT, LB-02 shifted +60 min, framework clause 4 | 59.25 / 59.50 / 55.75 / 59.25 / 59.75 / 59.75 / 59.75, matches |
| Weekly charge | 22.56 an hour, Sunday x1.25 | EUR 9,654.27, matches. The per-day rounded sum is identical |
| Marina Alves sent home on 12 Aug | timesheet note | 4.00 h minimum applies, matches the 55.75 total |

## Literal-reading forks

1. **Forecast method (main call).** The prompt and HK-04 say only "forecast". The literal text does not name the stay-through constraint. The constraint is forced by physics (a stay needs every night) and confirmed by the five past concert weekends. A per-night pickup forecast is the one surviving rival. It gives 600 and the concert week first, and it is wrong, so the fork does not hold up.
2. **Attrition of the book.** An analyst who replays later bookings against the unshrunk book gets 500 and 300 and still calls the closing week, because the ranking holds. The rounded figures are exposed. Cancellations and no-shows are in the extract status field and in HK-04 2.3, so a careful reader has to apply them. Moderate risk on the two stated figures.
3. **Week next.** The ranking concert week (209) over Monday 16 to 22 August (140) holds in all five single-season replays (203 to 249 against 100 to 206). A hybrid solver would constrain the concert week and use additive pickup elsewhere. That solver gets about 225 for Monday 16 to 22 August and could flip the second place. It is inconsistent method, not a licensed alternative. Note it as a thin margin on the "next" figure.
4. **LB-02 clock (asks 4 and 5).** No shipped document says the loading bay reader logs in UTC. Read literally, the hours are 56.75 / 57.75 / 53.75 / 57.5 / 57.0 / 57.0 / 57.75 and the charge is EUR 9,293.31. The UTC fact is recoverable from the data. Crew exits at LB-02 peak at hour 15 (123 events), while SE-02 exits peak at hour 16 (654), on a 16:00 shift end. Event order breaks less with the +60 shift (32 violations against 76). It is evidence in the files, not a stated rule, so the exposure is real but small.

## Files/Hygiene
PASS. 20 files. Formats: pdf (3), xlsx (7), csv (8), json, txt. One file has 360,694 rows, the 34 MB extract, and the task log has 13,887.
- Distractors that are relevant but unused: compset_rate_shop, the tourism occupancy survey, the night audit statistics (reconstructing occupancy from the extract is enough), the HR list beyond the three logins.
- Realistic noise: stale amendments, channel code revision, UTC against local, shared `blockNN` logins, supervisor notes, 2020 and 2021 edition years.
- No authoring disclosures found in the shipped text. Dates are coherent with the 2027-07-01 snapshot.
- License and provenance were not checked (metadata.json is out of bounds). Nothing exclusion-level.

## Stump power
Strong. The pickup route a capable analyst would take (per-night pickup or final-to-book ratio, capped at 480) gives the concert week first at about 600. It reproduces Gate A's naive path exactly and goes wrong because each stay is a whole booking across nights. Stumping for the right reason: the data has no wrong number to catch. The asks add device-heavy attribution (notes, three reassigned logins, the day-badge join, the UTC reader) that a strong model can plausibly get partly wrong.

## Stumping type
`mechanism: forecasting` (a binding stay-through capacity constraint on honest data), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. On clean data the whole-stay constraint would still stump a pickup forecast. No reported figure is misleading; there is no reported forecast.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Field analysis: a length-of-stay constrained booking-pace forecast (constrained against unconstrained demand), swap test fails for any non-lodging setting. Layer 1: amendment-log as-of reconstruction, UTC against local, channel revision, festival edition gaps. Layer 2: constrained demand under whole-stay booking. Easy route: per-night pickup capped at 480, giving the concert week about 556 to 600 and the wrong block week.

## Fix
none required. Optional, solution or input_files: pin the LB-02 clock, for example one line in folder_contents.csv ("LB-02 logs in UTC"), to close fork 4. It would weaken the device on asks 4 and 5 and needs no rerun of the main call. Also loosen "ran through the aligned Friday and Saturday" in the narrative to "touched either".
