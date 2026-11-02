# Verdict (task149)

**Verdict:** DETERMINISTIC (main call and chart figures reproduce; one supplementary input, the PORTAL weight unit, is not stated in any shipped document, see Evidence and Fix).

**Disposition:** FIX_NOW. Add one unit line for WEIGHT_SOURCE PORTAL (kilograms) to export_notes.txt or the item-master notes. This is a pin on supplementary 3 only. The forecast, the days table and the chart data are untouched, so prior runs on the main call stay valid. Reruns are needed only for any run scored on supplementary 3.

**Why:** The literal reading is an expected-value forecast of FY2027 recordable cases on the plan's volumes and hours. Rebuilding cases, hours, engineered standard hours and pace from the shipped files, then fitting recordable cases on log pace with a baseline per DC and a log-hours offset, gives 1,001.8, which is 1,000 to the nearest hundred. Every other construction I ran lands between 808 and 1,002, and the pace model is the one the data pick out of sample, so the call is forced and sits mid-bin (950 to 1,049). The weak point is that the prompt does not file the selection criterion, so a solver who files the plain rate on planned hours (about 800) has a licensed-looking alternative. The back-test settles it on the data, which makes it a Layer 2 stump and not a fork.

## Evidence (recomputed from target/ only)

| Value | Golden | My recompute | Source |
|---|---|---|---|
| Recordable cases, 20 DCs, FY2021 to FY2025 | 609, 623, 637, 588, 661 | 609, 623, 637, 588, 661 | legacy CSV + platform JSON |
| FY2026 to 11/01 (for the fit) | not stated | 557 (10,909 across 60 DCs to wk 44) | same |
| Pace, plan vs latest 52 weeks | about 9% | 1.0294 / 0.9458 = +8.8% | WFM, WMS, IE, plan |
| Pace response | 2.7 (SE 0.2) | 2.73 (SE 0.20; 0.17 clustered) | Poisson fit, DC fixed effects |
| Forecast | 1,001.8 | 1,001.8 | plan v3 |
| Plain rate per hour on plan hours | about 800 | 817 | latest 12 months |
| Back-test, FY2025 and 2026 to date, mean DC error | 11 / 21 / 15 | 11.1 / 20.6 / 16.3 | pace, FY2024 rate, cases per direct hour |
| Supp 1: days carried to 10/31 | 20 DC values | 20 of 20 exact | RTW log + platform |
| Supp 2: heavy picks | 20 DC values | 20 of 20 exact | picks + item history |

How each reproduced:
- **Case counts.** A case counts if it is recordable and not removed or not work-related. A case migrated at go-live (113 of them) is counted once, through the platform's legacy reference. Platform UTC times become local by state, which I checked against all 113 migrated cases (0 mismatches against the legacy local time). Fiscal weeks run from the Sunday after the last December Saturday. Illness cases are included, as EHS-RK-01 section 3.4 says. If the removed cases were kept, the counts would be 621, 627, 640, 597, 671.
- **Hours and standard hours.** Hours are WFM regular + overtime + agency hours across all eight departments. Rockford 311 and 318 are merged. Pre-FY2023 week 27 category codes are mapped (DRYG to AMB, PERI to CHL, FROZ to FRZ, BULK to HVB). Lebanon's site factor changes on 2024-06-30. Pace is standard hours over direct hours.
- **Robustness of the pace response.** Adding period-of-year effects, year effects, or both leaves the coefficient between 2.72 and 2.80. Throughput (cases shipped per hour) takes no weight beside pace (coefficient -0.26, SE 0.30), and its own model fits worse (deviance 4,789 against 4,728). Fitting only the 20 program DCs gives a coefficient of 2.51 and a forecast of 982. Using direct hours as the offset gives 1,001.8.
- **Alternatives.** Cases-per-hour-shipped model 841. Rate per case shipped about 833. Rate per standard hour about 879. Rate per direct hour about 808. All of these ignore the +9% pace and land on 800 or 900, so none matches 1,000. The back-test (mean DC error 11% against 14 to 21%) separates them on the data.
- **Supp 1, days.** Platform `days_away` + `days_job_transfer_restriction` are stale for open cases: summed, they give 8,871 against 10,146. They have to be rebuilt from the RTW log under EHS-RK-01 section 9. That means counting from the day after injury to 10/31, ending at FULL DUTY or SEPARATED, and capping at 180. A "TRANSFER OUT" row opens a second RTW file, which has a blank EHS_CASE_NO and starts the same day for the same associate. The two files must be chained, or the total is 9,236 against 10,146. Three cases injured on 10/31 (Sun Prairie, Memphis, West Chester) carry 0 days to 10/31, although the platform stores 1. Golden reproduces on all 20 DCs.
- **Supp 2, heavy picks.** Match on the item version in force in the fiscal period, because SKUs are reused (300 version-2 rows, all starting on period boundaries). WEIGHT_SOURCE = PORTAL weights must be converted from kilograms (factor 2.2, 2.20462 and 2.205 all give the golden exactly). Taken as recorded, the total is off by 2.87M cases, and the current master alone is off by 2.64M. I found no shipped statement of the PORTAL unit. The evidence is only density: PORTAL weight per cubic foot averages 8.1 against 18.0 for BUYER and CUBISCAN, a ratio of 0.447, which is 1/2.2. A strong analyst can see this, but no document says it.
- **Forks examined.** Window (12/28/2025 to 10/31/2026) and the strict "more than 50" test are filed in the prompt. Rounding is filed. FY2027 is 52 weeks (Periods sheet), so no length fork. No competing main answer survives once the back-test is applied. The margin to the nearest-hundred boundary is 48 cases in either direction against a model SE of 26, and every credible model-based construction (982 to 1,028) rounds to 1,000.

