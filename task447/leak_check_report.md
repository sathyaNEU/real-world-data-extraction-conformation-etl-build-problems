# leak check, task447

**Verdict: REVIEW.** 19 files read, 23 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: product, referral, placement, projection, decisive, acquisitions, carrier, capture, records, acquirer, method, history, claims, exhibit, earlier, sentence, reproduces, purchases, readable, repeats, appendix, acquisition, specialty, closed, placements

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `N25-014_notice_of_material_change.pdf`: golden figure 014 appears: ...ost Review under s. 153.86 Item Notice number N25-014 Received 8 October 2025 (complete on receipt) Fil...
- **REVIEW** `N25-014_notice_of_material_change.pdf`: candidate 'Brightwater Medical Group' sits beside decision vocabulary: ...Jacob Murillo, Halloran Pike LLP, for Ledgestone Health Debra Prince, Administrator, for Brightwater Medical Group, S.C. 6 October 2025 Exhibit A. Entities owned or controlled by Ledgestone Health Entity...
- **REVIEW** `apcd_extract_data_dictionary.pdf`: golden figure 014 appears: ...dictionary, request OHCCR-MO-2025-031 (notice N25-014) 1 The files apcd_op_facility_claims_2024.csv (la...
- **REVIEW** `ohccr_rule_4_preliminary_review.pdf`: golden figure 4.05 appears: ...t service in the projection year, estimated under 4.05; the part that moves is priced at the acquiring p...
- **REVIEW** `ohccr_rule_4_preliminary_review.pdf`: golden figure 4.06 appears: ...per cent and projects with the shares as stated. 4.06 Determination The projected increase is projected...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `N25-014_notice_of_material_change.pdf`: 3 of 25 stump-paragraph terms appear (carrier, exhibit, specialty); read whether the document names the move
- **REVIEW** `apcd_extract_data_dictionary.pdf`: 4 of 25 stump-paragraph terms appear (product, carrier, claims, acquisition); read whether the document names the move
- **REVIEW** `market_oversight_technical_appendix.pdf`: 8 of 25 stump-paragraph terms appear (product, records, history, claims, exhibit, appendix); read whether the document names the move
- **REVIEW** `ohccr_rule_4_preliminary_review.pdf`: 7 of 25 stump-paragraph terms appear (product, projection, history, claims, exhibit, appendix); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Read 1, isolated, on the stage 3 pack (before the appendix pins).

## 1. The sentence that gives the decisive step
No sentence announces it. The nearest is Rule OHCCR 4.04(b)/4.05, which is the filed method for the 2026 increase: "a referred service that the acquiring party offers, and that was not at one of the acquiring party's sites in the baseline, moves to the acquiring party's sites in the share expected for that service in the projection year, estimated under 4.05" and "The share that moves is the rise, after the acquisition, in the share of those services at the acquiring system, as a share of the services that were elsewhere before it." These are stated as the rule's method, in neutral rule language, with no warning about a shortcut. 4.06 gives the threshold ("$2,000,000 or more ... proceeds to a cost and market impact review under rule OHCCR 5"). The execution is so fully written that rule application, not judgement, carries it (author's concern, not a leak). No file says "expected share", the 2021-23 extract's purpose or a naive alternative in a way that names the trap. The data dictionary's description of the 2021-2023 file ("whose referring provider is a physician of a practice acquired by Ledgestone Health or Wolf River Health from 2021 to 2023") points a solver to the 4.05 population, but it is a data description.

## 2. Files that rank or answer
None. No file contains the increase, the call, a per-candidate ranking, or either exhibit's figures. Exhibit C holds rates (inputs); network_tier_placements, HCRIS and the MA file are context or distractors with no shares or totals. The notice says only "eighteen physicians" and lists them (Exhibit B); it states no spending.

