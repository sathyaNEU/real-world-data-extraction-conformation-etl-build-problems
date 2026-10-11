# task445: start here

| | |
|---|---|
| Task | task445 |
| Objective (Axis 1) | Data Extraction & Conformation (ETL) |
| Block | task445 to task493 |
| Lane owner | unassigned (current owner and status: the root `START_HERE.md` on main) |
| Seed | ET02, `analytical_tasks/07_data_extraction_conformation/ET02_sec-13f-institutional-ownership-bridge.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task445`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task445-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** 13F institutional ownership: the quarter the units changed and the amendments that only add
- **objective:** Data Extraction & Conformation (ETL / Pipeline Build)
- **domain:** Asset management / market-data product (ownership analytics)
- **decision_shape:** 03 · Bridge between two totals (raw 13F sum → conformed ownership)
- **committed_call:** For the 12 issuers on the client watchlist, which ones should carry the "crowded" flag for the 2022-12-31 report period, and who is each flagged issuer's largest holder by market value?
- **technique:** Amendment-type-aware supersession; filing-date-driven unit conformance; option-row exclusion; CUSIP normalization
- **trap:** Mixed value units inside one report period; RESTATEMENT vs NEW HOLDINGS semantics
- **sources:** SEC Form 13F Data Sets; SEC Financial Statement Data Sets (cover-page shares outstanding)

## Seed note

## ET02, 13F institutional ownership: the quarter the units changed and the amendments that only add

| Field | Value |
|---|---|
| Domain | Asset management / market-data product (ownership analytics) |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 03 · Bridge between two totals (raw 13F sum → conformed ownership) |
| Core technique | Amendment-type-aware supersession; filing-date-driven unit conformance; option-row exclusion; CUSIP normalization |
| Trap family (honest data) | Mixed value units inside one report period; RESTATEMENT vs NEW HOLDINGS semantics |
| Primary sources | SEC Form 13F Data Sets; SEC Financial Statement Data Sets (cover-page shares outstanding) |

### 1. The real-world project

An ownership-analytics team publishes quarterly "institutional ownership %" and "top holders" for every U.S. listed
issuer, built from the SEC's structured Form 13F data sets (`SUBMISSION`, `COVERPAGE`, `SUMMARYPAGE`, `INFOTABLE`,
`OTHERMANAGER`, `OTHERMANAGER2`, `SIGNATURE`). Clients use a **"crowded" flag** (institutional ownership above 80% of
shares outstanding) to size positions.

In early 2023 the flag fired on several issuers at once and the top-holder league tables reshuffled. The pipeline had
not changed. The filings had.

### 2. The business decision (one deterministic recommendation)

**For the 12 issuers on the client watchlist, which ones should carry the "crowded" flag for the 2022-12-31 report
period, and who is each flagged issuer's largest holder by market value?** The recommendation is the flag list; the
headline figure is the conformed institutional ownership % of the issuer closest to the 80% line.

Rules fixed in the methodology note:

* Holdings = `INFOTABLE` rows with `SSHPRNAMTTYPE = SH` and empty `PUTCALL`. Option rows are exposure, not ownership.
* Per `(filer CIK, report period)`: start from the original `13F HOLDINGS REPORT`/`13F COMBINATION REPORT`; an
  amendment with `AMENDMENTTYPE = RESTATEMENT` **replaces** everything filed before it; an amendment with
  `AMENDMENTTYPE = NEW HOLDINGS` **adds** its rows to the current state. Apply in `FILING_DATE` order using data visible
  by the cut-off (2023-03-31).
* `VALUE` is in **thousands of dollars for filings submitted before 2023-01-03** and in **dollars for filings submitted
  on or after 2023-01-03** (Form 13F amendments adopted 2022). The unit follows the *filing date*, not the report
  period, an amendment to 2022-09-30 filed in February 2023 is in dollars.
* CUSIP normalized to 9 characters (upper-case, left-pad zeros), validated with the CUSIP check digit; rows that fail
  validation are matched on issuer name + title of class only if exactly one valid CUSIP candidate exists.
* Shares outstanding = `dei:EntityCommonStockSharesOutstanding` from the issuer's most recent 10-K/10-Q cover page
  accepted on or before 2023-02-14 (FSDS `num.txt`). Multi-class issuers: sum classes that share the watchlist CUSIP's
  economic class only.

### 3. Why this gets overlooked in real projects

* Pipelines are written once against a schema, and the schema did not change in 2023, only the meaning of `VALUE`.
  Row counts, nulls and types all pass.
* Amendment handling is usually "keep latest accession per filer-period". That is right for restatements and silently
  wrong for NEW HOLDINGS amendments, which contain only the *added* positions (often previously confidential ones).
* Option rows look like holdings (same CUSIP, share count populated) and large market makers report huge put/call
  notionals.
* CUSIPs in INFOTABLE are entered by filers; dropped leading zeros and lower-case letters are common and harmless to the
  filer but break exact joins.

