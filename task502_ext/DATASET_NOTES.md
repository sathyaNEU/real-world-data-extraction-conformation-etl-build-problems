# task502 dataset notes

- Domain: Policy & Education
- Subdomain: Program evaluation (the effect of a policy or program on outcomes, net of composition)
- Objective: Experiment & Causal Analysis
- Spine: Tennessee Project STAR student file, 1985-86 to 1988-89 with follow-up to high school (11,601 rows, 379 columns), joined to the K-3 school file (80 schools) on the grade-year school id

This is a clean real-data bundle only, like task112_ext and task113_ext. No draw has been made and
nothing is planted: there is no ladder, no stump sentence, no calibration file, no governing document
and no social layer, and no fingerprint card is filed. The pairing (policy-education x
experiment-causal) has never been built in the corpus, per `guard.py coverage` on 2026-10-13.

**Why the objective is the domain's own analysis.** STAR is a randomized trial of an education policy
lever (class size), so the causal machinery is the program's own design, not a generic method put
onto education nouns. The pack ships what the objective needs as real columns: assignment
(`g*classtype`, randomized within school), outcomes at pinned horizons (Stanford Achievement Test scaled
scores each grade K to 3, then grades 4 to 8, high school graduation and ACT/SAT taking), and the confounders and
design features as fields (`g*freelunch`, race, school urbanicity, school and teacher ids for
clustering, late entry in grade 1, the regular and aide re-randomization after kindergarten, movement
between class types, and attrition). The comparison-school file gives the non-experimental contrast
the experimental estimate can be held against.

The mess is the publisher's own and nothing was added: numeric codes with labels only in the DDI and
the guide, `NA` for every grade a student was not in STAR, uninformative school-file column names
(`var1` to `var52`, labelled in the DDI), one grade-3 record with no teacher id, and the guide's
statement that 22.0% of the non-four-year students entered in grade 1 and stayed through grade 3,
which does not reproduce from the file under any obvious definition (the closest readings give 13.6%
and 14.0% of that remainder). Anyone building on this pack should not lean on that sentence.

`generator/build_pack.py` rebuilds `target/` from the Dataverse API, copies in
`generator/provenance.md`, runs 31 checks (Dataverse MD5s, all 590 DDI value-label frequencies
reproduced, joins, id nesting, the arm counts and the 11,601, 1,780, 79 and 26.6% figures the guide
states) and writes a flat `target.zip`.

Input gates as built: 15 files, six formats (tab, xml, pdf, htm, json, md), largest file 11,601 rows.

## Tried and rejected

- The original SPSS `.sav` files (in the deposit's `PROJECT STAR.zip`): they duplicate the tab exports, and shipping both would double the tables. The tab exports plus the DDI codebooks carry the same values and labels.
- The fact sheets, press release, order form, reference list and the teacher-practices and pupil-teacher-ratio papers in the deposit: they describe or promote the study and add no fields or results the analysis uses.
- A check on the guide's 22.0% first-grade-entrant figure: it does not reproduce (see above), so the generator asserts the arm counts and the 26.6% four-year share instead.
