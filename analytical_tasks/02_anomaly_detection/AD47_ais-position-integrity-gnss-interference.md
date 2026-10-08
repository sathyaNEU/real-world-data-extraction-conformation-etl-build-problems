# AD47 — Ships that teleport: jamming, two ships sharing one ID, or a receiver gap?

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Location-integrity teams at ride-hail and delivery platforms (GPS spoofing by drivers), fleet telematics providers and maritime-security analysts |
| Domain | Maritime / location data integrity |
| Task shape | 18 · Hypotheses versus evidence (three causes of impossible jumps × lines of evidence → the dominant cause in the alert region, and the response it calls for) |
| Core method | Track separation before kinematics: split each MMSI's messages into consistent tracks by implied speed (multiple-hypothesis assignment); implied speed between consecutive positions in the *same* track; spatial and temporal concentration of jumps across many vessels (common-mode interference) versus per-MMSI persistence (identity collision) versus gap length (receiver dropouts) |
| Analytical stump | Implied speed computed on raw MMSI sequences flags thousands of "teleports" that are really two vessels broadcasting the same MMSI, and long reception gaps create large but legitimate displacements. GNSS interference shows up as *many vessels at once* in one area and time window reporting displaced or circular positions — a cross-sectional signal, not a per-vessel one |
| Primary sources | Danish Maritime Authority historical AIS data (daily CSV) |

## 1. The real-world situation

A maritime-security analytics provider saw a surge in "impossible movement" alerts for the southern Baltic over one month. Customers
wanted to know whether the alerts reflected GNSS jamming or spoofing — which requires notifying shipping and authorities — or data
artefacts. The alerting pipeline computed implied speed on consecutive messages per MMSI and alerted above 50 knots.

## 2. The decision (one deterministic recommendation)

**The dominant cause of the month's alerts in the alert region (interference, identity collision or reception gaps), measured by alert share
after the memo's tests, and therefore the notice to issue.**

Rules (integrity memo):

* Data: DMA AIS position reports (message types 1–3, 18–19) for the month and bounding box in the memo; drop positions with invalid
  lat/lon (91/181 sentinels).
* Track separation: within an MMSI, assign each message to the existing track whose last position implies ≤ 40 knots; otherwise start a new
  track; an MMSI with ≥ 2 concurrent tracks for > 6 hours is an identity collision.
* Alert: consecutive messages within a track with implied speed > 50 knots.
* Gap test: alert with time gap > 30 minutes → reception gap (implied speed is then over a long interval; the memo recomputes with
  great-circle distance ÷ gap and checks ≤ 40 knots).
* Interference test: grid cells of 0.5° × 0.5° and 1-hour windows; a cell-hour is "interfered" if ≥ 10 distinct MMSIs have alerts in it.
  Alerts in interfered cell-hours → interference.
* Remaining alerts on raw MMSI sequences that disappear after track separation → identity collision.
* Dominant cause = largest share of the original raw alerts.

## 3. Why capable analysts get it wrong

* Per-vehicle kinematic rules are the standard integrity check.
* Identity collisions (duplicated MMSIs, default IDs) are common in AIS and look like teleports.
* Reception gaps make legitimate long moves look fast if gap duration is ignored.
* Interference is a common-mode event across vessels; it appears only in cross-sectional aggregation.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–30 | `aisdk-<yyyy-mm-dd>.zip` (30 daily files) | CSV | ~10–15M each (region subset ~2M) | Danish Maritime Authority (web.ais.dk) | DMA terms for AIS data (free reuse with attribution; verify) | Position reports |
| 31 | `dma_ais_field_description.pdf` | PDF | — | DMA | Same | Fields |
| 32 | `alert_region_bbox.json` | JSON | 1 | Task author | — | Region |
| 33 | `integrity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 34 | `raw_alerts.parquet` | Parquet | ~50k | Task author (replay of existing pipeline) | — | Existing alerts |
| 35 | `published_gnss_interference_notices.json` | JSON | ~5 | Task author (from public aviation/maritime notices) | — | Context |
| 36 | `itu_m1371_excerpt_citation.pdf` | PDF | — | ITU-R M.1371 (cite) | Cite | AIS message types |
| 37 | `grid_cells.geojson` | GeoJSON | ~200 | Derived | — | Analysis grid |

## 5. Deterministic solution path

1. Filter messages and sentinels; sort per MMSI by time.
2. Track separation; detect identity collisions.
3. Recompute alerts within tracks; apply the gap test.
4. Cross-sectional interference test by cell-hour.
5. Attribute every raw alert to a cause; shares; dominant cause.

## 6. Wrong paths (method errors, not misreadings)

**A — per-MMSI implied speed only.** Collisions counted as spoofing.

**B — ignoring gap duration.** Dropouts counted as jumps.

**C — per-vessel interference judgement.** Common-mode signal missed.

**D — counting cell-hours rather than alerts.** Shares misstated.

## 7. Why the stump is analytical, not semantic

The tests and thresholds are specified. The traps are the order of operations (identity before kinematics) and recognising a cross-sectional
signal.

## 8. Draft task prompt (prose)

> What is behind this month's surge of impossible-movement alerts in the southern Baltic? Apply the integrity memo's tests to the DMA AIS data
> and tell me the dominant cause and what notice we should issue. Provide `cause_evidence_grid.csv` (cause × test: alerts, share, consistent?),
> `interference_heatmap.png` (cell-hours with ≥ 10 alerting vessels), and a one-page `integrity_notice.pdf`.

## 9. Deliverables

* `cause_evidence_grid.csv`, `interference_heatmap.png`, `integrity_notice.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 causes × 4 evidence lines = 12 cells; alert counts by cause; collision MMSI count; interfered cell-hours; dominant cause; notice.

## 11. Golden-output checklist

* Sentinels; track separation; gap test; cell-hour aggregation; attribution order; shares.

## 12. Build notes (scope tuning)

* Choose a month with documented regional GNSS interference and many duplicated MMSIs.
* Confirm that interference is the dominant cause while identity collisions alone exceed the gap share, so that skipping track separation
  or the cross-sectional test changes the answer.
