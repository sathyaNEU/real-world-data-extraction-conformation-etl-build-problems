# leak check, task285

**Verdict: REVIEW.** 18 files read, 38 golden figures and 27 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: network, envelope, guidance, village, storage, isolation, survey, sentence, silent, report, council, levels, standard, stages, descriptive, decisive, section, analyst, reflex, trustees, surveyed, golden, moment, closures, deepest

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: \bthe model\b x2: ...ghways authority's 2019 levels survey, which covers every road inside the model's floodplain. The hospital is reached at its emergency department ent...
- **REVIEW** `quarnell_flood_model_report_2025.pdf`: \bthe model\b x5: ...llin Beck, Ravelsby Brook and Lunnerby Beck. This summary records how the model was built, the hydrology, the calibration and the design results; the...

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: carries 17 of 18 distinctive words of the committed call: 'Share the 2027 Flood Ready budget between the six parishes the design flood would cut off from Hawkesbridge General Hosp'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: 8 of 25 stump-paragraph terms appear (network, guidance, village, storage, survey, council); read whether the document names the move
- **REVIEW** `quarnell_flood_model_report_2025.pdf`: 8 of 25 stump-paragraph terms appear (storage, survey, report, council, levels, stages); read whether the document names the move

## 6 ranking artifacts (REVIEW 6, INFO 5)
- **REVIEW** `council_tax_dwellings_by_parish_oct2026.csv`: names 5 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: names 7 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `highways_network_2025.geojson`: names 9 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `highways_road_closures_jul2021.csv`: names 15 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pfr_property_survey_2022.xlsx`: names 5 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `quarnell_flood_model_report_2025.pdf`: names 4 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `address_register_extract_oct2026.csv`: names 5 of 27 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `flood_warning_areas_2025.geojson`: names 4 of 27 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `police_road_closures_jul2021.csv`: names 4 of 27 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `rest_centres_2026.xlsx`: names 6 of 27 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `storage_areas_QRN25.geojson`: names 3 of 27 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: names 4 column(s) of the data files verbatim (Highfold, Hollinside, Parish, Whinnerby): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 3a9e57dbdb11885fe8249fd346fafbaff8c8144adc03be5b1290a26eebe48a5a). Sweep 4's lines were kept out of the brief and ruled in the main thread. Verdict: no leak; question 6 read as largely an analytical reconstruction, with the caution that the guidance is a very complete procedure (weighed against Gate H with the judge); the realism tells below go to the generator.

# Leak read, task285 (no solving)

1. Decisive step: flood_ready_fund_guidance_2027.pdf s.2: "A village is cut off when it has no road route to the hospital that an emergency ambulance could use. The county ambulance service's crews will not take a vehicle along a carriageway where floodwater stands deeper than 0.25 m." This names the depth rule, but the per-road depth is not filed; the pack gives only 2019 carriageway levels, storage-area stages, a link crosswalk. It states the criterion, not a ranking. Closest to an announcement of the method: "Road routes are the public highways in the council's 2025 network; carriageway levels are the highways authority's 2019 levels survey".
2. None. No file ranks or scores parishes (checked csv, xlsx, geojson, pdf).
3. None that is purely a helper. Closest: link_reference_crosswalk_2019_2025.csv (maps 2019 link refs to 2025 link ids), which reads like a council's own renumbering table.
4. None. Annex A lists parish, code, access node only; no cut-off status or grant.
5. Guidance s.3: "Each qualifying parish receives a base grant of GBP 3,000 and a share of the rest of the GBP 30,000 in proportion to its households: the rest multiplied by the parish's households and divided by the households of all the qualifying parishes. Households are the dwellings on the council tax valuation list for the parish at 1 October 2026. Each grant is rounded to the nearest pound once its share is worked out." Fixes: population = qualifying parishes, base 3,000 each, remainder 3,000... (30,000 minus base is a function of the count of qualifying parishes), pro rata on the council tax all_dwellings at 1 Oct 2026, round once. Also s.2 fixes design flood = QRN25 D100CC, hospital node HBN-3224, 0.25 m ambulance depth, main-village access nodes in Annex A. Also s.3 "Any part of a parish's 2026 Flood Ready award still unpaid at 31 October 2026 is paid with the 2027 grant." and s.4 for dwellings (RD/RH classes, ground floor, peak stage above threshold, threshold fallback ground level + 0.15 m).
6. Mostly an analytical/reconstruction choice (which parishes are cut off needs joining carriageway levels via the crosswalk to the network, comparing with the storage-area stage, and routing), but the guidance states the 0.25 m rule, data sources and routing basis, so much of it reads as following a stated procedure. Deciding text: guidance s.2 sentences above. Nothing visible reads as a planted item beyond the ordinary mess (police UTC vs highways local closures, cancelled cheques, QRN23 vs QRN25 stages, Hawkesbridge West merger note).

## Flagged items
a. harmless, because "the model" is how a flood-modelling partnership and its funder would naturally refer to QRN25; the report has issue block, authors, checker, and the guidance cites model QRN25 run D100CC and the 2023 superseded model.
b. harmless, because it gives criterion, formula and the Annex A access nodes only; no parish is declared qualifying and no share or grant is given (GBP 30,000, 3,000 base are policy parameters). Mild caution: it is a very complete specification of procedure (see Q5/Q6), but not the answer.
c. harmless, because none ranks parishes on cut-off or grants: council tax gives dwelling counts by band; guidance gives parish codes and access nodes; geojson gives link attributes; closures give durations by road; survey gives property levels; model report gives storage-area stages by river reach (names like "Quarnell at Whinnerby" are area labels, not parish verdicts).
d. harmless, because it reads as the fund's own grant guidance (letterhead, trustee approval date, owner, version 3, replaces 2026 guidance, timetable, vouchers section) and the parishes appear as the fund's own annex, not as a note on the data. Slight tell: s.4 defines address register classes and threshold fallback in detail, which a funder would plausibly include but is data-descriptive in flavour.
e. Prompt: harmless, because it fixes what is asked, the files, and rounding only ("Households and dwellings are whole numbers, hours go to the nearest hour and amounts to the nearest pound"). No method stated; no data described. One minor thing: it names the parish set "the valley" and 1 in 100 design flood, which are question terms.

## Realism
Mostly none. Observations: both PDFs are tiny (about 5 KB, 2 pages, producer string equals the organisation name, no tagged structure, PDF 1.4, plain generator output) and lack a document-control block beyond a header line; the guidance PDF has "Page 1/Page 2" footers and a version line but no sign-off signature; the model report is 2 pages for a hydraulic model summary (thin for "report QCP-FM-25-04, issue 2", no figures/maps, no appendix), which is the main machine-built tell. The report's tables are neat and uniform. Metadata author equals org rather than a person while the body names persons. Different orgs' files do use different schemas (UK date format in highways, UTC ISO in police, GBP ledger with Finance creator), which reads as separate systems. The bank cheque file (3 rows) and stage CSVs (hourly, smooth) are tidy but plausible.
