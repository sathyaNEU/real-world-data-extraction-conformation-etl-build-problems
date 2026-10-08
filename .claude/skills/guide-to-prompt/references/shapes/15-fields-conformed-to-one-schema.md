# Shape 15 · Fields conformed to one schema

> **Where the criteria come from:** each target field, checked on its source and its transformation, in every system.

You map many source columns into one target schema, grading each field on where it came from and
how it was transformed in every system. The answer is the entity-matching rule you adopt as the
key. The many criteria come from each target field, checked on its source and its transformation.

**Canonical Axis 1 objective under our roster:** Data Extraction & Conformation (ETL).

## Sizing it to 25

Ten target fields, each graded twice (which source column fed it, and what transformation was
applied), is twenty criteria and this shape reaches 25 more easily than any other. Add the rows
dropped per system, the lineage column itself, the adopted rule, the conformed headcount under
that rule, and the known links the rule reunites.

**What makes it hard rather than long.** The adoption test is a **two-part test with a
tiebreak**: the candidate rule whose count lands inside audit tolerance of a certified figure
*and* links every verified pair wins, ties to the simplest. That forces the solver to build every
candidate rule completely, not just its favourite, and it punishes a rule that hits the count by
over-merging. The verified transfer or merge list is the second gate and is what defeats the
loosest rule. Keep the tolerance in an audit memo, the certified figure in a separate
certification, and the verified pairs in a third file.

**House caution.** This is the one shape whose difficulty is conformance end to end, so on a build
tagged ETL it collides with the standing house ban on conformance in the top two rungs of the main
ladder. Use it when the ladder's decisive move is the **adjudication between candidate rules**,
not the conformance itself, and check `supplemental-stumping` Part 1 before the ask layer draws
its devices from the same family.

---

## Four worked prompts


> **Before you draft, read [`../prompt-voice.md`](../prompt-voice.md).** The four prompts below are
> the client's. Across the eighteen shape files these examples open on the rule, the constraint,
> the deliverable, the question, the symptom, the number and the person, so **none of them is the
> template and the four below are not a menu of four.** Read four in a row and you will write the
> fifth in whichever voice you just read, which is how eighteen consecutive builds came to open
> with "I run". Pick the move from what forces your decision, then check it against the last three
> builds with `../voice-check.py`.

> **Idea seeds only.** Nothing below transfers into a build: not the scenario, not the entity,
> not the metric, not a file name, not the wording of a single ask.

### Policy & Education · 2 files · ~30 criteria
*The student key across four district systems*

I lead data for an education service authority and I owe the state one student table whose key
follows a child across districts. The test: the candidate matching rule whose headcount lands
inside audit tolerance of the certified October count and links every verified transfer wins,
ties going to the simplest. Produce the conformed table under the rule that wins,
students_unified_2026.csv, one row per student under the adopted rule with the districts each
student came from. And the lineage record state reviewers will read, a JSON file, each target
field with its source column per district and the transformation applied, the rows dropped per
district, and the rule adopted with the verified transfers each candidate rule links.

*Criteria:* 10 target-schema fields x 2 (source column per district + transformation per
district) = 20 + the drop-count set + the lineage column + the adopted rule + conformed headcount
+ verified links under the rule + 2 deliverables + implicit key/format rows.

### Product Analytics · 2 files · ~30 criteria
*The identity rule across four customer systems*

I run the data platform, where billing, the CRM, the product database and support all key
customers differently, and I need one identity-resolution rule adopted as the customer key. The
test: the candidate rule whose deduplicated count lands inside tolerance of the audited billing
roster and reunites every known merged account wins, ties to the simplest. Build the conformed
customer table under the rule that wins, a CSV, one row per customer under the adopted rule with
the systems each customer was seen in. Then the lineage the data-governance review signs off,
customers_lineage.json, each target field with its source column per system and the
transformation applied, the rows dropped per system, and the rule adopted with the known account
merges each candidate rule reunites.

*Criteria:* 10 target-schema fields x 2 (source column per system + transformation per system) =
20 + the drop-count set + the lineage column + the adopted rule + deduplicated count + merges
reunited under the rule + 2 deliverables + implicit key/format rows.

### Supply Chain & Logistics · 2 files · ~29 criteria
*The vendor key across four procurement systems*

I manage master data, where two ERPs, the sourcing tool and the payments ledger all key vendors
differently, and I need one vendor-matching rule adopted as the vendor key. The test: the
candidate rule whose consolidated count lands inside tolerance of the audited AP master and links
every confirmed duplicate pair wins, ties to the simplest. Produce the conformed vendor master
under the rule that wins, vendors_unified.csv, one row per vendor under the adopted rule with the
systems each vendor was sourced from. And the lineage record audit will trace, a JSON file, each
target field with its source column per system and the transformation applied, the rows dropped
per system, and the rule adopted with the confirmed duplicate vendor pairs each candidate rule
links.

*Criteria:* 10 target-schema fields x 2 (source column per system + transformation per system) =
20 + the drop-count set + the lineage column + the adopted rule + consolidated vendor count +
duplicate pairs linked under the rule + 2 deliverables + implicit key row.

### Nonprofit & Grant-making · 2 files · ~29 criteria
*The constituent key across four fundraising systems*

I lead development operations, where our CRM, giving platform, direct-mail file and grants
database all key donors differently, and I need one constituent-matching rule adopted as the
household key. The test: the candidate rule whose deduplicated count lands inside tolerance of the
audited gift ledger and reunites every known household merge wins, ties to the simplest. Build the
conformed constituent table under the rule that wins, a CSV, one row per constituent under the
adopted rule with the systems each was recorded in. Then the lineage record the auditors review,
constituents_lineage.json, each target field with its source column per system and the
transformation applied, the rows dropped per system, and the rule adopted with the known household
merges each candidate rule reunites.

*Criteria:* 10 target-schema fields x 2 (source column per system + transformation per system) =
20 + the drop-count set + the lineage column + the adopted rule + deduplicated count + household
merges reunited under the rule + 2 deliverables + implicit key row.
