# P29 — Terminal berth dwell from AIS: calls cut at midnight UTC and two ships sharing one MMSI

| Field | Value |
|---|---|
| Domain | Ports & maritime logistics / terminal capital planning / geospatial streaming data |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (one terminal receives new cranes) |
| Core technique | Sessionization of positional streams across file boundaries; geofencing with speed/duration rules and gap bridging; vessel identity resolution (MMSI + static attributes); filtering by vessel type |
| Trap family (honest data) | Daily files processed independently; gap = call end; MMSI treated as a unique vessel; tugs counted |
| Primary sources | NOAA/BOEM MarineCadastre AIS daily point files, terminal polygons, AIS message/type documentation |

## 1. The real-world project

A port authority will fund new ship-to-shore cranes at **one** of six container terminals: the terminal with the longest
average berth dwell for large cargo vessels in 2023. The analytics team processed each daily AIS file separately and ended
a call whenever pings stopped for more than an hour. Average dwells came out under 14 hours everywhere — terminal
operators' own berth logs said 30–40.

## 2. The business decision (one deterministic recommendation)

**Which terminal gets the cranes (longest mean 2023 berth dwell among terminals with ≥ 30 qualifying calls), and what
is the gap to second place?**

Rules (call-detection standard):

* Vessels: AIS `VesselType` 70–79 (cargo) and `Length` ≥ 200 m; MMSI must be 9 digits with a valid maritime
  identification digit range (no 000000000, 111111111, 123456789, etc.).
* Identity: a "vessel" is an MMSI segment with consistent `IMO` (and `VesselName` when IMO is missing). When the static
  identity changes, or when consecutive pings imply speed > 50 knots, a new segment starts.
* Call: inside a terminal polygon with SOG ≤ 0.5 kn for ≥ 2 hours. A call continues through AIS gaps of up to 6 hours if the
  vessel's next ping is still inside the polygon with SOG ≤ 0.5 kn; it ends when the vessel leaves the polygon or SOG > 1 kn
  for ≥ 30 minutes.
* Calls are built on the **continuous** stream across daily files (files are cut at 00:00 UTC).
* Calls starting in 2023 count; dwell = end − start in hours.

## 3. Why this gets overlooked in real projects

* AIS arrives as daily files; per-file processing is natural for parallelism and silently truncates every call that
  spans midnight UTC — most berth calls do.
* Berthed ships ping less often and coverage has holes; treating every gap as departure fragments calls.
* MMSI is assumed to be a vessel ID; in practice it is reused after re-flagging, shared by mistake, or mis-entered,
  producing "teleporting" tracks that create phantom calls.
* Tugs and service craft at the berth are numerous and short-dwelling.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–365 | `AIS_2023_MM_DD.csv` (regional spatial extract of each daily file) | CSV / zipped CSV | 0.2–1M each (regional) | MarineCadastre.gov (NOAA OCM / BOEM) | U.S. Gov public domain | Position + static fields |
| 366 | `terminal_polygons.geojson` | GeoJSON | 6 | Task author (digitized from public port maps / OpenStreetMap, ODbL) | ODbL if from OSM | Geofences |
| 367 | `ais_data_dictionary.pdf` | PDF | — | MarineCadastre | Public domain | Field meanings, 1-minute filtering |
| 368 | `itu_mid_table.csv` | CSV | ~300 | ITU MID list (public reference) | Public reference (verify) | MMSI validity |
| 369 | `vessel_type_codes.csv` | CSV | ~100 | USCG NAIS / ITU-R M.1371 types | Public domain | Type ranges |
| 370 | `call_detection_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 371 | `terminal_berth_stats_2023.xlsx` | XLSX | 6 | Port authority annual report (public) | Public | Sanity check only |

## 5. Deterministic solution path

1. Filter to the port bounding box, vessel type/length, valid MMSI; sort by MMSI and time across all days.
2. Segment identity by static changes and implied-speed breaks.
3. Point-in-polygon; run the state machine for call start/continue/end with gap bridging.
4. Compute dwell per call; aggregate by terminal; apply ≥ 30 calls; rank; winner and gap.
5. Contrast: per-file processing; gap-as-end; MMSI-only identity; tugs included.

## 6. The traps

**Trap A — per-day processing.** Calls truncated at midnight UTC; terminals with longer stays lose the most; ranking
changes.

**Trap B — gaps end calls.** Fragmentation lowers means unevenly by terminal (coverage differs by berth).

**Trap C — MMSI as identity.** Phantom calls from shared MMSIs; spurious long dwells.

**Trap D — no type/length filter.** Tugs dominate counts.

## 7. Why the data is honest

MarineCadastre publishes AIS as received by the U.S. Coast Guard network; coverage gaps, MMSI reuse and daily partitioning
are real properties of the system. The standard defines how to build calls.

## 8. Draft task prompt (prose)

> One terminal gets the new cranes: the one whose large cargo vessels dwelt longest at berth in 2023, measured by our
> call-detection standard. Using the AIS files and terminal polygons in the folder, build the calls, rank the six
> terminals and tell me the winner and its margin. Provide `port_calls_2023.csv` (one row per call: vessel segment, MMSI,
> IMO, terminal, start, end, dwell, gaps bridged), `terminal_dwell.png` showing each terminal's dwell distribution with
> the mean marked and the winner highlighted, and a one-page `crane_decision.pdf` stating the winner, the mean dwell and
> call count for all six, and what the ranking would have been if each day's file had been processed separately.

## 9. Deliverables

* `port_calls_2023.csv`, `terminal_dwell.png`, `crane_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 terminals × (mean dwell, call count, rank); winner and gap; per-day variant ranking; identity splits count; spot-check
  of 5 calls spanning midnight.

## 11. Golden-output checklist

* Cross-file sessionization; gap bridging; identity segmentation; filters; decision stated.

## 12. Build notes (scope tuning)

* Choose a port where two terminals are within ~10% on true dwell and differ in midnight-spanning share; confirm Trap A
  flips the winner.
* Daily national files are large; ship a regional extract and document the extraction query.
