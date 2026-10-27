# Judge verdict, task157 (winter guarantee fund, Larch Rides)

Isolation kept: only the judge directory and target/ were read. The cross-batch check against other tasks was not run, because other task folders are forbidden here.

**Verdict:** DETERMINISTIC. One residual Gate C caution on the rounding edge of the driver count (see Evidence).

**Disposition:** APPROVE. No solver-visible change is needed and no solution block is wrong in a way that matters. Optional lever: if the author wants the driver count safer on the lower rounding line, file the population of "winter drivers". That would change what solvers see and needs a rerun, so it is not required.

**Why:** Every committed answer reproduces from the shipped files. The payout tables are forced by winter_guarantee_payout_notes.docx, the pipeline table by onboarding_pipeline_counts.docx, and the fund by the 30 December email together with the 2027 terms PDF. The fund of $1,650,000 and the 4,700 drivers come out of a seasonal-cohort forecast. The reasonable variants I ran, which vary the ratio years, the price bands, paid versus main-only versus paid-less-recovered, and the winter-pool definition with a May-to-October gap, land at 4,658 to 4,728. All of these round to 4,700 and $1,650,000. The risk is that a few weaker but arguable routes round one step lower (4,600 and $1,600,000). No gate fails.

## Evidence (recomputed from the bundle)

**Payout tables**

| Item | Golden | Recomputed | Source |
|---|---|---|---|
| 2025 main run | $900,900 | 2,574 x 350 = $900,900 (xlsx cents / 100) | winter_guarantee_2025_payout_run.xlsx |
| 2026 main run | $1,053,500 | 3,010 x 350 = $1,053,500 | winter_guarantee_2026_payout_run.csv |
| Later runs, 2025 | $5,950 | 17 late_credit lines, $5,950 | adjustments csv |
| Later runs, 2026 | $7,350 | 21 late_credit lines, $7,350 | adjustments csv |
| Never reached a driver, 2025 | $12,950 | Last event is "returned" (resent-and-settled paid out ignored, 7 returned twice counted): 37 payouts, $12,950 | payout_events csv |
| Never reached a driver, 2026 | $16,100 | 46 payouts, $16,100 | payout_events csv |
| Recovered, 2025 | $4,550 | 12 lines in 2025 batches ($4,200) plus 1 line in a WG2026 batch that reverses a 2025 payout ($350) | adjustments csv, notes docx |
| Recovered, 2026 | $6,300 | 18 lines | adjustments csv |
| Net cost, 2025 | $889,350 | 900,900 + 5,950 - 12,950 - 4,550 | |
| Net cost, 2026 | $1,038,450 | 1,053,500 + 7,350 - 16,100 - 6,300 | |
| Drivers paid, 2025 | 2,541 | 2,541 payouts kept, 2,541 people after merged_into | accounts csv |
| Drivers paid, 2026 | 2,966 | 2,967 payouts kept, 2,966 people (one person holds two kept payouts) | accounts csv |

- Returned payouts: the 187 "returned" events equal the 187 GUARANTEE rows in the ACH report.
- Recoveries and final returns overlap on no payout.
- A reader who ignored merged_into would file 2,967 for 2026.

**Pipeline**

Method: persons are candidate_id, month is the Central month of the first vendor order, "approved" includes approval_lapsed, and a first trip is any trip before 4 Jan 2027 Central. This reproduces all fifteen figures exactly: June 446/313/263, July 448/322/274, August 500/350/294, September 423/311/255, October 481/338/286.

- A UTC month cut shifts several counts, for example June 443 and September 424.
- Using the application's submitted time moves 885 applications across months.
- Counting only status=approved gives September 263 and cuts the approved counts for June to September. docx plus data notes define a lapsed approval as "approved", so the literal reading is the golden. Minor residual wording risk.

**Main call**

- Dec 2026 roster excluding last winter's drivers, priced by December-trip band at the share the 2026 guarantee paid in the Dec 2025 roster: 2,688. Golden says "about 2,700".
- Last winter's drivers (Jan to Mar trip, none May to Oct), back by Nov or Dec 2026: 1,087. Reproduces.
- Winter drivers back by December 2025 paid by the 2026 guarantee: 92.8 percent. Reproduces the golden 93 percent.
- Winter drivers back in January 2026 only and paid: 82.2 percent. Reproduces the golden 82 percent.
- January to Nov/Dec returns ratio, winters 2022 to 2025 in my labelling: 1.077, 1.098, 1.093, 1.074. Pooled over 2023 to 2025: 1.086. Reproduces golden 1.086 (the golden labels the winters differently).
- Due back: 1,087 x 1.086 = 1,180.
- Total: 2,688 + 1,009 + 970 + 26 (other breaks) + about 16 (new, no trip) = 4,708 -> 4,700 drivers; 4,708 x 350 = $1.648M -> $1,650,000. Last winter's drivers contribute 1,979, matching the golden "about 2,000".
- Not reproduced exactly: the "14 of 174" new accounts. My simplest definition (opened by 4 Jan 2026, no trip through Dec 2025) gives 14 of 183. The term is worth about 16 drivers and is immaterial.
- Out-of-sample check: the same method applied to the 2026 guarantee gives about 3,085 against 3,031 payees (+1.8 percent). The share-based January return (0.312 x 1,502 away = 469 against 405 actual) overshoots by 16 percent, as the golden says. The 352 rental_partner drivers sit in the 2025 winter pool and never come back.
- The wrong routes the golden rejects each land distinctly:
  - Away pool at last January's return rate: about 4,328.
  - Whole December roster banded, no returns: about 3,661.
  - Back-by-December winter drivers priced by December band with the non-winter shares: about 4,556, which rounds to 4,600.

