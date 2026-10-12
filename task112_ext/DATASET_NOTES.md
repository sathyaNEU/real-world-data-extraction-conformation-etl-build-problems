# task112 dataset notes

- Domain: Economics
- Subdomain: Labor markets (wages and earnings distribution), with household income on the housing file
- Objective: Descriptive & Distribution Analysis
- Spine: 2023 ACS 1-year PUMS, Oregon, person file (43,935 rows) joined to the housing file (21,004 rows) on SERIALNO

This is a clean real-data bundle only. No draw has been made and nothing is planted: there is no
ladder, no stump sentence, no calibration file, no governing document and no social layer, and no
fingerprint card is filed. The spine is shipped exactly as the Census Bureau published it, so the
mess it carries (out-of-universe blanks, top coding, ADJINC, group quarters records) is the
publisher's own.

`generator/build_pack.py` rebuilds `target/` from the Census URLs and checks it against the
published verification estimates.

Input gates as built: 10 files, four formats (csv, pdf, txt, md), largest file 43,935 rows.

## Tried and rejected

- Census Data API for published PUMA-level B19013/B20002 tables: the API now refuses calls without a key. Used the PUMS verification estimates file as the published reference instead.
- BLS (OEWS, QCEW) as the spine: www.bls.gov returns 403 to scripted downloads.
