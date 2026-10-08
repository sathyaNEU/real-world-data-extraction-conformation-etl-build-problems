# RC29 — Fifteen regional outages last quarter: which were power cuts, which were routing withdrawals, and which were transit failures?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Outage triage at CDNs, messaging and cloud providers (Meta, Google, Cloudflare): deciding whether a regional traffic drop is an external power or connectivity event or something else, using independent signals |
| Domain | Internet measurement / network operations |
| Task shape | 18 · Hypotheses versus evidence (outage events × signals: BGP-visible prefixes, active-probing responsiveness, network-telescope traffic, at region and ASN level; each event classified, then SLA exclusion decisions) |
| Core method | For each event window, compute each signal's drop against its own baseline (median of the same hour over the prior 7 days); classify with a signal-pattern table: power outage (probing and telescope drop, BGP stable), routing withdrawal (BGP drops with probing), upstream transit degradation (partial BGP and probing drops concentrated in ASNs sharing an upstream); require alignment of drop onsets; check concentration across ASNs |
| Analytical stump | BGP visibility is the most familiar signal, so "routes stayed up" is read as "not an internet outage". Power cuts leave routes announced while hosts go dark. Raw signal levels have strong diurnal cycles, so drops must be measured against same-hour baselines. A large ASN's outage can look regional when aggregated; concentration across ASNs decides whether it is local to one network |
| Primary sources | IODA (Internet Outage Detection and Analysis, Georgia Tech) signals API — BGP, active probing, network telescope — for regions and ASNs |

## 1. The real-world situation

A CDN's contracts exclude force-majeure events (regional power outages and routing withdrawals by local networks) from availability SLAs; failures of
upstream transit providers are not excluded. Last quarter, fifteen regional events hit customers in one country. The account team classified them from BGP dashboards
alone: events with route withdrawals were excluded, the rest were treated as service failures. Customers disputed several exclusions, and finance
suspects that some power outages were missed. Finance needs a defensible classification to decide which credits to pay.

## 2. The decision (one deterministic recommendation)

**For each of the 15 events, the cause class (power outage, routing withdrawal, upstream transit degradation, unclassified), and therefore whether
SLA credits are owed (owed for transit degradation and unclassified events), with the signal evidence.**

Rules (operations memo):

* Data: IODA signals for the memo's country, its regions and its 20 largest ASNs, at 5-minute (BGP, telescope) and 10-minute (active probing)
  resolution, for each event window ± 6 hours.
* Baseline: for each signal and entity, the median of the same time-of-day bin over the 7 days before the event.
* Drop: 1 − (event-window minimum of the 30-minute rolling mean ÷ baseline at the same time of day).
* Onset: the first bin where the rolling mean falls below 80% of baseline.
* Region-level pattern:
  * Power outage: active probing drop ≥ 30% and telescope drop ≥ 30%, BGP drop < 10%.
  * Routing withdrawal: BGP drop ≥ 30% and active probing drop ≥ 30%, onsets within 20 minutes.
  * Upstream transit degradation: BGP drop 10–30% or probing drop ≥ 30% with BGP < 30%, and ≥ 70% of the probing loss concentrated in ASNs sharing
    one upstream (memo's AS-relationship table).
  * Otherwise unclassified.
* Concentration: if one ASN accounts for ≥ 80% of the region's probing loss, apply the patterns at that ASN instead and label the event "single
  network" in addition to its class.

## 3. Why capable analysts get it wrong

* BGP dashboards are the default view of "the internet is down".
* Signals have different resolutions and react at different speeds.
* Diurnal cycles make night-time levels look like outages.
* Aggregation across ASNs hides single-network failures.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ioda_signals_region_<country>_<quarter>.json` | JSON | ~400k points | IODA API (Georgia Tech) | IODA data terms (free with attribution; verify) | Regional signals |
| 2 | `ioda_signals_asn_<country>_<quarter>.json` | JSON | ~700k points | IODA API | Same | ASN signals |
| 3 | `ioda_outage_events_<country>_<quarter>.json` | JSON | ~40 | IODA outage alerts/events | Same | Event windows |
| 4 | `as_relationships_<date>.txt` | TXT | ~500k | CAIDA AS Relationships (serial-2) | CAIDA AUA (research use; verify) | Upstream mapping |
| 5 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2, the 15 events |
| 6 | `account_team_classification.xlsx` | XLSX | 15 | Task author | — | BGP-based classification |
| 7 | `public_event_reports.csv` | CSV | ~10 | Task author (links to grid operator and network operator public notices) | Cite | Validation only |

## 5. Deterministic solution path

1. Pull signals for events ± 6 h and 7 prior days; build baselines by time-of-day bin.
2. Rolling means, drops and onsets per signal and entity.
3. Concentration check; classify each event; SLA credit decision.
4. Validate against public reports; contrast with the account team's classification.

## 6. Wrong paths (method errors, not misreadings)

**A — BGP only.** Power outages are classified as no outage or as service problems.

**B — absolute thresholds without same-hour baselines.** Night-time troughs read as drops.

**C — region aggregate only.** Single-network failures are labelled regional and excluded wrongly.

**D — onset ignored.** Unrelated drops in different signals are combined into one pattern.

## 7. Why the stump is analytical, not semantic

The thresholds, baselines and patterns are numeric; the AS-relationship table resolves upstreams. The trap is single-signal inference and
unnormalised time series.

## 8. Draft task prompt (prose)

> Customers dispute our force-majeure exclusions for last quarter's regional outages. Classify the 15 events using the operations memo's
> signal-triangulation rules and tell me which credits we owe. Provide `event_classification.csv` (event: drops, onsets, class, credit owed),
> `signal_panels.png`, and a one-page `sla_credit_decision.pdf`.

## 9. Deliverables

* `event_classification.csv` — one row per event with signal drops, onsets, concentration and class.
* `signal_panels.png` — small multiples of the three normalised signals per event, coloured by class.
* `sla_credit_decision.pdf` — credits owed and the evidence, with the account-team contrast.

## 10. Where 25+ rubric criteria come from

* Baselines and drops for 15 events × 3 signals (sampled 5 events): 15.
* Onsets and alignment: 3.
* Concentration checks: 2.
* Classes and credit decisions for 15 events: 15 (grouped as 5 criteria).
* Validation and contrast: 3.

## 11. Golden-output checklist

* Same-hour 7-day median baselines; 30-minute rolling minima.
* Onset rule; 20-minute alignment.
* Concentration ≥ 80% handling; upstream mapping.

## 12. Build notes (scope tuning)

* Choose a country and quarter with at least two documented grid-related power outages and one transit-provider incident; confirm that the BGP-only
  classification misclassifies the power outages.
