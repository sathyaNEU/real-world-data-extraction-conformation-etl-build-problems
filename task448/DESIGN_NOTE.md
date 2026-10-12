# task448 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task448.json`, registered 2026-10-12 (guard WARN repeat.gate_g, answered below).
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / Data Extraction & Conformation (ETL). The ETL lane has six client task types; this seed's world (HMDA lender volumes) sits in administrative-data quality, where the deciding quantity, each lender's true volume when the register misses whole producers, is what official statistics estimates by dual-system estimation.
- **Seed:** ET05 (`analytical_tasks/07_data_extraction_conformation/ET05_hmda-lender-market-share-composite-key.md`), header and Situation only: the HMDA world, a lender league table and a decision taken from it. The seed's two-part-key and purchased-loan traps are data semantics and rule application, so neither is used; the pitfall is re-found from the data.
- **Shape:** 01, ranked list under a cap (the five lenders recruited first, in order, each with its two-year volume).
- **Strategy:** composition_mix. The second list's capture is a mix over recording routes, and the registered producers and the missing producers hold different mixes.
- **World:** the Prairie Lantern Housing Fund, a statewide homeownership nonprofit in Kansas, runs a down-payment assistance program through participating lenders. For 2027 it extends the program to eight non-metropolitan central Kansas counties (Saline, McPherson, Dickinson, Marion, Rice, Ottawa, Ellsworth, Lincoln) and recruits first the five lenders that made the most home-purchase first-lien mortgages there in 2024 and 2025. HMDA covers a depository only if it has an office in a metropolitan area, so local banks and credit unions headquartered in these counties never report. The fund buys a county recorder vendor's purchase-money mortgage file (Venridge Property Data) for the eight counties.
- **Forum and forcing event:** board_of_directors (the board approves the 2027 recruitment list), vote_or_meeting (the December board meeting). Organisation nonprofit_or_charity, role research_desk. Personas from `guard.py names --geo "United States" --seed 448`: Laura Cohen (research), Maxwell Ewing (director).
- **Data-native sentence:** HMDA drops every lender with no office in a metropolitan area, and the recorder vendor flags a purchase mortgage only when it can pair it with the deed, which it does for closings that record the two in one package and often fails to do for lenders that record their own mortgage afterwards, so the lenders the register misses are the ones the second list undercounts.
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, census-register-administrative-data-quality 1 (dual-system estimates within post-strata, after erroneous enumerations): one pooled Lincoln-Petersen on raw counts is biased when capture is heterogeneous; here the register's misses are whole producers, so the second list's capture measured on the overlap is carried to them by recording route, and the erroneous enumerations are the vendor's non-purchase pairings and re-recordings.
  - `stumping/references/strategies.md` Part 6: a move visible in the schema and a reflex correction are dead, so the stratifier is no column (route is built from the paired recording dates) and county, charter and year stratification each land wrong.
