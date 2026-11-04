# leak check, task285

**Verdict: REVIEW.** 18 files read, 38 golden figures and 27 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: network, envelope, guidance, village, storage, isolation, survey, report, sentence, silent, council, levels, standard, stages, descriptive, decisive, section, moment, reflex, surveyed, golden, analyst, closures, deepest, reachability

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: \bthe model\b x2: ...ghways authority's 2019 levels survey, which covers every road inside the model's floodplain. The hospital is reached at its emergency department ent...
- **REVIEW** `quarnell_flood_model_report_2025.pdf`: \bthe model\b x5: ...llin Beck, Ravelsby Brook and Lunnerby Beck. This summary records how the model was built, the hydrology, the calibration and the design results; the...

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: carries 17 of 18 distinctive words of the committed call: 'Share the 2027 Flood Ready budget between the six parishes the design flood would cut off from Hawkesbridge General Hosp'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: 7 of 25 stump-paragraph terms appear (network, guidance, village, storage, survey, council); read whether the document names the move
- **REVIEW** `quarnell_flood_model_report_2025.pdf`: 8 of 25 stump-paragraph terms appear (storage, survey, report, council, levels, stages); read whether the document names the move

## 6 ranking artifacts (REVIEW 8, INFO 3)
- **REVIEW** `council_tax_dwellings_by_parish_oct2026.csv`: names 5 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flood_ready_fund_guidance_2027.pdf`: names 7 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flood_warning_areas_2025.geojson`: names 4 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `highways_network_2025.geojson`: names 9 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `highways_road_closures_jul2021.csv`: names 15 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pfr_property_survey_2022.xlsx`: names 5 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `quarnell_flood_model_report_2025.pdf`: names 4 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `storage_areas_QRN25.geojson`: names 3 of 27 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `address_register_extract_oct2026.csv`: names 5 of 27 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `police_road_closures_jul2021.csv`: names 4 of 27 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `rest_centres_2026.xlsx`: names 6 of 27 answer-set candidates; confirm it does not rank them on the decision question

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

### Second read, on the ask-layer repair cut

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 f2bd06c463b2004bb7f83a5e133a0550081cdad6d81bc196be2f156f5c48591b), after the prompt, the guidance and the model report changed. Sweep 4's lines were kept out of the brief and ruled in the main thread (neither document says when one storage area peaks or drains relative to another). Verdict: no leak. Question 6 again reads the guidance as a near-complete procedure whose one unfiled judgement is how each link's stage is taken through the event (time-varying against peak); weighed against Gate H with the judge, which classes that step analytical.

# Leak read, task285 (read and quote only; nothing solved)

1. Decisive step stated: flood_ready_fund_guidance_2027.pdf s2: "A village is cut off when it has no road route to the hospital that an emergency ambulance could use. The county ambulance service's crews will not take a vehicle along a carriageway where floodwater stands deeper than 0.25 m." plus "The hospital is reached at its emergency department entrance on Infirmary Road (network node HBN-3224). Each parish's main village and its access point on the network are listed in Annex A." It states the rule and inputs, not a ranking. Mild concern: it names the depth test, the model run, the node and the access nodes, so the cut-off call is an executable procedure.
2. Ranking/scoring of candidates on the prompt's question: none. (No file lists cut-off parishes, grants or depths per road.)
3. Files existing only to help the analyst: link_reference_crosswalk_2019_2025.csv (columns "link_ref_2019, link_id_2025, from_chainage_m, to_chainage_m, change_type" with values "renumbered" / "split 2024 junction") is a bridge between the 2019 survey and the 2025 network; it reads as a highways authority's own cross-reference. Otherwise none; section 4 of the guidance ("The record of a building of flats is not a home...") is the fund's own rule.
4. Figure/name reading as the answer: none. The nearest are the fixed parameters in the guidance ("GBP 30,000", "base grant of GBP 3,000", "0.25 m", "0.15 m"), which are inputs.
5. Literal sentence: guidance s3: "Each qualifying parish receives a base grant of GBP 3,000 and a share of the rest of the GBP 30,000 in proportion to its households: the rest multiplied by the parish's households and divided by the households of all the qualifying parishes. Households are the dwellings on the council tax valuation list for the parish at 1 October 2026. Each grant is rounded to the nearest pound once its share is worked out." Literal result: population = qualifying (cut-off) parishes only; unit = council-tax dwellings (all_dwellings in council_tax_dwellings_by_parish_oct2026.csv); base 3,000 each plus (30,000 minus base total... "the rest of the GBP 30,000") pro rata; round once at the end. Also s4: voucher home = address-register home whose storage-area peak stage exceeds the threshold (survey level for the home or its building, else ground level + 0.15 m), flats above ground floor excluded. Also s3 last paragraph: unpaid 2026 balance at 31 Oct 2026 added to the grant.
6. What decides the main answer: mostly following a stated rule or procedure (cut-off defined by 0.25 m depth on the public-highway route to node HBN-3224, with levels from the 2019 survey, crosswalk to 2025 links, stage from QRN25 D100CC), with data joining as the mess layer. Deciding sentence: guidance s2 "A village is cut off when it has no road route to the hospital that an emergency ambulance could use. ... deeper than 0.25 m." and "carriageway levels are the highways authority's 2019 levels survey". Any analytical choice (e.g. the time dimension, whether peak vs hourly stage, which storage area a link sits in) is not signalled by any filed sentence; that residual judgement is the only non-rule element I can see. Nothing looks planted.

## Flagged items
a. Harmless, because "the model" in both PDFs is the partnership's own name for QRN25 ("QRN25 replaces the 2023 model (QRN23) as the partnership's model...") and the fund's guidance cites it as a planning input; it reads as organisational usage, not exercise vocabulary.
b. Harmless, because it gives no qualifying-parish list and no parish share; the only parish-linked content is Annex A (parish, code, access node) and rules. Wording is the fund's procedure, not an answer. (It does hand over the method, see Q5/Q6, but not a result.)
c. Harmless, because none ranks or scores parishes on the question: council tax file is dwellings by band; guidance has Annex A nodes; highways_network_2025.geojson has only LINK_ID, ROAD_NAME, nodes, length (no parish values); closures csv is a duty log; the survey xlsx has levels per property; the model report gives peak stage per storage area, not per parish (storage-area names embed village names, e.g. "Quarnell at Tolmarsh", but that is a hydraulic fact, not a cut-off ranking).
d. Harmless, because it is a signed-off policy document (approval date, owner, version 3, "Replaces the 2026 guidance", trustees' signatures, next review); it speaks to applicants and trustees, not to an analyst about files. Only the line "Hawkesbridge West parish was merged into Hawkesbridge North on 1 April 2025" is data-explaining, but it is a natural annex footnote for a fund.
e. Harmless, because prompt.txt only fixes what is asked, the output names, and rounding ("Households and dwellings are whole numbers, hours go to the nearest hour and amounts to the nearest pound"). It does say "mark each parish cut off", "the 1 in 100 design flood", "closed by highways or police" and "unpaid at 31 October 2026", which fix the estimand, not the method. It does not describe the data.
f. Harmless, because columns "closure_ref, road_number, location, barrier_position, closed_bst, reopened_bst, duty_officer, reason" and reasons like "flood water on carriageway" / "road closed, diversion in place" read as a duty log; nothing says how to count overlapping barrier rows, route closures or police overlap. (Duplicate closure_refs reused for different roads, e.g. HW21-07-04, look like genuine log untidiness.)

## Realism
- flood_ready_fund_guidance_2027.pdf: letterhead, approval line, version, page footers, signatures present; metadata Author "Gareth Johnston" matches the stated owner; no Producer/Creator fields, 5 KB, 2 pages is plausible for a short guidance. Tell: PDF creation date 24 Sep 2026 equals approval date, and empty Producer/Creator (minor, scrubbed metadata).
- quarnell_flood_model_report_2025.pdf: "Issue 2, February 2026" with revision table, preparer/checker initials, appendices listed as separate, limitations section; metadata Title "QRN25 summary report QCP-FM-25-04", Author "Eleanor Rose", created 16 Feb 2026. Tell (minor): 2 pages for a model summary is thin but it declares itself a summary; table headers repeat across page break without being cut mid-row artefacts. Also storage area areas and "revitalised rainfall-runoff method" read fine.
- flood_ready_ledger_2026.xlsx: sheet named "2025 awards b-f" is an odd name (reads as a leftover hint of a "balance brought forward" label); mild. Ledger and bank_cancelled_cheques cross-reference consistently (cheques 004817, 004903).
- Logs: highways closure log and police log (UTC vs BST) are irregular in times and officers; not too uniform. The three-row route closure sharing identical 05:40/20:41 times is plausible for a route closure.
- Overall: none that clearly reads as machine-generated; only the minor items above.

### Third read, on the pass-2 closure cut

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 79c8cbf7d9ce5b0cc9f00c1b7a9ce62fbf58506971d41c6bea4d3fee29700301), after the model report's datum sentence, the guidance's payment rule and the register's class descriptions changed. Verdict: no leak; items a to d harmless; one realism tell (axis-aligned polygons and round-hundred coordinates in the three geojson files) goes to the generator.

# Leak read, task285 r3 (read and quote only; nothing solved)

1. Decisive step: no sentence announces it. Nearest is guidance section 2: "A village is cut off when it has no road route to the hospital that an emergency ambulance could use. The county ambulance service's crews will not take a vehicle along a carriageway where floodwater stands deeper than 0.25 m." This is the Fund's stated criterion, not a hint about a trap.
2. Ranking/scoring files: none. The stage CSVs, levels survey and network are raw data. The QRN25 report section 6 lists peak stage per storage area but does not rank parishes or candidates.
3. Files that only help the analyst: link_reference_crosswalk_2019_2025.csv (2019-to-2025 link id map, a plausible highways-authority table) and council_tax_dwellings_by_parish_oct2026.csv (feeds households). Neither names an answer. Annex A of the guidance (parish to access node) is also a convenience but reads as the Fund's own annex.
4. Answer-like figures or names: none. The prompt states the 1 in 100 flood and the hospital, and the guidance repeats them. No cut-off list, grant, unpaid balance or hours total appears anywhere.
5. Literal-fixing sentences:
 - Guidance s3: "Each qualifying parish receives a base grant of GBP 3,000 and a share of the rest of the GBP 30,000 in proportion to its households: the rest multiplied by the parish's households and divided by the households of all the qualifying parishes. Households are the dwellings on the council tax valuation list for the parish at 1 October 2026." Fixes a 3,000 base plus a pro-rata of the remaining 30,000 less base amounts (3,000 times the qualifying count; the count itself is the model's to find), on the council tax dwellings column at 1 Oct 2026, rounded once to the pound.
 - Guidance s2: cut off = no ambulance-usable route to node HBN-3224 on the 2025 network, carriageway impassable where water is deeper than 0.25 m, design flood = QRN25 D100CC, carriageway levels = 2019 levels survey, access point per parish from Annex A.
 - Guidance s4: "The design flood reaches a home when the peak stage ... is above the home's threshold level" with the threshold hierarchy (survey threshold for the home or its building, else ground level plus 0.15 m); flats above ground floor and the building record excluded.
 - Guidance s3: "Any part of a parish's 2026 Flood Ready award still unpaid at 31 October 2026 is paid with the 2027 grant." Fixes the award (incl. variations) less payments to 31 Oct 2026, payee being parish council, clerk or village body.
6. What decides the main answer: mainly an analytical/GIS-hydraulic composition (network routing under flood depth, joining 2019 levels to 2025 links via the crosswalk, per-hour peak stage in a storage area, datum alignment). There is a mild data-semantics component (mAOD vs the datum in report s5). The guidance states the rules, so parts read as rule application. Files carrying the decision: guidance s2 plus the levels survey, crosswalk, network and QRN25 stage CSV. Nothing looks planted. Note guidance s2 says the survey "covers every road inside the model's floodplain"; harmless.

## Items
a. harmless, because report s5 only states the model's datum ("Stages are in metres above Ordnance Datum Newlyn. Survey levels ... taken to the Quarnell Navigation Datum, which lies 0.42 m above Ordnance Datum Newlyn, were converted before use"). It names no register or survey file and does not say how to treat any shipped file's levels. (Mild observation: it supplies the 0.42 m figure, which a solver needs only if some shipped levels are on QND. Report s5 does not say which. highways_levels_survey_2019.csv column is level_mAOD, and no shipped file mentions QND.)
b. harmless, because s3 is the Fund's own general rule ("The Fund pays an award to the parish council, or on its behalf to its clerk or to a village body for the parish's flood preparations"), with no parish, payment or ledger row named.
c. harmless, because CLASS_DESC pairs with the CLASS code in the OS AddressBase-style classification wording ("Residential, Dwelling, Terraced", "Property Shell"), as a real extract's own field. It is not an analyst note.
d. harmless, because it names no qualifying parish, no parish share and no grant figure. It gives only the Fund's total, base amount, formula, threshold rules and the Annex A list of all 18 parishes with access nodes. Shared wording with the prompt is the criterion, not a result.

Realism: none. Minor tells only: round hand-made look of storage-area polygons (storage_areas_QRN25.geojson and flood_warning_areas_2025.geojson are axis-aligned near-rectangles with round coordinates) and highways_network_2025.geojson coordinates in round hundreds. They read as simplified synthetic geometry rather than an organisation's system output.
