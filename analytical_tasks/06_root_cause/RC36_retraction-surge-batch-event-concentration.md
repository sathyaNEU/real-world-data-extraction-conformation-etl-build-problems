# RC36 — Retractions in our journals rose fivefold: a collapse in research integrity, or a few mass events?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | KPI spikes driven by a single source (support tickets from one customer's outage, refund spikes from one merchant, content takedowns from one coordinated network) |
| Domain | Scholarly publishing / research integrity |
| Task shape | 12 · Drill-down to one leaf (retractions by year → publisher → journal → retraction event (batch) → the event that carries the increase) |
| Core method | Cluster retractions into events (same journal, retraction notices dated within 7 days, ≥ 10 papers); compute the increase in retractions and the share explained by the largest events; concentration measures (top-event share, Herfindahl across events); compare event-adjusted retraction rates per published paper by publisher with an integrity baseline |
| Analytical stump | Year-over-year counts treat each retraction as an independent signal of misconduct. Mass retractions of guest-edited special issues or paper-mill batches arrive as one decision covering hundreds of papers; one event can explain most of the increase. Counting events, not papers, and measuring concentration reveals whether the problem is broad or a specific process failure (such as guest-editor controls) |
| Primary sources | Retraction Watch database (openly available via Crossref); Crossref REST API works counts by publisher and journal |

## 1. The real-world situation

A publisher's research-integrity office reported that retractions in its portfolio rose fivefold in a year. The board asked whether integrity
standards had collapsed across the portfolio and proposed an expensive portfolio-wide re-review. Integrity staff suspected that a few special
issues compromised by paper mills explained most of the rise, which would call for targeted controls on guest-edited issues instead.

## 2. The decision (one deterministic recommendation)

**The remediation adopted — targeted special-issue controls (if the top 3 events explain ≥ 60% of the year-over-year increase) or a portfolio-wide
re-review (otherwise) — with the event-level drill-down.**

Rules (integrity memo):

* Data: Retraction Watch records with retraction notice date in the reference and current years and the publisher in the memo (publisher name
  normalised via the memo's mapping); exclude records whose nature is "correction" or "expression of concern" (retractions only).
* Events: within a journal, sort by retraction notice date; consecutive retractions ≤ 7 days apart form a group; a group with ≥ 10 papers is a
  mass event, otherwise each retraction is a singleton event.
* Increase Δ = retractions_cur − retractions_ref; top-3 share = retractions in the current year's 3 largest events ÷ Δ (capped at 100%).
* Concentration: Herfindahl index over events in each year; number of events.
* Rates: event-adjusted retraction rate = (singletons + number of mass events) ÷ papers published by the publisher in the 5 prior years (Crossref
  counts), for both years.
* Drill path: publisher → journal with the largest increase → the largest event in that journal (leaf); report its reasons field distribution.

## 3. Why capable analysts get it wrong

* Paper counts are the natural unit of retractions.
* Batch decisions are recorded as many separate records.
* Retractions lag publication by years, so publication volume growth matters for rates.
* Portfolio averages hide a single compromised process.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `retraction_watch.csv` | CSV | ~55k | Retraction Watch database via Crossref (open data release) | Open via Crossref (verify terms) | Retraction records |
| 2 | `crossref_publisher_journal_counts.json` | JSON | ~20k (journal × year) | Crossref REST API (works counts by ISSN and year) | Crossref metadata (CC0) | Published papers |
| 3 | `publisher_name_mapping.csv` | CSV | ~200 | Task author | — | Publisher normalisation |
| 4 | `retraction_watch_field_guide.html` | HTML | — | Retraction Watch / Crossref | Same as 1 | Field definitions, reasons taxonomy |
| 5 | `integrity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `board_rereview_proposal.xlsx` | XLSX | — | Task author | — | Paper-count trend |

## 5. Deterministic solution path

1. Filter publisher, years and nature; normalise names.
2. Build events per journal; label mass events.
3. Δ, top-3 share, Herfindahl and event counts; event-adjusted rates.
4. Drill to the leaf event; decision; contrast with the board's paper-count trend.

## 6. Wrong paths (method errors, not misreadings)

**A — paper counts by year.** Treats one batch decision as hundreds of independent failures.

**B — per-journal averages.** Spreads a concentrated event across the portfolio.

**C — rates per papers published in the same year.** Ignores the lag between publication and retraction.

**D — including expressions of concern and corrections.** Inflates the count with non-retractions.

## 7. Why the stump is analytical, not semantic

The event rule and thresholds are numeric; the reasons field is reported, not used for the decision. The trap is ignoring dependence between
records.

## 8. Draft task prompt (prose)

> The board wants a portfolio-wide re-review because retractions rose fivefold. Use the integrity memo's event-based drill-down to tell me whether the
> rise is broad or concentrated, and which remediation fits. Provide `retraction_events.csv` (event: journal, dates, papers), `concentration_drilldown.png`,
> and a one-page `integrity_remediation_decision.pdf`.

## 9. Deliverables

* `retraction_events.csv` — all events in both years with sizes and mass-event flags.
* `concentration_drilldown.png` — retractions by year split into mass events and singletons, with the drill path.
* `integrity_remediation_decision.pdf` — decision, concentration metrics, event-adjusted rates and the leaf event.

## 10. Where 25+ rubric criteria come from

* Filtering counts by nature and year: 4.
* Event construction (mass events, singletons per year): 4.
* Δ, top-3 share, Herfindahl, event counts: 6.
* Event-adjusted rates (2 years): 4.
* Drill path (journal, leaf event, reasons distribution): 4.
* Decision and contrast: 3.

## 11. Golden-output checklist

* Retractions only; publisher normalisation.
* 7-day grouping within journal; ≥ 10 papers for mass events.
* Top-3 share against Δ; 5-year publication base for rates.

## 12. Build notes (scope tuning)

* Choose a publisher-year with a documented mass retraction of special-issue papers; confirm the top-3 share exceeds 60% while event-adjusted rates
  change little.
