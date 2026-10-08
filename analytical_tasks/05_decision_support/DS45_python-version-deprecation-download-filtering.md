# DS45 — Can we drop support for an old Python version? Mirrors and CI bots download the most

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Deprecating old OS, app or API versions based on telemetry (Apple/Google minimum OS versions, SaaS API version sunsets) where automated traffic distorts usage shares |
| Domain | Open-source software / developer platforms |
| Task shape | 10 · Scorecard against thresholds (Python minor versions × usage filters → share of human-driven installs of the library; the deprecation call for the next major release) |
| Core method | Filter download records to likely human installs: exclude mirror/proxy installers (bandersnatch, devpi, etc.), CI environments (CI flag per details field), and one-off bursts; compute shares by Python minor version over the last 90 days; deprecate a version if its filtered share < 5% and declining for 3 consecutive months |
| Analytical stump | Raw download counts are dominated by CI pipelines and mirrors that re-download on every run, often on pinned old interpreters (or the newest); version shares from raw counts misstate the user base. Deprecation must be judged on filtered, human-like installs and on trends |
| Primary sources | PyPI download statistics (BigQuery public dataset `bigquery-public-data.pypi.file_downloads`) |

## 1. The real-world situation

A popular Python library plans its next major release. The maintainers' dashboard (raw downloads) shows Python 3.8 at 14% of downloads, so they
planned to keep supporting it. A contributor argued that most of those downloads come from CI systems pinned to 3.8 in a few large organisations.

## 2. The decision (one deterministic recommendation)

**Drop or keep Python 3.8 (and 3.9) in the next major release, based on filtered human-install shares and trends, with the share table by
version.**

Rules (maintainers' memo):

* Data: PyPI file_downloads for the project in memo, last 6 months.
* Exclusions: installer names in the mirror list (bandersnatch, z3c.pypimirror, devpi, artifactory, nexus per memo); `details.ci` = true;
  downloads with unknown Python version; bursts: > 1,000 downloads per (country, installer version) per hour removed.
* Shares: filtered downloads by `details.python` minor version per month.
* Rule: deprecate a version if last-90-day filtered share < 5% and monthly share declined in each of the last 3 months.
* Report raw shares for contrast.

## 3. Why capable analysts get it wrong

* Download counts are the readily available usage metric.
* Automated traffic dominates popular packages.
* CI pinned versions persist long after users move.
* Trends matter as much as levels for deprecation.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `pypi_downloads_<project>_6m.parquet` (query export) | Parquet | ~50–200M downloads (aggregated to ~1M rows) | BigQuery public dataset (PyPI file_downloads) | PyPI public data via Google BigQuery public datasets (verify terms) | Downloads with installer, Python version, CI flag |
| 2 | `pypi_bigquery_schema.json` | JSON | — | PyPI/linehaul docs | Public | Field definitions |
| 3 | `mirror_installers.json` | JSON | ~10 | Task author | — | Exclusion list |
| 4 | `maintainers_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `raw_dashboard_shares.xlsx` | XLSX | — | Task author | — | Raw shares |
| 6 | `bigquery_export_sql.sql` | SQL | — | Task author | — | Reproducible extraction query |
| 7 | `python_eol_dates.json` | JSON | ~10 | python.org release schedule | PSF (public) | Context |

## 5. Deterministic solution path

1. Run/export the query; apply exclusions; burst filter.
2. Monthly shares by version (raw and filtered).
3. Apply the rule for 3.8 and 3.9; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — raw downloads.** Automated traffic dominates.

**B — excluding CI but not mirrors.** Mirror re-downloads remain.

**C — level-only rule.** Ignores trend requirement.

**D — counting downloads with unknown Python version as old.** Bias; memo excludes unknowns.

## 7. Why the stump is analytical, not semantic

Filters and the rule are specified. The trap is measuring user base with automation-dominated telemetry.

## 8. Draft task prompt (prose)

> Should the next major release drop Python 3.8 and 3.9? Filter PyPI downloads to human-like installs and apply the deprecation rule in the
> maintainers' memo. Provide `version_shares.csv` (month × version: raw and filtered shares), `share_trends.png`, and a one-page
> `deprecation_decision.pdf`.

## 9. Deliverables

* `version_shares.csv`, `share_trends.png`, `deprecation_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 months × 5 versions filtered shares = 30; exclusion counts; decisions for 3.8 and 3.9; raw contrast.

## 11. Golden-output checklist

* Exclusion list; CI flag; burst filter; monthly shares; rule application.

## 12. Build notes (scope tuning)

* Choose a project where raw 3.8 share > 10% but filtered < 5%.