### 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–7 | `2022q4_form13f/` `SUBMISSION.tsv`, `COVERPAGE.tsv`, `SUMMARYPAGE.tsv`, `INFOTABLE.tsv`, `OTHERMANAGER.tsv`, `OTHERMANAGER2.tsv`, `SIGNATURE.tsv` | TSV | INFOTABLE ≈ 2–3M | SEC Form 13F data sets (sec.gov/dera/data/form-13f) | U.S. Gov public domain | Q4 2022 period filings |
| 8–14 | `2023q1_form13f/` same 7 files | TSV | INFOTABLE ≈ 2–3M | same | same | Filings *submitted* in Q1 2023 (amendments, late filers) |
| 15 | `FORM13F_metadata.json` / readme | JSON/HTML |, | SEC | Public domain | Column definitions |
| 16 | `13f_faq_extract.pdf` | PDF |, | SEC Division of Investment Management FAQ | Public domain | Unit change + amendment types |
| 17 | `2023q1_fsds/num.txt`, `sub.txt` | TSV | ~3M | SEC FSDS | Public domain | Shares outstanding |
| 18 | `watchlist.xlsx` | XLSX | 12 | Task author |, | Issuers, CUSIPs, share classes |

### 5. Deterministic solution path

1. Union the two quarterly 13F drops; filter `REPORTCALENDARORQUARTER = 31-DEC-2022` (and `30-SEP-2022` for the prior
   period); drop `13F NOTICE` filings.
2. Order each filer-period's accessions by filing date; build current state by applying RESTATEMENT (replace) and NEW
   HOLDINGS (append) amendments.
3. Convert `VALUE` to dollars by **each accession's** filing date.
4. Normalize CUSIPs; validate check digit; repair per rule.
5. Filter `SH`, empty `PUTCALL`.
6. Aggregate shares and dollar value by issuer CUSIP and filer; compute IO% against cover-page shares outstanding.
7. Flag > 80%; rank holders by dollar value.
8. Build the bridge for each flagged issuer: raw sum of all rows → minus option rows → minus superseded originals →
   plus NEW HOLDINGS rows dropped by "latest only" logic → plus repaired CUSIPs → conformed total.

### 6. The traps

**Trap A, period-based unit conversion.** Multiplying every 2022-period row by 1,000 (or none) mixes units for
amendments filed after 2023-01-03; one large filer's restated value becomes 1,000× too large or too small and takes
over the top-holder rank.

**Trap B, "latest accession wins".** Treats a NEW HOLDINGS amendment as the complete report; the filer's entire
original book disappears and IO% drops below 80% for an issuer that should be flagged.

**Trap C, "sum everything".** Counts originals and restatements together; IO% for widely held issuers jumps above 80%.

**Trap D, options as holdings.** Adds put/call underlying shares; market-maker 13Fs push heavily optioned names over
the line.

**Trap E, exact-match CUSIP join.** Silently drops rows with formatting differences, undercounting.

### 7. Why the data is honest

Every filing is reported exactly as the rules required at the time it was filed; the unit change is regulatory and
documented, and amendment types are explicit fields. Nothing is planted, the work is applying the documented semantics.

### 8. Draft task prompt (prose)

> Clients rely on our "crowded" flag, which fires when institutional ownership in the 13F filings exceeds 80% of shares
> outstanding. Using the 13F data sets and filings in the folder, decide which of the twelve watchlist issuers carry the
> flag for the 31 December 2022 report period, and name each flagged issuer's largest holder by market value. Build
> `io_flags_2022q4.csv` with one row per issuer: conformed 13F shares, shares outstanding and its source filing, IO% for
> both 30 Sep and 31 Dec 2022, the flag, and the top holder with its dollar value. Then create `io_bridge.png`, a
> waterfall for the issuer closest to the 80% line that walks from a straight sum of every information-table row to the
> conformed total, one bar per reconciling item, with the 80% line drawn. Close with a short `io_memo.docx` that states
> the flag list, the issuer nearest the line and its IO%, and which reconciling item would flip that issuer's flag on
> its own.

### 9. Deliverables

* `io_flags_2022q4.csv`, 12 rows, fixed column set.
* `io_bridge.png`, waterfall with 80% threshold.
* `io_memo.docx`, 1 page.

### 10. Where 25+ rubric criteria come from

* 12 flag decisions; IO% for 4–5 issuers near the line in both periods.
* Top holder (name + value) for each flagged issuer.
* Each bridge bar (options, superseded originals, new-holdings adds, CUSIP repairs, unit conformance) with magnitude.
* Identification of the single item that flips the marginal issuer.

### 11. Golden-output checklist

* Units converted by filing date; amendments applied by type; options excluded; CUSIPs repaired.
* Flag list and marginal issuer IO% stated; bridge reconciles to the conformed total exactly.

### 12. Build notes (scope tuning)

* Choose watchlist issuers where (a) at least one top-25 holder filed a NEW HOLDINGS amendment and (b) at least one
  large holder filed a RESTATEMENT after 2023-01-03 for the 2022-09-30 or 2022-12-31 period. Query `COVERPAGE` for
  `ISAMENDMENT = Y` grouped by `AMENDMENTTYPE` and filing date.
* Include 2 issuers within ±3 points of 80% so that Traps B–D each flip at least one flag.
* Confirm the unit rule wording against the current SEC 13F FAQ before freezing the prompt.
