# Determinism check, task142 (stage 4 re-judge)

The single re-judge after the FIX_NOW pass, verbatim: a fresh isolated thread at medium effort that saw a fresh unzip
of `target.zip`, the prompt and the submission's graded blocks. The first verdict (NOT_DETERMINISTIC on one ask cell,
the re-post survivor at Kingsdale September, FIX_NOW) and its disposition are in commit fe9bd2c.

---

# Verdict (task142, re-judge, fresh)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed, no rerun. Optional note: nothing in the shipped text states that admissions are Poisson, that stays are pooled across Members, or that duplicate postings are collapsed. Each is pinned by evidence in the files (below), so none is an open fork.

**Why:** Clause 2.3 to 2.7 of Schedule 2 file the estimand, the expected value (plan), the lot rule and the booking order. The files separate the candidate methods. Admissions are Poisson in the history (dispersion index about 1). Stays are long and clustered, and the pooled stay model reproduces each plan's own Jan to Mar visits to within 1 to 2 visits. A compound-Poisson requirement therefore gives P90 of 2,400 / 2,150 / 1,800 / 1,400 / 1,250 and the booking 300 / 250 / 225 / 75 / 0. The visit-Poisson and history-spread routes give clearly different bookings. All three supplementary tables and the chart totals recompute to the cent.

## Evidence (recomputed from target/)

**Literal reading, main call.**
- Requirement (2.3) is all HITH visits on the quarter's days, whoever makes them. Expected value (2.5) is the plan's Jan to Mar visits. P90 (2.4) is taken over the quarter total. Lots (2.6) are 25-visit lots covering the excess over in-house capacity. Order (2.2/2.7) is N, R, W, K, H until 850 is used.
- Silent on: the distribution family, the stay source, pooled versus per-Member stays, which episodes count as completed, and the treatment of unrounded versus rounded P90 in the lot calculation. I tested each (below).

