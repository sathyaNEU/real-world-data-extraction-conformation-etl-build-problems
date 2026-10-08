# P05 — Mortgage market share across the 2018 HMDA overhaul: purchased loans and the two-part lender key

| Field | Value |
|---|---|
| Domain | Mortgage lending / fair-lending compliance / market intelligence |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (top lenders by originations) |
| Core technique | Multi-year schema conformance with key migration (respondent ID + agency → LEI); transaction-type filtering to avoid double counting |
| Trap family (honest data) | Unique identifier is n+1 columns, not n; purchased loans counted twice in the market |
| Primary sources | FFIEC/CFPB HMDA public loan-level data, Transmittal Sheet, Reporter Panel, ARID-to-LEI crosswalk |

## 1. The real-world project

A mid-size lender's market-intelligence team maintains a five-year view of home-purchase lending share in its
footprint MSAs (2016–2022) for strategy and for CRA/fair-lending peer comparisons. HMDA was overhauled for 2018: new
fields, LEI-based identifiers, new loan-purpose codes. The team stitched pre-2018 and post-2018 files and produced
a lender league table that the CRA officer then used to choose a peer group.

Two lenders appeared where none existed; one lender's share doubled in a year with no new branches.

## 2. The business decision (one deterministic recommendation)

**Which ten lenders form the CRA peer group for MSA X (the top ten by count of first-lien, owner-occupied home-purchase
originations summed over 2016–2022), and which lender is the first one left out?**

Rules (peer-group standard):

* Count only `action_taken = 1` (loan originated). `action_taken = 6` (purchased loan) is excluded — the same loan was
  already reported by its originator.
* Home purchase: pre-2018 `loan_purpose = 1`; 2018+ `loan_purpose = 1`. First lien (`lien_status = 1`), owner-occupied
  principal residence (pre-2018 `owner_occupancy = 1`; 2018+ `occupancy_type = 1`).
* Pre-2018 lender identity = **`respondent_id` + `agency_code`** (the same 10-character respondent ID can belong to
  different institutions under different agencies). 2018+ identity = LEI. Link the two eras with the FFIEC ARID-to-LEI
  crosswalk (ARID = agency code + respondent ID).
* Roll up to the parent named in the Reporter Panel/Transmittal Sheet only where the standard says so (here: no
  roll-up; peer group is at the reporting-institution level).
* Geography: MSA/MD code as reported in each year's file (MSA delineations changed in 2018 — use the 2018+ delineation
  for all years via the county FIPS of each record).

## 3. Why this gets overlooked in real projects

* `respondent_id` *looks* like a primary key — it is a 10-character code and mostly unique. Collisions across agency codes
  are rare enough to pass a casual uniqueness check on a sample, common enough to merge two unrelated lenders in a large
  MSA.
* Purchased loans are real HMDA records, so "count all records with a loan amount" feels complete; in markets with
  big aggregators the double counting is material.
* After 2018 the identifiers change entirely, so analysts match lenders by *name*, which merges affiliates and splits
  renamed institutions.
* MSA codes changed with OMB delineation updates; using each year's reported MSA moves counties in and out of the
  market.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–2 | `hmda_2016_lar.csv`, `hmda_2017_lar.csv` (state extract) | CSV | ~0.5–2M each (state) | CFPB HMDA historic data | U.S. Gov public domain | Pre-2018 LAR |
| 3–7 | `hmda_2018_lar.csv` … `hmda_2022_lar.csv` (state extract, snapshot) | CSV | ~0.5–2M each | FFIEC HMDA Data Browser / snapshot | Public domain | Post-2018 LAR |
| 8 | `arid2017_to_lei_xref.csv` | CSV | ~6k | FFIEC | Public domain | Key crosswalk |
| 9 | `hmda_2017_panel.csv`, `hmda_2022_panel.csv` (Reporter Panel) | CSV | ~7k each | FFIEC | Public domain | Institution names, parents |
| 10 | `ts_2022.csv` (Transmittal Sheet) | CSV | ~4.5k | FFIEC | Public domain | LEI ↔ name |
| 11 | `omb_delineation_2018.xlsx` | XLSX | ~1.9k counties | Census/OMB | Public domain | County → CBSA |
| 12 | `hmda_filing_instructions_guide_2018.pdf`, `hmda_2017_lar_formatting.pdf` | PDF | — | CFPB/FFIEC | Public domain | Code definitions |
| 13 | `cra_peer_group_standard.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Harmonize fields across eras (purpose, lien, occupancy, action taken); map counties to the 2018 CBSA definition and
   keep the target MSA.
2. Build pre-2018 lender key = `agency_code` + `respondent_id`; map to LEI through the ARID crosswalk; unmatched ARIDs
   (institutions that stopped reporting before 2018) keep their ARID as identity.
3. Filter originations only; apply loan filters.
4. Count by lender identity across 2016–2022; rank; cut at 10; report #11 and the gap.
5. Produce the comparison: rank under (a) respondent-ID-only key, (b) including purchased loans — to show sensitivity.

## 6. The traps

**Trap A — n-column key.** Keying pre-2018 lenders on `respondent_id` alone merges two institutions; the merged entity
enters the top ten.

**Trap B — purchased loans.** Including `action_taken = 6` lifts aggregators/correspondent buyers into the peer group
and pushes a genuine originator to #11.

**Trap C — name matching across 2018.** Splits a renamed lender into two half-sized entities that both fall out.

**Trap D — per-year MSA codes.** Counties added to the MSA in the 2018 delineation are missing from 2016–2017.

## 7. Why the data is honest

HMDA records are exactly as reported. Purchased-loan reporting is mandated; the composite pre-2018 key is documented in
the LAR formatting guide. The challenge is applying documented semantics consistently across the overhaul.

## 8. Draft task prompt (prose)

> Our CRA officer needs the peer group for MSA X: the ten institutions with the most first-lien, owner-occupied
> home-purchase originations from 2016 through 2022, under our peer-group standard. Using the HMDA files and crosswalks
> in the folder, tell me the ten peers and who just missed. Produce `peer_group.csv` listing every lender with at least
> 500 qualifying originations: identity used (LEI or agency+respondent ID), name, yearly counts, total and rank. Create
> `peer_rank_chart.png`, a ranked horizontal bar chart of the top fifteen with the cut line after ten and the totals
> labelled. In a one-page `peer_group_memo.docx`, give the peer group, the margin between #10 and #11, and say what the
> list would look like — which names enter and leave — if purchased loans had been counted.

## 9. Deliverables

* `peer_group.csv`, `peer_rank_chart.png`, `peer_group_memo.docx`.

## 10. Where 25+ rubric criteria come from

* 10 peers + #11 + gap; 7 yearly counts for 2–3 named lenders (checks key and era stitching).
* Entrants/leavers under the purchased-loan variant.
* Correct separation of the two institutions sharing a respondent ID.

## 11. Golden-output checklist

* Composite pre-2018 key; ARID→LEI mapping; originations only; 2018 delineation applied to all years.

## 12. Build notes (scope tuning)

* Find an MSA where a respondent-ID collision across agency codes exists among active lenders (group 2016–2017 LARs by
  `respondent_id` and count distinct `agency_code`), and where a large correspondent aggregator buys many loans.
* Verify the ARID crosswalk covers the colliding IDs and that both traps change the ten-name list.
