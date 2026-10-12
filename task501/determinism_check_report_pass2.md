# Verdict, task501 (re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No rerun needed. One optional pin (see Evidence, fork 1) would remove a 1-to-3-person ambiguity in five supplementary cells; not required.

**Why:** Every committed answer reproduced from the shipped files with no competing answer. The age-structured next-generation matrix is forced by the shipped contact table and by PS-07 3.2, which defines R0 as the value with nobody immune. The only option under one is B (0.89 against 1.31 with no catch-up), and the other four sit at 1.29 to 1.31, clear of any rounding line. The register counts follow from the circular, the merge file, the query log and guideline 12.5.

## Evidence (recomputed from target/)
| Item | Result | Source |
|---|---|---|
| Susceptible share, 15-19 on 1 Jan 2028 / region | 11.2% / 5.4% reproduced | population_projection (4 counties summed, "100 and over" mapped to the 1927-and-earlier row) joined to immunity_profile by year of birth |
| R, no catch-up | 1.311 -> 1.3 | Table 2 x susceptible share by column, dominant eigenvalue, scaled so all-susceptible = 15 |
| R under A / B / C / D / E | 1.291 / 0.888 / 1.305 / 1.302 / 1.298 -> 1.3 / 0.9 / 1.3 / 1.3 / 1.3 | options PDF made-immune counts removed pro rata from susceptibles of the birth years |
| Residents at 30 Jun 2027 | A 35,346; B 33,217; C 29,398; D 30,625; E 57,865, all reproduced | active register, region by the scheme in force on lho_recorded (LH27 before 1 Jul 2024 = Monaghan West, in region; LH27 from then = Portlaoise, Midlands) |
| No valid dose / exactly one | A 3,542/4,724; B 4,285/6,094; C 2,859/3,960; D 4,971/7,302; E 8,530/11,788, all reproduced | events re-pointed through merges (23 chains followed), replaced or withdrawn GP lines dropped, doses before the first birthday dropped, doses less than 28 days after the previous dose dropped, given date no later than 30 Jun 2027, non-active registrations excluded |
| Confirmed cases / imported | A 9/2; B 10/2; C 11/3; D 10/3; E 16/5, all reproduced | 113 rows reduced to 81 by legacy number (32 back-entered 2019 records matched to migrated records); Confirmed, onset 1 Jan 2019 to 30 Jun 2027, by year of birth of the pair; importation = "Imported" |

Competing answers tested:
- Homogeneous mixing, R = 15 x 0.054 = 0.81, gives "no catch-up needed". The shipped contact table and the concentration of the susceptibles at ages 15 to 19 and 30 to 34 make the age-structured matrix the only defensible method. This is the intended trap, not an open fork.
- Matrix orientation (transpose) gives the same eigenvalue. Re-imposing reciprocity with the 2028 regional population gives 1.3112, the same figure. The interval chain rule (previous valid dose against previous given dose) changes nothing. Ignoring the query log shifts cells by 4 to 20 people, but the log and the register notes make dropping those lines the literal reading.
- Naive region by the 2024-07 code file counts 32,466 for B (and about 700 fewer for the others), so the circular is decisive for the register cells. That is rule application on an ask, which is allowed.
- Counting imported plus import-related for the imported column would give a different number, but the field notes define "Imported" (infected abroad) separately from "Import-related", so the literal reading is forced.

**Residual minor fork 1 (ask 4 only):** the 3 July extract loaded 13 doses on 1 and 2 July that were given on or before 30 June (loaded_on after 30 June). Counting by given date, as the prompt's "have had" reads, gives the golden. Counting by load date at 30 June moves B to 4,287 / 6,094, C to 2,861 / 3,959, D to 4,973 / 7,301, E to 8,533 / 11,787; A is unchanged. The golden reading is the more natural one, so this is low risk, but a one-line pin would close it.
**Residual minor fork 2:** a dose given exactly on the first birthday (1 event) counts under "before the first birthday"; a strict reading changes nothing in the cells.

