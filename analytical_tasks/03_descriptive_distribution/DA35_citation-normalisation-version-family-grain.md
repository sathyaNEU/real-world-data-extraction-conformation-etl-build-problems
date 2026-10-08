# DA35 — Which citation-normalisation structure a research council adopts for its excellence grants, when one paper circulates as several records

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · research funding assessment |
| Mirrors | Ranking creators or sellers on a normalised percentile when one item circulates as several records (cross-posts and reposts on social platforms, app variants in stores, duplicate listings on marketplaces), so the record grain splits the best items' counts |
| Decision shape | A structure the body adopts: the reference-set structure for field-normalised top-10% shares, scored on the council's audited subsample, which then fixes the eight funded universities |
| Committed call | The structure adopted (unit, reference sets, tie rule), and the university it brings into the funded eight in place of the one it drops |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern D (two grains: database records against papers), with a quiet second trap carrying its own control at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #11 beats the headline trap, misses the quiet one · #3 stops at a close but inexact match |
| Calibration form | Gold-standard verification subsample: 600 papers classified by an external bibliometrics provider under the council's framework |
| Driving force | The database holds a preprint and its published version as separate works, and citing works cite whichever version they found. At the record grain, a heavily cited paper's citations split across two records and the extra records crowd each reference set. The paper, the framework's unit, is a version family joined through the relations file, counted on distinct citing works. Physics and computing papers circulate as preprints most, so the grain decides which universities clear the line. |

## 1. Situation

A national research council funds eight universities from 25 candidates on their share of 2016–2020 papers in the top 10% of their field
and year. Reviewers rejected last cycle's global percentile, and the council's bibliometrics committee must adopt a structure for the
reference sets before the ranking is run. The framework makes the paper the unit of assessment. The pack holds the publication database
export with its relations file, field assignments, the council's framework, and the external provider's audit of 600 papers.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each record, each citation link, each field and each audited class. Nobody files a ranking and
  nothing reported is overturned. The difficulty is what one paper is in a database of records.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the association's list and both voices. Field-year reference sets with fractional ties, built from the records,
  still match 548 of 600 audited classes and still fund the wrong university.
* **Instrument repair.** Make every record and citation link perfect: preprints and published versions remain distinct works by design,
  and a paper is still a family to be assembled.
* **Lens swap.** The naive structure ranks records with their own citations; the answer ranks families with their distinct citers. The
  units, their counts and the reference-set populations all differ.

## 3. The driving force

A strong solver throws out the global percentile, builds field-year reference sets, shares tied papers fractionally at the threshold as
the audit's fractional classes demand, and checks the audit: 548 of 600 classes match. The 52 misses look like edge cases. They are not.
Every one belongs to a paper that circulates as a preprint and a published version, or sits in a field-year crowded with such records. At
the record grain, a paper cited 300 times in its published form and 120 times as a preprint, 60 citers citing both, is two middling
records, not one paper with 360 citers. The framework's unit is the paper, and the relations file joins its versions. Rebuilt on families,
every audited class matches. Physics-heavy Northfield University then clears the line that Harrowgate held.

## 4. The ladder

| Rung | Structure | Boundary (8th in, 9th out) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | One global reference set, records as units | Harrowgate 13.8% in; Northfield 21st at 7.9% | The provider's default percentile | The audit: global classes match 233 of 600 |
| 1 | Field × year reference sets, records as units, papers at the threshold counted whole | Harrowgate 12.6% in; Northfield 11th | The textbook normalisation the reviewers asked for | The audit's fractional classes (0.12 to 0.88) for tied papers, which whole counting cannot return |
| 2 | Field × year, records as units, tied papers shared fractionally | Harrowgate 12.0% in (1.15× Northfield, 9th at 10.4%) | 548 of 600 audited classes match, and both visible traps are beaten | The audit: all 52 misses are version-family papers or their field-years |
| 3 | **Decisive:** field × year, papers as version families joined through the relations file, citations as distinct citing works, ties shared | **Northfield 14.1% in (1.20× Harrowgate, now 9th at 11.75%)** | — | — |

* **Position table.** Northfield sits 21st, 11th and 9th on rungs 0 to 2 and enters the eight only on rung 3. Each rung's boundary
  margin is at least 1.15×.
* **Discriminator dominance.** Harrowgate carries 1.15× into rung 3. Families raise Northfield's share 1.36× and lower Harrowgate's 0.98×,
  an edge of 1.39×, above the 1.2 × 1.15 = 1.38 needed. The product, 1.39 / 1.15 = 1.20, is the final margin.
* **Partial correction priced (L3).** A solver who merges versions but keeps each version's own citation count (summing rather than
  de-duplicating citers) overstates preprint-heavy fields and funds Calder Institute of Technology instead, leaving Northfield 10th. A
  solver who merges families but takes the preprint's field drops 31 physics papers into an astronomy reference set and leaves Harrowgate
  in.
