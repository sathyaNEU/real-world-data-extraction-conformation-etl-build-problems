# DA39 — How many journeys does the region's transit carry? Boardings count every leg

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Sessions versus page views, journeys versus legs, orders versus shipments — any metric where one user action generates several counted events across systems |
| Domain | Public transportation |
| Task shape | 03 · Bridge between two totals (sum of unlinked passenger trips across agencies and modes → regional linked trips; the agency whose fare-integration subsidy share is set by its linked-trip share) |
| Core method | Convert unlinked trips (boardings) to linked trips using transfer rates (boardings per linked trip) from the memo's on-board survey tables by agency and mode; inter-agency transfers counted once at the regional level; attribute linked trips to the first-boarding agency per memo |
| Analytical stump | Agencies report boardings; a journey with two transfers counts three times. Summing across agencies double counts inter-agency transfers, and per-agency shares of boardings overstate agencies that serve as feeders. Subsidy shares based on journeys require the conversion |
| Primary sources | Federal Transit Administration National Transit Database (NTD) monthly ridership (unlinked passenger trips by agency and mode) |

## 1. The real-world situation

A regional transit authority splits a fare-integration subsidy among its member agencies in proportion to each agency's share of regional
linked trips (journeys). The draft allocation used each agency's share of total unlinked passenger trips. A feeder bus operator received a
much larger share than its role in journeys warrants; a commuter rail operator objected.

## 2. The decision (one deterministic recommendation)

**Each agency's subsidy share (percent, two decimals, summing to 100.00) based on linked trips for the year, and the bridge from total
boardings to regional linked trips.**

Rules (allocation memo):

* Data: NTD monthly ridership for the region's 6 agencies, calendar year in the memo; unlinked passenger trips (UPT) by agency × mode.
* Transfer rates: boardings per linked trip by agency × mode from `onboard_survey_transfer_rates.csv` (regional on-board survey), split into
  intra-agency and inter-agency transfers.
* Agency linked trips (first-boarding attribution) = Σ over its modes of UPT ÷ (boardings per linked trip), where inter-agency transfer
  boardings are attributed to the first agency per the survey's first-agency shares.
* Regional linked trips = Σ agency linked trips (no double counting by construction); bridge: total UPT → minus intra-agency transfers → minus
  inter-agency transfers → regional linked trips.
* Subsidy share = agency linked trips ÷ regional linked trips; round with largest remainder to two decimals.

## 3. Why capable analysts get it wrong

* UPT is the standard reported ridership measure.
* Transfers inflate boardings unevenly across agencies and modes.
* Summing agency totals double counts journeys that use more than one agency.
* Feeder modes have high transfer rates; their boarding share overstates their journey share.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Monthly_Ridership_<release>.xlsx` (UPT, VRM, VRH sheets) | XLSX | ~2.2k agency-modes × ~270 months | FTA NTD | U.S. Gov public domain | Monthly ridership |
| 2 | `ntd_glossary.pdf` | PDF | — | FTA | Public domain | UPT definition |
| 3 | `agencies_in_scope.json` | JSON | 6 | Task author | — | Region's agencies (NTD IDs) |
| 4 | `onboard_survey_transfer_rates.csv` | CSV | ~20 | Task author (from the region's published on-board survey report) | Cite | Transfer rates, first-agency shares |
| 5 | `onboard_survey_report_citation.pdf` | PDF | — | Regional planning agency (cite) | Public | Source of rates |
| 6 | `allocation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `draft_upt_allocation.xlsx` | XLSX | 6 | Task author | — | Draft shares |
| 8 | `ntd_annual_agency_profiles.csv` | CSV | ~2k | FTA NTD | Public domain | Validation of annual UPT |

## 5. Deterministic solution path

1. Extract annual UPT by agency × mode for the year.
2. Apply transfer rates and first-agency attribution; linked trips.
3. Bridge totals; shares with rounding.
4. Contrast with the UPT-based draft.

## 6. Wrong paths (method errors, not misreadings)

**A — UPT shares.** Feeder agencies overpaid.

**B — dividing by a single regional transfer rate.** Mode and agency differences lost.

**C — inter-agency transfers counted for both agencies.** Regional total inflated.

**D — rounding without largest remainder.** Shares don't sum to 100.00.

## 7. Why the stump is analytical, not semantic

The rates and attribution are given. The trap is event-versus-journey counting.

## 8. Draft task prompt (prose)

> Set each agency's fare-integration subsidy share from linked trips as the allocation memo specifies, and show how boardings bridge to regional
> journeys. Provide `agency_linked_trips.csv` (agency × mode: UPT, rate, linked trips; agency share), `boardings_to_journeys.png` (waterfall), and a
> one-page `subsidy_allocation.pdf`.

## 9. Deliverables

* `agency_linked_trips.csv`, `boardings_to_journeys.png`, `subsidy_allocation.pdf`.

## 10. Where 25+ rubric criteria come from

* ~15 agency-mode linked-trip values; 6 shares; bridge items; contrast with draft shares.

## 11. Golden-output checklist

* Year extraction; rates by mode; first-agency attribution; bridge; rounding.

## 12. Build notes (scope tuning)

* Confirm at least two agencies' shares change by more than 3 percentage points versus the draft.