## Files/Hygiene
PASS. 19 files in 5 formats (csv x10, pdf x5, xlsx, docx, txt). There are 278,746 event rows and 163,368 register rows, and the transmittal row counts match. The fiction is coherent: dates are on or before 12 Jul 2027, and the options paper (9 Jun 2027) and PS-07 (10 Mar 2026) are consistent with each other. Distractors present and unused: national_mmr_uptake_report_2027q1.pdf, mmr_stock_return_2027-06-30.csv, nmrl_measles_results_2019-2027.csv, and the Table 1 population and unit costs. No authoring or benchmark language and no README artifact found. Realistic noise is present: day-month swaps between back-entered and migrated records, query-log churn, merged registrations, and the old and new LHO code schemes. Nothing exclusion-level.

## Stump power
Moderate. A strong model that reads the contact table builds the age-structured matrix and gets the call. The traps that do the work are (a) the homogeneous R0 x susceptible shortcut, which says no catch-up is needed, (b) applying each option's made-immune count to the right age group's susceptible share, and (c) in the asks, the LHO scheme change, merge re-pointing, the withdrawn and replaced GP lines, and the legacy-number deduplication of cases. The asks carry most of the failure weight, because each is a many-cell grid and one missed rule shifts every cell.

## Stumping type
`mechanism: method_or_model_selection` (age-structured next-generation matrix against homogeneous mixing, plus etl_conformance on the register asks), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. On clean data the contact-structured eigenvalue would still stump, because homogeneous mixing says 0.81 and the structured answer says 1.3. No reported figure is wrong.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Swap test: the reproduction number from a contact-matrix next-generation eigenvalue with age-specific immunity is a core infectious-disease modelling quantity, so it does not survive a change of nouns. Layer 1 is the mess across the register, merges, query log, LHO recode and case export; Layer 2 is the age-structured transmission model. The easy route (national or regional susceptible share times R0 = 0.81, "no catch-up needed") is reachable by a strong analyst who read every rule correctly, and it gives the wrong answer; the register and case rules sit in the asks and are not the main step.

## Fix
none. Optional, to remove fork 1: add to the prompt that doses count by date given. This changes nothing a solver sees in the files, so no model rerun is needed.

## Disposition

Approved as judged (judge-task501d, the re-judge after the pass-1 send-back in determinism_check_report.md). Nothing
changed in the generator, the pack, the goldens, the write-up or the prompt.

1. **Residual fork 1 (13 doses given on or before 30 June 2027 and loaded on 1 or 2 July).** Already closed in the
   shipped record. register_extract_notes_2027-07.docx defines `date_given` as "Date the dose was given, as returned."
   and `loaded_on` separately as "Date the event was loaded to the register.", and says the 3 July run loaded the returns
   received on 1 and 2 July. A person has had a dose on the date it was given, so the golden counts each dose by its date
   given, on or before 30 June 2027: the field's own definition and the prompt's "have had". No document or prompt edit;
   the optional prompt clause is not needed.
2. **Residual fork 2 (one dose given on a first birthday).** Moves no cell (the judge); nothing to close.
3. **The shipped bundle is the judged bundle.** The final rebuild (`build.py --zip`) is byte-identical to the pack the
   re-judge read (19 of 19 files compared with its copy) and to the build before it, and so are both goldens,
   figures.json, metadata.json and submission.md. Free gates on it: `checks.py` 212 PASS; `verify.py` PASS; two builds
   byte-identical; `figures_check.py` exit 0 (57 figures); `precut.py` exit 0; `voice-check.py` exit 0; `leak.py` REVIEW
   (no LEAK, sweep 11 clean, every line answered in the design note); `guard.py surface` no hard tell (task104 and
   task70 promoted on card axes only, already differentiated); `guard.py heart` PASS; `freeze.py check task501 --mode
   determinism` PASS. target.zip is cut from that rebuild by the generator's own `cut_zip` (19 members, identical to
   target/).
