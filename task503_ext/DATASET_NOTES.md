# task503 dataset notes

- Domain: Supply Chain & Logistics
- Subdomain: Trade & flows (port and border performance)
- Objective: Anomaly Detection & Diagnostics
- Spine: BTS Border Crossing Entry Data, inbound crossings by US land port, measure and month, January 1996 to August 2026 (276,749 rows, 118 ports, 8 measures)

This is a clean real-data bundle only, like task112_ext and task113_ext. No draw has been made and
nothing is planted: there is no ladder, no stump sentence, no calibration file, no governing document
and no social layer, and no fingerprint card is filed. Supply chain x anomaly detection has one
earlier build (task54), trade & flows has one (task39, ETL on a synthetic spine), and no
earlier build used the BTS crossings data or any of these publishers.

**Why the objective is the domain's own analysis.** The anomalies in this pack are disruptions to
freight and traveller flow at land ports, and diagnosing them needs logistics structure that a noun
swap would lose. Freight conveyances (trucks, trains) are set against passenger measures at the same
port. Thirty years of monthly history give each port its own baseline and seasonality. The national
series carries the dollar value of freight with Canada and Mexico, so a drop in truck counts can be
checked against the value of trade. The Canadian table counts trucks going the other way, so a
recording artifact on one side can be told apart from a real event on both. The Federal Register
notices are the operational log: they dated the 2020 restrictions that exempted cargo and truck
drivers, the November 2021 lifting, the January 2022 vaccination requirement that made no exception for truck drivers, and
the May 2023 end. Real events in the data that no file explains (the February 2022 bridge blockades,
the April 2022 Texas commercial inspections, port openings and closures) are left for the analysis
to find.

The mess is the publishers' own and nothing was added:
- nine blank `Value` cells and 70,683 zeros in the spine
- Chief Mountain (port 3315) with no state or coordinates
- two different ports both named Eastport (103 Maine, 3302 Idaho)
- the national series labels the pedestrian count "Incoming Person Crossings", and it matches the spine's pedestrians exactly in 304 of 368 months (Canada) and 330 of 368 (Mexico)
- national truck totals match the spine exactly in 332 of 368 months (Canada, worst gap 2.6%) and 357 of 368 (Mexico, worst gap 6.3% in July 2003)
- April 2023 appears twice in the national series
- the Statistics Canada table was archived after December 2021 and has 594 suppressed cells, and its Ontario rows include crossings not published port by port, so Ontario's listed ports fall short of the province total (the other eight provinces add up exactly)

`generator/build_pack.py` rebuilds `target/` from data.bts.gov, the Federal Register API, govinfo and
Statistics Canada, copies in `generator/provenance.md`, runs 23 checks (row count against the live
API, keys, measures, contiguous months on both borders, the reconciliations above, the notice index,
the Canadian table's province totals and suppression) and writes a flat `target.zip`. The
reconciliation checks assert floors (90% of months exact for trucks, 80% for pedestrians) rather
than the counts at the pull, so a rebuild after a BTS revision still passes and prints the new
counts.

Input gates as built: 12 files, four formats (csv, json, pdf, md), largest file 276,749 rows (and a
second at 88,080).

## Tried and rejected

- www.bts.gov pages and the TransBorder Freight raw files: www.bts.gov returns 403 to scripted downloads, and the TransBorder entry on data.bts.gov (kijm-95mr) is a link rather than a table. The freight value series in Monthly Transportation Statistics stands in at border level.
- Statistics Canada table 24-10-0002-01 in full (839,880 rows, 151 MB): cut to the truck rows from 1996 (88,080 rows), the only mode the US-side freight analysis needs.
- All 48 Federal Register notices as PDFs: the monthly extensions repeat the first notice, so the index carries all 48 and five PDFs carry the regime changes.
- Monthly Transportation Statistics' catalogue metadata (400 KB): it has no column descriptions, so it adds nothing the CSV headers do not.
