# P27 — Historical fleet mix by tail number: the registry tells you who owns the N-number today, not who flew in 2019

| Field | Value |
|---|---|
| Domain | Airports / aviation planning / emissions inventories |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 07 · Grid of cells (airport × aircraft size class) |
| Core technique | Slowly-changing-dimension lookup with validity intervals (current + deregistered registrations); identifier formatting conformance; reference-table enrichment |
| Trap family (honest data) | Join to the current registry only (reassigned and retired tails mis-typed or dropped); 'N' prefix mismatch; multiple historical registrations per N-number |
| Primary sources | BTS Reporting Carrier On-Time Performance (tail numbers), FAA Releasable Aircraft Database (MASTER, DEREG, ACFTREF) |

## 1. The real-world project

A state aviation office runs a grant for airports facing the retirement of 50-seat regional jets. The first airport funded
is the one with the **highest 2019 share of departures flown by aircraft with ≤ 50 seats**. Analysts joined 2019 BTS
flights' tail numbers to today's FAA registry. Many tails did not match and were dropped; some matched to small private
aircraft; the ranking looked odd to everyone who had actually watched those airports in 2019.

## 2. The business decision (one deterministic recommendation)

**Which of the eight candidate airports had the highest share of 2019 scheduled departures flown by aircraft with ≤ 50
seats (and gets the grant first)?**

Rules (grant method):

* Flights: 2019 departures (Origin = airport) in the BTS Reporting Carrier On-Time table, excluding cancelled flights.
* Tail → registration: strip the leading `N` from `Tail_Number` to match FAA `N-NUMBER`; find the registration whose
  interval [`CERT ISSUE DATE`, `CANCEL DATE` or open) contains the flight date, searching **both** `MASTER.txt` and
  `DEREG.txt`. If several match, take the latest `CERT ISSUE DATE`.
* Seats from `ACFTREF.txt` via the registration's `MFR MDL CODE`; classes: ≤ 50, 51–76, 77–150, > 150.
* Unresolved tails are reported as their own column and excluded from the share denominator.
* Grid = airport × class shares; the grant goes to the max ≤ 50 share; report the runner-up and the gap.

## 3. Why this gets overlooked in real projects

* The FAA registry is a current-state table; joining history to it is the default. N-numbers are reassigned after
  deregistration, and airlines move N-numbers between airframes.
* The aircraft that left the fleet since 2019 — overwhelmingly the 50-seat jets being studied — exist only in `DEREG.txt`,
  so a current-only join drops exactly the class of interest.
* BTS stores tails with the `N`; FAA stores them without. A failed join looks like "bad data", not a formatting rule.
* `DEREG.txt` can hold several historical registrations for one N-number; the date interval decides.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–12 | `ontime_2019_01.csv` … `ontime_2019_12.csv` | CSV | ~600k each | BTS Reporting Carrier On-Time Performance | U.S. Gov public domain | Flights with tail numbers |
| 13 | `MASTER.txt` | CSV-like text | ~300k | FAA Releasable Aircraft Database | Public domain | Current registrations |
| 14 | `DEREG.txt` | CSV-like text | ~400k+ | FAA | Public domain | Deregistered history |
| 15 | `ACFTREF.txt` | CSV-like text | ~90k | FAA | Public domain | Make/model, seats |
| 16 | `ardata.pdf` (record layouts) | PDF | — | FAA | Public domain | Field definitions, date formats |
| 17 | `L_AIRPORT_ID.csv` | CSV | ~6.5k | BTS | Public domain | Airport IDs |
| 18 | `grant_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 19 | `candidate_airports.json` | JSON | 8 | Task author | — | Scope |

## 5. Deterministic solution path

1. Filter 2019 departures at the eight airports; normalize tails.
2. Union MASTER and DEREG with validity intervals; interval-join on N-number and flight date; tie-break.
3. Enrich with seats; classify; compute grid shares (excluding unresolved).
4. Rank ≤ 50 shares; grant to the top; report runner-up and gap; report unresolved share by airport.
5. Contrast with current-registry-only join.

## 6. The traps

**Trap A — MASTER only.** Retired 50-seaters vanish; airports that relied on them drop in the ranking.

**Trap B — no date interval.** Reassigned N-numbers map 2019 flights to the wrong aircraft type.

**Trap C — prefix mismatch.** Near-zero match rate; partial fixes (e.g. string contains) create false matches.

**Trap D — unresolved in denominator.** Dilutes shares unevenly across airports.

## 7. Why the data is honest

The FAA registry and BTS performance data are official; registration history and N-number reassignment are documented
features of aircraft registration. Nothing is planted.

## 8. Draft task prompt (prose)

> The first regional-jet transition grant goes to whichever of the eight candidate airports had the highest share of 2019
> departures flown by aircraft with fifty seats or fewer, measured as our grant method describes. Using the BTS on-time
> files and the FAA registry files in the folder, build the airport-by-size-class grid and tell me the airport. Produce
> `fleet_mix_grid.csv` with departures and shares per airport and class plus unresolved tails, and `fleet_mix_heatmap.png`
> with airports as rows and size classes as columns, shares printed and the winning cell outlined. Add a one-page
> `grant_memo.pdf` stating the airport, its share, the runner-up gap, and which airport would have won with today's
> registry alone.

## 9. Deliverables

* `fleet_mix_grid.csv`, `fleet_mix_heatmap.png`, `grant_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 airports × 4 classes = 32 shares; unresolved rates; winner, runner-up gap; current-registry-only alternative.

## 11. Golden-output checklist

* MASTER + DEREG with intervals; prefix handled; seats from ACFTREF; unresolved excluded; decision stated.

## 12. Build notes (scope tuning)

* Choose airports where 50-seat jets were common in 2019 and retired by the download date; verify the MASTER-only join
  changes the winner.
* Confirm the date formats and the cancel-date field name in `DEREG.txt` from the FAA layout document.