## 3. Files that exist only to help the analyst
None clearly. Closest: export_manifest.csv (row counts, source, produced date; a real APCD request usually ships a transmittal, so plausible, but it lists "rows" and file descriptions that tell the solver which file is for what, e.g. "referred by physicians of practices acquired 2021 to 2023"). The data dictionary section 5 ("Provider taxonomy (NUCC) used in these files") and section 6 ("ZIP codes and counties") are convenience tables an APCD manager might plausibly include. apcd_product_reference and cms_opps_clfs (compiled "as CMS addenda as compiled by OHCCR", only 21 codes, exactly Exhibit C's codes) look curated for the task but are defensible as office reference tables.

## 4. Figures or names that read as the answer
No figure is the answer. Points that read as author's intent: the Exhibit C row set is exactly the code set in the claims (21 codes), and the Bayfield terms sheet lists "CPT/HCPCS in the category (Ledgestone services)" which matches the 21 codes one for one; the notice's emphasis that Brightwater clinics "will not become departments of a Ledgestone hospital and will not bill facility fees" and "Brightwater's physicians will continue to see their patients at the same clinics" is stated as fact and settles the trap-adjacent questions (no facility fee uplift for the clinic itself, same members), mildly steering. The "$2,000,000" threshold is stated; the final increase relative to it is not.

## 5. Filed sentences that fix the main figure and the exhibits
Main figure (2026 increase), literal execution:
- 4.02(b): "a commercial product is one the database's product reference lists with line of business Commercial, fully insured or self-funded" -> the 11 non-MA products in apcd_product_reference.csv (MA products BMH-MA05, CBH-MA01, NBH-MA03 out; tiered products are in).
- 4.02(c): "spending means the allowed amount on a claim line ... taken on the latest version of the line and net of voids" -> apply replacements (code 7) over the claim named, drop voids (code 8, negative lines).
- 4.02(e): "a physician of a practice is a physician billing under one of the practice's taxpayer identification numbers on the date of service" -> Brightwater TIN 39-9943822, physicians per NPI reassignment history / professional claim billing TIN on DOS.
- 4.03: "The baseline year is the most recent calendar year whose claims the database holds paid at least six months after its end on the date the notice is complete" (complete 8 Oct 2025; 2024 paid through 31 Aug 2025 -> 2024). "commercial professional services billed under its taxpayer identification numbers and its commercial referred services ... with dates of service in the baseline year and paid on or before 30 June of the following year" -> 2024 DOS, paid_date <= 2025-06-30.
- 4.04: "Prices and volumes are not trended"; (a) professional services re-priced "at the acquiring party's professional rates filed with the notice" (Exhibit C Professional sheet, per carrier, by CPT/modifier); (b) offered-and-not-already-at-acquirer referred services move "in the share expected for that service in the projection year", the moved part priced at the Exhibit C facility rate per carrier (Bayfield at percent of Medicare), the remainder keeps baseline allowed amount; (c) others keep baseline. 4.02(g) "a system offers a service when its outpatient sites bill that procedure code", 4.02(h) projection year = 2026.
- 4.05: expected share = for physicians who "joined health systems in the state by acquisition, as the market oversight unit's technical appendix defines joining" (A5), with referred services both before and after, services counted only if offered by the joined system; share that moves = rise in the share at the acquiring system, "as a share of the services that were elsewhere before it"; "states each expected share in whole per cent and projects with the shares as stated". Population: 2021-2024 referred services of acquired physicians (Ledgestone and Wolf River acquisitions, from register notices), per service (procedure code).
- 4.06: increase = projected less baseline spending; threshold $2,000,000; prompt: one decimal, millions.

Exhibit 1 (A2), literal: services in lines imaging (70010-76999, 77046-77067) / endoscopy (43235-43270, 45378-45398) / arthroscopy (29805-29999) "that facilities in the database provided to commercial members residing in the county, with dates of service in the year. Each unit of a procedure code that a facility provided to a member is one service. A member resides in the county holding the ZIP code on the member's eligibility span that covers the date of service." Count = quantity units (net of voids/replacements), 2024 commercial OP facility claims, county from the eligibility-span ZIP mapped by dictionary section 6, Manitowoc and Kewaunee only. "A practice's referred share is the part of those services whose referring provider is a physician of the practice" -> Brightwater share = units with referring NPI billing under 39-9943822 on DOS / all units in that county and line; one decimal per cent.

Exhibit 2 (A3), literal: visits are "services coded 99202 to 99215 that physicians of the specialty rendered in person to commercial members at locations in the two counties, with dates of service in the year; a visit by telehealth (place of service 10, or modifier 95) is not an office visit." Primary care = family medicine, internal medicine, pediatrics; others gastroenterology, orthopaedic surgery, cardiovascular disease. "A practice's or a system's share is the part of those visits billed under taxpayer identification numbers it owns or controls, read from the register as in A4" (owned, merged into, affiliated-controlled; CIN participation excluded; A4 MD/DO only, NPs/PAs not counted). Share = line units/visits in 2024 professional file, POS not 10, by specialty (rendering taxonomy), billing TIN grouped to Brightwater (39-9943822) and to Ledgestone (Health, Medical Group and its controlled/merged TINs), over all commercial visits of that specialty in the two counties; one decimal.

## 6. Realism / LLM-looking
- Names: Ledgestone, Brightwater, Cedarbrook, Norbridge, Heartland, Bayfield, Kinnickinnic, Wolf River, Lakefront are plausible-but-stylised invented names; Exhibit B physician names (Sydney Delgado, Loretta Ford, Clayton Brown, Michele Long) are realistic.
- Practice NPIs: reported values like 1042929160 pass as NPIs; "Kinnickinnic" in Manitowoc/Sheboygan is a Milwaukee-area stream name, fine.
- Facility_directory: the Ledgestone Manitowoc Outpatient Center shares CCN 520147 with the Green Bay hospital; correct for a department.
- Round carrier claim IDs (CB24001828078, NB-2406798012) are consistent. Rule text cites "Register February 2023 ... s. 153.85" and notice "s. 153.86": statute numbers in Chapter 153 are real (153.85/153.86 are not real material-change provisions); acceptable as fiction.
- Wage-adjusted CBSA 24580 is the real Green Bay CBSA. OPPS/CLFS amounts: MPFS(mammography) payment system label oddly placed; status indicator "Q3" and "T" plausible. Exhibit C Cedarbrook rate for 29881 = 4945 exactly (round), many rates are clean multiples of CMS (e.g. 1716 = 6.75 x 254.37 -> round), a visibly formulaic pattern ("one chargemaster" at fixed multiples across carriers 1.00/1.06/1.12/0.90). A real rate sheet would be less regular.
- Bayfield sheet gives 4.05, 1.55, 1.6, 1.15, 2.3 under "Percent of Medicare": these are multipliers (405 per cent etc.), not percent. Reads as an authoring slip or deliberate unit trap.
- HCRIS extract with 6 rows and CCN 520147 for two sites, fiscal year ends all 2023-12-31: tidy, short.
- Data dictionary "Prepared by Samantha Abbott" and "do not attempt re-identification" fine.
- The notice says "Received 8 October 2025 (complete on receipt)" but certification dated 6 October and "Exhibit C" produced 7 Oct; fine.

## 7. Places two careful readers could differ
1. "Percent of Medicare" in the Bayfield sheet (4.05 as 4.05 per cent vs 405 per cent); the Cedarbrook rates relative to Medicare (about 6.75x) and the claims' own Bayfield allowed amounts would settle it; no filed sentence does. Also "the Medicare amount for the service in the calendar year of service": the only Medicare file is CY2025 and the projection year is 2026; a reader may use CY2025 (not trended) or ask for CY2026. 4.04 "Prices ... not trended" settles toward 2025.
2. Exhibit 1 "Each unit of a procedure code ... is one service": quantity vs line count; voids carry negative quantity so net-of-void summation works, but A2 does not itself say replacements/voids are netted (4.02(c) defines that for "spending" only) and gives no paid-date cut-off for exhibits (2024 file paid through 31 Aug 2025 vs the 30 June 2025 cut of rule 4.03). Two readings differ for claims paid 1 Jul-31 Aug 2025. No file settles it.
3. Exhibit 1 residence: the eligibility spans split at every change of product, benefit period and address, and a member's DOS can fall in a gap or overlap; which span covers is by DOS, stated. Kewaunee ZIP 54201 and 54216/54217 are listed in dictionary section 6; the professional file also uses 54228 (Manitowoc). OK.
4. Exhibit 1 "commercial": A2 says "commercial members", whose definition is 4.02(b) (rule), appendix says terms in rule 4 carry the same meaning; MA claims are in a separate file so risk is low. Whether self-funded ASO (Lakefront) is in commercial: yes by 4.02(b).
5. Exhibit 1 lines: the prompt names only three lines (imaging, endoscopy, arthroscopy) while A1 has five; fine. Imaging band 70010-76999 includes codes such as 76700 and may include 77067 and others; echocardiography is a separate line so 93306 excluded; a reader should not include it.
6. Exhibit 2 "physicians of the specialty": specialty by claim rendering taxonomy (dictionary section 5), by carrier_provider_file primary_taxonomy, or by Exhibit B listing; Brightwater's two GI doctors are "Internal Medicine, Gastroenterology" and could be counted as internal medicine (primary care) or GI; 207RG0100X on claims probably decides, but internal-medicine physicians with 207R00000X rendering cardiology/GI could also be re-assigned via the carrier file. Pediatrics (208000000X) never appears in claim taxonomy.
7. Exhibit 2 "locations in the two counties": service_facility_zip vs billing_provider_zip (billing zip 53081 Sheboygan for Kinnickinnic Physician Network while service is in 54241); appendix says location, so service ZIP.
8. Exhibit 2 "billed under TINs it owns or controls, read from the register as in A4": register dates (effective_from) vs date of service; Ledgestone share for 2024 depends on which affiliates (Mishicot 2019, Fox River 2020, Baird Creek 2022, Cedar Ridge 2023, Oak Hollow and Harborview merged) count by DOS; Exhibit A of the notice omits merged TIN practices but includes them via Ledgestone Medical Group; Harbor Lakes (CIN) excluded. Exhibit A lists "Ledgestone Fox Cities Hospital" and Medical Center only: hospital TIN 39-2310616 professional billing (POS 22) counts. A visit at POS 22 or 24 "in person" at "locations in the two counties" is in; a reader might restrict to POS 11 as "office visits".
9. Exhibit 2 denominators: "of the commercial office visits in those two counties" includes visits by NPs and PAs (taxonomy 363L/363A); A3 says services "physicians of the specialty rendered" and A4 excludes NP/PA, so NP visits are out of the denominator; a reader might keep them. Nurse practitioners' lines are in the file (819 rows), a natural fork; appendix text settles it.
10. Main figure: 4.05 "the rise ... as a share of the services that were elsewhere before it" per service (code) vs per service line vs overall; "for that service" in 4.04(b) suggests per procedure code. Rounding to whole per cent before projecting is stated. Acquisition-joining test (A5, 90-day rule, "leaving none billing under the practice's number") is stated but intricate.

## Review lines
1. Notice "014" figure: harmless, it is the notice number N25-014 matched as a digit string.
2. Brightwater beside decision vocabulary in the certification block: harmless, signature line of the filing party; no figure or call.
3. Data dictionary "014": harmless, notice number in the request title.
4. Rule "4.05" figure: harmless, a section cross-reference, not a number in the answer.
5. Rule "4.06" figure: harmless, a section heading.
6. Notice, 3 of 25 stump terms (carrier, service, practice): harmless, generic nouns; the notice describes the transaction and names no method or shortcut.
7. Data dictionary, 7 of 25 terms: harmless, field and file descriptions; it says the 2021-2023 file holds referrals of acquired physicians' practices, which is a plain description of the extract and does not name the move or the estimate.
8. Technical appendix, 8 of 25 terms: harmless, it defines service lines, counts and who joins by acquisition (A5), stated as definitions as a real unit appendix would; it does not say how the share is applied.
9. Rule 4, 9 of 25 terms: harmless on leak grounds (the rule is the filed method and necessarily states the projection and share-moving procedure in neutral terms, no hint about a wrong path). Author note: 4.04 to 4.05 is written so fully that the decisive step is rule application; that is a design concern, not a leak.

Read 2, isolated, on the final pack (after the appendix pins).

1. Decisive step: no sentence names it. Rule 4.04(b) and 4.05 state the mechanism neutrally ("a referred service that the acquiring party offers, and that was not at one of the acquiring party's sites in the baseline, moves ... in the share expected for that service in the projection year, estimated under 4.05"; "The share that moves is the rise, after the acquisition, in the share of those services at the acquiring system, as a share of the services that were elsewhere before it"). That is the method as a rule, not an announcement of the step. The notice's "Brightwater's physicians will continue to see their patients at the same clinics ... will not bill facility fees" is context. Threshold: 4.06 "$2,000,000 or more". No file says "the increase turns on referral steering" or similar.

2. No file ranks or answers. Exhibit C is filer rates (inputs). cms_opps_clfs, hcris, network_tier_placements are inputs/distractors with no computed outputs. The two exhibits' figures appear nowhere.

3. Nothing is analyst-only. export_manifest.csv is plausible as an extract transmittal (it does give row counts). All files read as office/APCD records. network_tier_placements_2020_2026.json, hcris and cms_opps_clfs are context/distractor but plausible office files.

4. Nothing reads as the answer. Only the $2,000,000 threshold (rule) and "eighteen physicians" (matches Exhibit B's 18). Both are context.

5. Main figure: Rule 4.06 "The projected increase is projected spending less baseline spending", with 4.03 baseline (commercial professional services billed under the practice's TINs plus commercial referred services, 2024 DOS, paid on or before 30 June 2025, allowed amount, latest version, net of voids), 4.04 projection (professional priced at Ledgestone Medical Group rates; offered-and-not-already-at-acquirer referred services move in the 4.05 share, priced at Ledgestone facility rate, rest keep baseline allowed; others keep baseline), 4.05 shares "in whole per cent ... projects with the shares as stated", from physicians "who joined health systems in the state by acquisition ... where the database holds their referred services both before and after", "only the services offered by the system he or she joined are counted". Literal execution: the 2025 Exhibit C rates are applied to 2024 services (4.02(h) projection year 2026, "Prices ... not trended"), the expected share per service (procedure code) is computed from the 2021-2023 + 2024 facility extracts via appendix A5 joiners, rounded to whole per cent, and the dollar difference is totalled and stated in $ millions to one decimal. The Bayfield terms sheet gives percent of Medicare, so the Bayfield facility rate needs OPPS/CLFS CY2025 (4.04 says "calendar year of service", ambiguity for a 2026 projection; literal reading is 2025 file).
   Exhibit 1 (services): Appendix A2 "the services the county's residents received are the services in the line that facilities in the database provided to commercial members residing in the county, with dates of service in the year, whenever paid. Each unit of a procedure code that a facility provided to a member is one service, read on the latest version of the claim line, net of voids. A member resides in the county holding the ZIP code on the member's eligibility span that covers the date of service. ... referred share is the part of those services whose referring provider is a physician of the practice." Literal count: sum of quantity (units, not lines or claims) on the latest version, voids netted, by member's ZIP on the covering eligibility span (not the facility ZIP), mapped to county via dictionary section 6, lines by A1 CPT ranges (Imaging, endoscopy, arthroscopy), Brightwater physicians per rule 4.02(e)/A4 (billing under a Brightwater TIN on the DOS, via NPI reassignment history and the notice's Exhibit B; the hospital-based services count whenever paid, not only to 30 June).
   Exhibit 2 (office visits): A3 "the services coded 99202 to 99215 that physicians of the specialty rendered in person to commercial members at locations in the two counties ... read on the latest version of each claim; a visit by telehealth (place of service 10, or modifier 95) is not an office visit. A physician's specialty is the classification of the physician's NUCC taxonomy: ... A practice's or a system's share is the part of those visits billed under taxpayer identification numbers it owns or controls, read from the register as in A4". Specialty field: the appendix does not name a file. The literal reader takes the taxonomy "submitted with the claim for the rendering provider", i.e. rendering_provider_taxonomy on the professional claims (dictionary section 3 and section 5), with carrier_provider_file.primary_taxonomy and Exhibit B "Specialty" as competing sources the appendix does not rule on. Counting: each service line coded 99202-99215 is one visit; whether a visit is a unit or a line is not defined in A3 (only A2 defines unit counting), so a literal reader counts lines/quantity unclear (flag: A3 does not say quantity). Shares are of all commercial visits in the two counties in the specialty; the TIN is read as of... the date is not stated for the register in A3 (A4 says "on a date"), a literal reader uses the DOS.

6. No sentence flags special handling beyond version netting. Dictionary: "Each line carries the version the carrier last submitted for it: a replacement (code 7) supersedes the claim it names, and a void (code 8) cancels the claim it names, its lines carrying negative quantities and amounts. The database does not remove superseded or voided lines." That is version netting only. Section 5 and the 2.4 layout mapping are plain layout notes. Nothing says certain claims/fields (taxonomy on claims, layout 2.4 date/TIN formats, tiered products) need special treatment. The only near-hint: "the taxonomy code submitted with the claim for the rendering provider" (phrase "submitted with the claim" is neutral).

## Review lines
1. notice "014" in N25-014 header: harmless, the notice number, not a figure.
2. notice 'Brightwater Medical Group' beside signature block: harmless, the party's name in the certification.
3. dictionary "014" in notice number: harmless, same notice number.
4. rule "4.05" cross-reference: harmless, a rule section number.
5. rule "4.06" heading: harmless, a rule section number.
6. notice stump terms (carrier, exhibit, specialty): harmless, the notice only describes the transaction and Exhibit B lists specialty as filer data; names no move.
7. dictionary stump terms: harmless, layout and field definitions; only version netting is stated, no instruction on the decisive step.
8. appendix stump terms: harmless, it defines exhibits and joining by acquisition as method definitions, does not name the decisive step or the wrong path (one open point noted in Q5: A3 does not say which taxonomy source or whether quantity counts, a determinism matter rather than a leak).
9. rule stump terms: harmless, 4.04/4.05 state the projection mechanics as rules; they do not announce which step is decisive.

### Read after the prompt repair (2026-10-14, isolated Sonnet reader at medium effort: "how much the deal will change commercial spending")

- **Q1** no sentence names a pitfall or an easy route; the nearest are rules 4.04(b) and 4.05, the filed method for the share that moves.
- **Q2 to Q4** none; the only threshold is 4.06's $2,000,000, a rule and not a result.
- **Q5** rules 4.02(c) to 4.06 and appendix A2 to A5 quoted; one visible difference noted (A2 and A3 count exhibit services "whenever paid" while 4.03 cuts the baseline at 30 June), the two governing different figures.
- **Q6** the reader judged the main call mainly rule application (4.03 to 4.06 with appendix A2 to A5, the 4.05 share definition deciding), as read 1's author note did; the judge's Gate H read it analytical (the share follows each patient's tier for the acquirer in the projection year). An open design concern for the author, not a leak and not moved by the repair.
- **Prompt read** "how much the deal will change commercial spending" is neutral; nothing presupposes the answer; none, zero or a fall is a grammatical answer to every question and ask.
- **REVIEW lines** all harmless.

