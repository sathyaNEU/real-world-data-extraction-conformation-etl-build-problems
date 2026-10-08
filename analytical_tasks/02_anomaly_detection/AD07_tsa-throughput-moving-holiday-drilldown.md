# AD07 — The airport "traffic drop" that was Easter moving: aligning calendars before drilling down

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Calendar alignment in metric anomaly detection (Easter, Ramadan, Lunar New Year or shopping events moving between years in traffic, sales and app usage) |
| Domain | Aviation security operations / airport capacity planning |
| Task shape | 12 · Drill-down to one leaf (national → hub size → airport), separating calendar shift from real change |
| Core method | Holiday- and weekday-aligned year-over-year baselines (moving-holiday alignment, 364-day lag elsewhere), decomposition of each node's change into calendar effect and aligned (real) change, drill on the largest real decline |
| Analytical stump | Same-date or same-week comparisons across years with a moving holiday attribute the holiday's shift to "anomalous demand"; real change only appears after aligning both weekday and holiday position |
| Primary sources | TSA checkpoint throughput (national daily; FOIA airport/checkpoint hourly releases), FAA hub classifications |

## 1. The real-world situation

TSA's staffing analytics team runs an automated anomaly detector comparing each airport's weekly throughput with the same
ISO week a year earlier. In April 2024 it flagged a dozen airports with drops of 8–15%, and a regional director asked for
an operational review. Easter fell on 31 March 2024 but on 9 April 2023; the comparison week in 2023 contained Easter
travel, 2024's did not.

## 2. The decision (one deterministic recommendation)

**Which airport, if any, shows a real throughput decline in ISO week 15 of 2024 after calendar alignment — and which
operations team owns the follow-up?** (If no airport's aligned decline exceeds 5%, the answer is "no anomaly".)

Rules (analytics memo):

* Throughput = passengers screened per day (sum of checkpoints and hours) for each airport in the FOIA files; national
  totals from the daily national series.
* Aligned baseline for a 2024 date d: if d is within 14 days of Easter 2024, use 2023's date at the same offset from Easter
  2023; otherwise use d − 364 days (same weekday).
* For any node (national, hub-size group, airport): naive change = actual week − same ISO week 2023; calendar effect =
  aligned baseline − same ISO week 2023; real change = actual − aligned baseline.
* Drill: national → FAA hub-size group (large/medium/small) → airport, each time following the child with the largest
  negative real change in passengers; report the leaf if its real change < −5% of its aligned baseline.
* Owner: the airport's TSA Federal Security Director operations team (lookup in folder).

## 3. Why capable analysts get it wrong

* Same-week-last-year comparisons are standard in dashboards and work for 49 weeks a year.
* Moving holidays shift a peak by one or more weeks, creating paired "anomalies" (a spike one week, a drop the next).
* Weekday mix also shifts when comparing dates rather than weekdays (364-day lag preserves weekday).
* Drilling into raw percentage drops follows the airports with the biggest holiday traffic, not real problems.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–8 | `TSA_throughput_FOIA_2023-03-26_2023-05-06.pdf`, … (weekly releases covering March–May 2023 and 2024) | PDF | ~100k+ rows each when parsed | TSA FOIA Electronic Reading Room | U.S. Gov public domain | Hourly throughput by airport/checkpoint |
| 9 | `tsa_throughput_parsed_2023_2024.parquet` | Parquet | ~2–4M | Derived from 1–8 | Public domain | Parsed table |
| 10 | `tsa_national_daily_throughput.csv` | CSV | ~2k | tsa.gov passenger volumes | Public domain | National series |
| 11 | `faa_cy2023_enplanements_hub_types.xlsx` | XLSX | ~500 | FAA Passenger Boarding Data | Public domain | Hub-size groups |
| 12 | `easter_dates.json` | JSON | 2 | Public calendar | Public | Alignment anchors |
| 13 | `fsd_lookup.csv` | CSV | ~450 | TSA public directory (task-prepared) | Public | Owner mapping |
| 14 | `analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 15 | `detector_alerts_2024w15.xlsx` | XLSX | ~12 | Task author | — | The naive alerts |

## 5. Deterministic solution path

1. Parse FOIA PDFs to airport-day throughput; validate against the national daily totals.
2. Build aligned baselines per airport-day; compute naive change, calendar effect, real change for week 15 at every node.
3. Drill national → hub group → airport by largest negative real change; apply the 5% rule; name the owner (or "no anomaly").
4. Re-examine each detector alert: share of its naive drop explained by calendar effect.

## 6. Wrong paths (method errors, not misreadings)

**A — same ISO week comparison.** Twelve false anomalies; drill follows holiday-heavy airports.

**B — 365-day date comparison.** Weekday mismatch adds spurious changes.

**C — percentage-ranked drill.** Small airports with noisy volumes chosen as leaves.

**D — aligning only national totals.** Airport-level calendar effects differ (leisure vs business airports).

## 7. Why the stump is analytical, not semantic

Throughput, weeks and alignment rules are defined. The error is in constructing the counterfactual baseline — a
time-series comparison design issue — not in reading the data.

## 8. Draft task prompt (prose)

> The detector flagged a dozen airports for week 15 of 2024. Using the TSA throughput files and the analytics memo in the
> folder, rebuild each airport's comparison with an Easter- and weekday-aligned baseline, drill from national through hub
> size to airport following the largest real decline, and tell me which airport (if any) needs an operations review and who
> owns it. Provide `drilldown.xlsx` with naive change, calendar effect and real change for every node at each level, plus a
> sheet re-scoring the twelve alerts, and `calendar_vs_real.png` showing the national and leaf-airport daily series for
> both years aligned by Easter. On the first sheet, state the answer and the share of the national naive drop explained by
> the calendar.

## 9. Deliverables

* `drilldown.xlsx`, `calendar_vs_real.png`.

## 10. Where 25+ rubric criteria come from

* National and 3 hub groups × 3 components = 12; leaf-level airports (~10) real changes; 12 alerts re-scored; decision;
  owner; national calendar share.

## 11. Golden-output checklist

* Correct alignment windows; 364-day lag elsewhere; component decomposition; drill rule; 5% test; owner.

## 12. Build notes (scope tuning)

* Parse and validate the FOIA PDFs (they are large tabular PDFs); publish the parser and validation totals.
* Confirm that after alignment either one airport stands out or none does; both are acceptable deterministic answers.
