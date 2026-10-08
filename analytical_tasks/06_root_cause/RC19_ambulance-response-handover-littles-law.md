# RC19 — Ambulance response times up 60%: more calls, sicker patients, or ambulances stuck outside hospitals?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Capacity consumed by a slow downstream dependency (thread pools exhausted by a slow database, delivery vans idling at blocked docks, support agents waiting on engineering) |
| Domain | Emergency medical services |
| Task shape | 18 · Hypotheses versus evidence (call demand, acuity and conveyance mix, hospital handover delays → unit-hours consumed and panel evidence; the lever the region acts on) |
| Core method | Little's law accounting: ambulance unit-hours consumed = Σ incidents by outcome × reference job time + handover excess hours; decompose the year-over-year increase in unit-hours into volume, outcome mix and handover excess; corroborate with a services × months panel of category 2 mean response on unit-hours consumed per staffed-hour proxy and handover excess, with service fixed effects |
| Analytical stump | Analysts compare incidents with response times and conclude that a 4% rise in incidents cannot explain a 60% rise in waits, so they blame staffing or acuity. Waiting outside an ED holds a crewed ambulance just like a job does; by Little's law, the hours lost at handover are capacity removed from the street. Counting them as unit-hours shows where capacity went, and the per-incident view never sees it |
| Primary sources | NHS England Ambulance Quality Indicators (AmbSYS) — monthly incidents by category and outcome, response-time means and 90th centiles; NHS England urgent and emergency care situation reports — ambulance arrivals and handover delays by acute trust |

## 1. The real-world situation

A regional ambulance service's mean category 2 response time rose from 32 to 51 minutes year over year in winter. Incidents rose about 4%. The
service's board asked for more crews; acute hospitals argued that patient acuity had risen; the service argued that ambulances were queuing
outside EDs for hours. The region must choose where to put a limited winter fund: extra crews, demand management, or handover improvement at the
worst hospitals.

## 2. The decision (one deterministic recommendation)

**The lever the region funds — the component with the largest increase in ambulance unit-hours consumed (volume, outcome mix, or handover excess),
provided the panel evidence for that component is significant — with the unit-hour bridge.**

Rules (regional memo):

* Data: AmbSYS monthly indicators for all English ambulance services, for the reference and current winters (December–February); handover delay
  counts by acute trust from the situation reports for the same weeks, mapped to ambulance services by the memo's trust → service table.
* Outcomes: hear-and-treat, see-and-treat, see-and-convey to ED, see-and-convey elsewhere (AmbSYS outcome counts).
* Reference job times per outcome (memo table, from the reference winter): 0, 75, 115 and 105 minutes.
* Handover excess hours = (delays 30–60 min × 30 + delays > 60 min × the memo's reference excess per delay) ÷ 60.
* Unit-hours U = Σ outcomes × job time ÷ 60 + handover excess hours.
* Bridge (current − reference, for the region's service): volume = (incidents_C − incidents_R) × reference hours per incident (excluding handover
  excess); mix = Σ (share_C − share_R) × incidents_C × job time ÷ 60; handover = excess_C − excess_R.
* Panel evidence: services × months, OLS of C2 mean response (minutes) on log(incidents) (volume), job hours per incident Σ share × job time ÷ 60
  (mix) and handover excess hours per 1,000 incidents (handover), with service and calendar-month fixed effects; a component's evidence is
  significant if its coefficient is positive with p < 0.05.
* Fund the largest bridge component whose evidence is significant.

## 3. Why capable analysts get it wrong

* Incident growth and response times are the published headline pair.
* Capacity lost at hospitals is invisible in ambulance-service statistics unless joined from acute-trust reports.
* Acuity is plausible and hard to refute without outcome mix data.
* Response time is the symptom of utilisation, not a per-incident property.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ambsys_<years>.csv` | CSV | ~15k (service × month × indicator) | NHS England Ambulance Quality Indicators | Open Government Licence v3.0 | Incidents, outcomes, response times |
| 2 | `uec_sitrep_handovers_<winters>.xlsx` | XLSX | ~30k (trust × day) | NHS England UEC daily situation reports | OGL v3.0 | Ambulance arrivals and handover delays |
| 3 | `trust_to_ambulance_service.csv` | CSV | ~130 | Task author (from NHS ODS geography) | OGL-derived | Trust → service mapping |
| 4 | `ambsys_specification.pdf` | PDF | — | NHS England | OGL v3.0 | Indicator definitions |
| 5 | `regional_memo.pdf` | PDF | — | Task author | — | Rules in §2, reference job times |
| 6 | `board_crews_request.xlsx` | XLSX | — | Task author | — | Staffing request |
| 7 | `littles_law_reference.pdf` | PDF | — | Cite (Little 1961) | Cite | Method |

## 5. Deterministic solution path

1. Extract winter AmbSYS indicators; compute outcome shares and response times.
2. Aggregate handover delays to services and months; compute excess hours.
3. Unit-hours and the three-component bridge.
4. Panel regression; significance of each component.
5. Choose the lever; contrast with the crews request.

## 6. Wrong paths (method errors, not misreadings)

**A — incidents vs response times only.** Concludes demand cannot explain the rise and funds crews by default.

**B — per-incident handover averages.** Averages across all incidents dilute handover hours that fall on conveyed patients only.

**C — no fixed effects in the panel.** Large, busy services differ structurally; the coefficients reflect geography.

**D — whole-year comparison.** Handover delays concentrate in winter; annual totals dilute the effect.

## 7. Why the stump is analytical, not semantic

Every quantity is computed from published counts and memo constants. The trap is a capacity-accounting one: hours lost downstream are capacity,
not delay statistics.

## 8. Draft task prompt (prose)

> Category 2 response times are up 60% and the board wants more crews. Use the regional memo's unit-hour accounting and panel check to tell me where
> ambulance capacity went and which lever we should fund. Provide `unit_hour_bridge.csv` (component: unit-hours, share), `capacity_bridge.png`, and a
> one-page `winter_fund_decision.pdf`.

## 9. Deliverables

* `unit_hour_bridge.csv` — volume, mix and handover components, with reference and current totals.
* `capacity_bridge.png` — waterfall of unit-hours, with the C2 response time trend inset.
* `winter_fund_decision.pdf` — decision, panel coefficients, and why the crews request is or is not the best lever.

## 10. Where 25+ rubric criteria come from

* Indicator extraction (incidents, outcomes, C2 mean) for both winters: 6.
* Handover aggregation and excess hours: 4.
* Unit-hours and three components, with closure: 5.
* Panel coefficients and significance: 6.
* Decision and contrast: 3.
* Chart elements: 2+.

## 11. Golden-output checklist

* December–February windows; trust → service mapping applied.
* Excess-hour formula with the memo constants.
* Bridge components exactly as defined; closure check.
* Fixed-effects panel; significance rule.

## 12. Build notes (scope tuning)

* Choose a service and winters where handover delays rose sharply; confirm that the handover component exceeds volume and mix combined, and that
  its panel coefficient is significant.
