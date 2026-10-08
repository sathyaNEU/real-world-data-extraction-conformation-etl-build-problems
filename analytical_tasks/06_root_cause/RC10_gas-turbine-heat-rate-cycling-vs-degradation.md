# RC10 — Heat rate up 3.5%: is the gas turbine degrading, or is it being cycled harder?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Efficiency KPIs that worsen when utilisation falls (data-centre PUE at low IT load, energy per token at low GPU batch occupancy, cost per unit at low factory run rates) |
| Domain | Power generation (combined-cycle fleet performance) |
| Task shape | 03 · Bridge between two totals (reference-year heat rate → current-year heat rate, bridged by start-up fuel, load profile, ambient temperature and a residual that is the only part attributable to degradation) |
| Core method | Hourly unit data: split start-up hours from steady hours; fit the reference year's steady-state heat-input curve HI(L, T) with a no-load term; evaluate it hour by hour on each year's own load and temperature to separate the load-profile (part-load) effect from the ambient effect; price the extra starts at reference start-up fuel; residual = observed change − explained change |
| Analytical stump | Heat input has a large fixed no-load term, so heat rate (HI ÷ L) is convex in load. Evaluating the curve at the average load (Jensen's inequality) makes a 5-point fall in mean load look like a 0.4% effect, when the current year's many hours at minimum load cost several times that. Excluding start-up hours, or folding them into the curve fit, hides a doubling of starts. Both errors leave a large "unexplained" residual that is then blamed on degradation |
| Primary sources | U.S. EPA Clean Air Markets Program Data (CAMPD) — hourly unit-level emissions and operating data (operating time, gross load, heat input); NOAA Integrated Surface Database hourly temperature |

## 1. The real-world situation

A combined-cycle plant's annual heat rate (fuel burned per MWh) rose 3.5% year over year. The plant engineer proposed an offline compressor wash
and a hot-gas-path borescope inspection, which needs a five-day outage. The commercial team pointed out that the plant now runs two shifts a day
(off at midday when solar floods the market, back on for the evening ramp) and sits at minimum load overnight. The general manager wants a heat-rate
bridge before approving the outage.

## 2. The decision (one deterministic recommendation)

**Whether to schedule the degradation outage (triggered only if the residual heat-rate deterioration is ≥ 1.5% of the reference heat rate), with the
four-component bridge in Btu/kWh.**

Rules (performance memo):

* Data: CAMPD hourly records for the facility's combined-cycle units (memo lists ORIS code and unit IDs), reference year R and current year C;
  facility-hour totals of gross load (MWh) and heat input (mmBtu); ambient temperature from the memo's ISD station, hourly, aligned to local standard
  time (CAMPD hours are local standard time).
* Operating hour: operating time > 0. A start is an operating hour preceded by ≥ 1 non-operating hour. Start-up hours: the first 3 operating hours
  after each start, plus any hour with operating time < 1. All other operating hours are steady hours.
* Heat rate (both years) = Σ heat input ÷ Σ gross load over all operating hours, in Btu/kWh (ratio of totals).
* Reference curve, fitted by OLS on R's steady hours only: HI = β0 + β1·L + β2·L² + β3·T + β4·T·L (L in MW, T in °F).
* Start-up fuel per start s_R = (Σ start-up-hour heat input − Σ HI_ref(L, T) over the same hours) ÷ starts in R.
* Bridge from HR_R to HR_C:
  * Starts effect = s_R × (starts_C ÷ G_C − starts_R ÷ G_R), with G the total gross load in MWh, converted to Btu/kWh.
  * Load-profile effect = HR_ref(C, 59 °F) − HR_ref(R, 59 °F), where HR_ref(P, 59 °F) = Σ_P HI_ref(L_h, 59) ÷ Σ_P L_h over P's operating hours.
  * Ambient effect = [HR_ref(C, T_h) − HR_ref(C, 59 °F)] − [HR_ref(R, T_h) − HR_ref(R, 59 °F)], each evaluated hour by hour.
  * Residual (degradation) = HR_C − HR_R − the three effects above.
* Outage if residual ÷ HR_R ≥ 1.5%.

## 3. Why capable analysts get it wrong

* A 3.5% heat-rate rise reads as a physical deterioration story; wash and inspection are the reflex.
* The heat-rate curve is convex, so any summary evaluated at the mean load understates part-load losses.
* Start-up fuel is burned while little is generated; two-shifting doubles starts without changing annual MWh much.
* Ambient temperature and load are correlated (summer evenings are hot and fully loaded), so effects must be evaluated on paired hours, not
  on separate averages.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `campd_hourly_<facility>_<R>.csv` | CSV | ~35k (4 units × 8,760 h) | EPA CAMPD (Power Sector Emissions Data, hourly) | U.S. Government work (public domain) | Reference-year operating data |
| 2 | `campd_hourly_<facility>_<C>.csv` | CSV | ~35k | Same | Same | Current-year operating data |
| 3 | `campd_facility_attributes.json` | JSON | ~10 | EPA CAMPD facility/unit attributes API | Public domain | Unit types, capacities, prime movers |
| 4 | `isd_<station>_<R>_<C>.csv` | CSV | ~17.5k | NOAA ISD (global hourly) | NOAA open data | Hourly ambient temperature |
| 5 | `performance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `engineering_outage_request.xlsx` | XLSX | — | Task author | — | The wash/inspection proposal and its 3.5% figure |
| 7 | `asme_ptc22_heat_rate_citation.pdf` | PDF | — | ASME PTC 22 (cite) | Cite | Heat-rate and correction conventions |

## 5. Deterministic solution path

1. Aggregate units to facility-hours; join temperatures; flag operating, start and start-up hours; count starts per year.
2. Fit the reference curve on R's steady hours; report coefficients and fit; compute s_R.
3. Compute HR_R and HR_C as ratios of totals; evaluate HR_ref hour by hour for both years at 59 °F and at actual T.
4. Compute the starts, load-profile and ambient effects and the residual; check that the bridge closes exactly.
5. Apply the 1.5% trigger; contrast with the engineering request, which treats the full 3.5% as degradation.

## 6. Wrong paths (method errors, not misreadings)

**A — curve evaluated at mean load.** HR_ref(mean L) in each year. Jensen's inequality hides most of the part-load penalty; the residual stays
above 1.5% and the outage is wrongly approved.

**B — average of hourly heat rates.** An unweighted mean of HI ÷ L across hours overweights minimum-load hours. It gives a different and
non-additive "heat rate" that does not reconcile to fuel burned.

**C — start-up hours dropped from both years, or included in the curve fit.** Dropping them deletes the starts effect from the bridge. Including
them inflates β0 and moves part of the starts effect into the load curve.

**D — curve fitted on both years.** The fit absorbs any real degradation and drives the residual to about zero, so a genuine problem could never be
detected.

## 7. Why the stump is analytical, not semantic

The hour classification, curve form, reference conditions and bridge formulas are all specified. The trap is purely methodological: a convex
efficiency curve summarised at the mean, and a fixed per-start cost that is invisible in annual averages.

## 8. Draft task prompt (prose)

> Our plant's heat rate is up 3.5% and engineering wants a five-day outage for a compressor wash and inspection. Before I approve it, bridge last
> year's heat rate to this year's using the performance memo's rules and tell me how much of the rise is genuine degradation. Provide
> `heat_rate_bridge.csv` (component: Btu/kWh, % of reference), `heat_rate_waterfall.png`, and a one-page `outage_decision.pdf`.

## 9. Deliverables

* `heat_rate_bridge.csv` — reference HR, starts, load-profile, ambient, residual, current HR.
* `heat_rate_waterfall.png` — the bridge as a waterfall, with the 1.5% trigger marked on the residual bar.
* `outage_decision.pdf` — decision, the load-band histogram for both years, starts per year, and the contrast with the engineering request.

## 10. Where 25+ rubric criteria come from

* Hour classification counts (operating, steady, start-up hours; starts) for both years: 8.
* Curve coefficients and fit statistics: 6.
* HR_R, HR_C and the four components, with the closure check: 7.
* Hours by 10% load band in each year: 2 criteria (histograms).
* Decision, trigger arithmetic and engineering contrast: 3+.

## 11. Golden-output checklist

* Hours in local standard time and joined correctly to ISD (UTC) temperatures.
* Starts defined by off-to-on transitions; start-up hour window of 3 hours.
* Curve fitted on R's steady hours only, with the no-load term retained.
* Hour-by-hour evaluation at 59 °F and at actual temperature; ratio-of-totals heat rates.
* Bridge closes to HR_C exactly; residual compared with 1.5%.

## 12. Build notes (scope tuning)

* Choose a facility whose starts at least doubled between R and C (two-shift operation in a solar-heavy market such as CAISO or ERCOT) and whose
  share of hours below 60% load rose sharply. Confirm the mean-load shortcut leaves a residual ≥ 1.5% while the hour-by-hour bridge leaves one
  < 1.5%.
* CAMPD gross load for some combined-cycle configurations includes apportioned steam-turbine output; state the convention used and apply it to both
  years.