**Competing routes (Gate C / near-tie)**

| Variant | Total | Rounds to |
|---|---|---|
| Ratio years 2025 only, 2024 only | 4,699, 4,715 | 4,700 |
| Band sets (2 to 20 wide), paid basis | 4,697 to 4,728 | 4,700 |
| Main-run-only payees | 4,679 | 4,700 |
| Paid less recovered | 4,686 | 4,700 |
| Main-only less recovered | 4,658 | 4,700 |
| Winter pool defined with May to Oct gap, or Feb/Mar to Oct, or Jan to Apr / Jun to Oct | 4,696 to 4,716 | 4,700 |
| Generic "back after a break of k months" ratio, k = 6, 4 | 4,683, 4,661 | 4,700 |
| k = 3 | 4,617 | 4,600 / $1,600,000 |
| k = 2 | 4,527 | 4,500 |
| "Kept" basis (strips returned-and-never-resent payees, who did qualify) | 4,619 | 4,600 / $1,600,000 |
| Gap defined as Apr to Oct | about 4,080 | far off |

- The Apr-to-Oct pool excludes campaign recruits who drove in April, who are the pool being forecast. It is a pool-definition error rather than a rival method.
- The k=2 and k=3 routes carry a ratio that drifts (0.93 to 1.02), i.e. they mix in occasional drivers. The 2026 back-test cannot separate k = 2 to 6 (errors 0.7 to 1.3 percent). So the winter-pool framing is preferred on ratio stability (1.07 to 1.10) rather than on out-of-sample error.
- The fund of $1,650,000 needs only 4,643 to 4,785 drivers and is robust to the reasonable variants. The 4,700 figure needs 4,650 to 4,749. The golden's 4,708 sits 42 below the upper line, and a few reasonable-but-weaker routes sit about 50 to 90 below the lower one.
- This is a thin-and-partly-contested margin only at the lower driver-count edge. The central plausible cluster (4,658 to 4,728) is inside the window, so I do not call it fragility.

**Rate-trend variant:** a share-based January return extrapolated with its year trend (0.19, 0.27, 0.31, 0.35 ex-rental, to about 0.39) gives about 1,037 January returners against 1,180, about 4,590 in total. That is a weak four-point extrapolation. The data gives the better explanation: the conditional rate follows the November/December return share (b = r x a / (1 - a)), which the ratio method captures. I treat it as dominated, not defensible.

**Gate B:** every decisive fact is present: the terms PDF (eligibility, window, $350), the email (once-only funding, leave out returns and recoveries, $50,000 steps), the notes docx (cost definition, attribution, person definition), the pipeline docx, and the data notes (grain, months in Central time). No external dependency. Vocabulary check: "never reached", "returned", "recovered" and "later runs" all appear in the files.

**Gate E note:** the phrase "net of later runs" in the prompt could be read as subtracting later runs. winter_guarantee_payout_notes.docx pins "cost is what its runs paid, less returns and recoveries", so later runs add. Low risk.

## Files/Hygiene: PASS

- 20 files. Formats: csv (11), xlsx (2), docx (2), pdf (2), eml, md, log.
- One file of 165,826 rows (driver_activity_monthly), plus legacy 91,426 rows and events 17,074 rows.
- Layer-1 mess is present: legacy driver-number crosswalk with 38 double registrations, July 2024 split across two platforms, amounts in cents against dollars, UTC against Central time, resubmitted applications whose submit time is later than the order.
- Distractors: rider_demand_plan_q1_2027.xlsx, driver_supply_kpis_2026-11.pdf, driver_referral_bonuses_2026.csv, ach_returns csv (redundant with the events).
- Timeline is coherent: pull on 3 Jan 2027 21:40 CST; the log's 19 files plus the log itself make 20; the email is dated 30 Dec 2026.
- No benchmark or authoring disclosure found. The data-notes md reads as an analyst's field note, which is acceptable.
- Not checked: whether any file was copied from a public corpus. It reads as a synthetic company with plausible operational noise. No exclusion-level finding.

## Stump power

Plausible. A strong model that cleans the data correctly lands on one of the easy routes: the whole December roster banded (about 3,660), the away pool at last January's return rate (about 4,330), or drivers back by December priced by their December trips (about 4,560). A model that leans on the demand plan or the KPI report goes further astray. The ratio of January to November/December returns for the seasonal winter pool is not the first idea. Estimated stump power is good on the main call. The asks (person-level driver counts, cross-year recovery attribution, first-order month in Central time) are error-prone for a careless solver but resolvable from the notes.

## Stumping type

`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

The reported numbers are fine. The difficulty is a cohort-timing forecast validated against the previous winter: a seasonal pool's January return is tied to its November/December return, while a share-based rate moves with who sits in the pool. On clean data the task still stumps.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`

- Layer 1 is the legacy-to-new platform ID crosswalk, cents against dollars, UTC against Central time, the split July month, and resubmitted applications.
- Layer 2 is a driver-supply forecast of the guarantee's take-up from the seasonal return pattern of returning drivers.
- Swap test: put "visits" or "hospital" in and the task stops reading the same, because the return-pool dynamics are a supply-side cohort analysis.
- Easy route: price the away pool at last January's return rate (about 4,330 drivers, $1,500,000), or band the whole December roster (about 3,660, $1,300,000). A strong analyst with every field correctly read still files these. This is not semantics or rule application.

## Fix

none. Optional (prompt): if a safer lower edge on the driver count is wanted, file the population of "drivers who last drove in the winter" so the pool definition is not left to the solver. This changes solver-visible text and needs a rerun, so it is not recommended.
