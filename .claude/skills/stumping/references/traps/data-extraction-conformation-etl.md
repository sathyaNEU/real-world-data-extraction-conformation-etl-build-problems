# Trap catalog: Data Extraction & Conformation (ETL / Pipeline Build)

> The work is to reconcile messy multi-source inputs into one analysis-ready, contract-conforming dataset.

**18 traps.** One catalog file per Axis 1 objective that has one (Opportunity Sizing & Decision Support and Data Quality Monitoring & Alerting have none of their own). Read `_cross-objective.md` alongside it, which carries the constraint, comparison and monitoring families that are not tied to one objective.

**Two bans apply to every trap below, so read them before you adapt one.** The planted-defect
flip is banned: an answer that depends on a planted defect reversing the naive reading is not a
source of difficulty. And under determinism judge v3, **surface-read rejection is banned as the
primary strategy at any depth**, which also bans the honest-data version, a single lens or
definition swap that flips the naive read. Depth is not a defence.

Two tests on whichever trap you adapt, and it has to pass both:

- **Clean-data test.** If the data were perfectly clean and correct, would the task still be hard
  and the answer still non-obvious?
- **The litmus.** Is the reported number or stakeholder conclusion the task overturns actually
  wrong, and is catching that the main thing that defeats the model? If yes, redesign.

Most traps below pass both already, because they turn on analysis rather than on a broken file.
Where one does not, it is flagged in place. Messy multi-file data is still required, it just
cannot be the thing that flips the answer.

Build the trap into the evidence rather than the wording, keep it reconcilable from the shipped
files alone, and make sure the failure is a genuine analytical mistake rather than a formatting
or wording problem.

These are traps that have already stumped models on this objective. They are examples to adapt,
not a checklist to copy, and one trap is rarely a ladder on its own: stack two to four from
different gaps (`stumping` Part 1) and different families (`stumping` Part 6.3).

## Start here: the two structural traps

- **No governance document / no data contract to anchor on**. The pack deliberately ships no rule to quote, so the criterion has to be earned from the data. This is the shape that most often separates a real analyst from a model looking for a sentence to cite.

## The traps

### No governance document / no data contract to anchor on

**What it is.** The task ships raw sources with no target schema, grain, or type spec, leaving the model to derive the canonical shape from the data and domain conventions alone.

**How it stumps the model.** Without a spec the model either stalls and demands a contract or fabricates an arbitrary schema, guessing at grain and column types instead of reading them out of the sources.

### Currency normalization at the wrong rate/date

**What it is.** Foreign amounts must be converted using the FX rate effective on each line's own transaction date, with attention to currencies that have no minor unit.

**How it stumps the model.** The model converts everything at one spot rate, usually today's or the file's latest date, and forgets that JPY has no cents, so the reconciled total looks plausible but is wrong.

### Timezone / DST conflation

**What it is.** Timestamps arrive in various local zones and formats and need DST-aware localization to a single canonical UTC before anything is aligned to a daily grain.

**How it stumps the model.** The model treats naive local times as UTC or bolts on a fixed offset, botching daylight-saving transitions and second-vs-millisecond epochs, so events slide into the wrong hour or day.

### Unit normalization drift

**What it is.** Sources mix measurement units, sometimes within a single file, and each value has to be carried to one canonical unit with the right conversion factor.

**How it stumps the model.** Mixed units like mg/dL and mmol/L or kWh and Wh get concatenated untouched, or the model applies one blanket factor to a source whose units actually vary row by row.

### Grain mismatch / double aggregation

**What it is.** Inputs sit at different grains such as 15-minute versus hourly or per-line versus per-invoice, and each has to be rolled to the target grain before any join.

**How it stumps the model.** The model joins across mismatched grains without aligning first, so rows fan out into duplicates or already-aggregated values get summed a second time.

### Entity resolution over-merge / under-merge

**What it is.** Names, emails, and phones need normalizing and matching so that one real person maps to exactly one canonical identity.

**How it stumps the model.** Fuzzy matching either fuses distinct people into a single identity or leaves obvious duplicates split over casing and formatting differences, corrupting the entity count either way.

