# task113 dataset notes

- Domain: Quantitative finance. This is outside the six accepted domains in CLAUDE.md and was built at the author's request as a new domain.
- Objective: Anomaly Detection & Diagnostics
- Spine: New York Fed daily reference rates 2000 to 2026 (17,289 rows), with the Treasury par yield curve (9,198 days), Treasury auction results (11,143 auctions) and reverse repo operations (3,304) beside it

This is a clean real-data bundle only, like task112. No draw has been made and nothing is planted:
there is no ladder, stump sentence, calibration file, governing document or social layer, and no
fingerprint card is filed. The anomalies in it are the market's own (the September 2019 repo spike,
March 2020, quarter-ends and month-ends, the 2021 to 2023 reverse repo build-up, debt-ceiling bill
kinks) and the publishers' own artifacts (the December 2021 yield curve method change, suspended and
added tenors, rates published without percentiles, revisions).

`generator/build_pack.py` rebuilds `target/` from the publisher URLs and checks it.

Input gates as built: 10 files, five formats (csv, json, pdf, html, md), largest file 17,289 rows.

## Tried and rejected

- SEC fails-to-deliver and MIDAS market structure data: sec.gov returns 403 unless the request declares a contact email, and the author's email is not sent without asking.
- Treasury's all-years yield curve CSV: 403 from the Akamai edge. The per-year CSVs download, so they are stacked instead.
- FRED: the graph CSV endpoint timed out, and its series are re-publications of the Treasury and New York Fed sources already in the pack.
