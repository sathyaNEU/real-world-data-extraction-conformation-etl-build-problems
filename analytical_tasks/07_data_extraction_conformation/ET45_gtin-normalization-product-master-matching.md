# ET45 — Merging two food product catalogs on barcodes: leading zeros, UPC-E, check digits and in-store codes

| Field | Value |
|---|---|
| Domain | CPG / grocery retail / nutrition data products / product master data management |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 15 · Fields conformed to one schema (the adopted barcode matching rule is the answer) |
| Core technique | GTIN normalization (GTIN-8/12/13/14 → GTIN-14), UPC-E expansion, check-digit validation, exclusion of restricted-circulation prefixes; per-field survivorship and unit normalization |
| Trap family (honest data) | Barcodes cast to integers; naive left-padding of UPC-E; restricted-circulation (variable-weight/in-store) numbers treated as global identifiers |
| Primary sources | USDA FoodData Central (Branded Foods), Open Food Facts product database, GS1 General Specifications (prefix and check-digit rules) |

## 1. The real-world project

A nutrition-app company builds a **product master** by merging USDA FoodData Central's Branded Foods with Open Food Facts,
keyed on barcodes. The first merge matched 61% of U.S. products; a later "fix" that cast barcodes to integers raised the rate
to 78% — and users began seeing deli-counter cheese nutrition on a bag of apples.

## 2. The business decision (one deterministic recommendation)

**Which matching rule becomes the product-master key, and what does the conformed master contain?**

Candidate rules (in the folder):

* **R1** exact string equality of the raw barcode fields.
* **R2** integer cast of both fields, then equality.
* **R3** GTIN-14 normalization (strip non-digits, left-pad to 14) + check-digit validation; invalid codes unmatched.
* **R4** R3 + UPC-E (8-digit, number system 0/1) expanded to UPC-A before padding + restricted-circulation numbers excluded
  (GTIN-13 prefixes 020–029, 040–049, 200–299; UPC-A number systems 2 and 4; coupon/ISSN/ISBN prefixes as listed in GS1
  specs).
* **R5** R4 + fuzzy brand/name fallback for unmatched codes.

Adoption criterion (data-governance standard): choose the rule with the **highest recall subject to precision ≥ 99.0%** on
the steward-adjudicated audit sample (400 candidate pairs, labelled match/non-match by manual package verification).

Target schema (each field with mandated source/transformation): `gtin14`, `product_name` (FDC description if present, else
OFF), `brand` (FDC brand_owner/brand_name, else OFF brands), `package_size_g_or_ml` (parsed and converted from both sources;
oz→g ×28.3495, fl oz→ml ×29.5735), `serving_size_g`, `energy_kcal_100g`, `sugars_g_100g`, `sodium_mg_100g` (FDC per-100 g
values; OFF only if FDC missing; sodium from salt × 400 if only salt present), `category` (FDC branded_food_category),
`source_priority`, `match_rule`.

## 3. Why this gets overlooked in real projects

* Barcodes look numeric; CSV readers infer integers and drop leading zeros, so 12-, 13- and 14-digit encodings of the same
  product stop agreeing — and integer equality then "fixes" it while also merging unrelated codes.
* UPC-E codes are compressed UPC-A codes; padding them to 14 digits creates a different (often valid-looking) GTIN.
* Variable-measure and in-store codes (e.g. prefixes 02x/2xx) are reused across retailers for different products; they match
  frequently and wrongly.
* Precision is rarely measured; match rate is.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `branded_food.csv` | CSV | ~0.4–2M | USDA FoodData Central (Branded Foods download) | CC0 1.0 | Barcodes, brand, category, serving |
| 2 | `food.csv` | CSV | ~2M | USDA FDC | CC0 1.0 | Descriptions, data type |
| 3 | `food_nutrient.csv` (branded subset) | CSV | ~20M+ | USDA FDC | CC0 1.0 | Nutrients |
| 4 | `nutrient.csv` | CSV | ~500 | USDA FDC | CC0 1.0 | Nutrient IDs/units |
| 5 | `en.openfoodfacts.org.products.csv` (US subset) | TSV | ~0.5M (US) | Open Food Facts | ODbL 1.0 (database) / DbCL (contents) | Barcodes, quantities, nutriments |
| 6 | `openfoodfacts_products_us.jsonl` (sample) | JSONL | ~50k | Open Food Facts | ODbL 1.0 | Same, JSON |
| 7 | `gs1_general_specifications_prefix_tables.pdf` | PDF | — | GS1 (public specification) | GS1 terms (free download; verify reuse) | Prefix ranges, check digits, UPC-E |
| 8 | `fdc_download_documentation.pdf` | PDF | — | USDA | Public domain | Field definitions |
| 9 | `audit_sample_400.csv` | CSV | 400 | Task author (manually adjudicated) | — | Precision/recall evaluation |
| 10 | `governance_standard.pdf` | PDF | — | Task author | — | Rules, schema |

## 5. Deterministic solution path

1. Implement R1–R5 over both catalogs; evaluate each on the audit sample (precision, recall).
2. Adopt the highest-recall rule with precision ≥ 99.0% (expected R4 unless the data show otherwise).
3. Build the master under the adopted rule with field-level survivorship and conversions.
4. Report coverage, conflicts, and fields filled by fallback.

## 6. The traps

**Trap A — R2 integer equality.** Higher match rate; precision collapses through restricted codes and padding collisions.

**Trap B — R3 without UPC-E expansion.** Misses or mis-matches short codes.

**Trap C — restricted prefixes kept.** Deli/variable-weight codes match across unrelated products.

**Trap D — R5 fuzzy fallback.** Raises recall but drops precision below 99%.

**Trap E — field conversions.** Salt vs sodium, oz vs fl oz, per-serving vs per-100 g.

## 7. Why the data is honest

Both catalogs contain the barcodes as manufacturers and contributors provided them; GS1 rules define the encodings. The
challenge is applying the rules, measured against a manual audit.

## 8. Draft task prompt (prose)

> We need one barcode matching rule for the product master, chosen by our governance standard: the highest recall with at
> least 99% precision on the steward's audit sample. Evaluate the five candidate rules, tell me which one we adopt, and build
> the conformed master with it. Deliver `product_master.parquet` in the exact target schema, `rule_evaluation.png` plotting
> precision against recall for the five rules with the 99% line, and a one-page `matching_rule_memo.pdf` stating the adopted
> rule, its precision and recall, the number of products in the master, and the most common false-match pattern in the
> rejected rules.

## 9. Deliverables

* `product_master.parquet`, `rule_evaluation.png`, `matching_rule_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 rules × (precision, recall); adopted rule; 12 schema fields (source + transformation); master size; false-match pattern.

## 11. Golden-output checklist

* GTIN-14 with check digits; UPC-E expansion; restricted prefixes excluded; criterion applied; schema exact.

## 12. Build notes (scope tuning)

* Build the audit sample by stratified sampling across rules' disagreements (integer-only matches, restricted-prefix matches,
  UPC-E cases); adjudicate manually from package photos/labels and document the procedure.
* Confirm the GS1 prefix list you cite against the current General Specifications.
