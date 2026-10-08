# RC45 — School bus delay reports up 60%, and "heavy traffic" is the top reason: is it the city's roads, the weather, or a few contractors?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Vendor and supplier performance attribution when vendors self-report reasons (logistics carriers coding "weather" for late deliveries, outsourced support teams coding "customer unavailable"), with common shocks shared by all vendors |
| Domain | Public-sector contracting / student transportation |
| Task shape | 12 · Drill-down to one leaf (incident increase → weather, common non-weather, vendor-specific excess → the vendor that carries most of the excess → its reason-code shift) |
| Core method | Daily incident counts by vendor; weather component from a reference-year model of daily citywide incidents on snowfall and precipitation; common growth from the median vendor's growth rate; vendor-specific excess = actual change − reference × common growth; concentration of the excess; reason codes examined only within the leaf vendor as self-reported evidence |
| Analytical stump | Reason codes are chosen by the reporting contractor, and "heavy traffic" is the default; tallying reasons city-wide makes congestion the cause. Raw incident counts also scale with how many routes a vendor runs. Separating a common shock (shared by all vendors on the same days) from vendor-specific excess, and checking concentration, shows whether the problem is the city or a few contractors |
| Primary sources | NYC Open Data — Bus Breakdown and Delays (Office of Pupil Transportation); NOAA GHCN-Daily (Central Park station) |

## 1. The real-world situation

A school district's transportation office saw reported bus delays and breakdowns rise about 60% year over year. The city-wide reason tally put
"heavy traffic" first, and the transportation office proposed asking the city for bus lanes on school routes. The district's contract managers
suspected a few contractors that had taken over routes during the year. The office must decide between a city traffic request and contractor
enforcement.

## 2. The decision (one deterministic recommendation)

**The action taken — contractor enforcement against the leaf vendor (if its vendor-specific excess is ≥ 40% of the total increase) or a city traffic
request (otherwise) — with the decomposition and the leaf vendor's reason-code shift.**

Rules (contracts memo):

* Data: Bus Breakdown and Delays records with occurrence dates in the reference and current school years (school days only per the memo's calendar);
  both breakdowns and running-late reports counted as incidents; duplicate records (same bus, route and occurrence timestamp) removed.
* Vendor names normalised by the memo's mapping.
* Weather model (reference year): daily incidents = month FE + β1 × snowfall (inches) + β2 × precipitation (inches), Poisson; weather component =
  Σ over current school days of [predicted at observed weather − predicted at zero snow and precipitation] minus the same for the reference year.
* Common growth g = median across vendors with ≥ 200 reference incidents of (current ÷ reference incidents) − 1, after removing each vendor's share of
  the weather component.
* Vendor-specific excess_v = Δ_v − weather share_v − ref_v × g. Total increase = weather + common + Σ excess_v (closure).
* Leaf: vendor with the largest excess; report its reason-code shares in both years and its distinct routes reported.
* Enforcement if leaf excess ÷ total increase ≥ 40%.

## 3. Why capable analysts get it wrong

* Reason tallies look like evidence of cause.
* Common shocks (snow days, city-wide disruption) affect every vendor at once.
* Vendors running more routes report more incidents.
* Route transfers between vendors mid-year move incidents across vendors.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Bus_Breakdown_and_Delays.csv` | CSV | ~600k | NYC Open Data (Office of Pupil Transportation) | NYC Open Data terms (public) | Incident reports |
| 2 | `ghcnd_USW00094728.csv` | CSV | ~50k | NOAA GHCN-Daily (Central Park) | NOAA open data | Snowfall and precipitation |
| 3 | `school_calendar_<years>.csv` | CSV | ~400 | Task author (from the district's published calendars; cite) | Cite | School days |
| 4 | `vendor_name_mapping.csv` | CSV | ~120 | Task author | — | Normalised vendor names |
| 5 | `contracts_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `transportation_office_reason_tally.xlsx` | XLSX | — | Task author | — | The traffic explanation |

## 5. Deterministic solution path

1. Filter school days and years; deduplicate; normalise vendors.
2. Fit the weather model; weather component.
3. Common growth; vendor-specific excesses; closure.
4. Leaf vendor; reason-code shift; decision; contrast with the reason tally.

## 6. Wrong paths (method errors, not misreadings)

**A — reason-code tally.** Self-reported defaults read as cause.

**B — vendor totals compared without a common shock.** Every vendor looks worse in a snowy year.

**C — mean vendor growth.** Outlier vendors drag the common rate.

**D — no deduplication.** Re-submitted reports inflate counts.

## 7. Why the stump is analytical, not semantic

Reason codes are reported, not used to assign cause; all rules are numeric. The trap is self-reported attribution and missing common-shock controls.

## 8. Draft task prompt (prose)

> Transportation wants bus lanes because "heavy traffic" tops the delay reasons. Decompose the increase with the contracts memo's method and tell me
> whether to pursue contractor enforcement or a city traffic request. Provide `delay_decomposition.csv` (component and vendor excess),
> `vendor_excess.png`, and a one-page `bus_delay_action.pdf`.

## 9. Deliverables

* `delay_decomposition.csv` — weather, common and vendor-specific components; vendor detail.
* `vendor_excess.png` — vendor excess bars with the leaf highlighted and its reason-code shift inset.
* `bus_delay_action.pdf` — decision and why the reason tally misleads.

## 10. Where 25+ rubric criteria come from

* Filtering, deduplication and normalisation counts: 4.
* Weather model coefficients and component: 4.
* Common growth and eligible vendors: 3.
* Vendor excess for the top 5 vendors and closure: 7.
* Leaf vendor and reason-code shares: 4.
* Decision and contrast: 3.

## 11. Golden-output checklist

* School-day filter; duplicate rule; vendor mapping.
* Poisson weather model on the reference year only.
* Median common growth; closure of components.

## 12. Build notes (scope tuning)

* Choose a school-year pair with a contractor transition; confirm the leaf vendor's excess exceeds 40% while "heavy traffic" remains the top reason
  city-wide.
