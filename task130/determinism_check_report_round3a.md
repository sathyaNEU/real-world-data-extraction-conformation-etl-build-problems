# Verdict (task130, fresh pass after redesign)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is needed. Nothing here requires a model rerun.

**Why:** Every committed answer reproduces from the shipped files, and the main number is robust to every defensible variant I ran. The contribution is $1,263,838, which rounds to $1,250,000. The rounding band is $1.125M to $1.375M, and the defensible variants span $1.19M to $1.30M. The filed text pins the estimand: Funding Policy 3.1 to 3.4, plus Trust Agreement 1.3, 2.1, 2.2, Schedule A and Schedule B Note 2. The method stays open only where the data separates the candidates. The decisive step is analytical: claim cost depends on the delay from incident to first making, and the 2027 window truncates delay. The prompt and the files do not announce either point.

## Evidence (recomputed from the bundle)

| Item | Golden | My recompute | File and field |
|---|---|---|---|
| Experience Claims, 2016-2024, one per incident, covered clinician in the incident-month job | 3,043 | 3,043 reproduced | rm_claims_register_extract_20261002.csv, joined to clinician_fte_by_month on employee_id and pay_month, Schedule B code sets |
| Covered paid FTE-years 2016-2024 | 13,747.1 | 13,747.07 reproduced | clinician_fte_by_month_2016-01_2025-12.csv, `fte` summed over Schedule B jobs, both code sets, divided by 12 |
| 2027 contribution | $1,250,000 | $1,263,838 reproduced, rounds to $1.25M | The claim-level estimator: each Claim at its 1.05^(2027 - incident year) cost, counted once for each 2027 FTE-year of its class with at least its own delay left before 31 Dec 2027, divided by the class's experience FTE-years. Exposure comes from clinician_staffing_plan_2027.xlsx from each Transition Date, spread by day within each month. |
| Ask 2, Tolliver Falls | none | none reproduced | Register open and reopened matters, non-CONTRACT, incident on or after the carrier's first term (QM from 1 Jan 2021 per the premium history). Loss-run reference normalised: CL with and without hyphens, RMN mapped to incident_no through rm_carrier_notices, so a suit matches through its incident. |
| Ask 2, Alderwick | 4 claims, $839,000 | 4 claims, $839,000 reproduced | CL-2026-1143 reserves $832k (a resident defendant), plus CL-2026-1140 $5k and CL-2026-1161 $2k, plus CL-2026-0833 with $0 reserves |
| Ask 2, Medical Group | 5 claims, $16,000 | 5 claims, $16,000 reproduced | CL-2026-0952, 1148, 1157, 1141, 1151 |
| Ask 2, Brennick | none | none reproduced | The only candidate was a CONTRACT claim |
| Ask 3, Tolliver Falls, Jul/Aug/Sep | 188.6 / 187.1 / 188.0 | 188.63 / 187.10 / 187.97 reproduced | hcm_clinician_pay_lines: all hours on covered-profile lines divided by 173.33, by cost-centre entity. A resident's or fellow's additional covered position is excluded. |
| Ask 3, Alderwick | 464.5 / 463.6 / 465.4 | 464.52 / 463.57 / 465.37 reproduced | same |
| Ask 3, Medical Group | 1,037.1 / 1,036.8 / 1,040.6 | 1,037.12 / 1,036.80 / 1,040.58 reproduced | same |
| Ask 3, Brennick | 105.5 / 106.7 / 108.2 | 105.51 / 106.67 / 108.22 reproduced | same |

### Literal reading and the forks I tested (main call)

Every variant below stays inside the $1.125M to $1.375M band unless marked.

| Variant | Result |
|---|---|
| Strict versus inclusive day count; delay +1 | $1.256M |
| Valuing all defendant rows rather than covered rows | $1.269M |
| Trend to mid-2027 (+0.5 year) | $1.295M |
| One class pooled instead of seven | $1.186M |
| Claim numbers unmerged (3,097 Claims) | $1.185M |
| Capping at the $2M limit (no change: the three claims over $2M have delays of about 1,000 days, so zero 2027 exposure) | $1.264M |
| Delay-bin severity: 3, 6 or 8 bins, class-specific | $1.23M to $1.26M |
| Kernel-smoothed severity on delay, bandwidth 5 to 40 days | $1.21M to $1.27M |
| Over-smoothed kernel, bandwidth 80 days (outside the band) | $0.97M |
| Badly mis-specified quadratic log-curve (outside the band) | $1.61M |
| No trend (not licensed by Funding Policy 3.4; outside the band) | $0.92M |