- **Same-puzzle and abstraction:** gap population, pattern E and Gate G method_or_model_selection repeat seven older builds (task30, task31, task500 v2, task53 v2, task57 v19, task69 v2, task76 v2), each differentiated on the card. Nearest drivers: task62 (a unit's count completed from a second register that is complete for what it holds, a union), task229 v3 (a counting point's pass rate), task230 v2 (a detector's hit rate falling as targets get rarer). Stripped of nouns, none has a register missing whole producers completed from a second list whose capture differs by filing route and is measured only on the producers both lists hold.
- **Guard WARN repeat.gate_g (task185):** task185 selects a value-dependent conversion between two measuring devices for an anomaly count; here the selection is a coverage estimator's post-strata. Different mechanism, same Gate G label.

## Default path

1. Read the shortlist of twelve lenders and resolve each to the lender register's LEI; seven have records in the eight counties in the HMDA file, five do not.
2. For the seven reporters, count originated loans (action_taken 1) for home purchase (loan_purpose 1), first liens (lien_status 1), on properties in the eight counties, in the 2024 and 2025 Kansas loan-level file.
3. For the five that do not report, count their purchase-money mortgages in the Venridge file for the eight counties, closed in 2024 and 2025, after dropping re-recordings, second mortgages, seller-carried notes and the refinances the vendor paired with a quitclaim deed.
4. Rank the twelve and recruit the five largest.

Ends on: recruit Corvane Home Loans, Halverd Mortgage, Arkhaven Bank, Weyrauch State Bank and Shunga Valley Bank (311, 228, 182, 154 and 151), with Tessaline Home Lending sixth (141).
Golden: recruit Corvane Home Loans, Weyrauch State Bank, Halverd Mortgage, Mennwell Credit Union and Arkhaven Bank (310, 260, 230, 200 and 180), with Shunga Valley Bank sixth (150).

## Stump sentence

The default path recruits Shunga Valley Bank at 151 instead of Mennwell Credit Union because step 3 counts the five non-reporting lenders at their rows in the Venridge file, and the file holds 60 per cent of a lender's purchase mortgages when the lender records its own mortgage after the deed (97 per cent when the closing records the two together); measured on the reporters within each way of recording and carried to each non-reporting lender by its own, Mennwell made about 200 (121 rows) and Weyrauch State Bank about 260 (154 rows), while the strong analyst's pooled capture of 90 per cent still leaves Mennwell at about 130.

## Three rules

Task type: Survey Research & Official Statistics / census-register-administrative-data-quality, serving the ETL objective (the conformed lender table built from an administrative register and a second source).
Domain test: completing an administrative register that misses whole classes of producers by dual-system estimation against a second, incomplete source, within post-strata where that source's capture is homogeneous and after its erroneous enumerations, is official statistics' coverage-measurement method; with another field's nouns (a credit model's default rates, a pricing grid) there is no register coverage or capture to estimate, and the task stops reading the same.
Swap: put a credit-risk or pricing field's nouns in and nothing is missing from a register and captured by a second list; the deciding quantity (each lender's volume when HMDA omits it and the feed under-captures it) exists only as an admin-data coverage estimate.
Layer 1: two activity years of the HMDA public loan-level layout with every action and purpose and partial-exemption values; three recorder deliveries cut by recording date, the last in a renamed layout with ISO dates; mortgagee names as indexed (MERS nominee phrasing, truncation, abbreviations, city suffixes) resolved through an alias register; re-recordings, second mortgages and seller-carried notes in the purchase file; farmstead mortgages recorded in two counties; HMDA county codes taken from postal cities; the reporter panel, a lender register and the board's shortlist (inventory below).
Layer 2: the feed's capture is not one number; it is homogeneous only within recording routes, so it is estimated on the reporters within each route and carried to each non-reporting lender by its own route, after the erroneous enumerations leave both lists.
Decisive step: building each lender's recording route from the feed's paired recording dates (the mortgage recorded the same day as its deed, or later), and estimating the feed's capture within each route on the reporters before scaling the non-reporters by their own route's capture; nothing filed names the route or the capture.
Analyst test: a strong analyst who conforms the LAR and the feed, resolves the mortgagee names and removes the feed's non-purchase recordings measures the feed's capture against the reporters' HMDA counts and scales the non-reporters by it; the pooled capture (90 per cent) leaves Mennwell Credit Union at about 135, below Shunga Valley Bank's 151, because the route Mennwell records by is captured at 60 per cent.
Estimand: first-lien home-purchase mortgages each shortlisted lender made on homes in the eight counties, closed in 2024 and 2025, every lender counted whether or not it reports HMDA; the prompt states lender, product, place, period and the five-of-twelve cut, and the program guidelines define a home-purchase mortgage (7.3), a mortgage lender (7.2), an arm's-length sale (7.4) and when a mortgage is made (7.5).
No decoy: no filed rule, basis or metric gives the wrong five; the vendor's guide states what the file holds without a capture figure, and no document ranks the lenders.
Not semantics: no field, code, unit or definition read correctly reaches the golden; an analyst who reads every HMDA code, deed type and date field right and applies the guidelines' definitions still files the pooled capture's five (Mennwell Credit Union at about 135 against Shunga Valley Bank's 151), because the recording route is no field but a construction from two dates, and what the file's capture depends on is measured on the reporters, not read anywhere.
Not rule application: nothing filed says how a lender HMDA does not cover is counted, how the recorder file's capture is measured or what it is measured within; executing every filed rule (the prompt's estimand, guidelines 2.2, 6.1 and 7.1 to 7.5) leaves that open, and the default and pooled paths both execute every rule and file wrong fives.
No certified replay: no closed or certified figure blesses the pooled or unscaled method; the delivery register's row counts tie to the files under every handling.
Lesson: an administrative register's missing producers cannot be completed from a second list at that list's average capture when the producers the register misses are the ones the second list captures worst; the capture has to be stratified on its mechanism.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 HMDA only (the reporters on the shortlist) | the shortlist lists five lenders HMDA does not hold | no LEI with records for five lenders | yes | no | no | no | readable |
| R1 the feed's rows for the non-reporters, unscaled | the vendor's guide says the file holds matched mortgages | the feed holds them | yes | no | no | no | readable |
| R2 the feed's capture measured on the reporters, pooled | no | the reporters are in both | yes (compare sources) | no | no | one ratio | readable |
| R3 capture by county, by charter type or by year | no | county, charter and year are columns | yes (stratify on visible attributes) | no | no | no | readable |
| R4 capture by recording route, erroneous enumerations kept | no | no route column | no | no | no | no | silent |
| R5 (decisive) capture by recording route after the erroneous enumerations | no: no document names a route, a package or a capture | no column: the route is built from the paired recording dates | no: every visible stratifier lands wrong | no control scores a capture | the battery does not find it | no: a construction, then a stratified ratio | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | made | the lender named on the mortgage closed it; HMDA originations (action 1) for reporters | HMDA purchased loans (action 6) counted for the buyer | same call, same counts: no shortlisted lender buys loans (asserted) | the prompt's "made"; a purchased loan is another lender's origination |
| SF2 | closed in 2024 and 2025 | closing date (HMDA activity year; the feed's instrument date, DOC_DT in layout v4) | the feed's recording date | same five, same bins (asserted) | the prompt says "closed"; guidelines 7.5 |
| SF3 | first-lien home-purchase mortgage | a lender's first lien financing an arm's-length purchase, every buyer | second mortgages kept; quitclaim refinances into a trust kept; owner-occupants only for the reporters | seconds: same five, same bins; quitclaims: Heidebrecht in, Arkhaven out (R4); owner-occupants: same five (asserted) | the prompt says first-lien and home-purchase; guidelines 7.3 and 7.4 |
| SF4 | on homes in the eight counties | the home stands in one of the eight counties (2.2): the recording county, the county in which the property lies (the vendor's guide), for every lender; each reporter's eight-county total from HMDA, whose county is the institution's geocode of the address (the dictionary) | the lender's offices in the counties; the reporters counted from the recorder by route as well | same call, same counts (asserted: HMDA's geocoded codes move no loan into or out of the eight counties, and the recorder-based reporter counts keep the five and every bin) | the prompt says homes there; guidelines 2.2; the dictionary's county_code; the vendor's CNTY_FIPS |
| SF5 | lender | the legal entity on the shortlist, its indexed names and MERS nominee strings resolved through the alias register | MERS as the lender | MERS is not on the shortlist; every nominee row resolves (asserted) | the shortlist names the entities; the alias register carries their names |
| SF6 | a mortgage recorded in two counties | one mortgage, counted where the house stands | two | same five, same bins (asserted) | the prompt counts mortgages, not recordings |
| SF7 | rounding | each lender's two-year count from unrounded figures, rounded once to the nearest 10 | each year rounded, then summed | same call; every graded count sits 2 or more from a rounding edge (asserted) | the prompt asks for the two-year count rounded |
| SF8 | the order of the five | by the two-year count, largest first | alphabetical | the call is the set and the order; neighbours at least 1.11 apart (asserted) | the prompt asks for the five in that order |
| SF9 | the capture within a route | ratio of the route's feed rows to its HMDA counts, on every reporter | mean or median of the reporters' own ratios; only the shortlisted reporters; year by year | same five, same bins (asserted) | C1: the reporters' captures within a route are tight |
| SF10 | the program year | closings 1 July 2025 to 30 June 2026 | calendar 2025; recording dates | Ask A figures move; the main call does not (asserted) | the prompt names July 2025 to June 2026; guidelines 6.1 and 7.5 |

## Ladder

As built (`generator/checks.py` asserts every rung by name; `verify.py` recomputes the golden from the bundle alone).

| Rung | Method | Five recruited (two-year counts) | Dies to |
|---|---|---|---|
| R0 | the seven reporters from HMDA, the non-reporters left out | Corvane 311, Halverd 228, Arkhaven 182, Shunga Valley 151, Tessaline 141 | the shortlist: five lenders HMDA does not hold |
| R1 (default) | the non-reporters at their feed rows | Corvane 311, Halverd 228, Arkhaven 182, Weyrauch 154, Shunga Valley 151 | the reporters' own loans: the file holds 90 per cent of them |
| R2 | the non-reporters over the pooled capture (0.898) | Corvane, Halverd, Arkhaven, Weyrauch 171.5, Shunga Valley 151 (Mennwell 134.8) | the reporters' captures split into two tight groups |
| R3 | capture by charter type, county or year | the R1 five (Weyrauch 182.5 by charter, 172.3 by county, 171.5 by year) | each mixes the two groups |
| R4 | capture by recording route, quitclaim refinances kept | Corvane 311, Weyrauch 263.9, Halverd 228, Heidebrecht 202.4, Mennwell 200.7 | Heidebrecht's 43 quitclaim pairings are refinances (7.3, 7.4) |
| R5 (golden) | capture by recording route after the erroneous enumerations | Corvane 311, Weyrauch 257.8, Halverd 228, Mennwell 202.5, Arkhaven 182; Shunga Valley 151 sixth | none |

- **Separation.** R1 and R2 recruit the same wrong five through different counts (Mennwell at 121 and 135 against Shunga Valley's 151); R3 by charter recruits it in another order; R4 recruits Heidebrecht in place of Arkhaven; the golden adds Mennwell and drops Shunga Valley.
- **Margins (asserted).** Golden neighbours 1.207, 1.131, 1.126 and 1.113 apart; fifth over sixth 1.205 (182 against 151); sixth over seventh 1.071 (Tessaline 141); each wrong rung's intruder sits inside its five.
- **Worth.** The route strata move Mennwell from 134.8 (pooled) to 202.5 and Weyrauch from 171.5 to 257.8; removing the quitclaim refinances moves Heidebrecht from 202.4 to 137.2.
- **Grid.** Two corrections, route strata (S) and the erroneous enumerations out (E): S and E give the golden; S without E gives R4; E without S gives R2; neither gives the R2 five. Every cell missing S or E recruits a wrong five (asserted).
- **Dominance.** The routes' captures (0.967 and 0.597) differ by 0.369; the widest split any filed attribute gives (institution type) is 0.102.
- **Position.** On the default path Mennwell is ninth and Weyrauch fourth.
- **Captures.** The file holds 1,673 of the reporters' 1,731 mortgages recorded the same day as the deed and 236 of their 395 recorded after it; each lender records one way in 2024 and 2025 (asserted).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every first-lien home-purchase mortgage on a home in the eight counties closed in 2024 or 2025, by every lender, reporting HMDA or not | the prompt; 7.2 to 7.4; the estimand counts lenders HMDA omits |
| 2 | Unit of account | one mortgage (not a recording, not a parcel) | the prompt; SF6 asserted |
| 3 | Attribution window | closing date | SF2: the prompt's "closed" and 7.5; C1 on the recording date asserted |
| 4 | As-of dating | the shortlist and register as of the October 2026 pull | the export manifest's dates |
| 5 | Version basis | the 2025 loan-level file as published; the three Venridge deliveries, cut by recording date | the delivery register; a closing-date window reads the 2026 delivery too, and leaving it unread keeps the five and every bin (asserted) |
| 6 | Denominator | the route's reporters' HMDA counts under their feed rows | SF9, C1 across estimators |
| 7 | Weighting | ratio of totals within a route | SF9 C1 (per-lender captures tight) |
| 8 | Window length | two closing years for capture and counts | C1: year-by-year captures give the same five and bins (asserted) |
| 9 | Boundary inclusivity | 1 January 2024 to 31 December 2025 inclusive | C1: the recording-date window, which moves every edge case, keeps the bins (asserted) |
| 10 | Rounding path | each count from unrounded figures to the nearest 10 | the prompt; SF7 asserted |
| 11 | Tie-break | none needed | margins at least 1.11 (asserted) |
| 12 | Maturity and censoring | December 2025 closings recorded by February 2026 are in the 2026 delivery | C1: the deliveries run to August 2026 recordings |
| 13 | Order of operations | remove erroneous enumerations, collapse recordings, then estimate capture and scale | C4: R4 and the grid cells, each named |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | re-recordings and two-county recordings collapse to one mortgage | SF6 and the R2 items, asserted |
| 16 | Identity normalisation | mortgagee text to lenders through the alias register | every lender row resolves (asserted); semantics, never the stump |
| 17 | Netting against gross | none | not applicable; no offsets |
| 18 | Dimensional units | counts only | not applicable |
| 19 | Code and status semantics | HMDA action, purpose and lien codes; the feed's deed types | dictionary semantics; never the stump |
| 20 | Integerisation | estimates are not integers; rounded once | SF7 |
| 21 | Clause scope | the guidelines' definitions cover both sources | filed once in the program guidelines, section 7 |
| 22 | Forward window contents | the call is for 2027 recruitment on the two closed years; Ask A's program year is closed | not applicable; the decision uses closed years (retrospective reason: recruitment ranks lenders on their last two full years) |

## Literal reader

Executed word for word, the prompt fixes one quantity per shortlisted lender: first-lien home-purchase mortgages it made on homes in the eight counties, closed in 2024 and 2025, rounded to the nearest 10, with the five largest recruited in order. Nothing filed says how a lender HMDA does not cover is counted: that is HOW, and the records force it (the reporters' captures fall in two tight groups that only the recording route separates, and every visible stratifier mixes them), so only route-stratified capture after the erroneous enumerations reproduces each lender's volume. Every literal reading gives one figure per lender; the wrong fives come from easy methods on the same literal quantity, never from another reading.

## Oracles

None. No shipped figure ties to a lender's volume: the delivery register's row counts tie to the files under every handling, the vendor's guide carries no capture rate, the shortlist carries no volumes, and no published table reports the non-reporting lenders.

## Ask sheet

**Ask A: the program year by county.** Figures: first-lien home-purchase mortgages made on homes in Saline, McPherson, Dickinson and Marion counties each and in Rice, Ottawa, Ellsworth and Lincoln together from 1 July 2025 to 30 June 2026, and the eight counties' total (six, nearest 10; golden 710, 310, 190, 150, 240 and 1,610). H18 home: the construction on the program-year segment the board plans by. Use: the board's program-year budget by county. Construction: every recorded mortgage closed in the program year over the capture of the way it was recorded (HMDA has no closing dates, so the reporters' half-years come from the file too). Primary device: D2, a label stored before a silent switch: from 6 April 2026 the in-house lenders' closings are recorded with the deed, so their records carry the packaged route at 97 per cent capture; the route has to be read per record, not per lender (in the file, the in-house lenders' rows for 6 April to June run 2.05 times the same weeks of 2025, the title-company lenders' 0.92 times). Hazards: the 2026 delivery's renamed date columns. Path: the 2025 and 2026 deliveries, the 2024 delivery and the HMDA file for the captures, the alias register, the lender register, the program guidelines (seven files, eleven columns). Stops: the lender-level route carried into 2026 (every figure high, by 13 to 47 a county and 128 in all), pooled capture, the golden. Realism: county e-recording lets settlement agents submit a lender's mortgage with the deed, and lenders that mailed their own mortgages switch when their closings go through it.

**Ask B: the two years by county.** Figures: first-lien home-purchase mortgages made on homes in Saline, McPherson, Dickinson and Marion counties each and in the other four together, closed in 2024 and 2025 (five, nearest 10; golden 1,360, 580, 360, 270 and 440). H18 home: the decisive construction on the county segment the program's outreach is planned by. Use: where the recruited lenders' volume sits. Construction: each reporter's HMDA count spread over the counties its recorded mortgages stand in, every other lender's rows over its route's capture. Primary device: D9, an inconsistency only a cross-file cut shows: HMDA's county is the institution's geocode of the address (the dictionary), and the lenders' geocoding follows the home's postal city, so homes in Ottawa, Lincoln, Ellsworth, Dickinson and McPherson with a Salina address are coded to Saline and homes in Rice and Marion with a McPherson address to McPherson, while the recording county is the county in which the property lies (the vendor's guide) and guidelines 2.2 count a home where it stands (alone the HMDA codes miss all five figures). Secondary device: D6, a farmstead mortgage recorded in both counties it covers is two file rows and one loan, counted where the house stands (the land-only row carries no property address; alone it misses Dickinson and the other four). Hazards: re-recordings, MERS nominee strings, seller-carried notes (7.2). Path: the HMDA file, the three deliveries, the alias register, the lender register, the shortlist, the guidelines (eight files, twelve columns). Stops: HMDA county codes for the reporters (Saline 53 high, the other four 30 low), two-county rows counted twice, the golden. Realism: rural postal cities cross county lines across central Kansas, and a mortgage on land in two counties is recorded in both.

Main population zero-counts (asserted): no in-house lender's mortgage closing in 2024 or 2025 records with the deed; HMDA's postal-city county codes never move a loan into or out of the eight counties; two-county recordings collapse to one mortgage in the main count, and none belongs to a lender in the golden five or the sixth.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, six program-year figures | carries each lender's 2024 to 2025 route into 2026 and scales the switched lenders' April to June records at 60 per cent: 758, 324, 214, 177, 263 and 1,736 against 711, 311, 192, 152, 242 and 1,608 | miss |
| B, five two-year county figures | takes the reporters' county codes from HMDA and counts two-county recordings twice: 1,412, 597, 351, 253 and 412 against 1,359, 578, 362, 270 and 442 | miss |

Mirror leakage: 4 per cent (the mirror, stopping at the pooled capture, keeps no Ask A or Ask B figure; it keeps one chart criterion, the twelve-lender bar chart's layout, of about 15 ask-side criteria).

Pair ceiling: 32.5 (planning weights 38 / 7 / 55 with the five recruited lenders, their counts and the sixth as the main block and r = 5; the cracker keeps the main block and no ask figure, 38 + 7 + 0 = 45; the mirror keeps r, instruction-following and the chart layout, 5 + 7 + 55 x 1/15 = 15.7; (45 + 15.7) / 2 = 30.4, plus a margin of 2.1 for one chart criterion either response may keep).

Criteria: the call (the five in order), five counts, the sixth and its count, about four chart criteria, six Ask A figures, five Ask B figures and two files, about 26.

## Layer 1 inventory

Each item, the system that writes it, its file and its natural mishandling; the R2 block in `checks.py` asserts the golden method with the item mishandled.

| Item | System | File | Mishandled | Effect (asserted) |
|---|---|---|---|---|
| deliveries cut by recording date | the vendor's annual and year-to-date cuts | the three Venridge files | the 2026 delivery left unread for a 2024 to 2025 window | same five, same bins |
| layout v4 (renamed fields, ISO dates) | the vendor's September 2026 release | venridge_pmm_ks8_2026ytd.txt | stacked by position | covered by the row above |
| mortgagee names as indexed | the recorders' indexes (MERS nominee text, truncation at 80 characters, THE, city suffixes) | the Venridge files | matched on the legal name only | every row resolves through the alias register |
| re-recordings | the recorders (corrective re-recording) | the Venridge files | kept | same five, same bins |
| second mortgages against one deed | piggyback closings | the Venridge files | kept | same five, same bins |
| two-county farmsteads | the recorders of both counties | the Venridge files | counted twice | same five, same bins; Ask B (D6, ledgered) |
| seller-carried notes | title closings of seller-financed sales | the Venridge files | counted | main call untouched; Ask B moves (7.2) |
| HMDA county by postal city | lenders' geocoding of rural addresses | the HMDA file | taken for the county | eight-county totals untouched; Ask B (D9, ledgered) |
| partial exemption | small depositories' HMDA filings | the HMDA file | "Exempt" or 1111 read as a code | never touches action, purpose or lien |
| purchased loans | the aggregator's HMDA filing | the HMDA file | counted as made | same five, same bins |
| investor and second-home purchases | every lender's book | the HMDA file | dropped for the reporters | same five (7.3 counts every buyer) |
| consideration blank or nominal | Kansas non-disclosure | the Venridge files | read as a price | no figure uses a price |

The quitclaim refinances into family trusts are not in this table: removing them is the method's erroneous-enumeration step (the grid's E), and keeping them recruits R4's five.

## Pre-ship check

- **Three rules.** Domain: dual-system completion of a register that misses whole producers, the census-register task type's own coverage method (swap test in the Three rules section). Two layers: the inventory above (all of it what the agencies' and vendor's systems write) and the route-stratified capture. Decisive step analytical: the analyst who conforms everything and reads every rule lands on the pooled capture's five (R3a asserted on the clean truth).
- **Gates.** 15 files in 4 formats, the HMDA file at 62,167 rows, two distractors (the 2023 county summary and the homebuyer education completions) whose deletion moves nothing (asserted); 122 checks; `verify.py` PASS from the bundle alone; two builds byte-identical; `figures_check.py` exit 0.

## Leak check

- `leak.py` REVIEW, no LEAK (house and parcel numbers matching golden figures, lender names in the recorder rows, common words); the one LEAK on the first run was a generated buyer surname matching the author vocabulary, mapped to a neighbouring surname without spending a draw.
- Reader, one isolated pass on the stage 4 pack: questions 1 to 4 none; question 5 quotes the estimand (the prompt with guidelines 2.2, 7.3, 7.4 and 7.5), whose execution is the estimand, not another population; question 6 named the 7.3 to 7.5 filters and the date basis, each asserted neutral to the call, and never reached the capture step. Realism tells fixed in the generator: the oddest small-lender names, the alias register's review dates, the shortlist notes. Full read in `leak_check_report.md`.

## Determinism judge

- Pass 1 (2026-10-12): NOT_DETERMINISTIC scoped to Ask B (the two-year county figures), FIX_NOW; the main call, the order and counts, the program year and every other ask forced and reproduced; Gate G method_or_model_selection, analytical_non_defect (sole_data_defect flagged borderline: the recorder file's partial capture is the second source's coverage, the object the method estimates, not a planted defect); Gate H domain pass, layers pass, decisive step analytical. The fork: the dictionary called HMDA's county_code the property's county, so a literal reader kept HMDA's codes for the reporters (1,410, 590, 350, 250, 410). Fix in one pass: the dictionary now files HMDA's county as the institution's geocode of the address and the vendor's guide the recording county as the county in which the property lies, so 2.2 resolves to the recorder's county; SF4 restated to match; the 1,610 program-year total marked as rounded from the unrounded figures. `freeze.py` PASS (no frozen figure moved); 122 checks.

## Tried and rejected

- A bank's CRA officer picking a peer group (the seed's decision), drawn 2026-10-12: the guard's ban.org_family (financial_institution, task185) blocked it; the decision moved to a homeownership nonprofit recruiting participating lenders, which keeps the league table and needs the unregistered rural lenders even more.
- A committee as the deciding forum: ban.forum against task181 v4; the nonprofit's board decides.
- The prototype market (6,461 mortgages over two years in the eight counties): about twice what the counties' sales support; scaled to about 3,000, with the margins and devices kept.
- A parcel crosswalk to place two-county farmstead mortgages: the land-only record already carries no property address, so the crosswalk was one file with no work to do; dropped.
- Per-lender random capture: binomial noise left the reporters' captures inside a route too far apart for the mean and median of their ratios to share the golden's bins; capture is drawn systematically per lender, route and year, which a vendor's matching process does.
