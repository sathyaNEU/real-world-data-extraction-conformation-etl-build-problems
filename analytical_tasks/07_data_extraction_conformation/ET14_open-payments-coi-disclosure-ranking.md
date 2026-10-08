# ET14 — Conflict-of-interest review from Open Payments: whose money is it, and which publication is current?

| Field | Value |
|---|---|
| Domain | Academic medicine compliance / research integrity |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (15 committee review slots) |
| Core technique | Role-aware attribution (recipient vs principal investigator vs third party); publication supersession (initial vs refresh); identifier-based entity matching (NPI → profile ID) |
| Trap family (honest data) | Institutional research funding attributed to PIs; initial + refreshed publications unioned; name-based matching |
| Primary sources | CMS Open Payments (General, Research, Ownership files; Covered Recipient profile supplement); NPPES |

## 1. The real-world project

An academic medical center's COI office reviews physicians whose **personal** payments from a single manufacturer
exceed the $5,000 significant-financial-interest threshold used in its PHS-compliant policy. The committee can take 15
cases per cycle, highest single-manufacturer totals first. An analyst built the list from Open Payments and sent letters.
Three recipients replied that the money went to the university's research office; another showed that his total had
been counted twice.

## 2. The business decision (one deterministic recommendation)

**Which 15 physician–manufacturer pairs go to the committee for program year 2023, and which pair is 16th?**

Rules (COI office procedure):

* Roster: Type-1 NPIs whose NPPES primary practice location matches the center's campus addresses (list in folder),
  linked to Open Payments by NPI, or by `Covered_Recipient_Profile_ID` via the profile supplement when NPI is blank.
* Use only the **latest publication** of PY2023 (the refresh in the folder supersedes the initial publication; records
  not present in the refresh are treated as removed).
* Personal payments = General Payments to the physician as covered recipient, where
  `Third_Party_Payment_Recipient_Indicator` is "No Third Party Payment", or a third party with
  `Third_Party_Equals_Covered_Recipient_Indicator = Yes`; plus Research Payments where the physician is the **covered
  recipient** of the payment. Research payments made to a teaching hospital or non-covered entity that list the
  physician as a principal investigator are **not** personal.
* Ownership/investment interests are a separate disclosure and not summed.
* Aggregate by physician × paying manufacturer (`Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID`); keep
  pairs > $5,000; rank descending.

## 3. Why this gets overlooked in real projects

* The Research file lists up to five PIs per record. Joining the roster to *any* PI column attributes the full institutional
  payment to each listed investigator — the biggest numbers in the file, all wrong for a personal threshold.
* CMS republishes each program year after the dispute/correction cycle. Teams append the refresh to the initial load;
  `Record_ID`s repeat and totals double.
* NPIs are blank on some records; name matching then merges common names across specialties.
* Third-party indicators look like metadata and are dropped.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `OP_DTL_GNRL_PGY2023_P06xx2024.csv` (initial) | CSV | ~14M | CMS Open Payments | U.S. Gov public domain | General payments (initial) |
| 2 | `OP_DTL_GNRL_PGY2023_P01xx2025.csv` (refresh) | CSV | ~14M | CMS Open Payments | Public domain | General payments (current) |
| 3 | `OP_DTL_RSRCH_PGY2023_P01xx2025.csv` | CSV | ~0.7M | CMS | Public domain | Research payments |
| 4 | `OP_DTL_OWNRSHP_PGY2023_P01xx2025.csv` | CSV | ~4k | CMS | Public domain | Ownership interests |
| 5 | `OP_CVRD_RCPNT_PRFL_SPLMTL.csv` | CSV | ~1.5M | CMS | Public domain | Profile ID ↔ NPI |
| 6 | `OP_REMOVED_DELETED_PGY2023.csv` (if published) | CSV | small | CMS | Public domain | Removed records |
| 7 | `open_payments_methodology_data_dictionary.pdf` | PDF | — | CMS | Public domain | Field semantics |
| 8 | `npidata_pfile_YYYYMMDD.csv` (state extract) | CSV | ~0.5M | CMS NPPES | Public domain | Practice locations |
| 9 | `campus_addresses.json` | JSON | ~10 | Task author | — | Roster definition |
| 10 | `coi_procedure.pdf` | PDF | — | Task author (mirrors 42 CFR 50.603 threshold) | — | Rules in §2 |
| 11 | `manufacturer_profile.xlsx` | XLSX | ~2k | CMS Open Payments (reporting entity profiles) | Public domain | Manufacturer IDs/names |

## 5. Deterministic solution path

1. Build the roster from NPPES; map to profile IDs.
2. Load only the refresh publication; confirm removed records are absent.
3. Select personal general payments by third-party rules; select research payments where the roster physician is the
   covered recipient.
4. Aggregate by physician × manufacturer; threshold; rank; top 15 + 16th.
5. Quantify what the PI-attribution and unioned-publication variants would have done.

## 6. The traps

**Trap A — PI attribution.** Multi-site trial payments to the hospital appear as six-figure "personal" totals; they fill
most of the 15 slots.

**Trap B — initial + refresh union.** Every refreshed record counts twice; pairs near $5,000 cross the threshold, the
ranking reshuffles.

**Trap C — initial publication only.** Misses corrections and disputed-then-resolved changes; at least one pair changes.

**Trap D — name matching.** Merges two physicians with the same name.

**Trap E — third-party payments.** Payments directed to a practice or charity counted as personal.

## 7. Why the data is honest

Open Payments publishes exactly what manufacturers reported, with explicit role and third-party fields and a documented
refresh cycle. Research payments to institutions legitimately list PIs. Nothing is planted.

## 8. Draft task prompt (prose)

> The COI committee can review fifteen physician–manufacturer relationships this cycle: the largest personal payments
> above $5,000 from a single manufacturer in program year 2023, under our procedure. Using the Open Payments files, the
> NPPES extract and the campus address list in the folder, give me the fifteen and the relationship that just misses.
> Produce `coi_review_list.csv` with every qualifying pair (physician NPI, name, manufacturer, general and research
> personal amounts, total, rank). Create `coi_review_chart.png`, ranked bars for the top twenty-five pairs with the cut
> after fifteen. And write `coi_memo.docx`, one page that leads with the list, notes the gap between fifteenth and
> sixteenth, and states how many of the fifteen would have been different if institutional research payments listing the
> physician as investigator had been counted.

## 9. Deliverables

* `coi_review_list.csv`, `coi_review_chart.png`, `coi_memo.docx`.

## 10. Where 25+ rubric criteria come from

* 15 pairs + 16th + gap; component amounts for 5 pairs; PI-attribution variant count; roster size; excluded third-party
  amount.

## 11. Golden-output checklist

* Latest publication only; role-correct research attribution; third-party rules; NPI/profile matching; decision stated.

## 12. Build notes (scope tuning)

* Choose a large academic center (many research payments listing faculty PIs) and confirm the PI-attribution variant
  replaces ≥ 5 of the 15.
* Verify file names and the refresh date on the Open Payments site; record both publication dates.
