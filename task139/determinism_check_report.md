# Determinism check, task139 (architecture 3)

Pass 1, 2026-10-27, on target.zip f287a7bd (the pack before the stage 4 realism pass; that pass moved no figure: the VINs and dealer states are rebuilt from the same random draws, the surcharge base and the dollar rounding are pinned in words). One isolated judge thread (general-purpose, sonnet, medium) read only the brief and a fresh unzip of target.zip.

**Verdict: DETERMINISTIC. Disposition: APPROVE.** Gate G: mechanism forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical.

Optional pins the judge listed, both applied: the 40 per cent surcharge is filed on the price with any channel loading (rate manual 3; base times 1.6 gives 56.3, also 55 and the same call), and the prompt asks for each dollar total rounded once (per-contract rounding moved ask A's refunds by up to 9 dollars).

## The judge's verdict, verbatim

# Verdict, task139 (pass 1)

**Cross-batch check:** no earlier packages are readable from the allowed scope, so no near-duplicate could be tested. None observed.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed and no model rerun. Two optional wording pins are listed under Fix.
- **Why:** I rebuilt the whole chain from target/ and every committed answer reproduced exactly. The main call is forced. Read literally, rate manual 5 gives a current-price forecast of 75.0%, which is over 70%. At 1.4 times the price it is 53.6%, which is at or under 70%. The manual's rule therefore selects "renew with the maximum surcharge". The answer is robust to banding, to the surcharge arithmetic and to the treatment of the last reading.

## Evidence (all recomputed from target/)

**Join keys**
- contract_number_crosswalk_2024.csv maps all 9,166 old DP- numbers to register CV numbers.
- Every claim line and every non-feed odometer reference maps to the register.
- The Fareline feed maps by VIN to a unique Fareline contract (no Fareline VIN is resold).
- Odometer readings are monotone per contract. No reading falls before the sale date or below the odometer at sale.
- Readings stop at the cover end (closing reading), so the miles under cover are unambiguous: no contract's last reading is past sale odometer + 75,000.

**Claims cost per 1,000 miles by 10,000-mile odometer band (net of deductible and reversals, goodwill excluded)**

| Band start (miles) | Cost per 1,000 miles (USD) |
|---|---|
| 10,000 | 3.38 |
| 20,000 | 4.44 |
| 30,000 | 3.82 |
| 40,000 | 4.24 |
| 50,000 | 4.09 |
| 60,000 | 4.15 |
| 70,000 | 5.02 |
| 80,000 | 7.62 |
| 90,000 | 13.55 |
| 100,000 | 21.99 |
| 110,000 | 34.59 |
| 120,000 | 52.73 |

- Pooled below 70,000 miles the cost is about 4.1, flat, then climbing. This reproduces critical component 1 and the pptx chart.
- Fareline's own cost per mile by band agrees with the book (4.3, 4.0, 5.5, 7.1, 13.9, 20.8, 38.4).

**Forecast for the 6,000 contracts sold in 2026**
- Average price is 4,788.57 and mean claims cost over cover is USD 3,594 (all 6,000 contracts: 3,591). Cover is the earlier of 75,000 miles and 60 months at the contract's own annual mileage.
- Loss ratio at current price: 75.04% (all 6,000: 74.99%). At 1.4 times the price: 53.6%.
- Banding sensitivity: 5,000-mile bands give 75.15%, 10,000 gives 75.00%, 20,000 gives 74.5%. Without annual-mileage capping it is the same, because the 75,000-mile limit always binds (minimum annual mileage is 15,850).
- 5,933 contracts have a feed reading after sale. This reproduces critical component 3. Mean annual mileage is 45,707 and mean time to reach 75,000 miles is 21.0 months. Median odometer at sale is 74,927. All reproduce.
- Cost per claim within an odometer band shows no upward trend across 2019 to 2026, so "current repair costs, no trend" is not a fork.

**Competing answers (stress-tested)**
- Lapse: no. Surcharged forecast 53.6% is at or under 70%.
- Renew at current price: this is the easy route. Fareline's own claims to date are USD 700,171 against USD 28.73M of price (2.4%). Applying the whole-book average cost per mile to 75,000 miles gives 21.6%, and Fareline's own average cost per mile gives 16.1%. All sit far under 70% and would file "renew at current rates". Only the odometer-banded cost curve gives 75%.
- Surcharge arithmetic: price times 1.4 gives 53.6%. Base times (1.2 + 0.4) instead gives 56.3%. Both round to 55% and both are under 70%, so the call is unchanged. Nearest 5%: 75.0 gives 75 and 53.6 gives 55.
- Rounding closeness: 53.1 to 53.7% (the 74.4 to 75.2% range divided by 1.4) stays above the 52.5% boundary. A solver who rounds to 50 would need a current forecast below 73.5%, which no valid method gives.

**Cancellations (supplementary xlsx 1)**
- Method: first request per contract. Dealer and customer requests join by contract number. A lienholder request joins by VIN plus lienholder name, which gives exactly one contract for each of 697 requests. Refund by contract terms 5.
- Counts by quarter: 191, 202, 193.
- Refunds (USD): Q1 225,090.62 (lienholders 120,673.59); Q2 222,804.62 (136,837.33); Q3 264,815.97 (145,907.47). All reproduce.
- Same-day requests (8 contracts, 3 in 2026) change no refund, because the day share dominates the mile share.
- No request falls exactly on day 30; day-31 sensitivity moves only one 2026Q1 contract by USD 77, and 23 requests fall within 30 days with no claim.
- Minor fork: rounding each contract first gives USD 225,100 / 222,801 / 264,817, against 225,091 / 222,805 / 264,816 when the sum is rounded once. The prompt says "every dollar figure to the nearest dollar", so rounding the reported total is the literal reading.

**Dealer premium (supplementary xlsx 2)**
- Parsing: Trinity (USD), Brazos (cents, Period text), and independents (VIN plus day-first sale date). Independents map to contracts by VIN plus sale date with 0 unmatched. Bordereau amounts equal the register price on every row.
- Returns: all 53 ACH returns match exactly one dealer-month payment on dealer name (via dealer_directory), settlement month equal to bordereau month, and amount equal to the payment total. 3 of the 53 fall in dealer-months with two payments and need the payment-level total, which is unambiguous. 227 returned contract rows are re-sent later and count as received.
- Received and outstanding (USD): 2025Q1 1,252,537 / 28,963; 2025Q2 1,322,803 / 4,174; 2025Q3 1,341,549 / 25,274; 2025Q4 1,276,743 / 41,758. All reproduce.

**Decisive facts are all in shipped files:** rate manual 2, 3, 5 and 6; contract terms 2, 5 and 6; agreement summary 2 and 4; and the register, claims, odometer, cancellation, bordereau and ACH files. The 70% threshold and the 40% surcharge cap are both in the rate manual. No external fact is needed.

## Files/Hygiene: PASS
- 13 files. Formats: csv (9), pdf (4), xlsx (1), so 3 formats.
- Odometer file has 612,712 rows (over the 25,000 floor).
- Distractors: Tarrant Mutual policy summary, repair_facility_directory.csv, and the ACH report to a degree. None is used by the main call.
- No authoring or benchmark disclosures found in the PDFs or CSV headers.
- Temporal: claims paid_date runs to 2026-10-17 against records to 30 September 2026. Repair orders end 2026-09-29, so every claim is in. Minor oddities: dealer_directory lists "Fort Worth, OK" and "Oklahoma City, TX", and VINs have invalid check digits. These are non-decisive realism nits and not exclusion-level.

## Stump power (Gate F)
- The trap is immaturity and censoring. Fareline's own claims to date are 2.4% of price. A strong analyst who cleans the data and reads every rule correctly can still file about 2% to 22% and renew at current rates.
- Doing it right needs a whole-book cost-per-mile-by-odometer curve, exposure built from the readings, and a projection through bands the channel has not yet reached.
- The asks add heavy multi-row work: the lienholder join on a resold VIN, the refund formula, and three bordereau layouts with ACH matching.
- Margin is clean: 75.0 against 70 on a method-robust figure.

## Stumping type (Gate G)
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported numbers are all fine. The difficulty is a forward projection of lifetime cost that the channel's immature trailing experience does not pin, fixed by exposure-based development from the whole book. On clean data it would still stump.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: this is vehicle-service-contract pricing and actuarial loss-ratio forecasting from claim cost against exposure miles. The swap test fails to port: the odometer-band cost curve and per-contract cover limits are field-native.
- Layer 1: contract renumbering crosswalk, three bordereau layouts and units, returned ACH payments, resold VINs.
- Layer 2: exposure-based cost development with censoring, applied to the cover path through unobserved odometers.
- Easy route: the channel's own claims over premium or its own cost per mile gives 2% to 22%, which files "renew at current rates". The correct answer is 75%, so the surcharge.

## Fix: none required (optional)
- Optional (prompt): add a "round the total once" wording for dollar figures to remove the per-contract rounding fork.
- Optional (prompt or files): state whether the 40% surcharge applies to the loaded price. Both readings round to 55% and lead to the same election, so this is not a determinism hole.