* **Grid.** Reference sets (global or field-year) × ties (whole or fractional) × unit (record, family with summed counts, family with
  distinct citers) = 12 cells. Eleven fund Harrowgate or Calder; only field-year, fractional ties and distinct-citer families fund
  Northfield.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The framework says "the unit of assessment is the paper". No document says the database's works are versions, or
   that citations attach to versions.
2. **Pattern B, reproduction against the best rival.** Distinct-citer families reproduce 600 of 600 audited classes. The best rival
   (records with fractional ties) reproduces 548, summed-count families 571, whole ties 512 and the global set 233. Rivals miss the same
   way, under-classing family papers, so none ties the audit in total. The family is a construction: version links resolved through the
   relations file, then citing works de-duplicated across versions.
3. **No arithmetic symptom.** Records reconcile to the export, citation links to citing works, and every reference set's fractional
   shares sum to exactly 10% under both grains.
4. **Not a row predicate.** It needs a link resolution across records, a union of citers per family, and percentiles recomputed on a
   different population.
5. **The enumeration is arithmetic.** No column marks a record as one version of a paper.
6. **No cutover date.** Preprinting grew steadily, and nothing steps.
7. **Survives deletion.** With every voice removed, the record-grain structure still matches 548 of 600 and funds Harrowgate.

## 6. The calibration corpus

* **Form.** The external provider's audit: 600 papers stratified by field and year, each with its fractional top-10% class computed under
  the council's framework.
* **What it certifies.** Field-year reference sets and fractional ties, so a solver who back-tests is confirmed through rung 2.
* **What pins the grain.** The 52 classes only families with distinct citers return.
* **Twin pair.** Audited papers P-0193 and P-0471 share field, year, document type, field count and 38 citations to the published version.
  Their classes are 1.0 and 0.5 (2.0×): P-0193 has a preprint whose 26 further distinct citers lift it clear of the threshold.
* **Resemblance points at the decoy.** By field mix and citation totals, Northfield resembles the candidates the record grain already
  places 9th to 12th.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The framework: the unit of assessment is the paper; each paper is compared with papers of its field and year; the
  council funds the eight highest shares among eligible candidates.
* **Empirical pins.** The unit, the citation count and the tie rule, from the audit.
* **Voices.** The research director: "Field normalisation is the correction; after that the counts speak for themselves." The library's
  bibliometrician: "Ties at the threshold are noise; count them in."
* **Licensed wrong basis.** The framework records that the universities' association ranks candidates on global top-10% shares and will
  publish its own list the same week.

## 8. Determinism by construction

* **Links.** Every relation in the file is one-to-one, and no family has more than three versions.
* **Field and year.** A family takes its published version's field and year, the reading the audit pins; preprint categories are ignored.
* **Ties.** Fractional shares follow the audit's rule within each field-year, and the boundary pair's shares do not depend on rounding.
* **Eligibility.** Every candidate clears the 1,000-paper floor under both grains.

## 9. Prompt sketch and deliverables

> The committee has to settle how the excellence ranking is normalised before we run it, and the research director thinks field
> normalisation is all it needs. Tell me which structure we adopt and which university it brings into the funded eight in place of which,
> as the recommendation for the committee. Send `normalisation_structure.xlsx`, a chart `boundary_shift.png`, and a one-page
> `committee_note.pdf`.

* `normalisation_structure.xlsx` — the structure build, the publication-lag sheet (ask A), the author sheet (ask B) and the audit table
  (ask C).
* `boundary_shift.png` — the 25 candidates' shares under the four structures as slope lines, with the eight-place line drawn, Northfield
  and Harrowgate highlighted, and each structure's audit match count labelled.
* `committee_note.pdf` — the adopted structure, the boundary change, and why each rival structure fails the audit.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 26 fields, the median days from acceptance to publication for 2020 papers.
  *Device:* the dates file carries both the online date and the issue date, and the metadata note makes the online date the publication
  date; using issue dates misstates seven fields. No paper's two dates fall in different years.
* **Ask B (device-carried).** For each candidate, distinct corresponding authors over 2016–2020. *Device:* the author-disambiguation file
  merges split profiles; counting raw author IDs overstates nine candidates.
* **Ask C (validity).** Audited classes matched under each of the four rung structures, and the boundary pair's shares under each.
* **Decoupling.** Clearing the family construction changes no figure in asks A or B.

## 11. Rubric arithmetic

26 fields (ask A) + 25 candidates (ask B) + 4 match counts and 4 × 2 boundary shares (ask C) + the three parts of the structure, the
university brought in and the one dropped + 5 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Boundary shares (%): rung 0 Harrowgate 13.8, Northfield 7.9 (21st); rung 1 Harrowgate 12.6, Northfield 11th; rung 2 Harrowgate 12.0,
  Northfield 10.4; rung 3 Northfield 14.1, Harrowgate 11.75.
* 18% of records in physics, computing and mathematics belong to multi-version families, against 3% elsewhere.
* Audit: 600 / 571 / 548 / 512 / 233 by structure. P-0193 and P-0471 match on every record column.
* Date pairs and author merges never touch a version link, a citation or a field.