| Item | Result | Source |
|---|---|---|
| Plan Jan to Mar visits 2,143 / 1,905 / 1,570 / 1,209 / 1,064 | reproduced | operating plans, "All / Nurse visits" row, Jan+Feb+Mar |
| In-house visits 2,112 / 1,911 / 1,589 / 1,246 / 1,086 | reproduced (net shifts x visits per shift) | capacity return v1.1 |
| Visit schedule | census `nurse_visits` equals the PDF schedule on all 32,517 rows | census vs HITH-CG-07 |
| Admissions Poisson | monthly and weekly dispersion index about 1.0 (mean 1.05 and 0.99) | episodes |
| Compound-Poisson model (episodes admitted to 30 Jun 2026, separated, crosswalk applied, pooled by stream; N and W take the Alliance H04 stays; admissions Oct to Mar at the plan's monthly rate) | model mean 2,143 / 1,905 / 1,569 / 1,210 / 1,065 against plan 2,143 / 1,905 / 1,570 / 1,209 / 1,064 | episodes, crosswalk, plans |
| P90 (exact Panjer recursion) | 2,397 / 2,148 / 1,797 / 1,404 / 1,248, so 2,400 / 2,150 / 1,800 / 1,400 / 1,250 to the nearest 50 | as above |
| Lots | N 288 over (12 lots, 300), R 239 (10, 250), W 211 (9, 225), sum 775, K gets the 3 left (75), H none | Schedule 2, capacity return |

**Robustness of the main call.**
- 40 bootstrap resamples of the stay data: the booking is 300 / 250 / 225 / 75 / 0 in 40 of 40. P90 ranges are N 2,390 to 2,406, R 2,142 to 2,155, W 1,791 to 1,806, K 1,399 to 1,410, H 1,243 to 1,252.
- Normal approximation with compound variance gives 2,394 / 2,145 / 1,794 / 1,401 / 1,244, the same rounded figures.
- Stay-set variants, recentred on the plan per 2.5 (which the plan's means support):

| Variant | P90 (N / R / W / K / H) |
|---|---|
| Stays since Jan 2025 | about 2,398 / 2,147 / 1,800 / 1,402 / 1,245 |
| Stays since Jul 2025 | about 2,404 / 2,153 / 1,805 / 1,407 / 1,248 |
| Mode-1 stays only | about 2,404 / 2,154 / 1,805 / 1,409 / 1,251 |
| Per-Member stays | about 2,397 / 2,148 / 1,798 / 1,397 / 1,258 |

  Rounded requirements and all bookings are unchanged in every variant once centred on the plan (2.5). Without recentring, per-Member stays would move Kingsdale to 1,372 and Hillcrest to 1,306 (one 50 band), but 2.5 pins the mean to plan and the plan's own visits match the pooled model.
- Competing answers:
  - Poisson on visits (plan + 1.2816 sqrt(plan)): 2,202 / 1,961 / 1,621 / 1,254 / 1,106, so the booking is 100 / 50 / 50 / 25 / 25 = 250, as the golden says.
  - Weekly-spread route (sd x sqrt 13): 2,235 / 2,000 / 1,632 / 1,305 / 1,179.
  - Monthly-spread route: 2,247 / 2,065 / 1,660 / 1,378 / 1,238.
  - Fixed plan admissions with random stays only: 2,240 / 1,997 / 1,655 / 1,282 / 1,132. This contradicts the observed Poisson variation in admissions, so it is not a defensible reading.
  - All give clearly different bookings. None is supported by the structure of the data (long stays, new BJI stream at N and W with no own history, so a history spread cannot contain it).

**Supplementary answers (all reproduced).**
- Fees (monthly, in dollars, from the visit file). The method was UTC to Melbourne conversion (all AEST, no DST in Q3), rate by kind, loading by start time (Fri 25 Sep is the only Q3 public holiday), attempted at $68.40 with no loading, cancelled at nil, the month of the start, the C3920 account mapped to Westmere, 30 duplicate postings collapsed, and the 18 unique C4466 visits attributed to Members through the intake log numbers (`C4466/IL26-nnnn` joined to the intake register's Organisation). Result against golden:

| Member | Jul | Aug | Sep |
|---|---|---|---|
| Northgate | 3,819.20 (3,819) | 14,501.04 (14,501) | 8,111.69 (8,112) |
| Riverbend | 5,856.11 (5,856) | 4,174.19 (4,174) | 13,348.58 (13,349) |
| Westmere | 4,473.80 (4,474) | 6,435.62 (6,436) | 6,143.33 (6,143) |
| Kingsdale | 7,059.11 (7,059) | 5,350.96 (5,351) | 8,787.26 (8,787) |
| Hillcrest | 2,652.12 (2,652) | 6,640.95 (6,641) | 7,162.76 (7,163) |

- The 30 duplicate pairs are the same patient, same nurse and same kind, 0 to 12 minutes apart, both complete, with overlapping times. There is a clean gap to the next pair (60+ minutes). Not collapsing them would raise every figure, so this is the one step not filed in the prompt. The files support it: overlapping records for one nurse and one patient cannot be two visits, and the data dictionary says `visit_no` is assigned at posting and late posts arrive on reconnect.
- Referral response. 212 portal rows plus 9 phoned-through "Referral" rows from the intake register (Referral follow-up rows excluded) gives 56 / 43 / 40 / 45 / 37 referrals. Accepted within 2 hours (Schedule 4.5 wording; response UTC converted to Melbourne, no value between 115 and 120 minutes) is 75.0 / 81.4 / 82.5 / 73.3 / 75.7 per cent for N / R / W / K / H. Accepted referrals first visited within 24 hours (first completed or attempted visit at or after acceptance, patient key by digits without leading zeros or by IL number) is 94.1 / 82.1 / 94.4 / 84.6 / 90.6. All reproduced. The "any response within 2 hours" reading gives 82.1 / 88.4 / 92.5 / 84.4 / 86.5, but 4.5 says "accepted", so it is not a fork.
- Chart. Payable visits (completed or attempted) are 161 / 140 / 106 / 130 / 103 = 640, reproduced. Pay weeks come from the finance calendar, 13 weeks from Mon 29 Jun.

**Fork table (literal reading).**
- Hold-in-pool vs per-Member stays: same bookings; requirement bands same after the 2.5 recentre.
- Round-before or after lot calculation: same lots.
- Dedup window: any window from 15 to 55 minutes gives the same 30 pairs.
- Phone referrals in or out: the prompt says "referrals it made to Bellbird"; the intake log is Bellbird's own record of referrals made by phone, so in. A portal-only reader gets 53 / 42 / 38 / 43 / 36, which does not match the golden. This is Layer 1 mess (imperfect sources), forced by the files (the C4466 visits for these patients exist only through those log numbers).

## Files/Hygiene
PASS. 20 files; formats csv, pdf, jsonl, xlsx, docx (five); census 32,517 rows. Distractors that are relevant but unused: the patient survey, the 2025-26 service report and declined referrals, the Bellbird client accounts file (used for mapping only). Provenance clean (no generator banners; PDF producer fields empty; office metadata carries fictional author names, no tool signatures). Dates cohere: extracts before 2 Nov 2026, lodgement due 6 Nov 2026, capacity v1.1 of 19 Oct. No answer contamination (fictional, bespoke). The cross-batch reference check was not run (other task folders are outside the permitted directory).

## Stump power
Strong. The easy routes (Poisson on plan visits, weekly or monthly spread of history) each look reasonable and each books about a third of the correct amount (250 vs 850 used; Kingsdale and Hillcrest also land wrong). The decisive step is building the requirement from episode stays under the quarter's days with the new BJI stream borrowed from the other Members. The Layer 1 mess (crosswalk, DST/UTC, duplicates, C4466 account, intake log referrals, Altona Park account) is heavy on the asks, which is where the ask weight sits. No shipped artifact ranks the candidates wrongly.

## Stumping type
`mechanism: method_or_model_selection (forecasting)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported numbers (plan, capacity, history) are fine; the difficulty is choosing the compound-over-stays distribution against the visit-Poisson and period-spread routes. Clean data would still stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: replacing "visits" with "megawatt-hours" or "hospital" with "school" breaks it, because stay-length-driven demand clustering across a quarter boundary is hospital-in-the-home occupancy modelling.
- Layer 1: crosswalk of old to new program codes, UTC against Melbourne time, duplicate postings, account and intake-log keys, a merged campus account. Layer 2: capacity requirement distribution built from admissions and stays.
- Easy route: plan plus a Poisson margin (books 250: N100 R50 W50 K25 H25) or history spread, both treating visits or periods as independent. A strong analyst who cleaned everything correctly still files these.

## Fix
none.
