# RC42 — Root DNS query volume doubled: more internet users, attacks, or one browser's probing behaviour?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Platform load driven by a client software behaviour (a mobile SDK release multiplying API calls, a smart-TV firmware polling a CDN, a library retry storm) rather than by user growth or abuse |
| Domain | Internet infrastructure / DNS operations |
| Task shape | 18 · Hypotheses versus evidence (organic resolver growth, attack traffic, client software probes → evidence lines from per-letter daily metrics; the cause root operators address) |
| Core method | Per root-server letter, daily RSSAC002 metrics: query volume, response codes, unique sources; decompose query growth into NXDOMAIN and other responses; test whether growth tracks unique-source growth (organic), appears as spikes concentrated in few days (attacks), or rises smoothly in NXDOMAIN and reverses after a client software change (probes); use letters with consistent reporting and normalise by each letter's share |
| Analytical stump | Total query counts mix very different sources. Organic growth raises unique sources and all response types; attacks are bursty; a browser feature that issues random single-label lookups raises NXDOMAIN responses smoothly with browser adoption and falls after the vendor changes the feature. Looking at totals, or at one letter whose anycast footprint changed, leads to the wrong conclusion and the wrong remedy (capacity build-out vs outreach to a software vendor) |
| Primary sources | RSSAC002 root server operator metrics (daily YAML per root letter: traffic volume, rcode volume, unique sources); Chromium release history (public) |

## 1. The real-world situation

Root server operators saw query volume roughly double over two years. One operator proposed a major capacity expansion to keep up with "internet
growth". Engineers at another operator pointed out that most of the growth was NXDOMAIN responses for random-looking single-label names, which they
associated with a browser's intranet-redirect detection. The operators' caucus wants an evidence-based attribution before committing capital.

## 2. The decision (one deterministic recommendation)

**The dominant cause of query growth (organic, attack, or client software probes) by attributable share of the growth across consistently reporting
letters, and therefore the remedy (capacity, mitigation, or vendor engagement).**

Rules (caucus memo):

* Data: RSSAC002 daily metrics for the memo's letters with continuous reporting over the window; metrics: traffic-volume (queries), rcode-volume
  (NOERROR, NXDOMAIN, other), unique-sources (IPv4 and IPv6, aggregated).
* Window: the memo's start and end dates spanning the growth and the browser change (Chromium release that reduced the probes).
* Spikes, per letter: daily excess e_d = queries − 30-day rolling median when that difference exceeds 3 × the rolling MAD, else 0; spike days are
  days with e_d > 0.
* Monthly values per letter: E_m = mean of e_d over all days; on non-spike days, B_m = mean queries, N_m = mean NXDOMAIN responses, S_m = mean unique
  sources. "Start" is the window's first month; "end" is the month before the browser change.
* Components of growth: attack = E_end − E_start; probe = (N_end − N_start) − (N_start ÷ S_start) × (S_end − S_start); organic = (B_end − N_end) −
  (B_start − N_start) + (N_start ÷ S_start) × (S_end − S_start). Shares = component ÷ sum of components; the gap between that sum and the change in
  mean daily queries is reported as a residual.
* Reversal test: N_m falls by ≥ 20% within 6 months after the browser change.
* Dominant cause = largest share (aggregated across letters weighted by each letter's start-month volume).

## 3. Why capable analysts get it wrong

* Query volume is the headline capacity metric.
* Response-code composition is reported separately and is rarely examined.
* Letters differ in anycast footprint and reporting; one letter can mislead.
* Spikes and smooth growth have different causes and should be separated with robust statistics.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `rssac002-data/<letter>/<year>/<month>/*.yaml` | YAML | ~50k files (letter × day × metric) | RSSAC002 data repository (root server operators) | Published openly by operators (verify terms) | Daily metrics |
| 2 | `rssac002_metric_definitions.pdf` | PDF | — | ICANN RSSAC002 v4 | Public | Metric definitions |
| 3 | `chromium_release_dates.csv` | CSV | ~100 | Task author (from public Chromium release history; cite) | Cite | Release timing |
| 4 | `letter_reporting_gaps.csv` | CSV | ~50 | Task author (derived from file 1) | — | Coverage per letter |
| 5 | `caucus_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `capacity_expansion_proposal.xlsx` | XLSX | — | Task author | — | Total-volume trend |
| 7 | `verisign_chromium_root_study_citation.pdf` | PDF | — | Cite (public operator analysis of browser probes) | Cite | Background |

## 5. Deterministic solution path

1. Parse YAML files; select letters with continuous reporting; aggregate IPv4/IPv6 sources.
2. Spike excesses; non-spike monthly means; attack, probe and organic components.
3. Shares per letter and weighted aggregate; reversal test.
4. Dominant cause and remedy; contrast with the expansion proposal.

## 6. Wrong paths (method errors, not misreadings)

**A — total queries.** Growth read as internet growth; capacity build-out chosen.

**B — raw monthly means.** Without separating spike excess, attack traffic inflates growth and its attribution.

**C — a single letter.** Footprint changes at one letter look like global growth or decline.

**D — no source normalisation.** NXDOMAIN growth that merely tracks source growth is credited to probes.

## 7. Why the stump is analytical, not semantic

The metrics and rules are numeric; no query names are needed. The trap is aggregate volume hiding a composition change with a clear signature.

## 8. Draft task prompt (prose)

> One operator wants to expand capacity because root queries doubled. Attribute the growth with the caucus memo's response-code method and tell me
> what drove it and which remedy fits. Provide `query_growth_attribution.csv` (letter × cause: share), `rcode_timeline.png`, and a one-page
> `root_load_rca.pdf`.

## 9. Deliverables

* `query_growth_attribution.csv` — shares per letter and aggregate; reversal test.
* `rcode_timeline.png` — non-spike monthly means by response code with the browser change marked.
* `root_load_rca.pdf` — dominant cause, remedy and the contrast with the proposal.

## 10. Where 25+ rubric criteria come from

* Letter selection and coverage: 3.
* Start and end monthly values (B, N, S, E) for 4 letters: 12 (grouped).
* Attack, probe and organic shares: 6.
* Reversal test: 2.
* Dominant cause and remedy: 2.
* Contrast: 2.

## 11. Golden-output checklist

* Continuous-reporting letters only; IPv4+IPv6 sources.
* Rolling-median and MAD spike excess; non-spike monthly means.
* Source-normalised NXDOMAIN growth; weighting by start-month volume.

## 12. Build notes (scope tuning)

* Choose a window ending at least 6 months after the browser change; confirm the probe share exceeds the organic share for the majority of letters.
