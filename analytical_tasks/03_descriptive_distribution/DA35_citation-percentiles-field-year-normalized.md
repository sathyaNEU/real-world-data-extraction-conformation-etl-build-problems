# DA35 — "Top 10% papers": percentiles only mean something within field and year

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Creator- and seller-performance percentiles on platforms (normalising by category and age before comparing), sales-rep leaderboards across territories |
| Domain | Research analytics / funding |
| Task shape | 01 · Ranked list under a cap (8 institutions receiving a research-excellence grant, ranked by share of field-year top-10% publications) |
| Core method | For each publication, percentile rank of its citation count within its field (top-level concept/topic) and publication year; ties at the threshold split fractionally (Waltman–Schreiber); institution indicator = fractional share of papers in the top 10%; minimum output |
| Analytical stump | Raw citation counts favour fields with high citation density and older papers; a global top-10% pools biomedical papers with mathematics. Ties (many papers with the same low count, often zero) make naïve percentile thresholds assign "top 10%" to far more or fewer than 10% of papers |
| Primary sources | OpenAlex works snapshot (publications, citations, institutions, concepts/topics) |

## 1. The real-world situation

A national research council awards excellence grants to **8** universities based on the share of their publications among the most cited.
The analyst computed each university's share of papers in the global top 10% by citation count. Universities strong in mathematics and
humanities ranked low; medical schools dominated. Reviewers asked for field- and year-normalised percentiles.

## 2. The decision (one deterministic recommendation)

**The 8 institutions funded (highest PP(top 10%) among eligible institutions), and the 9th.**

Rules (council memo):

* Publications: OpenAlex works of type article, publication years 2016–2020, with at least one author affiliated to the 25 candidate
  institutions; citation counts as of the snapshot date.
* Field: the work's primary topic's field (OpenAlex topic hierarchy); each work belongs to one field.
* Reference sets: all OpenAlex articles in the same field and year (not only the candidates).
* Top-10% assignment with ties: within each field-year, sort by citations; a work above the threshold gets 1; works tied at the threshold get
  the fractional share needed so that exactly 10% of the reference set is assigned (Waltman–Schreiber).
* Institution counting: fractional by institution share of author affiliations (memo).
* Indicator PP(top 10%) = Σ (fractional top-10% × institution share) ÷ Σ institution share.
* Eligibility: ≥ 1,000 fractional papers. Rank; top 8; report #9.

## 3. Why capable analysts get it wrong

* Global citation thresholds are easy to compute.
* Citation practices differ by an order of magnitude between fields.
* Older papers have had more time to accumulate citations.
* Ties at low counts are massive in some fields; naïve "≥ threshold" rules mis-size the top set.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `openalex_works_2016_2020_articles.parquet` (extract) | Parquet | ~30M | OpenAlex snapshot (AWS open data) | CC0 | Works with year, topic, citation count |
| 2 | `openalex_work_authorships_candidates.parquet` | Parquet | ~5M | OpenAlex | CC0 | Authorships and institutions for candidates |
| 3 | `openalex_topics.csv` | CSV | ~4.5k | OpenAlex | CC0 | Topic → subfield → field |
| 4 | `candidate_institutions.csv` | CSV | 25 | Task author (ROR IDs) | — | Candidates |
| 5 | `council_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `analyst_global_top10.xlsx` | XLSX | 25 | Task author | — | Naive ranking |
| 7 | `waltman_schreiber_2013_citation.pdf` | PDF | — | Cite | Cite | Tie handling |
| 8 | `field_year_thresholds_check.json` | JSON | ~10 | Task author | — | Check values |
| 9 | `openalex_snapshot_manifest.json` | JSON | — | OpenAlex | CC0 | Snapshot date |

## 5. Deterministic solution path

1. Build field-year reference sets; sort by citations; assign fractional top-10% values with tie handling.
2. Attach candidate authorships; fractional institution shares.
3. PP(top 10%) per institution; eligibility; ranking.
4. Contrast with global top-10% ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — global threshold.** Field effects dominate.

**B — ignoring publication year.** Older papers favoured.

**C — ≥ threshold without tie splitting.** Top set size wrong.

**D — full counting of multi-institution papers.** Collaborative institutions inflated.

## 7. Why the stump is analytical, not semantic

The reference sets, tie rule and counting are specified. The trap is comparing skewed count distributions across heterogeneous groups.

## 8. Draft task prompt (prose)

> Which eight universities receive the excellence grants? Compute field- and year-normalised top-10% shares from OpenAlex following the
> council memo. Provide `institution_pp_top10.csv` (institution: fractional papers, PP(top 10%) normalised and global, rank),
> `normalised_vs_global.png`, and a one-page `grant_awards.pdf`.

## 9. Deliverables

* `institution_pp_top10.csv`, `normalised_vs_global.png`, `grant_awards.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 institutions + #9; PP values for 10 institutions; field-year thresholds for 5 cells; tie handling; contrast.

## 11. Golden-output checklist

* Reference sets; tie fractions; fractional counting; eligibility; ranking.

## 12. Build notes (scope tuning)

* Record the snapshot date; choose candidates with varied field profiles.
* Confirm at least three changes in the funded set versus the global method.
