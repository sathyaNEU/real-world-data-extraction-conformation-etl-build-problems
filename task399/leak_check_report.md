# leak check, task399

**Verdict: REVIEW.** 15 files read, 43 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, signaller, routes, incident, window, competence, incidents, review, export, findings, finding, control, geometry, layout, decisive, driver, hatherby, recorded, attribution, sentence, request, screen, graded, display, performance

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `governance/2027_improvement_plan_terms_of_reference.pdf`: carries 10 of 14 distinctive words of the committed call: "Fund programme B, the workstation display renewal: its cause produced 8,985 of the operating centre's delay minutes in t"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `governance/2027_improvement_plan_terms_of_reference.pdf`: 6 of 25 stump-paragraph terms appear (register, incident, incidents, review, attribution, performance); read whether the document names the move
- **REVIEW** `governance/improvement_catalogue_2027.docx`: 6 of 25 stump-paragraph terms appear (signaller, competence, layout, hatherby, screen, display); read whether the document names the move
- **REVIEW** `reference/fenmoor_roc_workload_assessment_2025.pdf`: 5 of 25 stump-paragraph terms appear (signaller, routes, hatherby, recorded, request); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `staffing/signalling_roster_2026-27_P01-P07.xlsx`: 12 ISO dates after 2026-10-09, e.g. 2026-10-10

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `reference/fenmoor_roc_workload_assessment_2025.pdf`: names 5 column(s) of the data files verbatim (Signaller, W01 Fenmoor, W03 Hatherby, Workload, Workstation): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 63ad083e621bf1a437906359dc06e73fbb240272f7aa2ed899ec150d1134cd3b). Sweep 4's lines were kept out of the brief and ruled in the main thread (the catalogue's programme B scope says the layouts are redrawn and names no slip; the terms of reference file a but-for WHAT). Verdict: no leak; question 6 an analytical choice; the realism tells below (the catalogue docx's generator residue, a shared PDF producer and sign-off names across organisations) go to the generator.

# Leak reader answers, task399

1. Decisive step. governance/2027_improvement_plan_terms_of_reference.pdf 2.3: "An incident counts for a programme when it would not have happened had that programme been in place." That states the counterfactual question but not how to decide it. 2.1 states the selection rule: "The plan funds the programme whose cause produced the most of the operating centre's delay minutes in the twelve months from 1 October 2025 to 30 September 2026." 2.5: "the plan begins with the stage that would have removed the most of those minutes." No sentence names a data field or the method.

2. Ranking or scoring of candidates: none. No file totals minutes by programme or cause. The registers carry a per-incident "Finding" (2025-26) / "Underlying cause" (2026-27) column; this is raw record, not a ranking. (The 2025-26 register has "Finding" values Workload/Competence/Attention/Fatigue/ARS data/Equipment; these are the organisation's per-incident labels, not a programme score.)

3. Files only to help the analyst: governance/2027_improvement_plan_terms_of_reference.pdf (it defines the population, window, delay-minute definition and counting test, so it works as the brief). The "Category codes" sheet in operating_incident_register_2026-27.xlsx maps 2026-27 codes to 2025-26 categories (a crosswalk), which reads slightly like an analyst aid but is plausible as a register legend. The workstation_layout_export JSON "ars_subareas" block with "replaces" (FM-A replaces "FENM N") is similar, a crosswalk between new and old ARS sub-area names.

4. Reads as the answer: none. No figure of minutes, no programme named as the recommendation.

5. Filed sentences fixing the computation:
- ToR 2.2: "The operating centre's incidents are those in its operating incident register whose delay is attributed to the operating centre (responsible code OCF). An incident belongs to the twelve months by the date and time it occurred, UK time." Fixes population (register incidents with OCF), window (1 Oct 2025 to 30 Sep 2026 by local occurrence time), unit (incident).
- ToR 2.4: "An incident's delay minutes are the primary and reactionary minutes held against its TRUST incident in the delay attribution records, after the moves the attribution review log records as agreed." Fixes the minutes measure: pfpi minutes of the TRUST incident, delay types P and R, with Agreed moves applied.
- ToR 2.1 fixes the selection: the programme whose cause produced the most minutes.
- ToR 2.3 fixes the attribution test (counterfactual) without a method. Literal result: minutes summed per programme over the stated population and window; the assignment of incident to programme is left to analysis.
- The prompt's own wording fixes the asks (hours by workstation, first two years since qualifying, ARS-off sub-area hours per calendar quarter).

6. What decides the main answer: mostly an analytical choice, with the data-reading and rule-following steps feeding it. ToR 2.3 ("would not have happened had that programme been in place") asks the analyst to judge causal counterfactual attribution of each incident to a programme (e.g. whether the cause is competence, a display/layout cause, shift length, ARS data, a workstation split), which is not read off one field: the register's cause/finding labels are the organisation's own and the filed test (2.3) points beyond them. The mechanical steps (OCF filter, UK-time window, TRUST join, agreed review moves) are rule application from 2.2 and 2.4. I see nothing in the pack that reads as a planted defect announced in a file. Caveat: the register category/finding labels may not align one to one with programmes, so the attribution rests on the analyst using the control-system logs; nothing quotes that route.

## Mechanical sweep items
a. harmless, because it names no programme to fund and carries no minutes figure; it only states the selection rule (most delay minutes in the twelve months), the window, the counting test and the minutes definition, which is what a terms of reference would hold. Note it does state the method of selection in plain words, so it is a brief, not an answer.
b. harmless, because the 2026-27 roster is an operational forward roster (rows run to 10 Oct 2026, a week or so past the 30 Sep window end; the roster file was last modified... created 2026-03-04 by "ROC Rostering"). A roster issued for P01-P07 would plausibly extend to the period end (P07 ends 10 Oct 2026). Mild caveat: the title says P01-P07 and the setting date is after 9 Oct only in that the file covers through 10 Oct, which is within a period boundary, not out of place.
c. harmless, because it is a third-party consultant report (Linwell Ergonomics, LE-2512-R2, accepted by Alan Pope) from March 2025 that uses the organisation's workstation names (W01 Fenmoor etc.) and task kinds; it reads as an independent assessment of the organisation, not a note describing the data. Its content is a distractor-like workload index, with no minutes or programme named.
d. harmless, because each programme entry only gives scope, cost, delivery and sponsor. None says which incidents its cause produced or points to a data field. Only slight nudges: B names "Corvane VDS-3" (matches the JSON vds_product), D mentions "ARS timetable data", A names "first two years since qualifying" (matches the prompt's staffing cut); these are scope descriptions, not pointers.

## Realism
- governance/improvement_catalogue_2027.docx: tells of a generated file. app.xml says Words 0, Characters 0, Lines 0, Paragraphs 0, TotalTime 0, and a Company element appears twice (empty `<Manager/>`, `<Company/>` and then `<Company>Wyvern Route</Company>`). The package holds the python-docx default template (stylesWithEffects.xml, customXml item1, docProps/thumbnail.jpeg, Normal.dotm, all file dates 1980-01-01). Core properties are creator Alan Pope / lastModifiedBy Helen Douglas with plausible dates, which are fine. The body has a revision table but no document reference number, page numbering visible in text (header/footer exist), or sign-off block, unlike the two PDFs.
- The two PDFs (both LibreOffice 24.2 "Writer", creator "Writer") read as plausible, with doc numbers, revision tables, sign-off tables with names and blank signature cells, "Page 1 of 1". Mild tell: both PDFs and the docx use the same two names (Alan Pope, Helen Douglas) in the sign-off, and the third-party consultant's PDF carries the same producer string (LibreOffice 24.2 Writer) as the client's internal ToR, though a consultant using a different tool would be expected. Also the ToR "Signature" column is empty.
- Systems: the control-system CSVs use UTC ISO timestamps with milliseconds and numeric user ids and servers ROC-A/ROC-B; the incident registers differ by year (2025-26 desk names and prose categories, 2026-27 W0n names and codes with a legend sheet); the delay records use UK dd/mm/yyyy and "2025/26 P01"; rosters differ in layout (per-period grids vs a flat list). These do read as different systems. 
- Too uniform: workstation_layout_export JSON has all six workstations with four 1920x1200 screens each and a regular x/y coordinate list with random ids (FM871 etc.), which looks synthetic but is plausible for a layout export. In the actions log the ROC-B server has only 647 rows against ROC-A 356,456 (reads like a standby server, fine). The ARS log is split almost evenly across ROC-A and ROC-B (7431 / 7463) and its reasons look neat (OOC, TTD, POSS, FAIL).
- Overall: docx is the file most likely to read as exercise-built (python-docx template residue with zero word counts). Others: none.

### Second read, on the FIX_NOW cut

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 5156aef810cef4008ca21339ddd39431c0aa234b2845ce1cbfa4c4f4bb2b78fa), after the catalogue's programme B scope sentence, the prompt's 'in total', and the catalogue's and the consultant report's metadata changed. Verdict: no leak; question 6 an analytical choice (the terms' 2.3 counterfactual against the catalogue scopes, rather than the register's own label); no realism tell beyond blank signature cells in typed copies.

# Leak read, task399 r2 (read and quote only; nothing solved)

1. Decisive step. TOR 2.3: "An incident counts for a programme when it would not have happened had that programme been in place." That is the only sentence that points at a counterfactual per-programme attribution, and it states the test, not the step. Nothing says which field or which programme. TOR 2.5 ("the plan begins with the stage that would have removed the most of those minutes") hints that a programme is staged and the chart question is about a start workstation (catalogue B: "Delivered one workstation at a time."). Neither names the trap.
2. Ranking/scoring file: none. The registers carry a per-incident cause label (2025-26 "Finding", 2026-27 "Underlying cause", e.g. "Competence - route setting", "ARS timetable data", "Workstation equipment") and the delay file carries minutes, but no file totals or ranks causes or programmes. The registers' own label is not a programme ranking.
3. Files existing only to help the analyst: none. 2026-27 register sheet "Category codes" (code to category to 2025-26 category) and roster "Key" sheet (D/N/RD/RN to hours) are ordinary code legends a real register/roster carries.
4. Figure or name reading as the answer: none. The catalogue costs (412,000; 1,860,000; 690,000 a year; 238,000; 1,120,000) are costs, not minutes. The assessment's "W03 Hatherby" high-workload and "very high" statements are about workload index, from a 2025 observation, and read as context (mild pull toward W03/Hatherby for the chart question, but it is a workload index, not delay minutes).
5. Filed sentences fixing computation/population: TOR 2.2 "The operating centre's incidents are those in its operating incident register whose delay is attributed to the operating centre (responsible code OCF). An incident belongs to the twelve months by the date and time it occurred, UK time." Fixes population (register incidents with OCF attribution), window (1 Oct 2025 to 30 Sep 2026 by local occurrence time), unit (incident). TOR 2.4 "An incident's delay minutes are the primary and reactionary minutes held against its TRUST incident in the delay attribution records, after the moves the attribution review log records as agreed." Fixes minutes = P + R delay types per TRUST incident, after Agreed review moves only (status Agreed, not Rejected). TOR 2.1 fixes the comparison: the programme whose cause produced the most minutes. All of this is estimand filing (what), not method.
6. What decides the main answer: an analytical choice, applying 2.3's counterfactual to decide which incidents a programme's scope would have prevented, versus the register's own cause label. Deciding sentence: TOR 2.3 plus the catalogue scopes (e.g. B "with every screen's track layout redrawn ... VDS-3 equipment removed", D "ARS timetable data rebuilt ... every later data load checked independently"). The register labels, ARS status log, competence register and railhead reports are the evidence for judging it. Some rule application and data reading (UK time vs UTC, agreed moves) also sit in the path but are stated in 2.2/2.4. I see no planted item.

a. harmless, because each scope paragraph describes what the programme does and costs; none says which incidents its cause produced, names a data field, file or column, or gives minutes. (Closest: B "VDS-3 ... removed from every workstation" and D "every later data load checked independently" describe the intervention, which is what the TOR's counterfactual test is applied against; that is context, not a pointer.)
b. harmless, because it names no programme to fund (only "one programme from the operating centre's improvement catalogue (ROC-IC-2027)") and carries no minutes figure; its only numbers are dates, document references and reference codes.
c. harmless, because it reads as the consultant's own report (Linwell Ergonomics, LE-2512-R2, purchase order, observers, 22 shifts, limitations section, author/checked/accepted block). Column values such as workstation names W01 to W06 and desk names are the site's own identifiers; it describes observations in Jan-Feb 2025, outside the window, and states no delay minutes. Minor: its 2.5 note on the December 2025 timetable and "W03 Hatherby" high workload are context that mildly colours the chart workstation question but cannot decide it.
d. harmless, because the prompt only fixes what is asked (programme, minutes, chart marking a start workstation, hours by workstation split by signallers within two years of qualifying vs others, ARS-off sub-area hours by quarter), the window, file names and rounding ("Delay minutes should be whole minutes and hours should be to one decimal"). "signallers then in their first two years since qualifying" fixes the population by time-varying status, which is a definition, not a method. No sentence tells how to attribute causes or describes the data.

Realism: none that reads as generated. Checked: catalogue docx (header "Fenmoor Rail Operating Centre ROC-IC-2027 issue 2", footer OFFICIAL + Page x of y, revision table, prepared/checked/approved block; core props creator Alan Pope, lastModifiedBy Helen Douglas, revision 9, dates consistent with the stated 18 June to 30 July 2026 and the named people); TOR PDF (letterhead, document number WR-SRP-TOR-26-04, revision table, sign-off table, footer "OFFICIAL Page 1 of 1"; metadata Writer/LibreOffice 24.2, created 3 Sep 2026 matching approval date; mild oddity: the Chair's signature cell reads "Route director, Wyvern" with a minute reference rather than a name, plausible); assessment PDF (Linwell letterhead, LaTeX pdfTeX metadata, created 28 Mar 2025 matching issue date, "Accepted for the route 7 April 2025" is after issue, plausible). Minor tell only: the signature columns are blank in both PDFs (typical of a typed, unsigned copy). The incident registers' creator "Helen Douglas" and the roster/competence xlsx creators are consistent with named staff in the documents.
