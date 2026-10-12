# solver round: round 1 (architecture 2)

**Proxy score 97.9 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 55.9 of 58). Main call LANDED. 4 of 4 ask items cracked (80 per cent of tokens). Ask share kept 96%. Gate: LANDED.

## Main call

golden: Hinckley, Daventry, Bellshill, Magor, Warrington and Avonmouth meet Thornacre's peak stock-record standard and run replenishment unattended through the freeze; Thurrock and Doncaster stay on supervised replenishment.

solver: Six of the eight centres qualify under SCS-07's 97.0% line and can run unattended through the freeze: Avonmouth 98%, Bellshill 98%, Daventry 98%, Hinckley 99%, Magor 99% and Warrington 98%; Doncaster (96%) and Thurrock (96%) fall short and must be supervised for the whole freeze (7 Dec 2026 to 4 Jan 2027).

tokens matched 8 of 9 (Hinckley, Daventry, Bellshill, Magor, Warrington, Avonmouth, Thornacre's, Thurrock, Doncaster)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| freeze_gate_2026.html | 1 | 18 | 21 | 86% |
| freeze_gate_2026.html | 2 | 18 | 18 | 100% |
| freeze_gate_2026.html | 3 | 17 | 17 | 100% |
| freeze_gate_2026.html | 4 | 8 | 8 | 100% |

## Solver's path

1. Read SCS-07 v3 (in scope = pick face slotted to a Thornacre line, not on hold or recall; correct = system qty equals the count's confirmed qty; measured at 06:00 7 Dec 2026; estimate = what a full count at that time would bear out; line 97.0%) and CP-THN-04 (classes A 28, B 56, C 91 days; CYC routine counts; exception codes SHP, NEG, EMP, OVR; confirmed = recount if any, else first count)
2. In-scope faces: wms_location_master_THN_eff version in force on 2026-12-07, location_type PICK, client THN, line_no present, status ACTIVE: 26,188 faces (AVO 3,054, BEL 2,835, DAV 3,935, DON 3,286, HNK 3,495, MAG 2,605, THU 3,267, WAR 3,711); excludes HOLD, RECALL, EMPTY and the HPF and MRV faces at HNK and THU
3. Count history (107,072 rows): ok = (recount if present else first count) == system_qty; this fixes 53 rows where the confirmed qty was wrongly posted although the first count agreed; exception counts are biased (all-reason accuracy 79-94%); used only the 93,136 CYC counts
4. Routine-count accuracy falls with days since the face's previous count (class A about 98% at 0-7 days to about 88% at 28 days); fitted an exponential error rate per site and class to CYC counts using that age
5. Applied each site and class rate to every in-scope face's age at 06:00 7 Dec, taken from its last count of any reason, and averaged per site: AVO 97.95, BEL 98.03, DAV 98.18, DON 96.03, HNK 98.83, MAG 99.12, THU 95.89, WAR 97.90; a linear error model gives the same within 0.1; DON and THU are below 97.0
6. Stock value: WMS_stock_by_location PICK rows joined to in-scope faces; location qty taken once per location because the batch register shows date-coded rows repeat the location total on each batch row (summing rows overstates by about 9%); EA qty divided by the line master case size valid on 7 Dec; cost = THN_cost_price_list_20261128 overwritten by THN_cost_changes_P10 effective 2026-12-06; per site AVO 1,001,000 to MAG 877,018; total £8.68m
7. Forecast: THN_store_replen_forecast_run_20261123 trading dates 2026-12-07 to 2027-01-03; category table gives supply chain, and EA categories are divided by units_per_case; depot from THN_store_servicing_map valid on each trading date (PZ26-04 re-zoning moves 5,684 rows); 492 store-days CLOSED on the trading calendar dropped (41 stores on 26 Dec added 01/12); depot mapped to site via the centre register: HNK 1,119,583, THU 923,111, DAV 666,008, BEL 450,814, WAR 435,500, AVO 398,597, DON 362,493, MAG 203,289

confidence: High on stock values, forecast cases and the six/two verdict under the age-based reading; medium on whether the reviewer expects that reading rather than a cycle-age class-weighted CYC rate, which would pass only HNK (97.7) and MAG (98.4).

notes: SCS-07 does not say how to model accuracy between counts; I read 4.5 as the expected accuracy at each face's actual age on 7 Dec, fitted from routine counts. Forecast cases rest on the category-level units_per_case for singles categories, since the forecast has no line detail.

### freeze_gate_2026.html (solver's answers)
- share of correct records per centre vs the 97.0% line, qualifies or not: Line 97.0%. Avonmouth (AVO) 98% qualifies; Bellshill (BEL) 98% qualifies; Daventry (DAV) 98% qualifies; Doncaster (DON) 96% does not qualify; Hinckley (HNK) 99% qualifies; Magor (MAG) 99% qualifies; Thurrock (THU) 96% does not qualify; Warrington (WAR) 98% qualifies (unrounded 97.95, 98.03, 98.18, 96.03, 98.83, 99.12, 95.89, 97.90)
- Thornacre stock value on the in-scope faces per centre, to nearest £1,000: AVO £1,001,000; BEL £939,000; DAV £1,292,000; DON £1,086,000; HNK £1,174,000; MAG £877,000; THU £1,068,000; WAR £1,241,000 (total about £8,678,000)
- cases the centre's stores are forecast to draw over the freeze, to nearest hundred: HNK 1,119,600 cases; THU 923,100; DAV 666,000; BEL 450,800; WAR 435,500; AVO 398,600; DON 362,500; MAG 203,300
- bar chart of forecast cases, largest first, labelled, title naming the top centre: Bars in order Hinckley 1,119,600; Thurrock 923,100; Daventry 666,000; Bellshill 450,800; Warrington 435,500; Avonmouth 398,600; Doncaster 362,500; Magor 203,300; title names Hinckley as the centre with the most forecast freeze cases (1,119,600)
