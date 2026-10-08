# P03 — Issuer-group concentration: rolling holdings up the LEI tree without climbing the wrong branches

| Field | Value |
|---|---|
| Domain | Asset management risk / regulatory reporting (BCBS 239-style risk data aggregation) |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 10 · Scorecard against thresholds (5/10/40 group-concentration test per fund) |
| Core technique | Graph roll-up over typed, time-bounded relationships; identifier fallback (ISIN→LEI); successor mapping |
| Trap family (honest data) | Treating "managed-by" as "owned-by"; treating LAPSED registrations as dead entities; ignoring successor LEIs |
| Primary sources | SEC Form N-PORT data sets; GLEIF Golden Copy (Level 1 + Level 2 + reporting exceptions); GLEIF ISIN–LEI mapping |

## 1. The real-world project

A fund family's risk team must certify each quarter that every fund respects the **issuer-group concentration
policy**: exposure to any single *ultimate parent group* ≤ 10% of net assets, and the sum of all groups individually
above 5% ≤ 40% of net assets (the familiar 5/10/40 structure, applied at group level). The data team builds the
group hierarchy from GLEIF Level 2 relationship data and joins it to the funds' public N-PORT holdings.

The first run flagged nine funds, including a short-term bond fund whose "largest group" was an asset manager the
fund never lent to. The second run, after someone "cleaned out lapsed LEIs", flagged none.

## 2. The business decision (one deterministic recommendation)

**Go / no-go: can the family certify compliance for the report period ending 2024-03-31? If no-go, which fund breaches
and through which ultimate-parent group, at what percentage of net assets?**

Policy rules (task folder):

