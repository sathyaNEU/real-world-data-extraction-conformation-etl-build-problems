# Provenance

Student and school records from Tennessee's Student/Teacher Achievement Ratio experiment (Project
STAR), with the codebooks and reports that go with them. Kindergarten pupils entering 79 Tennessee
elementary schools in 1985-86 were randomly assigned, within each school, to a small class (13 to
17 pupils), a regular class (22 to 25) or a regular class with a full-time teacher aide, and the
cohort was followed through grade 3. Pupils who joined a STAR school in first grade (by 1 November
1986) were assigned the same way on entry. Achievement records were later added for grades 4 to 8
and high school.

Every file was downloaded on 2026-10-13 from the Harvard Dataverse deposit:

> C.M. Achilles; Helen Pate Bain; Fred Bellott; Jayne Boyd-Zaharias; Jeremy Finn; John Folger;
> John Johnston; Elizabeth Word, 2008, "Tennessee's Student Teacher Achievement Ratio (STAR)
> project", https://doi.org/10.7910/DVN/SIWH9F, Harvard Dataverse, V1.

The deposit is released under CC0 1.0 (public domain dedication). Please cite it as above. The
overview page still carries the HEROS, Inc. footer from the website it was first published on.

| File | Rows | What it is | How it got here |
|---|---|---|---|
| STAR_Students.tab | 11,601 | One row per student who was in the experiment for at least one year in grades K to 3. Columns `gk*`, `g1*`, `g2*`, `g3*` hold that year's school, teacher, class type, class size, free-lunch status and test scores; `g4*` to `g8*` and `hs*` hold the later follow-up records. 379 columns | Dataverse tabular export of file 666716, unchanged |
| STAR_K-3_Schools.tab | 80 | One row per STAR school: urbanicity, grade range, which years it took part, enrolment, attendance, Chapter 1 status and pupil composition by year | Dataverse tabular export of file 666717, unchanged |
| STAR_High_Schools.tab | 161 | One row per high school attended by STAR students | Dataverse tabular export of file 666718, unchanged |
| Comparison_Students.tab | 1,780 | Students in grades 1 to 3 at 21 matched schools that were not in the experiment, tested on the same instruments | Dataverse tabular export of file 666719, unchanged |
| STAR_Students-ddi.xml, STAR_K-3_Schools-ddi.xml, STAR_High_Schools-ddi.xml, Comparison_Students-ddi.xml | | Variable-level codebook for each table in DDI 2.0: the variable label, every value label with its frequency, and the UNF fingerprint Dataverse computed at ingest | Dataverse variable metadata for each file, saved as served |
| starUsersGuide.pdf | | Finn, Boyd-Zaharias, Fish and Gerber, *Project STAR and Beyond: Database User's Guide* (HEROS, 2007). Study design, data collection, every variable and its coding | Dataverse file 666705, unchanged |
| Project STAR K-3 summary report.pdf | | Tennessee State Department of Education, *STAR Final Summary Report 1985-1990* | Dataverse file 666702, unchanged |
| STAR follow-up Studies (1996-1997) Report newstar.pdf | | HEROS, *STAR Follow-up Studies 1996-1997* (September 1997), on STAR students in the later grades | Dataverse file 666715, unchanged |
| star-college.pdf | | Krueger and Whitmore, *The Effect of Attending a Small Class in the Early Grades on College Attendance Plans* (executive summary) | Dataverse file 666704, unchanged |
| Overview of Public Data Files.htm | | HEROS page describing the four data files | Dataverse file 666710, unchanged |
| dataverse_SIWH9F_dataset_metadata.json | | The deposit's own metadata record: citation, authors, licence, and every file with its size and checksum | Dataverse `datasets/export?exporter=dataverse_json`, pretty-printed |

## Notes on the tables

- The tables are the tab-delimited files Dataverse produced when it ingested the original SPSS
  files. Codes are stored as numbers and blanks are `NA`. The value labels are in the DDI files and
  in chapter 3 of the user's guide; for class type, 1 is small, 2 is regular and 3 is regular with
  aide.
- A student's class type, school and teacher are blank for every grade in which the student was
  not in a STAR school. `yearsstar` counts the years in the experiment, `yearssmall` the years in
  small classes, and `cmpstype` and `cmpsdura` are the codebook's class type composite (small,
  regular or aide) and duration composite for each student.
- Teacher ids nest within school ids (the first six digits of `g1tchid` are `g1schid`). One
  grade-3 record has a school and a class type but no teacher id. School ids are anonymised and do
  not match any public school directory.
- The checksums Dataverse lists for the four tables are for the original SPSS files rather than for
  the tab export. Every value-label frequency in the DDI files reproduces from the tab files, and
  every other file matches its listed checksum.
