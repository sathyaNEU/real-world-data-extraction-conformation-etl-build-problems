# Verdict, task130 (fresh judge pass)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed; optional note: the prompt and dictionary leave "FTE the payroll paid" as hours/173.33 only by implication (see Evidence fork 2), which is acceptable on the asks.

**Why:** The shipped trust agreement (Art. 2.1/2.2, Sched. A) and funding policy (3.1 to 3.4) fix the estimand: expected cost, at 2027 level, of Claims first made in 2027 from incidents on or after each entity's Transition Date, with experience pooled by Schedule B class, per covered FTE-year. Executed literally, that estimand gives $1.264M, which rounds to $1,250,000, and every shortcut I tried lands far from it (13.1M, 2.6M, 0.64M, 0.93M). All load-bearing values and all supplementary answers reproduced from the bundle. Taxonomy: none.

## Evidence (recomputed from target/ only)

| Item | Golden | Mine | Source |
|---|---|---|---|
| Experience Claims, 2016-2024 incidents with a covered clinician, one per incident | 3,043 | 3,043 (class by first-named = same under both orderings) | rm_claims_register_extract_20261002.csv + payroll job in incident month + Sched. B code sets |
| Covered FTE-years 2016-2024 | 13,747.1 | 13,747.07 (L status adds 0; T-month FTE included) | clinician_fte_by_month csv, both code sets (switch July 2020) |
| 2027 contribution | $1,250,000 | $1,263,838 (daily exposure, per-claim lag weighting, 5% trend from incident year) | staffing plan xlsx, Transition Dates |
| AMC missing open claims | 4, $839,000 | 4, $839,000 (IR-2025-01259 832k, 09682 5k, 00766 0, 02619 2k) | register vs QMPL 2026-09-30 run via RMN notices, prior_claim_no, no-ref suits by entity/date/type |
| CMG missing | 5, $16,000 | 5, $16,000 | register vs Stoneleigh csv |
| TFH, BCH missing | none, none | none, none | same |
| Covered FTE Jul/Aug/Sep (TFH, AMC, CMG, BCH) | 188.6/187.1/188.0; 464.5/463.6/465.4; 1,037.1/1,036.8/1,040.6; 105.5/106.7/108.2 | identical (REG+PDM+PTO hours/173.33, crosswalk + Sched. B, trainee worker-months removed, entity by cost centre) | hcm pay lines, crosswalk, cost centre directory |

Robustness of the main figure: bins of 15/30/60/91 days give 1.267/1.265/1.216/1.158M; no class pooling 1.186M; unmerged claim numbers 1.185M; valuing all defendants 1.269M; trend from claim-made year 1.256M; 2M per-claim cap changes nothing (the three claims over 2M have delay over 365 days and carry no 2027 weight). All round to $1.25M. Observation: no experience incident is right-censored for the relevant window (delays at or under 364 days are fully observed for 2024 incidents).

Competing answers and where they land (all wrong by the filed estimand):
- No lag, full-year exposure at pooled average cost: 13.1M.
- Window count (lag-adjusted) times class average severity: 2.6M.
- Window count times average cost of claims made within a year: 0.64M.
- Severity curve fitted on delay (quadratic log): 0.93M.
- Untrended: 0.92M.

Forks examined:
1. Month-granularity exposure: month-start placement gives 1.388M (would round to 1.5M), mid-month 1.279M, month-end 1.154M. The staffing-plan note ("held through the month") and policy 3.2 license the daily reading, so this is not an open fork, but it is the one thin spot: margin to the 1.375M boundary is about 8.8 percent.
2. Ask 3 "FTE the payroll paid": hours/173.33 (golden) vs the position `fte` field. The latter gives e.g. AMC Jul 467.3, BCH Sep 106.0. The dictionary says hours are "paid on the line" and positions are 173.33 hours at 1.0 FTE, so hours is the literal reading; mild risk only, on an ask (asks are free of the main-call bar).
3. Open-claim matching: direct claim_no matching alone would flag 23 (AMC), 40 (CMG), 10 (TFH), 3 (BCH) claims; the dictionary and shipped notices/prior_claim_no/DOL fields support the golden linkage. Pre-tenure open claims (CMG 9, AMC 2, TFH 1, BCH 3) belong to earlier carriers and are excluded by the premium history. CONTRACT-only incidents are excluded per the dictionary.
4. Latest loss run is the 09-30 file (06-30 rev1 is a distractor).

## Files/Hygiene
PASS. 17 files; formats pdf, xlsx, csv, md; largest file 224,767 rows. Distractors in play: patient_safety_events csv, defense_panel_invoices csv, QMPL 06-30 rev1 run, premium-history rated FTE. Operational artifacts carry realistic mess (changed job-code sets July 2020, cost-centre effective dates, mixed date formats and RMN formats across loss runs, no-reference suits). No authoring or benchmark language, no dates after the setting (cost centre 140-7110 effective 2026-10-01 is not used in the paid months). No answer contamination. Not exclusion-level. Cross-batch fingerprint not run (no access to other tasks, as the brief forbids).

## Stump power
Good. The tempting routes (annual frequency times average severity, with or without a lag-completion factor, or a smoothed severity curve) land at 13.1M, 2.6M, 0.64M or 0.93M against the correct 1.25M, because claims made inside 2027 from post-Transition incidents are the cheap disclosed-harm and program-request claims (median under 60 days about $50k; 120 to 365 days about $5 to $8k) while the expensive suits (over 365 days) cannot be made inside the window. A strong model that sizes the window by claim count but prices at average severity should fail. Estimated that a majority of strong runs miss it; the asks add further independent failure points (linkage of 23+40 non-direct matches, trainee exclusion).

## Stumping type
`mechanism: forecasting` (expected cost of an open window, lag-conditioned, validated on a fully observed experience), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported register and payroll figures are fine; the difficulty is the estimand (claims made in the window from incidents after the retroactive date, with severity depending on reporting delay), and it persists on perfectly clean data.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: reporting lag, claims-made trigger with a retroactive date, FTE exposure by specialty class and trend-to-cost-level are actuarial funding work and do not survive swapping nouns. Layer 1: layout/code-set change July 2020, three loss-run layouts with imperfect keys, payroll replaced by HCM in 2026, a prelim and a revised loss run. Layer 2: lag-conditioned expected-cost estimation. Easy route for a strong analyst who read everything correctly: frequency times average claim cost over the 2027 exposure (or lag-adjusted count times mean severity), giving 13.1M or 2.6M instead of 1.25M.

## Fix
none (prompt, files and solution stand). Optional hardening is not needed. If the author wants extra margin on the rounding boundary, nothing in the shipped text requires a change; the daily-exposure reading is already licensed.