* Group = the LEI reached by following `IS_ULTIMATELY_CONSOLIDATED_BY` (or, if absent, the transitive chain of
  `IS_DIRECTLY_CONSOLIDATED_BY`) using only relationships whose `RelationshipStatus = ACTIVE` and whose relationship
  period covers the as-of date. `IS_FUND-MANAGED_BY`, `IS_SUBFUND_OF`, `IS_FEEDER_TO` and
  `IS_INTERNATIONAL_BRANCH_OF` are **not** consolidation and are never followed (a branch is the same legal entity as
  its head office and inherits its head office's group).
* An LEI's `RegistrationStatus = LAPSED` means the registration was not renewed; the entity and its relationships remain
  valid for grouping. `RETIRED`/`MERGED` LEIs are mapped to their successor LEI if the successor event is effective on or
  before the as-of date.
* Reporting exceptions (`NATURAL_PERSONS`, `NON_CONSOLIDATING`, `NO_KNOWN_PERSON`, …) terminate the chain: the entity is
  its own group top.
* Holding identifier: `ISSUER_LEI` from N-PORT; if missing/invalid, ISIN → LEI via the GLEIF ISIN–LEI file; if still
  unresolved, the holding is its own singleton group keyed by issuer name + CUSIP.
* Exposure = long, non-derivative holdings' USD value (N-PORT Item C.2.4) ÷ fund net assets (Item B.1).

## 3. Why this gets overlooked in real projects

* Level 2 data looks like one "parent" table. The relationship *type* column is easy to ignore, and fund-management
  relationships are numerous because asset managers register every fund they run.
* "Lapsed" sounds like "inactive". In practice a large share of LEIs are lapsed simply because renewal fees were not
  paid; dropping them removes intermediate holding companies and breaks chains.
* Mergers create successor LEIs; N-PORT filers often keep reporting the predecessor's LEI for legacy bonds.
* Validations focus on referential integrity ("every parent LEI exists"), not semantic integrity ("this edge means
  ownership").

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–6 | `2024q1_nport/` `SUBMISSION.tsv`, `REGISTRANT.tsv`, `FUND_REPORTED_INFO.tsv`, `FUND_REPORTED_HOLDING.tsv`, `IDENTIFIERS.tsv`, `DEBT_SECURITY.tsv` | TSV | holdings ≈ several million | SEC Form N-PORT data sets (sec.gov/dera/data/form-n-port-data-sets) | U.S. Gov public domain | Holdings and net assets |
| 7 | `lei2_golden_copy_20240331.csv` (Level 1) | CSV | ~2.5M | GLEIF Golden Copy | CC0 1.0 | LEI status, successor LEIs |
| 8 | `rr_golden_copy_20240331.csv` (Level 2 relationships) | CSV | ~0.5M+ | GLEIF | CC0 1.0 | Relationship type/status/periods |
| 9 | `repex_golden_copy_20240331.csv` | CSV | ~2M | GLEIF | CC0 1.0 | Reporting exceptions |
| 10 | `isin_lei_20240331.csv` | CSV | ~7M | GLEIF ISIN-to-LEI relationship files | CC0 1.0 | Fallback identifier |
| 11 | `LEI-CDF_3.1_and_RR-CDF_2.1_format_docs.pdf` | PDF | — | GLEIF | CC0 | Field semantics |
| 12 | `nport_readme.pdf` | PDF | — | SEC | Public domain | Field semantics |
| 13 | `concentration_policy.pdf` | PDF | — | Task author (internal policy memo) | — | Rules in §2 |
| 14 | `fund_family_scope.json` | JSON | ~12 funds | Task author | — | Series IDs in scope |

## 5. Deterministic solution path

1. Select the family's series IDs; take the latest N-PORT submission per series for the 2024-03-31 period (amendments
   supersede).
2. Filter holdings: long payoff profile, non-derivative asset categories.
3. Resolve each holding to an LEI (N-PORT → ISIN map → singleton).
4. Map retired/merged LEIs to successors effective by the as-of date.
5. Build the consolidation graph from `IS_DIRECTLY_CONSOLIDATED_BY`/`IS_ULTIMATELY_CONSOLIDATED_BY` edges that are
   ACTIVE and in-period; ignore all other types; keep LAPSED LEIs; stop at reporting exceptions; resolve branches to
   head office.
6. Aggregate exposure per fund per group; compute max-group % and the 5/40 sum.
7. Scorecard: pass/fail for both tests per fund; family go/no-go.

## 6. The traps

**Trap A — climbing management edges.** Following `IS_FUND-MANAGED_BY` rolls money-market and ETF holdings up to the
asset manager, manufacturing a breach in funds that hold many vehicles from one sponsor.

**Trap B — dropping LAPSED.** Removes intermediate holdcos; a bank's operating subsidiary and its funding vehicle end up
in different "groups", hiding the true breach in the flagship fund.

**Trap C — ignoring successors.** Legacy bonds of a merged issuer stay in a separate group; the combined group's
exposure is understated.

**Trap D — LEI-only matching.** Holdings without `ISSUER_LEI` become singletons although the ISIN map resolves them.

## 7. Why the data is honest

GLEIF data is exactly what registrants and LOUs published; N-PORT is exactly what the funds filed. Relationship types,
statuses and successor events are explicit, documented fields. The difficulty is graph semantics, not bad data.

## 8. Draft task prompt (prose)

> Risk needs to know whether we can certify the issuer-group concentration policy for the quarter ending 31 March
> 2024. Using the N-PORT holdings, the GLEIF files and the policy memo in the folder, roll every holding of the twelve
> funds in scope up to its ultimate parent group and run the 10% single-group and 40% aggregate tests. Produce
> `group_concentration_scorecard.xlsx` with one sheet showing every fund's largest group, its percentage, the sum of
> groups above 5%, and pass/fail on each test, and a second sheet listing each fund's top five groups with the LEIs that
> roll into them. Add `concentration_heatmap.png`: funds against their top groups, shaded by percentage of net assets,
> with the 10% limit made obvious. In a short note at the top of the workbook, give the certification decision, the
> breaching fund and group if there is one, and how far the next-closest fund sits from its limit.

## 9. Deliverables

* `group_concentration_scorecard.xlsx` (2 sheets + decision note).
* `concentration_heatmap.png`.

## 10. Where 25+ rubric criteria come from

* 12 funds × 2 tests = 24 pass/fail cells; max-group % for the breaching fund and runner-up.
* Correct group identity for 3–4 tricky issuers (lapsed holdco, merged predecessor, branch, fund-managed vehicle).
* Go/no-go and margin to limit for the next-closest fund.

## 11. Golden-output checklist

* Only consolidation edges followed; LAPSED retained; successors applied; ISIN fallback used.
* Decision stated with the breaching fund/group % (or certification if none).

## 12. Build notes (scope tuning)

* Pick a family with a bond fund holding many debt issuers from one banking or auto-finance group whose chain runs
  through a LAPSED intermediate LEI (verify in Level 2 data), and a fund holding many money-market/ETF vehicles from one
  sponsor (to trigger Trap A).
* Confirm the as-of Level 2 snapshot date matches the report period; GLEIF publishes golden copies three times daily —
  record the exact file timestamp.