- **Easy routes, which give wrong, distinct rounded answers:**
  - Expected in-window count times the average cost of all claims: about $2.6M.
  - Expected in-window count times the average cost of claims made within a year: about $0.64M, which rounds to $0.75M.
  - Frequency times average severity on the full 2027 exposure, ignoring the retroactive date: about $13.1M.
- **Competing answers on the asks:**
  - Counting open claims from before the carrier's first term (AMC +2, CMG +9, BCH +3, TFH +1) is excluded by "its policies with the carrier". Those incidents sit under Corrigan Lane, Westerholm, Tallis and Halberd per the premium history, even though register `coverage_line` carries the current programme code for them.
  - Counting CONTRACT claims is excluded: the data dictionary says "where the clinician's own group insures them".
  - A matcher that does not normalise references or map RMN notices finds many false "missing" claims. This is Layer 1 mess.
  - The 30 June rev1 run was received later (9 Oct) but is an older valuation. "Latest" reads naturally as the 30 September valuation, which also matches the register's valuation date.
- **Weakest ask-level readings, not fatal:**
  - FTE by position-level `fte` rather than hours over 173.33 gives different one-decimal values (for example TFH 188.4, 186.5, 188.5). The dictionary's "hours paid" and "173.33 hours at 1.0 FTE" language, and per-diem lines carrying `fte` = 0, favour the hours reading.
  - A resident's second covered position counts as covered in the other reading. Trust Agreement 1.5, "Residents, fellows and other trainees ... are not Covered Clinicians", is a person-level exclusion and favours exclusion. Including these positions moves each entity by 0.6 to 1.2 FTE.

Gates A, B, C and E pass. No decisive fact lives outside the package: the retroactive date and no-prior-acts rule are in Agreement 2.1, 2.2 and Schedule A. The trend rate and exposure definition are in Funding Policy 3.2 to 3.4. The carrier timeline is in the premium history. No solution blocks needed regeneration.

## Files/Hygiene: PASS

- **Count and formats:** 17 files in 4 formats: 10 CSV, 4 XLSX, 2 PDF, 1 MD. One file has 224,767 rows. Loss runs come in three native layouts.
- **Realism:** the loss runs carry carrier-style totals rows, hyphen-less references and mixed date formats. The workbook metadata names plausible in-fiction authors. There are no hidden sheets and no README-style or authoring-process text. The PDFs contain no stump vocabulary.
- **Distractors:** patient_safety_events, defense_panel_invoices and the 30 June rev1 loss run are relevant to weigh and unused by the solution. None are named in a file name.
- **Provenance and timeline:** the fiction is coherent, with the extract log dated October 2026 and the adopted policy dated 22 September 2026. All data is synthetic fiction with fictional carriers. There is no public-data contamination.
- **Cross-batch check:** not performed. Reading other task folders is forbidden by the isolation rules.

## Stump power

Good. A strong model reaches an average-severity number ($2.6M or $0.64M) or ignores the retroactive-date truncation ($13M) unless it ties cost to delay. That tie is visible only in the register itself. Disclosed-harm claims are made within weeks and cost about $50k, while months-later claims cost about $5 to 9k. Claims delayed more than a year average about $450k but carry zero 2027 exposure. The asks add independent traps:
- the prior-carrier exclusion
- the CONTRACT exclusion
- the RMN and suit key mapping
- the resident additional position
- the legacy versus HCM job-code crosswalk

The main margin is comfortable, with about 11% of room to the lower rounding boundary.

## Stumping type

`mechanism: forecasting` (claims-made first-year reporting development with exposure-weighted severity), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

No reported figure is wrong. The difficulty survives clean data, because the average-severity route still files the wrong number. This passes Gate G.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **Domain:** this is actuarial work, namely a claims-made contribution with a reporting lag, trend and exposure. The swap test fails to carry over: "visits" or "megawatt-hours" would not make sense in the delay-truncated severity step.
- **Layer 1:** changing job-code sets at July 2020; legacy payroll versus HCM; a claim and its suit under prior_claim_no; carrier references in two formats; a revised, older-valuation loss run; and `coverage_line` carrying the current programme code for earlier incidents.
- **Layer 2:** estimating the cost of claims made inside a truncated window, where severity depends on delay.
- **Easy route:** a capable analyst who cleaned everything and read every rule would file expected count times average claim cost, giving about $2.6M, or $0.64M if the average is limited to claims made within a year.

## Fix

None. The fix location is `none`.