### Idempotency failure on re-delivered files

**What it is.** Settlement and restatement files overlap in date range and get re-delivered, so the load has to be built as an upsert that a second run leaves unchanged.

**How it stumps the model.** The model appends overlapping rows or lets a stale version win, so running the pipeline twice changes the output instead of being a no-op.

### Silent row dropping on join

**What it is.** Joins have to be reconciled by row count so that records lacking a match are surfaced rather than quietly discarded.

**How it stumps the model.** An inner join drops unmatched rows for unmapped codes or missing keys, and the model reports a clean total that is silently missing records.

### Referential integrity violations ignored

**What it is.** Every fact-row foreign key such as facility_id or sku should resolve against its dimension, with orphans quarantined rather than loaded.

**How it stumps the model.** The model loads fact rows whose dimension keys don't exist, breaking the foreign-key guarantees the contract depends on and never reporting the orphans.

### Code crosswalk mis-mapping (ICD/NDC/status)

**What it is.** A supplied crosswalk has to be applied fully, accounting for many-to-one and unmapped codes and for mixed code versions in the same file.

**How it stumps the model.** The model maps naively, missing N:1 and no-match cases or leaving ICD-9 rows unmapped beside ICD-10, which corrupts every downstream count.

### Delimiter / decimal-separator / encoding misparse

**What it is.** Files vary in delimiter, decimal mark, and encoding, so each needs its parse settings detected before values can be trusted.

**How it stumps the model.** Default parsing on a semicolon-delimited comma-decimal European CSV truncates numbers at the comma, and Latin-1 or UTF-16 files turn accented names into mojibake, all without an error.

### Date format ambiguity (MM/DD vs DD/MM)

**What it is.** Date conventions differ across sources and have to be resolved per source, using provenance or disambiguating values, before normalizing to ISO.

**How it stumps the model.** The model picks one interpretation globally, so 03/04 flips between March 4 and April 3 and the time series scrambles with no parse error to warn anyone.

### Dedup window / near-duplicate mishandling

**What it is.** Retry and double-scan duplicates differ slightly in timestamp or origin, so dedup needs a defined key and time window rather than exact matching.

**How it stumps the model.** Exact-match dedup leaves the near-duplicates in, while an over-broad window collapses genuinely distinct events into one.

### Type coercion / precision loss

**What it is.** Identifiers, money, and high-precision timestamps each need a deliberate type so keys still join and totals stay exact on write.

**How it stumps the model.** The model reads IDs as floats and loses leading zeros or gains a .0, puts money in floating point and drifts by cents, or truncates timestamps so joins fail.

### Fixed-width / nested-structure parsing errors

**What it is.** Fixed-width mainframe files and deeply nested JSON need exact column offsets or correct path traversal to pull fields out intact.

**How it stumps the model.** The model mis-slices fixed-width columns or flattens nested arrays along the wrong path, shifting every value downstream from the error.

### Fragment stitching across a system split

**What it is.** A migration cutover splits single records into partial fragments under different id schemes that share a stable natural key and have to be stitched back together.

**How it stumps the model.** The model treats each fragment as a complete record, double-counting trips or orders instead of joining the pieces that span the cutover.

### Header / schema drift across periods

**What it is.** Multi-period exports rename, reorder, and add or drop columns over time, so each period's columns must be mapped to the canonical schema by name.

**How it stumps the model.** The model assumes a stable header and loads by position, so later periods land their values in the wrong columns.

### Aggregation total masks conformance failure

**What it is.** The conformed table is the real deliverable, and any headline figure should fall out of that validated table rather than standing in for it.

**How it stumps the model.** The model chases a plausible headline number via shortcuts like dropping hard rows or approximating conversions, so the figure looks right while the conformed table violates the contract.

---

Ask anatomy and example asks for this objective: `../../../guide-to-prompt/references/objectives/data-extraction-conformation-etl.md`

Mechanism families, the refusal ladder and the fourteen generators: `../../SKILL.md`