## Files/Hygiene
PASS. 18 files in 6 formats (csv, json, xlsx, pdf, txt, parquet). Large files: WFM 146,400 rows, picks 1.05 million rows, legacy cases 22,759 rows. Plausible distractors that the solution does not use: BBS observations, WC loss run, ITA Form 300A, RTW for the main call. Reads as operational exports (stale counts, SKU reuse, renumbered Rockford, a UTC feed). No authoring or benchmark disclosure found in the files I read. Minor flags: (a) the Lindqvist draft is dated 11/16/2026 but folder_index records it pulled 2026-11-02, a mild temporal oddity; (b) the PORTAL unit is undocumented (above). No exclusion-level finding. The cross-batch check was not run because no other task folder was readable.

## Stump power
Moderate to good. The easy route is the plain rate on planned hours (817, filed as 800), or a rate per case shipped or per standard hour (800 to 900). A strong model that reads the plan's +20% hours and the IE standards may find the pace link, but it has to build the standard-hour panel (legacy/platform merge, category recode, site factors, Rockford) and validate out of sample before trusting a 2.7 elasticity. Supplementary asks add independent stump devices: chaining the TRANSFER OUT RTW files, the 10/31 boundary, SKU reuse by period, and the PORTAL kilogram unit.

## Stumping type
`mechanism: method_or_model_selection (with forecasting)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
All reported figures are honest. The difficulty is choosing the exposure-and-pace model over the rate-per-hour models, judged on out-of-sample error, then carrying the plan's pace through it. Run on perfectly clean data it would still stump. Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **Domain.** The deciding quantity is an occupational-safety exposure and intensity model: a recordable-case count by Poisson regression with hours offset and work pace against engineered standards, validated by back-test. Swapping the nouns to another field breaks it.
- **Layer 1.** Legacy-to-platform migration, UTC against local time, Rockford renumbering, category recode, 53-week FY2022, SKU reuse, stale days.
- **Layer 2.** Rate versus pace-driven risk, validated out of sample.
- **Easy route.** A strong analyst who cleaned everything correctly would carry the latest twelve months' rate per hour onto the plan hours and file 800 (or 800 to 900 on a per-case or per-standard-hour basis) instead of 1,000.

## Fix
`input_files` (supp 3 only): add a single line stating the unit of PORTAL weights (kilograms) to export_notes.txt or an item-master note, so the ask rests on a stated fact and not on a density inference. The prompt, the main call, the golden figures and the other asks need no change. Optional, not required: file the back-test as the selection criterion for the main call. This would be an estimand filing, not a method filing, but it would make the stump easier. I do not recommend it since the data already separate the candidates.
